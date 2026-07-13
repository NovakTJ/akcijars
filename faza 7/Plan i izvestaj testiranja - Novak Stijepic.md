# Plan i izveštaj testiranja — Novak Stijepic 0124/2023

---

## 1. Uvod

Testirane su sledeće funkcionalnosti:


SSU 3 Pregled i pretraga akcija 
SSU 9 Slanje preporuka korisnicima 
SSU 14 Upravljanje akcijama i člancima
SSU 16 Praćenje učešća sponzora 
SSU 18 Potvrđivanje i odbijanje volontera

---

## 2. Lokacija i pokretanje testova


Jedinični (Django):`test_ssu03_akcije.py`, `test_ssu09_preporuke.py`, `test_ssu14_upravljanje.py`, `test_ssu16_sponzor_panel.py`, `test_ssu18_potvrda_volontera.py`, `_helpers.py`
UI (Selenium WebDriver): `test_ssu03_akcije_ui.py`, `test_ssu09_preporuke_ui.py`, `test_ssu14_upravljanje_ui.py`, `test_ssu16_sponzor_panel_ui.py`, `test_ssu18_potvrda_volontera_ui.py`, `_baza.py`


Pokretanje (iz `faza 5/akcijars`, uz aktiviran venv):
```
python manage.py test main.tests                       # svi jedinični testovi
python manage.py test main.tests.test_ssu03_akcije     # samo jedan SSU (jedinični)
python manage.py test main.tests --keepdb              # bez rekreiranja test baze (brže)

python manage.py test main.tests_ui                    # svi UI (Selenium) testovi
python manage.py test main.tests_ui.test_ssu03_akcije_ui   # samo jedan SSU (UI)
```
Prozor pretraživača se može videti uživo sa `SELENIUM_HEADLESS=0`.
Django automatski pravi izolovanu test bazu (`test_akcijars`), pokreće testove i briše
je na kraju — ne dira produkcionu bazu.

Ubrzanje testova: dodat je modul `akcijars/test_settings.py` koji za testove
koristi brzi MD5 heš lozinki umesto podrazumevanog PBKDF2 (stotine hiljada iteracija)
i email backend u memoriji. `manage.py test` automatski koristi ova podešavanja
(bez potrebe za `--settings`), pa je ceo suite višestruko brži; ostale komande
(`runserver`, `migrate`, …) ostaju na produkcionim podešavanjima.

Rezultat:
- Jedinični testovi: 67 testova za obrađene SSU-ove, svi prolaze (ceo `main.tests` paket: 144 testa, OK).
- UI (Selenium) testovi: 26 testova za obrađene SSU-ove, svi prolaze (ceo `main.tests_ui` paket: 47 testova, OK).

---

## 3. Jedinični test primeri po SSU

### SSU 3 — Pregled i pretraga akcija (`test_ssu03_akcije.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_osnovni_prikaz_stranice` | 2.2 | Stranica akcija se učitava (200), kontekst popunjen |
| `test_pretraga_po_nazivu_2_2_2` | 2.2.2 | Filter po podstringu naziva akcije |
| `test_pretraga_po_organizatoru_2_2_2` | 2.2.2 | Filter po nazivu organizatora |
| `test_neispravan_upit_se_odbija_2_2_11` | 2.2.11 | Nedozvoljeni karakteri → poruka, upit poništen |
| `test_filter_po_kategoriji_2_2_3` | 2.2.3 | Filter po kategoriji |
| `test_filter_po_statusu_2_2_4` | 2.2.4 | Filter po statusu akcije |
| `test_filter_po_datumu_2_2_5` | 2.2.5 | Filter po datumu održavanja |
| `test_sortiranja_rezultata_2_2_8` | 2.2.8 | Sortiranje (datum kačenja/održavanja/slobodna mesta) |
| `test_pretraga_po_lokaciji_2_2_6` | 2.2.6 | Geo-pretraga: samo akcije unutar radijusa |
| `test_nevalidan_radijus_podrazumeva_25_km_2_2_6` | 2.2.6 | Nevalidan radijus → podrazumevanih 25 km |
| `test_sortiranje_po_najblizim_akcijama_2_2_8` | 2.2.8 | Sortiranje „najbliže" po distanci |
| `test_paginacija_prikazuje_devet_po_strani_2_2_9` | 2.2.9 | Paginacija (9 po strani) |

