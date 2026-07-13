# Autor: Maša Nikolić 2023/0089
"""
Selenium WebDriver UI testovi za SSU 17 — Potvrđivanje i odbijanje sponzorstva
(implementirao Stefan Grujičić — ukrštanje).
"""
from uuid import uuid4

from django.test import override_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from main.models import SponzorskaPonuda
from main.tests._helpers import organizator, sponzor, akcija, ponuda
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')
class SponzorstvoUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'org.{s}@akcija.rs'
        self.org = organizator(self.org_email)
        self.spon = sponzor(f'spon.{s}@akcija.rs', naziv='Delta fond')
        self.akc = akcija(self.org, 'Akcija za sponzore')

    def test_organizator_prihvata_ponudu(self):
        """2.2.1 — organizator prihvati ponudu; ponuda prelazi u prihvaćene i sponzor se vidi na akciji."""
        pon = ponuda(self.spon, self.akc)
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-sp')                                   # tab „Sponzori"
        self.klik(f'.btn-prihvati-ponudu[data-ponuda-id="{pon.pk}"]')
        # dugme „Prihvati" nestaje (ponuda više nije na čekanju) — Ajax bez reload-a
        WebDriverWait(self.br, 10).until(
            lambda d: not d.find_elements(
                By.CSS_SELECTOR, f'.btn-prihvati-ponudu[data-ponuda-id="{pon.pk}"]'))
        self.assertEqual(
            SponzorskaPonuda.objects.get(pk=pon.pk).status,
            SponzorskaPonuda.Status.PRIHVACENA,
        )
        # 2.2.1 korak 7 — po ponovnom učitavanju sponzor je u sekciji „Sponzori"
        self.idi(f'/akcije/{self.akc.pk}/')
        self.cekaj_tekst('body', 'Sponzori ove akcije')
        self.assertIn('Delta fond', self.tekst('body'))

    def test_prazne_ponude_2_2_3(self):
        """
        2.2.3 — nema pristiglih ponuda: propisana SSU poruka.

        NAPOMENA: proverava tačan tekst iz SSU 2.2.3. Pašće dok Stefan ne
        uskladi poruku (kod ima „Nema pristiglih…", SSU traži „Trenutno nema…").
        """
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-sp')
        self.cekaj_tekst('#org-sp', 'Trenutno nema pristiglih ponuda za sponzorstvo.')
