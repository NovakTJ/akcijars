# Autor: Novak Stijepic 0124/2023
"""
Jedinični testovi za SSU 3 — Pregled i pretraga akcija.

Testira se kontroler ``lista_akcija``: osnovni prikaz, pretraga, filteri,
sortiranje, geo-pretraga i paginacija. Funkcionalnost je implementirala
Maša Nikolić.
"""
import datetime

from django.test import TestCase
from django.urls import reverse

from main.models import Akcija
from ._helpers import organizator, akcija, kat_akcije


def _idjevi(odgovor):
    return [a.pk for a in odgovor.context['akcije']]


class AkcijePristupTest(TestCase):
    def test_osnovni_prikaz_stranice(self):
        """2.2 — stranica akcija vraća osnovni kontekst i šablon liste."""
        org = organizator('ssu3.pristup.org@akcija.rs')
        akc = akcija(org, 'Osnovna SSU3 akcija')

        r = self.client.get(reverse('akcije'))

        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'akcije.html')
        self.assertIn(akc.pk, _idjevi(r))
        for kljuc in ('akcije', 'strana', 'kategorije', 'statusi', 'filteri'):
            self.assertIn(kljuc, r.context)


class AkcijePretragaFilteriTest(TestCase):
    def setUp(self):
        self.url = reverse('akcije')
        self.org_bg = organizator('ssu3.bg.org@akcija.rs', naziv='Zeleni Beograd')
        self.org_ns = organizator('ssu3.ns.org@akcija.rs', naziv='Novosadski centar')
        self.eko = kat_akcije('SSU3 ekologija')
        self.hum = kat_akcije('SSU3 humanitarno')

    def test_pretraga_po_nazivu_2_2_2(self):
        """2.2.2 — upit po nazivu prikazuje poklapanje, a izbacuje ostale akcije."""
        pogodak = akcija(self.org_bg, 'Čišćenje parka Košutnjak', kat=self.eko)
        promasaj = akcija(self.org_bg, 'Podela paketa', kat=self.hum)

        r = self.client.get(self.url, {'q': 'Košutnjak'})

        self.assertIn(pogodak.pk, _idjevi(r))
        self.assertNotIn(promasaj.pk, _idjevi(r))
        self.assertEqual(r.context['filteri']['q'], 'Košutnjak')

    def test_pretraga_po_organizatoru_2_2_2(self):
        """2.2.2 — upit po nazivu organizatora nalazi njegove akcije."""
        pogodak = akcija(self.org_ns, 'Radionica reciklaže', kat=self.eko)
        promasaj = akcija(self.org_bg, 'Sadnja drveća', kat=self.eko)

        r = self.client.get(self.url, {'q': 'Novosadski'})

        self.assertIn(pogodak.pk, _idjevi(r))
        self.assertNotIn(promasaj.pk, _idjevi(r))

    def test_neispravan_upit_se_odbija_2_2_11(self):
        """2.2.11 — nedozvoljeni karakteri daju poruku i poništavaju tekst upita."""
        prva = akcija(self.org_bg, 'Prva vidljiva akcija', kat=self.eko)
        druga = akcija(self.org_ns, 'Druga vidljiva akcija', kat=self.hum)

        r = self.client.get(self.url, {'q': '@#$'})

        self.assertEqual(
            r.context['greska_upita'],
            'U upitu su dozvoljeni samo slova, cifre i razmaci.',
        )
        self.assertEqual(r.context['filteri']['q'], '')
        self.assertIn(prva.pk, _idjevi(r))
        self.assertIn(druga.pk, _idjevi(r))

    def test_filter_po_kategoriji_2_2_3(self):
        """2.2.3 — izbor kategorije sužava listu akcija."""
        pogodak = akcija(self.org_bg, 'Eko akcija', kat=self.eko)
        promasaj = akcija(self.org_bg, 'Humanitarna akcija', kat=self.hum)

        r = self.client.get(self.url, {'kategorija': self.eko.pk})

        self.assertIn(pogodak.pk, _idjevi(r))
        self.assertNotIn(promasaj.pk, _idjevi(r))
        self.assertEqual(r.context['filteri']['kategorija'], str(self.eko.pk))

    def test_filter_po_statusu_2_2_4(self):
        """2.2.4 — izbor statusa sužava listu akcija."""
        pogodak = akcija(self.org_bg, 'Popunjena akcija', Akcija.Status.POPUNJENA)
        promasaj = akcija(self.org_bg, 'Aktivna akcija', Akcija.Status.AKTIVNA)

        r = self.client.get(self.url, {'status': Akcija.Status.POPUNJENA})

        self.assertIn(pogodak.pk, _idjevi(r))
        self.assertNotIn(promasaj.pk, _idjevi(r))
        self.assertEqual(r.context['filteri']['status'], Akcija.Status.POPUNJENA)

    def test_filter_po_datumu_2_2_5(self):
        """2.2.5 — izbor datuma prikazuje samo akcije tog datuma održavanja."""
        trazeni_datum = datetime.date.today() + datetime.timedelta(days=20)
        drugi_datum = datetime.date.today() + datetime.timedelta(days=21)
        pogodak = akcija(self.org_bg, 'Akcija traženog datuma')
        pogodak.datum = trazeni_datum
        pogodak.save()
        promasaj = akcija(self.org_bg, 'Akcija drugog datuma')
        promasaj.datum = drugi_datum
        promasaj.save()

        r = self.client.get(self.url, {'datum': trazeni_datum.isoformat()})

        self.assertIn(pogodak.pk, _idjevi(r))
        self.assertNotIn(promasaj.pk, _idjevi(r))
        self.assertEqual(r.context['filteri']['datum'], trazeni_datum.isoformat())

    def test_sortiranja_rezultata_2_2_8(self):
        """2.2.8 — podržana su sortiranja po kačenju, održavanju i slobodnim mestima."""
        starija = akcija(self.org_bg, 'Starije okačena akcija', max_vol=2)
        novija = akcija(self.org_bg, 'Novije okačena akcija', max_vol=8)
        Akcija.objects.filter(pk=starija.pk).update(
            datum_kreiranja=datetime.date.today() - datetime.timedelta(days=2),
        )
        Akcija.objects.filter(pk=novija.pk).update(
            datum_kreiranja=datetime.date.today(),
        )

        r = self.client.get(self.url, {'sort': 'datum_kacenja'})
        self.assertEqual(r.context['sortiranje'], 'datum_kacenja')
        self.assertEqual(_idjevi(r)[0], novija.pk)

        starija.datum = datetime.date.today() + datetime.timedelta(days=5)
        starija.save()
        novija.datum = datetime.date.today() + datetime.timedelta(days=30)
        novija.save()
        r = self.client.get(self.url, {'sort': 'datum_odrzavanja'})
        self.assertEqual(r.context['sortiranje'], 'datum_odrzavanja')
        self.assertEqual(_idjevi(r)[0], novija.pk)

        r = self.client.get(self.url, {'sort': 'slobodna_mesta'})
        self.assertEqual(r.context['sortiranje'], 'slobodna_mesta')
        self.assertEqual(_idjevi(r)[0], novija.pk)


