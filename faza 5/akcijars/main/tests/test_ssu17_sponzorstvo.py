# Autor: Maša Nikolić 2023/0089
"""
Jedinični testovi za SSU 17 — Potvrđivanje i odbijanje sponzorstva.

Testiraju se kontroleri ``prihvati_ponudu`` / ``odbij_ponudu``
(funkcionalnost je implementirao Stefan Grujičić — ukrštanje).

Očekivano ponašanje je preuzeto iz SSU 17. Testovi email obaveštenja
(2.2.1 korak 8 i 2.2.2 korak 7) su CRVENI dok se ne implementira slanje
mejla sponzoru — odstupanje koda od specifikacije, prijavljeno kolegi.
"""
import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import SponzorskaPonuda
from ._helpers import organizator, sponzor, akcija, ponuda


class PrihvatiPonuduTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.spon = sponzor('spon@akcija.rs')
        self.akc = akcija(self.org, 'Akcija SSU17')
        self.pon = ponuda(self.spon, self.akc)
        self.client.force_login(self.org)
        self.url = reverse('prihvati_ponudu', args=[self.akc.pk, self.pon.pk])

    def test_prihvatanje_menja_status_2_2_1(self):
        """2.2.1 — organizator prihvata ponudu; status prelazi u „prihvaćena"."""
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            SponzorskaPonuda.objects.get(pk=self.pon.pk).status,
            SponzorskaPonuda.Status.PRIHVACENA,
        )

    def test_prihvatanje_salje_email_2_2_1(self):
        """2.2.1 korak 8 — sponzor dobija email da je ponuda prihvaćena. [CRVENO — email nije implementiran]"""
        self.client.post(self.url)
        self.assertEqual(len(mail.outbox), 1)

    def test_samo_organizator_akcije_403(self):
        """Drugi organizator (ne vlasnik akcije) ne može da obrađuje ponude → 403."""
        drugi = organizator('drugi@akcija.rs')
        self.client.force_login(drugi)
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_vec_obradjena_ponuda_400(self):
        """Već obrađena ponuda ne može ponovo → 400."""
        self.pon.status = SponzorskaPonuda.Status.PRIHVACENA
        self.pon.save()
        self.assertEqual(self.client.post(self.url).status_code, 400)

    def test_nepostojeca_ponuda_404(self):
        """Nepostojeća ponuda → 404."""
        url = reverse('prihvati_ponudu', args=[self.akc.pk, 999999])
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_get_nije_dozvoljen_405(self):
        """require_POST — GET vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)


class OdbijPonuduTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.spon = sponzor('spon@akcija.rs')
        self.akc = akcija(self.org, 'Akcija SSU17')
        self.pon = ponuda(self.spon, self.akc)
        self.client.force_login(self.org)
        self.url = reverse('odbij_ponudu', args=[self.akc.pk, self.pon.pk])

    def test_odbijanje_menja_status_2_2_2(self):
        """2.2.2 — organizator odbija ponudu; status prelazi u „odbijena" (van liste aktivnih)."""
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            SponzorskaPonuda.objects.get(pk=self.pon.pk).status,
            SponzorskaPonuda.Status.ODBIJENA,
        )

    def test_odbijanje_salje_email_2_2_2(self):
        """2.2.2 korak 7 — sponzor dobija email da ponuda nije prihvaćena. [CRVENO — email nije implementiran]"""
        self.client.post(self.url)
        self.assertEqual(len(mail.outbox), 1)
