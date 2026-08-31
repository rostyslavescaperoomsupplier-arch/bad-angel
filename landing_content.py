# -*- coding: utf-8 -*-
"""Strony pod konkretne frazy wyszukiwane w Szczecinie.

Tylko po polsku i tylko w korzeniu serwisu: to sa zapytania zadawane po polsku
("manicure hybrydowy szczecin"), a konkurencja z miasta ma pod nie osobne
adresy z fraza w URL-u. Strona uslugi (usluga-<slug>.html) jest hubem
kategorii, te strony sa szczegolowymi galeziami — kazda o czym innym, zeby nie
konkurowaly ze soba o to samo zapytanie.

Pola:
  slug     — nazwa pliku bez .html (fraza w adresie)
  parent   — slug kategorii: cennik, galeria i link "wroc do kategorii"
  match    — fragmenty nazw pozycji z cennika, ktore maja trafic na strone
  h1/lead/title/desc/text/faq — tresc
"""

LANDINGS = [
 dict(
  slug="manicure-hybrydowy-szczecin", parent="manicure",
  h1="Manicure hybrydowy Szczecin",
  eyebrow="Dłonie · Centrum",
  title="Manicure hybrydowy Szczecin — cena od 60 zł | BAD ANGEL",
  desc="Manicure hybrydowy w Szczecinie, aleja Wyzwolenia 5/10. Cena od 60 zł, trwałość 3–4 tygodnie, pełna paleta kolorów. Salon z oceną 4.9. Rezerwacja online.",
  lead="Trwałość trzech tygodni i kolor, który nie schodzi przy zmywaniu naczyń",
  match=["hybryd", "lakier"],
  text=[
   "Manicure hybrydowy to najczęściej zamawiana usługa w naszym salonie w centrum Szczecina. Lakier hybrydowy utwardza się w lampie UV, dzięki czemu nie ściera się przy pracy, sprzątaniu ani na basenie — a przy tym pozostaje cienki i elastyczny, w odróżnieniu od żelu.",
   "Zaczynamy od opracowania płytki i skórek metodą kombinowaną. To etap, który decyduje o wszystkim: jeśli baza wejdzie na skórki albo na tłustą płytkę, hybryda odpryśnie w ciągu tygodnia niezależnie od tego, jak dobry jest lakier. Dlatego nie skracamy przygotowania nawet przy krótkich terminach.",
   "W palecie mamy pełny wachlarz kolorów, od nude i mlecznych francuzów po ciemne, mocne odcienie na jesień. Zdobienia, wzorki i efekty typu chrom czy kocie oko wyceniamy indywidualnie przy stanowisku — powiedz przy rezerwacji, że chcesz coś więcej niż jednolity kolor, a zarezerwujemy dodatkowy czas.",
   "Wizyta z opracowaniem skórek i odżywką proteinową trwa około półtorej godziny. Sam kolor na przygotowanej płytce zajmuje mniej. Terminy schodzą zwykle z kilkudniowym wyprzedzeniem, a przed świętami i długimi weekendami znacznie szybciej — warto zarezerwować od razu przy poprzedniej wizycie.",
  ],
  faq=[
   ("Ile kosztuje manicure hybrydowy w Szczecinie?",
    "U nas od 60 zł za samo pokrycie hybrydą, a od 117 zł za wersję z pełnym opracowaniem skórek i odżywką proteinową. Ceny na tej stronie są takie same jak w Booksy i aktualizujemy je razem z cennikiem salonu."),
   ("Ile trwa manicure hybrydowy?",
    "Od godziny do półtorej, zależnie od stanu płytki i tego, czy dochodzi zdejmowanie poprzedniej hybrydy. Pierwsza wizyta bywa dłuższa, bo zaczynamy od oceny paznokci."),
   ("Czy hybryda niszczy paznokcie?",
    "Sama hybryda nie. Płytkę niszczy zdzieranie jej na sucho i zbyt agresywne spiłowywanie bazy. Zdejmujemy hybrydę acetonem albo frezem do warstwy bazowej, bez schodzenia w naturalny paznokieć."),
   ("Czy można zrobić hybrydę na krótkich paznokciach?",
    "Tak, hybryda dobrze wygląda na krótkiej płytce i jest wtedy najtrwalsza. Jeśli chcesz długość, dokładamy żel albo przedłużenie na dual formach — to osobne pozycje w cenniku."),
  ]),

 dict(
  slug="paznokcie-zelowe-szczecin", parent="manicure",
  h1="Paznokcie żelowe i przedłużanie paznokci — Szczecin",
  eyebrow="Dłonie · Przedłużanie",
  title="Paznokcie żelowe Szczecin — przedłużanie od 135 zł | BAD ANGEL",
  desc="Przedłużanie paznokci żelem i na dual formach w Szczecinie, długości 1–5. Cena od 135 zł. Salon BAD ANGEL, aleja Wyzwolenia 5/10, ocena 4.9.",
  lead="Długość i kształt, których naturalna płytka nie utrzyma sama",
  match=["żel", "Przedłuż", "Odnowa", "Rekonstrukcja"],
  text=[
   "Przedłużanie paznokci robimy dwiema metodami: żelem na formie oraz na dual formach. Dual formy dają gładszy spód i szybszą pracę, żel na formie pozwala na większą kontrolę nad łukiem i sprawdza się przy nietypowych kształtach płytki. Metodę dobieramy do dłoni, nie odwrotnie.",
   "Długości opisujemy w skali od 1 do 5 — jedynka to niecały milimetr ponad opuszek, piątka to wyraźnie długi paznokieć. Jeśli przedłużasz pierwszy raz, odradzamy zaczynanie od czwórki: przez pierwszy tydzień trzeba na nowo nauczyć się pisać na klawiaturze i zapinać guziki. Większość osób zostaje przy długości 2–3.",
   "Osobną pozycją jest żel na naturalną płytkę. To nie jest przedłużanie, tylko wzmocnienie: cienka warstwa żelu wyrównuje płytkę i chroni ją przed łamaniem, zachowując własną długość. Dobre rozwiązanie dla osób, którym paznokcie pękają w rogach.",
   "Uzupełnienia robimy co trzy, cztery tygodnie. Przy złamanym paznokciu nie trzeba czekać na termin całego kompletu — rekonstrukcja jednego paznokcia to krótka wizyta, którą zwykle udaje się wcisnąć w grafik w ciągu kilku dni.",
  ],
  faq=[
   ("Ile kosztuje przedłużanie paznokci w Szczecinie?",
    "Przedłużanie żelem zaczyna się od 135 zł, a odnowa żelowa od 135 zł w zależności od długości. Żel na naturalną płytkę to 80 zł. Pełny cennik z długościami znajdziesz na tej stronie."),
   ("Ile trzymają się paznokcie żelowe?",
    "Do uzupełnienia zwykle trzy, cztery tygodnie. Sam materiał wytrzymałby dłużej, ale odrost przy skórkach zaczyna być widoczny i zmienia się rozkład sił na płytce, przez co paznokieć łatwiej pęka."),
   ("Czym różni się żel od hybrydy?",
    "Hybryda to kolor — cienka warstwa, która nie dodaje wytrzymałości ani długości. Żel to materiał konstrukcyjny: buduje długość, wyrównuje płytkę i przenosi obciążenia. Na żelu i tak kładzie się na wierzch lakier hybrydowy."),
   ("Co zrobić, gdy paznokieć się złamie?",
    "Zadzwoń albo napisz i umów się na rekonstrukcję jednego paznokcia. To krótki zabieg, znacznie tańszy niż zdejmowanie i zakładanie całego kompletu."),
  ]),

 dict(
  slug="przedluzanie-rzes-szczecin", parent="rzesy",
  h1="Przedłużanie rzęs Szczecin",
  eyebrow="Spojrzenie · Objętości 1:1 – 5:1",
  title="Przedłużanie rzęs Szczecin — od 135 zł, metody 1:1 do 5:1 | BAD ANGEL",
  desc="Przedłużanie rzęs w Szczecinie: objętości od 1:1 do 5:1, cena od 135 zł, uzupełnienie 126 zł. Salon BAD ANGEL, aleja Wyzwolenia 5/10. Rezerwacja online.",
  lead="Od efektu naturalnego po pełną objętość — dobrane do kształtu oka",
  match=["Metoda", "Uzupełnienie", "Ściągnięcie"],
  text=[
   "Objętość opisuje, ile sztucznych rzęs stawiamy na jedną własną. Metoda 1:1 daje efekt, którego z bliska nie odróżnisz od gęstych własnych rzęs — to wybór osób, które chcą wyglądać na wyspane, a nie umalowane. Objętości 3:1 i wyżej budują wyraźną, ciemną linię przy nasadzie i zastępują codzienny makijaż oka.",
   "Przed pierwszą aplikacją oglądamy własne rzęsy. Cienka, osłabiona rzęsa nie udźwignie objętości 5:1 — będzie się zaginać i wypadać przedwcześnie, ciągnąc za sobą własną. W takiej sytuacji proponujemy niższą objętość albo laminację, i mówimy to przed zabiegiem, nie po nim.",
   "Aplikacja trwa około dwóch godzin. Leży się z zamkniętymi oczami, więc to jedna z niewielu usług, przy których można faktycznie odpocząć albo posłuchać podcastu. Soczewki kontaktowe trzeba zdjąć przed zabiegiem.",
   "Uzupełnienie ma sens do trzech tygodni od aplikacji. Po tym czasie własnych rzęs w cyklu wzrostu zostaje za mało, żeby dołożyć równomiernie, i taniej wychodzi zdjęcie kompletu i założenie nowego. Ściągnięcie rzęs — także pracy z innego salonu — jest osobną, krótką usługą.",
  ],
  faq=[
   ("Ile kosztuje przedłużanie rzęs w Szczecinie?",
    "Metoda 1:1 to 135 zł, 2:1 — 144 zł, 3:1 — 153 zł, 4:1 od 162 zł, 5:1 — 171 zł. Uzupełnienie w metodzie 1:1 do trzech tygodni kosztuje 126 zł, a samo ściągnięcie rzęs od 36 zł."),
   ("Którą objętość wybrać przy pierwszym razie?",
    "Zwykle 2:1 albo 3:1. To wyraźnie widać, ale nie jest to jeszcze efekt, przy którym znajomi pytają, czy coś sobie zrobiłaś. Do wyższych objętości łatwo przejść przy kolejnej wizycie."),
   ("Czy można malować rzęsy tuszem?",
    "Przedłużonych rzęs nie trzeba i nie warto malować. Tusz, zwłaszcza wodoodporny, skleja kępki i skraca żywotność kleju. Jeśli chcesz nadal używać tuszu, lepszym wyborem jest laminacja rzęs."),
   ("Co zrobić przed wizytą?",
    "Przyjdź bez makijażu oka i bez kremów tłustych na powiece, zdejmij soczewki. Kawę lepiej odpuścić — przy dwóch godzinach z zamkniętymi oczami pomaga, gdy powieka jest spokojna."),
  ]),

 dict(
  slug="laminacja-brwi-szczecin", parent="brwi",
  h1="Laminacja brwi Szczecin",
  eyebrow="Brwi · Laminacja z botoksem",
  title="Laminacja brwi Szczecin — 100 zł, efekt na 4–6 tygodni | BAD ANGEL",
  desc="Laminacja brwi z botoksem w Szczecinie za 100 zł, z koloryzacją 130 zł. Efekt utrzymuje się 4–6 tygodni. Salon BAD ANGEL, aleja Wyzwolenia 5/10.",
  lead="Włoski ułożone w jednym kierunku przez sześć tygodni",
  match=["Laminacja", "Regulacja", "Korekta"],
  text=[
   "Laminacja to zabieg dla brwi, które rosną w różne strony, opadają albo mają prześwity. Preparat zmiękcza włos, układa go w wybranym kierunku i utrwala. Efekt jest widoczny od razu: łuk wygląda na gęstszy i wyższy, bo włoski przestają leżeć płasko i zasłaniać się nawzajem.",
   "Do laminacji zawsze dokładamy botoks. Sam zabieg laminacji jest chemiczny i wysusza włos, a botoks odbudowuje go od środka — bez tego po dwóch, trzech laminacjach brwi robią się szorstkie i łamliwe. Z tego samego powodu nie powtarzamy zabiegu częściej niż raz na miesiąc.",
   "Najczęściej łączymy laminację z koloryzacją henną pudrową i regulacją. Kolejność ma znaczenie: najpierw układamy włoski, potem widzimy realny kształt łuku i dopiero wtedy regulujemy, usuwając tylko to, co faktycznie wystaje. Regulacja przed laminacją zwykle kończy się usunięciem włosów, które po ułożeniu byłyby potrzebne.",
   "Zabieg trwa 40 minut, a z koloryzacją godzinę. Przez pierwsze 24 godziny brwi nie moczymy i nie dotykamy, później nie wymagają niczego poza czesaniem szczoteczką rano.",
  ],
  faq=[
   ("Ile kosztuje laminacja brwi w Szczecinie?",
    "Laminacja brwi z botoksem kosztuje 100 zł, a z koloryzacją 130 zł. Laminacja rzęs z botoksem to 160 zł, a z farbowaniem 180 zł."),
   ("Jak długo trzyma się laminacja brwi?",
    "Cztery do sześciu tygodni, zależnie od tempa wzrostu włosów. Efekt schodzi stopniowo, więc nie ma momentu, w którym brwi nagle wyglądają źle."),
   ("Czy laminacja niszczy brwi?",
    "Przy zachowanych odstępach i z botoksem — nie. Problemy pojawiają się przy powtarzaniu zabiegu co dwa tygodnie i przy pomijaniu odżywienia włosa."),
   ("Laminacja czy henna pudrowa?",
    "Laminacja układa włoski, henna je barwi i wypełnia kolorem prześwity w skórze. To dwa różne efekty i najczęściej robi się je razem — dlatego mamy pozycję łączoną w cenniku."),
  ]),

 dict(
  slug="pedicure-hybrydowy-szczecin", parent="pedicure",
  h1="Pedicure hybrydowy Szczecin",
  eyebrow="Stopy · Pełne opracowanie",
  title="Pedicure hybrydowy Szczecin — od 100 zł | Salon BAD ANGEL",
  desc="Pedicure hybrydowy w Szczecinie od 100 zł, z pełnym opracowaniem stopy od 120 zł. Osobne, zamknięte stanowisko. Salon BAD ANGEL, aleja Wyzwolenia 5/10.",
  lead="Pełne opracowanie stopy i kolor, który wytrzyma całe lato",
  match=["hybrydow", "hybryda", "Pedicure"],
  text=[
   "Pedicure hybrydowy występuje u nas w dwóch wariantach: z opracowaniem stopy i bez. Wersja bez stopy obejmuje paznokcie, wały i pokrycie hybrydą — to dobry wybór na uzupełnienie koloru między pełnymi zabiegami. Wersja pełna dokłada pięty, zrogowacenia i modzele i trwa dłużej.",
   "Pedicure robimy w zamkniętym stanowisku, osobno od części manicure. To nie jest usługa, przy której chce się siedzieć na środku salonu z nogami w misce — a dla nas oznacza spokojną pracę bez pośpiechu.",
   "Na paznokciach u stóp lakier hybrydowy trzyma się znacznie dłużej niż na dłoniach, bo płytka rośnie wolniej i nie pracuje tak intensywnie. Realnie to sześć do ośmiu tygodni, przy czym latem częściej wracamy z powodu pięt niż koloru.",
   "Wrastające paznokcie, grzybicę i głębokie pęknięcia pięt oglądamy i mówimy wprost, kiedy sprawa jest już podologiczna albo dermatologiczna. Zabieg kosmetyczny poprawi wygląd, ale nie wyleczy zmiany chorobowej i nie będziemy udawać, że jest inaczej.",
  ],
  faq=[
   ("Ile kosztuje pedicure hybrydowy w Szczecinie?",
    "Pedicure hybrydowy bez opracowania pięt to 100 zł, z pełnym opracowaniem stopy 120 zł, a wersja z pełną obróbką i pielęgnacją pięt od 153 zł. Aktualne pozycje są w cenniku na tej stronie."),
   ("Ile trwa pedicure hybrydowy?",
    "Od 80 minut w wersji bez stopy do około dwóch i pół godziny przy pełnym opracowaniu z piętami."),
   ("Jak często robić pedicure hybrydowy?",
    "Latem co cztery, pięć tygodni, zimą co sześć, osiem. Kolor wytrzymuje dłużej niż stan pięt, więc to zwykle skóra decyduje o terminie."),
   ("Czy robicie pedicure dla mężczyzn?",
    "Tak, pedicure męski jest osobną pozycją. To zabieg pielęgnacyjny bez koloru: paznokcie, wały i zrogowaciały naskórek."),
  ]),
]

