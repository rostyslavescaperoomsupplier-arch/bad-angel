#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator statycznej strony Salon Urody BAD ANGEL.
Tworzy: styles.css, index.html, strony usług (usluga-*.html),
strony mastrów (mistrz-*.html) oraz README z listą potrzebnych zdjęć.
Rezerwacja każdej usługi prowadzi na Booksy.
"""
import os
import re
import glob
import json
from datetime import date
from i18n import LANGS, LANG_LABEL, HTML_KEYS, REVIEWS, flat as _i18n_flat
from seo_content import SEO as CAT_SEO
from landing_content import LANDINGS

_ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_ROOT, "site_data.json"), encoding="utf-8") as _f:
    SITE_DATA = json.load(_f)
REVIEWS_COUNT = str(SITE_DATA["reviews"])
# Ocena i liczba opinii pochodza z profilu Booksy salonu (business 353903) i
# trafiaja tu przez sync_reviews.py. Nigdy nie wpisujemy ich na sztywno: te
# same liczby ida do znacznikow AggregateRating, a Google karze rozjazd miedzy
# tym, co deklaruje strona, a tym, co widzi klient przy rezerwacji.
RATING = str(SITE_DATA.get("rating", ""))
# Gwiazdki przy ocenie ogolnej rysujemy z tej samej liczby. Piec pelnych
# gwiazdek obok "4.4" to obietnica, ktorej dane nie potwierdzaja — zaokraglamy
# do najblizszej pelnej, tak jak robi to Booksy.
STARS = ("★" * round(float(RATING)) + "☆" * (5 - round(float(RATING)))) if RATING else "★★★★★"

def _fill_rating(obj):
    """{RATING} w tekstach landingow — ta sama liczba co w reszcie serwisu."""
    if isinstance(obj, str):
        return obj.replace("{RATING}", RATING).replace("{REVIEWS}", REVIEWS_COUNT)
    if isinstance(obj, list):
        return [_fill_rating(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _fill_rating(v) for k, v in obj.items()}
    return obj


LANDINGS = _fill_rating(LANDINGS)

I18N = _i18n_flat()
for _key, _langs in I18N.items():
    for _lang, _text in _langs.items():
        if isinstance(_text, str):
            _langs[_lang] = (_text.replace("{REVIEWS}", REVIEWS_COUNT)
                                  .replace("{RATING}", RATING))

# Jezyk aktualnie generowanej strony. Polski jest jezykiem glownym: lezy
# w korzeniu (te same nazwy plikow co dotad, zeby nie stracic zaindeksowanych
# adresow), reszta w /uk/, /ru/, /en/.
CUR = "pl"
OG_LOCALE = {"pl": "pl_PL", "uk": "uk_UA", "ru": "ru_RU", "en": "en_US"}


def P(key):
    """Tekst w jezyku aktualnie budowanej strony (z fallbackiem na polski)."""
    e = I18N.get(key)
    if not e:
        return ""
    return e.get(CUR) or e.get("pl", "")


def T(d):
    """Tekst z gotowego slownika {pl,uk,ru,en} w jezyku budowanej strony.

    Dluzsze akapity SEO nie ida do translations.js — kazdy jezyk ma wlasny
    URL, wiec nie ma czego podmieniac w przegladarce, a plik JS zostaje maly.
    """
    return d.get(CUR) or d.get("pl", "")


def U(page=""):
    """Adres strony w aktualnym jezyku, np. U('portfolio.html') -> /uk/portfolio.html"""
    return ("/" if CUR == "pl" else f"/{CUR}/") + page


def U_lang(lang, page=""):
    return ("/" if lang == "pl" else f"/{lang}/") + page


def A(path):
    """Zasoby sa wspolne dla wszystkich jezykow, wiec zawsze absolutnie."""
    return "/" + path.lstrip("/")

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = "16"  # cache-busting wersja dla styles.css / translations.js / app.js
BOOKSY = "https://badangel86.booksy.com/a/"
# Numer telefonu — mocny sygnal lokalny (NAP) dla Google. Uzupelnic!
PHONE = ""
IG = "https://www.instagram.com/badangel_wyzwolenia"
FB = "https://www.facebook.com/"

# Domena własna: badangelsalonpiękności.pl (punycode dla DNS/GitHub Pages).
DOMAIN = "xn--badangelsalonpiknoci-iwc96l.pl"
SITE_URL = f"https://{DOMAIN}" if DOMAIN else "https://rostyslavescaperoomsupplier-arch.github.io/bad-angel"
OG_IMAGE = f"{SITE_URL}/assets/feature-nails.jpg"

# ---------------------------------------------------------------------------
# DANE
# ---------------------------------------------------------------------------

# Kategorie usług. slug -> plik usluga-<slug>.html, zdjęcie assets/usluga-<slug>.jpg
CATEGORIES = [
    dict(slug="manicure", name="Manicure", tag="Dłonie",
         lead="Precyzyjne dłonie na każdą okazję",
         intro="Manicure klasyczny, hybrydowy i japoński oraz przedłużanie żelem w każdej długości. "
               "Dbałość o skórki, trwałość koloru i wykończenie dopracowane w detalu.",
         items=[
             ("Manicure klasyczny", "Opiłowanie, odsunięcie i usunięcie skórek, emulsja zmiękczająca.", "1 g", "od 90 zł"),
             ("Manicure + lakier", "Obrobienie skórek, baza i lakier hybrydowy.", "1 g 30 min", "od 99 zł"),
             ("Manicure higieniczny", "", "1 g 30 min", "99 zł"),
             ("Manicure męski", "", "1 g 30 min", "99 zł"),
             ("Manicure japoński", "Pielęgnacja odżywcza pastą i pudrem.", "1 g 30 min", "108 zł"),
             ("Manicure hybryda", "Opracowanie skórek, skrócenie paznokci, odżywka proteinowa.", "1 g 30 min", "od 117 zł"),
             ("Manicure hybrydowy", "", "2 g", "60 zł"),
             ("Żel na naturalną płytkę", "Wzmocnienie i wyrównanie naturalnej płytki żelem.", "2 g 30 min", "80 zł"),
             ("Odnowa żelowa długość 1/2", "", "2 g", "od 135 zł"),
             ("Odnowa żelowa długość 3/4", "Skórki, utwardzenie żelowe, lakier hybrydowy.", "2 g 30 min", "od 153 zł"),
             ("Przedłużanie paznokci długość 1", "Utwardzenie żelem i lakier hybrydowy.", "1 g 30 min", "od 153 zł"),
             ("Przedłużenie paznokci długość 2/3", "", "2 g", "171 zł"),
             ("Przedłużenie paznokci długość 3/4", "", "2 g 30 min", "180 zł"),
             ("Przedłużenie paznokci długość 4/5", "", "3 g", "189 zł"),
             ("Rekonstrukcja jednego paznokcia", "Piłowanie, utwardzanie, polerowanie, lakier hybrydowy.", "15 min", "od 9 zł"),
         ]),
    dict(slug="pedicure", name="Pedicure", tag="Stopy",
         lead="Zadbane stopy od pierwszego kroku",
         intro="Opracowanie stóp i paznokci w komfortowej atmosferze. "
               "Od klasyki po pełny zabieg hybrydowy z pielęgnacją pięt.",
         items=[
             ("Pedicure klasyczny z obramieniem skórek", "Opracowanie palców i skórek.", "1 g", "od 99 zł"),
             ("Pedicure męski", "", "1 g", "108 zł"),
             ("Pedicure z lakierem klasycznym", "", "1 g 20 min", "od 108 zł"),
             ("Pedicure hybrydowy (bez pięt)", "", "1 g 20 min", "od 135 zł"),
             ("Pedicure hybrydowy ze stopą", "Pełne opracowanie z pielęgnacją pięt.", "1 g 30 min", "od 153 zł"),
             ("Pedicure higieniczny", "", "1 g", "50 zł"),
             ("Pedicure hybrydowy z opracowaniem stopy", "", "2 g 30 min", "120 zł"),
             ("Pedicure hybryda (bez stóp)", "", "2 g 30 min", "100 zł"),
         ]),
    dict(slug="rzesy", name="Przedłużanie rzęs", tag="Spojrzenie",
         lead="Spojrzenie, które przyciąga uwagę",
         intro="Przedłużanie rzęs w objętościach od 1:1 do 5:1. "
               "Naturalny lub wyrazisty efekt dobrany do kształtu oka.",
         items=[
             ("Metoda 1:1", "Efekt naturalny.", "1 g 50 min", "135 zł"),
             ("Metoda 2:1", "", "2 g", "144 zł"),
             ("Metoda 3:1", "", "2 g 15 min", "153 zł"),
             ("Metoda 4:1", "", "2 g 30 min", "od 162 zł"),
             ("Metoda 5:1", "Efekt maksymalnej objętości.", "2 g 30 min", "171 zł"),
             ("Uzupełnienie 1:1 (do 3 tygodni)", "", "1 g 50 min", "126 zł"),
             ("Ściągnięcie rzęs (bez założenia)", "", "15 min", "od 36 zł"),
         ]),
    dict(slug="brwi", name="Brwi i rzęsy", tag="Brwi & Laminacja",
         lead="Naturalna oprawa oka",
         intro="Regulacja, geometria i koloryzacja brwi henną pudrową oraz laminacja z botoksem. "
               "Podkreślamy urodę, dbając o kondycję włosków.",
         items=[
             ("Regulacja brwi + geometria", "Wosk lub pęseta, korekta kształtu.", "20 min", "od 45 zł"),
             ("Regulacja brwi + geometria + farbka", "Henna marokańska / pudrowa.", "45 min", "od 72 zł"),
             ("Korekta brwi (bez farbowania)", "Geometria bez regulacji.", "25 min", "od 45 zł"),
             ("Laminacja brwi + botox", "", "1 g", "od 90 zł"),
             ("Laminacja brwi + botox + koloryzacja", "Stylizacja i regeneracja włosków.", "1 g", "od 117 zł"),
             ("Laminacja rzęs", "", "1 g 30 min", "144 zł"),
         ]),
    dict(slug="masaz", name="Masaż", tag="Ciało & Relaks",
         lead="Chwila wytchnienia dla ciała",
         intro="Masaże relaksacyjne, lecznicze i pielęgnacyjne. "
               "Od kręgosłupa po twarz, dopasowane do Twoich potrzeb.",
         items=[
             ("Masaż kręgosłupa (kobiety)", "", "30 min", "72 zł"),
             ("Masaż kręgosłupa (mężczyźni)", "", "45 min", "117 zł"),
             ("Masaż całego ciała (kobiety)", "", "1 g 30 min", "162 zł"),
             ("Masaż całego ciała (mężczyźni)", "", "1 g 30 min", "207 zł"),
             ("Masaż miodem", "Detoksykacja i ujędrnienie.", "30 min", "117 zł"),
             ("Masaż twarzy + peeling + maska + krem", "", "50 min", "144 zł"),
             ("Masaż antycellulitowy", "", "1 g", "162 zł"),
             ("Masaż karku, głowy i szyi", "", "30 min", "72 zł"),
             ("Masaż stóp", "", "20 min", "72 zł"),
             ("Masaż rąk", "", "20 min", "72 zł"),
             ("Masaż twarzy", "", "30 min", "81 zł"),
         ]),
    dict(slug="spa", name="Parafina & SPA dłoni", tag="Pielęgnacja",
         lead="Regeneracja dla zmęczonych dłoni",
         intro="Zabiegi parafinowe i SPA głęboko nawilżają, wygładzają i poprawiają krążenie. "
               "Idealne dla suchej, zmęczonej skóry dłoni.",
         items=[
             ("SPA parafinowe po innej usłudze", "Kąpiel parafinowa i krem regenerujący.", "30 min", "od 72 zł"),
             ("SPA (peeling, parafina, masaż, krem)", "Pełny rytuał pielęgnacyjny dłoni.", "50 min", "od 90 zł"),
         ]),
    dict(slug="blizny", name="Blizny i rozstępy", tag="Zabiegi specjalne",
         lead="Skóra gładsza po zabiegu",
         intro="Profesjonalna redukcja blizn i rozstępów. "
               "Zauważalny efekt już po pierwszym zabiegu, dobierany indywidualnie.",
         items=[
             ("Redukcja blizn do 5 cm", "", "45 min", "359,10 zł"),
             ("Redukcja blizn do 10 cm", "", "1 g", "449,10 zł"),
             ("Redukcja blizn większych", "", "1 g 30 min", "539,10 zł"),
             ("Redukcja rozstępów biustu", "", "45 min", "449,10 zł"),
             ("Redukcja rozstępów pośladki", "", "1 g 30 min", "490,50 zł"),
             ("Redukcja rozstępów ręce", "", "1 g", "494,10 zł"),
             ("Redukcja rozstępów uda", "", "1 g 10 min", "584,10 zł"),
             ("Redukcja rozstępów boki", "", "1 g 30 min", "629,10 zł"),
             ("Redukcja rozstępów brzucha", "", "1 g 30 min", "670,50 zł"),
             ("Redukcja rozstępów brzuch + boki", "", "2 g 30 min", "989,10 zł"),
         ]),
    dict(slug="wlosy", name="Warkoczyki", tag="Włosy",
         lead="Fryzura na kilka tygodni, która nie wymaga codziennego układania",
         intro="Warkoczyki z kanekalonem, afrykańskie box braids i warkocze bąbelkowe — "
               "od pojedynczego warkoczyka po całą głowę.",
         items=[
             ("Pojedynczy warkoczyk z kanekalonem", "", "1 g", "150 zł"),
             ("Dwa warkoczyki z kanekalonem", "", "2 g", "200 zł"),
             ("Warkoczyki z kanekalonem – cała głowa", "", "4 g", "350 zł"),
             ("Afrykańskie warkoczyki (box braids)", "", "5 g 30 min", "350 zł"),
             ("Bąbelkowe warkocze z kanekalonem", "", "1 g 30 min", "220 zł"),
         ]),
]

# Cennik jest edytowalny przez bota Telegram: site_data.json["services"] nadpisuje
# inline'owe items (te wyżej to tylko wartości startowe / fallback).
for _c in CATEGORIES:
    if _c["slug"] in SITE_DATA.get("services", {}):
        _c["items"] = [tuple(_i) for _i in SITE_DATA["services"][_c["slug"]]]

def _masters_from_site_data():
    out = []
    for m in SITE_DATA["masters"]:
        m = dict(m)
        m.setdefault("gen", m["name"])
        m.setdefault("bio", [])
        m.setdefault("serves", [])
        m.setdefault("works", "")
        out.append(m)
    return out

# Mastrzy. slug -> mistrz-<slug>.html, zdjęcie assets/mistrz-<slug>.jpg
MASTERS = [
    dict(slug="weronika", name="Weronika", gen="Weroniki", role="Manicure, pedicure, brwi, SPA i depilacja",
         serves=["manicure", "pedicure", "brwi", "spa"],
         bio=[
             "Mistrzyni manicure i pedicure oraz stylistka brwi. Stawia na estetyczny, naturalny "
             "efekt i komfort podczas każdej wizyty. Wykonuje także zabiegi SPA dłoni i depilację.",
             "Manicure i pedicure wykonuje od dwóch lat, a od roku zajmuje się laminacją i "
             "koloryzacją brwi — z dbałością o detal i kondycję włosków.",
             "Do każdej klientki podchodzi indywidualnie, dobierając pielęgnację i stylizację do "
             "jej potrzeb.",
         ]),
    dict(slug="wiktoria", name="Wiktoria", gen="Wiktorii", role="Mikroneedling, blizny i warkoczyki",
         serves=["blizny", "wlosy"],
         bio=[
             "Specjalistka mikroneedlingu po szkoleniach w Akademii LIBRO w Warszawie. Skupia się "
             "na terapii regeneracyjnej blizn, rozstępów, śladów po trądziku i przebarwień oraz "
             "poprawie jakości i gęstości skóry.",
             "Posiada międzynarodową akredytację KCCK z wyróżnieniem oraz certyfikat Global "
             "Creative Masters. Stale podnosi kwalifikacje — m.in. egzosomy i polinukleotydy w mikroneedlingu.",
             "Każdy etap zabiegu dokładnie wyjaśnia, a efekty jej pracy widoczne są już po "
             "pierwszej wizycie.",
             "Oprócz zabiegów na skórę wykonuje także efektowne warkoczyki — od pojedynczych "
             "po pełne stylizacje.",
         ]),
    dict(slug="fabian", name="Fabian", gen="Fabiana", role="Fizjoterapeuta, masażysta",
         serves=["masaz"], bio=[]),
    dict(slug="emilia", name="Emilia", gen="Emilii", role="Stylizacja paznokci, brwi i rzęs",
         serves=["manicure", "pedicure", "brwi", "rzesy"], bio=[]),
    dict(slug="elena", name="Elena", gen="Eleny", role="Stylistka przedłużania rzęs",
         serves=["rzesy"], bio=[]),
]

# Mistrzynie też edytowalne przez bota: site_data.json["masters"] nadpisuje listę wyżej.
if "masters" in SITE_DATA:
    MASTERS = _masters_from_site_data()

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """
:root{
  /* Neutrale ciepłe, dobrane pod złoty wordmark — czyste #fff na #000 czytało się
     jak dowolny ciemny szablon i wychłodzało logo. */
  --black:#08080a;--ink-2:#0e0e11;--white:#f4f1ea;--grey:#8d8880;
  --gold:#c2a066;--line:rgba(244,241,234,.11);
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  --serif:'Cormorant Garamond',Georgia,serif;
  /* jedna skala odstępów — sekcje wcześniej miały przypadkowe wartości */
  --sp-1:8px;--sp-2:16px;--sp-3:28px;--sp-4:48px;--sp-5:80px;--sp-6:120px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--white);background:#000;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}

