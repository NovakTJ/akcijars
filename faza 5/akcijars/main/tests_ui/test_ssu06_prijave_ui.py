# Autor: Milica Milošević 0357/2023
"""
Selenium WebDriver UI testovi za SSU 6 — Prijava/odjava volontera na akciju
(implementirala Maša Nikolić — ukrštanje).
"""
from uuid import uuid4

from django.test import override_settings

from main.models import Akcija
from main.tests._helpers import organizator, volonter, akcija
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')  # bez učitavanja Google Maps u testu
class PrijavaVolonteraUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.vol_email = f'jovana.petrovic.{s}@gmail.com'
        self.org = organizator(f'office.zelenibeograd.{s}@gmail.com')
        self.vol = volonter(self.vol_email)
        self.akc = akcija(self.org, 'Akcija za prijavu', Akcija.Status.AKTIVNA)

    def test_prijava_pa_odjava_2_2_1_2_2_2(self):
        """2.2.1 / 2.2.2 — volonter se prijavi (pojavi se dugme Odjavi), pa odjavi."""
        self.login(self.vol_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik('#btn-prijavi')
        # posle prijave sidebar prikazuje dugme za odjavu
        self.cekaj('#btn-odjavi')
        # odjava vraća dugme za prijavu
        self.klik('#btn-odjavi')
        self.cekaj('#btn-prijavi')

    def test_popunjena_akcija_nema_dugme_2_2_4(self):
        """2.2.4 — na popunjenoj akciji nema dugmeta „Prijavi se", već poruka."""
        self.akc.status = Akcija.Status.POPUNJENA
        self.akc.save()
        self.login(self.vol_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        telo = self.cekaj('#prijava-container').text
        self.assertIn('Sva mesta na ovoj akciji su popunjena.', telo)
        self.assertEqual(len(self.br.find_elements('css selector', '#btn-prijavi')), 0)
