Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti kreiranja akcija

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri kreiranju akcija.

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
|  |  |  |
|  |  |  |
|  |  |  |

# 2\. Scenario kreiranja akcije

## 2.1. Kratak opis

Organizator ima mogućnost da kreira novu volontersku akciju unošenjem sledećih podataka:  
naziv akcije, opis, datum i vreme održavanja, lokacija, maksimalan broj volontera, kategorija  
akcije i kontakt informacije. Kreirana akcija mora biti odobrena od strane jednog od administratora pre nego što postane vidljiva na sajtu. 

## 2.2. Tok događaja

2.2.1. Scenario uspešnog kreiranja akcije

1. Ulogovani organizator bira opciju "Kreiraj akciju" na navigacionoj traci.  
2. Prikazuje mu se forma sa sledećim obaveznim poljima: naziv akcije, opis, datum i vreme održavanja, lokacija (koja se bira preko integrisanog Google Maps prozorčića), maksimalan broj volontera, kategorija akcije, kontakt email i kontakt telefon.  
3. Organizator popunjava sva polja i klikće dugme "Kreiraj akciju".  
4. Sistem proverava unete podatke i kreira akciju.  
5. Organizatoru se prikazuje poruka "Akcija je uspešno kreirana i čeka odobrenje administratora." i korisnik biva preusmeren na stranicu “Moje akcije”.

2.2.2. Scenario nepopunjenih obaveznih polja

1. Organizator popunjava formu za kreiranje akcije, ali ostavlja jedno ili više obaveznih polja praznim, i klikće dugme "Kreiraj akciju".  
2. Sistem proverava unete podatke i prikazuje poruku "Nisu uneta sva obavezna polja."  
3. Organizator ostaje na stranici za kreiranje akcije.

2.2.3. Scenario datuma održavanja u prošlosti

1. Organizator popunjava formu za kreiranje akcije i unosi datum i vreme održavanja koji su u prošlosti, i klikće dugme "Kreiraj akciju".  
2. Sistem proverava unete podatke i prikazuje poruku "Datum održavanja akcije ne sme biti u prošlosti."  
3. Organizator ostaje na stranici za kreiranje akcije.

2.2.4. Scenario nevalidnog broja volontera

1. Organizator popunjava formu za kreiranje akcije i unosi vrednost 0 ili negativnu vrednost za maksimalan broj volontera, i klikće dugme "Kreiraj akciju".  
2. Sistem proverava unete podatke i prikazuje poruku "Maksimalan broj volontera mora biti pozitivan broj."  
3. Organizator ostaje na stranici za kreiranje akcije.

2.2.5. Scenario neispravnog formata kontakt email adrese

1. Organizator popunjava formu za kreiranje akcije, ali u polje za kontakt email unosi adresu pogrešnog formata (bez znaka "@" ili bez domena), i klikće dugme "Kreiraj akciju".  
2. Sistem proverava unete podatke i prikazuje poruku "Kontakt email nije ispravnog formata."  
3. Organizator ostaje na stranici za kreiranje akcije.

2.2.6. Scenario neispravnog formata kontakt telefona

1. Organizator popunjava formu za kreiranje akcije, ali u polje za kontakt telefon unosi vrednost koja sadrži karaktere koji nisu cifre, razmaci, plus ili crtica, i klikće dugme "Kreiraj akciju".  
2. Sistem proverava unete podatke i prikazuje poruku "Kontakt telefon nije ispravnog formata."  
3. Organizator ostaje na stranici za kreiranje akcije.

2.2.7. Scenario odustajanja od kreiranja akcije

1. Organizator otvara formu za kreiranje akcije, delimično je popunjava, a zatim klikće dugme "Odustani".  
2. Sistem ne čuva unete podatke.  
3. Organizator je preusmeren na početnu stranicu.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je ulogovan u ulogu organizatora.

## 2.5. Posledice

Akcija se postavlja u red za odobravanje od strane administratora.