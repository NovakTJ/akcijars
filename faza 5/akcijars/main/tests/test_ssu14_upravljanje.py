# Autor: Novak Stijepic 0124/2023
"""
Jedinični testovi za SSU 14 — Upravljanje akcijama i člancima.

Testiraju se Ajax kontroleri ``ajax_odobri_akciju`` / ``ajax_obrisi_akciju`` /
``ajax_odobri_clanak`` / ``ajax_obrisi_clanak`` (funkcionalnost je
implementirao Stefan Grujičić — ukrštanje).
"""
import json

from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, Clanak
from ._helpers import administrator, akcija, clanak, organizator, volonter


class OdobriAkcijaTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_odobri_akciju')
        self.org = organizator('org@akcija.rs')
        self.akcija = akcija(self.org, 'Akcija na čekanju', Akcija.Status.NA_CEKANJU)

    def _post(self, akcija_id):
        return self.client.post(
            self.url, data=json.dumps({'akcija_id': akcija_id}),
            content_type='application/json',
        )

    def test_odobravanje_akcije_2_2_1(self):
        """2.2.1 — admin odobrava akciju na čekanju; status prelazi u „odobrena"."""
        r = self._post(self.akcija.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertEqual(
            Akcija.objects.get(pk=self.akcija.pk).status,
            Akcija.Status.ODOBRENA,
        )

    def test_akcija_koja_nije_na_cekanju_400_i_nepostojeca_404(self):
        """2.2.1 — samo akcije na čekanju mogu da se odobre; nepostojeća akcija vraća 404."""
        vec_odobrena = akcija(self.org, 'Već odobrena', Akcija.Status.ODOBRENA)
        self.assertEqual(self._post(vec_odobrena.pk).status_code, 400)
        self.assertEqual(self._post(999999).status_code, 404)

    def test_ne_admin_403(self):
        """2.4 — ne-admin ne sme da odobrava akcije → 403."""
        self.client.force_login(volonter('vol@akcija.rs'))
        self.assertEqual(self._post(self.akcija.pk).status_code, 403)

    def test_get_nije_dozvoljen_405(self):
        """2.2.1 — odobravanje se radi POST zahtevom; GET vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)


class ObrisiAkcijaTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_obrisi_akciju')
        self.org = organizator('org@akcija.rs')
        self.akcija = akcija(self.org, 'Akcija za brisanje', Akcija.Status.NA_CEKANJU)

    def _post(self, akcija_id):
        return self.client.post(
            self.url, data=json.dumps({'akcija_id': akcija_id}),
            content_type='application/json',
        )

    def test_brisanje_akcije_2_2_2(self):
        """2.2.2 — admin briše akciju na čekanju; akcija se uklanja iz baze."""
        r = self._post(self.akcija.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertFalse(Akcija.objects.filter(pk=self.akcija.pk).exists())

    def test_akcija_koja_nije_na_cekanju_404_i_nepostojeca_404(self):
        """2.2.2 — za brisanje se pronalaze samo akcije na čekanju; nepostojeća akcija vraća 404."""
        aktivna = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        self.assertEqual(self._post(aktivna.pk).status_code, 404)
        self.assertTrue(Akcija.objects.filter(pk=aktivna.pk).exists())
        self.assertEqual(self._post(999999).status_code, 404)

    def test_ne_admin_403(self):
        """2.4 — ne-admin ne sme da briše akcije → 403, akcija ostaje."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self._post(self.akcija.pk)
        self.assertEqual(r.status_code, 403)
        self.assertTrue(Akcija.objects.filter(pk=self.akcija.pk).exists())

    def test_get_nije_dozvoljen_405(self):
        """2.2.2 — brisanje se radi POST zahtevom; GET vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)


class OdobriClanakTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_odobri_clanak')
        self.org = organizator('org@akcija.rs')
        self.clanak = clanak(self.org, 'Članak na čekanju', Clanak.Status.NA_CEKANJU)

    def _post(self, clanak_id):
        return self.client.post(
            self.url, data=json.dumps({'clanak_id': clanak_id}),
            content_type='application/json',
        )

    def test_odobravanje_clanka_2_2_4(self):
        """2.2.4 — admin odobrava članak na čekanju; status prelazi u „objavljen"."""
        r = self._post(self.clanak.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertEqual(
            Clanak.objects.get(pk=self.clanak.pk).status,
            Clanak.Status.OBJAVLJEN,
        )

    def test_clanak_koji_nije_na_cekanju_400_i_nepostojeci_404(self):
        """2.2.4 — samo članci na čekanju mogu da se odobre; nepostojeći članak vraća 404."""
        vec_objavljen = clanak(self.org, 'Već objavljen', Clanak.Status.OBJAVLJEN)
        self.assertEqual(self._post(vec_objavljen.pk).status_code, 400)
        self.assertEqual(self._post(999999).status_code, 404)

    def test_ne_admin_403(self):
        """2.4 — ne-admin ne sme da odobrava članke → 403."""
        self.client.force_login(volonter('vol@akcija.rs'))
        self.assertEqual(self._post(self.clanak.pk).status_code, 403)

    def test_get_nije_dozvoljen_405(self):
        """2.2.4 — odobravanje se radi POST zahtevom; GET vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)


class ObrisiClanakTest(TestCase):
    def setUp(self):
        self.admin = administrator('admin@akcija.rs')
        self.client.force_login(self.admin)
        self.url = reverse('ajax_obrisi_clanak')
        self.org = organizator('org@akcija.rs')
        self.clanak = clanak(self.org, 'Članak za brisanje', Clanak.Status.NA_CEKANJU)

    def _post(self, clanak_id):
        return self.client.post(
            self.url, data=json.dumps({'clanak_id': clanak_id}),
            content_type='application/json',
        )

    def test_brisanje_clanka_2_2_5(self):
        """2.2.5 — admin briše članak na čekanju; članak se uklanja iz baze."""
        r = self._post(self.clanak.pk)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertFalse(Clanak.objects.filter(pk=self.clanak.pk).exists())

    def test_clanak_koji_nije_na_cekanju_404_i_nepostojeci_404(self):
        """2.2.5 — za brisanje se pronalaze samo članci na čekanju; nepostojeći članak vraća 404."""
        objavljen = clanak(self.org, 'Objavljen članak', Clanak.Status.OBJAVLJEN)
        self.assertEqual(self._post(objavljen.pk).status_code, 404)
        self.assertTrue(Clanak.objects.filter(pk=objavljen.pk).exists())
        self.assertEqual(self._post(999999).status_code, 404)

    def test_ne_admin_403(self):
        """2.4 — ne-admin ne sme da briše članke → 403, članak ostaje."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self._post(self.clanak.pk)
        self.assertEqual(r.status_code, 403)
        self.assertTrue(Clanak.objects.filter(pk=self.clanak.pk).exists())

    def test_get_nije_dozvoljen_405(self):
        """2.2.5 — brisanje se radi POST zahtevom; GET vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)
