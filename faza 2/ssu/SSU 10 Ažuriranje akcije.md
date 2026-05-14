Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti ažuriranja akcije

Verzija 1.1

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
| 13.5.2026 | 1.1 | Ispravka defekata nakon pregleda \- dodato otvoreno pitanje i pojašnjeno vlasništvo nad akcijom u toku događaja  | Maša Nikolić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri ažuriranju akcije.

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
| 1 | Da li izmena već objavljene akcije zahteva ponovno odobrenje administratora pre nego što izmene postanu javno vidljive? | Ne. |
|  |  |  |
|  |  |  |

# 2\. Scenario ažuriranja akcije

## 2.1. Kratak opis

Organizator ima mogućnost da ažurira svoje objavljene akcije, tako što bi imao opciju dodavanja fotografija pre i posle akcije, menjanje datuma održavanja, otkazivanje akcije i drugih relevantnih izmena.

## 2.2. Tok događaja

### 2.2.1. Korisnik uspešno ažurira akciju

1. Organizator na stranici akcija bira akciju koju je kreirao i koju želi da ažurira.   
2. Sistem prikazuje detalje izabrane akcije.  
3. Organizator bira opciju „Izmeni akciju“.  
4. Sistem prikazuje formu sa postojećim podacima (naziv akcije, opis, datum i vreme održavanja, lokacija, maksimalan broj volontera, kategorija akcije, kontakt email i kontakt telefon, kao i opciju za dodavanje slika).  
5. Organizator menja željene podatke i klikće dugme „Sačuvaj izmene“.  
6. Sistem proverava unete podatke i ažurira akciju.  
7. Sistem šalje obaveštenje svim prijavljenim volonterima o izmenama akcije putem Email API-ja.  
8. Organizatoru se prikazuje poruka „Izmene su uspešno sačuvane.“

### 2.2.2. Korisnik ostavlja obavezna polja nepopunjena

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije, ali ostavlja jedno ili više obaveznih polja praznim i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Nisu uneta sva obavezna polja.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.3. Korisnik unosi datum iz prošlosti

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije i unosi datum i vreme održavanja koji su u prošlosti i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Datum održavanja akcije ne sme biti u prošlosti.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.4. Korisnik unosi nevalidan broj volontera

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije i unosi vrednost 0 ili negativnu vrednost za maksimalan broj volontera i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Maksimalan broj volontera mora biti pozitivan broj.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.5. Korisnik unosi maksimalan broj volontera manji od broja već prihvaćenih volontera

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije i unosi maksimalan broj volontera koji je manji od broja već prihvaćenih volontera i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Maksimalan broj volontera ne može biti manji od broja već prihvaćenih volontera.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.6. Korisnik unosi neispravan format kontakt email adrese

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije i u polje za kontakt email unosi adresu pogrešnog formata (bez znaka "@" ili bez domena), i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Kontakt email nije ispravnog formata.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.7. Korisnik unosi neispravan format kontakt telefona

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije i u polje za kontakt telefon unosi vrednost koja sadrži karaktere koji nisu cifre, razmaci, plus ili crtica, i klikće dugme „Sačuvaj izmene“.  
6\. Sistem proverava unete podatke i prikazuje poruku „Kontakt telefon nije ispravnog formata.“  
7\. Sistem zadržava korisnika na formi za izmenu akcije.

### 2.2.8. Korisnik odustaje od menjanja akcije

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator menja podatke akcije, a zatim klikće dugme „Otkaži“.  
6\. Sistem vraća korisnika na stranicu sa detaljima akcije bez čuvanja izmena.

### 2.2.9. Organizator otkazuje akciju

1–3. Isto kao u scenariju 2.2.1.   
4\. Organizator bira opciju „Otkaži akciju".   
5\. Sistem traži potvrdu: „Da li ste sigurni da želite da otkažete ovu akciju?"   
6\. Organizator potvrđuje otkazivanje.   
7\. Sistem menja status akcije u „Otkazana".   
8\. Sistem šalje obaveštenje svim prijavljenim volonterima o otkazivanju akcije putem Email API-ja.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao organizator i imati kreiranu akciju.

## 2.5. Posledice

Izmene nad akcijom su uspešno evidentirane u sistemu i vidljive pri njenom pregledu.