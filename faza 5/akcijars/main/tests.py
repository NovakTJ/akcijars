from django.test import TestCase
from django.urls import reverse

from .models import (
    Korisnik,
    VolonterProfil,
    OrganizatorProfil,
    SponzorProfil,
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