### SSU 9 — Slanje preporuka korisnicima (`test_ssu09_preporuke.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_volonter_aktivira_preporuke_2_2_2` | 2.2.2 | Volonter uključuje preporuke (opt-in) |
| `test_volonter_deaktivira_preporuke_2_2_3` | 2.2.3 | Volonter isključuje preporuke |
| `test_ne_volonter_403` | 2.4 | Ne-volonter → 403 |
| `test_get_nije_dozvoljen_405` | — | GET → 405 |
| `test_neispravan_json_400` | — | Neispravno JSON telo → 400 |
| `test_neprijavljen_korisnik_preusmeren` | 2.4 | Neulogovan → preusmeren |
| `test_bez_prethodnih_prihvacenih_akcija_nema_preporuka_2_2_4` | 2.2.4 | Bez istorije → prazna lista, email se ne šalje |
| `test_bliska_aktivna_akcija_se_preporucuje_2_2_1` | 2.2.1 | Bliska aktivna akcija se preporučuje (sa distancom) |
| `test_udaljena_akcija_se_ne_preporucuje_2_2_3` | 2.2.3 | Akcija van radijusa se izostavlja |
| `test_vec_prijavljena_akcija_se_iskljucuje` | — | Akcija na koju je već prijavljen se izostavlja |
| `test_neaktivna_akcija_se_iskljucuje` | — | Neaktivna akcija nije kandidat |
| `test_rezultat_sortiran_po_distanci_i_ogranicen_limitom` | 2.2.1 | Sortirano po distanci, ograničeno limitom |
| `test_prazna_lista_ne_salje_email_2_2_4` | 2.2.4 | Prazna lista → nijedan email |
| `test_neprazna_lista_salje_jedan_email_2_2_1` | 2.2.1 | Neprazna lista → jedan email volonteru |

### SSU 14 — Upravljanje akcijama i člancima (`test_ssu14_upravljanje.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_odobravanje_akcije_2_2_1` | 2.2.1 | Admin odobrava akciju na čekanju → status odobrena |
| `test_akcija_koja_nije_na_cekanju_400_i_nepostojeca_404` | 2.2.1 | Pogrešan status → 400, nepostojeća → 404 |
| `test_ne_admin_403` (OdobriAkcija) | 2.4 | Ne-admin → 403 |
| `test_get_nije_dozvoljen_405` (OdobriAkcija) | — | GET → 405 |
| `test_brisanje_akcije_2_2_2` | 2.2.2 | Admin briše akciju na čekanju → uklonjena iz baze |
| `test_akcija_koja_nije_na_cekanju_404_i_nepostojeca_404` | 2.2.2 | Nije na čekanju / ne postoji → 404 |
| `test_ne_admin_403` (ObrisiAkcija) | 2.4 | Ne-admin → 403 |
| `test_get_nije_dozvoljen_405` (ObrisiAkcija) | — | GET → 405 |
| `test_odobravanje_clanka_2_2_4` | 2.2.4 | Admin objavljuje članak na čekanju → objavljen |
| `test_clanak_koji_nije_na_cekanju_400_i_nepostojeci_404` | 2.2.4 | Pogrešan status → 400, ne postoji → 404 |
| `test_ne_admin_403` (OdobriClanak) | 2.4 | Ne-admin → 403 |
| `test_get_nije_dozvoljen_405` (OdobriClanak) | — | GET → 405 |
| `test_brisanje_clanka_2_2_5` | 2.2.5 | Admin briše članak na čekanju → uklonjen |
| `test_clanak_koji_nije_na_cekanju_404_i_nepostojeci_404` | 2.2.5 | Nije na čekanju / ne postoji → 404 |
| `test_ne_admin_403` (ObrisiClanak) | 2.4 | Ne-admin → 403 |
| `test_get_nije_dozvoljen_405` (ObrisiClanak) | — | GET → 405 |

