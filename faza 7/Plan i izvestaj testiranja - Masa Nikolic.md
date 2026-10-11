# Plan i izveštaj testiranja — Maša Nikolić 2023/0089

---

## 1. Uvod

Ovde su testirane sledeće funkcionalnosti:

|SSU|Funkcionalnost|Autor implementacije|
|-|-|-|
|1|Registracija korisnika|Novak Stijepić|
|13|Upravljanje korisničkim nalozima (admin)|Stefan Grujičić|
|15|Praćenje učešća volontera|Stefan Grujičić|
|17|Potvrđivanje i odbijanje sponzorstva|Stefan Grujičić|

---

## 2. Lokacija i pokretanje testova

|Vrsta|Lokacija|Fajlovi|
|-|-|-|
|Jedinični (Django)|faza 5/akcijars/main/tests/|test_ssu01_registracija.py, <br />test_ssu13_nalozi.py, <br />test_ssu15_pracenje.py, <br />test_ssu17_sponzorstvo.py, <br />_helpers.py|
|UI (Selenium WebDriver)|faza 5/akcijars/main/tests_ui/|test_ssu01_registracija_ui.py, <br />test_ssu13_nalozi_ui.py, <br />test_ssu15_pracenje_ui.py, <br />test_ssu17_sponzorstvo_ui.py, <br />_baza.py|

**Pokretanje** (iz faza 5/akcijars, uz aktiviran venv):

```
python manage.py test main.tests       # jedinični
python manage.py test main.tests_ui    # UI Selenium
python manage.py test main             # oba zajedno
```

**Preduslovi za UI testove:** instaliran selenium i **Google Chrome**.

Zajedničke fabrike test podataka (_helpers.py) i osnovna Selenium klasa (_baza.py) su deljene sa ostalim članovima tima i dopunjene su fabrikama administrator(), prijava() i ponuda() potrebnim za SSU 13/15/17.



**Rezultat:** 39 jediničnih + 11 UI = **50 testova, svi prolaze**.

---

## 3. Test primeri po SSU

### SSU 1 — Registracija korisnika (test_ssu01_registracija.py)

|Test|Scenario|Očekivano|
|-|-|-|
|test_uspesna_registracija_volontera_2_2_1|2.2.1|Nalog kreiran, tačna poruka, email poslat, korisnik nije ulogovan|
|test_registracija_organizatora_2_2_2|2.2.2|Poruka o čekanju odobrenja, status "na čekanju", email|
|test_registracija_sponzora_2_2_2|2.2.2|Sponzor dobija status "na čekanju"|
|test_neispravan_email_2_2_3|2.2.3|Poruka "Email adresa nije ispravnog formata."|
|test_lozinke_se_ne_poklapaju_2_2_4|2.2.4|Poruka "Lozinke se ne poklapaju."|
|test_postojeci_email_2_2_5|2.2.5|Poruka "Korisnik sa tom email adresom već postoji."|
|test_prazna_obavezna_polja_2_2_6|2.2.6|Poruka "Nisu uneta sva obavezna polja."|
|test_slaba_lozinka_2_2_7|2.2.7|Poruka o minimalnim uslovima lozinke|
|test_ulogovan_korisnik_preusmeren_preduslov_2_4|2.4|Ulogovan korisnik -> preusmeren (302)|
|test_neispravan_telefon_organizatora|—|Neispravan telefon organizatora -> greška na polju|

### SSU 13 — Upravljanje korisničkim nalozima (test_ssu13_nalozi.py)

|Test|Scenario|Očekivano|
|-|-|-|
|test_admin_vidi_panel|2.4|Admin otvara kontrolnu tablu (200)|
|test_ne_admin_preusmeren|2.4|Ne-admin -> preusmeren (302)|
|test_odobrenje_organizatora_2_2_1|2.2.1|Status "odobren", email, nalog aktivan|
|test_odobrenje_sponzora|2.2.1|Sponzor odobren|
|test_vec_odobren_nalog_400|—|Nalog koji nije na čekanju -> 400|
|test_nepostojeci_korisnik_404|—|Nepostojeći korisnik -> 404|
|test_ne_admin_403 (odobri)|2.4|Ne-admin -> 403|
|test_get_nije_dozvoljen_405|—|GET -> 405|
|test_odbijanje_organizatora_2_2_2|2.2.2|Status "odbijen", email, nalog neaktivan|
|test_uklanjanje_korisnika_2_2_3|2.2.3|Korisnik obrisan iz baze|
|test_admin_ne_moze_sam_sebe|—|Admin ne može ukloniti sebe -> 400|
|test_ne_admin_403 (ukloni)|2.4|Ne-admin -> 403|

