from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class KorisnikManager(BaseUserManager):
    """Menadžer koji koristi email umesto username-a."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email adresa je obavezna.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        AdministratorProfil.objects.create(korisnik=user)
        return user


class Korisnik(AbstractBaseUser, PermissionsMixin):
    """
    Tabela Korisnik iz specifikacije baze.
    Uloga se određuje po tome koji profil postoji (Volonter/Organizator/Sponzor/Administrator).
    """

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email adresa',
    )
    korisnicko_ime = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Korisničko ime',
        db_column='KorisnickoIme',
    )
    ime = models.CharField(max_length=50, verbose_name='Ime', db_column='Ime')
    prezime = models.CharField(max_length=50, verbose_name='Prezime', db_column='Prezime')
    datum_registracije = models.DateField(
        default=timezone.now,
        editable=False,
        verbose_name='Datum registracije',
        db_column='DatumRegistracije',
    )

    is_active = models.BooleanField(default=True, verbose_name='Aktivan nalog')
    is_staff = models.BooleanField(default=False, verbose_name='Pristup admin panelu')

    objects = KorisnikManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['korisnicko_ime', 'ime', 'prezime']

    class Meta:
        db_table = 'Korisnik'
        verbose_name = 'Korisnik'
        verbose_name_plural = 'Korisnici'

    def __str__(self):
        return f'{self.ime} {self.prezime} ({self.email})'

    def get_full_name(self):
        return f'{self.ime} {self.prezime}'.strip()

    def get_short_name(self):
        return self.ime

    @property
    def je_volonter(self):
        return hasattr(self, 'volonter_profil')

    @property
    def je_organizator(self):
        return hasattr(self, 'organizator_profil')

    @property
    def je_sponzor(self):
        return hasattr(self, 'sponzor_profil')

    @property
    def je_admin(self):
        return hasattr(self, 'administrator_profil')

    @property
    def je_odobren(self):
        """Da li korisnik može da koristi sistem u punom kapacitetu."""
        if self.je_volonter or self.je_admin:
            return True
        if self.je_organizator:
            return self.organizator_profil.status == OrganizatorProfil.Status.ODOBREN
        if self.je_sponzor:
            return self.sponzor_profil.status == SponzorProfil.Status.ODOBREN
        return False

    @property
    def ceka_odobrenje(self):
        """True za org/sponzora čiji nalog još nije odobren ili odbijen."""
        if self.je_organizator:
            return self.organizator_profil.status == OrganizatorProfil.Status.NA_CEKANJU
        if self.je_sponzor:
            return self.sponzor_profil.status == SponzorProfil.Status.NA_CEKANJU
        return False

class VolonterProfil(models.Model):
    """Tabela Volonter iz specifikacije baze."""

    korisnik = models.OneToOneField(
        Korisnik,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='volonter_profil',
        db_column='IdKor',
    )
    ukupno_sati = models.PositiveIntegerField(
        default=0,
        verbose_name='Ukupno volonterskih sati',
        db_column='UkupnoSati',
    )
    prima_preporuke = models.BooleanField(
        default=False,
        verbose_name='Prima preporuke akcija emailom',
        db_column='PrimaPreporuke',
    )

    class Meta:
        db_table = 'Volonter'
        verbose_name = 'Volonter profil'
        verbose_name_plural = 'Volonter profili'

    def __str__(self):
        return f'Volonter: {self.korisnik.get_full_name()}'


class OrganizatorProfil(models.Model):
    """Tabela Organizator iz specifikacije baze."""

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        ODOBREN = 'odobren', 'Odobren'
        ODBIJEN = 'odbijen', 'Odbijen'

    korisnik = models.OneToOneField(
        Korisnik,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='organizator_profil',
        db_column='IdKor',
    )
    br_telefona = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='Broj telefona',
        db_column='BrTelefona',
    )
    naziv_organizacije = models.CharField(
        max_length=100,
        verbose_name='Naziv organizacije',
        db_column='NazivOrganizacije',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status naloga',
        db_column='Status',
    )

    class Meta:
        db_table = 'Organizator'
        verbose_name = 'Organizator profil'
        verbose_name_plural = 'Organizator profili'

    def __str__(self):
        return f'Organizator: {self.naziv_organizacije} ({self.get_status_display()})'


class SponzorProfil(models.Model):
    """Tabela Sponzor iz specifikacije baze."""

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        ODOBREN = 'odobren', 'Odobren'
        ODBIJEN = 'odbijen', 'Odbijen'

    korisnik = models.OneToOneField(
        Korisnik,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='sponzor_profil',
        db_column='IdKor',
    )
    br_telefona = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='Broj telefona',
        db_column='BrTelefona',
    )
    naziv_organizacije = models.CharField(
        max_length=100,
        verbose_name='Naziv organizacije',
        db_column='NazivOrganizacije',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status naloga',
        db_column='Status',
    )

    class Meta:
        db_table = 'Sponzor'
        verbose_name = 'Sponzor profil'
        verbose_name_plural = 'Sponzor profili'

    def __str__(self):
        return f'Sponzor: {self.naziv_organizacije} ({self.get_status_display()})'


class AdministratorProfil(models.Model):
    """Tabela Administrator iz specifikacije baze (samo FK na Korisnika)."""

    korisnik = models.OneToOneField(
        Korisnik,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='administrator_profil',
        db_column='IdKor',
    )

    class Meta:
        db_table = 'Administrator'
        verbose_name = 'Administrator profil'
        verbose_name_plural = 'Administrator profili'

    def __str__(self):
        return f'Administrator: {self.korisnik.get_full_name()}'


class KategorijaAkcije(models.Model):
    """Tabela KategorijaAkcije iz specifikacije baze."""

    id_kat = models.AutoField(primary_key=True, db_column='IdKat')
    naziv = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Naziv',
        db_column='Naziv',
    )

    class Meta:
        db_table = 'KategorijaAkcije'
        verbose_name = 'Kategorija akcije'
        verbose_name_plural = 'Kategorije akcija'
        ordering = ['naziv']

    def __str__(self):
        return self.naziv


class Akcija(models.Model):
    """Tabela Akcija iz specifikacije baze."""

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        ODOBRENA = 'odobrena', 'Odobrena'
        ODBIJENA = 'odbijena', 'Odbijena'
        AKTIVNA = 'aktivna', 'Otvorena'
        POPUNJENA = 'popunjena', 'Popunjena'
        ZAVRSENA = 'zavrsena', 'Završena'
        OTKAZANA = 'otkazana', 'Otkazana'

    id_akc = models.AutoField(primary_key=True, db_column='IdAkc')
    organizator = models.ForeignKey(
        OrganizatorProfil,
        on_delete=models.CASCADE,
        related_name='akcije',
        db_column='IdKor',
        verbose_name='Organizator',
    )
    kategorija = models.ForeignKey(
        KategorijaAkcije,
        on_delete=models.PROTECT,
        related_name='akcije',
        db_column='IdKat',
        verbose_name='Kategorija',
    )
    naziv = models.CharField(max_length=100, verbose_name='Naziv', db_column='Naziv')
    opis = models.CharField(max_length=1024, verbose_name='Opis', db_column='Opis')
    datum = models.DateField(verbose_name='Datum', db_column='Datum')
    vreme = models.TimeField(verbose_name='Vreme', db_column='Vreme')
    lokacija = models.CharField(max_length=50, verbose_name='Lokacija', db_column='Lokacija')
    max_br_volontera = models.PositiveIntegerField(
        verbose_name='Maksimalan broj volontera',
        db_column='MaxBrVolontera',
    )
    kontakt_email = models.EmailField(
        max_length=50,
        verbose_name='Kontakt email',
        db_column='KontaktEmail',
    )
    kontakt_telefon = models.CharField(
        max_length=20,
        verbose_name='Kontakt telefon',
        db_column='KontaktTelefon',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status',
        db_column='Status',
    )
    datum_kreiranja = models.DateField(
        default=timezone.now,
        editable=False,
        verbose_name='Datum kreiranja',
        db_column='DatumKreiranja',
    )
    slika = models.ImageField(
        upload_to='akcije/',
        blank=True,
        null=True,
        verbose_name='Slika',
        db_column='Slika',
    )

    class Meta:
        db_table = 'Akcija'
        verbose_name = 'Akcija'
        verbose_name_plural = 'Akcije'
        ordering = ['-datum_kreiranja']

    def __str__(self):
        return self.naziv

    @property
    def badge_klasa(self):
        return {
            self.Status.AKTIVNA: 'badge-green',
            self.Status.POPUNJENA: 'badge-warning',
            self.Status.ZAVRSENA: 'badge-gray',
            self.Status.OTKAZANA: 'badge-error',
        }.get(self.status, 'badge-gray')