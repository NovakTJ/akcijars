**SI3PSI – Tim VolonTech**

**SPECIFIKACIJA BAZE PODATAKA 
za projekat AkcijaRS**

**Verzija V 1.0**

**Datum: 16. maj 2026.**

**Istorija revizija**

| Verzija | Datum | Autor | Opis |
| --- | --- | --- | --- |
| 1.0 | 16.05.2026. | Maša Nikolić, Milica Milošević | Inicijalna verzija |
|   |   |   |   |
|   |   |   |   |

**Sadržaj**

# 1.	Uvod

## 1.1	Namena

Baza podataka za projekat iz predmeta Principi softverskog inženjerstva predstavlja fleksibilan i pouzdan način čuvanja podataka i pristupa istim od strane veb servera radi generisanja veb strana.

U dokumentu je dat model podataka – dijagram sa IE (Information Engineering) notacijom, šema relacione baze podataka, kao i opis svih tabela u bazi podataka.

Ovaj dokument služi kao osnova za razvoj detaljne projektne specifikacije posmatranog podsistema, implementaciju i testiranje. Svi podaci koje je potrebno čuvati su dobijeni u fazi analize korisničkih zahteva.

## 1.2	Ciljne grupe

Dokument je namenjen vođi (tim lideru) projekta i članovima razvojnog tima.

Tim lideru ovaj dokument služi za planiranje razvojnih aktivnosti i specifikaciju imena tabela i imena polja u bazi, kako bi nezavisne celine, implementirane od strane različitih delova razvojnog tima, na kraju rada bile uspešno integrisane.

Razvojnom timu dokument služi kao osnova za dizajn i implementaciju.

## 1.3	Organizacija dokumenta

Ostatak dokumenta organizovan je u sledeća poglavlja:

- **Model podataka **- model podataka u bazi i šema baze;

- **Tabele **- spisak tabela;

## 1.4	Rečnik pojmova i skraćenica

Po potrebi ovde navesti objašnjenja pojmova i skraćenica koji su upotrebljavane u ovom dokumentu i ovoj fazi projekta, a mogli bi, kod nekih članova tima, da izazovu nedoumice. Na primer:

- IE – Information Engineering, notacija za modelovanje podataka;

## 1.5	Otvorena pitanja

U ovoj sekciji navode se otvorena pitanja. Ona se numerišu i pozicioniraju u vremenu radi lakšeg referisanja. Kada se pitanje reši, potrebno je to uneti u odgovarajuću rubriku.

| Broj | Datum | Problem | Rešenje |
| --- | --- | --- | --- |
|   |   |   |   |
|   |   |   |   |
|   |   |   |   |
|   |   |   |   |

# 2.   Model podataka

## 2.1	Dijagram IE notacije

## 2.2	Šema relacione baze podataka

Korisnik (IdKor, KorisnickoIme, Lozinka, Ime, Prezime, Email, DatumRegistracije)

Volonter (IdKor, UkupnoSati, PrimaPreporuke)

Organizator (IdKor, BrTelefona, NazivOrganizacije, Status)

Sponzor (IdKor, BrTelefona, NazivOrganizacije, Status)

Administrator (IdKor)

KategorijaAkcije (IdKat, Naziv)

Akcija (IdAkc, IdKor, IdKat, Naziv, Opis, Datum, Vreme, Lokacija, MaxBrVolontera, KontaktEmail, KontaktTelefon, Status, DatumKreiranja, Slika)

PrijavaVolontera (IdKor, IdAkc, DatumPrijave, Status, BrSati)

SponzorskaPonuda (IdPon, IdKor, IdAkc, Vrednost, Opis, Status, DatumSlanja)

Clanak (IdCla, IdKor, Naslov, Tekst, DatumKreiranja, Status)

SlikaClanka (IdSli, IdCla, Putanja)

FotografijaAkcije (IdFot, IdAkc, Putanja)

Komentar (IdKom, IdKor, IdCla, Tekst, DatumKomentara)

Dostignuce (IdDost, Naziv, Opis, Ikonica)

VolonterDostignuce (IdKor, IdDost, DatumOstvarivanja)

# 3. Tabele

## 3.1	Korisnik

