Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti praćenja učešća volontera

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 14.04.2026. | 1.0 | Inicijalna verzija | Stefan Grujičić |
|  |  |  |  |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri praćenju učešća volontera na volonterskim akcijama.

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
| 1 | Na koji način se beleži broj volonterskih sati: automatski na osnovu trajanja akcije, ili ga organizator unosi ručno? |  |
| 2 | Da li volonter može da pregleda detalje svake prethodne akcije, ili samo listu? |  |
|  |  |  |

# 2\. Scenario praćenja učešća volontera

## 2.1. Kratak opis

Registrovani volonter može da pregleda listu akcija na kojima je učestvovao, ukupan broj ostvarenih volonterskih sati (kao vrstu ličnih dostignuća), kao i listu akcija na koje je trenutno prijavljen i čeka se na realizaciju.

## 2.2. Tok događaja

### 2.2.1. Pregled istorije učešća i volonterskih sati

1. Volonter se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Volonter bira sekciju "Moje aktivnosti".  
3. Sistem prikazuje pregled koji sadrži:  
   * Ukupan broj ostvarenih volonterskih sati.  
   * Listu akcija na kojima je volonter učestvovao, sa nazivom akcije, datumom i brojem ostvarenih sati po akciji.  
4. Volonter pregledа istoriju svog učešća.

### 2.2.2. Pregled akcija na koje je volonter trenutno prijavljen

1. Volonter se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Volonter bira sekciju "Moje aktivnosti".  
3. Sistem prikazuje listu akcija na koje je volonter trenutno prijavljen i koje još nisu realizovane, sa nazivom akcije, datumom i statusom prijave (na čekanju / prihvaćena).  
4. Volonter pregledа predstojeće akcije.

### 2.2.3. Pregled kada volonter nema istorije učešća

1. Volonter se prijavljuje na sistem i pristupa svom korisničkom profilu.  
2. Volonter bira sekciju "Moje aktivnosti".  
3. Sistem prikazuje poruku "Još uvek niste učestvovali ni na jednoj akciji." uz poziv da pretraži dostupne akcije.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je uspešno ulogovan kao volonter.

## 2.5. Posledice

Nema promena u bazi podataka. Radi se isključivo o pregledu podataka.