# Autor: Milica Milošević 0357/2023
"""
Slanje email preporuka akcija volonterima (SSU 9 / FZ 5.9).

Predviđeno za periodično pokretanje (npr. Windows Task Scheduler / cron):

    python manage.py posalji_preporuke
    python manage.py posalji_preporuke --radius 50 --limit 3

Obrađuju se samo volonteri koji su aktivirali preporuke (``prima_preporuke``).
Ako za volontera nema odgovarajućih akcija, email se ne šalje (SSU 9, 2.2.4).
"""
from django.core.management.base import BaseCommand

from main.emails import posalji_preporuke
from main.models import VolonterProfil
from main.preporuke import generisi_preporuke


class Command(BaseCommand):
    help = 'Šalje email preporuke akcija volonterima koji su ih aktivirali (SSU 9).'

    def add_arguments(self, parser):
        parser.add_argument('--radius', type=int, default=25,
                            help='Radijus pretrage u km (podrazumevano 25).')
        parser.add_argument('--limit', type=int, default=5,
                            help='Maksimalan broj akcija po volonteru (podrazumevano 5).')

    def handle(self, *args, **options):
        radius = options['radius']
        limit = options['limit']

        volonteri = (
            VolonterProfil.objects
            .filter(prima_preporuke=True)
            .select_related('korisnik')
        )

        poslato = 0
        for volonter in volonteri:
            akcije = generisi_preporuke(volonter, max_km=radius, limit=limit)
            if akcije:
                posalji_preporuke(volonter, akcije)
                poslato += 1
                self.stdout.write(f'  → {volonter.korisnik.email}: {len(akcije)} akcija')

        self.stdout.write(self.style.SUCCESS(
            f'Gotovo. Preporuke poslate za {poslato} volontera '
            f'(od {volonteri.count()} sa aktiviranim preporukama).'
        ))
