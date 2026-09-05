#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synchronizacja cennika w site_data.json z profilem Booksy.

Booksy jest zrodlem prawdy dla cen — tam klient rezerwuje i tam widzi kwote.
Skrypt czyta payload __NUXT_DATA__ z publicznego profilu, dopasowuje pozycje
po nazwie i:
  * aktualizuje ceny tam, gdzie sie rozjechaly,
  * wypisuje pozycje z Booksy, ktorych nie ma na stronie,
  * wypisuje pozycje ze strony, ktorych nie ma w Booksy (np. depilacja —
    salon ja robi, ale nie wystawia online; tych NIE kasujemy automatycznie).

Uruchomienie:
    python3 sync_booksy.py          # tylko raport
    python3 sync_booksy.py --apply  # zapisuje nowe ceny do site_data.json
"""
import difflib
import json
import os
import re
import sys
import unicodedata
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PROFILE = ("https://booksy.com/pl-pl/353903_salon-urody-bad-angel"
           "_salon-kosmetyczny_18078_szczecin")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")


def norm(s):
    """Wspolna postac nazwy: bez ogonkow, bez interpunkcji, bez przyimkow.

    Booksy i strona zapisuja to samo inaczej ("z zwyklym" / "ze zwyklym",
    "posladki" / "posladkow", zdarza sie tez literowka "Rredukcja"), wiec
    dokladne porownanie nie wystarcza — reszte zalatwia dopasowanie rozmyte.
    """
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9:]+", " ", s)
    stop = {"z", "ze", "w", "i", "na", "do", "dla"}
    return " ".join(w for w in s.split() if w not in stop)


def best_match(key, pool, cutoff=0.84):
    """Nazwa z Booksy najblizsza podanej albo None."""
    hit = difflib.get_close_matches(key, pool, n=1, cutoff=cutoff)
    return hit[0] if hit else None


def money(v):
    """'1 099,00 zł' -> '1099 zł';  '130,00 zł' -> '130 zł'."""
    if not v:
        return None
    if "darmow" in v.lower():
        return "Darmowa"
    n = re.sub(r"[^\d,]", "", v).replace(",", ".")
    try:
        f = float(n)
    except ValueError:
        return None
    return f"{int(f)} zł" if f == int(f) else f"{f:.2f} zł"


def fetch_booksy():
    req = urllib.request.Request(PROFILE, headers={
        "User-Agent": UA, "Accept-Language": "pl-PL,pl;q=0.9"})
    html = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
    m = re.search(r'id="__NUXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        sys.exit("Nie znalazlem __NUXT_DATA__ — Booksy zmienilo strone.")
    data = json.loads(m.group(1))

    def deref(i, d=0):
        if d > 14:
            return None
        v = data[i] if isinstance(i, int) and 0 <= i < len(data) else i
        if isinstance(v, list):
            return [deref(x, d + 1) for x in v]
        if isinstance(v, dict):
            return {k: deref(x, d + 1) for k, x in v.items()}
        return v

    out = {}
    for i, v in enumerate(data):
        if not (isinstance(v, dict) and "name" in v and "services" in v):
            continue
        for s in (deref(i).get("services") or []):
            if not isinstance(s, dict):
                continue
            vs = [x for x in (s.get("variants") or []) if isinstance(x, dict)]
            # cena bazowa = wariant bez etykiety; reszta to dodatki i warianty
            base = next((x for x in vs if not (x.get("label") or "").strip()), None)
            price = money((base or {}).get("servicePrice") or s.get("servicePrice"))
            if price:
                out.setdefault(norm(s["name"]), (s["name"], price, False))
            for x in vs:
                lab = (x.get("label") or "").strip()
                p = money(x.get("servicePrice"))
                if lab and p:
                    # dodatek do uslugi ("Frencz", "Spa dla rak"), nie osobna
                    # pozycja — nie zglaszamy go jako brakujacego na stronie
                    out.setdefault(norm(lab), (lab, p, True))
    return out


def main():
    apply = "--apply" in sys.argv
    booksy = fetch_booksy()
    print(f"Booksy: {len(booksy)} pozycji\n")

    path = os.path.join(ROOT, "site_data.json")
    with open(path, encoding="utf-8") as f:
        site = json.load(f)

    changed, matched = [], set()
    for cat, items in site["services"].items():
        for it in items:
            key = norm(it[0])
            hit = booksy.get(key)
            if not hit:
                near = best_match(key, list(booksy))
                if near:
                    matched.add(near)  # ta sama usluga, inny zapis — bez zmiany ceny
                continue
            matched.add(key)
            if hit[1] != it[3].replace("\xa0", " ").strip():
                changed.append((cat, it[0], it[3], hit[1]))
                it[3] = hit[1]

    if changed:
        print("ROZJECHANE CENY (Booksy wygrywa):")
        for cat, name, old, new in changed:
            print(f"  [{cat}] {name}: {old}  ->  {new}")
    else:
        print("Wszystkie dopasowane ceny sie zgadzaja.")

    missing = [v for k, v in booksy.items() if k not in matched and not v[2]]
    if missing:
        print(f"\nJEST W BOOKSY, NIE MA NA STRONIE ({len(missing)}):")
        for name, price, _ in sorted(missing):
            print(f"  {price:>10}  {name}")

    on_site = {norm(it[0]) for items in site["services"].values() for it in items}
    only_site = sorted(it[0] for items in site["services"].values() for it in items
                       if norm(it[0]) not in booksy
                       and not best_match(norm(it[0]), list(booksy)))
    if only_site:
        print(f"\nJEST NA STRONIE, NIE MA W BOOKSY ({len(only_site)}) — "
              f"nie kasujemy, salon moze to robic poza rezerwacja online:")
        for n in only_site:
            print(f"  {n}")

    if apply and changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(site, f, ensure_ascii=False, indent=1)
        print(f"\nZapisano {len(changed)} zmian do site_data.json.")
    elif changed:
        print("\n(raport — uruchom z --apply, zeby zapisac)")


if __name__ == "__main__":
    main()
