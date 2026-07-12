# Autor: Milica Milošević 0357/2023
"""
Jedinični testovi za SSU 7 — Dodavanje sponzora akciji (slanje ponude).

Testira se kontroler ``posalji_ponudu`` i ``SponzorskaPonudaForm``
(funkcionalnost je implementirao Stefan Grujičić — ukrštanje).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, SponzorskaPonuda, SponzorProfil
from main.forms import SponzorskaPonudaForm
from ._helpers import organizator, sponzor, akcija


class PosaljiPonuduTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.akc = akcija(self.org, 'Akcija SSU7', Akcija.Status.AKTIVNA)
        self.spon = sponzor('sponzorstva.delta@gmail.com', naziv='Delta Holding')
        self.url = reverse('posalji_ponudu', args=[self.akc.pk])

    def _podaci(self, **izmene):
        d = {'akcija': self.akc.pk, 'vrednost': 500, 'opis': 'Oprema i sredstva.'}
        d.update(izmene)
        return d

    def test_uspesna_ponuda_2_2_1(self):
        """2.2.1 — sponzor uspešno šalje ponudu; evidentira se sa statusom na čekanju."""
        self.client.force_login(self.spon)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 200)
        p = SponzorskaPonuda.objects.get(sponzor=self.spon.sponzor_profil, akcija=self.akc)
        self.assertEqual(p.status, SponzorskaPonuda.Status.NA_CEKANJU)
        self.assertEqual(p.vrednost, 500)

    def test_nepotpuna_ponuda_bez_opisa_2_2_2(self):
        """2.2.2 — nepotpuna ponuda (prazan opis) se ne evidentira."""
        self.client.force_login(self.spon)
        r = self.client.post(self.url, self._podaci(opis=''))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(SponzorskaPonuda.objects.filter(akcija=self.akc).exists())

    def test_neispravna_vrednost_nula_2_2_3(self):
        """2.2.3 — vrednost 0 nije dozvoljena; ponuda se ne evidentira."""
        self.client.force_login(self.spon)
        r = self.client.post(self.url, self._podaci(vrednost=0))
        self.assertFalse(SponzorskaPonuda.objects.filter(akcija=self.akc).exists())

    def test_samo_sponzor_moze_403(self):
        """Organizator (ne-sponzor) ne može da pošalje ponudu (403)."""
        self.client.force_login(self.org)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 403)

    def test_neodobren_sponzor_403(self):
        """Sponzor čiji nalog nije odobren ne može da pošalje ponudu (403)."""
        neodobren = sponzor('kontakt.nis@gmail.com', status=SponzorProfil.Status.NA_CEKANJU)
        self.client.force_login(neodobren)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 403)

    def test_otkazana_akcija_403(self):
        """Na otkazanu akciju nije moguće poslati ponudu (403)."""
        self.akc.status = Akcija.Status.OTKAZANA
        self.akc.save()
        self.client.force_login(self.spon)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 403)


class SponzorskaPonudaFormTest(TestCase):
    """Validacija ``SponzorskaPonudaForm`` (SSU 7, 2.2.3)."""

    def setUp(self):
        self.org = organizator('crvenikrst.bg@gmail.com')
        self.akc = akcija(self.org, 'Akcija SSU7f')

    def test_nula_vrednost_nevalidna(self):
        forma = SponzorskaPonudaForm({'akcija': self.akc.pk, 'vrednost': 0, 'opis': 'x'})
        self.assertFalse(forma.is_valid())
        self.assertIn('Vrednost mora biti pozitivan broj.', forma.errors.get('vrednost', []))

    def test_prazan_opis_nevalidan(self):
        forma = SponzorskaPonudaForm({'akcija': self.akc.pk, 'vrednost': 100, 'opis': ''})
        self.assertFalse(forma.is_valid())

    def test_ispravna_ponuda_validna(self):
        forma = SponzorskaPonudaForm({'akcija': self.akc.pk, 'vrednost': 100, 'opis': 'Donacija.'})
        self.assertTrue(forma.is_valid())
