# Autor: Milica Milošević 0357/2023
"""
Jedinični testovi za SSU 6 — Prijava i odjava volontera na akciju.

Testira se kontroler ``prijavi_se`` / ``odjavi_se`` i model ``Prijava``
(funkcionalnost je implementirala Maša Nikolić — ukrštanje).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, Prijava
from ._helpers import volonter, organizator, sponzor, akcija


class PrijavaVolonteraTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.vol = volonter('jovana.petrovic@gmail.com')
        self.akc = akcija(self.org, 'Akcija SSU6', Akcija.Status.AKTIVNA, max_vol=2)
        self.url = reverse('prijavi_se', args=[self.akc.pk])

    def test_uspesna_prijava_2_2_1(self):
        """2.2.1 — volonter se uspešno prijavljuje; kreira se prijava na čekanju."""
        self.client.force_login(self.vol)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        p = Prijava.objects.get(korisnik=self.vol.volonter_profil, akcija=self.akc)
        self.assertEqual(p.status, Prijava.Status.NA_CEKANJU)

    def test_prijava_na_neotvorenu_nije_moguca_2_2_4(self):
        """2.2.4 — na popunjenu (neaktivnu) akciju prijava nije moguća."""
        self.akc.status = Akcija.Status.POPUNJENA
        self.akc.save()
        self.client.force_login(self.vol)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 400)
        self.assertFalse(Prijava.objects.filter(akcija=self.akc).exists())

    def test_dvostruka_prijava_ne_pravi_duplikat_2_2_5(self):
        """2.2.5 — ponovljena prijava ne pravi duplikat (jedna prijava po volonteru)."""
        self.client.force_login(self.vol)
        self.client.post(self.url)
        self.client.post(self.url)
        self.assertEqual(
            Prijava.objects.filter(korisnik=self.vol.volonter_profil, akcija=self.akc).count(),
            1,
        )

    def test_samo_volonter_moze_da_se_prijavi_403(self):
        """Sponzor (ne-volonter) ne može da se prijavi (403)."""
        spon = sponzor('sponzorstva.delta@gmail.com')
        self.client.force_login(spon)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 403)

    def test_neulogovan_preusmeren(self):
        """login_required — neulogovan korisnik se preusmerava (302)."""
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 302)

    def test_get_metoda_nije_dozvoljena_405(self):
        """require_POST — GET zahtev vraća 405."""
        self.client.force_login(self.vol)
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 405)


class OdjavaVolonteraTest(TestCase):
    def setUp(self):
        self.org = organizator('crvenikrst.bg@gmail.com')
        self.vol = volonter('marko.nikolic@gmail.com')
        self.akc = akcija(self.org, 'Akcija SSU6b', Akcija.Status.AKTIVNA)
        self.url = reverse('odjavi_se', args=[self.akc.pk])
        self.client.force_login(self.vol)

    def _prijava(self, status):
        return Prijava.objects.create(
            korisnik=self.vol.volonter_profil, akcija=self.akc, status=status,
        )

    def test_odjava_pre_potvrde_brise_prijavu_2_2_2(self):
        """2.2.2 — odjava prijave na čekanju je briše."""
        self._prijava(Prijava.Status.NA_CEKANJU)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Prijava.objects.filter(akcija=self.akc).exists())

    def test_odjava_posle_prihvatanja_brise_prijavu_2_2_3(self):
        """2.2.3 — odjava prihvaćene prijave je briše (oslobađa mesto)."""
        self._prijava(Prijava.Status.PRIHVACENA)
        self.client.post(self.url)
        self.assertFalse(Prijava.objects.filter(akcija=self.akc).exists())

    def test_odbijena_prijava_se_ne_moze_odjaviti(self):
        """Odbijena prijava je konačna — odjava je ne briše."""
        self._prijava(Prijava.Status.ODBIJENA)
        self.client.post(self.url)
        self.assertTrue(
            Prijava.objects.filter(akcija=self.akc, status=Prijava.Status.ODBIJENA).exists()
        )


class AkcijaSlobodnaMestaTest(TestCase):
    """Model ``Akcija`` — broj prihvaćenih i slobodna mesta (relevantno za SSU 6)."""

    def test_broj_prihvacenih_i_slobodna_mesta(self):
        org = organizator('vcns.info@gmail.com')
        akc = akcija(org, 'Akcija mesta', max_vol=3)
        v1 = volonter('ana.jovanovic@yahoo.com')
        v2 = volonter('stefan.ilic@outlook.com')
        Prijava.objects.create(korisnik=v1.volonter_profil, akcija=akc,
                               status=Prijava.Status.PRIHVACENA)
        Prijava.objects.create(korisnik=v2.volonter_profil, akcija=akc,
                               status=Prijava.Status.NA_CEKANJU)
        # Samo prihvaćeni se broje kao zauzeta mesta.
        self.assertEqual(akc.broj_prihvacenih, 1)
        self.assertEqual(akc.slobodna_mesta, 2)
