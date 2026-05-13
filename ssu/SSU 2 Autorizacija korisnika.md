Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti autorizacije korisnika

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri autorizacija korisnika.

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
| 1 | Da li je potrebno da konfigurisemo rate limiting? |  |
|  |   |  |
|  |  |  |

# 2\. Scenario autorizacije korisnika

## 2.1. Kratak opis

Svi registrovani korisnici se autorizuju unošenjem korisničkog imena i lozinke. Podaci moraju da  
se poklope sa postojećim podacima u bazi podataka. Nakon potvrđene autorizacije, korisnici  
mogu da pristupe funkcionalnostima koje odgovaraju njihovoj ulozi.

## 2.2. Tok događaja

2.2.1. Scenario uspešne autorizacije

1. Korisnik bira opciju "Prijavi se" na navigacionoj traci.  
2. Prikazuje mu se forma sa poljima za email adresu i lozinku.  
3. Korisnik unosi ispravne kredencijale i klikće dugme "Prijavi se".  
4. Sistem proverava unete podatke.  
5. Korisnik je uspešno autorizovan i preusmeren na ličnu stranicu.

2.2.2. Scenario nepostojeće email adrese

1. Korisnik unosi email adresu koja ne postoji u bazi podataka i lozinku, i klikće dugme "Prijavi se".  
2. Sistem proverava unete podatke i prikazuje poruku "Email adresa ili lozinka nisu ispravni."  
3. Korisnik ostaje na stranici za prijavu.

2.2.3. Scenario neispravne lozinke

1. Korisnik unosi ispravnu email adresu, ali pogrešnu lozinku, i klikće dugme "Prijavi se".  
2. Sistem proverava unete podatke i prikazuje poruku "Email adresa ili lozinka nisu ispravni."  
3. Korisnik ostaje na stranici za prijavu.

2.2.4. Scenario neodobrenog naloga

1. Korisnik unosi ispravne kredencijale naloga organizatora ili sponzora čiji nalog još nije odobren od strane administratora, i klikće dugme "Prijavi se".  
2. Sistem proverava unete podatke i status naloga, i prikazuje poruku "Nalog čeka odobrenje administratora."  
3. Korisnik ostaje na stranici za prijavu.

2.2.5. Scenario odjave korisnika

1. Ulogovani korisnik bira opciju "Odjavi se" na navigacionoj traci.  
2. Sistem odjavljuje korisnika i preusmerava ga na početnu stranicu.

## 2.3. Posebni zahtevi

Potrebno je implementirati heširanje lozinke.

## 2.4. Preduslovi

Nema.

## 2.5. Posledice

Korisnik postaje ulogovan.