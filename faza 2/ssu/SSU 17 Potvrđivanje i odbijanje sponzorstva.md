Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti potvrđivanja i odbijanja sponzorstva

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri potvrđivanju i odbijanju sponzorstva.

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

# 2\. Scenario potvrđivanja i odbijanja sponzorstva

## 2.1. Kratak opis

Organizator prima ponude za sponzorstvo koje su poslali sponzori i odlučuje da li će ih prihvatiti ili odbiti. Po prihvatanju ponude, sponzor se prikazuje na stranici date akcije i dobija obaveštenje putem email-a. U slučaju odbijanja, sponzor takođe dobija obaveštenje putem Email API-ja.

## 2.2. Tok događaja

### 2.2.1. Organizator uspešno potvrđuje sponzorstvo

1. Organizator na stranici svojih akcija bira akciju za koju želi da pregleda pristigle ponude.  
2. Sistem prikazuje detalje izabrane akcije.  
3. Organizator bira opciju „Ponude za sponzorstvo".  
4. Sistem prikazuje listu pristiglih ponuda sa detaljima svake ponude (naziv sponzora, opis doprinosa, vrednost u evrima).  
5. Organizator bira ponudu koju želi da potvrdi i pritiska dugme „Prihvati".  
6. Sistem evidentira sponzora kao potvrđenog za datu akciju.  
7. Sistem prikazuje sponzora u sekciji „Sponzori" na stranici akcije.  
8. Sistem šalje obaveštenje sponzoru putem Email API-ja da je njegova ponuda prihvaćena.

### 2.2.2. Organizator odbija ponudu sponzora

1–4. Isto kao u scenariju 2.2.1.   
5\. Organizator bira ponudu koju želi da odbije i pritiska dugme „Odbij".   
6\. Sistem uklanja ponudu iz liste aktivnih ponuda.   
7\. Sistem šalje obaveštenje sponzoru putem Email API-ja da njegova ponuda nije prihvaćena.

### 2.2.3. Organizator nema pristiglih ponuda

1–3. Isto kao u scenariju 2.2.1.   
4\. Sistem prikazuje poruku „Trenutno nema pristiglih ponuda za sponzorstvo."

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao organizator i imati kreiranu akciju.

## 2.5. Posledice

U slučaju prihvatanja, sponzor je evidentiran u sistemu kao sponzor akcije i vidljiv je na stranici akcije. U slučaju odbijanja, ponuda je uklonjena iz sistema. U oba slučaja sponzor dobija obaveštenje putem Email API-ja.