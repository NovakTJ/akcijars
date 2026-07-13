# Autor: Maša Nikolić 2023/0089
"""
Selenium WebDriver UI testovi za SSU 1 — Registracija korisnika
(implementirao Novak Stijepić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By

from main.models import Korisnik
from ._baza import SeleniumBazniTest


class RegistracijaUITest(SeleniumBazniTest):
    def _popuni(self, email, lozinka='Test1234!', lozinka2='Test1234!'):
        """Otvara registraciju i popunjava polja za volontera (uloga ostaje volonter)."""
        self.idi('/registracija/')
        self.br.find_element(By.NAME, 'ime').send_keys('Jovana')
        self.br.find_element(By.NAME, 'prezime').send_keys('Petrović')
        self.br.find_element(By.NAME, 'email').send_keys(email)
        self.br.find_element(By.NAME, 'lozinka').send_keys(lozinka)
        self.br.find_element(By.NAME, 'lozinka2').send_keys(lozinka2)

    def test_uspesna_registracija_volontera(self):
        """Volonter popuni ispravnu formu i dobije poruku o uspehu; nalog je kreiran."""
        email = f'jovana.{uuid4().hex[:6]}@gmail.com'
        self._popuni(email)
        self.klik('#reg-form button[type="submit"]')
        # SSU 2.2.1 korak 5 — tačna poruka o uspehu
        self.cekaj_tekst('body', 'Registracija je uspešna. Možete se prijaviti na sistem.')
        self.assertTrue(Korisnik.objects.filter(email=email).exists())

    def test_lozinke_se_ne_poklapaju(self):
        """Različite lozinke → prikazuje se greška, nalog se ne pravi."""
        email = f'neuspeh.{uuid4().hex[:6]}@gmail.com'
        self._popuni(email, lozinka='Test1234!', lozinka2='Drugacija9!')
        self.klik('#reg-form button[type="submit"]')
        self.cekaj_tekst('body', 'Lozinke se ne poklapaju.')
        self.assertFalse(Korisnik.objects.filter(email=email).exists())

    def test_prazna_polja(self):
        """Slanje prazne forme → jedinstvena poruka o nepopunjenim obaveznim poljima."""
        self.idi('/registracija/')
        self.klik('#reg-form button[type="submit"]')
        self.cekaj_tekst('body', 'Nisu uneta sva obavezna polja.')
