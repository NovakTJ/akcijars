# Autor: Novak Stijepic 0124/2023
"""
Podešavanja za brže pokretanje testova (faza 7 — testiranje).

Nasleđuje sva projektna podešavanja iz ``settings`` i menja samo ono što
ubrzava test suite bez uticaja na produkciju:

- ``PASSWORD_HASHERS`` — koristi se brzi MD5 heš umesto podrazumevanog
  PBKDF2 (stotine hiljada iteracija). Testovi kreiraju mnogo korisnika
  (``create_user``), pa je heširanje lozinki glavni uzrok sporosti.
- ``EMAIL_BACKEND`` — u memoriji (``locmem``), da testovi koji proveravaju
  ``mail.outbox`` rade pouzdano i bez ispisa u konzolu.

Pokretanje:

    python manage.py test main.tests --settings=akcijars.test_settings --keepdb
"""
from .settings import *  # noqa: F401,F403

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
