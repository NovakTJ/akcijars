# Autor: Stefan Grujičić 0030/2023
"""
Jedinični testovi za SSU 2 — Autorizacija (prijava/odjava) korisnika.

Testira se kontroler ``prijava``/``odjava`` i forma ``PrijavaForm``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).

Očekivane poruke i ponašanja su preuzeti iz SSU 2 (scenariji 2.2.1–2.2.5).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import OrganizatorProfil
from ._helpers import LOZINKA, volonter, organizator


class PrijavaTest(TestCase):
    def setUp(self):
        self.url = reverse('prijava')

    def test_uspesna_prijava_volontera_2_2_1(self):
        """2.2.1 — uspešna prijava volontera vodi na njegovu ličnu stranicu."""
        volonter('jovana.petrovic@gmail.com')
        r = self.client.post(self.url, {'email': 'jovana.petrovic@gmail.com', 'lozinka': LOZINKA})
        self.assertRedirects(r, reverse('volonter_panel'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_uspesna_prijava_organizatora_2_2_1(self):
        """2.2.1 — uspešna prijava organizatora vodi na organizatorski panel (prema ulozi)."""
        organizator('office.zelenibeograd@gmail.com')  # helper podrazumevano ODOBREN
        r = self.client.post(self.url, {'email': 'office.zelenibeograd@gmail.com', 'lozinka': LOZINKA})
        self.assertRedirects(r, reverse('organizator_panel'))

    def test_nepostojeci_email_2_2_2(self):
        """2.2.2 — nepostojeći email: propisana poruka, korisnik ostaje neulogovan."""
        r = self.client.post(self.url, {'email': 'nepostoji@gmail.com', 'lozinka': LOZINKA})
        self.assertIn(
            'Email adresa ili lozinka nisu ispravni.',
            r.context['form'].non_field_errors(),
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_neispravna_lozinka_2_2_3(self):
        """2.2.3 — pogrešna lozinka: ista poruka kao za nepostojeći email (ne otkriva se koji je slučaj)."""
        volonter('jovana.petrovic@gmail.com')
        r = self.client.post(self.url, {'email': 'jovana.petrovic@gmail.com', 'lozinka': 'PogresnaLoz1!'})
        self.assertIn(
            'Email adresa ili lozinka nisu ispravni.',
            r.context['form'].non_field_errors(),
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_neodobren_nalog_2_2_4(self):
        """2.2.4 — organizator čiji nalog čeka odobrenje ne može da se prijavi."""
        organizator('cekanje@org.rs', status=OrganizatorProfil.Status.NA_CEKANJU)
        r = self.client.post(self.url, {'email': 'cekanje@org.rs', 'lozinka': LOZINKA})
        self.assertIn(
            'Nalog čeka odobrenje administratora.',
            r.context['form'].non_field_errors(),
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_odbijen_nalog_takodje_blokiran(self):
        """Odbijen nalog (posledica 2.2.4) takođe ne može da se prijavi."""
        organizator('odbijen@org.rs', status=OrganizatorProfil.Status.ODBIJEN)
        r = self.client.post(self.url, {'email': 'odbijen@org.rs', 'lozinka': LOZINKA})
        self.assertIn(
            'Nalog čeka odobrenje administratora.',
            r.context['form'].non_field_errors(),
        )

    def test_prazna_polja(self):
        """Van SSU: nepopunjena obavezna polja — jedinstvena poruka, nema autentifikacije."""
        r = self.client.post(self.url, {'email': '', 'lozinka': ''})
        self.assertIn('Nisu uneta sva obavezna polja.', r.context['form'].non_field_errors())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_ulogovan_korisnik_preusmeren(self):
        """Ulogovanom korisniku se ne prikazuje forma za prijavu — preusmeren je na svoju stranicu."""
        self.client.force_login(volonter('vec.ulogovan@akcija.rs'))
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse('volonter_panel'))


class OdjavaTest(TestCase):
    def test_odjava_brise_sesiju_2_2_5(self):
        """2.2.5 — odjava briše sesiju i vraća korisnika na početnu."""
        vol = volonter('marko.nikolic@gmail.com')
        self.client.force_login(vol)
        self.assertIn('_auth_user_id', self.client.session)
        r = self.client.get(reverse('odjava'))
        self.assertRedirects(r, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)
