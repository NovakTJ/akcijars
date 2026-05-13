Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti pregleda i pretrage članaka

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 11.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
| 13.5.2026. | 1.1 | Odgovorio na otvorena pitanja | Novak Stijepić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri pregledu i pretrazi članaka.

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
| 1 | Izabrati vrednost numArticlesPerPage (izmedju 3 i 30\) | 9 |
| 2 | Mehanizmi navigacije (prethodna, sledeca, idi na pocetak, idi na kraj, brojevi (koji?)) | Strelice za prethodnu i za sledecu stranicu, broj trenutne, sledece i prethodne stranice, broj 1, i broj poslednje stranice. Brojevi se ne pokazuju duplo. |
| 3 | Uslov poklapanja pretrage od više reči (disjunkcija, konjunkcija, ceo substring) | Ceo substring mora biti isti |

# 2\. Scenario pregleda i pretrage članaka

## 2.1. Kratak opis

Svi korisnici sajta imaju mogućnost da pregledaju objavljene članke, kao i da ih pretražuju prema različitim kriterijumima, poput naziva članka, naziva organizatora i kategorije.

## 2.2. Tok događaja

Pri ulasku na stranicu pregleda članaka, sistem prikazuje početni prikaz: kontrole za pretragu i filtriranje (polje za pretragu po nazivu članka ili organizatora, izbor kategorije) i prvu stranicu liste članaka. Stranica sadrži najviše numArticlesPerPage članaka, sortiranih podrazumevano od najnovije objavljenih. Za svaki članak su vidljivi naslov, naziv organizatora, kategorija, datum objavljivanja i slika članka, ali ne i pun tekst. Ispod liste se nalaze kontrole za paginaciju i informacija o ukupnom broju pronađenih članaka (npr. „Prikazano 1–9 od 15 članaka"). Tekstualna polja za pretragu prihvataju najvise 64 karaktera.

#### 2.2.1. Scenario pregleda pojedinačnog članka

1. Korisnik klikće na članak u listi, ili unosi direktan link članka u pretraživač.  
2. Sistem prikazuje pun tekst članka sa svim detaljima i komentarima.

#### 2.2.2. Scenario pretrage po nazivu ili organizatoru

1. Korisnik upisuje upit u tekstualno polje za pretragu.  
2. Korisnik klikće dugme „Traži" ili pritiska Enter na tastaturi.  
3. Sistem prihvata upit i prikazuje prvu stranicu članaka kod kojih uneti podstring odgovara nazivu članka ili nazivu organizatora, zajedno sa vidljivim upitom u polju za pretragu.  
4. Korisnik klikće na članak od interesa, a sistem prikazuje pun tekst članka kao u scenariju 2.2.1.

#### 2.2.3. Scenario pretrage po kategoriji

1. Korisnik bira jednu od ponuđenih kategorija iz padajuće liste (kategorije su unapred definisane vrednosti iz enumeracije).  
2. Koraci 3–4 iz scenarija 2.2.2 se ponavljaju, pri čemu su rezultati filtrirani po izabranoj kategoriji.  
3. Ako korisnik izabere opciju „Sve kategorije", filter po kategoriji se poništava.

#### 2.2.4. Scenario kombinovane pretrage

1. Korisnik postavlja više filtera istovremeno (npr. naziv \+ kategorija).  
2. Korisnik klikće dugme „Traži" ili pritiska Enter.  
3. Sistem prikazuje prvu stranicu članaka koji zadovoljavaju sve postavljene filtere istovremeno (logičko I).  
4. Korisnik klikće na članak, a sistem prikazuje pun tekst članka kao u scenariju 2.2.1.

#### 2.2.5. Scenario navigacije između stranica

1. Korisnik klikće na kontrolu za paginaciju (sledeća stranica, prethodna stranica ili konkretan broj stranice).  
2. Sistem prikazuje odgovarajuću stranicu sa najviše numArticlesPerPage članaka, zadržavajući sve postavljene filtere.  
3. Koraci 1 i 2 se ponavljaju 0 ili više puta, proizvoljnim redom, dok korisnik ne pronađe članak od interesa.  
4. Korisnik klikće na članak, a sistem prikazuje pun tekst članka kao u scenariju 2.2.1.

#### 2.2.6. Scenario pretrage bez rezultata

1. Nijedan članak ne zadovoljava postavljene filtere.  
2. Sistem prikazuje poruku „Nema članaka koji odgovaraju zadatim kriterijumima" i predlaže korisniku da izmeni ili poništi filtere.

#### 2.2.7. Scenario nedozvoljenih karaktera u upitu za pretragu

1. Korisnik upisuje upit u polje za pretragu po nazivu/organizatoru, pri čemu upit sadrži karaktere koji nisu slova, cifre i razmaci.  
2. Korisnik klikće dugme „Traži" ili pritiska Enter.  
3. Sistem odbija upit i prikazuje početni prikaz stranice, uz poruku: „U upitu su dozvoljeni samo slova, cifre i razmaci".

#### 2.2.8. Scenario odustajanja od pretrage

1. Korisnik bira opciju za poništavanje filtera (ili ručno prazni polje za pretragu i bira podrazumevanu opciju „Sve kategorije").  
2. Sistem prikazuje početni prikaz stranice sa prvom stranicom najnovije objavljenih članaka.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Nema.

## 2.5. Posledice

Nema.