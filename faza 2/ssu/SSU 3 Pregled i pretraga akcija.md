Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti pregleda i pretrage akcija

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
| 13.5.2026. | 1.1. | Odgovorio na otvorena pitanja i izbacio referencu na komentare | Novak Stijepić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri pregledu i pretrazi akcija.

## 1.2. Namena dokumenta i ciljne grupe

Ovaj dokument će koristiti svi članovi projektnog tima u razvoju projekta i u njegovom testiranju, a može se koristiti i pri pisanju uputstva za upotrebu.

## 1.3. Reference

1. Projektni zadatak  
2. Uputstvo za pisanje specifikacije scenarija upotrebe funkcionalnosti   
3. Guidelines – Use Case, Rational Unified Process 2000  
4. Guidelines – Use Case Storyboard, Rational Unified Process 2000

## 1.4. Otvorena pitanja

| Redni broj | Opis | Rešenje |
| :---- | :---- | :---- |
| 1 | Izabrati vrednost numActionsPerPage (izmedju 1 i 15\) | 9 |
| 2 | Mehanizmi navigacije (prethodna, sledeca, idi na pocetak, idi na kraj, brojevi (koji?)) | Strelice za prethodnu i za sledecu stranicu, broj trenutne, sledece i prethodne stranice, broj 1, i broj poslednje stranice. Brojevi se ne pokazuju duplo. |
| 3 | Uslov poklapanja pretrage od više reči (disjunkcija, konjunkcija, ceo substring) | Ceo substring mora biti isti |

# 2\. Scenario pregleda i pretrage akcije

## 2.1. Kratak opis

Svi korisnici sajta imaju mogućnost da pregledaju objavljene volonterske akcije, kao i da ih pretražuju prema različitim kriterijumima, poput naziva, lokacije, datuma ili tipa akcije. Za pretragu po lokaciji bi se koristio Google Places API.

## 2.2. Tok događaja

