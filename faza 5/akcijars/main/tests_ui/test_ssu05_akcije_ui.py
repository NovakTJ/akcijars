# Autor: Stefan Grujičić 0030/2023
"""
Selenium WebDriver UI testovi za SSU 5 — Kreiranje akcije
(implementirao Novak Stijepić — ukrštanje).
"""
import datetime
from uuid import uuid4

from django.test import override_settings
from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from main.models import Akcija
from main.tests._helpers import organizator, kat_akcije
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')  # bez učitavanja Google Maps u testu
class KreirajAkcijuUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'office.zelenibeograd.{s}@gmail.com'
        self.org = organizator(self.org_email)
        self.kat = kat_akcije(f'Ekologija {s}')

    def _popuni_datum_vreme(self):
        datum = (timezone.localdate() + datetime.timedelta(days=10)).isoformat()
        self.br.execute_script(
            "document.querySelector('[name=datum]').value = arguments[0];"
            "document.querySelector('[name=vreme]').value = '09:00';",
            datum,
        )

    def test_uspesno_kreiranje_2_2_1(self):
        """2.2.1 — popunjena forma se čuva; akcija se pojavljuje na „Moje akcije"."""
        self.login(self.org_email)
        self.idi('/akcije/kreiraj/')
        self.br.find_element(By.NAME, 'naziv').send_keys('Čišćenje parka u Zvezdari')
        self.br.find_element(By.NAME, 'opis').send_keys('Čistimo park i sadimo drveće.')
        self._popuni_datum_vreme()
        self.br.find_element(By.NAME, 'lokacija').send_keys('Ada Ciganlija, Beograd')
        Select(self.br.find_element(By.NAME, 'kategorija')).select_by_value(str(self.kat.pk))
        self.br.find_element(By.NAME, 'max_br_volontera').send_keys('20')
        self.br.find_element(By.NAME, 'kontakt_email').send_keys('kontakt@zeleni.rs')
        self.br.find_element(By.NAME, 'kontakt_telefon').send_keys('060123456')
        self.klik('button[type="submit"]')
        self.cekaj_tekst('body', 'Čišćenje parka u Zvezdari')
        self.assertTrue(Akcija.objects.filter(naziv='Čišćenje parka u Zvezdari').exists())

    def test_prazna_obavezna_polja_prikazuje_gresku_2_2_2(self):
        """2.2.2 — slanje prazne forme prikazuje propisanu poruku o grešci."""
        self.login(self.org_email)
        self.idi('/akcije/kreiraj/')
        self.klik('button[type="submit"]')
        self.cekaj_tekst('body', 'Nisu uneta sva obavezna polja.')
        self.assertEqual(Akcija.objects.count(), 0)

    def test_odustajanje_ne_cuva_2_2_7(self):
        """2.2.7 — klik na „Odustani" vraća na početnu bez čuvanja akcije."""
        self.login(self.org_email)
        self.idi('/akcije/kreiraj/')
        self.klik('a.btn-ghost[href="/"]')
        self.assertEqual(Akcija.objects.count(), 0)