LANDINGS += [
 dict(
  slug="masaz-szczecin", parent="masaz",
  h1="Masaż Szczecin",
  eyebrow="Ciało · Kręgosłup i relaks",
  title="Masaż Szczecin — kręgosłupa od 100 zł, relaksacyjny | BAD ANGEL",
  desc="Masaż w Szczecinie: kręgosłupa od 100 zł, klasyczny całego ciała od 200 zł, relaksacyjny, miodowy i antycellulitowy. aleja Wyzwolenia 5/10, ocena 4.9.",
  lead="Od pół godziny na kark po dwie godziny pełnego relaksu",
  match=["Masaż"],
  text=[
   "Najkrótsza i najczęściej wybierana pozycja to masaż kręgosłupa: pół godziny pracy na odcinku szyjnym, piersiowym i barkach. Przychodzą po niego osoby pracujące przy komputerze, kierowcy i fryzjerki — wszyscy, którzy spędzają dzień w jednej pozycji z głową pochyloną do przodu.",
   "Masaż klasyczny całego ciała trwa półtorej godziny i pracuje nad napięciem mięśniowym. Relaksacyjny trwa dwie godziny, jest wolniejszy i spokojniejszy — to nie jest zabieg, po którym schodzą zakwasy, tylko taki, po którym się zasypia. Jeśli nie wiesz, który wybrać: przy bólu bierz klasyczny, przy przemęczeniu relaksacyjny.",
   "W ofercie jest też masaż miodowy, antycellulitowy, bańką chińską i masaż twarzy. Miodowy i bańką pracują ostro i mogą zostawić zaczerwienienie albo siniaki na dobę, dwie — mówimy o tym przed zabiegiem, żeby nie zaskoczyło to przed wyjściem w odsłoniętych plecach.",
   "Ceny dla kobiet i mężczyzn różnią się, bo różni się czas pracy na większej powierzchni ciała — obie stawki są wypisane w cenniku. Przed pierwszą wizytą pytamy o kontuzje, ciążę, żylaki, nadciśnienie i choroby przewlekłe. Przy części z nich potrzebna jest zgoda lekarza i nie robimy wyjątków.",
  ],
  faq=[
   ("Ile kosztuje masaż w Szczecinie?",
    "Masaż kręgosłupa od 100 zł za 30 minut, masaż klasyczny całego ciała od 200 zł, relaksacyjny 300 zł, masaż miodowy wybranej partii 100 zł. Pełny cennik z podziałem na kobiety i mężczyzn jest na tej stronie."),
   ("Ile masaży potrzeba przy bólu pleców?",
    "Pojedynczy masaż daje ulgę na kilka dni. Przy nawracającym bólu efekt utrzymuje się dłużej po serii czterech, sześciu zabiegów w odstępach tygodniowych."),
   ("Czy można przyjść na masaż w ciąży?",
    "Nie w pierwszym trymestrze. Później po konsultacji, w pozycji bocznej, z pominięciem brzucha i odcinka lędźwiowego. Powiedz o ciąży przy rezerwacji, nie na miejscu."),
   ("Jak przygotować się do masażu?",
    "Nie jedz obficie na godzinę przed wizytą i przyjdź kilka minut wcześniej, żeby spokojnie się przebrać. Ręczniki i podkłady mamy na miejscu."),
  ]),

 dict(
  slug="depilacja-woskiem-szczecin", parent="depilacja",
  h1="Depilacja woskiem Szczecin",
  eyebrow="Ciało · Wosk",
  title="Depilacja woskiem Szczecin — bikini, nogi, pachy | BAD ANGEL",
  desc="Depilacja woskiem w Szczecinie: pachy 54 zł, bikini pełne od 135 zł, nogi całe 144 zł, pakiet 315 zł. Salon BAD ANGEL, aleja Wyzwolenia 5/10.",
  lead="Trzy, cztery tygodnie gładkości zamiast codziennego golenia",
  match=["Broda", "Pachy", "Bikini", "Nogi"],
  text=[
   "Wosk usuwa włos razem z cebulką, dlatego odrost pojawia się po trzech, czterech tygodniach, a nie po dwóch dniach jak po maszynce. Przy regularnych wizytach włos odrasta cieńszy i rzadszy, więc odstępy między zabiegami z czasem same się wydłużają.",
   "Najczęściej zamawiany jest pakiet bikini, nogi i pachy — jedna wizyta zamyka temat na miesiąc i wychodzi taniej niż te same partie osobno. Pojedyncze partie robimy też oddzielnie, łącznie z depilacją brody i twarzy.",
   "Żeby wosk chwycił, włos musi mieć około pięciu milimetrów, czyli mniej więcej dwa tygodnie od ostatniego golenia. To najczęstszy powód przekładania wizyty: na zbyt krótkim włosie zabieg po prostu nie zadziała, a próba i tak boli. Odpuść maszynkę przed terminem.",
   "Po depilacji przez dobę odpuść saunę, basen, solarium i intensywny trening, a przez dwa dni mocne peelingi i perfumowane balsamy. Wrastające włoski najskuteczniej ogranicza regularne złuszczanie skóry, zaczęte trzy, cztery dni po zabiegu.",
  ],
  faq=[
   ("Ile kosztuje depilacja woskiem w Szczecinie?",
    "Pachy 54 zł, broda 45 zł, bikini pełne od 135 zł, nogi całe 144 zł. Pakiet bikini plus nogi plus pachy kosztuje 315 zł."),
   ("Jak długo utrzymuje się efekt?",
    "Trzy do czterech tygodni. Przy regularnych wizytach dłużej, bo włos staje się słabszy i rzadszy."),
   ("Czy depilacja woskiem boli?",
    "Pierwszy raz jest najbardziej odczuwalny, kolejne są łatwiejsze. Najwrażliwsze są bikini i pachy, nogi większość osób znosi spokojnie. Nie planuj zabiegu na kilka dni przed miesiączką — wtedy próg bólu jest niższy."),
   ("Jakiej długości muszą być włosy?",
    "Około pięciu milimetrów, czyli dwa tygodnie od golenia. Krótszego włosa wosk nie chwyci."),
  ]),

 dict(
  slug="mikroneedling-szczecin", parent="blizny",
  h1="Mikroneedling i redukcja blizn — Szczecin",
  eyebrow="Skóra · Konsultacja darmowa",
  title="Mikroneedling Szczecin — redukcja blizn i rozstępów | BAD ANGEL",
  desc="Mikroneedling w Szczecinie: redukcja blizn od 349 zł, rozstępów od 469 zł, konsultacja darmowa. Salon BAD ANGEL, aleja Wyzwolenia 5/10, ocena 4.9.",
  lead="Kontrolowana regeneracja skóry zamiast obietnic bez pokrycia",
  match=["blizn", "Blizna", "rozstęp", "Konsultacja", "Mikro"],
  text=[
   "Mikroneedling polega na nakłuwaniu skóry cienkimi igłami na precyzyjnie ustawioną głębokość. Mikrouszkodzenia uruchamiają odbudowę kolagenu i elastyny, przez co blizna spłaszcza się i blednie, a rozstęp traci ostrą granicę i zbliża się kolorem do reszty skóry.",
   "Konsultacja jest darmowa i zawsze poprzedza pierwszy zabieg. Oglądamy zmianę, pytamy, kiedy powstała i jak się goiła, i mówimy, ilu zabiegów realnie potrzeba oraz jakiego efektu można się spodziewać. Świeże blizny reagują znacznie lepiej niż kilkunastoletnie, a bliznowce i keloidy wymagają zupełnie innego podejścia — czasem odradzamy zabieg i mówimy to wprost.",
   "Osobno pracujemy z blizną po cesarskim cięciu, ze starymi bliznami pooperacyjnymi oraz z rozstępami na biuście, brzuchu, pośladkach i udach. Blizna po cesarskim cięciu wymaga pełnego zagojenia i minimum pół roku od porodu.",
   "Seria to zwykle trzy do sześciu zabiegów w odstępach czterech, sześciu tygodni. Efektu nie widać zaraz po wyjściu z gabinetu: skóra przez dobę, dwie jest zaczerwieniona, a odbudowa kolagenu zajmuje kilka tygodni. Realny postęp ocenia się po drugim, trzecim zabiegu.",
  ],
  faq=[
   ("Ile kosztuje redukcja blizn w Szczecinie?",
    "Blizna do 5 cm to 399 zł, do 10 cm 499 zł, większe od 599 zł. Blizna po cesarskim cięciu 349 zł, stare blizny pooperacyjne 449 zł, redukcja rozstępów od 469 zł. Konsultacja jest darmowa."),
   ("Ile zabiegów potrzeba?",
    "Zwykle trzy do sześciu, w odstępach czterech, sześciu tygodni. Dokładną liczbę podajemy po obejrzeniu blizny na darmowej konsultacji — podanie liczby wcześniej byłoby zgadywaniem."),
   ("Czy mikroneedling boli?",
    "Pracujemy w znieczuleniu miejscowym w kremie, więc odczuwalny jest ucisk i wibracja, a nie kłucie. Na cienkiej skórze i nad kośćmi bywa mniej komfortowo."),
   ("Kiedy można pracować z blizną po cesarskim cięciu?",
    "Nie wcześniej niż pół roku po porodzie i tylko przy w pełni zagojonej, niebolesnej bliźnie. Przy karmieniu piersią i powikłaniach gojenia prosimy o zgodę lekarza."),
  ]),

 dict(
  slug="warkoczyki-szczecin", parent="wlosy",
  h1="Warkoczyki z kanekalonem — Szczecin",
  eyebrow="Włosy · Kanekalon i box braids",
  title="Warkoczyki Szczecin — kanekalon, box braids od 150 zł | BAD ANGEL",
  desc="Warkoczyki z kanekalonem w Szczecinie: pojedynczy 150 zł, cała głowa 350 zł, box braids 350 zł, bąbelkowe 220 zł. Salon BAD ANGEL, aleja Wyzwolenia 5/10.",
  lead="Fryzura na kilka tygodni, która nie wymaga codziennego układania",
  match=["arkocz", "braids", "Przedłużanie", "trzyżenie"],
  text=[
   "Zaplatamy warkoczyki z kanekalonem w kilku wariantach: pojedynczy warkocz, dwa warkocze, cała głowa, afrykańskie box braids i warkocze bąbelkowe. Kanekalon dokłada długość i kolor, których własne włosy nie mają, i pozwala zapleść nawet cienkie włosy.",
   "To praca na kilka godzin — od godziny przy pojedynczym warkoczu do pięciu i pół przy box braids na całą głowę. Warto zjeść przed wizytą i zarezerwować sobie ten dzień. W zamian fryzura trzyma się trzy do sześciu tygodni i rano nie wymaga niczego.",
   "Kolor kanekalonu ustalamy przy rezerwacji, żeby mieć go na miejscu w dniu wizyty. Jeśli chcesz konkretny odcień albo mieszankę dwóch kolorów, napisz do nas wcześniej — część kolorów zamawiamy pod klienta.",
   "Dłużej niż sześć tygodni warkoczyków nosić nie warto: odrost zaczyna napinać włosy przy skórze głowy, co kończy się bólem i wypadaniem. Rozplatanie też robimy w salonie, jeśli nie chcesz robić tego sama.",
  ],
  faq=[
   ("Ile kosztują warkoczyki w Szczecinie?",
    "Pojedynczy warkoczyk z kanekalonem 150 zł, dwa warkoczyki 200 zł, cała głowa 350 zł. Box braids 350 zł, warkocze bąbelkowe 220 zł."),
   ("Ile trwa zaplatanie?",
    "Od godziny przy pojedynczym warkoczu, przez dwie godziny przy dwóch, do czterech, pięciu i pół godziny przy całej głowie i box braids."),
   ("Jak długo można nosić warkoczyki?",
    "Trzy do sześciu tygodni. Dłużej nie zalecamy, bo odrost napina włosy przy skórze głowy."),
   ("Czy zaplatacie na krótkich włosach?",
    "Zależy od długości — potrzebne jest minimum kilkanaście centymetrów, żeby splot się utrzymał. Prześlij zdjęcie przed rezerwacją, ocenimy i powiemy wprost."),
  ]),
]
