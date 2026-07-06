#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator statycznej strony Salon Urody BAD ANGEL.
Tworzy: styles.css, index.html, strony usług (usluga-*.html),
strony mastrów (mistrz-*.html) oraz README z listą potrzebnych zdjęć.
Rezerwacja każdej usługi prowadzi na Booksy.
"""
import os
import glob
import json
from i18n import LANGS, LANG_LABEL, HTML_KEYS, REVIEWS, flat as _i18n_flat

I18N = _i18n_flat()

def P(key):
    """Polski tekst domyslny (inline w HTML)."""
    return I18N[key]["pl"]

ROOT = os.path.dirname(os.path.abspath(__file__))
VER = "8"  # cache-busting wersja dla styles.css / translations.js / app.js
BOOKSY = "https://booksy.com/pl-pl/14573_salon-urody-bad-angel_salon-kosmetyczny_18078_szczecin"
IG = "https://www.instagram.com/"
FB = "https://www.facebook.com/"

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
    dict(slug="depilacja", name="Depilacja", tag="Gładka skóra",
         lead="Gładkość, która trwa",
         intro="Depilacja woskiem w komfortowych warunkach. "
               "Pojedyncze partie oraz wygodne pakiety.",
         items=[
             ("Broda", "", "30 min", "45 zł"),
             ("Pachy", "", "30 min", "54 zł"),
             ("Bikini pełne", "", "1 g 15 min", "od 135 zł"),
             ("Nogi całe", "", "1 g 15 min", "144 zł"),
             ("Bikini + nogi + pachy", "Pakiet kompletny.", "2 g 30 min", "315 zł"),
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
    dict(slug="wlosy", name="Włosy", tag="Fryzjer",
         lead="Fryzury, które podkreślają Twój styl",
         intro="Przedłużanie włosów (naturalne i syntetyczne), warkoczyki, a także strzyżenia "
               "damskie i męskie, modelowanie i regeneracja włosów.",
         items=[
             ("Przedłużanie włosów naturalne (cena bez włosów)", "Zagęszczenie i wydłużenie włosów naturalnymi pasmami.", "4 g", "od 600 zł"),
             ("Przedłużanie włosów syntetyczne (cena z włosami)", "Przedłużanie z pasmami syntetycznymi w komplecie.", "4 g", "od 600 zł"),
             ("Warkoczyki syntetyczne", "Pojedyncze warkoczyki syntetyczne.", "30 min", "od 20 zł"),
             ("Warkoczyki syntetyczne (pełne)", "Pełna głowa warkoczyków.", "2 g", "od 250 zł"),
             ("Strzyżenie damskie", "Strzyżenie z uwzględnieniem cech i kształtu twarzy.", "1 g", "od 80 zł"),
             ("Strzyżenie męskie", "", "45 min", "60 zł"),
             ("Modelowanie / stylizacja", "Mycie, suszenie i stylizacja.", "45 min", "od 70 zł"),
             ("Regeneracja włosów (zimna odbudowa)", "Głęboka pielęgnacja i odbudowa struktury włosa.", "1 g", "od 150 zł"),
             ("Upięcie okolicznościowe", "Fryzura na specjalną okazję.", "1 g", "od 150 zł"),
         ]),
]

# Mastrzy. slug -> mistrz-<slug>.html, zdjęcie assets/mistrz-<slug>.jpg
MASTERS = [
    dict(slug="angelina", name="Angelina", gen="Angeliny", role="Paznokcie i stylizacja brwi",
         serves=["manicure", "brwi", "spa"],
         bio=[
             "Wykwalifikowana specjalistka beauty, dla której liczą się estetyka i jakość. "
             "Łączy techniczną precyzję, artystyczny smak i uważne podejście do każdego klienta.",
             "Manicure i pedicure wykonuje z uwzględnieniem anatomii dłoni i stóp — jej pokrycia są "
             "trwałe, wygodne i estetyczne. Biegle włada technikami nail-artu, w tym klasycznym i "
             "nowoczesnym frenchem.",
             "Zajmuje się też stylizacją brwi: laminacją z trwałym efektem oraz koloryzacją dobraną "
             "indywidualnie do rysów twarzy.",
         ]),
    dict(slug="weronika", name="Weronika", gen="Weroniki", role="Manicure, pedicure i brwi",
         serves=["manicure", "pedicure", "brwi"],
         bio=[
             "Mistrzyni manicure i pedicure oraz stylistka brwi. Stawia na estetyczny, naturalny "
             "efekt i komfort podczas każdej wizyty.",
             "Manicure i pedicure wykonuje od dwóch lat, a od roku zajmuje się laminacją i "
             "koloryzacją brwi — z dbałością o detal i kondycję włosków.",
             "Do każdej klientki podchodzi indywidualnie, dobierając pielęgnację i stylizację do "
             "jej potrzeb.",
         ]),
    dict(slug="lidia", name="Lidia", gen="Lidii", role="Przedłużanie paznokci",
         serves=["manicure", "pedicure"],
         bio=[
             "Lidia to specjalistka od długich, efektownych form. Buduje paznokcie z dbałością "
             "o architekturę i idealny łuk.",
             "Wykonuje przedłużanie żelem w każdej długości, odnowy oraz pełny pedicure. "
             "Chętnie pracuje z modelkami i cierpliwie dopracowuje każdy detal.",
             "Atmosfera na jej fotelu jest miła i sympatyczna, a efekt zawsze na miarę oczekiwań.",
         ]),
    dict(slug="wiktoria", name="Wiktoria", gen="Wiktorii", role="Mikroneedling i zabiegi na skórę",
         serves=["blizny", "depilacja"],
         bio=[
             "Specjalistka mikroneedlingu po szkoleniach w Akademii LIBRO w Warszawie. Skupia się "
             "na terapii regeneracyjnej blizn, rozstępów, śladów po trądziku i przebarwień oraz "
             "poprawie jakości i gęstości skóry.",
             "Posiada międzynarodową akredytację KCCK z wyróżnieniem oraz certyfikat Global "
             "Creative Masters. Stale podnosi kwalifikacje — m.in. egzosomy i polinukleotydy w mikroneedlingu.",
             "Każdy etap zabiegu dokładnie wyjaśnia, a efekty jej pracy widoczne są już po "
             "pierwszej wizycie.",
         ]),
    dict(slug="wiktoria-masaz", name="Wiktoria", gen="Wiktorii", role="Masaż",
         serves=["masaz"],
         bio=[
             "Wiktoria to specjalistka od relaksu i regeneracji ciała. Wykonuje masaże, które "
             "przynoszą ulgę napiętym mięśniom i pomagają odzyskać równowagę.",
             "W jej ofercie znajdziesz masaże relaksacyjne, lecznicze i antycellulitowe, a także "
             "masaż twarzy i pielęgnacyjne rytuały dla całego ciała.",
             "Każdy etap masażu dopasowuje do potrzeb i samopoczucia klienta.",
         ]),
    dict(slug="anna", name="Anna", gen="Anny", role="Mistrzyni fryzjerstwa",
         serves=["wlosy"],
         bio=[
             "Doświadczona fryzjerka z ponad 20-letnim stażem w branży beauty. Profesjonalnie "
             "włada technikami nowoczesnych strzyżeń, realizując prace o każdym stopniu trudności "
             "z uwzględnieniem indywidualnych cech klienta.",
             "Specjalizuje się w zabiegach głębokiej pielęgnacji, w tym zimnej regeneracji włosów, "
             "oraz w tworzeniu stylowych upięć i stylizacji na każdą okazję.",
             "Odpowiedzialnie podchodzi do jakości usług i pomaga dobrać fryzurę, która podkreśli "
             "indywidualność klienta.",
         ]),
    dict(slug="astgik", name="Astgik", gen="Astgik", role="Pedicure",
         serves=["pedicure"],
         bio=[
             "Astgik to specjalistka pedicure. Dba o zdrowy wygląd i pielęgnację stóp, łącząc "
             "precyzję z komfortem zabiegu.",
             "Wykonuje pedicure klasyczny, hybrydowy oraz pełne opracowanie stóp z pielęgnacją "
             "pięt. Efekt jest estetyczny i trwały.",
             "Do każdej wizyty podchodzi indywidualnie, aby Twoje stopy były zadbane i wypoczęte.",
         ]),
    dict(slug="aryna", name="Aryna", gen="Aryny", role="Przedłużanie włosów i warkoczyki",
         serves=["wlosy"],
         bio=[
             "Aryna to stylistka włosów specjalizująca się w przedłużaniu i zagęszczaniu włosów "
             "oraz kolorowych warkoczykach.",
             "Wykonuje przedłużanie włosów naturalnych i syntetycznych, a także efektowne "
             "warkoczyki — od pojedynczych po pełne, fantazyjne stylizacje.",
             "Pomaga uzyskać wymarzoną długość, objętość i kolor, dbając o wygodę i trwałość każdej fryzury.",
         ]),
]

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """
:root{
  --black:#0a0a0a;--white:#fff;--grey:#8a8a8a;--line:rgba(255,255,255,.14);
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  --serif:'Cormorant Garamond',Georgia,serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--white);background:#000;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}