/* NAV */
/* Bez mix-blend-mode: difference — nad jasnym zdjęciem odwracał kolory, linki
   robiły się cyjanowe a wordmark praktycznie znikał. Zamiast tego stały scrim. */
header{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;
  padding:18px 28px;transition:background .4s,box-shadow .4s;color:var(--white)}
header::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(180deg,rgba(6,6,8,.72),rgba(6,6,8,.28) 62%,transparent);transition:opacity .4s}
header.solid::before{opacity:0}
header.solid{background:rgba(8,8,10,.86);backdrop-filter:blur(12px);box-shadow:0 1px 0 var(--line)}
header .brand{font-family:var(--serif);font-size:22px;letter-spacing:.32em;font-weight:500;padding-left:.32em}
header nav{display:flex;gap:30px}
header nav a{font-size:13px;font-weight:500;letter-spacing:.02em;padding:6px 4px;opacity:.95;transition:opacity .2s}
header nav a:hover{opacity:.6}
.nav-cta{display:flex;gap:14px;align-items:center}
.lang-switch{display:flex;align-items:center;gap:2px}
/* Przelacznik to teraz linki (kazdy jezyk ma wlasny URL), a nie <button>. */
.lang-switch a{display:inline-block;color:currentColor;text-decoration:none;
  font-family:var(--sans);font-size:12px;font-weight:500;letter-spacing:.12em;padding:5px 7px;
  opacity:.42;transition:opacity .2s;line-height:1}
