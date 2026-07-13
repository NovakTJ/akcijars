# Autor: Stefan Grujičić 0030/2023
"""
Jedinični testovi za SSU 11 — Kreiranje članka.

Testira se kontroler ``kreiraj_clanak`` i forma ``ClanakForma``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Clanak, OrganizatorProfil
from ._helpers import organizator, volonter, kat_clanka


class KreirajClanakTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')  # helper podrazumevano ODOBREN
        self.kat = kat_clanka('Ekologija')
        self.url = reverse('kreiraj_clanak')

    def _podaci(self, **izmene):
        """Vraća validne podatke za kreiranje članka; ``izmene`` prepisuju polja."""
        podaci = {
            'kategorija': self.kat.pk,
            'naslov': 'Uspešno završena akcija čišćenja',
            'tekst': 'Detaljan opis akcije, broja učesnika i postignutih rezultata.',
        }
        podaci.update(izmene)
        return podaci

    def test_uspesno_kreiranje_2_2_1(self):
        """2.2.1 — članak se čuva sa statusom „na čekanju" i vezuje za organizatora."""
        self.client.force_login(self.org)
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('organizator_panel'))
        c = Clanak.objects.get(naslov='Uspešno završena akcija čišćenja')
        self.assertEqual(c.status, Clanak.Status.NA_CEKANJU)
        self.assertEqual(c.autor, self.org.organizator_profil)

    def test_bez_naslova_2_2_2(self):
        """2.2.2 — prazan naslov se odbija (Django required polje), članak se ne pravi."""
        self.client.force_login(self.org)
        r = self.client.post(self.url, self._podaci(naslov=''))
        self.assertEqual(r.status_code, 200)
        self.assertIn('naslov', r.context['forma_clanka'].errors)
        self.assertEqual(Clanak.objects.count(), 0)

    def test_bez_sadrzaja_2_2_3(self):
        """2.2.3 — prazan sadržaj (tekst) se odbija (Django required polje), članak se ne pravi."""
        self.client.force_login(self.org)
        r = self.client.post(self.url, self._podaci(tekst=''))
        self.assertEqual(r.status_code, 200)
        self.assertIn('tekst', r.context['forma_clanka'].errors)
        self.assertEqual(Clanak.objects.count(), 0)

    def test_odustajanje_ne_kreira_2_2_4(self):
        """2.2.4 — otvaranje organizatorskog panela bez slanja forme ne pravi članak."""
        self.client.force_login(self.org)
        self.client.get(reverse('organizator_panel'))
        self.assertEqual(Clanak.objects.count(), 0)

    def test_ne_organizator_preusmeren(self):
        """Pristup imaju samo organizatori — volonter se preusmerava, članak se ne pravi."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('home'))
        self.assertEqual(Clanak.objects.count(), 0)

    def test_neodobren_organizator_preusmeren(self):
        """Preduslov — organizator čiji nalog čeka odobrenje ne može da kreira članak."""
        neodobren = organizator('neodobren@org.rs', status=OrganizatorProfil.Status.NA_CEKANJU)
        self.client.force_login(neodobren)
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('home'))
        self.assertEqual(Clanak.objects.count(), 0)

    def test_neulogovan_preusmeren(self):
        """login_required — neulogovan korisnik se preusmerava (302)."""
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Clanak.objects.count(), 0)

    def test_get_preusmerava_na_panel(self):
        """GET zahtev (bez slanja forme) samo preusmerava na organizatorski panel."""
        self.client.force_login(self.org)
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse('organizator_panel'))
