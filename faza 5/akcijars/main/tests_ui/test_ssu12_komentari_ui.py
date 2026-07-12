# Autor: Milica Milošević 0357/2023
"""
Selenium WebDriver UI testovi za SSU 12 — Komentarisanje članaka
(implementirao Stefan Grujičić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By

from main.tests._helpers import organizator, volonter, clanak
from ._baza import SeleniumBazniTest


class KomentarUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.vol_email = f'jovana.petrovic.{s}@gmail.com'
        self.org = organizator(f'office.zelenibeograd.{s}@gmail.com')
        self.clanak = clanak(self.org, 'Članak za komentare')
        self.vol = volonter(self.vol_email)

    def test_uspesan_komentar_2_2_1(self):
        """2.2.1 — ulogovani korisnik ostavlja komentar koji se odmah prikazuje."""
        self.login(self.vol_email)
        self.idi(f'/clanci/{self.clanak.pk}/')
        self.cekaj('#comment-input').send_keys('Odličan članak!')
        self.klik('#submit-comment')
        self.cekaj_tekst('#comments-list', 'Odličan članak!')

    def test_prazan_komentar_prikazuje_gresku_2_2_2(self):
        """2.2.2 — prazan komentar prikazuje poruku „Komentar ne može biti prazan!"."""
        self.login(self.vol_email)
        self.idi(f'/clanci/{self.clanak.pk}/')
        self.klik('#submit-comment')
        self.cekaj_tekst('#comment-error', 'Komentar ne može biti prazan!')

    def test_gost_ne_vidi_formu_2_2_3(self):
        """2.2.3 — gost (neulogovan) ne vidi formu, već poziv na prijavu."""
        self.idi(f'/clanci/{self.clanak.pk}/')
        self.cekaj('body')
        self.assertEqual(len(self.br.find_elements(By.CSS_SELECTOR, '#comment-input')), 0)
        self.assertIn('Prijavite se', self.br.find_element(By.TAG_NAME, 'body').text)
