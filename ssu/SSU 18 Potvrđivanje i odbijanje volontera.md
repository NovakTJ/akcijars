Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti potvrđivanja i odbijanja volontera

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
| 14.5.2026. | 1.1 | Definisano ponasanje sistema u slucaju popunjavanja akcije i preciziran izgled korisnickog interfejsa | Novak Stijepić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri potvrđivanju i odbijanju prijava za volontiranje.

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

# 2\. Scenario potvrđivanja i odbijanja volontera

## 2.1. Kratak opis

Organizator prima prijave za volontiranje i odlučuje da li će ih prihvatiti ili odbiti. Po prihvatanju prijave, volonter dobija obaveštenje putem email-a. U slučaju odbijanja, volonter takođe dobija obaveštenje putem Email API-ja.

## 2.2. Tok događaja

### 2.2.1. Organizator uspešno potvrđuje prijavu volontera

1. Organizator na stranici „Moje akcije" bira akciju za koju želi da pregleda pristigle prijave.  
2. Sistem prikazuje detalje izabrane akcije i listu prijava za volontiranje, podeljenu na prijave na čekanju i prihvaćene volontere.  
3. Organizator bira prijavu koju želi da potvrdi i pritiska dugme „Prihvati".  
4. Sistem proverava da li broj potvrđenih volontera nakon prihvatanja prijave dostiže maksimalan broj volontera za datu akciju.  
5. Sistem evidentira volontera kao potvrđenog za datu akciju.  
6. Sistem šalje obaveštenje volonteru putem Email API-ja da je njegova prijava prihvaćena.

### 2.2.2. Organizator odbija prijavu volontera

1–2. Isto kao u scenariju 2.2.1.   
3\. Organizator bira prijavu koju želi da odbije i pritiska dugme „Odbij".   
4\. Sistem uklanja prijavu iz reda za prijave za volontiranje.   
5\. Sistem šalje obaveštenje volonteru putem Email API-ja da njegova prijava nije prihvaćena.

### 2.2.3. Organizator nema pristiglih prijava

1. Organizator na stranici „Moje akcije" bira akciju za koju želi da pregleda pristigle prijave.  
2. Sistem prikazuje poruku „Trenutno nema pristiglih prijava za volontiranje."

### 2.2.4. Organizator potvrđuje poslednju prijavu cime akcija biva popunjena

1–5. Isto kao u scenariju 2.2.1.  
6\. Sistem označava akciju kao popunjenu.  
7\. Sistem šalje obaveštenje volonteru putem Email API-ja da je njegova prijava prihvaćena.  
8\. Sistem onemogućava prihvatanje novih prijava za volontiranje za datu akciju.

### 2.2.5. Organizator pokušava da potvrdi prijavu nakon sto je akcija popunjena

1–2. Isto kao u scenariju 2.2.1.  
3\. Prikazuje se poruka “Nije moguće prihvatiti više volontera – dostignut je maksimalan broj.”

	

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik mora biti prijavljen na sistem kao organizator i imati kreiranu akciju.

## 2.5. Posledice

U slučaju prihvatanja, volonter je evidentiran u sistemu kao volonter na akciji. U slučaju odbijanja, prijava je uklonjena iz sistema. U oba slučaja volonter dobija obaveštenje putem Email API-ja.