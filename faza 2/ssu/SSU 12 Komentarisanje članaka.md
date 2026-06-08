Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti komentarisanja članaka

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.04.2026. | 1.0 | Inicijalna verzija | Stefan Grujičić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri komentarisanju članaka

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
| 1 | Da li korisnik može da izmeni ili obriše svoj komentar nakon objave? |  |
| 2 | Da li administrator može da briše komentare koji krše pravila? |  |
|  |  |  |

# 2\. Scenario komentarisanja članaka

## 2.1. Kratak opis

Registrovani korisnici mogu da ostave komentar na objavljenom članku. Komentar se unosi u tekstualno polje ispod članka i objavljuje se klikom na odgovarajuće dugme. Neregistrovani korisnici (gosti) nemaju mogućnost ostavljanja komentara.

## 2.2. Tok događaja

### **2.2.1. Uspešno komentarisanje članka**

1. Korisnik pregledа stranicu sa objavljenim člankom.  
2. Korisnik pronalazi sekciju za komentare na dnu stranice.  
3. Korisnik unosi tekst komentara u predviđeno tekstualno polje.  
4. Korisnik bira opciju "Objavi komentar".  
5. Sistem proverava da polje nije prazno.  
6. Sistem objavljuje komentar ispod članka, uz prikaz korisničkog imena autora i datuma objave.

### **2.2.2. Neuspešno komentarisanje – prazno polje**

1. Korisnik pregledа stranicu sa objavljenim člankom.  
2. Korisnik pronalazi sekciju za komentare na dnu stranice.  
3. Korisnik bira opciju "Objavi komentar" bez unosa teksta.  
4. Sistem prikazuje grešku "Komentar ne može biti prazan\!".  
5. Sistem vraća korisnika na korak 3\.

### **2.2.3. Neuspešno komentarisanje – korisnik nije prijavljen**

1. Gost pregledа stranicu sa objavljenim člankom.  
2. Gost pronalazi sekciju za komentare na dnu stranice.  
3. Sekcija za unos komentara nije dostupna. Umesto nje prikazuje se poruka "Prijavite se da biste ostavili komentar.", sa linkom ka stranici za prijavu.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je uspešno ulogovan. Članak na koji se komentariše je objavljen i odobren od strane administratora.

## 2.5. Posledice

Komentar je vidljiv svim korisnicima sajta ispod odgovarajućeg članka.