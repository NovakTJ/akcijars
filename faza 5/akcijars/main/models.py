from django.db import models
from django.db.models import Case, IntegerField, Value, When
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class _OstaloNaKrajuManager(models.Manager):
    """
    Default menadžer za kategorije: sortira abecedno, ali „Ostalo" uvek na
    dnu (bez obzira koliko je novih kategorija dodato ili kojim redom).
    """

    def get_queryset(self):
        return super().get_queryset().annotate(
            _ostalo=Case(
                When(naziv__iexact='Ostalo', then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('_ostalo', 'naziv')


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

    objects = _OstaloNaKrajuManager()

    class Meta:
        db_table = 'KategorijaAkcije'
        verbose_name = 'Kategorija akcije'
        verbose_name_plural = 'Kategorije akcija'

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
    # FZ 4.3.1 — geografske koordinate lokacije (za prikaz na Google Maps karti i
    # pretragu akcija po lokaciji). Opcione: popunjava ih Google Places autocomplete
    # pri kreiranju akcije; akcija bez koordinata se i dalje čuva (nema markera).
    geo_sirina = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Geografska širina',
        db_column='GeoSirina',
    )
    geo_duzina = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Geografska dužina',
        db_column='GeoDuzina',
    )
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
    def ima_koordinate(self):
        """True ako akcija ima geografske koordinate (za prikaz na mapi)."""
        return self.geo_sirina is not None and self.geo_duzina is not None

    @property
    def badge_klasa(self):
        return {
            self.Status.AKTIVNA: 'badge-green',
            self.Status.POPUNJENA: 'badge-warning',
            self.Status.ZAVRSENA: 'badge-gray',
            self.Status.OTKAZANA: 'badge-error',
        }.get(self.status, 'badge-gray')

    @property
    def broj_prihvacenih(self):
        return self.prijave.filter(status=Prijava.Status.PRIHVACENA).count()

    @property
    def slobodna_mesta(self):
        return max(0, self.max_br_volontera - self.broj_prihvacenih)


class FotografijaAkcije(models.Model):
    """
    Tabela FotografijaAkcije iz specifikacije baze (3.12) — fotografije vezane
    za akciju; može ih biti više po akciji.

    Napomena: spec.baze (3.12) definiše samo (IdFot, IdAkc, Putanja). Polje
    ``tip`` (pre/posle) dodato je zbog SSU 10 (slike pre i posle akcije) —
    svesna devijacija u odnosu na 3.12, po ugledu na Clanak.kategorija.
    """

    class Tip(models.TextChoices):
        PRE = 'pre', 'Pre akcije'
        POSLE = 'posle', 'Posle akcije'

    id_fot = models.AutoField(primary_key=True, db_column='IdFot')
    akcija = models.ForeignKey(
        Akcija,
        on_delete=models.CASCADE,
        related_name='fotografije',
        db_column='IdAkc',
        verbose_name='Akcija',
    )
    slika = models.ImageField(
        upload_to='akcije/',
        verbose_name='Fotografija',
        db_column='Putanja',
    )
    tip = models.CharField(
        max_length=10,
        choices=Tip.choices,
        default=Tip.PRE,
        verbose_name='Tip (pre/posle)',
        db_column='Tip',
    )

    class Meta:
        db_table = 'FotografijaAkcije'
        verbose_name = 'Fotografija akcije'
        verbose_name_plural = 'Fotografije akcija'

    def __str__(self):
        return f'Fotografija {self.id_fot} ({self.get_tip_display()}) — {self.akcija.naziv}'


class Prijava(models.Model):
    """Tabela PrijavaVolontera iz specifikacije baze (3.8)."""

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        PRIHVACENA = 'prihvacena', 'Prihvaćena'
        ODBIJENA = 'odbijena', 'Odbijena'

    korisnik = models.ForeignKey(
        VolonterProfil,
        on_delete=models.CASCADE,
        related_name='prijave',
        db_column='IdKor',
        verbose_name='Volonter',
    )
    akcija = models.ForeignKey(
        Akcija,
        on_delete=models.CASCADE,
        related_name='prijave',
        db_column='IdAkc',
        verbose_name='Akcija',
    )
    datum_prijave = models.DateField(
        default=timezone.now,
        editable=False,
        verbose_name='Datum prijave',
        db_column='DatumPrijave',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status',
        db_column='Status',
    )
    br_sati = models.PositiveIntegerField(
        default=0,
        verbose_name='Broj sati',
        db_column='BrSati',
    )

    class Meta:
        db_table = 'PrijavaVolontera'
        verbose_name = 'Prijava volontera'
        verbose_name_plural = 'Prijave volontera'
        unique_together = ('korisnik', 'akcija')
        ordering = ['-datum_prijave']

    def __str__(self):
        return f'{self.korisnik.korisnik.get_full_name()} → {self.akcija.naziv} ({self.get_status_display()})'


class KategorijaClanka(models.Model):
    """Kategorija članka (SSU 4, 2.2.3 — filter po kategoriji)."""

    id_kat = models.AutoField(primary_key=True, db_column='IdKat')
    naziv = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Naziv',
        db_column='Naziv',
    )

    objects = _OstaloNaKrajuManager()

    class Meta:
        db_table = 'KategorijaClanka'
        verbose_name = 'Kategorija članka'
        verbose_name_plural = 'Kategorije članaka'

    def __str__(self):
        return self.naziv


