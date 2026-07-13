# Autor: Maša Nikolić 2023/0089
"""
Jedinični testovi za SSU 13 — Upravljanje korisničkim nalozima.

Testira se admin kontrolna tabla ``admin_panel`` i Ajax kontroleri
``ajax_odobri_nalog`` / ``ajax_odbij_nalog`` / ``ajax_ukloni_korisnika``
(funkcionalnost je implementirao Stefan Grujičić — ukrštanje).
"""
import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import Korisnik, OrganizatorProfil, SponzorProfil
from ._helpers import administrator, organizator, sponzor, volonter


class AdminPanelPristupTest(TestCase):
    def test_admin_vidi_panel(self):
        """Administrator uspešno otvara kontrolnu tablu."""
        self.client.force_login(administrator('admin@akcija.rs'))
        r = self.client.get(reverse('admin_panel'))
        self.assertEqual(r.status_code, 200)

    def test_ne_admin_preusmeren(self):
        """Ne-admin (volonter) se preusmerava sa admin panela."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self.client.get(reverse('admin_panel'))
        self.assertEqual(r.status_code, 302)


class OdobriNalogTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_odobri_nalog')
        self.org = organizator('org@akcija.rs', status=OrganizatorProfil.Status.NA_CEKANJU)

    def _post(self, korisnik_id):
        return self.client.post(
            self.url, data=json.dumps({'korisnik_id': korisnik_id}),
            content_type='application/json',
        )

    def test_odobrenje_organizatora_2_2_1(self):
        """2.2.1 — admin odobrava organizatora na čekanju; status prelazi u „odobren", šalje se email."""
        r = self._post(self.org.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertEqual(
            OrganizatorProfil.objects.get(korisnik=self.org).status,
            OrganizatorProfil.Status.ODOBREN,
        )
        self.assertEqual(len(mail.outbox), 1)  # 2.2.1 korak 7 — email
        # Posledica 2.5 — odobren korisnik može da pristupi sistemu.
        self.assertTrue(Korisnik.objects.get(pk=self.org.pk).je_odobren)

    def test_odobrenje_sponzora(self):
        """Admin odobrava i sponzora na čekanju."""
        spon = sponzor('spon@akcija.rs', status=SponzorProfil.Status.NA_CEKANJU)
        self._post(spon.pk)
        self.assertEqual(
            SponzorProfil.objects.get(korisnik=spon).status,
            SponzorProfil.Status.ODOBREN,
        )

    def test_vec_odobren_nalog_400(self):
        """Nalog koji nije na čekanju (već odobren) ne može ponovo da se odobri."""
        already = organizator('org2@akcija.rs')  # helper podrazumevano ODOBREN
        r = self._post(already.pk)
        self.assertEqual(r.status_code, 400)

    def test_nepostojeci_korisnik_404(self):
        """Nepostojeći korisnik → 404."""
        self.assertEqual(self._post(999999).status_code, 404)

    def test_ne_admin_403(self):
        """Ne-admin ne sme da odobrava naloge → 403."""
        self.client.force_login(volonter('vol@akcija.rs'))
        self.assertEqual(self._post(self.org.pk).status_code, 403)

    def test_get_nije_dozvoljen_405(self):
        """require_POST — GET zahtev vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)


class OdbijNalogTest(TestCase):
    def setUp(self):
        self.client.force_login(administrator('admin@akcija.rs'))
        self.url = reverse('ajax_odbij_nalog')
        self.org = organizator('org@akcija.rs', status=OrganizatorProfil.Status.NA_CEKANJU)

    def test_odbijanje_organizatora_2_2_2(self):
        """2.2.2 — admin odbija zahtev; status prelazi u „odbijen"."""
        r = self.client.post(
            self.url, data=json.dumps({'korisnik_id': self.org.pk}),
            content_type='application/json',
        )
        self.assertTrue(r.json()['success'])
        self.assertEqual(
            OrganizatorProfil.objects.get(korisnik=self.org).status,
            OrganizatorProfil.Status.ODBIJEN,
        )
        self.assertEqual(len(mail.outbox), 1)  # 2.2.2 korak 7 — email o odbijanju
        # Posledica 2.5 — odbijen nalog ostaje neaktivan.
        self.assertFalse(Korisnik.objects.get(pk=self.org.pk).je_odobren)


class UkloniKorisnikaTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_ukloni_korisnika')

    def _post(self, korisnik_id):
        return self.client.post(
            self.url, data=json.dumps({'korisnik_id': korisnik_id}),
            content_type='application/json',
        )

    def test_uklanjanje_korisnika_2_2_3(self):
        """2.2.3 — admin uklanja nalog korisnika; korisnik se briše iz baze."""
        vol = volonter('vol@akcija.rs')
        r = self._post(vol.pk)
        self.assertTrue(r.json()['success'])
        self.assertFalse(Korisnik.objects.filter(pk=vol.pk).exists())

    def test_admin_ne_moze_sam_sebe(self):
        """Admin ne može da ukloni sopstveni nalog → 400, nalog ostaje."""
        r = self._post(self.admin.pk)
        self.assertEqual(r.status_code, 400)
        self.assertTrue(Korisnik.objects.filter(pk=self.admin.pk).exists())

    def test_ne_admin_403(self):
        """Ne-admin ne sme da uklanja naloge → 403, nalog ostaje."""
        self.client.force_login(volonter('napadac@akcija.rs'))
        meta = volonter('meta@akcija.rs')
        r = self._post(meta.pk)
        self.assertEqual(r.status_code, 403)
        self.assertTrue(Korisnik.objects.filter(pk=meta.pk).exists())
