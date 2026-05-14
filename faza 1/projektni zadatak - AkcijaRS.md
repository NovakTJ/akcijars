Elektrotehnički fakultet u Beogradu  
SI3PSI Principi Softverskog Inženjerstva

# 

# AkcijaRS

![][image1]

Tim VolonTech

Projektni zadatak  
Verzija 1.0  
Istorija izmena

| Datum | Verzija | Kratak opis | Autori |
| :---- | :---- | :---- | :---- |
| 05.04.2026. | 1.0 | Inicijalna verzija | Grujičić Stefan, Nikolić Maša, Milošević Milica |
| 14.05.2026. | 1.1 | Ispravke nakon formalne inspekcije | Grujičić Stefan, Nikolić Maša, Milošević Milica, Novak Stijepić  |

Sadržaj

[**1\. Uvod	5**](#1.-uvod)

[1.1. Rezime	5](#1.1.-rezime)

[1.2. Namena dokumenta i ciljne grupe	5](#1.2.-namena-dokumenta-i-ciljne-grupe)

[**2\. Opis problema	5**](#2.-opis-problema)

[**3\. Kategorije korisnika	6**](#3.-kategorije-korisnika)

[3.1. Gost sajta	6](#3.1.-gost-sajta)

[3.2. Volonter	6](#3.2.-volonter)

[3.3. Organizator	6](#3.3.-organizator)

[3.4. Sponzor	6](#3.4.-sponzor)

[3.5. Administrator	6](#3.5.-administrator)

[**4\. Opis proizvoda	7**](#4.-opis-proizvoda)

[4.1. Pregled arhitekture	7](#4.1.-pregled-arhitekture)

[4.2. Pregled	7](#4.2.-pregled)

[4.3. Integracija sa eksternim servisima	8](#4.3.-integracija-sa-eksternim-servisima)

[4.3.1. Google Maps API	8](#4.3.1.-google-maps-api)

[4.3.2. Email API	8](#4.3.2.-email-api)

[**5\. Funkcionalni zahtevi	9**](#5.-funkcionalni-zahtevi)

[5.1. Registracija korisnika	9](#5.1.-registracija-korisnika)

[5.2. Autorizacija korisnika	9](#5.2.-autorizacija-korisnika)

[5.3. Pregled i pretraga akcija	9](#5.3.-pregled-i-pretraga-akcija)

[5.4. Pregled i pretraga članaka	9](#5.4.-pregled-i-pretraga-članaka)

[5.5. Kreiranje akcija	9](#5.5.-kreiranje-akcija)

[5.6. Prijava volontera na akciju	9](#5.6.-prijava-volontera-na-akciju)

[5.7. Dodavanje sponzora akciji	10](#5.7.-dodavanje-sponzora-akciji)

[5.8. Slanje informacija prijavljenim volonterima	10](#5.8.-slanje-informacija-prijavljenim-volonterima)

[5.9. Slanje preporuka korisnicima	10](#5.9.-slanje-preporuka-korisnicima)

[5.10. Ažuriranje akcije	10](#5.10.-ažuriranje-akcije)

[5.11. Kreiranje članaka o akcijama	10](#5.11.-kreiranje-članaka-o-akcijama)

[5.12. Komentarisanje članaka	10](#5.12.-komentarisanje-članaka)

[5.13. Upravljanje korisničkim nalozima	10](#5.13.-upravljanje-korisničkim-nalozima)

[5.14. Upravljanje akcijama i člancima	11](#5.14.-upravljanje-akcijama-i-člancima)

[5.15. Praćenje učešća volontera	11](#5.15.-praćenje-učešća-volontera)

[5.16. Praćenje učešća sponzora	11](#5.16.-praćenje-učešća-sponzora)

[**6\. Pretpostavke i ograničenja	12**](#6.-pretpostavke-i-ograničenja)

[**7\. Kvalitet	12**](#7.-kvalitet)

[**8\. Nefunkcionalni zahtevi	12**](#8.-nefunkcionalni-zahtevi)

[8.1. Sistemski zahtevi	12](#8.1.-sistemski-zahtevi)

[8.2. Ostali zahtevi	12](#8.2.-ostali-zahtevi)

[**9\. Zahtevi za korisničkom dokumentacijom	13**](#9.-zahtevi-za-korisničkom-dokumentacijom)

[9.1. Uputstva za korišćenje sajta	13](#9.1.-uputstva-za-korišćenje-sajta)

[9.2. Označavanje	13](#9.2.-označavanje)

[**10\. Plan i prioriteti	13**](#10.-plan-i-prioriteti)

# 

# 1\. Uvod {#1.-uvod}

## 1.1. Rezime {#1.1.-rezime}

Projekat AkcijaRS je deo praktične nastave na predmetu Principi softverskog inženjerstva. Aplikacija je namenjena osobama koje žele da učestvuju u volonterskim akcijama, organizuju ih ili ih podrže kroz sponzorstva. Cilj joj je da obezbedi jedinstvenu platformu na kojoj korisnici mogu da pronađu, kreiraju i koordinišu volonterske aktivnosti na jednom mestu. Sajt omogućava pregled, najavu i pretragu akcija, prijavu volontera, dodavanje sponzora, kao i obaveštavanje svih učesnika o relevantnim informacijama.

## 1.2. Namena dokumenta i ciljne grupe  {#1.2.-namena-dokumenta-i-ciljne-grupe}

Ovaj dokument definiše namenu projekta, kategorije korisnika i osnovne funkcionalne i nefunkcionalne zahteve. Dokument je namenjen svim članovima projektnog tima, kao i klijentu, kako bi se definisala materija koju treba modelovati.

# 2\. Opis problema {#2.-opis-problema}

Organizacija volonterskih akcija u praksi često nailazi na probleme koordinacije između volontera, organizatora i sponzora. Komunikacija se obično odvija putem više različitih kanala (društvene mreže, email, telefon), što dovodi do gubitka informacija i neefikasnosti. Takođe, volonteri nemaju centralizovano mesto gde bi mogli da pronađu akcije u svojoj blizini i prijave se za učešće. Ovaj sistem rešava navedene probleme obezbeđujući jedinstven portal na kome organizatori kreiraju i objavljuju akcije, volonteri ih pretražuju i prijavljuju se, a sponzori nude svoju podršku.

Gosti sajta imaju mogućnost da pregledaju objavljene akcije i obaveštenja, ali bez mogućnosti prijave. Volonteri se mogu prijavljivati na akcije, pratiti svoje učešće i dobijati obaveštenja. Organizatori kreiraju akcije, upravljaju volonterima i sponzorima, i kreiraju članke o realizovanim akcijama. Sponzori pregledaju akcije i šalju ponude za sponzorstvo. Administrator nadgleda celokupan sadržaj sajta i odobrava naloge korisnika.

# 

# 3\. Kategorije korisnika  {#3.-kategorije-korisnika}

Razlikujemo sledeće kategorije korisnika: gost sajta, volonter, organizator, sponzor i administrator sistema.

## 3.1. Gost sajta {#3.1.-gost-sajta}

Gost sajta može da pregleda objavljene volonterske akcije, čita članke o akcijama i pretražuje akcije po različitim kriterijumima (naziv, lokacija, datum, tip). Gost nema mogućnost prijave na akcije niti bilo kakve interakcije sa sistemom koja zahteva registraciju. Gost ima mogućnost da se registruje kao volonter, organizator ili sponzor.

## 3.2. Volonter {#3.2.-volonter}

Volonter je registrovani korisnik koji se prijavljuje na sajt unošenjem email adrese i lozinke. Volonter poseduje sve funkcionalnosti gosta, uz dodatne mogućnosti: prijavu na volonterske akcije, pregled akcija na kojima je učestvovao i ukupan broj volonterskih sati (kao vrstu dostignuća), pregled akcija na koje je trenutno prijavljen, primanje obaveštenja o akcijama na koje se prijavio, kao i primanje predloga o akcijama koje bi mogle da mu budu interesantne ako se da saglasnost za takva obaveštenja i ostavljanje komentara na člancima.

## 3.3. Organizator {#3.3.-organizator}

Organizator je registrovani korisnik zadužen za kreiranje i upravljanje volonterskim akcijama. Organizator ima mogućnost kreiranja akcija, modifikovanja akcija koje je kreirao, prihvatanja volontera na akcije, prihvatanja sponzora, kreiranja članaka o akcijama i slanja obaveštenja volonterima.

## 3.4. Sponzor {#3.4.-sponzor}

Sponzor je registrovani korisnik koji poseduje sve funkcionalnosti gosta sajta, uz dodatnu mogućnost da šalje ponude o sponzorisanju akcija koje mu se sviđaju, takođe, ima i mogućnost pregleda akcija koje je do sada podržao, kao i da ostavlja komentare na člancima.

## 3.5. Administrator {#3.5.-administrator}

Administrator sistema ima mogućnost pregleda svih objavljenih akcija i članaka, njihovo odobravanje ili brisanje. Takođe, administrator odobrava kreiranje naloga za sponzore i organizatore. Administrator vodi računa o celokupnom funkcionisanju sistema.

# 4\. Opis proizvoda  {#4.-opis-proizvoda}

U ovoj sekciji opisani su osnovni pojmovi od značaja za projekat AkcijaRS. Dat je pregled arhitekture sistema na najvišem nivou i sumirane su glavne karakteristike sa stanovišta pogodnosti za korisnike.

## 4.1. Pregled arhitekture  {#4.1.-pregled-arhitekture}

Sistem je zamišljen na bazi dinamičkog Internet sajta postavljenog na Web serveru koji podržava Django i Ajax. Postoji i server na kome je baza podataka MySQL u kojoj se čuvaju podaci o akcijama, korisnicima (volonterima, organizatorima, sponzorima, administratorima), člancima, sponzorskim ponudama, prijavama volontera, kao i njihove šifre za pristup.  Web server, koristeći Django za back-end obradu i pristup bazi, generiše HTML kod za front-end, koji se potom prikazuje posetiocu aplikacije.

Sistem takođe integriše spoljne servise: Google Maps API za geolokaciju i pretragu akcija po lokaciji, Email API za automatizovano slanje obaveštenja korisnicima.

##    4.2. Pregled {#4.2.-pregled}

| Korist za korisnika | Karakteristika koja je obezbeđuje |
| ----- | ----- |
| Svi tipovi korisnika imaju brz pristup sajtu. | U bilo kom trenutku od strane korisnika je moguće pristupiti sajtu. |
| Jednostavno korišćenje sajta. | Nakon što je korisnik ulogovan, moći će vrlo intuitivno da koristi funkcionalnosti sajta koje su mu na osnovu njegove uloge i omogućene. |
| Omogućen pristup sa bilo kog računara povezanog na Internet. | Nikakva dodatna prilagođavanja sa klijentske strane nisu potrebna. Korisnički interfejs je zasnovan na HTML-u, Web pretraživaču i JavaScript-u. |
| Lako administriranje. | Administrator koristi jednostavnu formu za pristup bazi podataka. Dovoljno je da njegov računar bude povezan na Internet. |

## 4.3. Integracija sa eksternim servisima {#4.3.-integracija-sa-eksternim-servisima}

### 4.3.1. Google Maps API {#4.3.1.-google-maps-api}

Koristi se za prikaz lokacija volonterskih akcija na mapi, kako bi korisnici imali precizan uvid u lokaciju održavanja akcije. Omogućava pretragu akcija prema trenutnoj lokaciji korisnika ili prema lokaciji koju korisnik odabere, olakšavajući pronalaženje relevantnih volonterskih aktivnosti u željenom području. Takođe se koristi pri određivanju koje akcije će se preporučiti korisniku na osnovu lokacija prethodnih akcija u kojima je učestvovao.

### 4.3.2. Email API {#4.3.2.-email-api}

Koristi se za automatsko slanje obaveštenja korisnicima sistema, uključujući potvrde registracije, obaveštenja o prihvatanju ili odbijanju prijave na akciju, informacije za prijavljene volontere, kao i slanje preporuka korisnicima. Ovaj servis omogućava pravovremenu i pouzdanu komunikaciju sa korisnicima, smanjujući potrebu za manuelnim slanjem email-ova od strane organizatora ili administratora. Na taj način se olakšava upravljanje volonterskim aktivnostima i poboljšava korisničko iskustvo.

# 

# 5\. Funkcionalni zahtevi {#5.-funkcionalni-zahtevi}

U ovom odeljku definišu se osnovne funkcije koje sistem treba da obezbedi različitim kategorijama korisnika.

## 5.1. Registracija korisnika {#5.1.-registracija-korisnika}

Ukoliko korisnik nema svoj nalog, može ga kreirati unošenjem ličnih podataka i izborom tipa naloga (volonter, organizator ili sponzor). Podaci se upisuju u bazu podataka. Nalog sponzora i organizatora mora biti odobren od strane administratora pre korišćenja sistema.

## 5.2. Autorizacija korisnika {#5.2.-autorizacija-korisnika}

Svi registrovani korisnici se autorizuju unošenjem email adrese i lozinke. Podaci moraju da se poklope sa postojećim podacima u bazi podataka. Nakon potvrđene autorizacije, korisnici mogu da pristupe funkcionalnostima koje odgovaraju njihovoj ulozi.

## 5.3. Pregled i pretraga akcija {#5.3.-pregled-i-pretraga-akcija}

Svi korisnici sajta imaju mogućnost da pregledaju objavljene volonterske akcije, kao i da ih pretražuju prema različitim kriterijumima, poput naziva, lokacije, datuma ili tipa akcije. Za pretragu po lokaciji bi se koristio Google maps API.

## 5.4. Pregled i pretraga članaka {#5.4.-pregled-i-pretraga-članaka}

Svi korisnici sajta imaju mogućnost da pregledaju objavljene članke, kao i da ih pretražuju prema različitim kriterijumima, poput naziva članka ili naziva organizatora.

## 5.5. Kreiranje akcija {#5.5.-kreiranje-akcija}

Organizator ima mogućnost da kreira novu volontersku akciju unošenjem sledećih podataka: naziv akcije, opis, datum i vreme održavanja, lokacija, maksimalan broj volontera, kategorija akcije i kontakt informacije. Kreirana akcija mora biti odobrena od strane administratora pre nego što postane vidljiva na sajtu.

## 5.6. Prijava volontera na akciju {#5.6.-prijava-volontera-na-akciju}

Registrovani volonter može da se prijavi na bilo koju objavljenu akciju koja je otvorena za prijave. Organizator ima mogućnost da prihvati ili odbije prijavu volontera. Po prihvatanju prijave, volonter dobija obaveštenje putem email-a. Email se automatski šalje volonteru korišćenjem Email API-ja.

## 5.7. Dodavanje sponzora akciji {#5.7.-dodavanje-sponzora-akciji}

Sponzor može da pregleda objavljene akcije i pošalje ponudu o sponzorisanju odabrane akcije. Organizator prima ponudu i može je prihvatiti ili odbiti. Po prihvatanju, sponzor se prikazuje na stranici date akcije.

## 5.8. Slanje informacija prijavljenim volonterima {#5.8.-slanje-informacija-prijavljenim-volonterima}

Organizator može slati obaveštenja volonterima koji su prijavljeni na određenu akciju, uključujući izmene u rasporedu, dodatne informacije, podsetnike i važne napomene, kako bi svi učesnici bili pravovremeno informisani. Ova obaveštenja se automatski šalju putem Email API-ja, čime se olakšava komunikacija.

## 5.9. Slanje preporuka korisnicima {#5.9.-slanje-preporuka-korisnicima}

Korisnici mogu da se prijave da putem email-a dobijaju obaveštenja o akcijama koje bi mogle da im budu od interesa. Tada bi sistem automatski mogao da šalje prijavljenom korisniku preporuke za akcije na bazi prethodnih akcija na kojima je dati korisnik učestvovao. Kako bi preporuke bile što relevantnije i korisnicima olakšale pronalaženje, koristiće se Google Maps API za identifikaciju akcija koje se nalaze u blizini lokacija prethodnih akcija na kojima je korisnik učestvovao. Preporuke će se automatski slati pomoću Email API-ja.

## 5.10. Ažuriranje akcije {#5.10.-ažuriranje-akcije}

Organizator ima mogućnost da ažurira svoje objavljene akcije, tako što bi imao opciju dodavanja fotografija pre i posle akcije, menjanje datuma održavanja, otkazivanje akcije i drugih relevantnih izmena.

## 5.11. Kreiranje članaka o akcijama {#5.11.-kreiranje-članaka-o-akcijama}

Organizator ima mogućnost kreiranja članaka o realizovanim i predstojećim akcijama, koji mogu sadržati naslov, tekst i slike. Nakon što administrator odobri sadržaj, članci se objavljuju na posebnoj stranici sajta posvećenoj obaveštenjima o akcijama.

## 5.12. Komentarisanje članaka {#5.12.-komentarisanje-članaka}

Registrovani korisnici imaju mogućnost da ostave komentar na članku.

## 5.13. Upravljanje korisničkim nalozima {#5.13.-upravljanje-korisničkim-nalozima}

Administrator odobrava kreiranje naloga za sponzore i organizatore. Takođe, administrator može ukloniti naloge korisnika koji krše pravila korišćenja sajta.

## 5.14. Upravljanje akcijama i člancima {#5.14.-upravljanje-akcijama-i-člancima}

Administrator ima mogućnost pregleda svih objavljenih akcija i članaka, njihovog odobravanja i brisanja.

## 5.15. Praćenje učešća volontera {#5.15.-praćenje-učešća-volontera}

Volonter ima mogućnost da pregleda akcije na kojima je učestvovao i ukupan broj volonterskih sati (kao vrstu ličnih dostignuća), kao i akcije na koje je trenutno prijavljen.

## 5.16. Praćenje učešća sponzora {#5.16.-praćenje-učešća-sponzora}

Sponzor ima mogućnost da pregleda akcije na kojima je donirao i ukupnu vrednost sponzorskog doprinosa merena u evrima (EUR) bez obzira na formu u kojoj je doprinos realizovan, bilo da se radi o novčanim sredstvima, robi, uslugama ili drugim nenovčanim davanjima. 

# 

# 6\. Pretpostavke i ograničenja {#6.-pretpostavke-i-ograničenja}

Sistem treba isprojektovati tako da dodavanje novih akcija i članaka bude što lakše i maksimalno automatizovano. Pored toga, neophodno je održati konzistentnost u dizajnu sajta. Treba obezbediti sigurno čuvanje podataka vezanih za autorizaciju kako bi se izbegao neovlašćeni pristup i opstrukcija rada sajta. Za integraciju sa Google Maps API-jem neophodno je obezbediti odgovarajući API ključ. 

# 7\. Kvalitet {#7.-kvalitet}

Potrebno je izvršiti funkcionalno (black-box) testiranje svih funkcija sistema. Takođe, važno je testirati ekstremne situacije kao, na primer, preopterećenje sajta, istovremeno prijavljivanje velikog broja volontera na istu akciju, pokušaj neovlašćenog pristupa, i sl.

# 8\. Nefunkcionalni zahtevi {#8.-nefunkcionalni-zahtevi}

Sistem se sastoji iz serverske i korisničke komponente.

## 8.1. Sistemski zahtevi {#8.1.-sistemski-zahtevi}

Serverski deo treba da može da se izvršava na bilo kom Web serveru koji podržava Django. Potrebna je i baza podataka MySQL. Korisnički interfejs treba da bude raspoloživ za većinu poznatih internet pretraživača (Chrome, Firefox, Safari, Edge). Potrebno je obezbediti da prikaz strana po dizajnu bitno ne odstupa u zavisnosti od toga koji se pretraživač koristi.

## 8.2. Ostali zahtevi {#8.2.-ostali-zahtevi}

Sistem treba da pruži zadovoljavajuće performanse pri odzivu, kao i određenu vizuelnu dinamičnost strana. Sajt treba da bude responzivan i prilagođen za korišćenje na mobilnim uređajima.

# 

# 9\. Zahtevi za korisničkom dokumentacijom {#9.-zahtevi-za-korisničkom-dokumentacijom}

## 9.1. Uputstva za korišćenje sajta {#9.1.-uputstva-za-korišćenje-sajta}

Predviđeno je da korisnički interfejs bude jako intuitivan i jednostavan za korišćenje, pa ne bi bilo potrebe za detaljnim uputstvima za korišćenje.  Eventualna uputstva bi se mogla obezbediti korisnicima tipa Administrator, koja bi sadržala detalje o kriterijumima odobravanja naloga organizacijama i sponzorima. 

## 9.2. Označavanje {#9.2.-označavanje}

Zaglavlje svih stranica trebalo bi da sadrži logo i naziv AkcijaRS. Potrebno je da svaka akcija bude označena od strane kog organizatora je kreirana. Svaki članak treba da sadrži informaciju o autoru.

# 10\. Plan i prioriteti {#10.-plan-i-prioriteti}

Razvoj aplikacije treba da se odvija iterativno. Prva verzija trebalo bi da obuhvati minimalno sledeće funkcionalnosti:

* Registracija i prijava na sistem  
* Kreiranje novih volonterskih akcija  
* Prijava volontera na akcije  
* Pregled akcija od strane gostiju i registrovanih korisnika  
* Osnovne administratorske funkcije

Implementacija ovih funkcionalnosti se smatra esencijalnom za razvoj sistema. Ostale navedene u ovom dokumentu predstavljaju korisna proširenja osnovnog sistema koja će biti dodata.

[image1]: <data:image/png;base64,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>