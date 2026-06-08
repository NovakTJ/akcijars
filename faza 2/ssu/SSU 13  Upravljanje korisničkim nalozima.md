Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti upravljanja korisničkim nalozima

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.04.2026. | 1.0 | Inicijalna verzija | Stefan Grujičić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri upravljanju korisničkim nalozima od strane administratora sistema.

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
| 1 | Da li korisnik dobija obaveštenje putem email-a kada mu je nalog odbijen ili uklonjen? |  |
| 2 | Da li administrator mora da navede razlog odbijanja ili uklanjanja naloga? |  |
| 3\.  | Da li korisnik moze da prijavi nekog drugog korisnika i da li administrator ima listu prijavljeni korisnika, ili mora rucno da trazi korsinike kojeg treba da ukloni na bazi prijave? |  |

# 2\. Scenario upravljanja korisničkim nalozima

## 2.1. Kratak opis

Administrator sistema odobrava ili odbija zahteve za kreiranje naloga sponzora i organizatora, koji ne mogu koristiti sistem dok nalog nije odobren. Pored toga, administrator može ukloniti nalog bilo kog korisnika koji krši pravila korišćenja sajta. Nalozi volontera se automatski aktiviraju po registraciji bez potrebe za odobrenjem.

## 2.2. Tok događaja

### 2.2.1. Odobravanje naloga organizatora ili sponzora

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Zahtevi za naloge".  
3. Sistem prikazuje listu naloga koji čekaju na odobrenje, sa podacima o korisniku (ime, tip naloga, datum registracije).  
4. Administrator bira nalog i pregleda detalje korisnika.  
5. Administrator bira opciju "Odobri".  
6. Sistem aktivira nalog korisnika.  
7. Sistem obaveštava korisnika putem Email API-ja da je nalog odobren.

### 2.2.2. Odbijanje zahteva za nalog organizatora ili sponzora

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Zahtevi za naloge".  
3. Sistem prikazuje listu naloga koji čekaju na odobrenje.  
4. Administrator bira nalog i pregleda detalje korisnika.  
5. Administrator bira opciju "Odbij".  
6. Sistem uklanja zahtev i nalog ostaje neaktivan.  
7. Sistem obaveštava korisnika putem Email API-ja da je zahtev odbijen.

### 2.2.3. Uklanjanje naloga korisnika koji krši pravila

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Korisnici".  
3. Sistem prikazuje listu svih registrovanih korisnika.  
4. Administrator pronalazi korisnika čiji nalog treba ukloniti (pretragom po imenu ili korisničkom imenu).  
5. Administrator bira opciju "Ukloni".  
6. Sistem traži potvrdu akcije: "Da li ste sigurni da želite da uklonite nalog korisnika \[Ime korisnika i mejl\]? Ova akcija je nepovratna."  
7. Administrator bira opciju “Ukloni”.  
8. Sistem deaktivira nalog korisnika i uklanja ga iz liste aktivnih korisnika.

Prosirenje:  
7a. Administrator odustaje od odbijanja. 

.1: Administrator bira opciju "Odustani" u dijalogu.   
	.2: Sistem zatvara dijalog, korisnik ostaje na liste aktivnih korisnika.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je prijavljen na sistem sa administratorskim privilegijama.

## 2.5. Posledice

Nakon odobravanja, korisnik može pristupiti funkcionalnostima koje odgovaraju njegovoj ulozi. Nakon odbijanja ili uklanjanja, korisnik ne može pristupiti sistemu.