# Autor: Milica Milošević 0357/2023
"""
Pomoćne fabrike za pravljenje test podataka.

Nije test modul (ime ne počinje sa ``test``), pa ga Django test runner ne
prikuplja — samo se uvozi iz test fajlova radi kraćeg i čitljivijeg setup-a.
"""
import datetime

from main.models import (
    Korisnik, VolonterProfil, OrganizatorProfil, SponzorProfil,
    KategorijaAkcije, Akcija, KategorijaClanka, Clanak,
)

LOZINKA = 'Test1234!'


def _kor(email, ime, prezime):
    return Korisnik.objects.create_user(
        email=email, password=LOZINKA,
        korisnicko_ime=email.split('@')[0], ime=ime, prezime=prezime,
    )


def volonter(email, ime='Volonter', prezime='Testni'):
    """Kreira korisnika sa volonterskim profilom i vraća Korisnik-a."""
    k = _kor(email, ime, prezime)
    VolonterProfil.objects.create(korisnik=k)
    return k


def organizator(email, naziv='Test organizacija', status=OrganizatorProfil.Status.ODOBREN):
    """Kreira korisnika sa organizatorskim profilom (podrazumevano odobrenim)."""
    k = _kor(email, 'Organizator', 'Testni')
    OrganizatorProfil.objects.create(korisnik=k, naziv_organizacije=naziv, status=status)
    return k


def sponzor(email, naziv='Test sponzor', status=SponzorProfil.Status.ODOBREN):
    """Kreira korisnika sa sponzorskim profilom (podrazumevano odobrenim)."""
    k = _kor(email, 'Sponzor', 'Testni')
    SponzorProfil.objects.create(korisnik=k, naziv_organizacije=naziv, status=status)
    return k


def kat_akcije(naziv='Test kategorija akcije'):
    return KategorijaAkcije.objects.get_or_create(naziv=naziv)[0]


def kat_clanka(naziv='Test kategorija članka'):
    return KategorijaClanka.objects.get_or_create(naziv=naziv)[0]


def akcija(org, naziv='Test akcija', status=Akcija.Status.AKTIVNA, max_vol=5, kat=None):
    """Kreira akciju datog organizatora (Korisnik sa organizator_profil-om)."""
    return Akcija.objects.create(
        organizator=org.organizator_profil, kategorija=kat or kat_akcije(),
        naziv=naziv, opis='Opis test akcije.',
        datum=datetime.date.today() + datetime.timedelta(days=10),
        vreme=datetime.time(9, 0), lokacija='Beograd', max_br_volontera=max_vol,
        kontakt_email='kontakt@test.rs', kontakt_telefon='060123456', status=status,
    )


def clanak(org, naslov='Test članak', status=Clanak.Status.OBJAVLJEN, kat=None):
    """Kreira članak datog organizatora (autora)."""
    return Clanak.objects.create(
        autor=org.organizator_profil, kategorija=kat or kat_clanka(),
        naslov=naslov, tekst='Tekst test članka.', status=status,
    )