### SSU 15 — Praćenje učešća volontera (test_ssu15_pracenje.py)

|Test|Scenario|Očekivano|
|-|-|-|
|test_volonter_vidi_panel|2.4|Volonter otvara panel (200)|
|test_ne_volonter_preusmeren|2.4|Ne-volonter -> preusmeren (302)|
|test_prazan_panel_2_2_3|2.2.3|Bez učešća: sve nule|
|test_tekuca_prijava_2_2_2|2.2.2|Prijava na aktivnu akciju je među tekućima|
|test_zavrsena_akcija_u_istoriji_2_2_1|2.2.1|Prihvaćena na završenu akciju -> istorija|
|test_ukupno_sati_je_zbir_prihvacenih_2_2_1|2.2.1|Ukupni sati = zbir prihvaćenih prijava|
|test_sati_ne_racunaju_prijave_na_cekanju|2.2.1|Prijava na čekanju ne broji sate|
|test_odbijena_prijava_u_istoriji|—|Odbijena prijava -> istorija|
|test_vidi_samo_svoje_prijave|—|Volonter vidi samo svoje prijave|

### SSU 17 — Potvrđivanje i odbijanje sponzorstva (test_ssu17_sponzorstvo.py)

|Test|Scenario|Očekivano|
|-|-|-|
|test_prihvatanje_menja_status_2_2_1|2.2.1|Ponuda -> status "prihvaćena"|
|test_prihvatanje_salje_email_2_2_1|2.2.1|Sponzor dobija email o prihvatanju|
|test_samo_organizator_akcije_403|2.4|Drugi organizator -> 403|
|test_vec_obradjena_ponuda_400|—|Već obrađena ponuda -> 400|
|test_nepostojeca_ponuda_404|—|Nepostojeća ponuda -> 404|
|test_get_nije_dozvoljen_405|—|GET -> 405|
|test_odbijanje_menja_status_2_2_2|2.2.2|Ponuda -> status "odbijena"|
|test_odbijanje_salje_email_2_2_2|2.2.2|Sponzor dobija email o odbijanju|

---

## 3b. Selenium WebDriver (UI) test primeri

Testovi kroz pravi pretraživač (headless Chrome) simuliraju korisničke akcije.

|SSU|Test|Scenario|Provera kroz UI|
|-|-|-|-|
|1|test_uspesna_registracija_volontera|2.2.1|Popuni formu -> poruka o uspehu, nalog kreiran|
|1|test_lozinke_se_ne_poklapaju|2.2.4|Različite lozinke -> prikaz greške|
|1|test_prazna_polja|2.2.6|Prazna forma -> "Nisu uneta sva obavezna polja."|
|13|test_admin_odobrava_nalog|2.2.1|Klik "Odobri" -> modal -> zahtev nestane (Ajax), nalog odobren|
|13|test_admin_odustaje_od_uklanjanja|2.2.3 (7a)|Klik "Ukloni" -> "Otkaži" -> korisnik ostaje|
|13|test_ne_admin_ne_pristupa_panelu|2.4|Volonter -> preusmeren sa admin panela|
|15|test_panel_prikazuje_sate_i_tekucu_prijavu|2.2.1 / 2.2.2|Panel prikazuje sate i tekuću prijavu|
|15|test_prazan_panel_2_2_3|2.2.3|Bez učešća: 0 sati + propisana poruka|
|15|test_ne_volonter_ne_pristupa_panelu|2.4|Organizator -> preusmeren sa volonterskog panela|
|17|test_organizator_prihvata_ponudu|2.2.1|Prihvati ponudu -> sponzor vidljiv na akciji|
|17|test_prazne_ponude_2_2_3|2.2.3|Bez ponuda -> propisana poruka|

---

## 4. Nalazi testiranja

Testiranje je vršeno **prema SSU dokumentima**. Ovim pristupom su otkrivena sledeća **odstupanja implementacije od specifikacije**, koja su potom ispravljena:

|SSU|Odstupanje (u odnosu na SSU)|Status|
|-|-|-|
|15, 2.2.3|Prazna istorija prikazivala "Nema istorije prijava." umesto propisane poruke "Još uvek niste učestvovali ni na jednoj akciji."|Ispravljeno|
|17, 2.2.3|Prazna lista ponuda prikazivala "Nema pristiglih ponuda za sponzorstvo." umesto propisane "Trenutno nema pristiglih ponuda za sponzorstvo."|Ispravljeno|

Za SSU 1 (registracija) i SSU 13 (upravljanje nalozima) **nisu pronađena odstupanja** — implementacija se u potpunosti ponaša u skladu sa specifikacijom.

Nakon ispravki, **svih 50 testova prolazi**.

---