### SSU 16 — Praćenje učešća sponzora (`test_ssu16_sponzor_panel.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_sponzor_vidi_panel` | 2.2 | Sponzor uspešno otvara panel (200) |
| `test_volonter_preusmeren_na_home` | 2.4 | Volonter → preusmeren na početnu |
| `test_organizator_preusmeren_na_home` | 2.4 | Organizator → preusmeren na početnu |
| `test_neulogovan_preusmeren_na_prijavu` | 2.4 | Neulogovan → preusmeren na prijavu |
| `test_prazan_panel_2_2_3` | 2.2.3 | Bez ponuda: svi brojači i doprinos = 0 |
| `test_prihvacena_ponuda_2_2_1` | 2.2.1 | Prihvaćena ponuda: broj i ukupan doprinos |
| `test_ponuda_na_cekanju_2_2_2` | 2.2.2 | Ponuda na čekanju u odgovarajućoj grupi |
| `test_odbijena_ponuda_u_odbijenim` | 2.2.2 | Odbijena ponuda u grupi odbijenih |
| `test_doprinos_racuna_samo_prihvacene_2_2_1_i_2_2_2` | 2.2.1 / 2.2.2 | Doprinos = zbir samo prihvaćenih ponuda |
| `test_vise_prihvacenih_se_sabira_2_2_1` | 2.2.1 | Više prihvaćenih se ispravno sabira |
| `test_vidi_samo_svoje_ponude` | — | Sponzor vidi samo svoje ponude, ne tuđe |

### SSU 18 — Potvrđivanje i odbijanje volontera (`test_ssu18_potvrda_volontera.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_prihvatanje_menja_status_salje_email_i_vraca_fragmente_2_2_1` | 2.2.1 | Prihvatanje → status prihvaćena, email, JSON (panel+sidebar) |
| `test_prihvatanje_poslednjeg_mesta_popunjava_akciju_2_2_4` | 2.2.4 | Prihvatanje poslednjeg mesta → akcija „popunjena" |
| `test_drugi_organizator_ne_moze_da_prihvati_403` | 2.4 | Tuđi organizator → 403 |
| `test_neorganizatori_ne_mogu_da_prihvate_403` | 2.4 | Ne-organizator (volonter/sponzor) → 403 |
| `test_nema_prijave_na_cekanju_404` (Prihvati) | — | Nema prijave na čekanju → 404 |
| `test_zatvorena_akcija_ne_menja_prijavu_2_2_5` | 2.2.5 | Popunjena/završena/otkazana → prijava nepromenjena |
| `test_get_nije_dozvoljen_405` (Prihvati) | — | GET → 405 |
| `test_neprijavljen_korisnik_preusmeren_302` (Prihvati) | 2.4 | Neulogovan → 302 |
| `test_odbijanje_menja_status_salje_email_i_vraca_fragmente_2_2_2` | 2.2.2 | Odbijanje → status odbijena, email, JSON |
| `test_drugi_organizator_ne_moze_da_odbije_403` | 2.4 | Tuđi organizator → 403 |
| `test_otkazana_akcija_ne_menja_prijavu` | 2.2.5 | Otkazana akcija → prijava nepromenjena |
| `test_nema_prijave_na_cekanju_404` (Odbij) | — | Nema prijave na čekanju → 404 |
| `test_get_nije_dozvoljen_405` (Odbij) | — | GET → 405 |
| `test_neprijavljen_korisnik_preusmeren_302` (Odbij) | 2.4 | Neulogovan → 302 |

---

## 4. UI (Selenium WebDriver) test primeri po SSU

UI testovi voze pravi headless Chrome kroz interfejs: otvaraju stranice, popunjavaju
forme, klikcu dugmad i čekaju da se AJAX odgovori i modali odraze u DOM-u. Kontrola
pristupa se na UI sloju proverava kao preusmeravanje (nedozvoljeni korisnik ne vidi
panel), što odgovara 403/redirect proverama iz jediničnih testova.

