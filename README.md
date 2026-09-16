# Salon Urody BAD ANGEL — strona

Statyczna strona (bez zależności). Otwórz przez lokalny serwer:

```
cd "Salon Urody BAD ANGEL"
python3 -m http.server 8777
# http://localhost:8777
```

Regeneracja stron po zmianie danych: `python3 build.py`

## Zdjęcia — wrzuć do folderu `assets/` (nazwy dokładnie takie):

Do czasu dodania plików w tych miejscach wyświetla się elegancki ciemny gradient.

**Tło / sekcje główne:**
- `assets/hero.jpg` — duże tło hero na stronie głównej (opcjonalnie, np. wnętrze salonu)
- `assets/feature-nails.jpg` — sekcja „Paznokcie”
- `assets/feature-lashes.jpg` — sekcja „Rzęsy i brwi”

**Usługi (kafelki + baner podstrony):**
- `assets/usluga-manicure.jpg` — Manicure
- `assets/usluga-pedicure.jpg` — Pedicure
- `assets/usluga-rzesy.jpg` — Przedłużanie rzęs
- `assets/usluga-brwi.jpg` — Brwi i rzęsy
- `assets/usluga-masaz.jpg` — Masaż
- `assets/usluga-spa.jpg` — Parafina & SPA dłoni
- `assets/usluga-blizny.jpg` — Blizny i rozstępy

**Mastrzy (kafelek + portret na podstronie):**
- `assets/mistrz-weronika.jpg` — Weronika (Manicure, pedicure, brwi, SPA i depilacja)
- `assets/mistrz-natasha.jpg` — Natasha (Stylistka paznokci)
- `assets/mistrz-wiktoria.jpg` — Wiktoria (Mikroneedling i blizny)
- `assets/mistrz-fabian.jpg` — Fabian (Fizjoterapeuta, masażysta)
- `assets/mistrz-emilia.jpg` — Emilia (Stylizacja paznokci, brwi i rzęs)
- `assets/mistrz-elena.jpg` — Elena (Stylistka przedłużania rzęs)

## Rezerwacja
Każdy przycisk „Rezerwuj / Zarezerwuj” prowadzi na profil Booksy salonu.

## Uwaga
Biografie mastrów to teksty startowe — możesz je edytować w `build.py` (lista MASTERS) i uruchomić `python3 build.py`.
