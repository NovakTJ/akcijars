# Autor: Stefan Grujičić 0030/2023
"""
Selenium WebDriver UI testovi za SSU 11 — Kreiranje članka
(implementirao Novak Stijepić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from main.models import Clanak
from main.tests._helpers import organizator, kat_clanka
from ._baza import SeleniumBazniTest


class KreirajClanakUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'office.zelenibeograd.{s}@gmail.com'
        self.org = organizator(self.org_email)
        self.kat = kat_clanka(f'Ekologija {s}')

    def test_uspesno_kreiranje_2_2_1(self):
        """2.2.1 — popunjena forma se čuva; članak se pojavljuje u „Moji članci"."""
        self.login(self.org_email)
        self.idi('/organizator-panel/')
        self.klik('[data-tab="clanci"]')
        self.klik('#btn-otvori-formu-clanka')
        self.cekaj('#clanak-forma [name="naslov"]').send_keys('Uspešno završena akcija čišćenja')
        Select(self.br.find_element(By.CSS_SELECTOR, '#clanak-forma select[name="kategorija"]')) \
            .select_by_value(str(self.kat.pk))
        self.br.find_element(By.CSS_SELECTOR, '#clanak-forma [name="tekst"]') \
            .send_keys('Detaljan opis akcije i postignutih rezultata.')
        self.klik('#clanak-forma button[type="submit"]')
        self.klik('[data-tab="clanci"]')
        self.cekaj_tekst('#sec-clanci', 'Uspešno završena akcija čišćenja')
        self.assertTrue(Clanak.objects.filter(naslov='Uspešno završena akcija čišćenja').exists())

    def test_bez_naslova_prikazuje_gresku_2_2_2(self):
        """2.2.2 — slanje forme bez naslova prikazuje grešku, članak se ne pravi."""
        self.login(self.org_email)
        self.idi('/organizator-panel/')
        self.klik('[data-tab="clanci"]')
        self.klik('#btn-otvori-formu-clanka')
        Select(self.br.find_element(By.CSS_SELECTOR, '#clanak-forma select[name="kategorija"]')) \
            .select_by_value(str(self.kat.pk))
        self.br.find_element(By.CSS_SELECTOR, '#clanak-forma [name="tekst"]') \
            .send_keys('Tekst bez naslova.')
        self.klik('#clanak-forma button[type="submit"]')
        self.cekaj('#clanak-forma .form-error')
        self.assertEqual(Clanak.objects.count(), 0)
