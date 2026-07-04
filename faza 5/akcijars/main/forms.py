import re

from django import forms
from django.contrib.auth import authenticate
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.text import slugify

from .models import (
    Akcija,
    Komentar,
    Korisnik,
    VolonterProfil,
    OrganizatorProfil,
    SponzorProfil,
    SponzorskaPonuda,
)


# Specijalni karakteri koji se priznaju u lozinki (uključuje i cifre).
SPECIJALNI_KARAKTERI = r"[\d!@#$%^&*()_\-+=\[\]{};:'\",.<>?/\\|`~]"

# Telefon sme da sadrži samo cifre, razmake, + i -.
TELEFON_RE = re.compile(r'^[0-9 +\-]+$')


class RegistracijaForm(forms.Form):
    """
    Forma za registraciju korisnika (SSU 1).

    Sva polja su deklarisana kao ``required=False`` kako bismo sami
    kontrolisali poruke o greškama i reprodukovali tačne tekstove iz SSU 1
    (npr. jedinstvenu poruku „Nisu uneta sva obavezna polja.“ umesto
    Django podrazumevanih poruka po polju).
    """

    class Uloga(models.TextChoices):
        VOLONTER = 'volonter', 'Volonter'
        ORGANIZATOR = 'organizator', 'Organizator'
        SPONZOR = 'sponzor', 'Sponzor'

    ime = forms.CharField(max_length=50, required=False)
    prezime = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=254, required=False)
    lozinka = forms.CharField(required=False)
    lozinka2 = forms.CharField(required=False)
    uloga = forms.ChoiceField(
        choices=Uloga.choices,
        required=False,
    )
    naziv_organizacije = forms.CharField(max_length=100, required=False)
    br_telefona = forms.CharField(max_length=20, required=False)

    @property
    def trazi_organizaciju(self):
        """True ako izabrana uloga zahteva naziv organizacije i telefon."""
        uloga = self.data.get('uloga') or self.initial.get('uloga')
        return uloga in (self.Uloga.ORGANIZATOR, self.Uloga.SPONZOR)

    def clean(self):
        cleaned = super().clean()

        ime = cleaned.get('ime', '')
        prezime = cleaned.get('prezime', '')
        email = cleaned.get('email', '')
        lozinka = cleaned.get('lozinka', '')
        lozinka2 = cleaned.get('lozinka2', '')
        uloga = cleaned.get('uloga', '')
        naziv_organizacije = cleaned.get('naziv_organizacije', '')
        br_telefona = cleaned.get('br_telefona', '')

        je_org_ili_sponzor = uloga in (self.Uloga.ORGANIZATOR, self.Uloga.SPONZOR)

        # 2.2.6 — nepopunjena obavezna polja (jedinstvena globalna poruka).
        obavezna = [ime, prezime, email, lozinka, lozinka2, uloga]
        if je_org_ili_sponzor:
            obavezna += [naziv_organizacije, br_telefona]
        if not all(obavezna):
            raise ValidationError('Nisu uneta sva obavezna polja.')

        # 2.2.3 — neispravan format email adrese.
        format_ispravan = True
        try:
            validate_email(email)
        except ValidationError:
            format_ispravan = False
            self.add_error('email', 'Email adresa nije ispravnog formata.')

        # 2.2.5 — email adresa već postoji.
        if format_ispravan and Korisnik.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'Korisnik sa tom email adresom već postoji.')

        # 2.2.7 — lozinka ne zadovoljava minimalne uslove.
        if len(lozinka) < 8 or not re.search(SPECIJALNI_KARAKTERI, lozinka):
            self.add_error(
                'lozinka',
                'Lozinka mora imati najmanje 8 karaktera i sadržati barem '
                'jednu cifru ili specijalni karakter.',
            )

        # 2.2.4 — lozinke se ne poklapaju.
        if lozinka and lozinka2 and lozinka != lozinka2:
            self.add_error('lozinka2', 'Lozinke se ne poklapaju.')

        # Format kontakt telefona (samo za organizatora/sponzora).
        if je_org_ili_sponzor and br_telefona and not TELEFON_RE.match(br_telefona):
            self.add_error('br_telefona', 'Kontakt telefon nije ispravnog formata.')

        return cleaned

    def _generisi_korisnicko_ime(self, email):
        """
        Generiše jedinstveno korisničko ime iz lokalnog dela email adrese.

        SSU 1 ne traži korisničko ime od korisnika, ali ga model zahteva kao
        jedinstveno polje, pa ga izvodimo iz email-a i po potrebi dodajemo
        redni broj dok ne postane jedinstveno.
        """
        osnova = slugify(email.split('@')[0]) or 'korisnik'
        osnova = osnova[:40]
        kandidat = osnova
        i = 1
        while Korisnik.objects.filter(korisnicko_ime=kandidat).exists():
            sufiks = str(i)
            kandidat = f'{osnova[:50 - len(sufiks)]}{sufiks}'
            i += 1
        return kandidat

    def sacuvaj(self):
        """Kreira korisnika i odgovarajući profil. Vraća (korisnik, uloga)."""
        podaci = self.cleaned_data
        uloga = podaci['uloga']
        email = self.fields['email'].to_python(podaci['email'])

        korisnik = Korisnik.objects.create_user(
            email=email,
            password=podaci['lozinka'],
            korisnicko_ime=self._generisi_korisnicko_ime(email),
            ime=podaci['ime'],
            prezime=podaci['prezime'],
        )

        if uloga == self.Uloga.VOLONTER:
            VolonterProfil.objects.create(korisnik=korisnik)
        elif uloga == self.Uloga.ORGANIZATOR:
            OrganizatorProfil.objects.create(
                korisnik=korisnik,
                naziv_organizacije=podaci['naziv_organizacije'],
                br_telefona=podaci['br_telefona'],
            )
        elif uloga == self.Uloga.SPONZOR:
            SponzorProfil.objects.create(
                korisnik=korisnik,
                naziv_organizacije=podaci['naziv_organizacije'],
                br_telefona=podaci['br_telefona'],
            )

        return korisnik, uloga


