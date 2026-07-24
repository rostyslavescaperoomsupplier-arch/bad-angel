/**
 * Telegram-webhook bot dla strony BAD ANGEL (Cloudflare Worker).
 *
 * Telegram -> webhook -> ten worker -> commit do GitHuba (contents API).
 * Push PAT-em wyzwala workflow deploy, który sam buduje stronę (build.py).
 *
 * Sekrety (wrangler secret put): TELEGRAM_TOKEN, GH_TOKEN, WEBHOOK_SECRET.
 * KV binding: STATE (admini, ostatni album).
 */

const REPO = "rostyslavescaperoomsupplier-arch/bad-angel";

const CATEGORY_ALIASES = {
  "маникюр": "manicure", "manicure": "manicure", "ногти": "manicure",
  "педикюр": "pedicure", "pedicure": "pedicure",
  "ресницы": "rzesy", "rzesy": "rzesy", "рэсницы": "rzesy", "вии": "rzesy",
  "брови": "brwi", "brwi": "brwi",
  "массаж": "masaz", "masaz": "masaz", "масаж": "masaz",
  "депиляция": "depilacja", "depilacja": "depilacja", "депіляція": "depilacja",
  "спа": "spa", "spa": "spa",
  "шрамы": "blizny", "blizny": "blizny", "шрами": "blizny",
  "волосы": "wlosy", "wlosy": "wlosy", "косички": "wlosy", "волосся": "wlosy",
};
const CATEGORY_LIST = "маникюр, педикюр, ресницы, брови, массаж, депиляция, спа, шрамы, волосы";

const HELP =
  "Привет! Я обновляю сайт badangelsalonpiękności.pl\n\n" +
  "📸 <b>Добавить фото работы в галерею:</b>\n" +
  "Пришли фото (можно несколько сразу), в подписи укажи категорию:\n" +
  `<i>${CATEGORY_LIST}</i>\n\n` +
  "⭐ <b>Обновить число отзывов:</b>\n" +
  "напиши: <code>отзывы 1300</code>\n\n" +
  "После моего ✅ сайт обновляется ещё около 2 минут.";

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("ok");
    if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET)
      return new Response("forbidden", { status: 403 });

    let update;
    try { update = await request.json(); } catch { return new Response("ok"); }
    const msg = update.message;
    if (!msg) return new Response("ok");

    try { await handleMessage(msg, env); }
    catch (e) {
      await send(env, msg.chat.id, "⚠️ Ошибка: " + e.message);
    }
    return new Response("ok"); // zawsze 200, żeby Telegram nie powtarzał update'u
  },
};

async function handleMessage(msg, env) {
  const userId = msg.from.id;
  const chatId = msg.chat.id;
  const text = (msg.text || msg.caption || "").trim();

  let admins = JSON.parse((await env.STATE.get("admins")) || "[]");
  if (admins.length === 0) {
    admins = [userId];
    await env.STATE.put("admins", JSON.stringify(admins));
    await send(env, chatId, "Ты назначен администратором этого бота. 👑");
  }
  if (!admins.includes(userId)) {
    await send(env, chatId, `⛔ Нет доступа. Твой ID: ${userId} — попроси администратора добавить тебя.`);
    return;
  }

  const low = text.toLowerCase().replace(/^\//, "");

  if (msg.photo) {
    await handlePhoto(msg, text, env, chatId);
  } else if (low.startsWith("отзыв") || low.startsWith("opinie")) {
    await handleReviews(text, env, chatId);
  } else if (low.startsWith("разрешить") || low.startsWith("allow")) {
    const m = text.match(/\d{5,}/);
    if (m) {
      admins.push(Number(m[0]));
      await env.STATE.put("admins", JSON.stringify(admins));
      await send(env, chatId, `✅ Пользователь ${m[0]} добавлен.`);
    } else {
      await send(env, chatId, "Напиши так: <code>разрешить 123456789</code>");
    }
  } else {
    await send(env, chatId, HELP);
  }
}

async function handlePhoto(msg, caption, env, chatId) {
  let slug = caption ? CATEGORY_ALIASES[caption.toLowerCase().replace(/^[/#]+/, "").trim()] : null;
  const group = msg.media_group_id;
  if (!slug && group) {
    // album: podpis ma tylko pierwsze zdjęcie — reszta bierze kategorię z KV
    for (let i = 0; i < 6 && !slug; i++) {
      slug = await env.STATE.get(`album:${group}`);
      if (!slug) await new Promise(r => setTimeout(r, 500));
    }
  }
  if (!slug) {
    await send(env, chatId, `Не поняла категорию. Подпиши фото одним словом: ${CATEGORY_LIST}`);
    return;
  }
  if (group) await env.STATE.put(`album:${group}`, slug, { expirationTtl: 3600 });

  const photo = msg.photo.reduce((a, b) => ((a.file_size || 0) > (b.file_size || 0) ? a : b));
  const info = await tg(env, "getFile", { file_id: photo.file_id });
  const fileResp = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_TOKEN}/${info.result.file_path}`);
  const bytes = new Uint8Array(await fileResp.arrayBuffer());

  let bin = "";
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK)
    bin += String.fromCharCode(...bytes.subarray(i, i + CHUNK));

  const path = `assets/gallery/${slug}/tg-${msg.message_id}.jpg`;
  await gh(env, `contents/${path}`, "PUT", {
    message: `Bot: nowe zdjęcie w galerii ${slug}`,
    content: btoa(bin),
  });
  await send(env, chatId, `✅ Фото добавлено в галерею «${slug}». Сайт обновится через ~2 минуты.`);
}

async function handleReviews(text, env, chatId) {
  const m = text.match(/\d{2,6}/);
  if (!m) {
    await send(env, chatId, "Напиши так: <code>отзывы 1300</code>");
    return;
  }
  const n = Number(m[0]);
  const cur = await gh(env, "contents/site_data.json", "GET");
  const data = JSON.parse(atob(cur.content));
  if (data.reviews === n) {
    await send(env, chatId, `Число отзывов уже ${n} — ничего не меняю.`);
    return;
  }
  data.reviews = n;
  await gh(env, "contents/site_data.json", "PUT", {
    message: `Bot: liczba opinii ${n}`,
    content: btoa(JSON.stringify(data, null, 2) + "\n"),
    sha: cur.sha,
  });
  await send(env, chatId, `✅ Число отзывов обновлено: ${n}. Сайт обновится через ~2 минуты.`);
}

async function tg(env, method, params) {
  const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  const j = await r.json();
  if (!j.ok) throw new Error(`Telegram ${method}: ${j.description}`);
  return j;
}

async function send(env, chatId, text) {
  await tg(env, "sendMessage", { chat_id: chatId, text, parse_mode: "HTML" });
}

async function gh(env, path, method, body) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/${path}`, {
    method,
    headers: {
      "Authorization": `Bearer ${env.GH_TOKEN}`,
      "User-Agent": "badangel-bot",
      "Accept": "application/vnd.github+json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`GitHub ${method} ${path}: ${r.status} ${(await r.text()).slice(0, 200)}`);
  return r.json();
}
