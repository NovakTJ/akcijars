Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti slanja preporuke korisniku

Verzija 1.1

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 11.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
| 13.5.2026. | 1.1 | Ispravka defekata nakon pregleda \- dodato otvoreno pitanje  | Maša Nikolić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri slanju preporuke korisniku.

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
| 1 | Da li se preporuke korisnicima šalju periodično (i koliko često) ili ih okida neki određeni događaj u sistemu (npr. objavljivanje nove akcije)?  |  |
|  |  |  |

# 2\. Scenario slanja preporuka korisnicima

## 2.1. Kratak opis

Korisnici mogu da se prijave da putem email-a dobijaju obaveštenja o akcijama koje bi mogle da im budu od interesa. Tada bi sistem automatski mogao da šalje prijavljenom korisniku preporuke za akcije na bazi prethodnih akcija na kojima je dati korisnik učestvovao. Kako bi preporuke bile što relevantnije i korisnicima olakšale pronalaženje, koristiće se Google Maps API za identifikaciju akcija koje se nalaze u blizini lokacija prethodnih akcija na kojima je korisnik učestvovao. Preporuke će se automatski slati pomoću Email API-ja.

## 2.2. Tok događaja

### 2.2.1.  Sistem uspešno šalje preporuke korisniku

1. Sistem periodično generiše preporuke za korisnike koji su dali saglasnost za primanje obaveštenja.  
2. Sistem analizira prethodne akcije korisnika.  
3. Sistem pronalazi relevantne akcije na osnovu lokacije (Google Maps API) i drugih kriterijuma.  
4. Sistem generiše listu preporučenih akcija.  
5. Sistem šalje preporuke korisniku putem Email API-ja.

### 2.2.2. Korisnik uspešno aktivira primanje preporuka

1. Korisnik otvara stranicu svog profila.  
2. Sistem prikazuje podešavanja profila.  
3. Korisnik pronalazi opciju „Preporuke" i označava polje „Aktiviraj preporuke akcija".  
4. Sistem beleži korisnikovu saglasnost.

### 2.2.3. Korisnik deaktivira primanje preporuka

1. Korisnik otvara stranicu svog profila.  
2. Sistem prikazuje podešavanja profila.  
3. Korisnik pronalazi opciju „Preporuke akcija" i poništava oznaku polja „Aktiviraj preporuke akcija".  
4. Sistem beleži promenu.  
5. Sistem prestaje sa slanjem preporuka tom korisniku.

### 2.2.4. Nema dostupnih preporuka

1–2. Isto kao u scenariju 2.2.1.  
3\. Sistem ne pronalazi odgovarajuće akcije.  
4\. Sistem ne šalje email.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je prijavljen na sistem kao volonter.   
Za scenarije 2.2.1, 2.2.3 i 2.2.4, korisnik mora imati aktiviranu opciju za primanje preporuka.  
Za scenario 2.2.2 korisnik mora imati deaktiviranu opciju za primanje preporuka.

## 2.5. Posledice

Korisnik prima email sa preporučenim akcijama. 