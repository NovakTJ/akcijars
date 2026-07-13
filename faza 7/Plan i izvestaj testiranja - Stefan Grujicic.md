# Plan i izveštaj testiranja — Stefan Grujičić 0030/2023

---

## 1. Uvod

Ovde su testirane sledeće funkcionalnosti:

| SSU | Funkcionalnost | Autor implementacije |
|:----| :---- | :---- |
| 2   | Autorizacija (prijava/odjava) | Novak Stijepić |
| 5   | Kreiranje akcije | Novak Stijepić |
| 8   | Slanje informacija (obaveštenja) volonterima | Novak Stijepić |
| 10  | Ažuriranje i otkazivanje akcije | Novak Stijepić |
| 11  | Kreiranje članka | Novak Stijepić |

---

## 2. Lokacija i pokretanje testova

| Vrsta | Lokacija | Fajlovi |
| :---- | :---- | :---- |
| Jedinični (Django) | `faza 5/akcijars/main/tests/` | `test_ssu02_autorizacija.py`, `test_ssu05_akcije.py`, `test_ssu08_info_volonterima.py`, `test_ssu10_azuriranje_akcije.py`, `test_ssu11_clanci.py`, `_helpers.py` |
| UI (Selenium WebDriver) | `faza 5/akcijars/main/tests_ui/` | `test_ssu02_autorizacija_ui.py`, `test_ssu05_akcije_ui.py`, `test_ssu08_info_volonterima_ui.py`, `test_ssu10_azuriranje_akcije_ui.py`, `test_ssu11_clanci_ui.py`, `_baza.py` |

**Pokretanje** (iz `faza 5/akcijars`, uz aktiviran venv):
```
python manage.py test main.tests       # jedinični (brzo, bez pretraživača)
python manage.py test main.tests_ui    # UI Selenium (potreban Google Chrome)
python manage.py test main             # oba zajedno
```
Django automatski pravi izolovanu test bazu (`test_akcijars`), pokreće testove i briše
je na kraju — **ne dira produkcionu bazu**. Selenium testovi rade **headless** (bez
vidljivog prozora); za prikaz prozora: `SELENIUM_HEADLESS=0 python manage.py test main.tests_ui`.

**Preduslovi za UI testove:** instaliran `selenium` (u `requirements.txt`) i **Google
Chrome** (drajver se skida automatski). Kompletno UI testiranje isključivo koristi
Selenium WebDriver — Selenium IDE se u timu ne koristi.

**Rezultat:** 46 jediničnih + 12 UI = **58 testova, svi prolaze**.

---

## 3. Test primeri po SSU

### SSU 2 — Autorizacija (`test_ssu02_autorizacija.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesna_prijava_volontera_2_2_1` | 2.2.1 | Prijava volontera → redirect na `volonter_panel` |
| `test_uspesna_prijava_organizatora_2_2_1` | 2.2.1 | Prijava organizatora → redirect na `organizator_panel` (prema ulozi) |
| `test_nepostojeci_email_2_2_2` | 2.2.2 | Propisana poruka, korisnik ostaje neulogovan |
| `test_neispravna_lozinka_2_2_3` | 2.2.3 | Ista poruka kao za nepostojeći email |
| `test_neodobren_nalog_2_2_4` | 2.2.4 | Nalog na čekanju → propisana poruka |
| `test_odbijen_nalog_takodje_blokiran` | — | Odbijen nalog takođe blokiran |
| `test_prazna_polja` | — | Nepopunjena obavezna polja |
| `test_ulogovan_korisnik_preusmeren` | 2.4 | Ulogovan korisnik ne vidi formu za prijavu |
| `test_odjava_brise_sesiju_2_2_5` | 2.2.5 | Odjava briše sesiju, redirect na početnu |