class Clanak(models.Model):
    """
    Tabela Clanak iz specifikacije baze (3.10).

    Napomena: spec.baze ne pominje kategoriju na članku; dodato je FK polje
    zbog SSU 4 (filter po kategoriji) — svesna deviacija u odnosu na 3.10.
    """

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        OBJAVLJEN = 'objavljen', 'Objavljen'
        ODBIJEN = 'odbijen', 'Odbijen'

    id_cla = models.AutoField(primary_key=True, db_column='IdCla')
    autor = models.ForeignKey(
        OrganizatorProfil,
        on_delete=models.CASCADE,
        related_name='clanci',
        db_column='IdKor',
        verbose_name='Autor',
    )
    kategorija = models.ForeignKey(
        KategorijaClanka,
        on_delete=models.PROTECT,
        related_name='clanci',
        db_column='IdKat',
        verbose_name='Kategorija',
    )
    naslov = models.CharField(max_length=200, verbose_name='Naslov', db_column='Naslov')
    tekst = models.TextField(verbose_name='Tekst', db_column='Tekst')
    datum_kreiranja = models.DateField(
        default=timezone.now,
        editable=False,
        verbose_name='Datum kreiranja',
        db_column='DatumKreiranja',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status',
        db_column='Status',
    )
    glavna_slika = models.ImageField(
        upload_to='clanci/',
        blank=True,
        null=True,
        verbose_name='Glavna slika (cover)',
    )

    class Meta:
        db_table = 'Clanak'
        verbose_name = 'Članak'
        verbose_name_plural = 'Članci'
        ordering = ['-datum_kreiranja']

    def __str__(self):
        return self.naslov


class SponzorskaPonuda(models.Model):
    """Ponuda sponzora za finansijsku podršku akciji (SSU 7)."""

    class Status(models.TextChoices):
        NA_CEKANJU = 'na_cekanju', 'Na čekanju'
        PRIHVACENA = 'prihvacena', 'Prihvaćena'
        ODBIJENA = 'odbijena', 'Odbijena'

    sponzor = models.ForeignKey(
        SponzorProfil,
        on_delete=models.CASCADE,
        related_name='ponude',
        db_column='IdKor',
        verbose_name='Sponzor',
    )
    akcija = models.ForeignKey(
        Akcija,
        on_delete=models.CASCADE,
        related_name='sponzorske_ponude',
        db_column='IdAkc',
        verbose_name='Akcija',
    )
    vrednost = models.PositiveIntegerField(
        verbose_name='Vrednost (EUR)',
        db_column='Vrednost',
    )
    opis = models.TextField(
        max_length=1024,
        verbose_name='Opis doprinosa',
        db_column='Opis',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NA_CEKANJU,
        verbose_name='Status',
        db_column='Status',
    )
    datum_slanja = models.DateField(
        auto_now_add=True,
        verbose_name='Datum slanja',
        db_column='DatumSlanja',
    )

    class Meta:
        db_table = 'SponzorskaPonuda'
        verbose_name = 'Sponzorska ponuda'
        verbose_name_plural = 'Sponzorske ponude'
        ordering = ['-datum_slanja']

    def __str__(self):
        return f'{self.sponzor.naziv_organizacije} → {self.akcija.naziv} ({self.get_status_display()})'


class SlikaClanka(models.Model):
    """Slike koje pripadaju članku (spec.baze 3.11) — može ih biti više po članku."""

    id_sli = models.AutoField(primary_key=True, db_column='IdSli')
    clanak = models.ForeignKey(
        Clanak,
        on_delete=models.CASCADE,
        related_name='slike',
        db_column='IdCla',
        verbose_name='Članak',
    )
    slika = models.ImageField(
        upload_to='clanci/',
        verbose_name='Slika',
        db_column='Putanja',
    )

    class Meta:
        db_table = 'SlikaClanka'
        verbose_name = 'Slika članka'
        verbose_name_plural = 'Slike članaka'

    def __str__(self):
        return f'Slika {self.id_sli} — {self.clanak.naslov}'


class Komentar(models.Model):
    """Komentar na članak (SSU 12)."""

    korisnik = models.ForeignKey(
        Korisnik,
        on_delete=models.CASCADE,
        related_name='komentari',
        db_column='IdKor',
        verbose_name='Korisnik',
    )
    clanak = models.ForeignKey(
        Clanak,
        on_delete=models.CASCADE,
        related_name='komentari',
        db_column='IdCla',
        verbose_name='Članak',
    )
    tekst = models.TextField(verbose_name='Tekst', db_column='Tekst')
    datum_komentara = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Datum komentara',
        db_column='DatumKomentara',
    )

    class Meta:
        db_table = 'Komentar'
        verbose_name = 'Komentar'
        verbose_name_plural = 'Komentari'
        ordering = ['-datum_komentara']

    def __str__(self):
        return f'{self.korisnik.get_full_name()} → {self.clanak.naslov}'