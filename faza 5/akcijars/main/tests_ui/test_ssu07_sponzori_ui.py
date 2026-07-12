# Autor: Milica Milošević 0357/2023
"""
Selenium WebDriver UI testovi za SSU 7 — Dodavanje sponzora akciji
(implementirao Stefan Grujičić — ukrštanje).
"""
from uuid import uuid4

from django.test import override_settings
from selenium.webdriver.common.by import By

from main.models import Akcija
from main.tests._helpers import organizator, sponzor, akcija
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')
class SponzorskaPonudaUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.spon_email = f'sponzorstva.delta.{s}@gmail.com'
        self.org = organizator(f'office.zelenibeograd.{s}@gmail.com')
        self.akc = akcija(self.org, 'Akcija za sponzora', Akcija.Status.AKTIVNA)
        self.spon = sponzor(self.spon_email, naziv='Delta Holding')

    def test_uspesno_slanje_ponude_2_2_1(self):
        """2.2.1 — sponzor popuni formu i pošalje ponudu; prikazuje se poruka o čekanju."""
        self.login(self.spon_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.cekaj('#form-ponuda input[name="vrednost"]').send_keys('500')
        self.br.find_element(By.CSS_SELECTOR, '#form-ponuda textarea[name="opis"]').send_keys('Oprema i sredstva.')
        self.klik('#btn-posalji-ponudu')
        self.cekaj_tekst('#sponzor-ponuda-container', 'čeka odgovor organizatora')

    def test_nepotpuna_ponuda_prikazuje_gresku_2_2_2(self):
        """2.2.2 — ponuda bez opisa prikazuje poruku o grešci."""
        self.login(self.spon_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.cekaj('#form-ponuda input[name="vrednost"]').send_keys('100')
        # polje „opis" ostaje prazno
        self.klik('#btn-posalji-ponudu')
        self.cekaj_tekst('#sponzor-ponuda-container', 'Proverite unete podatke')
