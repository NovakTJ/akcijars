# Plan i izveštaj testiranja — Milica Milošević 0357/2023

---

## 1. Uvod

Ovde su testirane sledeće funkcionalnosti:

| SSU | Funkcionalnost | Autor implementacije |
|:----| :---- | :---- |
| 4   | Pregled i pretraga članaka | Maša Nikolić |
| 6   | Prijava/odjava volontera na akciju | Maša Nikolić |
| 7   | Dodavanje sponzora akciji (slanje ponude) | Stefan Grujičić |
| 12  | Komentarisanje članaka | Stefan Grujičić |

---

## 2. Lokacija i pokretanje testova

| Vrsta | Lokacija | Fajlovi |
| :---- | :---- | :---- |
| Jedinični (Django) | `faza 5/akcijars/main/tests/` | `test_ssu04_clanci.py`, `test_ssu06_prijave.py`, `test_ssu07_sponzori.py`, `test_ssu12_komentari.py`, `_helpers.py` |
| UI (Selenium WebDriver) | `faza 5/akcijars/main/tests_ui/` | `test_ssu04_clanci_ui.py`, `test_ssu06_prijave_ui.py`, `test_ssu07_sponzori_ui.py`, `test_ssu12_komentari_ui.py`, `_baza.py` |

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
Chrome** (drajver se skida automatski). 

**Rezultat:** 38 jediničnih + 10 UI = **48 testova, svi prolaze**.

---

## 3. Test primeri po SSU

### SSU 4 — Pregled i pretraga članaka (`test_ssu04_clanci.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_prikazuju_se_samo_objavljeni` | 2.2 | Članci na čekanju/odbijeni se ne prikazuju |
| `test_pretraga_po_naslovu_2_2_2` | 2.2.2 | Filter po podstringu naslova |
| `test_pretraga_po_organizatoru_2_2_2` | 2.2.2 | Filter po nazivu organizatora |
| `test_filter_po_kategoriji_2_2_3` | 2.2.3 | Filter po kategoriji |
| `test_kombinovana_pretraga_2_2_4` | 2.2.4 | Naziv + kategorija (logičko I) |
| `test_pretraga_bez_rezultata_2_2_6` | 2.2.6 | Prazan rezultat |
| `test_nedozvoljeni_karakteri_u_upitu_2_2_7` | 2.2.7 | Odbijen upit, poništen |
| `test_ajax_vraca_fragment` | 2.2 | Ajax vraća HTML fragment |
| `test_najvise_9_po_strani_2_2_5` | 2.2.5 | Paginacija (9 po strani) |
| `test_objavljen_clanak_prikazan_2_2_1` | 2.2.1 | Detalj objavljenog članka |
| `test_neobjavljen_clanak_nedostupan_404` | — | Neobjavljen → 404 |

### SSU 6 — Prijava/odjava volontera (`test_ssu06_prijave.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesna_prijava_2_2_1` | 2.2.1 | Prijava kreirana (na čekanju) |
| `test_prijava_na_neotvorenu_nije_moguca_2_2_4` | 2.2.4 | Na popunjenu → odbijeno (400) |
| `test_dvostruka_prijava_ne_pravi_duplikat_2_2_5` | 2.2.5 | Nema duplikata |
| `test_samo_volonter_moze_da_se_prijavi_403` | — | Ne-volonter → 403 |
| `test_neulogovan_preusmeren` | 2.4 | Neulogovan → 302 |
| `test_get_metoda_nije_dozvoljena_405` | — | GET → 405 |
| `test_odjava_pre_potvrde_brise_prijavu_2_2_2` | 2.2.2 | Odjava briše prijavu |
| `test_odjava_posle_prihvatanja_brise_prijavu_2_2_3` | 2.2.3 | Odjava oslobađa mesto |
| `test_odbijena_prijava_se_ne_moze_odjaviti` | — | Odbijena je konačna |
| `test_broj_prihvacenih_i_slobodna_mesta` | model | Broj prihvaćenih / slobodna mesta |

