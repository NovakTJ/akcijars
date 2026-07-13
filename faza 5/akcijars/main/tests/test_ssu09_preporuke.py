# Autor: Novak Stijepic 0124/2023
"""
Jedinični testovi za SSU 9 — Slanje preporuka korisnicima.

Testira se Ajax kontroler ``toggle_preporuke``, generisanje preporučenih
akcija po lokaciji i slanje email preporuka; funkcionalnost je implementirala
Milica Milošević.
"""
import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.emails import posalji_preporuke
from main.models import Akcija, Prijava
from main.preporuke import generisi_preporuke
from ._helpers import volonter, organizator, akcija, prijava


BEOGRAD_CENTAR = (44.8125, 20.4612)
BEOGRAD_BLIZU = (44.82, 20.47)
BEOGRAD_JOS_BLIZE = (44.8130, 20.4612)
BEOGRAD_DALJE = (44.90, 20.55)
NIS = (43.32, 21.90)


def _postavi_koordinate(akc, sirina, duzina):
    akc.geo_sirina = sirina
    akc.geo_duzina = duzina
    akc.save(update_fields=['geo_sirina', 'geo_duzina'])
    return akc


class TogglePreporukeTest(TestCase):
    def setUp(self):
        self.vol = volonter('vol@akcija.rs')
        self.url = reverse('toggle_preporuke')

    def _post(self, prima_preporuke):
        return self.client.post(
            self.url, data=json.dumps({'prima_preporuke': prima_preporuke}),
            content_type='application/json',
        )

    def test_volonter_aktivira_preporuke_2_2_2(self):
        """2.2.2 — volonter uključuje primanje preporuka; saglasnost se beleži."""
        self.client.force_login(self.vol)
        r = self._post(True)
        self.vol.volonter_profil.refresh_from_db()
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])
        self.assertTrue(r.json()['prima_preporuke'])
        self.assertTrue(self.vol.volonter_profil.prima_preporuke)

    def test_volonter_deaktivira_preporuke_2_2_3(self):
        """2.2.3 — volonter isključuje primanje preporuka; promena se beleži."""
        self.vol.volonter_profil.prima_preporuke = True
        self.vol.volonter_profil.save(update_fields=['prima_preporuke'])
        self.client.force_login(self.vol)
        r = self._post(False)
        self.vol.volonter_profil.refresh_from_db()
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.json()['prima_preporuke'])
        self.assertFalse(self.vol.volonter_profil.prima_preporuke)

    def test_ne_volonter_403(self):
        """Samo volonteri smeju da menjaju podešavanje preporuka."""
        self.client.force_login(organizator('org@akcija.rs'))
        r = self._post(True)
        self.assertEqual(r.status_code, 403)

    def test_get_nije_dozvoljen_405(self):
        """require_POST — GET zahtev vraća 405."""
        self.client.force_login(self.vol)
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 405)

    def test_neispravan_json_400(self):
        """Neispravno JSON telo Ajax zahteva vraća 400."""
        self.client.force_login(self.vol)
        r = self.client.post(self.url, data='{', content_type='application/json')
        self.assertEqual(r.status_code, 400)

    def test_neprijavljen_korisnik_preusmeren(self):
        """login_required — neprijavljen korisnik se preusmerava na prijavu."""
        r = self._post(True)
        self.assertEqual(r.status_code, 302)


class GenerisiPreporukeTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.vol = volonter('vol@akcija.rs')
        self.profil = self.vol.volonter_profil

    def _akcija_sa_koordinatama(self, naziv, status=Akcija.Status.AKTIVNA, koordinate=BEOGRAD_BLIZU):
        akc = akcija(self.org, naziv, status=status)
        return _postavi_koordinate(akc, *koordinate)

    def _prethodna_prihvacena(self):
        prethodna = self._akcija_sa_koordinatama(
            'Prethodna akcija', Akcija.Status.ZAVRSENA, BEOGRAD_CENTAR,
        )
        prijava(self.vol, prethodna, status=Prijava.Status.PRIHVACENA)
        return prethodna

    def test_bez_prethodnih_prihvacenih_akcija_nema_preporuka_2_2_4(self):
        """2.2.4 — bez prethodnih prihvaćenih akcija sa koordinatama nema preporuka."""
        self._akcija_sa_koordinatama('Kandidat blizu')
        self.assertEqual(generisi_preporuke(self.profil), [])

    def test_bliska_aktivna_akcija_se_preporucuje_2_2_1(self):
        """2.2.1 — sistem predlaže aktivnu akciju blizu prethodnog učešća."""
        self._prethodna_prihvacena()
        kandidat = self._akcija_sa_koordinatama('Kandidat blizu', koordinate=BEOGRAD_BLIZU)
        preporuke = generisi_preporuke(self.profil)
        self.assertEqual(preporuke, [kandidat])
        self.assertTrue(hasattr(preporuke[0], 'distanca'))

    def test_udaljena_akcija_se_ne_preporucuje_2_2_3(self):
        """2.2.3 — akcija van zadatog radijusa ne ulazi u preporuke."""
        self._prethodna_prihvacena()
        self._akcija_sa_koordinatama('Kandidat Niš', koordinate=NIS)
        self.assertEqual(generisi_preporuke(self.profil, max_km=10), [])

    def test_vec_prijavljena_akcija_se_iskljucuje(self):
        """Akcija na koju se volonter već prijavio ne sme biti ponovo preporučena."""
        self._prethodna_prihvacena()
        kandidat = self._akcija_sa_koordinatama('Već prijavljena akcija')
        prijava(self.vol, kandidat, status=Prijava.Status.NA_CEKANJU)
        self.assertEqual(generisi_preporuke(self.profil), [])

    def test_neaktivna_akcija_se_iskljucuje(self):
        """Samo aktivne akcije mogu biti kandidati za preporuke."""
        self._prethodna_prihvacena()
        self._akcija_sa_koordinatama(
            'Završena akcija', status=Akcija.Status.ZAVRSENA, koordinate=BEOGRAD_BLIZU,
        )
        self.assertEqual(generisi_preporuke(self.profil), [])

    def test_rezultat_sortiran_po_distanci_i_ogranicen_limitom(self):
        """2.2.1 — preporuke su sortirane od najbliže i poštuju zadati limit."""
        self._prethodna_prihvacena()
        srednja = self._akcija_sa_koordinatama('Srednje blizu', koordinate=BEOGRAD_BLIZU)
        bliza = self._akcija_sa_koordinatama('Najbliža', koordinate=BEOGRAD_JOS_BLIZE)
        self._akcija_sa_koordinatama('Dalja', koordinate=BEOGRAD_DALJE)
        preporuke = generisi_preporuke(self.profil, limit=2)
        self.assertEqual(preporuke, [bliza, srednja])
        self.assertLessEqual(preporuke[0].distanca, preporuke[1].distanca)


class PosaljiPreporukeEmailTest(TestCase):
    def setUp(self):
        self.org = organizator('org@akcija.rs')
        self.vol = volonter('vol@akcija.rs')
        self.profil = self.vol.volonter_profil

    def test_prazna_lista_ne_salje_email_2_2_4(self):
        """2.2.4 — kada nema dostupnih preporuka, email se ne šalje."""
        poslato = posalji_preporuke(self.profil, [])
        self.assertEqual(poslato, 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_neprazna_lista_salje_jedan_email_2_2_1(self):
        """2.2.1 — sistem šalje jedan email sa preporučenim akcijama."""
        kandidat = akcija(self.org, 'Preporučena akcija', Akcija.Status.AKTIVNA)
        poslato = posalji_preporuke(self.profil, [kandidat])
        self.assertEqual(poslato, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.vol.email])
