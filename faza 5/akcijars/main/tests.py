import json

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Akcija,
    KategorijaAkcije,
    Korisnik,
    OrganizatorProfil,
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
        self.assertRedirects(odgovor, reverse('home'))
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
        self.assertRedirects(odgovor, reverse('home'))


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
