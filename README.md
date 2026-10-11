# AkcijaRS

Veb aplikacija za organizaciju volonterskih akcija, razvijena u okviru predmeta
**SI3PSI – Principi softverskog inženjerstva** na Elektrotehničkom fakultetu u Beogradu
(školska 2025/2026).

Aplikacija povezuje volontere, organizatore i sponzore: omogućava pregled i pretragu
akcija i članaka, prijavu volontera na akcije, sponzorske ponude, obaveštenja i
preporuke putem email-a, kao i administraciju naloga i sadržaja.

**Tim VolonTech:** Milica Milošević, Maša Nikolić, Novak Stijepić, Stefan Grujičić

## Faze projekta

| Faza | Sadržaj | Rok |
| :--- | :--- | :--- |
| [1. Projektni zadatak](faza%201) | Opis problema, kategorije korisnika i funkcionalni zahtevi | 6.4.2026. |
| [2. SSU dokumenti i prototip](faza%202) | 18 scenarija slučajeva upotrebe (`ssu/`) i HTML prototip (`prototip/`) | 16.4.2026. |
| [3. Formalna inspekcija](faza%203) | Logovi inspektora i izveštaji formalne inspekcije | 9.5. / 14.5.2026. |
| [4. Modelovanje baze podataka](faza%204) | Specifikacija baze, SQL skripta i ER dijagram (MySQL Workbench) | 21.5.2026. |
| [5. Implementacija veb aplikacije](faza%205) | Django aplikacija (`akcijars/`) i spisak korišćenih alata | 12.7.2026. |
| [6. Modelovanje veb aplikacije](faza%206) | UML dijagrami slučajeva upotrebe, klasa i sekvence (StarUML) | 12.7.2026. |
| [7. Testiranje veb aplikacije](faza%207) | Planovi i izveštaji testiranja (jedinični i UI testovi) | 12.7.2026. |

## Tehnologije

- **Backend:** Python, Django
- **Baza podataka:** MySQL
- **Frontend:** HTML, CSS, JavaScript (Django šabloni)
- **Modelovanje:** MySQL Workbench, StarUML

## Pokretanje aplikacije

Detaljno uputstvo za instalaciju, podešavanje baze i pokretanje nalazi se u
[faza 5/akcijars/README.md](faza%205/akcijars/README.md).

Ukratko: napraviti virtuelno okruženje i instalirati pakete iz `requirements.txt`,
podesiti `.env` i MySQL bazu (uvozom `baza_akcijars.sql` ili sa `migrate`), pa pokrenuti
`python manage.py runserver`.