class AkcijeLokacijaTest(TestCase):
    def setUp(self):
        self.url = reverse('akcije')
        self.org = organizator('ssu3.lokacija.org@akcija.rs')

    def _sa_koordinatama(self, naziv, sirina, duzina):
        a = akcija(self.org, naziv)
        a.geo_sirina = sirina
        a.geo_duzina = duzina
        a.save()
        return a

    def test_pretraga_po_lokaciji_2_2_6(self):
        """2.2.6 — geo-pretraga zadržava samo akcije unutar izabranog radijusa."""
        blizu = self._sa_koordinatama('Akcija u Beogradu', 44.8125, 20.4612)
        daleko = self._sa_koordinatama('Akcija u Nišu', 43.3209, 21.8958)
        bez_koordinata = akcija(self.org, 'Akcija bez koordinata')

        r = self.client.get(self.url, {
            'lat': '44.8125', 'lng': '20.4612', 'radius': '10',
        })

        self.assertTrue(r.context['lokacija_aktivna'])
        self.assertEqual(r.context['filteri']['radius'], 10)
        self.assertIn(blizu.pk, _idjevi(r))
        self.assertNotIn(daleko.pk, _idjevi(r))
        self.assertNotIn(bez_koordinata.pk, _idjevi(r))

    def test_nevalidan_radijus_podrazumeva_25_km_2_2_6(self):
        """2.2.6 — nevalidan radijus se menja podrazumevanim radijusom od 25 km."""
        blizu = self._sa_koordinatama('Akcija blizu centra', 44.8230, 20.4500)

        r = self.client.get(self.url, {
            'lat': '44.8125', 'lng': '20.4612', 'radius': '999',
        })

        self.assertEqual(r.context['filteri']['radius'], 25)
        self.assertIn(blizu.pk, _idjevi(r))

    def test_sortiranje_po_najblizim_akcijama_2_2_8(self):
        """2.2.8 — uz aktivnu lokaciju sortiranje „najbliže” ide po distanci."""
        dalja = self._sa_koordinatama('Zemun akcija', 44.8450, 20.4100)
        bliza = self._sa_koordinatama('Centar akcija', 44.8130, 20.4620)

        r = self.client.get(self.url, {
            'lat': '44.8125', 'lng': '20.4612', 'radius': '25', 'sort': 'najblize',
        })

        self.assertEqual(r.context['sortiranje'], 'najblize')
        self.assertEqual(_idjevi(r)[:2], [bliza.pk, dalja.pk])
        self.assertLess(r.context['akcije'][0].distanca, r.context['akcije'][1].distanca)


class AkcijePaginacijaTest(TestCase):
    def test_paginacija_prikazuje_devet_po_strani_2_2_9(self):
        """2.2.9 — lista prikazuje 9 akcija na prvoj i ostatak na drugoj strani."""
        org = organizator('ssu3.paginacija.org@akcija.rs')
        for i in range(11):
            akcija(org, f'Paginirana akcija {i}')

        r1 = self.client.get(reverse('akcije'))
        r2 = self.client.get(reverse('akcije'), {'page': '2'})

        self.assertEqual(len(r1.context['strana'].object_list), 9)
        self.assertEqual(len(r2.context['strana'].object_list), 2)
        self.assertEqual(r1.context['strana'].number, 1)
        self.assertEqual(r2.context['strana'].number, 2)

