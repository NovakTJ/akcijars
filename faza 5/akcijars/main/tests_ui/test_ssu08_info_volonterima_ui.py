# Autor: Stefan Grujičić 0030/2023
"""
Selenium WebDriver UI testovi za SSU 8 — Slanje informacija volonterima
(implementirao Novak Stijepić — ukrštanje).
"""
from uuid import uuid4

from django.core import mail

from main.models import Akcija, Prijava
from main.tests._helpers import organizator, volonter, akcija, prijava
from ._baza import SeleniumBazniTest


class ObavestenjeVolonterimaUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'office.zelenibeograd.{s}@gmail.com'
        self.org = organizator(self.org_email)
        self.akc = akcija(self.org, 'Akcija SSU8 UI', Akcija.Status.AKTIVNA, max_vol=5)
        self.vol = volonter(f'vol.{s}@gmail.com')
        prijava(self.vol, self.akc, status=Prijava.Status.PRIHVACENA)

    def test_uspesno_slanje_obavestenja_2_2_1(self):
        """2.2.1 — unos teksta i slanje obaveštenja prihvaćenom volonteru."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-obavestenje')
        self.cekaj('#obavestenje-tekst').send_keys('Hvala vam na učešću u akciji!')
        self.klik('#btn-posalji-obavestenje')
        self.cekaj_tekst('#obavestenje-rezultat', 'Obaveštenje je poslato')
        self.assertEqual(len(mail.outbox), 1)

    def test_prazna_poruka_prikazuje_gresku_2_2_2(self):
        """2.2.2 — slanje bez unetog teksta prikazuje grešku, ništa se ne šalje."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#otab-org-obavestenje')
        self.klik('#btn-posalji-obavestenje')
        self.cekaj_tekst('#obavestenje-rezultat', 'Unesite tekst poruke.')
        self.assertEqual(len(mail.outbox), 0)
