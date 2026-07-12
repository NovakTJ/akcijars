# Autor: Milica Milošević 0357/2023
"""
Jedinični testovi za SSU 4 — Pregled i pretraga članaka.

Testira se kontroler ``lista_clanaka`` i ``detalj_clanka`` (funkcionalnost je
implementirala Maša Nikolić; Milica testira tuđu funkcionalnost — ukrštanje).
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Clanak
from ._helpers import organizator, clanak, kat_clanka


class ListaClanakaTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com', naziv='Zeleni Beograd')
        self.kat_eko = kat_clanka('Ekologija')
        self.kat_vesti = kat_clanka('Vesti')
        self.c1 = clanak(self.org, 'Čišćenje parka', kat=self.kat_eko)
        self.c2 = clanak(self.org, 'Sadnja drveća', kat=self.kat_vesti)
        self.c_cekanje = clanak(self.org, 'Neodobren tekst',
                                status=Clanak.Status.NA_CEKANJU, kat=self.kat_eko)

    def test_prikazuju_se_samo_objavljeni(self):
        """Članci na čekanju/odbijeni se ne prikazuju u javnoj listi."""
        r = self.client.get(reverse('clanci'))
        self.assertEqual(r.status_code, 200)
        clanci = list(r.context['clanci'])
        self.assertIn(self.c1, clanci)
        self.assertIn(self.c2, clanci)
        self.assertNotIn(self.c_cekanje, clanci)

    def test_pretraga_po_naslovu_2_2_2(self):
        """2.2.2 — pretraga po podstringu naslova."""
        r = self.client.get(reverse('clanci'), {'q': 'Sadnja'})
        self.assertEqual(list(r.context['clanci']), [self.c2])

    def test_pretraga_po_organizatoru_2_2_2(self):
        """2.2.2 — pretraga po nazivu organizatora vraća sve njegove članke."""
        r = self.client.get(reverse('clanci'), {'q': 'Zeleni'})
        self.assertEqual(len(r.context['clanci']), 2)

    def test_filter_po_kategoriji_2_2_3(self):
        """2.2.3 — filtriranje po izabranoj kategoriji."""
        r = self.client.get(reverse('clanci'), {'kategorija': self.kat_vesti.pk})
        self.assertEqual(list(r.context['clanci']), [self.c2])

    def test_kombinovana_pretraga_2_2_4(self):
        """2.2.4 — naziv + kategorija (logičko I)."""
        r = self.client.get(reverse('clanci'), {'q': 'Čišćenje', 'kategorija': self.kat_eko.pk})
        self.assertEqual(list(r.context['clanci']), [self.c1])

    def test_pretraga_bez_rezultata_2_2_6(self):
        """2.2.6 — nijedan članak ne zadovoljava kriterijume."""
        r = self.client.get(reverse('clanci'), {'q': 'nepostojecipojam'})
        self.assertEqual(len(r.context['clanci']), 0)

    def test_nedozvoljeni_karakteri_u_upitu_2_2_7(self):
        """2.2.7 — nedozvoljeni karakteri se odbijaju, upit se poništava."""
        r = self.client.get(reverse('clanci'), {'q': 'test@#$%'})
        self.assertEqual(
            r.context['greska_upita'],
            'U upitu su dozvoljeni samo slova, cifre i razmaci.',
        )
        self.assertEqual(r.context['filteri']['q'], '')

    def test_ajax_vraca_fragment(self):
        """Ajax zahtev vraća samo HTML fragment liste, ne celu stranu."""
        r = self.client.get(reverse('clanci'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed(r, '_clanci_grid.html')


class PaginacijaClanakaTest(TestCase):
    def test_najvise_9_po_strani_2_2_5(self):
        """2.2.5 — podrazumevano najviše 9 članaka po strani; ostatak na sledećoj."""
        org = organizator('vcns.info@gmail.com')
        kat = kat_clanka('Paginacija')
        for i in range(12):
            clanak(org, f'Članak broj {i}', kat=kat)
        r1 = self.client.get(reverse('clanci'))
        self.assertEqual(len(r1.context['clanci']), 9)
        r2 = self.client.get(reverse('clanci'), {'page': 2})
        self.assertEqual(len(r2.context['clanci']), 3)


class DetaljClankaTest(TestCase):
    def test_objavljen_clanak_prikazan_2_2_1(self):
        """2.2.1 — pun tekst objavljenog članka je dostupan."""
        org = organizator('crvenikrst.bg@gmail.com')
        c = clanak(org, 'Detaljni članak')
        r = self.client.get(reverse('detalj_clanka', args=[c.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['clanak'], c)

    def test_neobjavljen_clanak_nedostupan_404(self):
        """Članak koji nije objavljen ne sme biti dostupan preko direktnog linka."""
        org = organizator('ruka.prijateljstva@gmail.com')
        c = clanak(org, 'Skriveni članak', status=Clanak.Status.NA_CEKANJU)
        r = self.client.get(reverse('detalj_clanka', args=[c.pk]))
        self.assertEqual(r.status_code, 404)
