Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti kreiranja članaka

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 11.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri kreiranju članaka.

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

# 2\. Scenario kreiranja članaka

## 2.1. Kratak opis

Organizator ima mogućnost kreiranja članaka o realizovanim i predstojećim akcijama, koji mogu sadržati naslov, tekst i slike. Nakon što neko od administratora odobri sadržaj, članci se objavljuju na posebnoj stranici sajta posvećenoj obaveštenjima o akcijama.

## 2.2. Tok događaja

### 2.2.1. Korisnik uspešno kreira članak

1. Organizator bira opciju „Kreiraj članak“.  
2. Sistem prikazuje formu za unos podataka koja sadrži sledeća polja: unos naslova članka (tekstualno polje), unos sadržaja članka (veće tekstualno polje), opciju za dodavanje jedne ili više slika (upload fajlova), kao i dugmad „Sačuvaj“ i „Otkaži“.  
3. Organizator popunjava formu i pritiska dugme „Sačuvaj“.  
4. Sistem evidentira članak i prosleđuje ga administratorima na odobravanje.

### 2.2.2. Organizator šalje članak bez naslova

1-2. Isto kao u scenariju 2.2.1.  
3\.	Organizator ne popunjava polje za naslov i pritiska dugme „Sačuvaj“.  
4\.	Sistem prikazuje poruku o grešci i traži unos naslova.  
5\.	Sistem vraća korisnika na korak 3\.

### 2.2.3. Organizator šalje članak bez sadržaja

1-2. Isto kao u scenariju 2.2.1.  
3\.	Organizator ne popunjava polje za sadržaj i pritiska dugme „Sačuvaj“.  
4\.	Sistem prikazuje poruku o grešci i traži unos sadržaja.  
5\.	Sistem vraća korisnika na korak 3\.

### 2.2.4. Organizator odustaje od kreiranja članka

1-2. Isto kao u scenariju 2.2.1.  
 3\. Organizator pritiska dugme „Otkaži“.  
 4\. Sistem odbacuje unesene podatke.  
 5\. Sistem vraća organizatora na prethodnu stranicu bez čuvanja članka.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao organizator.

## 2.5. Posledice

Članak je evidentiran u sistemu i, nakon odobrenja administratora, postaje dostupan na stranici za prikaz članaka.