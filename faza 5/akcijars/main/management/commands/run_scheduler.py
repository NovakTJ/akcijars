# Autor: Milica Milošević 0357/2023
"""
Planer koji periodično (jednom nedeljno) šalje email preporuke akcija (SSU 9).

Pokreće se jednom i ostaje aktivan — APScheduler u pozadini okida komandu
``posalji_preporuke`` po rasporedu (podrazumevano: svakog ponedeljka u 08:00).

    python manage.py run_scheduler
    python manage.py run_scheduler --odmah     # pošalji odmah pri pokretanju (test)

Prekid: Ctrl+C. Napomena: proces mora da ostane pokrenut da bi se posao okidao.
Na serveru se obično umesto ovoga koristi sistemski cron / Task Scheduler.
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Pokreće planer za nedeljno slanje preporuka akcija (SSU 9).'

    def add_arguments(self, parser):
        parser.add_argument('--odmah', action='store_true',
                            help='Pošalji preporuke odmah pri pokretanju (za test).')

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        def posao():
            self.stdout.write(f'[{timezone.localtime():%Y-%m-%d %H:%M}] Slanje preporuka...')
            call_command('posalji_preporuke')

        # Svakog ponedeljka u 08:00 (jednom nedeljno).
        scheduler.add_job(
            posao,
            CronTrigger(day_of_week='mon', hour=8, minute=0),
            id='nedeljne_preporuke',
            replace_existing=True,
        )

        if options['odmah']:
            posao()

        self.stdout.write(self.style.SUCCESS(
            'Planer pokrenut — preporuke se šalju svakog ponedeljka u 08:00. '
            'Prekid: Ctrl+C.'
        ))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            self.stdout.write('Planer zaustavljen.')
