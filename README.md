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

| Phase | Contents |
| :--- | :--- |
| [1. Project specification](faza%201) | Problem description, user categories and functional requirements |
| [2. Use case scenarios and prototype](faza%202) | 18 use case scenarios (`ssu/`) and an HTML prototype (`prototip/`) |
| [3. Formal inspection](faza%203) | Inspector logs and formal inspection reports |
| [4. Database modeling](faza%204) | Database specification, SQL script and ER diagram (MySQL Workbench) |
| [5. Web application implementation](faza%205) | Django application (`akcijars/`) and a list of tools used |
| [6. Web application modeling](faza%206) | UML use case, class and sequence diagrams (StarUML) |
| [7. Web application testing](faza%207) | Test plans and reports (unit and UI tests) |

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