### SSU 7 — Dodavanje sponzora (`test_ssu07_sponzori.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesna_ponuda_2_2_1` | 2.2.1 | Ponuda evidentirana (na čekanju) |
| `test_nepotpuna_ponuda_bez_opisa_2_2_2` | 2.2.2 | Nepotpuna → nije evidentirana |
| `test_neispravna_vrednost_nula_2_2_3` | 2.2.3 | Vrednost 0 → odbijeno |
| `test_samo_sponzor_moze_403` | 2.4 | Ne-sponzor → 403 |
| `test_neodobren_sponzor_403` | 2.4 | Neodobren sponzor → 403 |
| `test_otkazana_akcija_403` | — | Otkazana akcija → 403 |
| `test_nula_vrednost_nevalidna` | 2.2.3 | Forma: vrednost 0 nevalidna |
| `test_prazan_opis_nevalidan` | 2.2.2 | Forma: prazan opis nevalidan |
| `test_ispravna_ponuda_validna` | 2.2.1 | Forma: ispravna ponuda validna |

### SSU 12 — Komentarisanje članaka (`test_ssu12_komentari.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_uspesan_komentar_2_2_1` | 2.2.1 | Komentar objavljen |
| `test_prazan_komentar_odbijen_na_serveru_2_2_2` | 2.2.2 | Prazan → odbijen (400) na serveru |
| `test_neulogovan_ne_moze_da_komentarise_2_2_3` | 2.2.3 | Gost → 302 (login) |
| `test_komentar_na_neobjavljen_clanak_404` | — | Neobjavljen članak → 404 |
| `test_ulogovan_dobija_formu` | 2.2.1 | Ulogovan vidi formu |
| `test_gost_ne_dobija_formu` | 2.2.3 | Gost ne vidi formu |
| `test_prazan_tekst_nevalidan` | 2.2.2 | Forma: prazan tekst nevalidan |
| `test_validan_tekst` | 2.2.1 | Forma: validan tekst |

---

## 3b. Selenium WebDriver (UI) test primeri

Testovi kroz pravi pretraživač (headless Chrome) simuliraju korisničke akcije.

| SSU | Test | Scenario | Provera kroz UI |
| :---- | :---- | :---- | :---- |
| 4 | `test_lista_prikazuje_objavljene_clanke` | 2.2 | Lista prikazuje objavljene članke |
| 4 | `test_pretraga_po_naslovu_2_2_2` | 2.2.2 | Unos u polje + pretraga filtrira listu |
| 4 | `test_klik_na_clanak_otvara_detalj_2_2_1` | 2.2.1 | Klik na članak otvara pun tekst |
| 6 | `test_prijava_pa_odjava_2_2_1_2_2_2` | 2.2.1 / 2.2.2 | Klik „Prijavi se" → „Odjavi se" → nazad |
| 6 | `test_popunjena_akcija_nema_dugme_2_2_4` | 2.2.4 | Popunjena akcija: nema dugmeta, poruka |
| 7 | `test_uspesno_slanje_ponude_2_2_1` | 2.2.1 | Popuni formu → pošalji → poruka o čekanju |
| 7 | `test_nepotpuna_ponuda_prikazuje_gresku_2_2_2` | 2.2.2 | Prazan opis → prikaz greške |
| 12 | `test_uspesan_komentar_2_2_1` | 2.2.1 | Unos + „Objavi" → komentar se prikaže |
| 12 | `test_prazan_komentar_prikazuje_gresku_2_2_2` | 2.2.2 | Prazan → „Komentar ne može biti prazan!" |
| 12 | `test_gost_ne_vidi_formu_2_2_3` | 2.2.3 | Gost: nema forme, poziv na prijavu |

---

## 4. Nalazi testiranja

Testiranjem **nisu pronađeni funkcionalni defekti** u obrađenim SSU-ovima (4, 6, 7, 12).
Sve testirane funkcionalnosti ponašaju se u skladu sa specifikacijom.

---
