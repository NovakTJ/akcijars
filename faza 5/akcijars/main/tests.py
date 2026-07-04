import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Akcija,
    KategorijaAkcije,
    KategorijaClanka,
    Clanak,
    Komentar,
    Korisnik,
    OrganizatorProfil,
    Prijava,
    SponzorProfil,
    SponzorskaPonuda,
    VolonterProfil,
    AdministratorProfil,
)


class RegistracijaTest(TestCase):
    """Testovi za scenario registracije korisnika (SSU 1)."""

    def setUp(self):
        self.url = reverse('registracija')
        self.osnovni_podaci = {
            'ime': 'Petar',
            'prezime': 'Petrović',
            'email': 'petar@example.com',
            'lozinka': 'Lozinka1!',
            'lozinka2': 'Lozinka1!',
            'uloga': 'volonter',
        }

    def test_get_prikazuje_formu(self):
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'registracija.html')

    def test_get_preset_uloge_iz_url_a(self):
        odgovor = self.client.get(self.url, {'uloga': 'organizator'})
        self.assertEqual(odgovor.context['uloga'], 'organizator')

    # ── 2.2.1 — uspešna registracija volontera ──
    def test_uspesna_registracija_volontera(self):
        odgovor = self.client.post(self.url, self.osnovni_podaci)
        self.assertEqual(odgovor.status_code, 200)
        korisnik = Korisnik.objects.get(email='petar@example.com')
        self.assertTrue(korisnik.je_volonter)
        self.assertTrue(korisnik.check_password('Lozinka1!'))
        self.assertTrue(VolonterProfil.objects.filter(korisnik=korisnik).exists())
        self.assertContains(odgovor, 'Registracija je uspešna. Možete se prijaviti na sistem.')

    def test_volonter_se_ne_loguje_automatski(self):
        # Posledica: korisnik nije ulogovan na kraju scenarija.
        self.client.post(self.url, self.osnovni_podaci)
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── 2.2.2 — uspešna registracija organizatora ──
    def test_uspesna_registracija_organizatora_ceka_odobrenje(self):
        podaci = dict(self.osnovni_podaci, uloga='organizator',
                      email='org@example.com',
                      naziv_organizacije='Zeleni krug',
                      br_telefona='+381 11 123 456')
        odgovor = self.client.post(self.url, podaci)
        korisnik = Korisnik.objects.get(email='org@example.com')
        profil = OrganizatorProfil.objects.get(korisnik=korisnik)
        self.assertEqual(profil.status, OrganizatorProfil.Status.NA_CEKANJU)
        self.assertEqual(profil.naziv_organizacije, 'Zeleni krug')
        self.assertTrue(korisnik.ceka_odobrenje)
        self.assertContains(odgovor, 'Nalog čeka odobrenje jednog od administratora.')

    def test_uspesna_registracija_sponzora(self):
        podaci = dict(self.osnovni_podaci, uloga='sponzor',
                      email='sponzor@example.com',
                      naziv_organizacije='Dobrotvor doo',
                      br_telefona='021-555-000')
        self.client.post(self.url, podaci)
        korisnik = Korisnik.objects.get(email='sponzor@example.com')
        self.assertTrue(SponzorProfil.objects.filter(korisnik=korisnik).exists())
        self.assertEqual(korisnik.sponzor_profil.status, SponzorProfil.Status.NA_CEKANJU)

    # ── 2.2.3 — neispravan format email adrese ──
    def test_neispravan_email_format(self):
        podaci = dict(self.osnovni_podaci, email='petar.example.com')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(odgovor, 'Email adresa nije ispravnog formata.')
        self.assertFalse(Korisnik.objects.filter(ime='Petar').exists())

    # ── 2.2.4 — lozinke se ne poklapaju ──
    def test_lozinke_se_ne_poklapaju(self):
        podaci = dict(self.osnovni_podaci, lozinka2='Drugacija1!')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(odgovor, 'Lozinke se ne poklapaju.')
        self.assertEqual(Korisnik.objects.count(), 0)

    # ── 2.2.5 — već registrovana email adresa ──
    def test_email_vec_postoji(self):
        Korisnik.objects.create_user(
            email='petar@example.com', password='Lozinka1!',
            korisnicko_ime='postojeci', ime='Pera', prezime='Perić')
        odgovor = self.client.post(self.url, self.osnovni_podaci)
        self.assertContains(odgovor, 'Korisnik sa tom email adresom već postoji.')
        self.assertEqual(Korisnik.objects.filter(email='petar@example.com').count(), 1)

    # ── 2.2.6 — nepopunjena obavezna polja ──
    def test_nepopunjena_obavezna_polja(self):
        podaci = dict(self.osnovni_podaci, ime='', prezime='')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(odgovor, 'Nisu uneta sva obavezna polja.')
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_organizator_bez_dodatnih_polja(self):
        podaci = dict(self.osnovni_podaci, uloga='organizator', email='org@example.com')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(odgovor, 'Nisu uneta sva obavezna polja.')
        self.assertEqual(Korisnik.objects.count(), 0)

    # ── 2.2.7 — lozinka ne zadovoljava minimalne uslove ──
    def test_prekratka_lozinka(self):
        podaci = dict(self.osnovni_podaci, lozinka='Kr1!', lozinka2='Kr1!')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(
            odgovor,
            'Lozinka mora imati najmanje 8 karaktera i sadržati barem '
            'jednu cifru ili specijalni karakter.')
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_lozinka_bez_cifre_i_specijalnog(self):
        podaci = dict(self.osnovni_podaci, lozinka='samoslova', lozinka2='samoslova')
        odgovor = self.client.post(self.url, podaci)
        self.assertContains(odgovor, 'Lozinka mora imati najmanje 8 karaktera')
        self.assertEqual(Korisnik.objects.count(), 0)

    # ── 2.4 — preduslov: ulogovan korisnik nema pristup registraciji ──
    def test_ulogovan_korisnik_preusmeren(self):
        Korisnik.objects.create_user(
            email='ulogovan@example.com', password='Lozinka1!',
            korisnicko_ime='ulogovan', ime='Mika', prezime='Mikić')
        self.client.login(email='ulogovan@example.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertRedirects(odgovor, reverse('home'))

    # Korisničko ime se generiše automatski i jedinstveno je.
    def test_jedinstveno_korisnicko_ime(self):
        self.client.post(self.url, self.osnovni_podaci)
        self.client.post(self.url, dict(self.osnovni_podaci, email='petar@drugi.com'))
        imena = list(Korisnik.objects.values_list('korisnicko_ime', flat=True))
        self.assertEqual(len(imena), len(set(imena)))

    # ── 2.2.1 / 2.2.2 — potvrda registracije se šalje na email (FZ 4.3.2) ──
    def test_volonteru_se_salje_potvrda_na_email(self):
        self.client.post(self.url, self.osnovni_podaci)
        self.assertEqual(len(mail.outbox), 1)
        poruka = mail.outbox[0]
        self.assertEqual(poruka.to, ['petar@example.com'])
        self.assertIn('potvrda registracije', poruka.subject)
        self.assertIn('možete se odmah prijaviti', poruka.body)

    def test_organizatoru_potvrda_pominje_odobrenje(self):
        podaci = dict(self.osnovni_podaci, uloga='organizator',
                      email='org@example.com',
                      naziv_organizacije='Zeleni krug',
                      br_telefona='+381 11 123 456')
        self.client.post(self.url, podaci)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['org@example.com'])
        self.assertIn('mora biti odobren', mail.outbox[0].body)

    def test_neuspesna_registracija_ne_salje_email(self):
        podaci = dict(self.osnovni_podaci, lozinka2='Drugacija1!')
        self.client.post(self.url, podaci)
        self.assertEqual(len(mail.outbox), 0)


