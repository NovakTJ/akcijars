# AkcijaRS

A web application for organizing volunteer campaigns, developed as part of the
**SI3PSI – Principles of Software Engineering** course at the School of Electrical
Engineering, University of Belgrade (academic year 2025/2026).

The application connects volunteers, organizers and sponsors: it supports browsing and
searching campaigns and articles, volunteer sign-ups, sponsorship offers, email
notifications and recommendations, as well as account and content administration.

**Team VolonTech:** Milica Milošević, Maša Nikolić, Novak Stijepić, Stefan Grujičić

> Project documentation is written in Serbian.

## Project phases

| Phase | Contents | Deadline |
| :--- | :--- | :--- |
| [1. Project specification](faza%201) | Problem description, user categories and functional requirements | Apr 6, 2026 |
| [2. Use case scenarios and prototype](faza%202) | 18 use case scenarios (`ssu/`) and an HTML prototype (`prototip/`) | Apr 16, 2026 |
| [3. Formal inspection](faza%203) | Inspector logs and formal inspection reports | May 9 / May 14, 2026 |
| [4. Database modeling](faza%204) | Database specification, SQL script and ER diagram (MySQL Workbench) | May 21, 2026 |
| [5. Web application implementation](faza%205) | Django application (`akcijars/`) and a list of tools used | Jul 12, 2026 |
| [6. Web application modeling](faza%206) | UML use case, class and sequence diagrams (StarUML) | Jul 12, 2026 |
| [7. Web application testing](faza%207) | Test plans and reports (unit and UI tests) | Jul 12, 2026 |

## Technologies

- **Backend:** Python, Django
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Modeling:** MySQL Workbench, StarUML

## Running the application

Detailed instructions for installation, database setup and running the app are in
[faza 5/akcijars/README.md](faza%205/akcijars/README.md) (in Serbian).

In short: create a virtual environment and install the packages from `requirements.txt`,
configure `.env` and the MySQL database (by importing `baza_akcijars.sql` or running
`migrate`), then start the server with `python manage.py runserver`.