/* NAV */
header{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;
  padding:18px 28px;transition:background .4s,box-shadow .4s;mix-blend-mode:difference}
header.solid{mix-blend-mode:normal;background:rgba(8,8,9,.82);backdrop-filter:blur(10px);box-shadow:0 1px 0 rgba(255,255,255,.08)}
header .brand{font-family:var(--serif);font-size:22px;letter-spacing:.32em;font-weight:500;padding-left:.32em}
header nav{display:flex;gap:30px}
header nav a{font-size:13px;font-weight:500;letter-spacing:.02em;padding:6px 4px;opacity:.95;transition:opacity .2s}
header nav a:hover{opacity:.6}
.nav-cta{display:flex;gap:14px;align-items:center}
.lang-switch{display:flex;align-items:center;gap:2px}
.lang-switch button{appearance:none;-webkit-appearance:none;background:transparent;border:0;color:currentColor;
  font-family:var(--sans);font-size:12px;font-weight:500;letter-spacing:.12em;padding:5px 7px;cursor:pointer;
  opacity:.42;transition:opacity .2s;line-height:1}
.lang-switch button:hover{opacity:.8}
.lang-switch button.active{opacity:1;text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.drawer .lang-switch{margin-top:28px;gap:10px;justify-content:flex-start}
.drawer .lang-switch button{font-size:15px;letter-spacing:.14em;padding:8px 12px;border:1px solid var(--line);border-radius:40px;opacity:.6}
.drawer .lang-switch button.active{opacity:1;text-decoration:none;background:#fff;color:#111;border-color:#fff}
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
.btn.solid{background:rgba(255,255,255,.92);color:#111}
.btn.solid:hover{background:#fff}
.btn.ghost{background:rgba(30,30,30,.5);color:#fff}
.btn.ghost:hover{background:rgba(60,60,60,.7)}
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
#hero .logo{width:min(720px,90vw);margin:0 auto;filter:drop-shadow(0 6px 30px rgba(0,0,0,.5))}
.panel .top{padding-top:22vh}
.panel .bottom{margin-top:auto;padding-bottom:56px;width:100%}
.panel h1{font-family:var(--serif);font-size:clamp(48px,9vw,104px);font-weight:400;letter-spacing:.02em;line-height:1.02}
#hero .rating{margin-top:14px;font-size:14px;letter-spacing:.06em;opacity:.9}

/* SECTION headers */
.section-head{text-align:center;margin-bottom:64px}
.section-head h2{font-family:var(--serif);font-size:clamp(36px,5vw,60px);font-weight:400}
.section-head p{margin-top:14px;color:var(--grey);font-weight:300;letter-spacing:.03em}
section.block{padding:120px 24px}

/* SERVICE CARDS (photo) */
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#0b0b0c;
  transition:transform .3s,border-color .3s;text-decoration:none}
.card:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.32)}
.card .thumb{aspect-ratio:4/5;background-size:cover;background-position:center}
.card .cap{padding:22px 20px 24px}
.card h3{font-family:var(--serif);font-size:24px;font-weight:400}
.card .price{font-size:13px;color:var(--grey);margin-top:6px;letter-spacing:.04em}
.card .go{font-size:12px;letter-spacing:.06em;color:#fff;margin-top:14px;opacity:.55;transition:opacity .3s}
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
.gallery img{width:100%;margin:0 0 14px;border-radius:8px;display:block;break-inside:avoid;
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
  .grid{grid-template-columns:1fr}
  .team{grid-template-columns:1fr 1fr}
  .price-item .book{width:100%}
  .price-item .book .btn{width:100%}
}

/* ---- REVEAL (animacje scrollem) ---- */
.reveal{transition:opacity .7s ease,transform .7s ease}
.js .reveal{opacity:0;transform:translateY(26px)}
.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.js .reveal{opacity:1;transform:none;transition:none}}

/* ---- BACK TO TOP + MOBILE CTA ---- */
.to-top{position:fixed;right:20px;bottom:20px;z-index:90;width:46px;height:46px;border-radius:50%;
  background:rgba(20,20,22,.82);backdrop-filter:blur(8px);border:1px solid var(--line);color:#fff;cursor:pointer;
  display:flex;align-items:center;justify-content:center;font-size:20px;opacity:0;pointer-events:none;transition:opacity .3s}
.to-top.show{opacity:1;pointer-events:auto}
.to-top:hover{background:rgba(45,45,50,.92)}
.mcta{position:fixed;left:0;right:0;bottom:0;z-index:95;display:none;padding:11px 14px;
  background:rgba(8,8,9,.94);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
.mcta .btn{display:block;min-width:0;width:100%}
@media(max-width:760px){.mcta{display:block}.to-top{bottom:78px;right:16px}}

/* ---- OPEN NOW BADGE ---- */
.open-badge{display:inline-flex;align-items:center;gap:9px;font-size:13px;letter-spacing:.03em;margin-top:14px;
  padding:7px 14px;border-radius:40px;border:1px solid var(--line);color:#dcdce0}
.open-badge::before{content:"";width:8px;height:8px;border-radius:50%;background:#888}
.open-badge.open::before{background:#48c774;box-shadow:0 0 0 3px rgba(72,199,116,.22)}
.open-badge.closed::before{background:#e06060}

/* ---- FAQ ---- */
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
.gift-art{background:url('assets/emblem.png') center/58% no-repeat, radial-gradient(120% 120% at 30% 20%,#241d14,#0a0a0c);
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
.ba{max-width:720px;margin:44px auto 0;position:relative;aspect-ratio:4/3;border-radius:12px;overflow:hidden;
  border:1px solid var(--line);user-select:none;touch-action:none;cursor:ew-resize}
.ba .ba-img{position:absolute;inset:0;background-size:cover;background-position:center}
.ba .ba-after{clip-path:inset(0 0 0 50%)}
.ba .ba-line{position:absolute;top:0;bottom:0;left:50%;width:2px;background:#fff;transform:translateX(-1px);box-shadow:0 0 12px rgba(0,0,0,.5)}
.ba .ba-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;
  background:rgba(255,255,255,.95);display:flex;align-items:center;justify-content:center;color:#111;font-size:15px;box-shadow:0 4px 16px rgba(0,0,0,.4)}
.ba .ba-tag{position:absolute;bottom:14px;font-size:11px;letter-spacing:.16em;font-weight:600;color:#fff;
  background:rgba(0,0,0,.5);padding:5px 11px;border-radius:40px;backdrop-filter:blur(4px)}
.ba .ba-tag.l{left:14px}.ba .ba-tag.r{right:14px}
"""

# ---------------------------------------------------------------------------
# SZABLONY
# ---------------------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500'
         '&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">')


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/emblem.png">
{FONTS}
<link rel="stylesheet" href="styles.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
<script defer src="translations.js?v={VER}"></script>
<script defer src="app.js?v={VER}"></script>
</head>
<body>"""


def lang_switch():
    btns = "".join(f'<button data-lang="{l}" onclick="__setLang(\'{l}\')">{LANG_LABEL[l]}</button>' for l in LANGS)
    return f'<div class="lang-switch">{btns}</div>'


def header_html():
    return f"""
<header id="topbar">
  <a href="index.html" class="brand">BAD&nbsp;ANGEL</a>
  <nav>
    <a href="index.html#uslugi" data-i18n="nav_services">{P('nav_services')}</a>
    <a href="portfolio.html" data-i18n="nav_portfolio">{P('nav_portfolio')}</a>
    <a href="kalkulator.html" data-i18n="nav_calc">{P('nav_calc')}</a>
    <a href="index.html#zespol" data-i18n="nav_team">{P('nav_team')}</a>
    <a href="index.html#kontakt" data-i18n="nav_contact">{P('nav_contact')}</a>
  </nav>
  <div class="nav-cta">
    {lang_switch()}
    <a class="btn solid sm" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book">{P('btn_book')}</a>
    <button class="burger" aria-label="Menu" onclick="document.getElementById('drawer').classList.add('open')">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="drawer" id="drawer">
  <button class="close" onclick="document.getElementById('drawer').classList.remove('open')">&times;</button>
  <a href="index.html#uslugi" onclick="closeDrawer()" data-i18n="nav_services">{P('nav_services')}</a>
  <a href="portfolio.html" onclick="closeDrawer()" data-i18n="nav_portfolio">{P('nav_portfolio')}</a>
  <a href="kalkulator.html" onclick="closeDrawer()" data-i18n="nav_calc">{P('nav_calc')}</a>
  <a href="index.html#zespol" onclick="closeDrawer()" data-i18n="nav_team">{P('nav_team')}</a>
  <a href="index.html#opinie" onclick="closeDrawer()" data-i18n="nav_reviews">{P('nav_reviews')}</a>
  <a href="index.html#kontakt" onclick="closeDrawer()" data-i18n="nav_contact">{P('nav_contact')}</a>
  <a href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="book_online">{P('book_online')}</a>
  {lang_switch()}
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
    return f"background:url('{img_path}') center/cover, {fallback};"


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
def build_index():
    cards = ""
    grads = ["linear-gradient(150deg,#26201d,#0a0a0c)", "linear-gradient(150deg,#1d2226,#0a0a0c)",
             "linear-gradient(150deg,#231d24,#0a0a0c)", "linear-gradient(150deg,#20261f,#0a0a0c)"]
    for i, c in enumerate(CATEGORIES):
        g = grads[i % len(grads)]
        s = c['slug']
        cards += f"""
        <a class="card" href="usluga-{s}.html">
          <div class="thumb" style="{bg('assets/usluga-'+s+'.jpg', g)}"></div>
          <div class="cap">
            <h3 data-i18n="cat_{s}_name">{c['name']}</h3>
            <div class="price">{len(c['items'])} <span data-i18n="unit_uslug">{P('unit_uslug')}</span> · {c['items'][0][3]}</div>
            <div class="go" data-i18n="card_cta">{P('card_cta')}</div>
          </div>
        </a>"""

    members = ""
    for m in MASTERS:
        members += f"""
        <a class="member" href="mistrz-{m['slug']}.html">
          <div class="ph" data-i="{m['name'][0]}" style="{bg('assets/mistrz-'+m['slug']+'.jpg','linear-gradient(160deg,#26262c,#0e0e11)')}"></div>
          <h4>{m['name']}</h4><span data-i18n="role_{m['slug']}">{m['role']}</span>
        </a>"""

    rv = ""
    for i, r in enumerate(REVIEWS):
        rv += f"""
        <div class="review"><div class="stars">★★★★★</div><p>„<span data-i18n="rev{i}_text">{r['text']['pl']}</span>”</p>
          <div class="who"><b>{r['who']}</b> · <span data-i18n="rev{i}_svc">{r['svc']['pl']}</span></div></div>"""

    html = head("Salon Urody BAD ANGEL — Szczecin",
                "Salon Urody BAD ANGEL w Szczecinie. Manicure, pedicure, przedłużanie rzęs, masaż, depilacja. Ocena 4.9 — 1246 opinii.")
    html += header_html()
    html += f"""
<main>
  <section class="panel" id="hero">
    <div class="bg"></div>
    <div class="top">
      <div class="eyebrow" data-i18n="hero_eyebrow">{P('hero_eyebrow')}</div>
      <img class="logo" src="assets/logo.png" alt="BAD ANGEL Beauty Salon">
      <div class="rating"><span class="stars">★★★★★</span> &nbsp;<span data-i18n="hero_rating">{P('hero_rating')}</span></div>
    </div>
    <div class="bottom"><div class="btns">
      <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
      <a class="btn ghost" href="#uslugi" data-i18n="btn_see_services">{P('btn_see_services')}</a>
    </div></div>
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
      <div class="btns"><a class="btn solid" href="usluga-manicure.html" data-i18n="btn_see_services">{P('btn_see_services')}</a></div>
    </div>
  </section>
  <section class="split reveal">
    <div class="body">
      <div class="eyebrow" data-i18n="feat2_eyebrow">{P('feat2_eyebrow')}</div>
      <h2 data-i18n="feat2_title">{P('feat2_title')}</h2>
      <p data-i18n="feat2_text">{P('feat2_text')}</p>
      <div class="btns"><a class="btn solid" href="usluga-rzesy.html" data-i18n="btn_see_services">{P('btn_see_services')}</a></div>
    </div>
    <div class="media" style="{bg('assets/feature-lashes.jpg','linear-gradient(135deg,#221a1f,#0a0a0c)')}"></div>
  </section>

  <section class="block" id="efekty" style="background:#0b0b0c">
    <div class="wrap">
      <div class="section-head reveal"><h2 data-i18n="ba_title">{P('ba_title')}</h2><p data-i18n="ba_sub">{P('ba_sub')}</p></div>
      <div class="ba reveal" id="baSlider">
        <div class="ba-img ba-before" style="background-image:url('assets/ba-before.jpg')"></div>
        <div class="ba-img ba-after" style="background-image:url('assets/ba-after.jpg')"></div>
        <span class="ba-tag l" data-i18n="ba_before">{P('ba_before')}</span>
        <span class="ba-tag r" data-i18n="ba_after">{P('ba_after')}</span>
        <div class="ba-line"></div>
        <div class="ba-handle">⇄</div>
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
      <div class="section-head reveal"><h2 data-i18n="sec_reviews_title">{P('sec_reviews_title')}</h2><p><span class="stars">★★★★★</span> &nbsp;<span data-i18n="sec_reviews_sub">{P('sec_reviews_sub')}</span></p></div>
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

    html = head(f"{c['name']} — Salon Urody BAD ANGEL Szczecin",
                f"{c['name']} w Salonie Urody BAD ANGEL w Szczecinie. {c['intro']}")
    html += header_html()
    # Galeria — zdjęcia z assets/gallery/<slug>/
    gdir = os.path.join(ROOT, "assets", "gallery", c["slug"])
    gfiles = sorted(os.path.basename(p) for p in glob.glob(os.path.join(gdir, "*.jpg")))
    gallery = ""
    if gfiles:
        imgs = "".join(
            f'<img loading="lazy" src="assets/gallery/{c["slug"]}/{fn}" alt="{c["name"]} — Salon Urody BAD ANGEL Szczecin">'
            for fn in gfiles)
        gallery = f"""
  <section class="block" style="background:#000;padding-top:40px">
    <div class="section-head reveal"><h2 data-i18n="gallery_title">{P('gallery_title')}</h2><p>{len(gfiles)} <span data-i18n="gallery_photos">{P('gallery_photos')}</span></p></div>
    <div class="gallery"><div class="cols">{imgs}</div></div>
  </section>"""

    html += f"""
<main>
  <section class="subhero">
    <div class="bg" style="{bg('assets/usluga-'+c['slug']+'.jpg','linear-gradient(150deg,#20202a,#0a0a0c)')}"></div>
    <div class="scrim"></div>
    <div class="crumbs"><a href="index.html" data-i18n="crumb_home">{P('crumb_home')}</a> &nbsp;/&nbsp; <a href="index.html#uslugi" data-i18n="nav_services">{P('nav_services')}</a> &nbsp;/&nbsp; <span data-i18n="cat_{c['slug']}_name">{c['name']}</span></div>
    <div class="inner">
      <div class="eyebrow" data-i18n="cat_{c['slug']}_tag">{c['tag']}</div>
      <h1 data-i18n="cat_{c['slug']}_name">{c['name']}</h1>
      <p class="lead" data-i18n="cat_{c['slug']}_lead">{c['lead']}</p>
    </div>
  </section>

  <section class="intro-band"><p data-i18n="cat_{c['slug']}_intro">{c['intro']}</p></section>

  <section class="pricelist">
    {rows}
    <div class="btns" style="margin-top:50px">
      <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="svc_book_booksy">{P('svc_book_booksy')}</a>
      <a class="btn ghost" href="index.html#uslugi" data-i18n="svc_other">{P('svc_other')}</a>
    </div>
  </section>
{gallery}
</main>"""
    html += footer_html()
    return html


# ---------------------------------------------------------------------------
# STRONA MASTRA
# ---------------------------------------------------------------------------
def build_master(m):
    cat_by_slug = {c["slug"]: c for c in CATEGORIES}
    chips = ""
    for s in m["serves"]:
        if s in cat_by_slug:
            chips += f'<a class="chip" href="usluga-{s}.html" data-i18n="cat_{s}_name">{cat_by_slug[s]["name"]}</a>'
    bio = "".join(f'<p data-i18n="bio_{m["slug"]}_{i}">{p}</p>' for i, p in enumerate(m["bio"]))

    html = head(f"{m['name']} — {m['role']} · Salon Urody BAD ANGEL",
                f"{m['name']} — {m['role']} w Salonie Urody BAD ANGEL w Szczecinie. Poznaj naszą specjalistkę i zarezerwuj wizytę.")
    html += header_html()
    html += f"""
<main>
  <div class="crumbs" style="position:relative;top:96px;margin:0 auto;max-width:1100px;padding:0 24px">
    <a href="index.html" data-i18n="crumb_home">{P('crumb_home')}</a> &nbsp;/&nbsp; <a href="index.html#zespol" data-i18n="nav_team">{P('nav_team')}</a> &nbsp;/&nbsp; {m['name']}
  </div>
  <section class="master">
    <div class="portrait" style="{bg('assets/mistrz-'+m['slug']+'.jpg','linear-gradient(160deg,#26262c,#0e0e11)')}"></div>
    <div>
      <div class="role" data-i18n="role_{m['slug']}">{m['role']}</div>
      <h1>{m['name']}</h1>
      <div class="bio">{bio}</div>
      <div class="serves">
        <div class="k"><span data-i18n="master_services_by">{P('master_services_by')}</span> {m['gen']}</div>
        {chips}
      </div>
      <div class="btns" style="justify-content:flex-start;padding:0;margin-top:40px">
        <a class="btn solid" href="{BOOKSY}" target="_blank" rel="noopener" data-i18n="btn_book_visit">{P('btn_book_visit')}</a>
        <a class="btn ghost" href="index.html#zespol" data-i18n="master_all_team">{P('master_all_team')}</a>
      </div>
    </div>
  </section>
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
        <summary><span data-i18n="cat_{c['slug']}_name">{c['name']}</span></summary>{rows}
      </details>"""
    html = head("Kalkulator cen — Salon Urody BAD ANGEL",
                "Kalkulator orientacyjnych cen usług Salon Urody BAD ANGEL w Szczecinie.")
    html += header_html()
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
        fbtns += f'<button data-filter="{s}" data-i18n="cat_{s}_name">{name_by[s]}</button>'
    imgs = "".join(f'<img loading="lazy" data-cat="{s}" src="assets/gallery/{s}/{fn}" alt="Salon Urody BAD ANGEL">'
                   for s, fn in items)
    html = head("Portfolio — Salon Urody BAD ANGEL Szczecin",
                "Portfolio prac Salon Urody BAD ANGEL w Szczecinie — manicure, pedicure, rzęsy, brwi.")
    html += header_html()
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
    return f"""// Auto-generowane przez build.py — tlumaczenia i przelacznik jezyka.
window.I18N = {data};
(function(){{
  var LS = "ba_lang", LANGS = {langs};
  function apply(lang){{
    if(LANGS.indexOf(lang) < 0) lang = "pl";
    document.documentElement.lang = lang;
    var T = window.I18N;
    document.querySelectorAll("[data-i18n]").forEach(function(e){{
      var t = T[e.getAttribute("data-i18n")]; if(t && t[lang] != null) e.textContent = t[lang];
    }});
    document.querySelectorAll("[data-i18n-html]").forEach(function(e){{
      var t = T[e.getAttribute("data-i18n-html")]; if(t && t[lang] != null) e.innerHTML = t[lang];
    }});
    document.querySelectorAll(".lang-switch button").forEach(function(b){{
      b.classList.toggle("active", b.getAttribute("data-lang") === lang);
    }});
    // badge "otwarte teraz" (09:00-20:00 codziennie)
    document.querySelectorAll("[data-open-badge]").forEach(function(e){{
      var hh = new Date().getHours(), open = hh >= 9 && hh < 20, k = open ? "open_now" : "closed_now";
      if(T[k]) e.textContent = T[k][lang];
      e.classList.toggle("open", open); e.classList.toggle("closed", !open);
    }});
    window.__lang = lang;
    if(window.__afterLang) window.__afterLang(lang);
    try{{ localStorage.setItem(LS, lang); }}catch(e){{}}
  }}
  window.__setLang = apply;
  var saved = null;
  try{{ saved = localStorage.getItem(LS); }}catch(e){{}}
  if(!saved){{
    var nl = (navigator.language || "pl").slice(0,2).toLowerCase();
    saved = LANGS.indexOf(nl) >= 0 ? nl : "pl";
  }}
  if(document.readyState !== "loading") apply(saved);
  else document.addEventListener("DOMContentLoaded", function(){{ apply(saved); }});
}})();
"""


def build_app_js():
    return r"""// Auto-generowane przez build.py — funkcje interaktywne.
(function(){
  "use strict";
  var $ = function(s,r){return (r||document).querySelector(s);};
  var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
  var visibleGallery = function(){ return $$(".gallery img").filter(function(im){return im.offsetParent!==null;}); };

  document.addEventListener("DOMContentLoaded", function(){
    reveal(); toTop(); faq(); lightbox(); calc(); filter(); beforeAfter(); share();
  });

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

  function beforeAfter(){
    var ba=$("#baSlider"); if(!ba) return;
    var after=$(".ba-after",ba), line=$(".ba-line",ba), handle=$(".ba-handle",ba), drag=false;
    function set(p){ p=Math.max(0,Math.min(100,p)); after.style.clipPath="inset(0 0 0 "+p+"%)"; line.style.left=p+"%"; handle.style.left=p+"%"; }
    function fromX(x){ var r=ba.getBoundingClientRect(); set((x-r.left)/r.width*100); }
    ba.addEventListener("pointerdown", function(e){ drag=true; fromX(e.clientX); try{ba.setPointerCapture(e.pointerId);}catch(_){} });
    ba.addEventListener("pointermove", function(e){ if(drag){ e.preventDefault(); fromX(e.clientX); } });
    addEventListener("pointerup", function(){ drag=false; });
    set(50);
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


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    w("styles.css", CSS.strip() + "\n")
    w("translations.js", build_translations_js())
    w("app.js", build_app_js())
    w("index.html", build_index())
    w("portfolio.html", build_portfolio())
    w("kalkulator.html", build_calculator())
    for c in CATEGORIES:
        w(f"usluga-{c['slug']}.html", build_service(c))
    for m in MASTERS:
        w(f"mistrz-{m['slug']}.html", build_master(m))
    w("README.md", build_readme())
    print("Gotowe.")


if __name__ == "__main__":
    main()
