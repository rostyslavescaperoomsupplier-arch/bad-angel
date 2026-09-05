#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synchronizacja opinii i oceny z profilu Booksy salonu.

Ocena i liczba opinii sa na stronie nie tylko ozdoba — ida do znacznikow
schema.org AggregateRating, wiec musza zgadzac sie z tym, co klient widzi
przy rezerwacji. Skrypt czyta publiczne API Booksy i:
  * porownuje ocene / liczbe opinii z site_data.json,
  * sprawdza, czy cytaty pokazywane na stronie (REVIEWS w i18n.py, kazdy
    z id opinii w Booksy) nadal tam sa — klient moze opinie skasowac,
  * zapisuje pobrane opinie do reviews_booksy.json, zeby bylo z czego
    wybrac nowe cytaty.

Uruchomienie:
    python3 sync_reviews.py          # tylko raport
    python3 sync_reviews.py --apply  # zapisuje ocene i liczbe do site_data.json

UWAGA: profil salonu to business 353903 (al. Wyzwolenia 5). Stare id 14573
to INNA firma ("Anastasiia", ul. Łokietka) — nie brac stamtad liczb.
"""
import json
import os
import sys
import urllib.error
import urllib.request

from i18n import REVIEWS

ROOT = os.path.dirname(os.path.abspath(__file__))
BUSINESS = 353903
API = f"https://pl.booksy.com/api/pl/2/customer_api/businesses/{BUSINESS}/reviews"
# Klucz publicznego frontu Booksy — ten sam, ktorego uzywa ich strona www.
API_KEY = "web-e3d812bf-d7a2-445d-ab38-55589ae6a121"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")


def fetch(per_page=20):
    req = urllib.request.Request(
        f"{API}?page=1&per_page={per_page}",
        headers={"User-Agent": UA, "Accept": "application/json",
                 "x-api-key": API_KEY, "x-fingerprint": "web",
                 "Accept-Language": "pl-PL"})
    try:
        raw = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        sys.exit(f"Booksy odpowiedzialo {e.code} — sprawdz API/klucz.")
    return json.loads(raw)


def main():
    apply = "--apply" in sys.argv
    data = fetch()
    reviews = data.get("reviews") or []
    count = data.get("reviews_count")
    rank = data.get("reviews_rank")
    if not count or rank is None:
        sys.exit("Brak oceny w odpowiedzi Booksy — format sie zmienil.")
    rating = f"{round(rank, 1):.1f}"

    print(f"Booksy (business {BUSINESS}): ocena {rating} z {count} opinii; "
          f"pobrano {len(reviews)} najnowszych.")
    per_rank = data.get("num_reviews_per_rank") or {}
    if per_rank:
        print("  rozklad ocen: " + ", ".join(f"{k}★={v}" for k, v in sorted(per_rank.items(), reverse=True)))

    with open(os.path.join(ROOT, "reviews_booksy.json"), "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=1)
    print("  pelna lista -> reviews_booksy.json")

    path = os.path.join(ROOT, "site_data.json")
    with open(path, encoding="utf-8") as f:
        site = json.load(f)

    changes = []
    if str(site.get("reviews")) != str(count):
        changes.append(("liczba opinii", site.get("reviews"), count))
        site["reviews"] = count
    if str(site.get("rating")) != rating:
        changes.append(("ocena", site.get("rating"), rating))
        site["rating"] = rating

    if changes:
        print("\nROZJAZD ZE STRONA:")
        for what, old, new in changes:
            print(f"  {what}: {old}  ->  {new}")
    else:
        print("\nOcena i liczba opinii na stronie sa aktualne.")

    # Cytaty na stronie: kazdy ma id opinii z Booksy. Jesli opinia zniknela,
    # nie mozemy jej dalej cytowac jako opinii z Booksy.
    live = {r["id"] for r in reviews}
    gone = [r for r in REVIEWS if r.get("id") and r["id"] not in live]
    if gone:
        print(f"\nCYTATY, KTORYCH NIE MA W POBRANEJ PARTII ({len(gone)}):")
        for r in gone:
            print(f"  [{r['id']}] {r['who']}: {r['text']['pl'][:60]}…")
        print("  (moga byc starsze niz pobrana partia — sprawdz, zanim skasujesz)")
    else:
        print("\nWszystkie cytaty ze strony nadal sa w Booksy.")

    if apply and changes:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(site, f, ensure_ascii=False, indent=1)
        print(f"\nZapisano do site_data.json. Uruchom teraz python3 build.py.")
    elif changes:
        print("\n(raport — uruchom z --apply, zeby zapisac)")


if __name__ == "__main__":
    main()
