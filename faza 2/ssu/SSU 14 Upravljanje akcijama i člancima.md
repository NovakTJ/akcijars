Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti upravljanja akcijama i člancima

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.04.2026. | 1.0 | Inicijalna verzija | Stefan Grujičić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri upravljanju akcijama i člancima od strane administratora sistema.

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
| 1 | Da li organizator dobija obaveštenje kada mu je akcija ili članak odbijen? |  |
| 2 | Da li se volonteri prijavljeni na obrisanu akciju automatski obaveštavaju? |  |
|  |  |  |

# 2\. Scenario upravljanja akcijama i člancima

## 2.1. Kratak opis

Administrator sistema ima mogućnost pregleda svih kreirana akcija i članaka koji čekaju na odobrenje, kao i svih već objavljenih. Administrator može odobriti ili obrisati akciju ili članak. Akcije i članci postaju vidljivi na sajtu tek nakon administratorskog odobravanja.

## 2.2. Tok događaja

### 2.2.1. Odobravanje akcije

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Akcije na čekanju".  
3. Sistem prikazuje listu akcija koje čekaju na odobrenje, sa podacima o akciji (naziv, organizator, datum, lokacija).  
4. Administrator bira akciju i pregleda njene detalje.  
5. Administrator bira opciju "Odobri".  
6. Sistem objavljuje akciju i čini je vidljivom svim korisnicima sajta.

### 2.2.2. Odbijanje akcije

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Akcije na čekanju".  
3. Sistem prikazuje listu akcija koje čekaju na odobrenje, sa podacima o akciji (naziv, organizator, datum, lokacija).  
4. Administrator bira akciju i pregleda njene detalje.  
5. Administrator bira opciju “Obriši”.  
6. Sistem briše akciju sa liste “Akcije na čekanju” i akcija se ne objavljuje.

### 2.2.3. Brisanje akcije

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Sve akcije" (pregled svih akcija, uključujući objavljene i one na čekanju).  
3. Administrator pronalazi akciju koju želi da obriše.  
4. Administrator bira opciju obriši akciju koja je predstavljena slikom kante za smeće.  
5. Sistem traži potvrdu akcije: "Da li ste sigurni da želite da obrišete \[Ime akcije\]? Ova akcija je nepovratna."  
6. Administrator bira opciju “Obriši”.  
7. Sistem briše akciju i uklanja je sa sajta.

Proširenja: 6a. Administrator odustaje od brisanja. 

.1: Administrator bira opciju "Otkaži" u dijalogu.  
	.2: Sistem zatvara dijalog, akcija ostaje na listi akcija.

### 

### 2.2.4. Odobravanje članka

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Članci na čekanju".  
3. Sistem prikazuje listu članaka koji čekaju na odobrenje, sa podacima o članku (naslov, autor, datum kreiranja).  
4. Administrator bira članak i pregleda njegov sadržaj.  
5. Administrator bira opciju "Odobri".  
6. Sistem objavljuje članak i čini ga vidljivim svim korisnicima sajta.

### 2.2.5. Odbijanje članka

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Članci na čekanju".  
3. Sistem prikazuje listu članaka koji čekaju na odobrenje, sa podacima o članku (naslov, autor, datum kreiranja).  
4. Administrator bira članak i pregleda njegov sadržaj.  
5. Sistem traži potvrdu akcije: "Da li ste sigurni da želite da obrišete \[Ime članka \]? Ova akcija je nepovratna."  
6. Administrator bira opciju "Obriši".  
7. Sistem briše članka sa liste “Članci na čekanju" i članka se ne objavljuje.

### 2.2.6. Brisanje članka

1. Administrator se prijavljuje na sistem i pristupa administratorskom panelu.  
2. Administrator bira sekciju "Svi članci" (pregled svih članaka, uključujući objavljene i one na čekanju).  
3. Administrator pronalazi članak koji želi da obriše.  
4. Administrator bira opciju "Obriši".  
5. Sistem traži potvrdu akcije: "Da li ste sigurni da želite da obrišete \[Ime članka \]? Ova akcija je nepovratna."  
6. Administrator bira opciju “Obriši”.  
7. Sistem briše članak i uklanja ga sa sajta.

Proširenja: 6a. Administrator odustaje od brisanja. 

.1: Administrator bira opciju "Otkaži" u dijalogu.

 .2: Sistem zatvara dijalog, članak ostaje na listi članaka.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je prijavljen na sistem sa administratorskim privilegijama.

## 2.5. Posledice

Nakon odobravanja, akcija ili članak postaju vidljivi svim korisnicima sajta. Nakon brisanja, akcija ili članak se trajno uklanjaju sa sajta.