### SSU 5 — Kreiranje akcije (`test_ssu05_akcije.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesno_kreiranje_2_2_1` | 2.2.1 | Akcija se čuva sa statusom „na čekanju" |
| `test_prazna_obavezna_polja_2_2_2` | 2.2.2 | Jedinstvena poruka, akcija se ne pravi |
| `test_datum_u_proslosti_2_2_3` | 2.2.3 | Datum u prošlosti se odbija |
| `test_nevalidan_max_broj_volontera_2_2_4` | 2.2.4 | 0/negativan broj volontera se odbija |
| `test_neispravan_email_format_2_2_5` | 2.2.5 | Neispravan format kontakt email-a |
| `test_neispravan_telefon_format_2_2_6` | 2.2.6 | Neispravan format kontakt telefona |
| `test_odustajanje_ne_cuva_2_2_7` | 2.2.7 | Otvaranje forme bez slanja ne pravi akciju |
| `test_neodobren_organizator_preusmeren` | 2.4 | Neodobren organizator ne može da kreira akciju |
| `test_ne_organizator_preusmeren` | 2.4 | Ne-organizator (volonter) ne može da kreira akciju |
| `test_neulogovan_preusmeren` | — | Neulogovan korisnik → 302 |

### SSU 8 — Slanje informacija volonterima (`test_ssu08_info_volonterima.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesno_slanje_svim_prihvacenim_2_2_1` | 2.2.1 | Email svim prihvaćenim volonterima (ne odbijenim) |
| `test_prazna_poruka_2_2_2` | 2.2.2 | Prazna poruka se odbija, ništa se ne šalje |
| `test_odustajanje_ne_salje_2_2_3` | 2.2.3 | Bez slanja obaveštenja niko ne prima email |
| `test_bez_prihvacenih_volontera_400` | — | Akcija bez prihvaćenih volontera → 400 |
| `test_otkazana_akcija_400` | — | Otkazana akcija → slanje nije moguće |
| `test_ne_vlasnik_403` | — | Samo vlasnik akcije sme da šalje obaveštenja |
| `test_neulogovan_preusmeren` | — | Neulogovan korisnik → 302 |

### SSU 10 — Ažuriranje i otkazivanje akcije (`test_ssu10_azuriranje_akcije.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesno_azuriranje_2_2_1` | 2.2.1 | Izmene sačuvane + email prijavljenim volonterima |
| `test_prazna_obavezna_polja_2_2_2` | 2.2.2 | Jedinstvena poruka, izmene se ne čuvaju |
| `test_datum_u_proslosti_2_2_3` | 2.2.3 | Datum u prošlosti se odbija |
| `test_nevalidan_broj_volontera_2_2_4` | 2.2.4 | 0/negativan broj volontera se odbija |
| `test_max_manji_od_prihvacenih_2_2_5` | 2.2.5 | Max manji od već prihvaćenih se odbija |
| `test_neispravan_email_2_2_6` | 2.2.6 | Neispravan format kontakt email-a |
| `test_neispravan_telefon_2_2_7` | 2.2.7 | Neispravan format kontakt telefona |
| `test_odustajanje_ne_cuva_2_2_8` | 2.2.8 | Bez slanja izmena podaci ostaju nepromenjeni |
| `test_ne_vlasnik_403` | — | Samo vlasnik akcije sme da je menja |
| `test_otkazivanje_2_2_9` | 2.2.9 | Status → „Otkazana" + email svim prijavljenim (ne odbijenim) |
| `test_vec_otkazana_400` | — | Već otkazana akcija se ne može ponovo otkazati |
| `test_ne_vlasnik_403` (otkazivanje) | — | Samo vlasnik akcije sme da je otkaže |

