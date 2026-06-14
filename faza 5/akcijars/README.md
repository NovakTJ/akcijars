# AkcijaRS

## Pokretanje projekta

### Preduslovi
- Python 3.10+
- MySQL

### Instalacija

1. Kloniraj repozitorijum
2. Kreiraj i aktiviraj virtuelno okruženje:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instaliraj pakete:
   ```
   pip install -r requirements.txt
   ```
4. Kreiraj bazu u MySQL Workbench:
   ```sql
   CREATE DATABASE akcijars CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. Kreiraj `.env` fajl prema `.env.example` i popuni svoje podatke
6. Pokreni migracije:
   ```
   python manage.py migrate
   ```
7. Pokreni server:
   ```
   python manage.py runserver
   ```
