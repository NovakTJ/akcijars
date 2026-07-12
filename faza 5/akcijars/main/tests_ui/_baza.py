# Autor: Milica Milošević 0357/2023
"""
Zajednička osnova za Selenium WebDriver UI testove (faza 7).

Koristi Django ``StaticLiveServerTestCase`` — Django sam podigne test server i
izolovanu test bazu, a Selenium (headless Chrome) kroz pravi pretraživač klika
kroz interfejs. Ništa se ne dira u produkcionoj bazi.

Da bi se prozor pretraživača video tokom izvršavanja (umesto headless):
    SELENIUM_HEADLESS=0 python manage.py test main.tests_ui
"""
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBazniTest(StaticLiveServerTestCase):
    """Podiže headless Chrome jednom po test klasi i nudi pomoćne metode."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opcije = Options()
        if os.getenv('SELENIUM_HEADLESS', '1') != '0':
            opcije.add_argument('--headless=new')
        opcije.add_argument('--no-sandbox')
        opcije.add_argument('--disable-gpu')
        opcije.add_argument('--window-size=1400,1000')
        cls.br = webdriver.Chrome(options=opcije)
        cls.br.implicitly_wait(3)
        # Spori režim za posmatranje uživo: SELENIUM_SLOW=1 (sekunde pauze po akciji).
        cls.sporo = float(os.getenv('SELENIUM_SLOW', '0'))

    @classmethod
    def tearDownClass(cls):
        cls.br.quit()
        super().tearDownClass()

    # ── pomoćne metode ──────────────────────────────────────────────────────

    def _pauza(self):
        """Kratka pauza u sporom režimu (da se akcije vide uživo)."""
        if self.sporo:
            time.sleep(self.sporo)

    def idi(self, putanja):
        """Otvara datu putanju na test serveru."""
        self.br.get(self.live_server_url + putanja)
        self._pauza()

    def cekaj(self, css, t=10):
        """Čeka da element (CSS selektor) bude prisutan i vraća ga."""
        return WebDriverWait(self.br, t).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css)))

    def klik(self, css, t=10):
        """
        Skroluje element u centar ekrana i klikne. Ako native klik presretne
        fiksni element (footer/navbar), pada na JS klik (koji svejedno okine
        isti event handler).
        """
        el = self.cekaj(css, t)
        self.br.execute_script('arguments[0].scrollIntoView({block: "center"});', el)
        try:
            WebDriverWait(self.br, t).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
            el.click()
        except ElementClickInterceptedException:
            self.br.execute_script('arguments[0].click();', el)
        self._pauza()
        return el

    def cekaj_tekst(self, css, tekst, t=10):
        """Čeka da se dati tekst pojavi u elementu (CSS selektor)."""
        WebDriverWait(self.br, t).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, css), tekst))

    def tekst(self, css):
        """Vraća tekst elementa po CSS selektoru."""
        return self.br.find_element(By.CSS_SELECTOR, css).text

    def login(self, email, lozinka='Test1234!'):
        """Prijavljuje korisnika kroz login formu i čeka preusmeravanje."""
        self.idi('/prijava/')
        self.br.find_element(By.NAME, 'email').send_keys(email)
        self.br.find_element(By.NAME, 'lozinka').send_keys(lozinka)
        self.br.find_element(By.CSS_SELECTOR, '#login-form button[type="submit"]').click()
        WebDriverWait(self.br, 10).until(lambda d: '/prijava/' not in d.current_url)