class SponzorskaPonudaForm(forms.ModelForm):
    class Meta:
        model = SponzorskaPonuda
        fields = ['akcija', 'vrednost', 'opis']
        widgets = {
            'akcija': forms.HiddenInput(),
            'vrednost': forms.NumberInput(attrs={'min': 1, 'placeholder': 'npr. 500'}),
            'opis': forms.Textarea(attrs={'rows': 4, 'maxlength': 1024, 'placeholder': 'Opišite vaš doprinos…'}),
        }
        labels = {
            'vrednost': 'Vrednost (EUR)',
            'opis': 'Opis doprinosa',
        }

    def clean_vrednost(self):
        vrednost = self.cleaned_data.get('vrednost')
        if vrednost is not None and vrednost < 1:
            raise forms.ValidationError('Vrednost mora biti pozitivan broj.')
        return vrednost


class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ['tekst']
        widgets = {
            'tekst': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Napišite komentar...',
                'class': 'form-control',
                'id': 'comment-input',
            }),
        }
        labels = {'tekst': 'Vaš komentar'}

    def clean_tekst(self):
        tekst = self.cleaned_data.get('tekst', '').strip()
        if not tekst:
            raise forms.ValidationError('Komentar ne može biti prazan!')
        return tekst


class PrijavaForm(forms.Form):
    """
    Forma za prijavu korisnika (SSU 2).

    Polja su ``required=False`` da bismo sami kontrolisali poruke i
    reprodukovali tačne tekstove iz SSU 2 (npr. jedinstvenu poruku
    „Email adresa ili lozinka nisu ispravni.“ i za nepostojeći email i za
    pogrešnu lozinku, tako da se ne otkriva da li email postoji).

    Po uspešnoj validaciji autentifikovani ``Korisnik`` je dostupan kao
    ``self.korisnik``.
    """

    email = forms.CharField(max_length=254, required=False)
    lozinka = forms.CharField(required=False)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email', '')
        lozinka = cleaned.get('lozinka', '')

        # Nepopunjena obavezna polja.
        if not email or not lozinka:
            raise ValidationError('Nisu uneta sva obavezna polja.')

        # 2.2.2 / 2.2.3 — nepostojeći email ili pogrešna lozinka daju istu
        # poruku (neaktivan nalog takođe vraća None).
        # Email se normalizuje pre pretrage: SQLite je case-sensitive za =,
        # a korisnici su sačuvani sa malim slovima (normalize_email u create_user).
        korisnik = authenticate(email=email.lower(), password=lozinka)
        if korisnik is None:
            raise ValidationError('Email adresa ili lozinka nisu ispravni.')

        # 2.2.4 — nalog organizatora/sponzora još nije odobren od strane
        # administratora (pokriva i odbijene naloge).
        if not korisnik.je_odobren:
            raise ValidationError('Nalog čeka odobrenje administratora.')

        self.korisnik = korisnik
        return cleaned
