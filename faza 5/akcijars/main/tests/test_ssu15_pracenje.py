# Autor: Maša Nikolić 2023/0089
"""
Jedinični testovi za SSU 15 — Praćenje učešća volontera.

Testira se kontroler ``volonter_panel`` (tekuće prijave, istorija učešća i
ukupan broj volonterskih sati) — funkcionalnost je implementirao
Stefan Grujičić (ukrštanje).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, Prijava
from ._helpers import volonter, organizator, akcija, prijava


class VolonterPanelPristupTest(TestCase):
    def test_volonter_vidi_panel(self):
        """Volonter uspešno otvara svoj panel."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self.client.get(reverse('volonter_panel'))
        self.assertEqual(r.status_code, 200)

    def test_ne_volonter_preusmeren(self):
        """Ne-volonter (organizator) se preusmerava sa volonterskog panela."""
        self.client.force_login(organizator('org@akcija.rs'))
        r = self.client.get(reverse('volonter_panel'))
        self.assertEqual(r.status_code, 302)


class VolonterPanelSadrzajTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.vol = volonter('vol@akcija.rs')
        self.client.force_login(self.vol)
        self.url = reverse('volonter_panel')

    def test_prazan_panel_2_2_3(self):
        """2.2.3 — volonter bez učešća: sve nule."""
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_tekucih'], 0)
        self.assertEqual(r.context['br_istorija'], 0)
        self.assertEqual(r.context['ukupno_sati'], 0)

    def test_tekuca_prijava_2_2_2(self):
        """2.2.2 — prijava na aktivnu akciju (na čekanju) je među tekućima, ne u istoriji."""
        akc = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        prijava(self.vol, akc, status=Prijava.Status.NA_CEKANJU)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_tekucih'], 1)
        self.assertEqual(r.context['br_na_cekanju'], 1)
        self.assertEqual(r.context['br_istorija'], 0)

    def test_zavrsena_akcija_u_istoriji_2_2_1(self):
        """2.2.1 — prihvaćena prijava na završenu akciju ide u istoriju, ne u tekuće."""
        akc = akcija(self.org, 'Zavrsena akcija', Akcija.Status.ZAVRSENA)
        prijava(self.vol, akc, status=Prijava.Status.PRIHVACENA, br_sati=5)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_istorija'], 1)
        self.assertEqual(r.context['br_tekucih'], 0)

    def test_ukupno_sati_je_zbir_prihvacenih_2_2_1(self):
        """2.2.1 — ukupan broj sati je zbir sati prihvaćenih prijava."""
        a1 = akcija(self.org, 'A1', Akcija.Status.ZAVRSENA)
        a2 = akcija(self.org, 'A2', Akcija.Status.ZAVRSENA)
        prijava(self.vol, a1, status=Prijava.Status.PRIHVACENA, br_sati=4)
        prijava(self.vol, a2, status=Prijava.Status.PRIHVACENA, br_sati=6)
        r = self.client.get(self.url)
        self.assertEqual(r.context['ukupno_sati'], 10)

    def test_sati_ne_racunaju_prijave_na_cekanju(self):
        """Prijava na čekanju ne doprinosi ukupnom broju sati."""
        akc = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        prijava(self.vol, akc, status=Prijava.Status.NA_CEKANJU, br_sati=9)
        r = self.client.get(self.url)
        self.assertEqual(r.context['ukupno_sati'], 0)

    def test_odbijena_prijava_u_istoriji(self):
        """Odbijena prijava pripada istoriji, ne tekućim."""
        akc = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        prijava(self.vol, akc, status=Prijava.Status.ODBIJENA)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_istorija'], 1)
        self.assertEqual(r.context['br_tekucih'], 0)

    def test_vidi_samo_svoje_prijave(self):
        """Volonter u panelu vidi samo svoje prijave, ne tuđe."""
        drugi = volonter('drugi@akcija.rs')
        akc = akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        prijava(drugi, akc, status=Prijava.Status.NA_CEKANJU)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_tekucih'], 0)
