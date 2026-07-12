# Autor: Milica Milošević 0357/2023
"""
Selenium WebDriver UI testovi za SSU 4 — Pregled i pretraga članaka
(implementirala Maša Nikolić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main.tests._helpers import organizator, clanak
from ._baza import SeleniumBazniTest


class ListaClanakaUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org = organizator(f'office.zelenibeograd.{s}@gmail.com', naziv='Zeleni Beograd')
        self.c1 = clanak(self.org, 'Čišćenje parka')
        self.c2 = clanak(self.org, 'Sadnja drveća')

    def test_lista_prikazuje_objavljene_clanke(self):
        """Na strani članaka su vidljivi objavljeni članci."""
        self.idi('/clanci/')
        telo = self.cekaj('#clanci-container').text
        self.assertIn('Čišćenje parka', telo)
        self.assertIn('Sadnja drveća', telo)

    def test_pretraga_po_naslovu_2_2_2(self):
        """2.2.2 — unos upita u polje i pretraga prikazuje samo odgovarajuće članke."""
        self.idi('/clanci/')
        polje = self.cekaj('#filter-form-clanci input[name="q"]')
        polje.send_keys('Sadnja')
        polje.send_keys(Keys.ENTER)
        self.cekaj_tekst('#clanci-container', 'Sadnja drveća')
        self.assertNotIn('Čišćenje parka', self.tekst('#clanci-container'))

    def test_klik_na_clanak_otvara_detalj_2_2_1(self):
        """2.2.1 — klik na članak otvara pun tekst."""
        self.idi('/clanci/')
        self.cekaj('#clanci-container')
        link = self.br.find_element(By.PARTIAL_LINK_TEXT, 'Sadnja drveća')
        self.br.execute_script('arguments[0].scrollIntoView({block: "center"});', link)
        link.click()
        self.cekaj_tekst('body', 'Tekst test članka.')