### SSU 11 — Kreiranje članka (`test_ssu11_clanci.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesno_kreiranje_2_2_1` | 2.2.1 | Članak se čuva sa statusom „na čekanju" |
| `test_bez_naslova_2_2_2` | 2.2.2 | Prazan naslov se odbija |
| `test_bez_sadrzaja_2_2_3` | 2.2.3 | Prazan tekst se odbija |
| `test_odustajanje_ne_kreira_2_2_4` | 2.2.4 | Bez slanja forme članak se ne pravi |
| `test_ne_organizator_preusmeren` | 2.4 | Pristup samo prijavljenim organizatorima |
| `test_neodobren_organizator_preusmeren` | 2.4 | Neodobren organizator nema pristup |
| `test_neulogovan_preusmeren` | — | Neulogovan korisnik → 302 |
| `test_get_preusmerava_na_panel` | — | GET zahtev preusmerava na organizatorski panel |

---

## 3b. Selenium WebDriver (UI) test primeri

Testovi kroz pravi pretraživač (headless Chrome) simuliraju korisničke akcije.

| SSU | Test | Scenario | Provera kroz UI |
| :---- | :---- | :---- | :---- |
| 2 | `test_uspesna_prijava_2_2_1` | 2.2.1 | Prijava kroz formu → redirect na ličnu stranicu |
| 2 | `test_neispravna_lozinka_prikazuje_gresku_2_2_3` | 2.2.3 | Pogrešna lozinka → poruka o grešci |
| 2 | `test_odjava_2_2_5` | 2.2.5 | Klik „Odjavi se" → ponovo vidljiv link „Prijavi se" |
| 5 | `test_uspesno_kreiranje_2_2_1` | 2.2.1 | Popunjena forma → akcija vidljiva na „Moje akcije" |
| 5 | `test_prazna_obavezna_polja_prikazuje_gresku_2_2_2` | 2.2.2 | Prazna forma → poruka o grešci |
| 5 | `test_odustajanje_ne_cuva_2_2_7` | 2.2.7 | Klik „Odustani" → akcija se ne pravi |
| 8 | `test_uspesno_slanje_obavestenja_2_2_1` | 2.2.1 | Unos + „Pošalji" → poruka o uspehu, email poslat |
| 8 | `test_prazna_poruka_prikazuje_gresku_2_2_2` | 2.2.2 | Prazno + „Pošalji" → „Unesite tekst poruke." |
| 10 | `test_uspesno_azuriranje_2_2_1` | 2.2.1 | Izmena naziva u tabu „Izmeni akciju" → sačuvano |
| 10 | `test_otkazivanje_akcije_2_2_9` | 2.2.9 | „Otkaži akciju" + potvrda → status „Otkazana" |
| 11 | `test_uspesno_kreiranje_2_2_1` | 2.2.1 | Popunjena forma → članak vidljiv u „Moji članci" |
| 11 | `test_bez_naslova_prikazuje_gresku_2_2_2` | 2.2.2 | Prazan naslov → prikaz greške na polju |

---

## 4. Nalazi testiranja

Testiranjem **nisu pronađeni funkcionalni defekti** u obrađenim SSU-ovima (2, 5, 8, 10, 11).
Sve testirane funkcionalnosti ponašaju se u skladu sa specifikacijom.

Jedina napomena van funkcionalnih defekata: forma `ClanakForma` (SSU 11) ima sopstvenu
validaciju u `clean_naslov`/`clean_tekst` koja proverava da polje nije prazno nakon
`strip()`, ali polja `naslov`/`tekst` su Django `required=True` polja sa podrazumevanim
`strip=True` — prazan ili unos od samih razmaka Django-ova sopstvena validacija hvata
pre custom `clean_*` metode, pa se prikazuje generička poruka („Ovo polje se mora
popuniti.") umesto custom poruke iz `clean_naslov`/`clean_tekst`. Funkcionalno
zahtev iz SSU 11 (prazan naslov/tekst se odbija) i dalje je ispunjen — reč je samo o
tome da je deo custom validacije praktično nedostižan kodom. Nije ozbiljno dovoljno da
bude prijavljeno kao defekat, ali može biti od koristi kolegi koji je implementirao.

---
