# Autor: Maša Nikolić 2023/0089
"""
Selenium WebDriver UI testovi za SSU 15 — Praćenje učešća volontera
(implementirao Stefan Grujičić — ukrštanje).
"""
from uuid import uuid4

from django.test import override_settings

from main.models import Akcija, Prijava
from main.tests._helpers import volonter, organizator, akcija, prijava
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')
class VolonterPanelUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.vol_email = f'vol.{s}@akcija.rs'
        self.vol = volonter(self.vol_email)
        self.org = organizator(f'org.{s}@akcija.rs')

    def test_panel_prikazuje_sate_i_tekucu_prijavu(self):
        """Panel prikazuje ukupne sate i tekuću prijavu volontera."""
        zavrsena = akcija(self.org, 'Zavrsena akcija', Akcija.Status.ZAVRSENA)
        prijava(self.vol, zavrsena, status=Prijava.Status.PRIHVACENA, br_sati=8)
        aktivna = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        prijava(self.vol, aktivna, status=Prijava.Status.NA_CEKANJU)

        self.login(self.vol_email)
        self.idi('/volonter-panel/')
        # ukupni sati u zaglavlju panela
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '8')
        # tab „Tekuće" prikazuje aktivnu akciju
        self.klik('[data-tab="tekuce"]')
        self.cekaj_tekst('#sec-tekuce', 'Aktivna akcija')

    def test_prazan_panel_2_2_3(self):
        """
        2.2.3 — volonter bez učešća: 0 sati i propisana SSU poruka.

        NAPOMENA: proverava tačnu poruku iz SSU 2.2.3. Pašće dok Stefan ne
        uskladi prazno stanje istorije sa specifikacijom (prijavljeno kolegi).
        """
        self.login(self.vol_email)
        self.idi('/volonter-panel/')
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '0')
        self.klik('[data-tab="istorija"]')
        self.cekaj_tekst('#sec-istorija', 'Još uvek niste učestvovali ni na jednoj akciji.')

    def test_ne_volonter_ne_pristupa_panelu(self):
        """Organizator ne može da otvori volonterski panel — preusmeren je."""
        org_email = f'org2.{uuid4().hex[:6]}@akcija.rs'
        organizator(org_email)
        self.login(org_email)
        self.idi('/volonter-panel/')
        self.assertNotIn('/volonter-panel', self.br.current_url)
