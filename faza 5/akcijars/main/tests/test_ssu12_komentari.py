# Autor: Milica Milošević 0357/2023
"""
Jedinični testovi za SSU 12 — Komentarisanje članaka.

Testira se kontroler ``ajax_dodaj_komentar``, prikaz forme na ``detalj_clanka``
i ``KomentarForm`` (funkcionalnost je implementirao Stefan Grujičić — ukrštanje).
"""
import json

from django.test import TestCase
from django.urls import reverse

from main.models import Clanak, Komentar
from main.forms import KomentarForm
from ._helpers import organizator, volonter, clanak


class DodajKomentarTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.clanak = clanak(self.org, 'Članak SSU12')
        self.vol = volonter('jovana.petrovic@gmail.com')
        self.url = reverse('ajax_dodaj_komentar', args=[self.clanak.pk])

    def _posalji(self, tekst):
        return self.client.post(
            self.url, data=json.dumps({'tekst': tekst}), content_type='application/json',
        )

    def test_uspesan_komentar_2_2_1(self):
        """2.2.1 — ulogovani korisnik uspešno ostavlja komentar."""
        self.client.force_login(self.vol)
        r = self._posalji('Odličan članak!')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['br_komentara'], 1)
        k = Komentar.objects.get(clanak=self.clanak)
        self.assertEqual(k.tekst, 'Odličan članak!')
        self.assertEqual(k.korisnik, self.vol)

    def test_prazan_komentar_odbijen_na_serveru_2_2_2(self):
        """
        2.2.2 — prazan komentar se odbija i ne evidentira.

        Napomena: poruku „Komentar ne može biti prazan!" (SSU 12, 2.2.2)
        prikazuje klijentska strana (clanak.js) pre slanja zahteva. Ovaj test
        proverava serversku odbranu — direktan zahtev sa praznim tekstom se
        odbija (400) i komentar se ne kreira.
        """
        self.client.force_login(self.vol)
        r = self._posalji('   ')
        self.assertEqual(r.status_code, 400)
        self.assertIn('error', r.json())
        self.assertFalse(Komentar.objects.filter(clanak=self.clanak).exists())

    def test_neulogovan_ne_moze_da_komentarise_2_2_3(self):
        """2.2.3 — gost ne može da ostavi komentar (login_required)."""
        r = self._posalji('Pokušaj gosta')
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Komentar.objects.filter(clanak=self.clanak).exists())

    def test_komentar_na_neobjavljen_clanak_404(self):
        """Komentarisanje neobjavljenog članka nije moguće (404)."""
        neobjavljen = clanak(self.org, 'Neobjavljen', status=Clanak.Status.NA_CEKANJU)
        self.client.force_login(self.vol)
        r = self.client.post(
            reverse('ajax_dodaj_komentar', args=[neobjavljen.pk]),
            data=json.dumps({'tekst': 'x'}), content_type='application/json',
        )
        self.assertEqual(r.status_code, 404)


class KomentarFormaPrikazTest(TestCase):
    """SSU 12, 2.2.3 — forma za komentar dostupna samo ulogovanima."""

    def setUp(self):
        self.org = organizator('crvenikrst.bg@gmail.com')
        self.clanak = clanak(self.org, 'Članak SSU12b')

    def test_ulogovan_dobija_formu(self):
        vol = volonter('marko.nikolic@gmail.com')
        self.client.force_login(vol)
        r = self.client.get(reverse('detalj_clanka', args=[self.clanak.pk]))
        self.assertIsNotNone(r.context['forma'])

    def test_gost_ne_dobija_formu(self):
        r = self.client.get(reverse('detalj_clanka', args=[self.clanak.pk]))
        self.assertIsNone(r.context['forma'])


class KomentarFormTest(TestCase):
    """Validacija ``KomentarForm``."""

    def test_prazan_tekst_nevalidan(self):
        """Prazan/whitespace tekst čini formu nevalidnom (greška na polju 'tekst')."""
        forma = KomentarForm({'tekst': '   '})
        self.assertFalse(forma.is_valid())
        self.assertIn('tekst', forma.errors)

    def test_validan_tekst(self):
        forma = KomentarForm({'tekst': 'Sadržajan komentar.'})
        self.assertTrue(forma.is_valid())