### SSU 3 — Pregled i pretraga akcija (`test_ssu03_akcije_ui.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_osnovni_prikaz_stranice_2_2` | 2.2 | Stranica `/akcije/` se učitava i prikazuje postojeću akciju |
| `test_pretraga_po_nazivu_2_2_2` | 2.2.2 | Unos naziva u pretragu zadržava pogodak, uklanja ostale |
| `test_pretraga_po_organizatoru_2_2_2` | 2.2.2 | Upit po imenu organizatora pronalazi njegove akcije |
| `test_neispravan_upit_se_odbija_2_2_11` | 2.2.11 | Nedozvoljeni karakteri → upozorenje, akcije ostaju |
| `test_filter_po_kategoriji_2_2_3` | 2.2.3 | Izbor kategorije sužava listu (AJAX) |
| `test_filter_po_statusu_2_2_4` | 2.2.4 | Izbor statusa sužava listu (AJAX) |
| `test_sortiranje_po_slobodnim_mestima_2_2_8` | 2.2.8 | Sortiranje po slobodnim mestima stavlja prostraniju akciju prvu |
| `test_paginacija_prikazuje_devet_po_strani_2_2_9` | 2.2.9 | Prva strana 9 kartica, druga strana ostatak (klik na „2") |

> Napomena: geo-pretraga po lokaciji (2.2.6) prikazuje se samo kada je postavljen
> `GOOGLE_MAPS_API_KEY`, pa je van dometa UI sloja i pokrivena je jediničnim testovima.

### SSU 9 — Slanje preporuka korisnicima (`test_ssu09_preporuke_ui.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_volonter_aktivira_preporuke_2_2_2` | 2.2.2 | Volonter uključuje prekidač → potvrda „uključene" (opt-in) |
| `test_volonter_deaktivira_preporuke_2_2_3` | 2.2.3 | Volonter isključuje prekidač → potvrda „isključene" |
| `test_ne_volonter_ne_pristupa_panelu_2_4` | 2.4 | Ne-volonter ne može do panela → preusmeren |

### SSU 14 — Upravljanje akcijama i člancima (`test_ssu14_upravljanje_ui.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_odobravanje_akcije_2_2_1` | 2.2.1 | Admin odobrava akciju (modal potvrde) → red nestaje iz tabele |
| `test_brisanje_akcije_2_2_2` | 2.2.2 | Admin briše akciju (modal potvrde) → uklonjena iz baze |
| `test_odobravanje_clanka_2_2_4` | 2.2.4 | Admin objavljuje članak (modal potvrde) → objavljen |
| `test_brisanje_clanka_2_2_5` | 2.2.5 | Admin briše članak (modal potvrde) → uklonjen |
| `test_ne_admin_ne_pristupa_panelu_2_4` | 2.4 | Ne-admin ne može do admin panela → preusmeren |

### SSU 16 — Praćenje učešća sponzora (`test_ssu16_sponzor_panel_ui.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_sponzor_vidi_panel_2_2` | 2.2 | Sponzor otvara panel i vidi sponzorsku oznaku |
| `test_prazan_panel_2_2_3` | 2.2.3 | Bez ponuda: brojači i doprinos = 0 |
| `test_prihvacena_ponuda_2_2_1` | 2.2.1 | Prihvaćena ponuda ulazi u broj i ukupan doprinos |
| `test_vise_prihvacenih_se_sabira_2_2_1` | 2.2.1 | Ukupan doprinos = zbir svih prihvaćenih ponuda |
| `test_doprinos_racuna_samo_prihvacene_2_2_2` | 2.2.2 | Ponude na čekanju i odbijene se ne računaju u doprinos |
| `test_volonter_preusmeren_na_home_2_4` | 2.4 | Volonter nije sponzor → preusmeren na početnu |

### SSU 18 — Potvrđivanje i odbijanje volontera (`test_ssu18_potvrda_volontera_ui.py`)

| Test | Scenario | Očekivano |
| :---- | :---- | :---- |
| `test_prihvatanje_menja_status_2_2_1` | 2.2.1 | Organizator prihvata prijavu → status „prihvaćena" (AJAX osvežava panel) |
| `test_prihvatanje_poslednjeg_mesta_popunjava_akciju_2_2_4` | 2.2.4 | Prihvatanje poslednjeg mesta popunjava akciju (nema više prihvatanja) |
| `test_odbijanje_menja_status_2_2_2` | 2.2.2 | Organizator odbija prijavu → status „odbijena" |
| `test_drugi_organizator_ne_vidi_panel_2_4` | 2.4 | Tuđi organizator ne vidi upravljački panel akcije |

---

## 5. Nalazi testiranja

Testiranjem (jediničnim i UI/Selenium) nisu pronađeni funkcionalni defekti u
obrađenim SSU-ovima (3, 9, 14, 16, 18). Sve testirane funkcionalnosti ponašaju se u
skladu sa specifikacijom.

---