Pri ulasku na stranicu pregleda akcija, sistem prikazuje početni prikaz: kontrole za pretragu i filtriranje (polje za pretragu po nazivu/organizatoru, izbor kategorije, izbor statusa, izbor datuma, polje za lokaciju sa izborom radijusa pretrage), kontrolu za sortiranje i prvu stranicu liste akcija. Stranica sadrži najviše numActionsPerPage akcija, sortiranih podrazumevano od najnovije objavljenih. Za svaku akciju su vidljivi naslov, naziv organizatora, kategorija, status, datum održavanja, lokacija i slika akcije, ali ne i pun tekst. Ispod liste se nalaze kontrole za paginaciju i informacija o ukupnom broju pronađenih akcija (npr. „Prikazano 1–9 od 15 akcija"). Tekstualna polja za pretragu prihvataju najvise 64 karaktera.

#### 2.2.1. Scenario pregleda pojedinačne akcije

1. Korisnik klikće na akciju u listi, ili unosi direktan link akcije u pretraživač.  
2. Sistem prikazuje pun tekst akcije sa svim detaljima.

   #### 2.2.2. Scenario pretrage po nazivu ili organizatoru

1. Korisnik upisuje upit u tekstualno polje za pretragu.  
2. Korisnik klikće dugme „Traži" ili pritiska Enter na tastaturi.  
3. Sistem prihvata upit i prikazuje prvu stranicu akcija kod kojih uneti podstring odgovara nazivu akcije ili nazivu organizatora, zajedno sa vidljivim upitom u polju za pretragu.  
4. Korisnik klikće na akciju od interesa, a sistem prikazuje pun tekst akcije kao u scenariju 2.2.1.

   #### 2.2.3. Scenario pretrage po kategoriji

1. Korisnik bira jednu od ponuđenih kategorija iz padajuće liste (kategorije su unapred definisane vrednosti iz enumeracije).  
2. Koraci 3–4 iz scenarija 2.2.2 se ponavljaju, pri čemu su rezultati filtrirani po izabranoj kategoriji.  
3. Ako korisnik izabere opciju „Sve kategorije", filter po kategoriji se poništava.

   #### 2.2.4. Scenario pretrage po statusu

1. Korisnik bira jedan od ponuđenih statusa iz padajuće liste.  
2. Koraci 3–4 iz scenarija 2.2.2 se ponavljaju, pri čemu su rezultati filtrirani po izabranom statusu.  
3. Ako korisnik izabere opciju „Svi statusi", filter po statusu se poništava.

   #### 2.2.5. Scenario pretrage po datumu

1. Korisnik bira datum u polju za datum akcije.  
2. Koraci 3–4 iz scenarija 2.2.2 se ponavljaju, pri čemu su rezultati filtrirani tako da datum održavanja akcije odgovara izabranom datumu.

   #### 2.2.6. Scenario pretrage po lokaciji

1. Korisnik počinje da kuca naziv mesta u polje za lokaciju.  
2. Sistem, koristeći Google Places API, prikazuje listu predloga mesta koja odgovaraju unosu.  
3. Korisnik bira jedan od ponuđenih predloga.  
4. Korisnik opciono menja radijus pretrage iz padajuće liste (podrazumevano 25 km, konfigurabilno).  
5. Koraci 3–4 iz scenarija 2.2.2 se ponavljaju, pri čemu su rezultati filtrirani tako da je lokacija akcije unutar izabranog radijusa od izabranog mesta.

   #### 2.2.7. Scenario kombinovane pretrage

1. Korisnik postavlja više filtera istovremeno (npr. naziv \+ kategorija \+ lokacija sa radijusom).  
2. Korisnik klikće dugme „Traži" ili pritiska Enter.  
3. Sistem prikazuje prvu stranicu akcija koje zadovoljavaju sve postavljene filtere istovremeno (logičko I).  
4. Korisnik klikće na akciju, a sistem prikazuje pun tekst akcije kao u scenariju 2.2.1.

   #### 2.2.8. Scenario sortiranja rezultata

1. Korisnik bira način sortiranja iz padajuće liste: „Najnovije (datum kačenja)”, „Najnovije (datum održavanja)”, „Najbliže" ili „Slobodna mesta".  
2. Sistem preuređuje prikazane rezultate prema izabranom kriterijumu, zadržavajući postavljene filtere i trenutnu stranicu.  
3. Opcija „Najbliže" je dostupna samo kada je u pretrazi izabrana lokacija.

   #### 2.2.9. Scenario navigacije između stranica

1. Korisnik klikće na kontrolu za paginaciju (sledeća stranica, prethodna stranica ili konkretan broj stranice).  
2. Sistem prikazuje odgovarajuću stranicu sa najviše numActionsPerPage akcija, zadržavajući sve postavljene filtere i izabrano sortiranje.  
3. Koraci 1 i 2 se ponavljaju 0 ili više puta, proizvoljnim redom, dok korisnik ne pronađe akciju od interesa.  
4. Korisnik klikće na akciju, a sistem prikazuje pun tekst akcije kao u scenariju 2.2.1.

   #### 2.2.10. Scenario pretrage bez rezultata

1. Nijedna akcija ne zadovoljava postavljene filtere.  
2. Sistem prikazuje poruku „Nema akcija koje odgovaraju zadatim kriterijumima" i predlaže korisniku da izmeni ili poništi filtere.

   #### 2.2.11. Scenario nedozvoljenih karaktera u upitu za pretragu

1. Korisnik upisuje upit u polje za pretragu po nazivu/organizatoru, pri čemu upit sadrži karaktere koji nisu slova, cifre i razmaci.  
2. Korisnik klikće dugme „Traži" ili pritiska Enter.  
3. Sistem odbija upit i prikazuje početni prikaz stranice, uz poruku: „U upitu su dozvoljeni samo slova, cifre i razmaci".

   #### 2.2.12. Scenario odustajanja od pretrage

1. Korisnik bira opciju za poništavanje filtera (ili ručno prazni polja i bira podrazumevane opcije „Sve kategorije", „Svi statusi" itd.).  
2. Sistem prikazuje početni prikaz stranice sa prvom stranicom najnovije objavljenih akcija.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Nema.

## 2.5. Posledice

Nema.  
