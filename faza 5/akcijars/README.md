# AkcijaRS

Veb aplikacija za organizaciju volonterskih akcija (Django + MySQL). Omogućava
pregled i pretragu akcija i članaka, prijavu volontera, sponzorske ponude,
upravljanje akcijama, obaveštenja i preporuke putem email-a, kao i administraciju
naloga i sadržaja.

---

## Preduslovi

- **Python 3.10+**
- **MySQL 8+** (server pokrenut)
- Git

---

## 1. Instalacija

### 1a. Kloniranje i virtuelno okruženje

**Windows (PowerShell):**
```powershell
cd "faza 5\akcijars"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
cd "faza 5/akcijars"
python3 -m venv venv
source venv/bin/activate
```

### 1b. Instalacija paketa
```
pip install -r requirements.txt
```

> **macOS napomena:** ako `mysqlclient` ne prođe (greška „mysql_config not found"),
> instaliraj MySQL klijent biblioteke pa probaj ponovo:
> ```bash
> brew install mysql pkg-config
> pip install -r requirements.txt
> ```
> Na Apple Silicon-u po potrebi: `export PKG_CONFIG_PATH="$(brew --prefix mysql)/lib/pkgconfig"`

---

## 2. Konfiguracija (`.env`)

Napravi `.env` fajl (u `faza 5/akcijars/`) prema `.env.example` i popuni svoje
MySQL podatke, npr:
```
DB_NAME=akcijars
DB_USER=root
DB_PASSWORD=tvoja_lozinka
DB_HOST=127.0.0.1
DB_PORT=3306
```
`GOOGLE_MAPS_API_KEY` i `EMAIL_*` su **opcioni** (vidi sekciju 6). Bez njih
aplikacija radi — mape se ne prikazuju, a email se ispisuje u terminal.

> `.env` se **ne commit-uje** (u `.gitignore` je) — svako drži svoj lokalno.

---

## 3. Baza podataka

Napravi praznu bazu (u MySQL-u):
```sql
CREATE DATABASE akcijars CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Zatim biraš **jednu** od dve opcije:

### Opcija A — Uvoz demo podataka (preporučeno)
Dobijaš tabele **i sve demo podatke** (akcije, korisnike, članke, slike…):

**Windows:**
```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p akcijars < baza_akcijars.sql
```
**macOS / Linux:**
```bash
mysql -u root -p akcijars < baza_akcijars.sql
```
> Uz uvoz dump-a **ne treba** `migrate` (dump već nosi i stanje migracija).

### Opcija B — Prazna baza
Ako želiš čist start bez podataka:
```
python manage.py migrate
```

> Slike (`media/` folder) dolaze sa repozitorijumom — ne treba ništa dodatno.

---

## 4. Pokretanje

```
python manage.py runserver
```
Aplikacija je na **http://127.0.0.1:8000/**

---

## 5. Test nalozi

Svi nalozi imaju istu lozinku: **`Volonter2024!`**

| Uloga | Email | Napomena |
| :---- | :---- | :---- |
| **Admin** | `admin@akcijars.rs` | Django admin (`/admin/`) + admin panel (`/admin-panel/`) |
| Volonter | `jovana.petrovic93@gmail.com` | prijave, sati, prima preporuke |
| Volonter | `marko.nikolic@gmail.com` | volonterski sati (završena akcija) |
| Volonter | `ana.jovanovic@yahoo.com` | prijave + sati |
| Volonter | `stefan.ilic@outlook.com` | prima preporuke |
| Volonter | `milica.djordjevic7@gmail.com` | sati |
| Volonter | `nikola.markovic@gmail.com` | odbijena / prijava na čekanju |
| Organizator | `office.zelenibeograd@gmail.com` | Zeleni Beograd (odobren) |
| Organizator | `crvenikrst.bg@gmail.com` | Crveni krst Beograd (odobren) |
| Organizator | `vcns.info@gmail.com` | Volonterski centar NS (odobren) |
| Organizator | `ruka.prijateljstva@gmail.com` | **na čekanju** — za demo admin odobravanja |
| Sponzor | `sponzorstva.delta@gmail.com` | Delta Holding (odobren) |
| Sponzor | `bojan.stojanovic.nis@gmail.com` | NIS a.d. (odobren) |

> Nalozi organizatora/sponzora moraju biti **odobreni od strane admina** pre
> nego što mogu da se uloguju (volonteri ne čekaju odobrenje).

---

## 6. Opcione integracije

### Google Maps (mape i pretraga po lokaciji)
Dodaj u `.env` (ključ sa uključenim **Maps JavaScript API** i **Places API** +
billing na Google Cloud projektu):
```
GOOGLE_MAPS_API_KEY=tvoj_kljuc
```
Bez ključa aplikacija radi, samo se umesto mape prikazuje tekst lokacije.

### Email (pravo slanje)
Podrazumevano se koristi **konzolni backend** (mejlovi se ispisuju u terminal).
Za pravo slanje preko Gmail-a, dodaj u `.env`:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=nalog@gmail.com
EMAIL_HOST_PASSWORD=app_lozinka_16_karaktera
DEFAULT_FROM_EMAIL=AkcijaRS <nalog@gmail.com>
```

---

## 7. Dodatne komande

- **Slanje preporuka volonterima** (SSU 9) — jednokratno:
  ```
  python manage.py posalji_preporuke
  ```
- **Automatski nedeljni planer preporuka** (šalje ponedeljkom u 08:00):
  ```
  python manage.py run_scheduler
  ```
- **Dokumentacija koda** (docstring-ovi kroz admindocs): uloguj se kao admin i
  otvori **http://127.0.0.1:8000/admin/doc/**

---

## 8. Napomena o restartu

Izmene u `.env` (npr. dodavanje Maps ključa ili email podataka) primenjuju se
tek nakon **restarta servera** (`Ctrlgit +C`, pa ponovo `runserver`).
