#!/usr/bin/env python
# Autor: Milica Milošević 0357/2023
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Faza 7 — testovi podrazumevano koriste `akcijars.test_settings` (brzi MD5
    # heš lozinki umesto sporog PBKDF2, email u memoriji). Aktivira se samo za
    # `manage.py test` i samo ako korisnik nije sam prosledio `--settings`.
    if len(sys.argv) > 1 and sys.argv[1] == 'test' and not any(
        a == '--settings' or a.startswith('--settings=') for a in sys.argv[2:]
    ):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akcijars.test_settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akcijars.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
