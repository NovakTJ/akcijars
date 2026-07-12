# Autor: Maša Nikolić 2023/0089
"""
Jedinični testovi za SSU 1 — Registracija korisnika.

Testira se kontroler ``registracija`` i forma ``RegistracijaForm``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).
"""
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import Korisnik, OrganizatorProfil
from ._helpers import volonter


class RegistracijaTest(TestCase):
    def setUp(self):
        self.url = reverse('registracija')

    def _podaci(self, **izmene):
        """Vraća validne podatke za registraciju volontera; ``izmene`` prepisuju polja."""
        podaci = {
            'ime': 'Jovana', 'prezime': 'Petrović',
            'email': 'jovana.petrovic@gmail.com',
            'lozinka': 'Test1234!', 'lozinka2': 'Test1234!',
            'uloga': 'volonter',
        }
        podaci.update(izmene)
        return podaci

    def test_uspesna_registracija_volontera_2_2_1(self):
        """2.2.1 / 2.2.2 — volonter se uspešno registruje; kreiran nalog, profil i poslat email."""
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['uspeh'])
        k = Korisnik.objects.get(email='jovana.petrovic@gmail.com')
        self.assertTrue(k.je_volonter)
        self.assertEqual(len(mail.outbox), 1)  # potvrda registracije

    def test_registracija_organizatora_ceka_odobrenje(self):
        """Organizator se registruje; nalog dobija status „Na čekanju"."""
        self.client.post(self.url, self._podaci(
            uloga='organizator', naziv_organizacije='Zeleni Beograd',
            br_telefona='060123456',
        ))
        k = Korisnik.objects.get(email='jovana.petrovic@gmail.com')
        self.assertTrue(k.je_organizator)
        self.assertEqual(k.organizator_profil.status, OrganizatorProfil.Status.NA_CEKANJU)

    def test_prazna_obavezna_polja_2_2_6(self):
        """2.2.6 — nepopunjena obavezna polja: jedinstvena globalna poruka, nalog se ne pravi."""
        r = self.client.post(self.url, {'uloga': 'volonter'})
        self.assertIn('Nisu uneta sva obavezna polja.', r.context['form'].non_field_errors())
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_neispravan_email_2_2_3(self):
        """2.2.3 — neispravan format email adrese: greška na polju, nalog se ne pravi."""
        r = self.client.post(self.url, self._podaci(email='ovo-nije-email'))
        self.assertIn('email', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_postojeci_email_2_2_5(self):
        """2.2.5 — email već postoji: greška, nema novog naloga."""
        volonter('jovana.petrovic@gmail.com')
        r = self.client.post(self.url, self._podaci())
        self.assertIn('email', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.filter(email='jovana.petrovic@gmail.com').count(), 1)

    def test_slaba_lozinka_2_2_7(self):
        """2.2.7 — lozinka ne zadovoljava uslove (prekratka, bez cifre/spec. znaka)."""
        r = self.client.post(self.url, self._podaci(lozinka='abc', lozinka2='abc'))
        self.assertIn('lozinka', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_lozinke_se_ne_poklapaju_2_2_4(self):
        """2.2.4 — lozinke se ne poklapaju: greška, nalog se ne pravi."""
        r = self.client.post(self.url, self._podaci(lozinka2='Drugacija9!'))
        self.assertIn('lozinka2', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_neispravan_telefon_organizatora(self):
        """Organizator sa neispravnim telefonom: greška na polju ``br_telefona``."""
        r = self.client.post(self.url, self._podaci(
            uloga='organizator', naziv_organizacije='Org', br_telefona='abc123',
        ))
        self.assertIn('br_telefona', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.count(), 0)
