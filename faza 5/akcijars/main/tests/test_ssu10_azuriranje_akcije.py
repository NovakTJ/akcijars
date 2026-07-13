# Autor: Stefan Grujičić 0030/2023
"""
Jedinični testovi za SSU 10 — Ažuriranje i otkazivanje akcije.

Testira se kontroler ``izmeni_akciju``/``otkazi_akciju`` i forma ``AkcijaForm``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).

Google Maps je isključen (``GOOGLE_MAPS_API_KEY=''``) da izbor lokacije preko
mape ne bude obavezan u testu.
"""
import datetime

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from main.models import Akcija, Prijava
from ._helpers import organizator, volonter, akcija, prijava


@override_settings(GOOGLE_MAPS_API_KEY='')
class AzuriranjeAkcijeTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.akc = akcija(self.org, 'Originalna akcija', max_vol=10)
        self.url = reverse('izmeni_akciju', args=[self.akc.pk])
        self.client.force_login(self.org)

    def _podaci(self, **izmene):
        """Vraća validne podatke za izmenu akcije; ``izmene`` prepisuju polja."""
        podaci = {
            'naziv': 'Izmenjena akcija',
            'opis': 'Izmenjen opis akcije.',
            'datum': (timezone.localdate() + datetime.timedelta(days=15)).isoformat(),
            'vreme': '10:00',
            'lokacija': 'Kalemegdan, Beograd',
            'kategorija': self.akc.kategorija_id,
            'max_br_volontera': 10,
            'kontakt_email': 'novi.kontakt@zeleni.rs',
            'kontakt_telefon': '060 999 999',
        }
        podaci.update(izmene)
        return podaci

    def test_uspesno_azuriranje_2_2_1(self):
        """2.2.1 — izmene se čuvaju i prijavljeni volonteri se obaveštavaju emailom."""
        vol = volonter('vol@gmail.com')
        prijava(vol, self.akc, status=Prijava.Status.PRIHVACENA)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.context['izmena_uspeh'])
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.naziv, 'Izmenjena akcija')
        self.assertEqual(self.akc.kontakt_email, 'novi.kontakt@zeleni.rs')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['vol@gmail.com'])

    def test_prazna_obavezna_polja_2_2_2(self):
        """2.2.2 — nepopunjena obavezna polja: jedinstvena poruka, izmene se ne čuvaju."""
        r = self.client.post(self.url, {'kategorija': self.akc.kategorija_id})
        self.assertIn(
            'Nisu uneta sva obavezna polja.',
            r.context['izmeni_forma'].non_field_errors(),
        )
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.naziv, 'Originalna akcija')

    def test_datum_u_proslosti_2_2_3(self):
        """2.2.3 — datum održavanja u prošlosti se odbija."""
        r = self.client.post(self.url, self._podaci(
            datum=(timezone.localdate() - datetime.timedelta(days=1)).isoformat(),
        ))
        self.assertIn(
            'Datum održavanja akcije ne sme biti u prošlosti.',
            r.context['izmeni_forma'].errors['datum'],
        )

    def test_nevalidan_broj_volontera_2_2_4(self):
        """2.2.4 — nevalidan (0 ili negativan) maksimalan broj volontera se odbija."""
        r = self.client.post(self.url, self._podaci(max_br_volontera=0))
        self.assertIn(
            'Maksimalan broj volontera mora biti pozitivan broj.',
            r.context['izmeni_forma'].errors['max_br_volontera'],
        )

    def test_max_manji_od_prihvacenih_2_2_5(self):
        """2.2.5 — novi maksimum ne sme biti manji od broja već prihvaćenih volontera."""
        for i in range(3):
            vol = volonter(f'vol{i}@gmail.com')
            prijava(vol, self.akc, status=Prijava.Status.PRIHVACENA)
        r = self.client.post(self.url, self._podaci(max_br_volontera=2))
        self.assertIn(
            'Maksimalan broj volontera ne može biti manji od broja već '
            'prihvaćenih volontera.',
            r.context['izmeni_forma'].errors['max_br_volontera'],
        )

    def test_neispravan_email_2_2_6(self):
        """2.2.6 — neispravan format kontakt email adrese se odbija."""
        r = self.client.post(self.url, self._podaci(kontakt_email='nije-email'))
        self.assertIn(
            'Kontakt email nije ispravnog formata.',
            r.context['izmeni_forma'].errors['kontakt_email'],
        )

    def test_neispravan_telefon_2_2_7(self):
        """2.2.7 — neispravan format kontakt telefona se odbija."""
        r = self.client.post(self.url, self._podaci(kontakt_telefon='###abc'))
        self.assertIn(
            'Kontakt telefon nije ispravnog formata.',
            r.context['izmeni_forma'].errors['kontakt_telefon'],
        )

    def test_odustajanje_ne_cuva_2_2_8(self):
        """2.2.8 — otvaranje strane akcije bez slanja izmena ne menja podatke."""
        self.client.get(reverse('detalj_akcije', args=[self.akc.pk]))
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.naziv, 'Originalna akcija')

    def test_ne_vlasnik_403(self):
        """Samo vlasnik akcije sme da je menja — drugi organizator dobija 403."""
        drugi_org = organizator('drugi.org@gmail.com')
        self.client.force_login(drugi_org)
        r = self.client.post(self.url, self._podaci())
        self.assertEqual(r.status_code, 403)
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.naziv, 'Originalna akcija')


class OtkazivanjeAkcijeTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.akc = akcija(self.org, 'Akcija za otkazivanje', max_vol=5)
        self.url = reverse('otkazi_akciju', args=[self.akc.pk])
        self.client.force_login(self.org)

    def test_otkazivanje_2_2_9(self):
        """2.2.9 — status prelazi u „Otkazana", svi prijavljeni (ne odbijeni) se obaveštavaju emailom."""
        prihvacen = volonter('prihvacen@gmail.com')
        na_cekanju = volonter('cekanje@gmail.com')
        odbijen = volonter('odbijen@gmail.com')
        prijava(prihvacen, self.akc, status=Prijava.Status.PRIHVACENA)
        prijava(na_cekanju, self.akc, status=Prijava.Status.NA_CEKANJU)
        prijava(odbijen, self.akc, status=Prijava.Status.ODBIJENA)

        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])
        self.akc.refresh_from_db()
        self.assertEqual(self.akc.status, Akcija.Status.OTKAZANA)
        self.assertEqual(len(mail.outbox), 2)
        primaoci = {poruka.to[0] for poruka in mail.outbox}
        self.assertEqual(primaoci, {'prihvacen@gmail.com', 'cekanje@gmail.com'})

    def test_vec_otkazana_400(self):
        """Akcija koja je već otkazana ne može ponovo da se otkaže."""
        self.akc.status = Akcija.Status.OTKAZANA
        self.akc.save(update_fields=['status'])
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 400)

    def test_ne_vlasnik_403(self):
        """Samo vlasnik akcije sme da je otkaže — drugi organizator dobija 403."""
        drugi_org = organizator('drugi.org@gmail.com')
        self.client.force_login(drugi_org)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 403)
        self.akc.refresh_from_db()
        self.assertNotEqual(self.akc.status, Akcija.Status.OTKAZANA)