class PrijavaTest(TestCase):
    """Testovi za scenario autorizacije korisnika (SSU 2)."""

    def setUp(self):
        self.url = reverse('prijava')
        self.volonter = Korisnik.objects.create_user(
            email='volonter@example.com', password='Lozinka1!',
            korisnicko_ime='volonter', ime='Mila', prezime='Milić')
        VolonterProfil.objects.create(korisnik=self.volonter)

    def test_get_prikazuje_formu(self):
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'prijava.html')

    # ── 2.2.1 — uspešna autorizacija ──
    def test_uspesna_prijava_volontera(self):
        odgovor = self.client.post(
            self.url, {'email': 'volonter@example.com', 'lozinka': 'Lozinka1!'})
        self.assertRedirects(odgovor, reverse('volonter_panel'))
        self.assertEqual(
            int(self.client.session['_auth_user_id']), self.volonter.pk)

    def test_prijava_email_case_insensitive(self):
        odgovor = self.client.post(
            self.url, {'email': 'VOLONTER@example.com', 'lozinka': 'Lozinka1!'})
        self.assertIn('_auth_user_id', self.client.session)

    # ── 2.2.2 — nepostojeća email adresa ──
    def test_nepostojeci_email(self):
        odgovor = self.client.post(
            self.url, {'email': 'nema@example.com', 'lozinka': 'Lozinka1!'})
        self.assertContains(odgovor, 'Email adresa ili lozinka nisu ispravni.')
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── 2.2.3 — neispravna lozinka ──
    def test_pogresna_lozinka(self):
        odgovor = self.client.post(
            self.url, {'email': 'volonter@example.com', 'lozinka': 'Pogresna1!'})
        self.assertContains(odgovor, 'Email adresa ili lozinka nisu ispravni.')
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── 2.2.4 — neodobren nalog organizatora/sponzora ──
    def test_neodobren_organizator(self):
        org = Korisnik.objects.create_user(
            email='org@example.com', password='Lozinka1!',
            korisnicko_ime='org', ime='Ognjen', prezime='Ognjenović')
        OrganizatorProfil.objects.create(
            korisnik=org, naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.NA_CEKANJU)
        odgovor = self.client.post(
            self.url, {'email': 'org@example.com', 'lozinka': 'Lozinka1!'})
        self.assertContains(odgovor, 'Nalog čeka odobrenje administratora.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_odobren_organizator_se_prijavljuje(self):
        org = Korisnik.objects.create_user(
            email='org2@example.com', password='Lozinka1!',
            korisnicko_ime='org2', ime='Ognjen', prezime='Ognjenović')
        OrganizatorProfil.objects.create(
            korisnik=org, naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN)
        odgovor = self.client.post(
            self.url, {'email': 'org2@example.com', 'lozinka': 'Lozinka1!'})
        self.assertRedirects(odgovor, reverse('home'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_nepopunjena_polja(self):
        odgovor = self.client.post(self.url, {'email': '', 'lozinka': ''})
        self.assertContains(odgovor, 'Nisu uneta sva obavezna polja.')

    # ── 2.2.5 — odjava korisnika ──
    def test_odjava(self):
        self.client.login(email='volonter@example.com', password='Lozinka1!')
        self.assertIn('_auth_user_id', self.client.session)
        odgovor = self.client.get(reverse('odjava'))
        self.assertRedirects(odgovor, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    # ── 2.4 — preduslov: ulogovan korisnik ne vidi formu za prijavu ──
    def test_ulogovan_korisnik_preusmeren(self):
        self.client.login(email='volonter@example.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertRedirects(odgovor, reverse('volonter_panel'))


class AdminPanelTest(TestCase):
    """Testovi za SSU 13 — upravljanje korisničkim nalozima."""

    def setUp(self):
        self.admin = Korisnik.objects.create_user(
            email='admin@example.com', password='Admin123!',
            korisnicko_ime='admin', ime='Admin', prezime='Adminović')
        AdministratorProfil.objects.create(korisnik=self.admin)

        self.org = Korisnik.objects.create_user(
            email='org@example.com', password='Lozinka1!',
            korisnicko_ime='org', ime='Ognjen', prezime='Ognjenović')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=self.org,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.NA_CEKANJU,
        )

        self.sponzor = Korisnik.objects.create_user(
            email='sponzor@example.com', password='Lozinka1!',
            korisnicko_ime='sponzor', ime='Sara', prezime='Sarić')
        self.sponzor_profil = SponzorProfil.objects.create(
            korisnik=self.sponzor,
            naziv_organizacije='ProNatura',
            status=SponzorProfil.Status.NA_CEKANJU,
        )

        self.volonter = Korisnik.objects.create_user(
            email='vol@example.com', password='Lozinka1!',
            korisnicko_ime='vol', ime='Vanja', prezime='Vanić')
        VolonterProfil.objects.create(korisnik=self.volonter)

    def _prijavi_admina(self):
        self.client.login(email='admin@example.com', password='Admin123!')

    def _ajax_post(self, url_name, podaci):
        return self.client.post(
            reverse(url_name),
            data=json.dumps(podaci),
            content_type='application/json',
        )

    # ── Pristup admin panelu ──

    def test_admin_panel_dostupan_adminu(self):
        self._prijavi_admina()
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'admin_panel.html')

    def test_admin_panel_nedostupan_volonteru(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertRedirects(odgovor, reverse('home'))

    def test_admin_panel_nedostupan_anonimnom(self):
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertRedirects(odgovor, reverse('home'))

    def test_admin_panel_prikazuje_zahteve(self):
        self._prijavi_admina()
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertContains(odgovor, 'Zeleni krug')
        self.assertContains(odgovor, 'ProNatura')

    # ── Odobravanje naloga (SSU 13, 2.2.1) ──

    def test_ajax_odobri_organizatora(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.org_profil.refresh_from_db()
        self.assertEqual(self.org_profil.status, OrganizatorProfil.Status.ODOBREN)

    def test_ajax_odobri_sponzora(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.sponzor.pk})
        self.assertEqual(odgovor.status_code, 200)
        self.sponzor_profil.refresh_from_db()
        self.assertEqual(self.sponzor_profil.status, SponzorProfil.Status.ODOBREN)

    def test_ajax_odobri_salje_email(self):
        self._prijavi_admina()
        self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('odobren', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['org@example.com'])

    def test_odobren_organizator_moze_da_se_uloguje(self):
        self._prijavi_admina()
        self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.org.pk})
        self.client.logout()
        odgovor = self.client.post(
            reverse('prijava'), {'email': 'org@example.com', 'lozinka': 'Lozinka1!'})
        self.assertRedirects(odgovor, reverse('home'))

    # ── Odbijanje naloga (SSU 13, 2.2.2) ──

    def test_ajax_odbij_organizatora(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odbij_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.org_profil.refresh_from_db()
        self.assertEqual(self.org_profil.status, OrganizatorProfil.Status.ODBIJEN)

    def test_ajax_odbij_salje_email(self):
        self._prijavi_admina()
        self._ajax_post('ajax_odbij_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('odbijen', mail.outbox[0].subject)

    def test_odbijen_organizator_ne_moze_da_se_uloguje(self):
        self._prijavi_admina()
        self._ajax_post('ajax_odbij_nalog', {'korisnik_id': self.org.pk})
        self.client.logout()
        odgovor = self.client.post(
            reverse('prijava'), {'email': 'org@example.com', 'lozinka': 'Lozinka1!'})
        self.assertContains(odgovor, 'Nalog čeka odobrenje administratora.')

    # ── Uklanjanje korisnika (SSU 13, 2.2.3) ──

    def test_ajax_ukloni_korisnika(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_ukloni_korisnika', {'korisnik_id': self.volonter.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.assertFalse(Korisnik.objects.filter(pk=self.volonter.pk).exists())

    def test_admin_ne_moze_ukloniti_sopstveni_nalog(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_ukloni_korisnika', {'korisnik_id': self.admin.pk})
        self.assertEqual(odgovor.status_code, 400)
        data = json.loads(odgovor.content)
        self.assertIn('error', data)
        self.assertTrue(Korisnik.objects.filter(pk=self.admin.pk).exists())

    def test_ajax_ukloni_ne_pronalazi_nepostojeci_nalog(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_ukloni_korisnika', {'korisnik_id': 99999})
        self.assertEqual(odgovor.status_code, 404)

    # ── Zaštita Ajax endpointa ──

    def test_ajax_odbija_nonautentifikovanog(self):
        odgovor = self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_ajax_odbija_volontera(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self._ajax_post('ajax_odobri_nalog', {'korisnik_id': self.org.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_neodobren_organizator_ne_moze_da_se_uloguje(self):
        odgovor = self.client.post(
            reverse('prijava'), {'email': 'org@example.com', 'lozinka': 'Lozinka1!'})
        self.assertContains(odgovor, 'Nalog čeka odobrenje administratora.')
        self.assertNotIn('_auth_user_id', self.client.session)


class AdminAkcijeClancakTest(TestCase):
    """Testovi za admin upravljanje akcijama i člancima na čekanju."""

    def setUp(self):
        self.admin = Korisnik.objects.create_user(
            email='admin@example.com', password='Admin123!',
            korisnicko_ime='admin', ime='Admin', prezime='Adminović')
        AdministratorProfil.objects.create(korisnik=self.admin)

        kat_akcije = KategorijaAkcije.objects.create(naziv='Ekologija')
        kat_clanka = KategorijaClanka.objects.create(naziv='Opšte')

        org = Korisnik.objects.create_user(
            email='org@example.com', password='Lozinka1!',
            korisnicko_ime='org', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org, naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN)

        self.akcija = Akcija.objects.create(
            organizator=self.org_profil, kategorija=kat_akcije,
            naziv='Test akcija na čekanju', opis='Opis',
            datum=timezone.now().date(), vreme='10:00', lokacija='Beograd',
            max_br_volontera=10, kontakt_email='org@example.com',
            kontakt_telefon='011-111', status=Akcija.Status.NA_CEKANJU)

        self.clanak = Clanak.objects.create(
            autor=self.org_profil, kategorija=kat_clanka,
            naslov='Test članak na čekanju', tekst='Tekst.',
            status=Clanak.Status.NA_CEKANJU)

        vol = Korisnik.objects.create_user(
            email='vol@example.com', password='Lozinka1!',
            korisnicko_ime='vol', ime='Vanja', prezime='Vanić')
        VolonterProfil.objects.create(korisnik=vol)

    def _prijavi_admina(self):
        self.client.login(email='admin@example.com', password='Admin123!')

    def _ajax_post(self, url_name, podaci):
        return self.client.post(
            reverse(url_name),
            data=json.dumps(podaci),
            content_type='application/json',
        )

    # ── Admin panel prikazuje akcije i članke ──

    def test_panel_prikazuje_akcije_na_cekanju(self):
        self._prijavi_admina()
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertContains(odgovor, 'Test akcija na čekanju')

    def test_panel_prikazuje_clanke_na_cekanju(self):
        self._prijavi_admina()
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertContains(odgovor, 'Test članak na čekanju')

    def test_panel_kontekst_sadrzi_akcije_i_clanke(self):
        self._prijavi_admina()
        odgovor = self.client.get(reverse('admin_panel'))
        self.assertEqual(odgovor.context['br_akcija_na_cekanju'], 1)
        self.assertEqual(odgovor.context['br_clanaka_na_cekanju'], 1)

    # ── Odobri akciju ──

    def test_ajax_odobri_akciju_menja_status(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.akcija.refresh_from_db()
        self.assertEqual(self.akcija.status, Akcija.Status.ODOBRENA)

    def test_ajax_odobri_akciju_vraca_403_anonimnom(self):
        odgovor = self._ajax_post('ajax_odobri_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 403)
        self.akcija.refresh_from_db()
        self.assertEqual(self.akcija.status, Akcija.Status.NA_CEKANJU)

    def test_ajax_odobri_akciju_vraca_403_volonteru(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self._ajax_post('ajax_odobri_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_ajax_odobri_akciju_vraca_400_kad_nije_na_cekanju(self):
        self.akcija.status = Akcija.Status.ODOBRENA
        self.akcija.save()
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 400)

    def test_ajax_odobri_akciju_vraca_404_nepostojeca(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_akciju', {'akcija_id': 99999})
        self.assertEqual(odgovor.status_code, 404)

    # ── Obriši akciju ──

    def test_ajax_obrisi_akciju_brise_akciju(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_obrisi_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.assertFalse(Akcija.objects.filter(pk=self.akcija.pk).exists())

    def test_ajax_obrisi_akciju_vraca_403_anonimnom(self):
        odgovor = self._ajax_post('ajax_obrisi_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 403)
        self.assertTrue(Akcija.objects.filter(pk=self.akcija.pk).exists())

    def test_ajax_obrisi_akciju_vraca_403_volonteru(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self._ajax_post('ajax_obrisi_akciju', {'akcija_id': self.akcija.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_ajax_obrisi_akciju_vraca_404_nepostojeca(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_obrisi_akciju', {'akcija_id': 99999})
        self.assertEqual(odgovor.status_code, 404)

    # ── Odobri članak ──

    def test_ajax_odobri_clanak_menja_status(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.clanak.refresh_from_db()
        self.assertEqual(self.clanak.status, Clanak.Status.OBJAVLJEN)

    def test_ajax_odobri_clanak_vraca_403_anonimnom(self):
        odgovor = self._ajax_post('ajax_odobri_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 403)
        self.clanak.refresh_from_db()
        self.assertEqual(self.clanak.status, Clanak.Status.NA_CEKANJU)

    def test_ajax_odobri_clanak_vraca_403_volonteru(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self._ajax_post('ajax_odobri_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_ajax_odobri_clanak_vraca_400_kad_nije_na_cekanju(self):
        self.clanak.status = Clanak.Status.OBJAVLJEN
        self.clanak.save()
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 400)

    def test_ajax_odobri_clanak_vraca_404_nepostojeci(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_odobri_clanak', {'clanak_id': 99999})
        self.assertEqual(odgovor.status_code, 404)

    # ── Obriši članak ──

    def test_ajax_obrisi_clanak_brise_clanak(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_obrisi_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertTrue(data['success'])
        self.assertFalse(Clanak.objects.filter(pk=self.clanak.pk).exists())

    def test_ajax_obrisi_clanak_vraca_403_anonimnom(self):
        odgovor = self._ajax_post('ajax_obrisi_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 403)
        self.assertTrue(Clanak.objects.filter(pk=self.clanak.pk).exists())

    def test_ajax_obrisi_clanak_vraca_403_volonteru(self):
        self.client.login(email='vol@example.com', password='Lozinka1!')
        odgovor = self._ajax_post('ajax_obrisi_clanak', {'clanak_id': self.clanak.pk})
        self.assertEqual(odgovor.status_code, 403)

    def test_ajax_obrisi_clanak_vraca_404_nepostojeci(self):
        self._prijavi_admina()
        odgovor = self._ajax_post('ajax_obrisi_clanak', {'clanak_id': 99999})
        self.assertEqual(odgovor.status_code, 404)


class SponzorskaPonudaTest(TestCase):
    """Testovi za SSU 7 — slanje sponzorske ponude."""

    def setUp(self):
        kategorija = KategorijaAkcije.objects.create(naziv='Ekologija')

        org_korisnik = Korisnik.objects.create_user(
            email='org@primer.com', password='Lozinka1!',
            korisnicko_ime='org_primer', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org_korisnik,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        self.akcija = Akcija.objects.create(
            organizator=self.org_profil,
            kategorija=kategorija,
            naziv='Test akcija',
            opis='Opis test akcije',
            datum=timezone.now().date(),
            vreme='10:00',
            lokacija='Beograd',
            max_br_volontera=10,
            kontakt_email='org@primer.com',
            kontakt_telefon='011-123-456',
            status=Akcija.Status.AKTIVNA,
        )

        self.sponzor_korisnik = Korisnik.objects.create_user(
            email='sponzor@primer.com', password='Lozinka1!',
            korisnicko_ime='sponzor_primer', ime='Sara', prezime='Sarić')
        self.sponzor_profil = SponzorProfil.objects.create(
            korisnik=self.sponzor_korisnik,
            naziv_organizacije='ProNatura',
            status=SponzorProfil.Status.ODOBREN,
        )

        self.volonter_korisnik = Korisnik.objects.create_user(
            email='vol@primer.com', password='Lozinka1!',
            korisnicko_ime='vol_primer', ime='Vanja', prezime='Vanić')
        VolonterProfil.objects.create(korisnik=self.volonter_korisnik)

        self.url = reverse('posalji_ponudu', kwargs={'id_akc': self.akcija.pk})

    def _podaci_ponude(self):
        return {
            'akcija': self.akcija.pk,
            'vrednost': 500,
            'opis': 'Finansijska podrška za opremu',
        }

    # ── Sponzor može da pošalje ponudu ──────────────────────────────────────

    def test_sponzor_moze_da_posalje_ponudu(self):
        self.client.login(email='sponzor@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url, self._podaci_ponude())
        self.assertEqual(odgovor.status_code, 200)
        self.assertTrue(SponzorskaPonuda.objects.filter(
            sponzor=self.sponzor_profil, akcija=self.akcija
        ).exists())

    def test_ponuda_se_kreira_sa_statusom_na_cekanju(self):
        self.client.login(email='sponzor@primer.com', password='Lozinka1!')
        self.client.post(self.url, self._podaci_ponude())
        ponuda = SponzorskaPonuda.objects.get(sponzor=self.sponzor_profil, akcija=self.akcija)
        self.assertEqual(ponuda.status, SponzorskaPonuda.Status.NA_CEKANJU)

    def test_ponuda_cuva_ispravne_vrednosti(self):
        self.client.login(email='sponzor@primer.com', password='Lozinka1!')
        self.client.post(self.url, self._podaci_ponude())
        ponuda = SponzorskaPonuda.objects.get(sponzor=self.sponzor_profil, akcija=self.akcija)
        self.assertEqual(ponuda.vrednost, 500)
        self.assertEqual(ponuda.opis, 'Finansijska podrška za opremu')

    # ── Volonter ne može da pošalje ponudu ──────────────────────────────────

    def test_volonter_ne_moze_da_posalje_ponudu(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url, self._podaci_ponude())
        self.assertEqual(odgovor.status_code, 403)
        self.assertFalse(SponzorskaPonuda.objects.exists())

    # ── Neautentifikovan korisnik ne može ────────────────────────────────────

    def test_anoniman_ne_moze_da_posalje_ponudu(self):
        odgovor = self.client.post(self.url, self._podaci_ponude())
        self.assertNotEqual(odgovor.status_code, 200)
        self.assertFalse(SponzorskaPonuda.objects.exists())

    # ── Neodobren sponzor ne može ────────────────────────────────────────────

    def test_neodobren_sponzor_ne_moze_da_posalje_ponudu(self):
        neodobren = Korisnik.objects.create_user(
            email='neodobren@primer.com', password='Lozinka1!',
            korisnicko_ime='neodobren', ime='Neo', prezime='Neović')
        SponzorProfil.objects.create(
            korisnik=neodobren,
            naziv_organizacije='NeNatura',
            status=SponzorProfil.Status.NA_CEKANJU,
        )
        self.client.login(email='neodobren@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url, self._podaci_ponude())
        self.assertEqual(odgovor.status_code, 403)
        self.assertFalse(SponzorskaPonuda.objects.exists())

    # ── Validacija forme ─────────────────────────────────────────────────────

    def test_ponuda_sa_nultom_vrednoscu_nije_validna(self):
        self.client.login(email='sponzor@primer.com', password='Lozinka1!')
        podaci = self._podaci_ponude()
        podaci['vrednost'] = 0
        self.client.post(self.url, podaci)
        self.assertFalse(SponzorskaPonuda.objects.exists())

    # ── Detalj akcije prikazuje formu sponzoru ───────────────────────────────

    def test_detalj_akcije_prikazuje_formu_sponzoru(self):
        self.client.login(email='sponzor@primer.com', password='Lozinka1!')
        odgovor = self.client.get(reverse('detalj_akcije', kwargs={'id_akc': self.akcija.pk}))
        self.assertEqual(odgovor.status_code, 200)
        self.assertIn('ponuda_forma', odgovor.context)

    def test_detalj_akcije_ne_prikazuje_formu_volonteru(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self.client.get(reverse('detalj_akcije', kwargs={'id_akc': self.akcija.pk}))
        self.assertEqual(odgovor.status_code, 200)
        self.assertNotIn('ponuda_forma', odgovor.context)


class OdlukaPonudaTest(TestCase):
    """Testovi za SSU 17 — prihvatanje/odbijanje sponzorske ponude."""

    def setUp(self):
        kategorija = KategorijaAkcije.objects.create(naziv='Ekologija')

        org_korisnik = Korisnik.objects.create_user(
            email='org@primer.com', password='Lozinka1!',
            korisnicko_ime='org_primer', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org_korisnik,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        drugi_org = Korisnik.objects.create_user(
            email='org2@primer.com', password='Lozinka1!',
            korisnicko_ime='org2_primer', ime='Org2', prezime='Drugi')
        OrganizatorProfil.objects.create(
            korisnik=drugi_org,
            naziv_organizacije='Plave reke',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        self.akcija = Akcija.objects.create(
            organizator=self.org_profil,
            kategorija=kategorija,
            naziv='Test akcija',
            opis='Opis',
            datum=timezone.now().date(),
            vreme='10:00',
            lokacija='Beograd',
            max_br_volontera=10,
            kontakt_email='org@primer.com',
            kontakt_telefon='011-111',
            status=Akcija.Status.AKTIVNA,
        )

        sponzor_korisnik = Korisnik.objects.create_user(
            email='sponzor@primer.com', password='Lozinka1!',
            korisnicko_ime='sponzor_primer', ime='Sara', prezime='Sarić')
        self.sponzor_profil = SponzorProfil.objects.create(
            korisnik=sponzor_korisnik,
            naziv_organizacije='ProNatura',
            status=SponzorProfil.Status.ODOBREN,
        )

        self.volonter_korisnik = Korisnik.objects.create_user(
            email='vol@primer.com', password='Lozinka1!',
            korisnicko_ime='vol_primer', ime='Vanja', prezime='Vanić')
        VolonterProfil.objects.create(korisnik=self.volonter_korisnik)

        self.ponuda = SponzorskaPonuda.objects.create(
            sponzor=self.sponzor_profil,
            akcija=self.akcija,
            vrednost=500,
            opis='Finansijska podrška za opremu',
        )

        self.url_prihvati = reverse('prihvati_ponudu', kwargs={
            'id_akc': self.akcija.pk, 'ponuda_id': self.ponuda.pk})
        self.url_odbij = reverse('odbij_ponudu', kwargs={
            'id_akc': self.akcija.pk, 'ponuda_id': self.ponuda.pk})

    # ── Prihvatanje (SSU 17, 2.2.1) ─────────────────────────────────────────

    def test_organizator_moze_prihvatiti_ponudu(self):
        self.client.login(email='org@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_prihvati)
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertIn('ponude', data)
        self.ponuda.refresh_from_db()
        self.assertEqual(self.ponuda.status, SponzorskaPonuda.Status.PRIHVACENA)

    def test_prihvatanje_vraca_br_na_cekanju(self):
        self.client.login(email='org@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_prihvati)
        data = json.loads(odgovor.content)
        self.assertEqual(data['br_na_cekanju'], 0)

    # ── Odbijanje (SSU 17, 2.2.2) ────────────────────────────────────────────

    def test_organizator_moze_odbiti_ponudu(self):
        self.client.login(email='org@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_odbij)
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertIn('ponude', data)
        self.ponuda.refresh_from_db()
        self.assertEqual(self.ponuda.status, SponzorskaPonuda.Status.ODBIJENA)

    # ── Autorizacija ─────────────────────────────────────────────────────────

    def test_drugi_organizator_dobija_403_na_prihvati(self):
        self.client.login(email='org2@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_prihvati)
        self.assertEqual(odgovor.status_code, 403)
        self.ponuda.refresh_from_db()
        self.assertEqual(self.ponuda.status, SponzorskaPonuda.Status.NA_CEKANJU)

    def test_drugi_organizator_dobija_403_na_odbij(self):
        self.client.login(email='org2@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_odbij)
        self.assertEqual(odgovor.status_code, 403)
        self.ponuda.refresh_from_db()
        self.assertEqual(self.ponuda.status, SponzorskaPonuda.Status.NA_CEKANJU)

    def test_volonter_dobija_403(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_prihvati)
        self.assertEqual(odgovor.status_code, 403)

    def test_anoniman_ne_moze_promeniti_status(self):
        odgovor = self.client.post(self.url_prihvati)
        self.assertNotEqual(odgovor.status_code, 200)
        self.ponuda.refresh_from_db()
        self.assertEqual(self.ponuda.status, SponzorskaPonuda.Status.NA_CEKANJU)

    # ── Error handling ───────────────────────────────────────────────────────

    def test_vec_prihvacena_ponuda_vraca_gresku(self):
        self.ponuda.status = SponzorskaPonuda.Status.PRIHVACENA
        self.ponuda.save()
        self.client.login(email='org@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_odbij)
        self.assertEqual(odgovor.status_code, 400)
        self.assertIn('error', json.loads(odgovor.content))

    def test_vec_odbijena_ponuda_vraca_gresku(self):
        self.ponuda.status = SponzorskaPonuda.Status.ODBIJENA
        self.ponuda.save()
        self.client.login(email='org@primer.com', password='Lozinka1!')
        odgovor = self.client.post(self.url_prihvati)
        self.assertEqual(odgovor.status_code, 400)
        self.assertIn('error', json.loads(odgovor.content))

    def test_nepostojeca_ponuda_vraca_404(self):
        self.client.login(email='org@primer.com', password='Lozinka1!')
        url = reverse('prihvati_ponudu', kwargs={
            'id_akc': self.akcija.pk, 'ponuda_id': 99999})
        odgovor = self.client.post(url)
        self.assertEqual(odgovor.status_code, 404)

    # ── Javni prikaz prihvaćenih sponzora ────────────────────────────────────

    def test_detalj_prikazuje_prihvacene_sponzore(self):
        self.ponuda.status = SponzorskaPonuda.Status.PRIHVACENA
        self.ponuda.save()
        odgovor = self.client.get(reverse('detalj_akcije', kwargs={'id_akc': self.akcija.pk}))
        self.assertEqual(odgovor.status_code, 200)
        self.assertContains(odgovor, 'ProNatura')
        self.assertContains(odgovor, '500')

    def test_detalj_ne_prikazuje_ponude_na_cekanju(self):
        odgovor = self.client.get(reverse('detalj_akcije', kwargs={'id_akc': self.akcija.pk}))
        self.assertEqual(odgovor.status_code, 200)
        self.assertNotContains(odgovor, 'Sponzori ove akcije')


class SponzorPanelTest(TestCase):
    """Testovi za sponzorski panel (SSU 16)."""

    def setUp(self):
        kategorija = KategorijaAkcije.objects.create(naziv='Ekologija')

        org_korisnik = Korisnik.objects.create_user(
            email='org@primer.com', password='Lozinka1!',
            korisnicko_ime='org_primer', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org_korisnik,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        self.akcija = Akcija.objects.create(
            organizator=self.org_profil,
            kategorija=kategorija,
            naziv='Test akcija',
            opis='Opis',
            datum='2026-06-01',
            vreme='10:00',
            lokacija='Beograd',
            max_br_volontera=10,
            kontakt_email='org@primer.com',
            kontakt_telefon='011-111',
            status=Akcija.Status.AKTIVNA,
        )

        # Sponzor 1 — ima ponude sva tri statusa
        self.sponzor1 = Korisnik.objects.create_user(
            email='sponzor1@primer.com', password='Lozinka1!',
            korisnicko_ime='sponzor1', ime='Sara', prezime='Sarić')
        self.sponzor1_profil = SponzorProfil.objects.create(
            korisnik=self.sponzor1,
            naziv_organizacije='ProNatura',
            status=SponzorProfil.Status.ODOBREN,
        )
        self.ponuda_prihvacena = SponzorskaPonuda.objects.create(
            sponzor=self.sponzor1_profil, akcija=self.akcija,
            vrednost=800, opis='Oprema',
            status=SponzorskaPonuda.Status.PRIHVACENA,
        )
        self.ponuda_na_cekanju = SponzorskaPonuda.objects.create(
            sponzor=self.sponzor1_profil,
            akcija=Akcija.objects.create(
                organizator=self.org_profil, kategorija=kategorija,
                naziv='Druga akcija', opis='Opis',
                datum='2026-07-01', vreme='10:00', lokacija='Niš',
                max_br_volontera=5, kontakt_email='org@primer.com',
                kontakt_telefon='011-222', status=Akcija.Status.AKTIVNA,
            ),
            vrednost=300, opis='Čekanje',
            status=SponzorskaPonuda.Status.NA_CEKANJU,
        )
        self.ponuda_odbijena = SponzorskaPonuda.objects.create(
            sponzor=self.sponzor1_profil,
            akcija=Akcija.objects.create(
                organizator=self.org_profil, kategorija=kategorija,
                naziv='Treća akcija', opis='Opis',
                datum='2026-08-01', vreme='10:00', lokacija='NiS',
                max_br_volontera=5, kontakt_email='org@primer.com',
                kontakt_telefon='011-333', status=Akcija.Status.AKTIVNA,
            ),
            vrednost=200, opis='Odbijeno',
            status=SponzorskaPonuda.Status.ODBIJENA,
        )

        # Sponzor 2 — tuđe ponude, ne smiju biti vidljive sponzoru1
        self.sponzor2 = Korisnik.objects.create_user(
            email='sponzor2@primer.com', password='Lozinka1!',
            korisnicko_ime='sponzor2', ime='Bojan', prezime='Bojić')
        self.sponzor2_profil = SponzorProfil.objects.create(
            korisnik=self.sponzor2,
            naziv_organizacije='EkoFirma',
            status=SponzorProfil.Status.ODOBREN,
        )
        SponzorskaPonuda.objects.create(
            sponzor=self.sponzor2_profil, akcija=self.akcija,
            vrednost=9999, opis='Tuđa ponuda',
            status=SponzorskaPonuda.Status.PRIHVACENA,
        )

        self.volonter = Korisnik.objects.create_user(
            email='vol@primer.com', password='Lozinka1!',
            korisnicko_ime='vol_primer', ime='Vanja', prezime='Vanić')
        VolonterProfil.objects.create(korisnik=self.volonter)

        self.url = reverse('sponzor_panel')

    # ── Pristup ──────────────────────────────────────────────────────────────

    def test_sponzor_vidi_panel(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'sponzor_panel.html')

    def test_anoniman_ne_vidi_panel(self):
        odgovor = self.client.get(self.url)
        self.assertNotEqual(odgovor.status_code, 200)

    def test_volonter_preusmeren_na_pocetnu(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertRedirects(odgovor, reverse('home'))

    # ── Sponzor vidi samo svoje ponude ───────────────────────────────────────

    def test_sponzor_vidi_samo_svoje_prihvacene(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        prihvacene = list(odgovor.context['ponude_prihvacene'])
        self.assertEqual(len(prihvacene), 1)
        self.assertEqual(prihvacene[0].pk, self.ponuda_prihvacena.pk)

    def test_sponzor_ne_vidi_tude_ponude(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        svi_pk = (
            [p.pk for p in odgovor.context['ponude_prihvacene']]
            + [p.pk for p in odgovor.context['ponude_na_cekanju']]
            + [p.pk for p in odgovor.context['ponude_odbijene']]
        )
        tude = SponzorskaPonuda.objects.filter(sponzor=self.sponzor2_profil)
        for t in tude:
            self.assertNotIn(t.pk, svi_pk)

    def test_sponzor_vidi_ponude_na_cekanju(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        na_cekanju = list(odgovor.context['ponude_na_cekanju'])
        self.assertEqual(len(na_cekanju), 1)
        self.assertEqual(na_cekanju[0].pk, self.ponuda_na_cekanju.pk)

    def test_sponzor_vidi_odbijene_ponude(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        odbijene = list(odgovor.context['ponude_odbijene'])
        self.assertEqual(len(odbijene), 1)
        self.assertEqual(odbijene[0].pk, self.ponuda_odbijena.pk)

    # ── Ukupan doprinos ───────────────────────────────────────────────────────

    def test_ukupan_doprinos_je_suma_prihvacenih(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.context['ukupan_doprinos'], 800)

    def test_ukupan_doprinos_ne_ukljucuje_cekanje_ni_odbijene(self):
        self.client.login(email='sponzor1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        # Vrednosti 300 (čekanje) i 200 (odbijena) ne smeju biti uključene
        self.assertNotEqual(odgovor.context['ukupan_doprinos'], 1300)

    def test_ukupan_doprinos_nula_bez_prihvacenih(self):
        self.client.login(email='sponzor2@primer.com', password='Lozinka1!')
        # Sponzor2 ima jednu prihvaćenu ali je to 9999
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.context['ukupan_doprinos'], 9999)

    # ── Login redirekcija za sponzora ─────────────────────────────────────────

    def test_sponzor_se_loguje_na_panel(self):
        odgovor = self.client.post(
            reverse('prijava'),
            {'email': 'sponzor1@primer.com', 'lozinka': 'Lozinka1!'})
        self.assertRedirects(odgovor, self.url)


class VolonterPanelTest(TestCase):
    """Testovi za volonterski panel (SSU 15)."""

    def setUp(self):
        kategorija = KategorijaAkcije.objects.create(naziv='Ekologija')

        org_korisnik = Korisnik.objects.create_user(
            email='org@primer.com', password='Lozinka1!',
            korisnicko_ime='org_primer', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org_korisnik,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        def nova_akcija(naziv, status=Akcija.Status.AKTIVNA, datum='2026-09-01'):
            return Akcija.objects.create(
                organizator=self.org_profil,
                kategorija=kategorija,
                naziv=naziv,
                opis='Opis',
                datum=datum,
                vreme='10:00',
                lokacija='Beograd',
                max_br_volontera=10,
                kontakt_email='org@primer.com',
                kontakt_telefon='011-111',
                status=status,
            )

        self.akcija_aktivna = nova_akcija('Aktivna akcija')
        self.akcija_zavrsena = nova_akcija('Završena akcija', Akcija.Status.ZAVRSENA, '2026-01-01')
        self.akcija_otkazana = nova_akcija('Otkazana akcija', Akcija.Status.OTKAZANA, '2026-02-01')
        self.akcija_druga = nova_akcija('Druga aktivna akcija')

        # Volonter 1 — ima prijave svih statusa
        self.vol1 = Korisnik.objects.create_user(
            email='vol1@primer.com', password='Lozinka1!',
            korisnicko_ime='vol1', ime='Ana', prezime='Anić')
        self.vol1_profil = VolonterProfil.objects.create(korisnik=self.vol1)

        self.prijava_na_cekanju = Prijava.objects.create(
            korisnik=self.vol1_profil, akcija=self.akcija_aktivna,
            status=Prijava.Status.NA_CEKANJU, br_sati=0,
        )
        self.prijava_prihvacena = Prijava.objects.create(
            korisnik=self.vol1_profil, akcija=self.akcija_druga,
            status=Prijava.Status.PRIHVACENA, br_sati=6,
        )
        self.prijava_odbijena = Prijava.objects.create(
            korisnik=self.vol1_profil, akcija=self.akcija_zavrsena,
            status=Prijava.Status.ODBIJENA, br_sati=0,
        )
        self.prijava_zavrsena_akcija = Prijava.objects.create(
            korisnik=self.vol1_profil, akcija=self.akcija_otkazana,
            status=Prijava.Status.PRIHVACENA, br_sati=4,
        )

        # Volonter 2 — tuđe prijave, ne smiju biti vidljive vol1
        self.vol2 = Korisnik.objects.create_user(
            email='vol2@primer.com', password='Lozinka1!',
            korisnicko_ime='vol2', ime='Bojan', prezime='Bojić')
        self.vol2_profil = VolonterProfil.objects.create(korisnik=self.vol2)
        self.tuda_prijava = Prijava.objects.create(
            korisnik=self.vol2_profil, akcija=self.akcija_aktivna,
            status=Prijava.Status.PRIHVACENA, br_sati=8,
        )

        self.url = reverse('volonter_panel')

    # ── Pristup ──────────────────────────────────────────────────────────────

    def test_volonter_vidi_panel(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'volonter_panel.html')

    def test_anoniman_ne_vidi_panel(self):
        odgovor = self.client.get(self.url)
        self.assertNotEqual(odgovor.status_code, 200)

    def test_sponzor_preusmeren_na_pocetnu(self):
        sponzor = Korisnik.objects.create_user(
            email='sp@primer.com', password='Lozinka1!',
            korisnicko_ime='sp', ime='Sara', prezime='Sarić')
        SponzorProfil.objects.create(
            korisnik=sponzor, naziv_organizacije='Sp doo',
            status=SponzorProfil.Status.ODOBREN)
        self.client.login(email='sp@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertRedirects(odgovor, reverse('home'))

    # ── Volonter vidi samo svoje prijave ─────────────────────────────────────

    def test_volonter_vidi_samo_svoje_tekuce(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        tekuce_pk = [p.pk for p in odgovor.context['tekuce_prijave']]
        self.assertNotIn(self.tuda_prijava.pk, tekuce_pk)

    def test_volonter_vidi_samo_svoju_istoriju(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        istorija_pk = [p.pk for p in odgovor.context['istorija_prijava']]
        self.assertNotIn(self.tuda_prijava.pk, istorija_pk)

    # ── Tekuće prijave (na_cekanju + prihvacena za aktivne akcije) ───────────

    def test_tekuce_sadrze_prijavu_na_cekanju(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        tekuce_pk = [p.pk for p in odgovor.context['tekuce_prijave']]
        self.assertIn(self.prijava_na_cekanju.pk, tekuce_pk)

    def test_tekuce_sadrze_prihvacenu_za_aktivnu_akciju(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        tekuce_pk = [p.pk for p in odgovor.context['tekuce_prijave']]
        self.assertIn(self.prijava_prihvacena.pk, tekuce_pk)

    def test_tekuce_ne_sadrze_odbijena(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        tekuce_pk = [p.pk for p in odgovor.context['tekuce_prijave']]
        self.assertNotIn(self.prijava_odbijena.pk, tekuce_pk)

    def test_tekuce_ne_sadrze_prijavu_za_zavrsenu_akciju(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        tekuce_pk = [p.pk for p in odgovor.context['tekuce_prijave']]
        self.assertNotIn(self.prijava_zavrsena_akcija.pk, tekuce_pk)

    # ── Istorija (odbijene + završene/otkazane akcije) ────────────────────────

    def test_istorija_sadrzi_odbijena(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        istorija_pk = [p.pk for p in odgovor.context['istorija_prijava']]
        self.assertIn(self.prijava_odbijena.pk, istorija_pk)

    def test_istorija_sadrzi_prijavu_za_otkazanu_akciju(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        istorija_pk = [p.pk for p in odgovor.context['istorija_prijava']]
        self.assertIn(self.prijava_zavrsena_akcija.pk, istorija_pk)

    def test_istorija_ne_sadrzi_tekuce(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        istorija_pk = [p.pk for p in odgovor.context['istorija_prijava']]
        self.assertNotIn(self.prijava_na_cekanju.pk, istorija_pk)
        self.assertNotIn(self.prijava_prihvacena.pk, istorija_pk)

    # ── Ukupan broj sati ──────────────────────────────────────────────────────

    def test_ukupno_sati_je_suma_prihvacenih(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        # prijava_prihvacena(6) + prijava_zavrsena_akcija(4) = 10
        self.assertEqual(odgovor.context['ukupno_sati'], 10)

    def test_ukupno_sati_ne_ukljucuje_na_cekanju_ni_odbijene(self):
        self.client.login(email='vol1@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url)
        self.assertNotEqual(odgovor.context['ukupno_sati'], 0)
        # Odbijene i na čekanju imaju br_sati=0, ali provera da
        # suma nije uvećana tuđim satima
        self.assertNotEqual(odgovor.context['ukupno_sati'], 18)

    # ── Login redirekcija za volontera ────────────────────────────────────────

    def test_volonter_se_loguje_na_panel(self):
        odgovor = self.client.post(
            reverse('prijava'),
            {'email': 'vol1@primer.com', 'lozinka': 'Lozinka1!'})
        self.assertRedirects(odgovor, self.url)


class KomentarTest(TestCase):
    """Testovi za SSU 12 — komentarisanje članaka."""

    def setUp(self):
        kategorija_clanka = KategorijaClanka.objects.create(naziv='Opšte')

        org_korisnik = Korisnik.objects.create_user(
            email='org@primer.com', password='Lozinka1!',
            korisnicko_ime='org_primer', ime='Org', prezime='Orgić')
        self.org_profil = OrganizatorProfil.objects.create(
            korisnik=org_korisnik,
            naziv_organizacije='Zeleni krug',
            status=OrganizatorProfil.Status.ODOBREN,
        )

        self.clanak = Clanak.objects.create(
            autor=self.org_profil,
            kategorija=kategorija_clanka,
            naslov='Test članak',
            tekst='Sadržaj test članka.',
            status=Clanak.Status.OBJAVLJEN,
        )

        self.volonter = Korisnik.objects.create_user(
            email='vol@primer.com', password='Lozinka1!',
            korisnicko_ime='vol_primer', ime='Ana', prezime='Anić')
        VolonterProfil.objects.create(korisnik=self.volonter)

        self.url_detalj = reverse('detalj_clanka', kwargs={'id_cla': self.clanak.pk})
        self.url_komentar = reverse('ajax_dodaj_komentar', kwargs={'id_cla': self.clanak.pk})

    def _ajax_post(self, tekst):
        return self.client.post(
            self.url_komentar,
            data=json.dumps({'tekst': tekst}),
            content_type='application/json',
        )

    # ── Prikaz detalja članka ────────────────────────────────────────────────

    def test_detalj_clanka_prikazuje_stranicu(self):
        odgovor = self.client.get(self.url_detalj)
        self.assertEqual(odgovor.status_code, 200)
        self.assertTemplateUsed(odgovor, 'detalj_clanka.html')
        self.assertContains(odgovor, 'Test članak')

    def test_detalj_clanka_sadrzi_tekst(self):
        odgovor = self.client.get(self.url_detalj)
        self.assertContains(odgovor, 'Sadržaj test članka.')

    def test_neobjavljen_clanak_vraca_404(self):
        clanak_na_cekanju = Clanak.objects.create(
            autor=self.org_profil,
            kategorija=Clanak.objects.first().kategorija,
            naslov='Na čekanju',
            tekst='Tekst.',
            status=Clanak.Status.NA_CEKANJU,
        )
        odgovor = self.client.get(
            reverse('detalj_clanka', kwargs={'id_cla': clanak_na_cekanju.pk}))
        self.assertEqual(odgovor.status_code, 404)

    # ── Ulogovan korisnik može da komentariše (SSU 12, 2.2.1) ───────────────

    def test_ulogovan_moze_da_komentarise(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self._ajax_post('Odličan članak!')
        self.assertEqual(odgovor.status_code, 200)
        data = json.loads(odgovor.content)
        self.assertIn('html', data)
        self.assertEqual(data['br_komentara'], 1)
        self.assertTrue(Komentar.objects.filter(
            clanak=self.clanak, korisnik=self.volonter
        ).exists())

    def test_komentar_se_cuva_sa_ispravnim_tekstom(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        self._ajax_post('Moj komentar')
        komentar = Komentar.objects.get(clanak=self.clanak)
        self.assertEqual(komentar.tekst, 'Moj komentar')
        self.assertEqual(komentar.korisnik, self.volonter)

    # ── Neulogovan korisnik ne može da komentariše (SSU 12, 2.2.2) ──────────

    def test_neulogovan_ne_moze_da_komentarise(self):
        odgovor = self._ajax_post('Komentar anonimnog')
        self.assertNotEqual(odgovor.status_code, 200)
        self.assertFalse(Komentar.objects.exists())

    def test_detalj_ne_prikazuje_formu_neulogovanom(self):
        odgovor = self.client.get(self.url_detalj)
        self.assertNotContains(odgovor, 'id="comment-input"')
        self.assertContains(odgovor, 'Prijavite se')

    def test_detalj_prikazuje_formu_ulogovanom(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self.client.get(self.url_detalj)
        self.assertContains(odgovor, 'id="comment-input"')

    # ── Error handling ───────────────────────────────────────────────────────

    def test_prazan_komentar_vraca_gresku(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self._ajax_post('')
        self.assertEqual(odgovor.status_code, 400)
        data = json.loads(odgovor.content)
        self.assertIn('error', data)
        self.assertFalse(Komentar.objects.exists())

    def test_whitespace_komentar_vraca_gresku(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        odgovor = self._ajax_post('   ')
        self.assertEqual(odgovor.status_code, 400)
        self.assertFalse(Komentar.objects.exists())

    # ── Lista komentara sortirana najnoviji prvi ─────────────────────────────

    def test_komentari_sortirani_najnoviji_prvi(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        Komentar.objects.create(clanak=self.clanak, korisnik=self.volonter, tekst='Prvi')
        Komentar.objects.create(clanak=self.clanak, korisnik=self.volonter, tekst='Drugi')
        odgovor = self.client.get(self.url_detalj)
        komentari = list(odgovor.context['komentari'])
        self.assertEqual(komentari[0].tekst, 'Drugi')
        self.assertEqual(komentari[1].tekst, 'Prvi')

    # ── Broj komentara se ažurira nakon Ajax slanja ──────────────────────────

    def test_ajax_vraca_ispravni_broj_komentara(self):
        self.client.login(email='vol@primer.com', password='Lozinka1!')
        self._ajax_post('Komentar 1')
        odgovor = self._ajax_post('Komentar 2')
        data = json.loads(odgovor.content)
        self.assertEqual(data['br_komentara'], 2)