.lang-switch a:hover{opacity:.8}
.lang-switch a.active{opacity:1;text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.drawer .lang-switch{margin-top:28px;gap:10px;justify-content:flex-start}
.drawer .lang-switch a{font-size:15px;letter-spacing:.14em;padding:8px 12px;border:1px solid var(--line);border-radius:40px;opacity:.6}
.drawer .lang-switch a.active{opacity:1;text-decoration:none;background:var(--white);color:#111;border-color:var(--white)}
.burger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:0}
.burger span{width:22px;height:2px;background:currentColor;display:block}
.drawer{position:fixed;inset:0;z-index:200;background:rgba(10,10,10,.97);backdrop-filter:blur(8px);
  display:flex;flex-direction:column;padding:80px 28px 40px;transform:translateX(100%);
  transition:transform .45s cubic-bezier(.6,0,.2,1)}
.drawer.open{transform:translateX(0)}
.drawer a{font-size:20px;font-weight:500;padding:16px 0;border-bottom:1px solid var(--line)}
.drawer .close{position:absolute;top:22px;right:26px;font-size:30px;line-height:1;cursor:pointer;background:none;border:0;color:#fff}

.btn{display:inline-block;min-width:264px;padding:13px 24px;border-radius:4px;font-size:13px;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;transition:all .25s;cursor:pointer;text-align:center;backdrop-filter:blur(4px)}
.btn.solid{background:rgba(244,241,234,.94);color:#111}
.btn.solid:hover{background:#fff}
/* Ghost nad ścianą zdjęć: .5 alfa nie wystarczało, tekst gubił się na jaśniejszym kadrze. */
.btn.ghost{background:rgba(14,14,17,.72);color:var(--white);border:1px solid var(--line)}
.btn.ghost:hover{background:rgba(30,30,34,.85);border-color:rgba(244,241,234,.24)}
.btn.sm{min-width:auto;padding:9px 20px}
.btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;padding:0 20px}

.eyebrow{font-size:12px;letter-spacing:.36em;text-transform:uppercase;opacity:.72;margin-bottom:20px}
.wrap{max-width:1200px;margin:0 auto}
.stars{color:#e9c46a;letter-spacing:2px}

/* HERO (home) */
.panel{position:relative;min-height:100vh;display:flex;flex-direction:column;align-items:center;text-align:center;overflow:hidden}
.panel .bg{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center}
#hero .bg{background:radial-gradient(120% 90% at 50% 0%,#2a2a2e 0%,#141416 45%,#000 100%)}
#hero .bg::after{content:"";position:absolute;inset:0;
  background:radial-gradient(60% 55% at 50% 42%,rgba(190,195,205,.16),transparent 60%),
  radial-gradient(40% 40% at 72% 60%,rgba(150,160,180,.10),transparent 70%)}
#hero.has-photo .bg{background:none}
#hero .photo{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center}
#hero .scrim{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,.25) 40%,rgba(0,0,0,.75))}
.monogram{font-family:var(--serif);font-size:clamp(140px,34vw,420px);line-height:.8;font-weight:300;letter-spacing:-.04em;
  background:linear-gradient(180deg,#eef1f6,#aeb4c0 40%,#6a6f7a 60%,#e6e9ef);-webkit-background-clip:text;background-clip:text;color:transparent;
  opacity:.9;position:absolute;top:50%;left:50%;transform:translate(-50%,-52%);z-index:-1;filter:drop-shadow(0 8px 40px rgba(0,0,0,.6));pointer-events:none}
#hero.has-photo .monogram{display:none}
#hero .logo{width:min(680px,86vw);margin:0 auto;filter:drop-shadow(0 6px 30px rgba(0,0,0,.5))}

/* ŚCIANA PRAC — sygnaturowy element strony głównej.
   Zamiast pustego czarnego gradientu tłem hero są prawdziwe zdjęcia z salonu:
   trzy kolumny przesuwające się w różnym tempie. Tylko desktop — na telefonie
   zostaje lekki gradient, żeby nie psuć LCP. */
#hero .wall{position:absolute;inset:-10% -2%;z-index:-3;display:none;grid-template-columns:repeat(5,1fr);gap:8px}
#hero .wall .col{display:flex;flex-direction:column;gap:8px;will-change:transform;animation:wallDrift 78s linear infinite}
#hero .wall .col:nth-child(2){animation-duration:104s;animation-direction:reverse}
#hero .wall .col:nth-child(3){animation-duration:88s}
#hero .wall .col:nth-child(4){animation-duration:118s;animation-direction:reverse}
#hero .wall .col:nth-child(5){animation-duration:94s}
#hero .wall img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:2px;filter:grayscale(.18) contrast(1.03)}
@keyframes wallDrift{from{transform:translateY(0)}to{transform:translateY(-50%)}}
#hero.has-wall .wall{display:grid}
/* Scrim: najciemniej w środku, pod wordmarkiem — na brzegach prace zostają widoczne.
   Odwrotnie niż intuicja podpowiada; jaśniejszy środek zabijał czytelność logo. */
#hero.has-wall .bg{background:
  radial-gradient(52% 42% at 50% 47%,rgba(8,8,10,.97) 0%,rgba(8,8,10,.93) 52%,rgba(8,8,10,.5) 100%),
  radial-gradient(120% 100% at 50% 50%,transparent 40%,rgba(8,8,10,.55) 100%),
  linear-gradient(180deg,rgba(8,8,10,.92) 0%,rgba(8,8,10,.34) 30%,rgba(8,8,10,.34) 68%,rgba(8,8,10,.96) 100%)}
#hero.has-wall .bg::after{content:none}
@media (min-width:1500px){#hero .wall{grid-template-columns:repeat(6,1fr)}}
@media (max-width:1100px){#hero .wall{grid-template-columns:repeat(4,1fr)}}
/* Telefon: ściana zostaje, ale w dwóch kolumnach. Kolumny 3-5 są display:none,
   więc przeglądarka nie ściąga ich zdjęć (obrazki mają loading=lazy) — na
   telefonie dociąga się 8 miniatur zamiast 20. */
@media (max-width:860px){
  #hero .wall{grid-template-columns:repeat(2,1fr);gap:6px;inset:-6% -4%}
  #hero .wall .col:nth-child(n+3){display:none}
  #hero.has-wall .bg{background:
    radial-gradient(64% 34% at 50% 44%,rgba(8,8,10,.96) 0%,rgba(8,8,10,.9) 60%,rgba(8,8,10,.62) 100%),
    linear-gradient(180deg,rgba(8,8,10,.94) 0%,rgba(8,8,10,.5) 26%,rgba(8,8,10,.5) 62%,rgba(8,8,10,.97) 100%)}
}

/* Jeden wyśrodkowany stos zamiast top/bottom — wcześniej logo trzymało się góry,
   przyciski dna, a między nimi zostawało ~450px pustki. */
.panel{justify-content:center;gap:0}
.panel .top{padding-top:96px}
.panel .bottom{padding-top:var(--sp-4);padding-bottom:0;width:100%}
#hero .cue{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);display:flex;flex-direction:column;
  align-items:center;gap:8px;font-size:10px;letter-spacing:.34em;text-transform:uppercase;color:var(--grey)}
#hero .cue i{display:block;width:1px;height:42px;background:linear-gradient(180deg,var(--gold),transparent);animation:cueDrop 2.6s ease-in-out infinite}
@keyframes cueDrop{0%,100%{opacity:.25;transform:scaleY(.6)}50%{opacity:1;transform:scaleY(1)}}
.panel h1{font-family:var(--serif);font-size:clamp(48px,9vw,104px);font-weight:400;letter-spacing:.02em;line-height:1.02}
#hero .rating{margin-top:14px;font-size:14px;letter-spacing:.06em;opacity:.9}

/* SECTION headers */
.section-head{text-align:center;margin-bottom:var(--sp-5)}
.section-head h2{font-family:var(--serif);font-size:clamp(36px,5vw,60px);font-weight:400;letter-spacing:-.01em}
/* Złota kreska pod nagłówkiem sekcji — jedyny powtarzalny element strukturalny,
   ten sam akcent co w wordmarku. */
.section-head h2::after{content:"";display:block;width:34px;height:1px;background:var(--gold);
  margin:20px auto 0;opacity:.85}
.section-head p{margin-top:18px;color:var(--grey);font-weight:300;letter-spacing:.03em}
section.block{padding:var(--sp-6) 24px}

/* SERVICE CARDS (photo) — 9 kategorii, więc 3 kolumny dają pełne 3x3.
   Przy 4 kolumnach ostatnia karta zostawała sama w rzędzie. */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
/* Karta bez ramki i bez zaokrągleń: zdjęcie ma być kartą, a nie zawartością
   pudełka. Podpis trzyma się zdjęcia cienką złotą kreską. */
.card{display:flex;flex-direction:column;overflow:hidden;background:var(--ink-2);
  transition:transform .35s cubic-bezier(.2,.7,.3,1);text-decoration:none;position:relative}
.card::after{content:"";position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 0 0 1px var(--line);transition:box-shadow .35s}
.card:hover{transform:translateY(-5px)}
.card:hover::after{box-shadow:inset 0 0 0 1px rgba(194,160,102,.5)}
.card .thumb{aspect-ratio:4/5;background-size:cover;background-position:center;transition:filter .35s}
.card:hover .thumb{filter:brightness(1.06)}
.card .cap{padding:20px 20px 22px;position:relative}
.card .cap::before{content:"";position:absolute;top:0;left:20px;width:26px;height:1px;background:var(--gold);opacity:.8}
.card h3{font-family:var(--serif);font-size:25px;font-weight:400;letter-spacing:.005em}
.card .price{font-size:13px;color:var(--gold);margin-top:6px;letter-spacing:.05em}
.card .go{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--white);
  margin-top:14px;opacity:.5;transition:opacity .3s}
.card:hover .go{opacity:1}

/* SPLIT */
.split{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;min-height:90vh}
.split .media{background-size:cover;background-position:center;min-height:60vh}
.split .body{display:flex;flex-direction:column;justify-content:center;padding:8vw;background:#0b0b0c}
.split .body h2{font-family:var(--serif);font-size:clamp(34px,4.4vw,56px);font-weight:400;line-height:1.05}
.split .body p{margin-top:20px;color:#b9b9bf;font-weight:300;line-height:1.7;font-size:15px}
.split .body .btns{justify-content:flex-start;padding:0;margin-top:34px}

/* TEAM */
.team{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:60px}
.member{text-align:center;text-decoration:none;display:block;transition:transform .3s}
.member:hover{transform:translateY(-4px)}
.member .ph{aspect-ratio:3/4;border-radius:8px;background-size:cover;background-position:center;
  background-color:#16161a;border:1px solid var(--line);position:relative}
.member .ph::after{content:attr(data-i);position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-family:var(--serif);font-size:64px;color:#33333b;z-index:-1}
.member h4{font-family:var(--serif);font-size:24px;font-weight:400;margin-top:18px}
.member span{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey)}

/* REVIEWS */
.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:56px}
.review{border:1px solid var(--line);border-radius:6px;padding:32px;background:#0d0d0f}
.review p{margin-top:16px;font-weight:300;line-height:1.6;color:#cfcfd4;font-size:15px}
.review .who{margin-top:22px;font-size:13px;color:var(--grey)}
.review .who b{color:#fff;font-weight:500}

/* CONTACT */
.contact-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:60px;margin-top:56px;align-items:start}
.info-row{padding:22px 0;border-bottom:1px solid var(--line)}
.info-row .k{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#5f5f66}
.info-row .v{font-size:17px;font-weight:300;margin-top:8px;line-height:1.5}
.map{aspect-ratio:1/1;border-radius:8px;overflow:hidden;border:1px solid var(--line);filter:grayscale(1) contrast(1.05) brightness(.85);transition:filter .4s}
.map:hover{filter:grayscale(0)}
.map iframe{width:100%;height:100%;border:0}

/* SUBPAGE HERO */
.subhero{position:relative;min-height:64vh;display:flex;align-items:flex-end;overflow:hidden}
.subhero .bg{position:absolute;inset:0;z-index:-2;background-size:cover;background-position:center}
.subhero .scrim{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.8))}
.subhero .inner{padding:0 24px 60px;max-width:1200px;margin:0 auto;width:100%}
.subhero .eyebrow{margin-bottom:14px}
.subhero h1{font-family:var(--serif);font-size:clamp(40px,7vw,84px);font-weight:400;line-height:1}
.subhero .lead{margin-top:16px;font-size:18px;font-weight:300;color:#cfcfd4;max-width:640px}
.crumbs{position:absolute;top:96px;left:24px;z-index:2;font-size:12px;letter-spacing:.1em;color:#cfcfd4}
.crumbs a{opacity:.8}.crumbs a:hover{opacity:1;text-decoration:underline}

/* PRICE LIST */
.intro-band{padding:80px 24px;text-align:center;background:#0b0b0c}
.intro-band p{max-width:720px;margin:0 auto;font-size:19px;font-weight:300;line-height:1.7;color:#cbcbd1}
.pricelist{max-width:900px;margin:0 auto;padding:20px 24px 100px}
.price-item{display:flex;align-items:center;gap:24px;padding:26px 0;border-bottom:1px solid var(--line)}
.price-item .txt{flex:1;min-width:0}
.price-item h3{font-family:var(--serif);font-size:23px;font-weight:400}
.price-item .desc{color:var(--grey);font-weight:300;font-size:14px;margin-top:6px;line-height:1.5}
.price-item .dur{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#5f5f66;margin-top:8px}
.price-item .amt{font-family:var(--serif);font-size:24px;white-space:nowrap}
.price-item .book{white-space:nowrap}

/* GALLERY */
.gallery{padding:20px 24px 40px;max-width:1240px;margin:0 auto}
.gallery .cols{column-count:4;column-gap:14px}
.gallery img{width:100%;height:auto;margin:0 0 14px;border-radius:8px;display:block;break-inside:avoid;
  border:1px solid var(--line);transition:opacity .3s}
.gallery img:hover{opacity:.85}
@media(max-width:1000px){.gallery .cols{column-count:3}}
@media(max-width:680px){.gallery .cols{column-count:2}}

/* MASTER PAGE */
.master{display:grid;grid-template-columns:1fr 1fr;gap:64px;max-width:1100px;margin:0 auto;padding:120px 24px;align-items:start}
.master .portrait{aspect-ratio:3/4;border-radius:10px;background-size:cover;background-position:center;background-color:#16161a;border:1px solid var(--line);position:sticky;top:110px}
.master .role{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--grey)}
.master h1{font-family:var(--serif);font-size:clamp(44px,6vw,72px);font-weight:400;margin:12px 0 28px}
.master .bio p{color:#c4c4ca;font-weight:300;line-height:1.8;font-size:16px;margin-bottom:18px}
.master .serves{margin-top:36px}
.master .serves .k{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#5f5f66;margin-bottom:16px}
.chip{display:inline-block;border:1px solid var(--line);border-radius:40px;padding:9px 18px;font-size:13px;margin:0 8px 8px 0;transition:all .25s}
.chip:hover{background:#fff;color:#111;border-color:#fff}

/* FOOTER */
footer{background:#000;padding:50px 24px;text-align:center;border-top:1px solid var(--line)}
footer .brand{font-family:var(--serif);font-size:20px;letter-spacing:.3em;padding-left:.3em}
footer .soc{display:flex;gap:26px;justify-content:center;margin:24px 0;font-size:13px;letter-spacing:.08em}
footer .soc a{color:var(--grey)}footer .soc a:hover{color:#fff}
footer small{color:#4a4a50;font-size:12px}

@media(max-width:900px){
  header nav{display:none}
  header .nav-cta .btn{display:none}
  header .brand{font-size:18px;letter-spacing:.24em}
  .burger{display:flex}
  .grid{grid-template-columns:repeat(2,1fr)}
  .team{grid-template-columns:repeat(2,1fr)}
  .reviews{grid-template-columns:1fr}
  .split{grid-template-columns:1fr}
  .contact-grid{grid-template-columns:1fr;gap:40px}
  .master{grid-template-columns:1fr;gap:32px}
  .master .portrait{position:relative;top:0;max-width:420px}
  .btn{min-width:min(88vw,320px)}
  .price-item{flex-wrap:wrap;gap:12px}
  .price-item .amt{font-size:20px}
}
@media(max-width:560px){
  /* Wcześniej 1 kolumna: 9 usług = ponad 6 ekranów przewijania, zanim
     zobaczysz ostatnią. Dwie kolumny z niższą kartą mieszczą je w trzech. */
  .grid{grid-template-columns:repeat(2,1fr);gap:12px}
  .card .thumb{aspect-ratio:1/1}
  .card .cap{padding:12px 12px 14px}
  .card .cap::before{left:12px;width:20px}
  .card h3{font-size:19px}
  .card .price{font-size:12px;margin-top:4px}
  /* Cała karta jest linkiem, a w dwóch kolumnach ten podpis łamał się na dwie
     linijki i tylko zagęszczał kadr. */
  .card .go{display:none}
  .team{grid-template-columns:1fr 1fr}
  .price-item .book{width:100%}
  .price-item .book .btn{width:100%}
  section.block{padding:var(--sp-5) 16px}
  .section-head{margin-bottom:var(--sp-4)}
  .panel .top{padding-top:76px}
}

/* ---- REVEAL (animacje scrollem) ---- */
.reveal{transition:opacity .7s ease,transform .7s ease}
.js .reveal{opacity:0;transform:translateY(26px)}
.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
  .js .reveal{opacity:1;transform:none;transition:none}
  #hero .wall .col,#hero .cue i{animation:none}
}

/* ---- FOKUS KLAWIATURY ----
   Nic wcześniej nie pokazywało, gdzie jest fokus przy nawigacji tabem. */
:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:2px}
.btn:focus-visible,.card:focus-visible,.member:focus-visible{outline-offset:4px}

/* ---- BACK TO TOP + MOBILE CTA ---- */
.to-top{position:fixed;right:20px;bottom:20px;z-index:90;width:46px;height:46px;border-radius:50%;
  background:rgba(20,20,22,.82);backdrop-filter:blur(8px);border:1px solid var(--line);color:#fff;cursor:pointer;
  display:flex;align-items:center;justify-content:center;font-size:20px;opacity:0;pointer-events:none;transition:opacity .3s}
.to-top.show{opacity:1;pointer-events:auto}
.to-top:hover{background:rgba(45,45,50,.92)}
.mcta{position:fixed;left:0;right:0;bottom:0;z-index:95;display:none;padding:11px 14px;
  background:rgba(8,8,9,.94);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
.mcta .btn{display:block;min-width:0;width:100%}
/* Pasek wchodzi dopiero za hero (klasa past-hero z app.js) i wjeżdża z dołu. */
.mcta{transform:translateY(110%);transition:transform .32s cubic-bezier(.2,.7,.3,1)}
body.past-hero .mcta{transform:none}
@media(max-width:760px){.mcta{display:block}.to-top{bottom:78px;right:16px}}
@media(prefers-reduced-motion:reduce){.mcta{transition:none}}

/* ---- OPEN NOW BADGE ---- */
.open-badge{display:inline-flex;align-items:center;gap:9px;font-size:13px;letter-spacing:.03em;margin-top:14px;
  padding:7px 14px;border-radius:40px;border:1px solid var(--line);color:#dcdce0}
.open-badge::before{content:"";width:8px;height:8px;border-radius:50%;background:#888}
.open-badge.open::before{background:#48c774;box-shadow:0 0 0 3px rgba(72,199,116,.22)}
.open-badge.closed::before{background:#e06060}

/* ---- FAQ ---- */
.svc-seo{background:#0e0e10}
.prose{max-width:820px;margin:34px auto 0}
.prose p{color:#b9b9bf;font-weight:300;line-height:1.8;font-size:16px;margin:0 0 20px}
.prose p:last-child{margin-bottom:0}
.rel-block{background:#0b0b0c;padding-bottom:70px}
.rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:34px}
@media(max-width:760px){.rel-grid{grid-template-columns:1fr}}
.rel-card{display:block;padding:22px 24px;border:1px solid var(--line);border-radius:2px;
  text-decoration:none;transition:border-color .3s,background .3s}
.rel-card:hover{border-color:var(--gold);background:#121214}
.rel-n{display:block;font-family:var(--serif);font-size:19px;color:#fff;margin-bottom:6px}
.rel-d{display:block;font-size:13px;color:#8a8a91;font-weight:300;line-height:1.6}
.faq{max-width:820px;margin:52px auto 0}
.faq-item{border-bottom:1px solid var(--line)}
.faq-q{width:100%;text-align:left;background:none;border:0;color:#fff;font-family:var(--serif);font-size:clamp(19px,2.4vw,23px);
  font-weight:400;padding:24px 42px 24px 0;cursor:pointer;position:relative}
.faq-q::after{content:"+";position:absolute;right:4px;top:50%;transform:translateY(-50%);font-family:var(--sans);
  font-size:24px;font-weight:300;color:var(--grey);transition:transform .3s}
.faq-item.open .faq-q::after{content:"−"}
.faq-a{max-height:0;overflow:hidden;transition:max-height .4s ease}
.faq-a p{color:#b9b9bf;font-weight:300;line-height:1.7;font-size:15px;padding:0 0 24px;margin:0}

/* ---- GIFT CARDS ---- */
.gift-wrap{max-width:1040px;margin:0 auto;display:grid;grid-template-columns:1.05fr .95fr;
  border:1px solid var(--line);border-radius:14px;overflow:hidden}
.gift-body{padding:clamp(36px,5vw,60px);background:#0d0d0f}
.gift-body h2{font-family:var(--serif);font-size:clamp(30px,4vw,48px);font-weight:400}
.gift-body p{margin:18px 0 32px;color:#b9b9bf;font-weight:300;line-height:1.7;font-size:16px}
.gift-art{background:url('/assets/emblem.png') center/58% no-repeat, radial-gradient(120% 120% at 30% 20%,#241d14,#0a0a0c);
  min-height:240px}
@media(max-width:760px){.gift-wrap{grid-template-columns:1fr}.gift-art{min-height:170px}}

/* ---- SHARE ---- */
.share-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:34px}
.share-row a,.share-row button{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;border-radius:40px;
  border:1px solid var(--line);background:rgba(20,20,22,.5);color:#fff;font-size:14px;font-weight:500;cursor:pointer;
  font-family:var(--sans);transition:all .2s;letter-spacing:.02em}
.share-row a:hover,.share-row button:hover{background:#fff;color:#111;border-color:#fff}
.share-row svg{width:17px;height:17px;fill:currentColor;flex:none}

/* ---- LIGHTBOX ---- */
.gallery img{cursor:zoom-in}
.lb{position:fixed;inset:0;z-index:300;background:rgba(0,0,0,.93);display:none;align-items:center;justify-content:center}
.lb.open{display:flex}
.lb img{max-width:92vw;max-height:86vh;border-radius:6px;box-shadow:0 20px 70px rgba(0,0,0,.7)}
.lb button{position:absolute;background:none;border:0;color:#fff;cursor:pointer;line-height:1}
.lb .lb-close{top:18px;right:24px;font-size:36px}
.lb .lb-nav{top:50%;transform:translateY(-50%);font-size:46px;padding:12px 20px;opacity:.65}
.lb .lb-nav:hover{opacity:1}
.lb .lb-prev{left:6px}.lb .lb-next{right:6px}
@media(max-width:600px){.lb .lb-nav{font-size:34px;padding:8px 12px}}

/* ---- KALKULATOR ---- */
#kalk{padding:130px 24px 170px;background:#0b0b0c;min-height:100vh}
.calc{max-width:900px;margin:44px auto 0}
.calc-cat{margin-bottom:14px;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#0d0d0f}
.calc-cat>summary{list-style:none;cursor:pointer;padding:20px 24px;font-family:var(--serif);font-size:23px;font-weight:400;
  display:flex;justify-content:space-between;align-items:center}
.calc-cat>summary::-webkit-details-marker{display:none}
.calc-cat>summary::after{content:"+";color:var(--grey);font-size:22px;font-family:var(--sans)}
.calc-cat[open]>summary::after{content:"−"}
.calc-row{display:flex;align-items:center;gap:15px;padding:15px 24px;border-top:1px solid var(--line);cursor:pointer}
.calc-row:hover{background:#141417}
.calc-row input{width:18px;height:18px;accent-color:#fff;cursor:pointer;flex:none}
.calc-row .cn{flex:1;font-weight:300;font-size:15px}
.calc-row .cp{font-family:var(--serif);font-size:18px;white-space:nowrap;color:#dcdce0}
.calc-note{max-width:900px;margin:22px auto 0;color:#5f5f66;font-size:13px;text-align:center;line-height:1.6}
.calc-bar{position:fixed;left:0;right:0;bottom:0;z-index:95;background:rgba(8,8,9,.96);backdrop-filter:blur(12px);
  border-top:1px solid var(--line);padding:15px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.calc-bar .sum{font-family:var(--serif);font-size:27px;line-height:1.1}
.calc-bar .sum small{display:block;font-family:var(--sans);font-size:11px;color:var(--grey);letter-spacing:.14em;text-transform:uppercase}
.calc-bar .cta{display:flex;gap:10px;align-items:center;flex:none}
.calc-bar .clear{background:none;border:0;color:var(--grey);cursor:pointer;font-size:13px;font-family:var(--sans);text-decoration:underline;text-underline-offset:3px}
@media(max-width:620px){.calc-bar{flex-wrap:wrap;justify-content:center;text-align:center;gap:10px}.calc-bar .sum{width:100%}}
.calc-bar ~ .mcta{display:none !important}

/* ---- PORTFOLIO FILTER ---- */
.filters{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:40px auto 8px;max-width:900px}
.filters button{appearance:none;background:transparent;border:1px solid var(--line);border-radius:40px;color:#cfcfd4;
  font-family:var(--sans);font-size:13px;letter-spacing:.03em;padding:9px 18px;cursor:pointer;transition:all .2s}
.filters button:hover{border-color:rgba(255,255,255,.4)}
.filters button.active{background:#fff;color:#111;border-color:#fff}
.gallery img.hide{display:none}

/* ---- BEFORE / AFTER SLIDER ---- */
/* Dwa zabiegi obok siebie: laminacja brwi i mikroneedling. */
.ba-pair{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:44px;align-items:start}
.ba-item{margin:0}
.ba-item figcaption{margin-top:14px;text-align:center;font-size:12px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gold);opacity:.9}
@media(max-width:860px){.ba-pair{grid-template-columns:1fr;gap:34px}}
.ba{max-width:720px;margin:0 auto;position:relative;aspect-ratio:4/3;border-radius:2px;overflow:hidden;
  border:1px solid var(--line);user-select:none;touch-action:none;cursor:ew-resize}
.ba .ba-img{position:absolute;inset:0;background-size:cover;background-position:center}
.ba .ba-after{clip-path:inset(0 0 0 50%)}
.ba .ba-line{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff;transform:translateX(-1px);box-shadow:0 0 12px rgba(0,0,0,.5)}
.ba .ba-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;
  background:rgba(255,255,255,.95);display:flex;align-items:center;justify-content:center;color:#111;font-size:15px;box-shadow:0 4px 16px rgba(0,0,0,.4)}
.ba .ba-tag{position:absolute;bottom:14px;font-size:11px;letter-spacing:.16em;font-weight:600;color:#fff;
  background:rgba(0,0,0,.5);padding:5px 11px;border-radius:40px;backdrop-filter:blur(4px)}
.ba .ba-tag.l{left:14px}.ba .ba-tag.r{right:14px}

/* ---- WYSZUKIWARKA CENNIKA ---- */
.s-open{background:none;border:0;color:currentColor;cursor:pointer;padding:6px;display:flex;
  align-items:center;opacity:.7;transition:opacity .2s}
.s-open:hover{opacity:1}
.drawer a[data-search-open]{color:var(--gold)}
.s-box{position:fixed;inset:0;z-index:300;display:none;background:rgba(4,4,6,.82);
  backdrop-filter:blur(6px);padding:12vh 20px 20px}
.s-box.on{display:block}
body.search-open{overflow:hidden}
.s-panel{max-width:660px;margin:0 auto;background:var(--ink-2);border:1px solid var(--line);
  border-radius:3px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.s-head{display:flex;align-items:center;gap:12px;padding:16px 18px;border-bottom:1px solid var(--line);color:var(--grey)}
.s-head input{flex:1;background:none;border:0;outline:none;color:var(--white);font-family:var(--sans);
  font-size:17px;letter-spacing:.01em;min-width:0}
.s-head input::placeholder{color:var(--grey)}
.s-head input::-webkit-search-cancel-button{display:none}
.s-close{background:none;border:0;color:var(--grey);font-size:26px;line-height:1;cursor:pointer;padding:0 2px}
.s-close:hover{color:var(--white)}
.s-out{max-height:52vh;overflow-y:auto}
.s-row{display:grid;grid-template-columns:1fr auto auto;gap:6px 16px;align-items:baseline;
  padding:13px 18px;border-bottom:1px solid var(--line);transition:background .2s}
.s-row:hover{background:rgba(244,241,234,.05)}
/* Pozycje w siatce ustawione wprost — bez tego cena wskakiwala w pierwsza
   kolumne i wypychala nazwe uslugi na prawo. */
.s-name{grid-column:1;grid-row:1;color:var(--white);font-size:15px}
.s-cat{grid-column:1;grid-row:2;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--grey)}
.s-dur{grid-column:2;grid-row:1;font-size:12px;color:var(--grey);white-space:nowrap}
.s-price{grid-column:3;grid-row:1;color:var(--gold);font-size:14px;white-space:nowrap}
.s-none,.s-hint{padding:16px 18px;color:var(--grey);font-size:12.5px;line-height:1.5}
.s-hint{border-top:1px solid var(--line)}
.s-box.has-results .s-hint{display:none}
@media(max-width:560px){.s-box{padding:8vh 12px 12px}.s-row{padding:12px 14px}}
"""

# ---------------------------------------------------------------------------
# SZABLONY
# ---------------------------------------------------------------------------
_FONT_CSS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500"
             "&family=Inter:wght@300;400;500;600&display=swap")
# Arkusz z Google Fonts blokowal pierwsze malowanie strony (LCP). Ladujemy go
# asynchronicznie: media="print" -> przegladarka nie czeka, onload wlacza go dla ekranu.
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         f'<link rel="stylesheet" href="{_FONT_CSS}" media="print"'
         ' onload="this.media=\'all\'">'
         f'<noscript><link rel="stylesheet" href="{_FONT_CSS}"></noscript>')


SALON_ID = SITE_URL + "/#salon"


def salon_ld(rating=False):
    d = {
        "@context": "https://schema.org", "@type": "BeautySalon",
        "@id": SALON_ID, "name": "Salon Urody BAD ANGEL",
        "alternateName": ["BAD ANGEL Szczecin", "Salon Urody BAD ANGEL Szczecin"],
        "url": SITE_URL + "/",
        "image": f"{SITE_URL}/assets/feature-nails.jpg",
        "logo": f"{SITE_URL}/assets/emblem.png",
        "address": {"@type": "PostalAddress", "streetAddress": "aleja Wyzwolenia 5/10",
                    "postalCode": "70-552", "addressLocality": "Szczecin",
                    "addressRegion": "zachodniopomorskie", "addressCountry": "PL"},
        "geo": {"@type": "GeoCoordinates", "latitude": 53.4337, "longitude": 14.5518},
        "hasMap": "https://www.google.com/maps/search/?api=1&query="
                  "Salon+Urody+BAD+ANGEL+aleja+Wyzwolenia+5%2F10+Szczecin",
        "areaServed": [{"@type": "City", "name": "Szczecin"},
                       {"@type": "AdministrativeArea", "name": "województwo zachodniopomorskie"}],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "09:00", "closes": "20:00"}],
        "priceRange": "50-600 PLN",
        "currenciesAccepted": "PLN",
        "paymentAccepted": "Gotówka, karta płatnicza",
        "availableLanguage": [{"@type": "Language", "name": n} for n in
                              ("Polski", "Українська", "Русский", "English")],
        "knowsAbout": [c["name"] for c in CATEGORIES],
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {
                "@type": "Service", "name": f"{c['name']} Szczecin",
                "url": f"{SITE_URL}/usluga-{c['slug']}.html"}}
            for c in CATEGORIES],
        "sameAs": [BOOKSY],
        "potentialAction": {"@type": "ReserveAction", "target": BOOKSY,
                            "name": "Rezerwacja online"},
    }
    if PHONE:
        d["telephone"] = PHONE
    if rating:
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": RATING,
                                "reviewCount": REVIEWS_COUNT, "bestRating": "5"}
    return d


def head(title, desc, page="", extra="", alt_langs=True, canonical=None):
    canonical = canonical or (SITE_URL + U(page))
    # hreflang dla wszystkich wersji + x-default na polska (jezyk glowny).
    # Strony jednojezyczne (landingi na polskie frazy) daja alt_langs=False.
    if alt_langs:
        alts = "".join(
            f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{U_lang(l, page)}">\n'
            for l in LANGS)
        alts += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{U_lang("pl", page)}">'
    else:
        alts = '<link rel="alternate" hreflang="pl" href="' + canonical + '">'
    return f"""<!DOCTYPE html>
<html lang="{CUR}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alts}
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#08080a">
<meta name="geo.region" content="PL-ZP">
<meta name="geo.placename" content="Szczecin">
<meta name="geo.position" content="53.4337;14.5518">
<meta name="ICBM" content="53.4337, 14.5518">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Salon Urody BAD ANGEL">
<meta property="og:locale" content="{OG_LOCALE[CUR]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{A('assets/favicon-32.png')}">
<link rel="apple-touch-icon" href="{A('assets/apple-touch-icon.png')}">
{FONTS}
<link rel="stylesheet" href="{A('styles.css')}?v={VER}">
<script>document.documentElement.classList.add('js')</script>
<script defer src="{A('translations.js')}?v={VER}"></script>
<script defer src="{A('app.js')}?v={VER}"></script>
{ld(salon_ld())}{extra}</head>
<body>"""


def lang_switch(page="", alt_page=None):
    """Przelacznik jezyka jako linki.

    Wczesniej podmienial teksty w JS na jednym adresie — Google widzial wtedy
    tylko polska wersje. Teraz kazdy jezyk ma wlasny URL, wiec to zwykle <a>.
    """
    out = ""
    for l in LANGS:
        cls = ' class="active"' if l == CUR else ""
        target = page if (l == CUR or alt_page is None) else alt_page
        out += (f'<a href="{U_lang(l, target)}" hreflang="{l}" data-lang="{l}"{cls}'
                f' rel="alternate">{LANG_LABEL[l]}</a>')
    return f'<div class="lang-switch">{out}</div>'


def header_html(page="", alt_page=None):
    return f"""
<header id="topbar">
  <a href="{U()}" class="brand">BAD&nbsp;ANGEL</a>
  <nav>
    <a href="{U()}#uslugi" data-i18n="nav_services">{P('nav_services')}</a>
    <a href="{U('portfolio.html')}" data-i18n="nav_portfolio">{P('nav_portfolio')}</a>
    <a href="{U('kalkulator.html')}" data-i18n="nav_calc">{P('nav_calc')}</a>
    <a href="{U()}#zespol" data-i18n="nav_team">{P('nav_team')}</a>
    <a href="{U()}#kontakt" data-i18n="nav_contact">{P('nav_contact')}</a>
  </nav>
  <div class="nav-cta">
    <button class="s-open" data-search-open aria-label="{P('search_label')}">
      <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7">
        <circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4.2-4.2"></path></svg>
    </button>
    {lang_switch(page, alt_page)}
    <a class="btn solid sm" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book">{P('btn_book')}</a>
    <button class="burger" aria-label="Menu" onclick="document.getElementById('drawer').classList.add('open')">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="drawer" id="drawer">
  <button class="close" onclick="document.getElementById('drawer').classList.remove('open')">&times;</button>
  <a href="{U()}#uslugi" onclick="closeDrawer()" data-i18n="nav_services">{P('nav_services')}</a>
  <a href="{U('portfolio.html')}" onclick="closeDrawer()" data-i18n="nav_portfolio">{P('nav_portfolio')}</a>
  <a href="{U('kalkulator.html')}" onclick="closeDrawer()" data-i18n="nav_calc">{P('nav_calc')}</a>
  <a href="{U()}#zespol" onclick="closeDrawer()" data-i18n="nav_team">{P('nav_team')}</a>
  <a href="{U()}#opinie" onclick="closeDrawer()" data-i18n="nav_reviews">{P('nav_reviews')}</a>
  <a href="{U()}#kontakt" onclick="closeDrawer()" data-i18n="nav_contact">{P('nav_contact')}</a>
  <a href="#" data-search-open onclick="closeDrawer()" data-i18n="search_label">{P('search_label')}</a>
  <a href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="book_online">{P('book_online')}</a>
  {lang_switch(page, alt_page)}
</div>

<div class="s-box" id="searchBox" role="dialog" aria-modal="true" aria-label="{P('search_label')}">
  <div class="s-panel">
    <div class="s-head">
      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7">
        <circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4.2-4.2"></path></svg>
      <input id="searchInput" type="search" autocomplete="off" placeholder="{P('search_ph')}"
             aria-label="{P('search_label')}">
      <button class="s-close" aria-label="Zamknij">&times;</button>
    </div>
    <div class="s-out" id="searchOut"></div>
    <div class="s-hint">{P('search_hint')}</div>
  </div>
</div>"""


def footer_html():
    return f"""
<footer>
  <div class="brand">BAD&nbsp;ANGEL</div>
  <div class="soc">
    <a href="{IG}" target="_blank" rel="noopener">Instagram</a>
    <a href="{FB}" target="_blank" rel="noopener">Facebook</a>
    <a href="{BOOKSY}" target="_blank" rel="noopener">Booksy</a>
  </div>
  <small>© 2026 Salon Urody BAD ANGEL · aleja Wyzwolenia 5/10, Szczecin</small>
</footer>

<button class="to-top" id="toTop" aria-label="Do góry">↑</button>
<div class="mcta">
  <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
</div>
<div class="lb" id="lightbox">
  <button class="lb-close" aria-label="Zamknij">&times;</button>
  <button class="lb-nav lb-prev" aria-label="Poprzednie">‹</button>
  <img id="lbImg" src="" alt="">
  <button class="lb-nav lb-next" aria-label="Następne">›</button>
</div>
<script>
function closeDrawer(){{document.getElementById('drawer').classList.remove('open');}}
var bar=document.getElementById('topbar');
addEventListener('scroll',function(){{bar.classList.toggle('solid',scrollY>60);}});
</script>
</body>
</html>"""


def bg(img_path, fallback):
    """Warstwa: zdjęcie (gdy istnieje) nad gradientem-fallbackiem."""
    return f"background:url('{A(img_path)}') center/cover, {fallback};"


# --- ceny w tekstach ------------------------------------------------------
# Cennik zyje w site_data.json i zmienia go bot z Telegrama. Gdyby ceny byly
# wpisane na sztywno w akapitach i FAQ, po pierwszej podwyzce strona klamalaby
# klientowi i Google. Zamiast liczby piszemy {cena:Nazwa pozycji}, a build
# podstawia aktualna wartosc i krzyczy, gdy pozycja zniknela z cennika.
_PRICE_MISSES = []


def price_of(cat_slug, item_name):
    cat = next((c for c in CATEGORIES if c["slug"] == cat_slug), None)
    if not cat:
        return None
    for name, desc, dur, price in cat["items"]:
        if name.strip().lower() == item_name.strip().lower():
            return price.split("(")[0].strip()
    return None


def fill_prices(text, cat_slug):
    def sub(m):
        want = m.group(1)
        slug, _, name = want.rpartition("|")
        val = price_of(slug or cat_slug, name)
        if val is None:
            _PRICE_MISSES.append((cat_slug, name))
            return "—"
        return val
    return re.sub(r"\{cena:([^}]+)\}", sub, text)


def report_price_misses():
    if _PRICE_MISSES:
        print("\nUWAGA — pozycje cennika, do ktorych odwoluje sie tresc, nie istnieja:")
        for slug, name in sorted(set(_PRICE_MISSES)):
            print(f"  [{slug}] {name}")
        print("Popraw nazwe w seo_content.py / landing_content.py albo w site_data.json.\n")


# --- zdjecia: wymiary i teksty alternatywne --------------------------------
# Atrybuty width/height blokuja przeskakiwanie ukladu przy ladowaniu (CLS),
# co Google liczy do Core Web Vitals. Wymiary trzymamy w image_sizes.json,
# bo build.py leci tez w GitHub Actions, gdzie nie ma Pillow.
_SIZES_FILE = os.path.join(ROOT, "image_sizes.json")
try:
    with open(_SIZES_FILE, encoding="utf-8") as _f:
        IMG_SIZES = json.load(_f)
except (OSError, ValueError):
    IMG_SIZES = {}
_SIZES_DIRTY = False


def img_dims(rel):
    """(szerokosc, wysokosc) zdjecia albo None."""
    global _SIZES_DIRTY
    rel = rel.lstrip("/")
    if rel not in IMG_SIZES:
        try:
            from PIL import Image
            with Image.open(os.path.join(ROOT, rel)) as im:
                IMG_SIZES[rel] = list(im.size)
        except Exception:
            return None
        _SIZES_DIRTY = True
    v = IMG_SIZES.get(rel)
    return tuple(v) if v else None


def save_img_sizes():
    if _SIZES_DIRTY:
        with open(_SIZES_FILE, "w", encoding="utf-8") as f:
            json.dump(dict(sorted(IMG_SIZES.items())), f, indent=0, sort_keys=True)
        print("napisano image_sizes.json")


def dim_attr(rel):
    d = img_dims(rel)
    return f' width="{d[0]}" height="{d[1]}"' if d else ""


# Zroznicowane opisy alt — wczesniej kazde zdjecie w galerii mialo ten sam
# tekst, wiec Google Images widzialo 60 identycznych podpisow.
ALT_PHRASES = {
    "manicure": ["Manicure hybrydowy", "Paznokcie żelowe", "Manicure klasyczny",
                 "Przedłużanie paznokci", "Stylizacja paznokci", "Manicure japoński"],
    "pedicure": ["Pedicure hybrydowy", "Pedicure klasyczny", "Pedicure z opracowaniem stopy",
                 "Stylizacja paznokci u stóp"],
    "rzesy": ["Przedłużanie rzęs metodą objętościową", "Rzęsy 1:1 — efekt naturalny",
              "Rzęsy 3:1", "Przedłużanie rzęs"],
    "brwi": ["Laminacja brwi", "Henna pudrowa brwi", "Regulacja i stylizacja brwi",
             "Laminacja rzęs"],
    "masaz": ["Masaż relaksacyjny", "Masaż pleców", "Masaż klasyczny"],
    "blizny": ["Mikroneedling twarzy", "Zabieg na blizny", "Terapia mikroigłowa"],
    "wlosy": ["Warkoczyki z kanekalonem", "Box braids", "Warkoczyki"],
    "spa": ["Zabieg SPA na dłonie", "Pielęgnacja SPA"],
}


def gallery_alt(slug, name, i):
    """Alt: fraza z rotacji + marka + miasto. Rozny dla kazdego zdjecia."""
    ph = ALT_PHRASES.get(slug)
    lead = ph[i % len(ph)] if ph else name
    return f"{lead} — Salon Urody BAD ANGEL, Szczecin (praca nr {i + 1})"


def breadcrumb_ld(trail):
    """BreadcrumbList — Google pokazuje sciezke zamiast golego URL-a w wynikach."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": nm,
             "item": SITE_URL + url}
            for i, (nm, url) in enumerate(trail)],
    }


def ld(*objs):
    """Bloki JSON-LD do wstawienia w <head>."""
    return "".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n'
        for o in objs)


def parse_price(s):
    """'od 90 zł' -> (90.0, True); '359,10 zł' -> (359.1, False)."""
    is_from = "od" in s
    num = s.replace("od", "").replace("zł", "").replace("\xa0", "").strip().replace(" ", "").replace(",", ".")
    try:
        return float(num), is_from
    except ValueError:
        return 0.0, is_from


# ---------------------------------------------------------------------------
# STRONA GŁÓWNA
# ---------------------------------------------------------------------------
def hero_wall_html(cols=5):
    """Ściana prac w hero: kolumny zdjęć z assets/wall.

    Każda kolumna jest renderowana dwa razy, bo animacja przesuwa ją o -50% —
    druga kopia domyka pętlę bez skoku. To te same pliki, więc nic nie dociąga.
    """
    files = sorted(glob.glob(os.path.join(ROOT, "assets", "wall", "*.jpg")))
    if not files:
        return ""
    names = [os.path.basename(f) for f in files]
    out = ""
    for ci in range(cols):
        mine = names[ci::cols]
        if not mine:
            continue
        imgs = "".join(
            f'<img src="/assets/wall/{n}" alt="" loading="lazy" decoding="async" '
            f'width="300" height="375">'
            for n in mine + mine)
        out += f'<div class="col">{imgs}</div>'
    return out


# Karty, na których stockowe assets/usluga-<slug>.jpg zamieniamy na prawdziwą
# pracę z galerii. Tylko tam, gdzie realne zdjęcie jest mocniejsze od stocku —
# masaz/spa nadal czekają na własne zdjęcia z salonu.
CARD_OVERRIDE = {
    "wlosy": "assets/gallery/wlosy/01.jpg",
    "blizny": "assets/gallery/blizny/06.jpg",
    # usluga-pedicure.jpg (746x1280) i usluga-brwi.jpg (651x1280) to pionowe
    # składanki dwóch zdjęć. Kadr 4/5 wypadał na szwie i karta pokazywała pół
    # jednego zdjęcia i pół drugiego — tu pojedyncze ujęcia.
    "pedicure": "assets/gallery/pedicure/07.jpg",
    "brwi": "assets/gallery/brwi/06.jpg",
}


def category_card_image(slug, fallback_grad):
    override = CARD_OVERRIDE.get(slug)
    if override and os.path.exists(os.path.join(ROOT, override)):
        return bg(override, fallback_grad)
    return bg(f"assets/usluga-{slug}.jpg", fallback_grad)


def build_index():
    wall = hero_wall_html()
    cards = ""
    grads = ["linear-gradient(150deg,#26201d,#0a0a0c)", "linear-gradient(150deg,#1d2226,#0a0a0c)",
             "linear-gradient(150deg,#231d24,#0a0a0c)", "linear-gradient(150deg,#20261f,#0a0a0c)"]
    for i, c in enumerate(CATEGORIES):
        g = grads[i % len(grads)]
        s = c['slug']
        surl = U(f"usluga-{s}.html")
        cards += f"""
        <a class="card" href="{surl}">
          <div class="thumb" style="{category_card_image(s, g)}"></div>
          <div class="cap">
            <h3 data-i18n="cat_{s}_name">{P(f"cat_{s}_name") or c['name']}</h3>
            <div class="price">{len(c['items'])} <span data-i18n="unit_uslug">{P('unit_uslug')}</span> · {c['items'][0][3]}</div>
            <div class="go" data-i18n="card_cta">{P('card_cta')}</div>
          </div>
        </a>"""

    members = ""
    for m in MASTERS:
        murl = U("mistrz-" + m['slug'] + ".html")
        mrole = P("role_" + m['slug']) or m['role']
        members += f"""
        <a class="member" href="{murl}">
          <div class="ph" data-i="{m['name'][0]}" style="{bg('assets/mistrz-'+m['slug']+'.jpg','linear-gradient(160deg,#26262c,#0e0e11)')}"></div>
          <h4>{m['name']}</h4><span data-i18n="role_{m['slug']}">{mrole}</span>
        </a>"""

    rv = ""
    for i, r in enumerate(REVIEWS):
        rv += f"""
        <div class="review"><div class="stars">★★★★★</div><p>„<span data-i18n="rev{i}_text">{r['text']['pl']}</span>”</p>
          <div class="who"><b>{r['who']}</b> · <span data-i18n="rev{i}_svc">{r['svc']['pl']}</span></div></div>"""

    jsonld = {
        "@context": "https://schema.org",
        "@type": "BeautySalon",
        "name": "Salon Urody BAD ANGEL",
        "url": f"{SITE_URL}/",
        "image": OG_IMAGE,
        "address": {"@type": "PostalAddress", "streetAddress": "aleja Wyzwolenia 5/10",
                    "postalCode": "70-552", "addressLocality": "Szczecin", "addressCountry": "PL"},
        "geo": {"@type": "GeoCoordinates", "latitude": 53.4337, "longitude": 14.5518},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Salon+Urody+BAD+ANGEL+aleja+Wyzwolenia+5%2F10+Szczecin",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                                                     "Friday", "Saturday", "Sunday"],
                                       "opens": "09:00", "closes": "20:00"}],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": RATING, "reviewCount": REVIEWS_COUNT},
        "priceRange": "50-600 PLN",
        "sameAs": [BOOKSY],
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": P(f"faq_q{i}"),
             "acceptedAnswer": {"@type": "Answer", "text": P(f"faq_a{i}")}}
            for i in range(4) if f"faq_q{i}" in I18N
        ],
    }
    extra = (f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
             f'<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>\n')
    page = ""
    html = head(P('seo_home_title'),
                P('seo_home_desc').replace("{n}", REVIEWS_COUNT),
                extra=extra)
    html += header_html("")
    html += f"""
<main>
  <section class="panel has-wall" id="hero">
    <div class="wall" aria-hidden="true">{wall}</div>
    <div class="bg"></div>
    <div class="top">
      <div class="eyebrow" data-i18n="hero_eyebrow">{P('hero_eyebrow')}</div>
      <img class="logo" src="/assets/logo.png" alt="BAD ANGEL Beauty Salon">
      <div class="rating"><span class="stars">{STARS}</span> &nbsp;<span data-i18n="hero_rating">{P('hero_rating')}</span></div>
    </div>
    <div class="bottom"><div class="btns">
      <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
      <a class="btn ghost" href="#uslugi" data-i18n="btn_see_services">{P('btn_see_services')}</a>
    </div></div>
    <div class="cue" aria-hidden="true"><i></i><span data-i18n="hero_cue">{P('hero_cue')}</span></div>
  </section>

  <section class="block" id="uslugi" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="sec_services_title">{P('sec_services_title')}</h2><p data-i18n="sec_services_sub">{P('sec_services_sub')}</p></div>
      <div class="grid">{cards}</div>
    </div>
  </section>

  <section class="split reveal">
    <div class="media" style="{bg('assets/feature-nails.jpg','linear-gradient(135deg,#1c1c22,#0a0a0c)')}"></div>
    <div class="body">
      <div class="eyebrow">Manicure &amp; Nails</div>
      <h2 data-i18n="feat1_title">{P('feat1_title')}</h2>
      <p data-i18n="feat1_text">{P('feat1_text')}</p>
      <div class="btns"><a class="btn solid" href="{U('usluga-manicure.html')}" data-i18n="btn_see_services">{P('btn_see_services')}</a></div>
    </div>
  </section>
  <section class="split reveal">
    <div class="body">
      <div class="eyebrow" data-i18n="feat2_eyebrow">{P('feat2_eyebrow')}</div>
      <h2 data-i18n="feat2_title">{P('feat2_title')}</h2>
      <p data-i18n="feat2_text">{P('feat2_text')}</p>
      <div class="btns"><a class="btn solid" href="{U('usluga-rzesy.html')}" data-i18n="btn_see_services">{P('btn_see_services')}</a></div>
    </div>
    <div class="media" style="{bg('assets/feature-lashes.jpg','linear-gradient(135deg,#221a1f,#0a0a0c)')}"></div>
  </section>

  <section class="block" id="efekty" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="ba_title">{P('ba_title')}</h2><p data-i18n="ba_sub">{P('ba_sub')}</p></div>
      <div class="ba-pair">
        <figure class="ba-item reveal">
          <div class="ba" id="baSlider">
            <div class="ba-img ba-before" style="background-image:url('/assets/ba2-before.jpg')"></div>
            <div class="ba-img ba-after" style="background-image:url('/assets/ba2-after.jpg')"></div>
            <span class="ba-tag l" data-i18n="ba_before">{P('ba_before')}</span>
            <span class="ba-tag r" data-i18n="ba_after">{P('ba_after')}</span>
            <div class="ba-line"></div>
            <div class="ba-handle" aria-label="{P('ba_handle_label')}">⇄</div>
          </div>
          <figcaption data-i18n="ba_cap_brwi">{P('ba_cap_brwi')}</figcaption>
        </figure>
        <figure class="ba-item reveal">
          <div class="ba" id="baSlider2">
            <div class="ba-img ba-before" style="background-image:url('/assets/ba-before.jpg')"></div>
            <div class="ba-img ba-after" style="background-image:url('/assets/ba-after.jpg')"></div>
            <span class="ba-tag l" data-i18n="ba_before">{P('ba_before')}</span>
            <span class="ba-tag r" data-i18n="ba_after">{P('ba_after')}</span>
            <div class="ba-line"></div>
            <div class="ba-handle" aria-label="{P('ba_handle_label')}">⇄</div>
          </div>
          <figcaption data-i18n="ba_cap_blizny">{P('ba_cap_blizny')}</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="block" id="zespol" style="background:#000">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="sec_team_title">{P('sec_team_title')}</h2><p data-i18n="sec_team_sub">{P('sec_team_sub')}</p></div>
      <div class="team">{members}</div>
    </div>
  </section>

  <section class="block" id="opinie" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="sec_reviews_title">{P('sec_reviews_title')}</h2><p><span class="stars">{STARS}</span> &nbsp;<span data-i18n="sec_reviews_sub">{P('sec_reviews_sub')}</span></p></div>
      <div class="reviews">{rv}</div>
      <div class="btns" style="margin-top:48px"><a class="btn ghost" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="all_reviews">{P('all_reviews')}</a></div>
    </div>
  </section>

  <section class="block" id="faq" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="faq_title">{P('faq_title')}</h2></div>
      <div class="faq">
        <div class="faq-item"><button class="faq-q" data-i18n="faq_q0">{P('faq_q0')}</button><div class="faq-a"><p data-i18n="faq_a0">{P('faq_a0')}</p></div></div>
        <div class="faq-item"><button class="faq-q" data-i18n="faq_q1">{P('faq_q1')}</button><div class="faq-a"><p data-i18n="faq_a1">{P('faq_a1')}</p></div></div>
        <div class="faq-item"><button class="faq-q" data-i18n="faq_q2">{P('faq_q2')}</button><div class="faq-a"><p data-i18n="faq_a2">{P('faq_a2')}</p></div></div>
        <div class="faq-item"><button class="faq-q" data-i18n="faq_q3">{P('faq_q3')}</button><div class="faq-a"><p data-i18n="faq_a3">{P('faq_a3')}</p></div></div>
      </div>
    </div>
  </section>

  <section class="block" id="share" style="background:#000">
    <div class="wrap" style="text-align:center">
      <div class="section-head reveal"><h2 data-i18n="share_title">{P('share_title')}</h2><p data-i18n="share_sub">{P('share_sub')}</p></div>
      <div class="share-row">
        <a class="js-share" data-net="wa" target="_blank" rel="noopener">WhatsApp</a>
        <a class="js-share" data-net="tg" target="_blank" rel="noopener">Telegram</a>
        <a class="js-share" data-net="fb" target="_blank" rel="noopener">Facebook</a>
        <button class="js-copy" data-i18n="share_copy">{P('share_copy')}</button>
      </div>
    </div>
  </section>

  <section class="block" id="kontakt" style="background:#000">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="sec_contact_title">{P('sec_contact_title')}</h2><p data-i18n="sec_contact_sub">{P('sec_contact_sub')}</p></div>
      <div class="contact-grid">
        <div>
          <div class="info-row"><div class="k" data-i18n="contact_addr_label">{P('contact_addr_label')}</div><div class="v" data-i18n-html="contact_addr_value">{P('contact_addr_value')}</div></div>
          <div class="info-row"><div class="k" data-i18n="contact_hours_label">{P('contact_hours_label')}</div><div class="v" data-i18n-html="contact_hours_value">{P('contact_hours_value')}</div><span class="open-badge" data-open-badge></span></div>
          <div class="info-row"><div class="k" data-i18n="contact_amen_label">{P('contact_amen_label')}</div><div class="v" data-i18n="contact_amen_value">{P('contact_amen_value')}</div></div>
          <div class="btns" style="justify-content:flex-start;padding:0;margin-top:34px"><a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="contact_book">{P('contact_book')}</a></div>
        </div>
        <div class="map"><iframe loading="lazy" src="https://www.google.com/maps?q=aleja+Wyzwolenia+5,+Szczecin&output=embed"></iframe></div>
      </div>
    </div>
  </section>
</main>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# STRONA USŁUGI
# ---------------------------------------------------------------------------
def landing_links_html(slug):
    """Z huba kategorii w dol, do stron pod konkretne frazy. Tylko PL —
    landingi celuja w polskie zapytania i istnieja tylko w korzeniu."""
    ls = landings_for(slug) if CUR == "pl" else []
    if not ls:
        return ""
    cards = "".join(
        f'<a class="rel-card" href="/{l["slug"]}.html">'
        f'<span class="rel-n">{l["h1"]}</span>'
        f'<span class="rel-d">{l["lead"]}</span></a>' for l in ls)
    return f"""
  <section class="block rel-block" style="background:#0e0e10;padding-bottom:0">
    <div class="wrap">
      <div class="section-head reveal"><h2>Szczegółowo o zabiegach</h2></div>
      <div class="rel-grid reveal">{cards}</div>
    </div>
  </section>"""


def related_services_html(slug, n=3):
    """Linki do innych usług z opisowym anchor textem.

    Podstrony usług byly wczesniej slepymi zaulkami — robot wchodzil i wracal
    na strone glowna. Krzyzowe linki rozkladaja moc linkowa po calym serwisie.
    """
    others = [c for c in CATEGORIES if c["slug"] != slug][:n + 2]
    # bierzemy sasiadow z listy, zeby na kazdej stronie zestaw byl inny
    idx = next((i for i, c in enumerate(CATEGORIES) if c["slug"] == slug), 0)
    pool = [CATEGORIES[(idx + k) % len(CATEGORIES)] for k in range(1, n + 1)] or others
    cards = ""
    for c in pool:
        nm = P(f"cat_{c['slug']}_name") or c["name"]
        lead = P(f"cat_{c['slug']}_lead") or c["lead"]
        cards += (f'<a class="rel-card" href="{U("usluga-" + c["slug"] + ".html")}">'
                  f'<span class="rel-n">{nm} {P("seo_in_szczecin")}</span>'
                  f'<span class="rel-d">{lead}</span></a>')
    return f"""
  <section class="block rel-block">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="rel_title">{P('rel_title') or 'Zobacz też'}</h2></div>
      <div class="rel-grid reveal">{cards}</div>
    </div>
  </section>"""


def build_service(c):
    rows = ""
    for name, desc, dur, price in c["items"]:
        d = f'<div class="desc">{desc}</div>' if desc else ""
        rows += f"""
      <div class="price-item">
        <div class="txt"><h3>{name}</h3>{d}<div class="dur">{dur}</div></div>
        <div class="amt">{price}</div>
        <div class="book"><a class="btn solid sm" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book">{P('btn_book')}</a></div>
      </div>"""

    cname = P(f"cat_{c['slug']}_name") or c['name']
    cintro = P(f"cat_{c['slug']}_intro") or c['intro']
    page = f"usluga-{c['slug']}.html"
    url = SITE_URL + U(page)

    # Katalog ofert z cenami — Google moze pokazac widelki cenowe w wynikach.
    offers = []
    for name, desc, dur, price in c["items"]:
        val, _ = parse_price(price)
        if not val:
            continue
        offers.append({
            "@type": "Offer", "name": name, "price": f"{val:g}",
            "priceCurrency": "PLN", "url": url,
            "availability": "https://schema.org/InStock",
        })

    svc_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"{cname} Szczecin",
        "serviceType": cname,
        "description": cintro,
        "provider": {"@type": "BeautySalon", "name": "Salon Urody BAD ANGEL",
                     **({"telephone": PHONE} if PHONE else {}),
                     "address": {"@type": "PostalAddress", "streetAddress": "aleja Wyzwolenia 5/10",
                                 "postalCode": "70-552", "addressLocality": "Szczecin", "addressCountry": "PL"}},
        "areaServed": {"@type": "City", "name": "Szczecin"},
        "url": url,
        "image": f"{SITE_URL}/assets/usluga-{c['slug']}.jpg",
    }
    if offers:
        svc_ld["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": f"Cennik — {cname}",
                                     "itemListElement": offers}

    blocks = [svc_ld, breadcrumb_ld([
        (P('crumb_home') or "Strona główna", U()),
        (P('nav_services') or "Usługi", U() + "#uslugi"),
        (cname, U(page)),
    ])]

    seo = CAT_SEO.get(c["slug"])
    if seo and seo.get("faq"):
        blocks.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": fill_prices(T(qa["q"]), c["slug"]),
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": fill_prices(T(qa["a"]), c["slug"])}}
                for qa in seo["faq"]],
        })

    html = head(f"{cname} Szczecin — cennik, opinie | Salon Urody BAD ANGEL",
                f"{cname} {P('seo_in_szczecin')} — Salon Urody BAD ANGEL, aleja Wyzwolenia 5/10. {cintro} {P('seo_booksy')}",
                page=page, extra=ld(*blocks))
    html += header_html(page)

    # Galeria — zdjęcia z assets/gallery/<slug>/
    gdir = os.path.join(ROOT, "assets", "gallery", c["slug"])
    gfiles = sorted(os.path.basename(p) for p in glob.glob(os.path.join(gdir, "*.jpg")))
    gallery = ""
    if gfiles:
        imgs = ""
        for i, fn in enumerate(gfiles):
            rel = f"assets/gallery/{c['slug']}/{fn}"
            imgs += (f'<img loading="lazy" decoding="async" src="/{rel}"{dim_attr(rel)}'
                     f' alt="{gallery_alt(c["slug"], c["name"], i)}">')
        gallery = f"""
  <section class="block" style="background:#000;padding-top:40px">
    <div class="section-head reveal"><h2 data-i18n="gallery_title">{P('gallery_title')}</h2><p>{len(gfiles)} <span data-i18n="gallery_photos">{P('gallery_photos')}</span></p></div>
    <div class="gallery"><div class="cols">{imgs}</div></div>
  </section>"""

    # Rozszerzony opis + FAQ — bez tego strona usługi to sam cennik,
    # a Google nie ma z czego zrozumieć, na jakie zapytania odpowiada.
    seo_html = ""
    if seo:
        paras = "".join(f"<p>{fill_prices(T(t), c['slug'])}</p>" for t in seo["text"])
        faq_items = "".join(
            f'<div class="faq-item"><button class="faq-q">{fill_prices(T(qa["q"]), c["slug"])}</button>'
            f'<div class="faq-a"><p>{fill_prices(T(qa["a"]), c["slug"])}</p></div></div>'
            for qa in seo["faq"])
        faq_block = ""
        if faq_items:
            faq_block = f"""
  <section class="block" id="faq" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="faq_title">{P('faq_title')}</h2></div>
      <div class="faq">{faq_items}</div>
    </div>
  </section>"""
        seo_html = f"""
  <section class="block svc-seo">
    <div class="wrap">
      <div class="section-head reveal"><h2>{T(seo['h'])}</h2></div>
      <div class="prose reveal">{paras}</div>
    </div>
  </section>{faq_block}"""

    html += f"""
<main>
  <section class="subhero">
    <div class="bg" style="{bg('assets/usluga-'+c['slug']+'.jpg','linear-gradient(150deg,#20202a,#0a0a0c)')}"></div>
    <div class="scrim"></div>
    <div class="crumbs"><a href="{U()}" data-i18n="crumb_home">{P('crumb_home')}</a> &nbsp;/&nbsp; <a href="{U()}#uslugi" data-i18n="nav_services">{P('nav_services')}</a> &nbsp;/&nbsp; <span data-i18n="cat_{c['slug']}_name">{cname}</span></div>
    <div class="inner">
      <div class="eyebrow" data-i18n="cat_{c['slug']}_tag">{c['tag']}</div>
      <h1 data-i18n="cat_{c['slug']}_name">{cname} {P('seo_in_szczecin')}</h1>
      <p class="lead" data-i18n="cat_{c['slug']}_lead">{c['lead']}</p>
    </div>
  </section>

  <section class="intro-band"><p data-i18n="cat_{c['slug']}_intro">{c['intro']}</p></section>

  <section class="pricelist">
    {rows}
    <div class="btns" style="margin-top:50px">
      <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="svc_book_booksy">{P('svc_book_booksy')}</a>
      <a class="btn ghost" href="{U()}#uslugi" data-i18n="svc_other">{P('svc_other')}</a>
    </div>
  </section>
{landing_links_html(c['slug'])}
{seo_html}
{gallery}
{related_services_html(c['slug'])}
</main>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# STRONA MASTRA
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# STRONY POD KONKRETNE FRAZY (tylko PL)
# ---------------------------------------------------------------------------
def _landing_filled(l):
    """Kopia landingu z podstawionymi aktualnymi cenami."""
    d = dict(l)
    f = lambda t: fill_prices(t, l["parent"])
    for k in ("title", "desc", "h1", "lead"):
        d[k] = f(d[k])
    d["text"] = [f(t) for t in d["text"]]
    d["faq"] = [(f(q), f(a)) for q, a in d["faq"]]
    return d


def landings_for(parent_slug):
    return [x for x in LANDINGS if x["parent"] == parent_slug]


def landing_items(l, cat):
    """Pozycje z cennika kategorii pasujace do frazy tej strony."""
    out = [it for it in cat["items"]
           if any(m.lower() in it[0].lower() for m in l["match"])]
    return out or cat["items"]


def build_landing(l):
    l = _landing_filled(l)
    """Strona pod jedno zapytanie, np. "manicure hybrydowy szczecin".

    Konkurencja z miasta ma pod te frazy osobne adresy z fraza w URL-u i to
    one wychodza w wynikach, a nie ogolna strona kategorii. Tresc jest inna
    niz na stronie uslugi — inaczej obie konkurowalyby o to samo zapytanie.
    """
    cat = next(c for c in CATEGORIES if c["slug"] == l["parent"])
    page = f"{l['slug']}.html"
    url = f"{SITE_URL}/{page}"
    items = landing_items(l, cat)

    rows = ""
    for name, desc, dur, price in items:
        d = f'<div class="desc">{desc}</div>' if desc else ""
        rows += f"""
      <div class="price-item">
        <div class="txt"><h3>{name}</h3>{d}<div class="dur">{dur}</div></div>
        <div class="amt">{price}</div>
        <div class="book"><a class="btn solid sm" href="{BOOKSY}" target="_blank" rel="noopener">Rezerwuj</a></div>
      </div>"""

    offers = []
    for name, desc, dur, price in items:
        val, _ = parse_price(price)
        if val:
            offers.append({"@type": "Offer", "name": name, "price": f"{val:g}",
                           "priceCurrency": "PLN", "url": url,
                           "availability": "https://schema.org/InStock"})

    svc_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": l["h1"], "description": l["desc"], "url": url,
        "provider": {"@type": "BeautySalon", "name": "Salon Urody BAD ANGEL",
                     "url": SITE_URL + "/",
                     **({"telephone": PHONE} if PHONE else {}),
                     "address": {"@type": "PostalAddress", "streetAddress": "aleja Wyzwolenia 5/10",
                                 "postalCode": "70-552", "addressLocality": "Szczecin",
                                 "addressCountry": "PL"},
                     "aggregateRating": {"@type": "AggregateRating", "ratingValue": RATING,
                                         "reviewCount": REVIEWS_COUNT}},
        "areaServed": {"@type": "City", "name": "Szczecin"},
        "image": f"{SITE_URL}/assets/usluga-{cat['slug']}.jpg",
    }
    if offers:
        svc_ld["hasOfferCatalog"] = {"@type": "OfferCatalog",
                                     "name": f"Cennik — {l['h1']}",
                                     "itemListElement": offers}

    blocks = [svc_ld, breadcrumb_ld([("Strona główna", "/"),
                                     (cat["name"], f"/usluga-{cat['slug']}.html"),
                                     (l["h1"], "/" + page)]),
              {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}}
                              for q, a in l["faq"]]}]

    html = head(l["title"], l["desc"], page=page, extra=ld(*blocks),
                alt_langs=False, canonical=url)
    html += header_html(page, alt_page=f"usluga-{cat['slug']}.html")

    gfiles = sorted(os.path.basename(x) for x in
                    glob.glob(os.path.join(ROOT, "assets", "gallery", cat["slug"], "*.jpg")))[:12]
    gallery = ""
    if gfiles:
        imgs = ""
        for i, name in enumerate(gfiles):
            rel = f"assets/gallery/{cat['slug']}/{name}"
            imgs += (f'<img loading="lazy" decoding="async" src="/{rel}"{dim_attr(rel)}'
                     f' alt="{l["h1"]} — praca salonu BAD ANGEL, Szczecin (nr {i + 1})">')
        gallery = f"""
  <section class="block" style="background:#000;padding-top:40px">
    <div class="section-head reveal"><h2>Nasze prace</h2></div>
    <div class="gallery"><div class="cols">{imgs}</div></div>
  </section>"""

    paras = "".join(f"<p>{t}</p>" for t in l["text"])
    faq_items = "".join(
        f'<div class="faq-item"><button class="faq-q">{q}</button>'
        f'<div class="faq-a"><p>{a}</p></div></div>' for q, a in l["faq"])

    i = LANDINGS.index(l)
    sibs = [LANDINGS[(i + k) % len(LANDINGS)] for k in range(1, 4)]
    siblings = "".join(
        f'<a class="rel-card" href="/{o["slug"]}.html">'
        f'<span class="rel-n">{o["h1"]}</span>'
        f'<span class="rel-d">{o["lead"]}</span></a>' for o in sibs)

    html += f"""
<main>
  <section class="subhero">
    <div class="bg" style="{bg('assets/usluga-' + cat['slug'] + '.jpg', 'linear-gradient(150deg,#20202a,#0a0a0c)')}"></div>
    <div class="scrim"></div>
    <div class="crumbs"><a href="/">Strona główna</a> &nbsp;/&nbsp; <a href="/usluga-{cat['slug']}.html">{cat['name']}</a> &nbsp;/&nbsp; <span>{l['h1']}</span></div>
    <div class="inner">
      <div class="eyebrow">{l['eyebrow']}</div>
      <h1>{l['h1']}</h1>
      <p class="lead">{l['lead']}</p>
    </div>
  </section>

  <section class="block svc-seo">
    <div class="wrap"><div class="prose reveal">{paras}</div></div>
  </section>

  <section class="pricelist">
    <div class="section-head reveal" style="margin-bottom:26px"><h2>Cennik — {l['h1']}</h2>
      <p>Ceny takie same jak w Booksy · aleja Wyzwolenia 5/10, Szczecin</p></div>
    {rows}
    <div class="btns" style="margin-top:50px">
      <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener">Zarezerwuj wizytę</a>
      <a class="btn ghost" href="/usluga-{cat['slug']}.html">Pełny cennik: {cat['name']}</a>
    </div>
  </section>

  <section class="block" id="faq" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2>Częste pytania</h2></div>
      <div class="faq">{faq_items}</div>
    </div>
  </section>
{gallery}
  <section class="block rel-block">
    <div class="wrap">
      <div class="section-head reveal"><h2>Zobacz też</h2></div>
      <div class="rel-grid reveal">{siblings}</div>
    </div>
  </section>
</main>"""
    html += footer_html()
    return html


def master_works(m):
    """Zdjecia prac mistrzyni — pliki z jej prefiksem w galeriach uslug.

    Zdjecia leza raz, w galerii kategorii; prefiks (np. "em-") mowi, czyja to
    praca, wiec nic sie nie duplikuje.
    """
    pref = (m.get("works") or "").strip()
    if not pref:
        return []
    out = []
    for c in CATEGORIES:
        for path in sorted(glob.glob(os.path.join(ROOT, "assets", "gallery",
                                                  c["slug"], pref + "*.jpg"))):
            out.append((c["slug"], os.path.basename(path)))
    return out


def build_master(m):
    mrole = P("role_" + m['slug']) or m['role']
    cat_by_slug = {c["slug"]: c for c in CATEGORIES}
    chips = ""
    for s in m["serves"]:
        if s in cat_by_slug:
            churl = U("usluga-" + s + ".html")
            chips += f'<a class="chip" href="{churl}" data-i18n="cat_{s}_name">{P("cat_" + s + "_name") or cat_by_slug[s]["name"]}</a>'
    bio = "".join(f'<p data-i18n="bio_{m["slug"]}_{i}">{p}</p>' for i, p in enumerate(m["bio"]))

    wfiles = master_works(m)
    works = ""
    if wfiles:
        imgs = ""
        for i, (cat, fn) in enumerate(wfiles):
            rel = f"assets/gallery/{cat}/{fn}"
            imgs += (f'<img loading="lazy" decoding="async" src="/{rel}"{dim_attr(rel)}'
                     f' alt="{gallery_alt(cat, m["name"], i)} — {m["name"]}, Salon Urody BAD ANGEL Szczecin">')
        works = f"""
  <section class="block" style="background:#000;padding:0 0 40px">
    <div class="section-head reveal">
      <h2><span data-i18n="master_works_by">{P('master_works_by')}</span> {m['gen']}</h2>
      <p>{len(wfiles)} <span data-i18n="gallery_photos">{P('gallery_photos')}</span></p>
    </div>
    <div class="gallery"><div class="cols">{imgs}</div></div>
  </section>"""

    html = head(f"{m['name']} — {P('role_' + m['slug']) or m['role']} · Salon Urody BAD ANGEL",
                f"{m['name']} — {m['role']} w Salonie Urody BAD ANGEL w Szczecinie. Poznaj naszą specjalistkę i zarezerwuj wizytę.",
                page=f"mistrz-{m['slug']}.html")
    html += header_html(f"mistrz-{m['slug']}.html")
    html += f"""
<main>
  <div class="crumbs" style="position:relative;top:96px;margin:0 auto;max-width:1100px;padding:0 24px">
    <a href="{U()}" data-i18n="crumb_home">{P('crumb_home')}</a> &nbsp;/&nbsp; <a href="{U()}#zespol" data-i18n="nav_team">{P('nav_team')}</a> &nbsp;/&nbsp; {m['name']}
  </div>
  <section class="master">
    <div class="portrait" style="{bg('assets/mistrz-'+m['slug']+'.jpg','linear-gradient(160deg,#26262c,#0e0e11)')}"></div>
    <div>
      <div class="role" data-i18n="role_{m['slug']}">{mrole}</div>
      <h1>{m['name']}</h1>
      <div class="bio">{bio}</div>
      <div class="serves">
        <div class="k"><span data-i18n="master_services_by">{P('master_services_by')}</span> {m['gen']}</div>
        {chips}
      </div>
      <div class="btns" style="justify-content:flex-start;padding:0;margin-top:40px">
        <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
        <a class="btn ghost" href="{U()}#zespol" data-i18n="master_all_team">{P('master_all_team')}</a>
      </div>
    </div>
  </section>
{works}
</main>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# KALKULATOR CEN
# ---------------------------------------------------------------------------
def build_calculator():
    cats = ""
    for c in CATEGORIES:
        rows = ""
        for name, desc, dur, price in c["items"]:
            val, isfrom = parse_price(price)
            rows += f"""
        <label class="calc-row">
          <input type="checkbox" data-price="{val:.2f}" data-from="{1 if isfrom else 0}">
          <span class="cn">{name}</span><span class="cp">{price}</span>
        </label>"""
        cats += f"""
      <details class="calc-cat">
        <summary><span data-i18n="cat_{c['slug']}_name">{P("cat_" + c["slug"] + "_name") or c['name']}</span></summary>{rows}
      </details>"""
    html = head(P('seo_calc_title'),
                P('seo_calc_desc'),
                page="kalkulator.html")
    html += header_html("kalkulator.html")
    html += f"""
<main>
  <section id="kalk">
    <div class="section-head reveal"><h2 data-i18n="calc_title">{P('calc_title')}</h2><p data-i18n="calc_sub">{P('calc_sub')}</p></div>
    <div class="calc" id="calc">{cats}</div>
    <p class="calc-note" data-i18n="calc_note">{P('calc_note')}</p>
  </section>
</main>
<div class="calc-bar">
  <div class="sum"><small><span data-i18n="calc_total">{P('calc_total')}</span> · <span id="calcCount">0</span> <span data-i18n="calc_count">{P('calc_count')}</span></small><span id="calcSum">0 zł</span></div>
  <div class="cta">
    <button class="clear" id="calcClear" data-i18n="calc_clear">{P('calc_clear')}</button>
    <a class="btn solid sm" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
  </div>
</div>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# PORTFOLIO (galeria z filtrem)
# ---------------------------------------------------------------------------
def build_portfolio():
    items, present = [], []
    for c in CATEGORIES:
        gdir = os.path.join(ROOT, "assets", "gallery", c["slug"])
        gfiles = sorted(os.path.basename(p) for p in glob.glob(os.path.join(gdir, "*.jpg")))
        if gfiles:
            present.append(c["slug"])
            items += [(c["slug"], fn) for fn in gfiles]
    fbtns = f'<button class="active" data-filter="all" data-i18n="filter_all">{P("filter_all")}</button>'
    name_by = {c["slug"]: c["name"] for c in CATEGORIES}
    for s in present:
        fbtns += f'<button data-filter="{s}" data-i18n="cat_{s}_name">{P("cat_" + s + "_name") or name_by[s]}</button>'
    imgs = "".join(f'<img loading="lazy" data-cat="{s}" src="/assets/gallery/{s}/{fn}" alt="{name_by[s]} Szczecin — Salon Urody BAD ANGEL">'
                   for s, fn in items)
    html = head(P('seo_portfolio_title'), P('seo_portfolio_desc'),
                page="portfolio.html")
    html += header_html("portfolio.html")
    html += f"""
<main>
  <section class="block" style="padding-top:120px;background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="portfolio_title">{P('portfolio_title')}</h2><p data-i18n="portfolio_sub">{P('portfolio_sub')}</p></div>
      <div class="filters" id="pfFilters">{fbtns}</div>
      <div class="gallery"><div class="cols" id="pfGrid">{imgs}</div></div>
    </div>
  </section>
</main>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# README (lista zdjęć)
# ---------------------------------------------------------------------------
def build_readme():
    lines = ["# Salon Urody BAD ANGEL — strona\n",
             "Statyczna strona (bez zależności). Otwórz przez lokalny serwer:\n",
             "```\ncd \"Salon Urody BAD ANGEL\"\npython3 -m http.server 8777\n# http://localhost:8777\n```\n",
             "Regeneracja stron po zmianie danych: `python3 build.py`\n",
             "## Zdjęcia — wrzuć do folderu `assets/` (nazwy dokładnie takie):\n",
             "Do czasu dodania plików w tych miejscach wyświetla się elegancki ciemny gradient.\n",
             "**Tło / sekcje główne:**",
             "- `assets/hero.jpg` — duże tło hero na stronie głównej (opcjonalnie, np. wnętrze salonu)",
             "- `assets/feature-nails.jpg` — sekcja „Paznokcie”",
             "- `assets/feature-lashes.jpg` — sekcja „Rzęsy i brwi”\n",
             "**Usługi (kafelki + baner podstrony):**"]
    for c in CATEGORIES:
        lines.append(f"- `assets/usluga-{c['slug']}.jpg` — {c['name']}")
    lines.append("\n**Mastrzy (kafelek + portret na podstronie):**")
    for m in MASTERS:
        lines.append(f"- `assets/mistrz-{m['slug']}.jpg` — {m['name']} ({m['role']})")
    lines.append("\n## Rezerwacja")
    lines.append("Każdy przycisk „Rezerwuj / Zarezerwuj” prowadzi na profil Booksy salonu.")
    lines.append("\n## Uwaga")
    lines.append("Biografie mastrów to teksty startowe — możesz je edytować w `build.py` (lista MASTERS) i uruchomić `python3 build.py`.")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# translations.js — dane + przelaczanie jezyka (PL/UK/RU/EN)
# ---------------------------------------------------------------------------
def build_translations_js():
    data = json.dumps(I18N, ensure_ascii=False)
    langs = json.dumps(LANGS)
    return f"""// Auto-generowane przez build.py.
// Kazdy jezyk ma teraz wlasny URL i gotowy tekst w HTML, wiec nic tu nie
// podmieniamy — inaczej skrypt nadpisalby to, co widzi Google. Zostaje
// slownik dla rzeczy liczonych w przegladarce (badge "otwarte teraz").
window.I18N = {data};
(function(){{
  var LANGS = {langs};
  var lang = (document.documentElement.lang || "pl").slice(0,2).toLowerCase();
  if(LANGS.indexOf(lang) < 0) lang = "pl";
  window.__lang = lang;

  function openBadge(){{
    var T = window.I18N;
    document.querySelectorAll("[data-open-badge]").forEach(function(e){{
      var hh = new Date().getHours(), open = hh >= 9 && hh < 20, k = open ? "open_now" : "closed_now";
      if(T[k] && T[k][lang]) e.textContent = T[k][lang];
      e.classList.toggle("open", open); e.classList.toggle("closed", !open);
    }});
    if(window.__afterLang) window.__afterLang(lang);
  }}
  if(document.readyState !== "loading") openBadge();
  else document.addEventListener("DOMContentLoaded", openBadge);
}})();
"""


def build_search_index():
    """Indeks wyszukiwarki: wszystkie pozycje cennika ze wszystkich kategorii.

    Nazwy uslug zostaja po polsku (tak jak w cenniku i w Booksy), ale kazda
    pozycja niesie swoj slug kategorii — dzieki temu wpisanie "манікюр" albo
    "lashes" trafia w kategorie, a nie w pusto.
    """
    items = []
    for c in CATEGORIES:
        for name, desc, dur, price in c["items"]:
            items.append({"n": name, "d": dur, "p": price, "c": c["slug"]})
    cat_names = {c["slug"]: {l: I18N.get(f"cat_{c['slug']}_name", {}).get(l, c["name"])
                             for l in LANGS} for c in CATEGORIES}
    return ("window.__SEARCH = " + json.dumps(items, ensure_ascii=False) + ";\n"
            "window.__CATNAMES = " + json.dumps(cat_names, ensure_ascii=False) + ";\n")


def build_app_js():
    return build_search_index() + r"""// Auto-generowane przez build.py — funkcje interaktywne.
(function(){
  "use strict";
  var $ = function(s,r){return (r||document).querySelector(s);};
  var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
  var visibleGallery = function(){ return $$(".gallery img").filter(function(im){return im.offsetParent!==null;}); };

  document.addEventListener("DOMContentLoaded", function(){
    reveal(); toTop(); faq(); lightbox(); calc(); filter(); beforeAfter(); share(); stickyCta(); search();
  });

  // Wyszukiwarka po cenniku: 92 pozycje z dziewieciu kategorii w jednym polu.
  // Dopasowuje nazwe uslugi (po polsku, tak jak w Booksy) ORAZ nazwe kategorii
  // w jezyku strony, wiec "манікюр" tez cos znajdzie.
  function search(){
    var box=$("#searchBox"); if(!box || !window.__SEARCH) return;
    var input=$("#searchInput",box), out=$("#searchOut",box), items=window.__SEARCH;
    var lang=(document.documentElement.lang||"pl").slice(0,2);
    var cats=window.__CATNAMES||{}, base=(lang==="pl"?"/":"/"+lang+"/");
    var T=window.I18N||{};

    // Nazwy uslug sa po polsku, wiec wpisane cyrylica "ламинирование" samo
    // z siebie nic nie znajdzie. Kilkanascie najczestszych hasel mapujemy
    // recznie na polski rdzen.
    var ALIAS={"ламин":"lamin","ламінув":"lamin","наращ":"przedluz","нарощ":"przedluz",
      "педикюр":"pedicure","маникюр":"manicure","манікюр":"manicure","массаж":"masaz",
      "масаж":"masaz","брови":"brwi","бровей":"brwi","ресниц":"rzes","вій":"rzes",
      "волос":"wlos",
      "гель":"zel","гел":"zel","шрам":"blizn","рубц":"blizn","коса":"warkocz","косич":"warkocz"};
    function norm(s){
      s=(s||"").toLowerCase();
      try{ s=s.normalize("NFD").replace(/[̀-ͯ]/g,""); }catch(e){}
      return s.replace(/ł/g,"l").replace(/ż|ź/g,"z").replace(/ę/g,"e").replace(/ą/g,"a")
              .replace(/ś/g,"s").replace(/ć/g,"c").replace(/ó/g,"o").replace(/ń/g,"n");
    }
    function expand(q){
      var out=[q];
      for(var k in ALIAS){ if(q.indexOf(k)>=0) out.push(ALIAS[k]); }
      return out;
    }
    function catName(slug){ return (cats[slug]&&cats[slug][lang])||slug; }

    function open(){ box.classList.add("on"); document.body.classList.add("search-open"); input.focus(); }
    function close(){ box.classList.remove("on"); document.body.classList.remove("search-open"); input.value=""; render(""); }

    function render(q){
      var nq=norm(q).trim();
      if(!nq){ out.innerHTML=""; box.classList.remove("has-results"); return; }
      var terms=expand(nq);
      var hits=items.filter(function(it){
        var n=norm(it.n), c=norm(catName(it.c));
        return terms.some(function(t){ return n.indexOf(t)>=0 || c.indexOf(t)>=0; });
      }).slice(0,12);
      box.classList.add("has-results");
      if(!hits.length){
        var none=(T.search_none&&T.search_none[lang])||"Brak wyników";
        out.innerHTML='<div class="s-none">'+none+"</div>";
        return;
      }
      out.innerHTML=hits.map(function(it){
        return '<a class="s-row" href="'+base+"usluga-"+it.c+'.html">'+
               '<span class="s-name">'+it.n+"</span>"+
               '<span class="s-cat">'+catName(it.c)+"</span>"+
               '<span class="s-dur">'+(it.d||"")+"</span>"+
               '<span class="s-price">'+it.p+"</span></a>";
      }).join("");
    }

    input.addEventListener("input", function(){ render(input.value); });
    $$("[data-search-open]").forEach(function(b){
      b.addEventListener("click", function(e){ e.preventDefault(); open(); });
    });
    var closeBtn=$(".s-close",box);
    if(closeBtn) closeBtn.addEventListener("click", close);
    box.addEventListener("click", function(e){ if(e.target===box) close(); });
    addEventListener("keydown", function(e){
      if(e.key==="Escape" && box.classList.contains("on")) close();
      else if(e.key==="/" && !box.classList.contains("on") &&
              !/^(INPUT|TEXTAREA)$/.test((e.target.tagName||""))){ e.preventDefault(); open(); }
    });
  }

  // Pasek "Zapisz sie" na dole dubluje przycisk z hero: na pierwszym ekranie
  // telefonu widac bylo trzy razy to samo CTA. Pokazujemy go dopiero za hero.
  function stickyCta(){
    var bar=document.querySelector(".mcta"), hero=$("#hero");
    if(!bar||!hero) return;
    function upd(){ document.body.classList.toggle("past-hero", scrollY > hero.offsetHeight*0.72); }
    upd(); addEventListener("scroll", upd, {passive:true}); addEventListener("resize", upd);
  }

  function reveal(){
    var els=$$(".reveal");
    if(!("IntersectionObserver" in window)){ els.forEach(function(e){e.classList.add("in");}); return; }
    var io=new IntersectionObserver(function(en){ en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add("in"); io.unobserve(x.target); } }); }, {threshold:0.12, rootMargin:"0px 0px -8% 0px"});
    els.forEach(function(e){ io.observe(e); });
  }

  function toTop(){
    var b=$("#toTop"); if(!b) return;
    addEventListener("scroll", function(){ b.classList.toggle("show", scrollY>500); });
    b.addEventListener("click", function(){ scrollTo({top:0, behavior:"smooth"}); });
  }

  function faq(){
    $$(".faq-item").forEach(function(it){
      var q=$(".faq-q",it), a=$(".faq-a",it);
      q.addEventListener("click", function(){ var o=it.classList.toggle("open"); a.style.maxHeight=o?a.scrollHeight+"px":"0"; });
    });
  }

  function lightbox(){
    var lb=$("#lightbox"); if(!lb) return;
    var img=$("#lbImg"), list=[], idx=0;
    function show(){ if(list[idx]) img.src=list[idx].src; }
    function open(i){ list=visibleGallery(); idx=i; show(); lb.classList.add("open"); document.body.style.overflow="hidden"; }
    function close(){ lb.classList.remove("open"); document.body.style.overflow=""; }
    function nav(d){ if(!list.length)return; idx=(idx+d+list.length)%list.length; show(); }
    document.addEventListener("click", function(e){
      var t=e.target; if(t.matches && t.matches(".gallery img")){ open(visibleGallery().indexOf(t)); }
    });
    $(".lb-close",lb).addEventListener("click", close);
    $(".lb-prev",lb).addEventListener("click", function(e){ e.stopPropagation(); nav(-1); });
    $(".lb-next",lb).addEventListener("click", function(e){ e.stopPropagation(); nav(1); });
    lb.addEventListener("click", function(e){ if(e.target===lb) close(); });
    addEventListener("keydown", function(e){ if(!lb.classList.contains("open"))return; if(e.key==="Escape")close(); else if(e.key==="ArrowLeft")nav(-1); else if(e.key==="ArrowRight")nav(1); });
  }

  function calc(){
    var box=$("#calc"); if(!box) return;
    var sumEl=$("#calcSum"), cntEl=$("#calcCount");
    function upd(){
      var s=0,n=0,from=false;
      $$("input[type=checkbox]",box).forEach(function(c){ if(c.checked){ s+=parseFloat(c.getAttribute("data-price"))||0; n++; if(c.getAttribute("data-from")==="1")from=true; } });
      sumEl.textContent=(from&&n?"od ":"")+Math.round(s)+" zł"; cntEl.textContent=n;
    }
    box.addEventListener("change", upd);
    var clr=$("#calcClear"); if(clr) clr.addEventListener("click", function(){ $$("input[type=checkbox]",box).forEach(function(c){c.checked=false;}); upd(); });
    upd();
  }

  function filter(){
    var f=$("#pfFilters"); if(!f) return;
    f.addEventListener("click", function(e){
      var b=e.target.closest("button"); if(!b) return;
      $$("button",f).forEach(function(x){x.classList.remove("active");}); b.classList.add("active");
      var flt=b.getAttribute("data-filter");
      $$("#pfGrid img").forEach(function(im){ im.classList.toggle("hide", flt!=="all" && im.getAttribute("data-cat")!==flt); });
    });
  }

  // Suwakow przed/po jest teraz kilka, wiec kazdy dostaje wlasna obsluge.
  // Doszla klawiatura: strzalki przesuwaja podzial, bo sam pointer wykluczal
  // czesc uzytkownikow.
  function beforeAfter(){
    $$(".ba").forEach(function(ba){
      var after=$(".ba-after",ba), line=$(".ba-line",ba), handle=$(".ba-handle",ba), drag=false, pos=50;
      if(!after||!line||!handle) return;
      function set(p){
        pos=Math.max(0,Math.min(100,p));
        after.style.clipPath="inset(0 0 0 "+pos+"%)";
        line.style.left=pos+"%"; handle.style.left=pos+"%";
        handle.setAttribute("aria-valuenow", Math.round(pos));
      }
      function fromX(x){ var r=ba.getBoundingClientRect(); set((x-r.left)/r.width*100); }
      ba.addEventListener("pointerdown", function(e){ drag=true; fromX(e.clientX); try{ba.setPointerCapture(e.pointerId);}catch(_){} });
      ba.addEventListener("pointermove", function(e){ if(drag){ e.preventDefault(); fromX(e.clientX); } });
      addEventListener("pointerup", function(){ drag=false; });
      handle.setAttribute("tabindex","0");
      handle.setAttribute("role","slider");
      handle.setAttribute("aria-valuemin","0");
      handle.setAttribute("aria-valuemax","100");
      handle.addEventListener("keydown", function(e){
        if(e.key==="ArrowLeft"){ e.preventDefault(); set(pos-4); }
        else if(e.key==="ArrowRight"){ e.preventDefault(); set(pos+4); }
        else if(e.key==="Home"){ e.preventDefault(); set(0); }
        else if(e.key==="End"){ e.preventDefault(); set(100); }
      });
      set(50);
    });
  }

  function share(){
    var url=location.origin+location.pathname.replace(/[^/]*$/,"")||location.href;
    var text="Salon Urody BAD ANGEL — Szczecin";
    var map={ wa:"https://wa.me/?text="+encodeURIComponent(text+" "+url),
      tg:"https://t.me/share/url?url="+encodeURIComponent(url)+"&text="+encodeURIComponent(text),
      fb:"https://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(url) };
    $$(".js-share").forEach(function(a){ a.href=map[a.getAttribute("data-net")]||url; });
    $$(".js-copy").forEach(function(b){
      b.addEventListener("click", function(){
        function done(){ var l=window.__lang||"pl", t=window.I18N&&window.I18N.share_copied;
          b.textContent=t?t[l]:"OK";
          setTimeout(function(){ var k=window.I18N&&window.I18N.share_copy; if(k)b.textContent=k[l]; },1600); }
        if(navigator.clipboard){ navigator.clipboard.writeText(url).then(done, function(){ prompt("Link:",url); }); }
        else { prompt("Link:",url); }
      });
    });
  }
})();
"""


def w(path, content):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(content)
    print("napisano", path)


def all_pages():
    pages = ["", "portfolio.html", "kalkulator.html"]
    pages += [f"usluga-{c['slug']}.html" for c in CATEGORIES]
    pages += [f"mistrz-{m['slug']}.html" for m in MASTERS]
    return pages


def build_sitemap():
    """Sitemap ze wszystkimi jezykami i wzajemnymi hreflang-ami."""
    today = date.today().isoformat()
    urls = ""
    for l in LANDINGS:  # jednojezyczne, bez hreflang
        urls += (f"  <url>\n    <loc>{SITE_URL}/{l['slug']}.html</loc>\n"
                 f"    <lastmod>{today}</lastmod>\n  </url>\n")
    for p in all_pages():
        links = "".join(
            f'    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}{U_lang(l, p)}"/>\n'
            for l in LANGS)
        links += (f'    <xhtml:link rel="alternate" hreflang="x-default"'
                  f' href="{SITE_URL}{U_lang("pl", p)}"/>\n')
        for l in LANGS:
            urls += (f"  <url>\n    <loc>{SITE_URL}{U_lang(l, p)}</loc>\n"
                     f"    <lastmod>{today}</lastmod>\n{links}  </url>\n")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f"{urls}</urlset>\n")


# Roboty asystentow AI. Czesc z nich (Google-Extended, Applebot-Extended)
# domyslnie NIE indeksuje tresci do odpowiedzi, dopoki nie dostanie zgody.
AI_BOTS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User",            # OpenAI / ChatGPT
    "ClaudeBot", "Claude-User", "Claude-SearchBot",        # Anthropic / Claude
    "PerplexityBot", "Perplexity-User",                    # Perplexity
    "Google-Extended",                                     # Gemini, AI Overviews
    "Applebot", "Applebot-Extended",                       # Siri, Apple Intelligence
    "Bingbot", "msnbot",                                   # Bing, Copilot
    "DuckAssistBot", "Amazonbot", "meta-externalagent",
    "CCBot", "cohere-ai", "YouBot", "Diffbot", "Timpibot",
]


def build_llms_txt():
    """/llms.txt — zwiezle fakty o salonie dla asystentow AI.

    ChatGPT, Perplexity czy Claude odpowiadaja z tego, co zdolaja wyczytac,
    i lubia zwiezly tekst z konkretami. Strona HTML jest dla ludzi, ten plik
    dla modeli: adres, godziny, pelny cennik i mapa podstron w jednym miejscu.
    """
    L = []
    L.append("# Salon Urody BAD ANGEL — Szczecin")
    L.append("")
    L.append("> Salon urody w ścisłym centrum Szczecina (aleja Wyzwolenia 5/10, "
             "wejście od ul. Małopolskiej). Manicure, pedicure, przedłużanie rzęs, "
             "brwi i laminacja, masaż, mikroneedling blizn "
             f"i rozstępów oraz warkoczyki. Ocena {RATING}/5 z {REVIEWS_COUNT} opinii. "
             "Obsługa po polsku, ukraińsku, rosyjsku i angielsku.")
    L.append("")
    L.append("## Fakty")
    L.append(f"- Nazwa: Salon Urody BAD ANGEL")
    L.append("- Adres: aleja Wyzwolenia 5/10, 70-552 Szczecin, Polska "
             "(wejście od ul. Małopolskiej)")
    L.append("- Dzielnica: Centrum / Śródmieście, obok placu Rodła")
    if PHONE:
        L.append(f"- Telefon: {PHONE}")
    L.append("- Godziny otwarcia: poniedziałek – niedziela, 09:00 – 20:00")
    L.append(f"- Ocena: {RATING}/5 ({REVIEWS_COUNT} opinii, Booksy)")
    L.append(f"- Rezerwacja: wyłącznie online przez Booksy — {BOOKSY}")
    L.append("- Płatność: gotówka i karta")
    L.append("- Języki obsługi: polski, ukraiński, rosyjski, angielski")
    L.append("- Udogodnienia: parking, Wi-Fi")
    L.append(f"- Strona: {SITE_URL}/")
    L.append("")
    L.append("## Cennik (PLN, ceny zgodne z Booksy)")
    for c in CATEGORIES:
        L.append("")
        L.append(f"### {c['name']} — {SITE_URL}/usluga-{c['slug']}.html")
        L.append(c["intro"])
        for name, desc, dur, price in c["items"]:
            L.append(f"- {name} — {price} — {dur}")
    L.append("")
    L.append("## Strony szczegółowe")
    for l in LANDINGS:
        L.append(f"- [{l['h1']}]({SITE_URL}/{l['slug']}.html): {l['desc']}")
    L.append("")
    L.append("## Zespół")
    for m in MASTERS:
        L.append(f"- {m['name']} — {SITE_URL}/mistrz-{m['slug']}.html")
    L.append("")
    L.append("## Częste pytania")
    for c in CATEGORIES:
        blk = CAT_SEO.get(c["slug"])
        if not blk:
            continue
        for qa in blk["faq"]:
            L.append(f"- **{qa['q']['pl']}** {qa['a']['pl']}")
    for l in LANDINGS:
        for q, a in l["faq"]:
            L.append(f"- **{q}** {a}")
    L.append("")
    L.append("## Wersje językowe")
    for lang in LANGS:
        L.append(f"- {LANG_LABEL[lang]}: {SITE_URL}{U_lang(lang)}")
    L.append("")
    return "\n".join(L)


def build_robots():
    ai = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
    return (f"User-agent: *\nAllow: /\n\n{ai}"
            f"Sitemap: {SITE_URL}/sitemap.xml\n")


def build_lang(lang):
    """Generuje komplet stron dla jednego jezyka.

    Polski (jezyk glowny) laduje w korzeniu pod tymi samymi nazwami plikow co
    dotad — zaindeksowane adresy zostaja bez zmian. Reszta w /uk/, /ru/, /en/.
    """
    global CUR
    CUR = lang
    sub = "" if lang == "pl" else lang
    if sub:
        os.makedirs(os.path.join(ROOT, sub), exist_ok=True)

    def wl(name, content):
        w(os.path.join(sub, name) if sub else name, content)

    wl("index.html", build_index())
    wl("portfolio.html", build_portfolio())
    wl("kalkulator.html", build_calculator())
    for c in CATEGORIES:
        wl(f"usluga-{c['slug']}.html", build_service(c))
    for m in MASTERS:
        wl(f"mistrz-{m['slug']}.html", build_master(m))
    if lang == "pl":
        for l in LANDINGS:
            wl(f"{l['slug']}.html", build_landing(l))

    # sprzatanie stron po usunietych mistrzyniach/uslugach
    valid = ({f"usluga-{c['slug']}.html" for c in CATEGORIES}
             | {f"mistrz-{m['slug']}.html" for m in MASTERS})
    base = os.path.join(ROOT, sub) if sub else ROOT
    for p in glob.glob(os.path.join(base, "usluga-*.html")) + glob.glob(os.path.join(base, "mistrz-*.html")):
        if os.path.basename(p) not in valid:
            os.remove(p)
            print("usunięto", os.path.relpath(p, ROOT))
    # adresy, ktore zdazyly trafic do Google, dostaja przekierowanie zamiast 404
    for name, target in REMOVED_PAGES.items():
        if name in valid or (sub and not name.startswith(("usluga-", "mistrz-"))):
            continue
        wl(name, redirect_html(U_lang(lang, target)))


# Strony zdjete ze strony (oferta/zespol wg Booksy, 2026-09-15) -> dokad odsylac.
# Landingi sa tylko po polsku, wiec w /uk /ru /en powstaja same usluga-/mistrz-.
REMOVED_PAGES = {
    "usluga-depilacja.html": "index.html#uslugi",
    "depilacja-woskiem-szczecin.html": "index.html#uslugi",
    "mistrz-lidia.html": "index.html#zespol",
    "mistrz-anna.html": "index.html#zespol",
    "mistrz-aryna.html": "index.html#zespol",
}


def redirect_html(url):
    canon = url.split("#")[0].replace("index.html", "")
    return (f'<!doctype html><html lang="pl"><head><meta charset="utf-8">'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}{canon}">'
            f'<meta http-equiv="refresh" content="0;url={url}"><title>Przekierowanie</title></head>'
            f'<body><a href="{url}">Przejdź na stronę salonu</a></body></html>\n')


def main():
    global CUR
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    CUR = "pl"
    w("sitemap.xml", build_sitemap())
    w("robots.txt", build_robots())
    w("llms.txt", build_llms_txt())
    if DOMAIN:
        w("CNAME", DOMAIN + "\n")
    w("styles.css", CSS.strip() + "\n")
    w("translations.js", build_translations_js())
    w("app.js", build_app_js())
    for lang in LANGS:
        build_lang(lang)
    CUR = "pl"
    w("README.md", build_readme())
    save_img_sizes()
    report_price_misses()
    print(f"Gotowe — {len(LANGS)} jezyki x {len(all_pages())} stron.")


if __name__ == "__main__":
    main()
