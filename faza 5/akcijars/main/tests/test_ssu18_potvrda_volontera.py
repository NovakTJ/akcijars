# Autor: Novak Stijepic 0124/2023
"""
Jedinični testovi za SSU 18 — Potvrđivanje i odbijanje volontera.

Testiraju se kontroleri ``prihvati_prijavu`` / ``odbij_prijavu``
(funkcionalnost je implementirala Maša Nikolić — ukrštanje).
"""
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main.models import Akcija, Prijava
from ._helpers import organizator, sponzor, volonter, akcija, prijava


class PrihvatiPrijavuTest(TestCase):
    def setUp(self):
        self.org = organizator('org18@akcija.rs')
        self.vol = volonter('vol18@akcija.rs')
        self.akc = akcija(self.org, 'Akcija SSU18')
        self.prijava = prijava(self.vol, self.akc)
        self.url = reverse('prihvati_prijavu', args=[self.akc.pk, self.vol.pk])

    def test_prihvatanje_menja_status_salje_email_i_vraca_fragmente_2_2_1(self):
        """2.2.1 — organizator prihvata prijavu, volonter dobija email, panel se osvežava."""
        self.client.force_login(self.org)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.PRIHVACENA)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('panel', r.json())
        self.assertIn('sidebar', r.json())

    def test_prihvatanje_poslednjeg_mesta_popunjava_akciju_2_2_4(self):
        """2.2.4 — prihvatanje poslednje slobodne prijave označava akciju kao popunjenu."""
        self.akc.max_br_volontera = 1
        self.akc.save(update_fields=['max_br_volontera'])
        self.client.force_login(self.org)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Akcija.objects.get(pk=self.akc.pk).status, Akcija.Status.POPUNJENA)

    def test_drugi_organizator_ne_moze_da_prihvati_403(self):
        """Samo organizator vlasnik akcije može da prihvati prijavu → 403."""
        drugi = organizator('drugi18@akcija.rs')
        self.client.force_login(drugi)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.NA_CEKANJU)

    def test_neorganizatori_ne_mogu_da_prihvate_403(self):
        """Volonter i sponzor nisu organizatori akcije i ne mogu da prihvate prijavu → 403."""
        for korisnik in (volonter('drugi.vol18@akcija.rs'), sponzor('spon18@akcija.rs')):
            with self.subTest(korisnik=korisnik.email):
                self.client.force_login(korisnik)
                r = self.client.post(self.url)
                self.assertEqual(r.status_code, 403)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.NA_CEKANJU)

    def test_nema_prijave_na_cekanju_404(self):
        """Prijava koja nije na čekanju ili ne postoji ne može da se prihvati → 404."""
        self.client.force_login(self.org)
        self.prijava.status = Prijava.Status.PRIHVACENA
        self.prijava.save(update_fields=['status'])
        self.assertEqual(self.client.post(self.url).status_code, 404)

        nepostojeci_url = reverse('prihvati_prijavu', args=[self.akc.pk, 999999])
        self.assertEqual(self.client.post(nepostojeci_url).status_code, 404)

    def test_zatvorena_akcija_ne_menja_prijavu_2_2_5(self):
        """2.2.5 — popunjena, završena ili otkazana akcija ne prihvata novu prijavu."""
        self.client.force_login(self.org)
        for status in (Akcija.Status.POPUNJENA, Akcija.Status.ZAVRSENA, Akcija.Status.OTKAZANA):
            with self.subTest(status=status):
                self.akc.status = status
                self.akc.save(update_fields=['status'])
                self.prijava.status = Prijava.Status.NA_CEKANJU
                self.prijava.save(update_fields=['status'])
                r = self.client.post(self.url)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.NA_CEKANJU)
                self.assertIn('panel', r.json())
                self.assertIn('sidebar', r.json())
        self.assertEqual(len(mail.outbox), 0)

    def test_get_nije_dozvoljen_405(self):
        """require_POST — GET zahtev za prihvatanje vraća 405."""
        self.client.force_login(self.org)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_neprijavljen_korisnik_preusmeren_302(self):
        """login_required — neprijavljen korisnik se preusmerava na prijavu."""
        self.assertEqual(self.client.post(self.url).status_code, 302)


class OdbijPrijavuTest(TestCase):
    def setUp(self):
        self.org = organizator('org18.odbij@akcija.rs')
        self.vol = volonter('vol18.odbij@akcija.rs')
        self.akc = akcija(self.org, 'Akcija SSU18 odbijanje')
        self.prijava = prijava(self.vol, self.akc)
        self.client.force_login(self.org)
        self.url = reverse('odbij_prijavu', args=[self.akc.pk, self.vol.pk])

    def test_odbijanje_menja_status_salje_email_i_vraca_fragmente_2_2_2(self):
        """2.2.2 — organizator odbija prijavu, volonter dobija email, panel se osvežava."""
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.ODBIJENA)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('panel', r.json())
        self.assertIn('sidebar', r.json())

    def test_drugi_organizator_ne_moze_da_odbije_403(self):
        """Samo organizator vlasnik akcije može da odbije prijavu → 403."""
        drugi = organizator('drugi18.odbij@akcija.rs')
        self.client.force_login(drugi)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.NA_CEKANJU)

    def test_otkazana_akcija_ne_menja_prijavu(self):
        """Otkazana akcija je zamrznuta: odbijanje ne menja prijavu i ne šalje email."""
        self.akc.status = Akcija.Status.OTKAZANA
        self.akc.save(update_fields=['status'])
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Prijava.objects.get(pk=self.prijava.pk).status, Prijava.Status.NA_CEKANJU)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn('panel', r.json())
        self.assertIn('sidebar', r.json())

    def test_nema_prijave_na_cekanju_404(self):
        """Prijava koja nije na čekanju ili ne postoji ne može da se odbije → 404."""
        self.prijava.status = Prijava.Status.ODBIJENA
        self.prijava.save(update_fields=['status'])
        self.assertEqual(self.client.post(self.url).status_code, 404)

        nepostojeci_url = reverse('odbij_prijavu', args=[self.akc.pk, 999999])
        self.assertEqual(self.client.post(nepostojeci_url).status_code, 404)

    def test_get_nije_dozvoljen_405(self):
        """require_POST — GET zahtev za odbijanje vraća 405."""
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_neprijavljen_korisnik_preusmeren_302(self):
        """login_required — neprijavljen korisnik se preusmerava na prijavu."""
        self.client.logout()
        self.assertEqual(self.client.post(self.url).status_code, 302)

