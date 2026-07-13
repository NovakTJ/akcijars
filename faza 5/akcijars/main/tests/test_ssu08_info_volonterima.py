# Autor: Stefan Grujičić 0030/2023
"""
Jedinični testovi za SSU 8 — Slanje informacija (obaveštenja) volonterima.

Testira se Ajax kontroler ``posalji_obavestenje``
(funkcionalnost je implementirao Novak Stijepić — ukrštanje).
"""
import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, Prijava
from ._helpers import organizator, volonter, akcija, prijava


class PosaljiObavestenjeTest(TestCase):
    def setUp(self):
        self.org = organizator('office.zelenibeograd@gmail.com')
        self.akc = akcija(self.org, 'Akcija SSU8', Akcija.Status.AKTIVNA, max_vol=5)
        self.vol1 = volonter('vol1@gmail.com')
        self.vol2 = volonter('vol2@gmail.com')
        self.vol_odbijen = volonter('odbijen@gmail.com')
        prijava(self.vol1, self.akc, status=Prijava.Status.PRIHVACENA)
        prijava(self.vol2, self.akc, status=Prijava.Status.PRIHVACENA)
        prijava(self.vol_odbijen, self.akc, status=Prijava.Status.ODBIJENA)
        self.url = reverse('posalji_obavestenje', args=[self.akc.pk])
        self.client.force_login(self.org)

    def _post(self, poruka):
        return self.client.post(
            self.url, data=json.dumps({'poruka': poruka}), content_type='application/json',
        )

    def test_uspesno_slanje_svim_prihvacenim_2_2_1(self):
        """2.2.1 — obaveštenje se šalje emailom svim prihvaćenim volonterima (ne i odbijenim)."""
        r = self._post('Hvala vam na učešću, akcija je uspešno završena!')
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['ok'])
        self.assertEqual(r.json()['poslato'], 2)
        self.assertEqual(len(mail.outbox), 2)
        primaoci = {poruka.to[0] for poruka in mail.outbox}
        self.assertEqual(primaoci, {'vol1@gmail.com', 'vol2@gmail.com'})

    def test_prazna_poruka_2_2_2(self):
        """2.2.2 — prazna poruka se odbija, ništa se ne šalje."""
        r = self._post('   ')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['error'], 'Unesite tekst poruke.')
        self.assertEqual(len(mail.outbox), 0)

    def test_odustajanje_ne_salje_2_2_3(self):
        """2.2.3 — organizator otvori stranu akcije ali ne pošalje obaveštenje; niko ne prima email."""
        self.client.get(reverse('detalj_akcije', args=[self.akc.pk]))
        self.assertEqual(len(mail.outbox), 0)

    def test_bez_prihvacenih_volontera_400(self):
        """Akcija bez ijednog prihvaćenog volontera — slanje nije moguće."""
        akc2 = akcija(self.org, 'Akcija bez volontera')
        r = self.client.post(
            reverse('posalji_obavestenje', args=[akc2.pk]),
            data=json.dumps({'poruka': 'Test poruka'}), content_type='application/json',
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['error'], 'Nema prihvaćenih volontera za slanje.')

    def test_otkazana_akcija_400(self):
        """Otkazana (zamrznuta) akcija — slanje obaveštenja nije moguće."""
        self.akc.status = Akcija.Status.OTKAZANA
        self.akc.save(update_fields=['status'])
        r = self._post('Test poruka')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)

    def test_ne_vlasnik_403(self):
        """Samo vlasnik akcije (organizator koji ju je kreirao) sme da šalje obaveštenja."""
        drugi_org = organizator('drugi.org@gmail.com')
        self.client.force_login(drugi_org)
        r = self._post('Test poruka')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    def test_neulogovan_preusmeren(self):
        """login_required — neulogovan korisnik se preusmerava (302)."""
        self.client.logout()
        r = self._post('Test poruka')
        self.assertEqual(r.status_code, 302)
