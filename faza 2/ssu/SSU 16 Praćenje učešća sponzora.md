Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti praćenja učešća sponzora

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 14.04.2026. | 1.0 | Inicijalna verzija | Stefan Grujičić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri praćenju učešća sponzora u volonterskim akcijama.

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
| 1 | Ko unosi vrednost sponzorskog doprinosa u evrima:  sponzor ili organizator? |  |
|  |  |  |
|  |  |  |

# 2\. Scenario praćenja učešća sponzora

## 2.1. Kratak opis

Registrovani sponzor može da pregleda listu akcija koje je podržao, kao i ukupnu vrednost svog sponzorskog doprinosa merenu u evrima (EUR). Vrednost doprinosa se uzima u obzir bez obzira na formu realizacije (novčana sredstva, roba, usluge ili druga nenovčana davanja).

## 2.2. Tok događaja

### 2.2.1. Pregled istorije sponzorstava i ukupnog doprinosa

1. Sponzor se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Sponzor bira sekciju "Moja sponzorstva".  
3. Sistem prikazuje pregled koji sadrži:  
   * Ukupnu vrednost sponzorskog doprinosa u evrima (EUR).  
   * Listu akcija koje je sponzor podržao, sa nazivom akcije, datumom, tip doprinosa kao i vrednošću doprinosa po akciji.  
4. Sponzor pregledа istoriju svog učešća.

### 2.2.2. Pregled ponuda koje čekaju na odobrenje

1. Sponzor se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Sponzor bira sekciju "Ponude na čekanju".  
3. Sistem prikazuje listu ponuda za sponzorstvo koje sponzor još nije dobio odgovor od organizatora, sa nazivom akcije i datumom slanja ponude.  
4. Sponzor pregledа status svojih aktivnih ponuda.

### 2.2.3. Pregled kada sponzor nema istorije sponzorstva

1. Sponzor se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Sponzor bira sekciju "Moja sponzorstva".  
3. Sistem prikazuje poruku "Još uvek niste podržali nijednu akciju." uz poziv da pretraži dostupne akcije.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je uspešno ulogovan kao sponzor.

## 2.5. Posledice

Nema promena u bazi podataka. Radi se isključivo o pregledu podataka.