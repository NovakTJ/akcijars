# Autor: Maša Nikolić 2023/0089
"""
Jedinični testovi za SSU 1 — Registracija korisnika.

Testira se kontroler ``registracija`` i forma ``RegistracijaForm``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).

Očekivane poruke i ponašanja su preuzeti iz SSU 1 (scenariji 2.2.1–2.2.7,
preduslov 2.4 i posledica 2.5), a ne iz implementacije.
"""
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import Korisnik, OrganizatorProfil, SponzorProfil
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

    def _greske_polja(self, r, polje):
        return r.context['form'].errors.get(polje, [])

    # ── 2.2.1 uspešna registracija volontera ────────────────────────────────
    def test_uspesna_registracija_volontera_2_2_1(self):
        """2.2.1 — kreira se nalog, prikazuje tačna poruka i šalje email; korisnik NIJE ulogovan (2.5)."""
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['uspeh'])
        self.assertEqual(
            r.context['poruka'],
            'Registracija je uspešna. Možete se prijaviti na sistem.',
        )
        k = Korisnik.objects.get(email='jovana.petrovic@gmail.com')
        self.assertTrue(k.je_volonter)
        self.assertEqual(len(mail.outbox), 1)  # 2.2.1 korak 6 — potvrda na email
        # Posledica 2.5 — korisnik ne postaje ulogovan.
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── 2.2.2 uspešna registracija organizatora / sponzora ──────────────────
    def test_registracija_organizatora_2_2_2(self):
        """2.2.2 — organizator: tačna poruka o čekanju odobrenja, status „na čekanju", email."""
        r = self.client.post(self.url, self._podaci(
            uloga='organizator', naziv_organizacije='Zeleni Beograd',
            br_telefona='060123456',
        ))
        self.assertEqual(
            r.context['poruka'],
            'Registracija je uspešna. Nalog čeka odobrenje jednog od administratora.',
        )
        k = Korisnik.objects.get(email='jovana.petrovic@gmail.com')
        self.assertEqual(k.organizator_profil.status, OrganizatorProfil.Status.NA_CEKANJU)
        self.assertEqual(len(mail.outbox), 1)

    def test_registracija_sponzora_2_2_2(self):
        """2.2.2 — sponzor: nalog dobija status „na čekanju"."""
        self.client.post(self.url, self._podaci(
            uloga='sponzor', naziv_organizacije='Delta fond',
            br_telefona='060123456',
        ))
        k = Korisnik.objects.get(email='jovana.petrovic@gmail.com')
        self.assertEqual(k.sponzor_profil.status, SponzorProfil.Status.NA_CEKANJU)

    # ── 2.2.3–2.2.7 greške (proveravamo TAČAN tekst poruke iz SSU) ───────────
    def test_neispravan_email_2_2_3(self):
        """2.2.3 — neispravan format email adrese: propisana poruka, nalog se ne pravi."""
        r = self.client.post(self.url, self._podaci(email='ovo-nije-email'))
        self.assertIn('Email adresa nije ispravnog formata.', self._greske_polja(r, 'email'))
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_lozinke_se_ne_poklapaju_2_2_4(self):
        """2.2.4 — lozinke se ne poklapaju: propisana poruka, nalog se ne pravi."""
        r = self.client.post(self.url, self._podaci(lozinka2='Drugacija9!'))
        self.assertIn('Lozinke se ne poklapaju.', self._greske_polja(r, 'lozinka2'))
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_postojeci_email_2_2_5(self):
        """2.2.5 — email već postoji: propisana poruka, nema novog naloga."""
        volonter('jovana.petrovic@gmail.com')
        r = self.client.post(self.url, self._podaci())
        self.assertIn('Korisnik sa tom email adresom već postoji.', self._greske_polja(r, 'email'))
        self.assertEqual(Korisnik.objects.filter(email='jovana.petrovic@gmail.com').count(), 1)

    def test_prazna_obavezna_polja_2_2_6(self):
        """2.2.6 — nepopunjena obavezna polja: jedinstvena globalna poruka, nalog se ne pravi."""
        r = self.client.post(self.url, {'uloga': 'volonter'})
        self.assertIn('Nisu uneta sva obavezna polja.', r.context['form'].non_field_errors())
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_slaba_lozinka_2_2_7(self):
        """2.2.7 — lozinka ne zadovoljava minimalne uslove: propisana poruka."""
        r = self.client.post(self.url, self._podaci(lozinka='abc', lozinka2='abc'))
        self.assertIn(
            'Lozinka mora imati najmanje 8 karaktera i sadržati barem '
            'jednu cifru ili specijalni karakter.',
            self._greske_polja(r, 'lozinka'),
        )
        self.assertEqual(Korisnik.objects.count(), 0)

    # ── Preduslov 2.4 ───────────────────────────────────────────────────────
    def test_ulogovan_korisnik_preusmeren_preduslov_2_4(self):
        """Preduslov 2.4 — ulogovanom korisniku se ne prikazuje registracija (preusmeren)."""
        self.client.force_login(volonter('vec.ulogovan@akcija.rs'))
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 302)

    # ── Dodatna validacija iz implementacije (van SSU scenarija) ─────────────
    def test_neispravan_telefon_organizatora(self):
        """Van SSU: organizator sa neispravnim formatom telefona → greška na polju."""
        r = self.client.post(self.url, self._podaci(
            uloga='organizator', naziv_organizacije='Org', br_telefona='abc123',
        ))
        self.assertIn('br_telefona', r.context['form'].errors)
        self.assertEqual(Korisnik.objects.count(), 0)
