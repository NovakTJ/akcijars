# Autor: Stefan Grujičić 0030/2023
"""
Selenium WebDriver UI testovi za SSU 2 — Autorizacija (prijava/odjava)
(implementirao Novak Stijepić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By

from main.tests._helpers import volonter
from ._baza import SeleniumBazniTest


class PrijavaOdjavaUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.vol_email = f'jovana.petrovic.{s}@gmail.com'
        volonter(self.vol_email)

    def test_uspesna_prijava_2_2_1(self):
        """2.2.1 — uspešna prijava vodi na ličnu (volontersku) stranicu."""
        self.login(self.vol_email)
        self.assertIn('/volonter-panel/', self.br.current_url)

    def test_neispravna_lozinka_prikazuje_gresku_2_2_3(self):
        """2.2.3 — pogrešna lozinka prikazuje propisanu poruku o grešci."""
        self.idi('/prijava/')
        self.br.find_element(By.NAME, 'email').send_keys(self.vol_email)
        self.br.find_element(By.NAME, 'lozinka').send_keys('PogresnaLoz1!')
        self.klik('#login-form button[type="submit"]')
        self.cekaj_tekst('body', 'Email adresa ili lozinka nisu ispravni.')

    def test_odjava_2_2_5(self):
        """2.2.5 — odjava vraća na početnu i ponovo prikazuje link „Prijavi se"."""
        self.login(self.vol_email)
        self.br.find_element(By.LINK_TEXT, 'Odjavi se').click()
        self.cekaj('body')
        self.assertTrue(self.br.find_elements(By.LINK_TEXT, 'Prijavi se'))
