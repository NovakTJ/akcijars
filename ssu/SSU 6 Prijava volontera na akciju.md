Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# AkcijaRS

Tim VolonTech

## Specifikacija scenarija upotrebe funkcionalnosti prijave i odjave volontera na akciju

Verzija 1.0

Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 12.4.2026. | 1.0 | Inicijalna verzija | Novak Stijepić |
| 13.5.2026. | 1.1 | Dodate sekcije 2.2.5 i 2.2.6 | Novak Stijepić |
| 14.5.2026. | 1.2 | Izbrisana sekcija 2.2.6 | Novak Stijepić |

# 1\. Uvod

## 1.1. Rezime

Definisanje scenarija upotrebe pri prijavi i odjavi volontera na akciju.

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

# 2\. Scenario prijave ili odjave volontera na akciju

## 2.1. Kratak opis

Registrovani volonter može da se prijavi na bilo koju objavljenu akciju koja je otvorena za  
prijave. Organizator ima mogućnost da prihvati ili odbije prijavu volontera. Po prihvatanju  
prijave, volonter dobija obaveštenje putem email-a. Email se automatski šalje volonteru  
korišćenjem email API-ja. Volonter može da se odjavi sa akcije, pre ili posle dobijanja mejla.

## 2.2. Tok događaja

2.2.1. Scenario uspešne prijave volontera na akciju

1. Ulogovani volonter pregledava stranicu akcije koja je otvorena za prijave i ima slobodnih mesta.  
2. Volonter klikće dugme "Prijavi se".  
3. Sistem registruje prijavu.  
4. Volonteru se prikazuje poruka "Uspešno ste se prijavili na akciju. Čekajte potvrdu organizatora."

2.2.2. Scenario odjave volontera pre potvrde organizatora

1. Volonter čija prijava još nije razmotrena od strane organizatora otvara stranicu akcije i klikće dugme "Odjavi se".  
2. Sistem briše prijavu iz reda za odobrenje.  
3. Volonteru se prikazuje poruka "Uspešno ste se odjavili sa akcije."

2.2.3. Scenario odjave volontera nakon potvrde organizatora

1. Volonter čija je prijava prihvaćena otvara stranicu akcije i klikće dugme "Odjavi se".  
2. Sistem briše volontera sa liste odobrenih učesnika i oslobađa jedno mesto na akciji.  
3. Volonteru se prikazuje poruka "Uspešno ste se odjavili sa akcije."

2.2.4. Scenario prijave na popunjenu akciju

1. Volonter pregledava stranicu akcije koja nema slobodnih mesta.  
2. Dugme "Prijavi se" nije prikazano, već se prikazuje poruka "Sva mesta na ovoj akciji su popunjena." Samim tim, volonter ne može da se prijavi na akciju.

2.2.5. Scenario prijave na akciju za koju se korisnik vec prijavio

1. Volonter pregledava stranicu akcije za koju se vec prijavio.  
2. Volonteru se ne prikazuje dugme “Prijavi se”, vec samo dugme “Odjavi se”.

## 2.3. Posebni zahtevi

Nema.

## 2.4. Preduslovi

Korisnik je uspešno ulogovan kao volonter.

## 2.5. Posledice

U slučaju prijave, korisnik se stavlja u red za odobrenje.  
U slučaju odjave, korisnik se briše iz reda za odobrenje ili iz liste odobrenih volontera.  
