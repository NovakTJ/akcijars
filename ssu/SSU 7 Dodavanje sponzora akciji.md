Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti dodavanje sponzora akciji

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 10.4.2026. | 1.0 | Inicijalna verzija | Maša Nikolić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri dodavanju sponzora akciji.

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

# 2\. Scenario dodavanja sponzora akciji

## 2.1. Kratak opis

Sponzor može da pregleda objavljene akcije i pošalje ponudu o sponzorisanju odabrane akcije. Organizator prima ponudu i može je prihvatiti ili odbiti. Po prihvatanju, sponzor se prikazuje na stranici date akcije.

## 2.2. Tok događaja

### 2.2.1. Korisnik uspešno dodaje sebe kao sponzora akciji

1. Sponzor pregleda listu dostupnih akcija i pritiska na akciju za koju želi da pošalje ponudu.  
2. Sistem prikazuje detalje izabrane akcije.  
3. Sponzor pritiska dugme “Sponzoriši”.  
4. Sistem prikazuje formu za unos podataka o sponzorstvu koja sadrži sledeća polja: unos opisa doprinosa (tekstualno polje), unos vrednosti doprinosa (numeričko polje u evrima), kao i dugmad „Pošalji ponudu“ i „Otkaži“.  
5. Sponzor popunjava formu i pritiska dugme „Pošalji ponudu“.  
6. Sistem evidentira ponudu i prosleđuje je organizatoru na razmatranje.

### 2.2.2. Sponzor šalje nepotpunu ponudu

1-4. Isto kao u scenariju 2.2.1.  
5\.	Sponzor ne popuni sva obavezna polja i pritiska dugme „Pošalji“.  
6\.	Sistem prikazuje poruku o grešci i traži unos svih obaveznih podataka.  
7\.	Sistem vraća korisnika na korak 5\.

### 2.2.3. Sponzor odustaje od slanja ponude

1-4. Isto kao u scenariju 2.2.1.  
 5\. Sponzor pritiska dugme „Otkaži“.  
 6\. Sistem odbacuje unesene podatke o sponzorstvu.  
 7\. Sistem vraća sponzora na stranicu akcije bez slanja ponude.

### 2.2.4. Sponzor pokušava da sponzoriše akciju na kojoj je već sponzor

1. Sponzor pregleda listu dostupnih akcija i pritiska na akciju za koju je već evidentiran kao sponzor.  
2. Sistem prikazuje detalje izabrane akcije.  
3. Dugme "Sponzoriši" je onemogućeno. Sponzor ne može da pošalje novu ponudu.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao sponzor.

## 2.5. Posledice

Ponuda je evidentirana u sistemu i prosleđena organizatoru na razmatranje.