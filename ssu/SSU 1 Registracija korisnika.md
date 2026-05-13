Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti registracije korisnika

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 11.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
| 13.5.2026. | 1.1 | Dodato slanje potvrde na email | Novak Stijepić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri registraciji korisnika.

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
| 1 | Da li postoji opcija za registrovanje novog administratora? Da li je vidljiva svima? |  |
| 2 | Da li je potrebno da konfigurišemo rate limiting? |  |
|  |  |  |

# 2\. Scenario registracije korisnika

## 2.1. Kratak opis

Ukoliko korisnik nema svoj nalog, može ga kreirati unošenjem ličnih podataka i izborom tipa  
naloga (volonter, organizator ili sponzor). Podaci se upisuju u bazu podataka. Nalog sponzora i  
organizatora mora biti odobren od strane jednog od administratora pre korišćenja sistema.

## 2.2. Tok događaja

2.2.1. Scenario uspešne registracije volontera

1. Korisnik bira opciju “Registruj se” na navigacionoj traci.  
2. Prikazuje mu se forma sa poljima za email adresu, lozinku, potvrdu lozinke, ime i prezime, kao i padajuća lista za izbor uloge.  
3. Korisnik bira ulogu “volonter”, popunjava sva obavezna polja i klikće dugme “Registruj se”.  
4. Sistem proverava unete podatke i kreira nalog.  
5. Korisniku se prikazuje poruka “Registracija je uspešna. Možete se prijaviti na sistem.”  
6. Na email adresu se salje potvrda registracije.

2.2.2. Scenario uspešne registracije organizatora ili sponzora

1. Korisnik bira opciju “Registruj se” na navigacionoj traci.  
2. Prikazuje mu se forma sa istim poljima kao u scenariju 2.2.1, uz dodatna obavezna polja: naziv organizacije i kontakt telefon.  
3. Korisnik bira ulogu “organizator” ili “sponzor”, popunjava sva polja i klikće dugme “Registruj se”.  
4. Sistem proverava unete podatke i pošalje zahtev administratoru za kreiranje naloga.  
5. Korisniku se prikazuje poruka “Registracija je uspešna. Nalog čeka odobrenje jednog od administratora.”  
6. Na email adresu se salje potvrda registracije.

2.2.3. Scenario neispravnog formata email adrese

1. Korisnik popunjava formu za registraciju, ali unosi email adresu pogrešnog formata (bez znaka “@” ili bez domena), i klikće dugme “Registruj se”.  
2. Sistem proverava unete podatke i prikazuje poruku “Email adresa nije ispravnog formata.”  
3. Korisnik ostaje na stranici za registraciju.

2.2.4. Scenario lozinki koje se ne poklapaju

1. Korisnik popunjava formu za registraciju, ali vrednosti u polju “Lozinka” i polju “Potvrda lozinke” se ne poklapaju, i klikće dugme “Registruj se”.  
2. Sistem proverava unete podatke i prikazuje poruku “Lozinke se ne poklapaju.”  
3. Korisnik ostaje na stranici za registraciju.

2.2.5. Scenario već registrovane email adrese

1. Korisnik popunjava formu za registraciju i unosi email adresu koja već postoji u bazi podataka, i klikće dugme “Registruj se”.  
2. Sistem proverava unete podatke i prikazuje poruku “Korisnik sa tom email adresom već postoji.”  
3. Korisnik ostaje na stranici za registraciju.

2.2.6. Scenario nepopunjenih obaveznih polja

1. Korisnik popunjava formu za registraciju, ali ostavlja jedno ili više obaveznih polja praznim, i klikće dugme “Registruj se”.  
2. Sistem proverava unete podatke i prikazuje poruku “Nisu uneta sva obavezna polja.”  
3. Korisnik ostaje na stranici za registraciju.

2.2.7. Scenario lozinke koja ne zadovoljava minimalne uslove

1. Korisnik popunjava formu za registraciju, ali unosi lozinku koja ima manje od 8 karaktera, ili ne sadrži barem jednu cifru ili specijalni karakter, i klikće dugme “Registruj se”.  
2. Sistem proverava unete podatke i prikazuje poruku “Lozinka mora imati najmanje 8 karaktera i sadržati barem jednu cifru ili specijalni karakter.”  
3. Korisnik ostaje na stranici za registraciju.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik nije ulogovan. Ulogovanom korisniku se ne prikazuje opcija za registraciju.

## 2.5. Posledice

U bazu podataka se upisuje zapis o novom korisniku.  
Korisnik ne postaje ulogovan na kraju ovog scenarija. Da bi se ulogovao, mora proći kroz scenario autorizacije.