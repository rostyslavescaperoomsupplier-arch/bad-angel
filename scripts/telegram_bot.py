#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram-bot do aktualizacji strony BAD ANGEL.

Uruchamiany co ~5 minut przez GitHub Actions (bot.yml). Pobiera nowe
wiadomości (getUpdates), wykonuje komendy, commituje zmiany i odpala
deploy (workflow_dispatch). Stan (offset, admini) w bot/state.json —
push z GITHUB_TOKEN nie wyzwala workflow deploy, więc deploy jest
wywoływany jawnie tylko gdy zmieniła się treść strony.

Komendy (RU, bo tak pisze właścicielka):
  фото <kategoria> — jako podpis zdjęcia: dodaje je do galerii
  отзывы <liczba>  — aktualizuje licznik opinii
  помощь / start   — instrukcja
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(ROOT, "bot", "state.json")
TOKEN = os.environ["TELEGRAM_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"
MAX_AGE = 2 * 3600  # ignoruj wiadomości starsze niż 2h (np. po przestoju)

# nazwa kategorii (ru/pl, małymi literami) -> slug galerii
CATEGORY_ALIASES = {
    "маникюр": "manicure", "manicure": "manicure", "ногти": "manicure",
    "педикюр": "pedicure", "pedicure": "pedicure",
    "ресницы": "rzesy", "rzesy": "rzesy", "рэсницы": "rzesy", "вии": "rzesy",
    "брови": "brwi", "brwi": "brwi",
    "массаж": "masaz", "masaz": "masaz", "масаж": "masaz",
    "депиляция": "depilacja", "depilacja": "depilacja", "депіляція": "depilacja",
    "спа": "spa", "spa": "spa",
    "шрамы": "blizny", "blizny": "blizny", "шрами": "blizny",
    "волосы": "wlosy", "wlosy": "wlosy", "косички": "wlosy", "волосся": "wlosy",
}
CATEGORY_LIST = "маникюр, педикюр, ресницы, брови, массаж, депиляция, спа, шрамы, волосы"

HELP = (
    "Привет! Я обновляю сайт badangelsalonpiękności.pl\n\n"
    "📸 <b>Добавить фото работы в галерею:</b>\n"
    "Пришли фото (можно несколько сразу), в подписи укажи категорию:\n"
    f"<i>{CATEGORY_LIST}</i>\n\n"
    "⭐ <b>Обновить число отзывов:</b>\n"
    "напиши: <code>отзывы 1300</code>\n\n"
    "Изменения появляются на сайте через 2-3 минуты после моего ответа. "
    "Я проверяю сообщения раз в 5 минут, так что ответ может прийти не сразу."
)


def api_call(method, **params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{API}/{method}", data=data)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def send(chat_id, text):
    api_call("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")


def download_photo(file_id, dest):
    info = api_call("getFile", file_id=file_id)
    path = info["result"]["file_path"]
    urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{TOKEN}/{path}", dest)


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"offset": 0, "admins": [], "last_album": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)


def resolve_category(text):
    return CATEGORY_ALIASES.get(text.strip().lower().lstrip("/#").strip())


def handle_reviews(arg, chat_id):
    m = re.search(r"\d{2,6}", arg)
    if not m:
        send(chat_id, "Напиши так: <code>отзывы 1300</code>")
        return False
    n = int(m.group())
    sd_path = os.path.join(ROOT, "site_data.json")
    with open(sd_path, encoding="utf-8") as f:
        sd = json.load(f)
    if sd.get("reviews") == n:
        send(chat_id, f"Число отзывов уже {n} — ничего не меняю.")
        return False
    sd["reviews"] = n
    with open(sd_path, "w", encoding="utf-8") as f:
        json.dump(sd, f, ensure_ascii=False, indent=2)
        f.write("\n")
    send(chat_id, f"✅ Число отзывов обновлено: {n}. Сайт обновится через пару минут.")
    return True


def handle_photo(msg, slug, chat_id):
    photo = max(msg["photo"], key=lambda p: p.get("file_size") or 0)
    gdir = os.path.join(ROOT, "assets", "gallery", slug)
    os.makedirs(gdir, exist_ok=True)
    dest = os.path.join(gdir, f"tg-{msg['message_id']}.jpg")
    download_photo(photo["file_id"], dest)
    return dest


def main():
    state = load_state()
    resp = api_call("getUpdates", offset=state["offset"], timeout=0)
    updates = resp.get("result", [])
    if not updates:
        return 0

    content_changed = False
    photo_count = {}   # chat_id -> {slug: n} dla zbiorczej odpowiedzi
    now = time.time()

    for upd in updates:
        state["offset"] = upd["update_id"] + 1
        msg = upd.get("message")
        if not msg or now - msg.get("date", 0) > MAX_AGE:
            continue
        user_id = msg["from"]["id"]
        chat_id = msg["chat"]["id"]
        text = (msg.get("text") or msg.get("caption") or "").strip()

        # pierwszy piszący zostaje adminem; reszta obcych — odmowa
        if not state["admins"]:
            state["admins"] = [user_id]
            send(chat_id, "Ты назначен администратором этого бота. 👑")
        if user_id not in state["admins"]:
            send(chat_id, f"⛔ Нет доступа. Твой ID: {user_id} — попроси администратора добавить тебя.")
            continue

        low = text.lower().lstrip("/")
        if "photo" in msg:
            slug = resolve_category(text) if text else None
            group = msg.get("media_group_id")
            if not slug and group and state["last_album"].get("id") == group:
                slug = state["last_album"]["slug"]  # album: podpis tylko przy 1. zdjęciu
            if not slug:
                send(chat_id, f"Не поняла категорию. Подпиши фото одним словом: {CATEGORY_LIST}")
                continue
            if group:
                state["last_album"] = {"id": group, "slug": slug}
            handle_photo(msg, slug, chat_id)
            content_changed = True
            photo_count.setdefault(chat_id, {})
            photo_count[chat_id][slug] = photo_count[chat_id].get(slug, 0) + 1
        elif low.startswith(("отзыв", "opinie")):
            content_changed |= handle_reviews(text, chat_id)
        elif low.startswith(("разрешить", "allow")):
            m = re.search(r"\d{5,}", text)
            if m:
                state["admins"].append(int(m.group()))
                send(chat_id, f"✅ Пользователь {m.group()} добавлен.")
            else:
                send(chat_id, "Напиши так: <code>разрешить 123456789</code>")
        else:
            send(chat_id, HELP)

    for chat_id, slugs in photo_count.items():
        det = ", ".join(f"{s}: +{n}" for s, n in slugs.items())
        send(chat_id, f"✅ Фото добавлены в галерею ({det}). Сайт обновится через пару минут.")

    save_state(state)

    if content_changed:
        subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], check=True, cwd=ROOT)
    return 1 if content_changed else 0


if __name__ == "__main__":
    changed = main()
    # wynik dla kroku workflow: czy trzeba commit+deploy treści
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
        f.write(f"content_changed={'true' if changed else 'false'}\n")
