# Autor: Stefan Grujičić 0030/2023
"""
Selenium WebDriver UI testovi za SSU 10 — Ažuriranje i otkazivanje akcije
(implementirao Novak Stijepić — ukrštanje).
"""
from uuid import uuid4

from django.test import override_settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from main.models import Akcija
from main.tests._helpers import organizator, akcija
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')  # bez učitavanja Google Maps u testu
class AzuriranjeAkcijeUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'office.zelenibeograd.{s}@gmail.com'
        self.org = organizator(self.org_email)
        self.akc = akcija(self.org, 'Originalna akcija UI', Akcija.Status.AKTIVNA, max_vol=5)

    def test_uspesno_azuriranje_2_2_1(self):
        """2.2.1 — izmena naziva akcije u tabu „Izmeni akciju" se čuva."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-izmeni')
        polje = self.cekaj('#izmeni-forma [name="naziv"]')
        polje.clear()
        polje.send_keys('Izmenjen naziv akcije')
        self.klik('#btn-sacuvaj-izmene')
        self.cekaj_tekst('#org-izmeni', 'Izmene su uspešno sačuvane.')
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.naziv, 'Izmenjen naziv akcije')

    def test_otkazivanje_akcije_2_2_9(self):
        """2.2.9 — otkazivanje akcije (uz potvrdu) menja status u „Otkazana"."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-izmeni')
        self.klik('#btn-otkazi-akciju')
        WebDriverWait(self.br, 10).until(EC.alert_is_present())
        self.br.switch_to.alert.accept()
        # Čekamo bedž statusa (`.badge-error` ↔ „Otkazana"), a ne bilo koje
        # pojavljivanje reči „Otkazana" — statičko upozorenje pored dugmeta
        # za otkazivanje već sadrži tu reč i pre stvarnog otkazivanja, pa bi
        # čekanje na golo pojavljivanje teksta prošlo pre završetka Ajax poziva.
        self.cekaj_tekst('.badge-error', 'Otkazana')
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.status, Akcija.Status.OTKAZANA)
