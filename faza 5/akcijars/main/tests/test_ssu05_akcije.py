# Autor: Stefan Grujičić 0030/2023
"""
Jedinični testovi za SSU 5 — Kreiranje akcije.

Testira se kontroler ``kreiraj_akciju`` i forma ``AkcijaForm``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).

Google Maps je isključen (``GOOGLE_MAPS_API_KEY=''``) da izbor lokacije preko
mape ne bude obavezan u testu — SSU 5 testira ostala polja forme.
"""
import datetime

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from main.models import Akcija
from ._helpers import organizator, volonter, kat_akcije


@override_settings(GOOGLE_MAPS_API_KEY='')
class KreirajAkcijuTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')  # helper podrazumevano ODOBREN
        self.kat = kat_akcije('Ekologija')
        self.url = reverse('kreiraj_akciju')
        self.client.force_login(self.org)

    def _podaci(self, **izmene):
        """Vraća validne podatke za kreiranje akcije; ``izmene`` prepisuju polja."""
        podaci = {
            'naziv': 'Čišćenje parka u Zvezdari',
            'opis': 'Čistimo park i sadimo nova drveća.',
            'datum': (timezone.localdate() + datetime.timedelta(days=10)).isoformat(),
            'vreme': '09:00',
            'lokacija': 'Ada Ciganlija, Beograd',
            'kategorija': self.kat.pk,
            'max_br_volontera': 20,
            'kontakt_email': 'kontakt@zeleni.rs',
            'kontakt_telefon': '060 123 456',
        }
        podaci.update(izmene)
        return podaci

    def test_uspesno_kreiranje_2_2_1(self):
        """2.2.1 — akcija se čuva sa statusom „na čekanju" i vezuje za organizatora."""
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('moje_akcije'))
        akc = Akcija.objects.get(naziv='Čišćenje parka u Zvezdari')
        self.assertEqual(akc.status, Akcija.Status.NA_CEKANJU)
        self.assertEqual(akc.organizator, self.org.organizator_profil)

    def test_prazna_obavezna_polja_2_2_2(self):
        """2.2.2 — nepopunjena obavezna polja: jedinstvena globalna poruka, akcija se ne pravi."""
        r = self.client.post(self.url, {'kategorija': self.kat.pk})
        self.assertIn('Nisu uneta sva obavezna polja.', r.context['form'].non_field_errors())
        self.assertEqual(Akcija.objects.count(), 0)

    def test_datum_u_proslosti_2_2_3(self):
        """2.2.3 — datum održavanja u prošlosti se odbija."""
        r = self.client.post(self.url, self._podaci(
            datum=(timezone.localdate() - datetime.timedelta(days=1)).isoformat(),
        ))
        self.assertIn(
            'Datum održavanja akcije ne sme biti u prošlosti.',
            r.context['form'].errors['datum'],
        )
        self.assertEqual(Akcija.objects.count(), 0)

    def test_nevalidan_max_broj_volontera_2_2_4(self):
        """2.2.4 — nevalidan (0 ili negativan) maksimalan broj volontera se odbija."""
        r = self.client.post(self.url, self._podaci(max_br_volontera=0))
        self.assertIn(
            'Maksimalan broj volontera mora biti pozitivan broj.',
            r.context['form'].errors['max_br_volontera'],
        )
        self.assertEqual(Akcija.objects.count(), 0)

    def test_neispravan_email_format_2_2_5(self):
        """2.2.5 — neispravan format kontakt email adrese se odbija."""
        r = self.client.post(self.url, self._podaci(kontakt_email='ovo-nije-email'))
        self.assertIn(
            'Kontakt email nije ispravnog formata.',
            r.context['form'].errors['kontakt_email'],
        )
        self.assertEqual(Akcija.objects.count(), 0)

    def test_neispravan_telefon_format_2_2_6(self):
        """2.2.6 — neispravan format kontakt telefona se odbija."""
        r = self.client.post(self.url, self._podaci(kontakt_telefon='060-abc-@@@'))
        self.assertIn(
            'Kontakt telefon nije ispravnog formata.',
            r.context['form'].errors['kontakt_telefon'],
        )
        self.assertEqual(Akcija.objects.count(), 0)

    def test_odustajanje_ne_cuva_2_2_7(self):
        """2.2.7 — otvaranje forme bez slanja podataka ne pravi akciju."""
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Akcija.objects.count(), 0)

    def test_neodobren_organizator_preusmeren(self):
        """Preduslov 2.4 — neodobren organizator ne može da kreira akciju."""
        neodobren = organizator('neodobren@org.rs')
        neodobren.organizator_profil.status = 'na_cekanju'
        neodobren.organizator_profil.save(update_fields=['status'])
        self.client.force_login(neodobren)
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('home'))
        self.assertEqual(Akcija.objects.count(), 0)

    def test_ne_organizator_preusmeren(self):
        """Preduslov 2.4 — ne-organizator (volonter) ne može da kreira akciju."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self.client.post(self.url, self._podaci())
        self.assertRedirects(r, reverse('home'))
        self.assertEqual(Akcija.objects.count(), 0)

    def test_neulogovan_preusmeren(self):
        """login_required — neulogovan korisnik se preusmerava (302)."""
        self.client.logout()
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 302)
