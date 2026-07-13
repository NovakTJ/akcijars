# Autor: Novak Stijepic 0124/2023
"""
Jedinični testovi za SSU 16 — Praćenje učešća sponzora.

Testira se kontroler ``sponzor_panel`` (prihvaćene ponude, ponude na čekanju,
odbijene ponude i ukupan doprinos) — funkcionalnost je implementirao
Stefan Grujičić.
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, SponzorProfil, SponzorskaPonuda
from ._helpers import akcija, organizator, ponuda, sponzor, volonter


class SponzorPanelPristupTest(TestCase):
    def test_sponzor_vidi_panel(self):
        """2.4 — prijavljeni sponzor uspešno otvara svoj panel."""
        self.client.force_login(
            sponzor('spon@akcija.rs', status=SponzorProfil.Status.ODOBREN)
        )
        r = self.client.get(reverse('sponzor_panel'))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'sponzor_panel.html')

    def test_volonter_preusmeren_na_home(self):
        """2.4 — volonter nije sponzor i preusmerava se na početnu stranu."""
        self.client.force_login(volonter('vol@akcija.rs'))
        r = self.client.get(reverse('sponzor_panel'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('home'))

    def test_organizator_preusmeren_na_home(self):
        """2.4 — organizator nije sponzor i preusmerava se na početnu stranu."""
        self.client.force_login(organizator('org@akcija.rs'))
        r = self.client.get(reverse('sponzor_panel'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('home'))

    def test_neulogovan_preusmeren_na_prijavu(self):
        """2.4 — neulogovan korisnik se preusmerava login_required pravilom."""
        r = self.client.get(reverse('sponzor_panel'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)


class SponzorPanelSadrzajTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.spon = sponzor('spon@akcija.rs')
        self.client.force_login(self.spon)
        self.url = reverse('sponzor_panel')

    def test_prazan_panel_2_2_3(self):
        """2.2.3 — sponzor bez ponuda vidi prazne liste i sve nule."""
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_prihvacenih'], 0)
        self.assertEqual(r.context['br_na_cekanju'], 0)
        self.assertEqual(r.context['br_odbijenih'], 0)
        self.assertEqual(r.context['ukupan_doprinos'], 0)
        self.assertEqual(r.context['ponude_prihvacene'].count(), 0)
        self.assertEqual(r.context['ponude_na_cekanju'].count(), 0)
        self.assertEqual(r.context['ponude_odbijene'].count(), 0)

    def test_prihvacena_ponuda_2_2_1(self):
        """2.2.1 — prihvaćena ponuda ulazi u istoriju i ukupan doprinos."""
        akc = akcija(self.org, 'Prihvaćena akcija', Akcija.Status.AKTIVNA)
        p = ponuda(
            self.spon, akc, vrednost=700,
            status=SponzorskaPonuda.Status.PRIHVACENA
        )
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_prihvacenih'], 1)
        self.assertEqual(r.context['ukupan_doprinos'], 700)
        self.assertEqual(list(r.context['ponude_prihvacene']), [p])

    def test_ponuda_na_cekanju_2_2_2(self):
        """2.2.2 — ponuda na čekanju je u posebnoj listi i brojaču."""
        akc = akcija(self.org, 'Akcija na čekanju', Akcija.Status.AKTIVNA)
        p = ponuda(
            self.spon, akc, vrednost=500,
            status=SponzorskaPonuda.Status.NA_CEKANJU
        )
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_na_cekanju'], 1)
        self.assertEqual(r.context['ukupan_doprinos'], 0)
        self.assertEqual(list(r.context['ponude_na_cekanju']), [p])

    def test_odbijena_ponuda_u_odbijenim(self):
        """Odbijena ponuda je u posebnoj listi i ne ulazi u doprinos."""
        akc = akcija(self.org, 'Odbijena akcija', Akcija.Status.AKTIVNA)
        p = ponuda(
            self.spon, akc, vrednost=400,
            status=SponzorskaPonuda.Status.ODBIJENA
        )
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_odbijenih'], 1)
        self.assertEqual(r.context['ukupan_doprinos'], 0)
        self.assertEqual(list(r.context['ponude_odbijene']), [p])

    def test_doprinos_racuna_samo_prihvacene_2_2_1_i_2_2_2(self):
        """2.2.1/2.2.2 — na čekanju i odbijene ponude ne ulaze u zbir doprinosa."""
        a1 = akcija(self.org, 'Prihvaćena', Akcija.Status.AKTIVNA)
        a2 = akcija(self.org, 'Na čekanju', Akcija.Status.AKTIVNA)
        a3 = akcija(self.org, 'Odbijena', Akcija.Status.AKTIVNA)
        ponuda(self.spon, a1, vrednost=1000, status=SponzorskaPonuda.Status.PRIHVACENA)
        ponuda(self.spon, a2, vrednost=800, status=SponzorskaPonuda.Status.NA_CEKANJU)
        ponuda(self.spon, a3, vrednost=600, status=SponzorskaPonuda.Status.ODBIJENA)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_prihvacenih'], 1)
        self.assertEqual(r.context['br_na_cekanju'], 1)
        self.assertEqual(r.context['br_odbijenih'], 1)
        self.assertEqual(r.context['ukupan_doprinos'], 1000)

    def test_vise_prihvacenih_se_sabira_2_2_1(self):
        """2.2.1 — ukupan doprinos je zbir svih prihvaćenih ponuda."""
        a1 = akcija(self.org, 'A1', Akcija.Status.AKTIVNA)
        a2 = akcija(self.org, 'A2', Akcija.Status.AKTIVNA)
        ponuda(self.spon, a1, vrednost=300, status=SponzorskaPonuda.Status.PRIHVACENA)
        ponuda(self.spon, a2, vrednost=450, status=SponzorskaPonuda.Status.PRIHVACENA)
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_prihvacenih'], 2)
        self.assertEqual(r.context['ukupan_doprinos'], 750)

    def test_vidi_samo_svoje_ponude(self):
        """Sponzor u panelu vidi samo svoje ponude, ne ponude drugih sponzora."""
        drugi = sponzor('drugi@akcija.rs')
        a1 = akcija(self.org, 'Moja akcija', Akcija.Status.AKTIVNA)
        a2 = akcija(self.org, 'Tuđa akcija', Akcija.Status.AKTIVNA)
        moja = ponuda(
            self.spon, a1, vrednost=200,
            status=SponzorskaPonuda.Status.PRIHVACENA
        )
        tudja = ponuda(
            drugi, a2, vrednost=900,
            status=SponzorskaPonuda.Status.PRIHVACENA
        )
        r = self.client.get(self.url)
        self.assertEqual(r.context['br_prihvacenih'], 1)
        self.assertEqual(r.context['ukupan_doprinos'], 200)
        self.assertEqual(list(r.context['ponude_prihvacene']), [moja])
        self.assertNotIn(tudja, list(r.context['ponude_prihvacene']))
