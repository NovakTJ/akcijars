Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti slanja informacija prijavljenim volonterima

Verzija 1.1

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 10.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
| 13.5.2026 | 1.1 | Ispravka defekata nakon pregleda \- pojašnjenje primaoca obaveštenja | Maša Nikolić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri slanju informacija prijavljenim volonterima.

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

# 2\. Scenario slanja informacija prijavljenim volonterima

## 2.1. Kratak opis

Organizator može slati obaveštenja volonterima koji su prijavljeni na određenu akciju, uključujući izmene u rasporedu, dodatne informacije, podsetnike i važne napomene, kako bi svi učesnici bili pravovremeno informisani. Ova obaveštenja se automatski šalju putem Email API-ja, čime se olakšava komunikacija.

## 2.2. Tok događaja

### 2.2.1. Korisnik uspešno šalje informacije prijavljenim volonterima

1. Organizator na stranici svojih akcija bira akciju za koju želi da pošalje obaveštenje.  
2. Sistem prikazuje detalje izabrane akcije.  
3. Organizator bira opciju „Pošalji obaveštenje“.  
4. Sistem prikazuje listu volontera koji su prihvaćeni na akciju i formu za unos poruke.  
5. Organizator unosi tekst poruke i pritiska dugme „Pošalji“.  
6. Sistem šalje obaveštenje svim prihvaćenim volonterima putem Email API-ja.

### 2.2.2 Organizator pokušava da pošalje praznu poruku

1-4. Isto kao u scenariju 2.2.1.  
5\. Organizator ne unosi tekst poruke i pritiska „Pošalji“.  
6\. Sistem prikazuje poruku o grešci i zahteva unos teksta.  
7\. Sistem vraća korisnika na korak 7\.

### 2.2.3. Organizator odustaje od slanja obaveštenja

1-4. Isto kao u scenariju 2.2.1.  
 5\. Organizator pritiska dugme „Otkaži“.  
 6\. Sistem zatvara formu za unos poruke.  
 7\. Sistem ne šalje obaveštenje i vraća organizatora na stranicu za pregled volontera akcije.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao organizator, imati kreiranu akciju i najmanje jednog prijavljenog volontera na toj akciji.

## 2.5. Posledice

Sistem je izvršio slanje obaveštenja prijavljenim volonterima.