Sadrži podatke o korisniku sistema. IdKor se automatski generiše u bazi (uz pomoć autoincrement-a). KorisnickoIme i Email imaju specifikaciju UNIQUE.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | No |
| KorisnickoIme | varchar(50) | No | No |
| Lozinka | varchar(50) | No | No |
| Ime | varchar(50) | No | No |
| Prezime | varchar(50) | No | No |
| Email | varchar(50) | No | No |
| DatumRegistracije | date | No | No |

## 3.2	Volonter

Sadrži podatke o volonteru.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | Yes |
| UkupnoSati | integer | No | No |
| PrimaPreporuke | bool | No | No |

## 3.3	Organizator

Sadrži podatke o organizatoru.  Status opisuje da li je korisnički nalog na čekanju, odobren ili odbijen.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | Yes |
| BrTelefona | varchar(20) | No | No |
| NazivOrganizacije | varchar(100) | No | No |
| Status | varchar(20) | No | No |

## Sponzor

Sadrži podatke o sponzoru. Status opisuje da li je korisnički nalog na čekanju, odobren ili odbijen.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | Yes |
| BrTelefona | varchar(20) | No | No |
| NazivOrganizacije | varchar(100) | No | No |
| Status | varchar(20) | No | No |

## Administrator

Sadrži podatke o administratoru.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | Yes |

## KategorijaAkcije

Sadrži podatke o tome koje kategorije akcija postoje. IdKat se automatski generiše u bazi (uz pomoć autoincrement-a).

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKat | integer | Yes | No |
| Naziv | varchar(50) | No | No |

## 3.7	Akcija

Sadrži podatke o akciji. Status opisuje da li je akcija na čekanju, odobrena, odbijena, popunjena i slično. IdKor predstavlja identifikacioni broj organizatora koji je napravio akciju. IdAkc se automatski generiše u bazi (uz pomoć autoincrement-a).

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdAkc | integer | Yes | No |
| IdKor | integer | No | Yes |
| IdKat | integer | No | Yes |
| Naziv | varchar(100) | No | No |
| Opis | varchar(1024) | No | No |
| Datum | date | No | No |
| Vreme | time | No | No |
| Lokacija | varchar(50) | No | No |
| MaxBrVolontera | integer | No | No |
| KontaktEmail | varchar(50) | No | No |
| KontaktTelefon | varchar(20) | No | No |
| Status | varchar(20) | No | No |
| DatumKreiranja | date | No | No |
| Slika | longblob | No | No |

## 3.8	PrijavaVolontera

Sadrži podatke o prijavi volontera na akcije. IdKor predstavlja identifikacioni broj volontera koji se prijavio na akciju. IdKor i IdAkc čine primaran ključ ove tabele. Status opisuje stanje prijave volontera, da li je prihvaćen, odbijen i slično.

| Name | Datatype | Is PK | Is FK |
| --- | --- | --- | --- |
| IdKor | integer | Yes | Yes |
| IdAkc | integer | Yes | Yes |
| DatumPrijave | date | No | No |
| Status | varchar(20) | No | No |
| BrSati | integer | No | No |

## 3.9	SponzorskaPonuda

Sadrži podatke o ponudama sponzora za akcije. Status opisuje da li je ponuda na čekanju, prihvaćena ili odbijena. IdKor predstavlja identifikacioni broj sponzora koji šalje ponudu. IdPon se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.10	Clanak

Sadrži podatke o članku. IdKor predstavlja identifikacioni broj organizatora koji je napisao članak. Status govori o tome da li je članak na čekanju, objavljen ili odbijen. IdKor se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.11	SlikaClanka

Sadrži podatke o slici koja se nalazi na članku. IdSli se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.12	FotografijaAkcije

Sadrži podatke o fotografiji koja se nalazi na stranici akcija. IdFot se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.13	Komentar

Sadrži podatke o komentaru koji može da se ostavi na članku. IdKom se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.14	Dostignuce

Sadrži podatke o dostignucu koje moze da se ostvari. IdDost se automatski generiše u bazi (uz pomoć autoincrement-a).

## 3.15	VolonterDostignuce

Sadrži podatke o dostignućima korisnika.
