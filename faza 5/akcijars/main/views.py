import re

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404


# SSU 3, otvoreno pitanje 2 — dozvoljena slova (uklj. srpske), cifre, razmaci.
_DOZVOLJEN_UPIT = re.compile(r'^[a-zA-ZčćžšđČĆŽŠĐ0-9 ]*$')


def _brojevi_paginacije(strana):
    """
    SSU 3, otvoreno pitanje 2 — kompaktna paginacija: 1, prethodna, trenutna,
    sledeća, poslednja, bez dupliranja; None = elipse „…".
    """
    ukupno = strana.paginator.num_pages
    trenutna = strana.number
    kljucni = sorted({1, trenutna - 1, trenutna, trenutna + 1, ukupno}
                     & set(range(1, ukupno + 1)))
    rezultat = []
    for i, broj in enumerate(kljucni):
        if i > 0 and broj - kljucni[i - 1] > 1:
            rezultat.append(None)
        rezultat.append(broj)
    return rezultat

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST

from .emails import posalji_potvrdu_registracije
from .forms import PrijavaForm, RegistracijaForm
from .models import Akcija, KategorijaAkcije, Prijava


def home(request):
    """Stub početna stranica — sadržaj dodaje Novak/Maša u kasnijim commitima."""
    return render(request, 'home.html')


def _pocetna_za_korisnika(korisnik):
    """
    Vraća naziv rute lične stranice u zavisnosti od uloge (SSU 2, 2.2.1).

    Kontrolne table po ulogama (volonter/organizator/sponzor/admin) još nisu
    implementirane, pa sve uloge za sada vode na početnu; ovde se uvode prave
    rute kad odgovarajući paneli budu gotovi.
    """
    return 'home'


def registracija(request):
    """
    Registracija korisnika (SSU 1).

    Preduslov: ulogovan korisnik se preusmerava na početnu — njemu se
    opcija registracije ne prikazuje.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistracijaForm(request.POST)
        if form.is_valid():
            korisnik, uloga = form.sacuvaj()
            if uloga == RegistracijaForm.Uloga.VOLONTER:
                poruka = 'Registracija je uspešna. Možete se prijaviti na sistem.'
            else:
                poruka = ('Registracija je uspešna. Nalog čeka odobrenje '
                          'jednog od administratora.')
            # SSU 1, 2.2.1/2.2.2 — potvrda registracije se šalje na email.
            posalji_potvrdu_registracije(korisnik, uloga)
            return render(request, 'registracija.html', {
                'uspeh': True,
                'poruka': poruka,
                'uloga': uloga,
            })
        uloga = form.data.get('uloga') or RegistracijaForm.Uloga.VOLONTER
    else:
        uloga = request.GET.get('uloga')
        if uloga not in RegistracijaForm.Uloga.values:
            uloga = RegistracijaForm.Uloga.VOLONTER
        form = RegistracijaForm(initial={'uloga': uloga})

    return render(request, 'registracija.html', {
        'form': form,
        'uloga': uloga,
    })


def prijava(request):
    """
    Prijava korisnika (SSU 2).

    Preduslov: ulogovan korisnik se preusmerava na ličnu stranicu — njemu se
    forma za prijavu ne prikazuje.
    """
    if request.user.is_authenticated:
        return redirect(_pocetna_za_korisnika(request.user))

    if request.method == 'POST':
        form = PrijavaForm(request.POST)
        if form.is_valid():
            # 2.2.1 — uspešna autorizacija: kreira se sesija i korisnik se
            # preusmerava na ličnu stranicu prema svojoj ulozi.
            auth_login(request, form.korisnik)
            return redirect(_pocetna_za_korisnika(form.korisnik))
    else:
        form = PrijavaForm()

    return render(request, 'prijava.html', {'form': form})


def odjava(request):
    """Odjava korisnika (SSU 2, 2.2.5) — gasi sesiju i vodi na početnu."""
    auth_logout(request)
    return redirect('home')

def lista_akcija(request):
    """Lista svih akcija sa filterima (SSU 3 / 5.3)."""
    akcije = Akcija.objects.select_related('organizator', 'kategorija').all()

    q = request.GET.get('q', '').strip()[:64]
    kategorija = request.GET.get('kategorija', '').strip()
    status = request.GET.get('status', '').strip()
    datum = request.GET.get('datum', '').strip()
    sortiranje = request.GET.get('sort', 'datum_kacenja')

    # SSU 3, 2.2.11 — neispravan upit se odbija, prikazuje se početni prikaz.
    greska_upita = ''
    if q and not _DOZVOLJEN_UPIT.match(q):
        greska_upita = 'U upitu su dozvoljeni samo slova, cifre i razmaci.'
        q = ''

    if q:
        akcije = akcije.filter(naziv__icontains=q) | akcije.filter(
            organizator__naziv_organizacije__icontains=q
        )
    if kategorija:
        akcije = akcije.filter(kategorija_id=kategorija)
    if status:
        akcije = akcije.filter(status=status)
    if datum:
        akcije = akcije.filter(datum=datum)

    # SSU 3, 2.2.8 — sortiranje. 'najblize' i 'slobodna_mesta' zavise od
    # tuđih komitova (#12 lokacija — Novak, #15 model Prijava — Maša),
    # do tada su u UI-u kao disabled opcije.
    poredak = {
        'datum_kacenja': '-datum_kreiranja',
        'datum_odrzavanja': '-datum',
    }.get(sortiranje, '-datum_kreiranja')

    # SSU 3, otvoreno pitanje 1 — numActionsPerPage = 9.
    paginator = Paginator(akcije.distinct().order_by(poredak), 9)
    strana = paginator.get_page(request.GET.get('page'))

    kontekst = {
        'akcije': strana.object_list,
        'strana': strana,
        'brojevi_paginacije': _brojevi_paginacije(strana),
        'greska_upita': greska_upita,
        'kategorije': KategorijaAkcije.objects.all(),
        'statusi': [
            (Akcija.Status.AKTIVNA, Akcija.Status.AKTIVNA.label),
            (Akcija.Status.POPUNJENA, Akcija.Status.POPUNJENA.label),
            (Akcija.Status.ZAVRSENA, Akcija.Status.ZAVRSENA.label),
            (Akcija.Status.OTKAZANA, Akcija.Status.OTKAZANA.label),
        ],
        'filteri': {'q': q, 'kategorija': kategorija, 'status': status, 'datum': datum},
        'sortiranje': sortiranje,
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, '_akcije_grid.html', kontekst)
    return render(request, 'akcije.html', kontekst)

def _moja_prijava(korisnik, akcija):
    """Vraća Prijavu ulogovanog volontera za datu akciju, ili None."""
    if not korisnik.is_authenticated or not korisnik.je_volonter:
        return None
    return Prijava.objects.filter(
        korisnik=korisnik.volonter_profil, akcija=akcija
    ).first()


def detalj_akcije(request, id_akc):
    """Detalj pojedinačne akcije (SSU 3, 2.2.1)."""
    akcija = get_object_or_404(
        Akcija.objects.select_related('organizator', 'kategorija'),
        pk=id_akc,
    )
    return render(request, 'detalj_akcije.html', {
        'akcija': akcija,
        'moja_prijava': _moja_prijava(request.user, akcija),
    })


@login_required
@require_POST
def prijavi_se(request, id_akc):
    """Volonter se prijavljuje na akciju (SSU 6, 2.2.1). Vraća sidebar fragment."""
    if not request.user.je_volonter:
        return HttpResponseForbidden('Samo volonteri mogu da se prijave.')
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if akcija.status != Akcija.Status.AKTIVNA:
        return HttpResponseBadRequest('Prijava na ovu akciju nije moguća.')
    Prijava.objects.get_or_create(
        korisnik=request.user.volonter_profil,
        akcija=akcija,
        defaults={'status': Prijava.Status.NA_CEKANJU},
    )
    return render(request, '_prijava_sidebar.html', {
        'akcija': akcija,
        'moja_prijava': _moja_prijava(request.user, akcija),
    })


@login_required
@require_POST
def odjavi_se(request, id_akc):
    """
    Volonter se odjavljuje sa akcije (SSU 6, 2.2.2 i 2.2.3).
    Odbijena prijava je konačna — ne dozvoljava se brisanje.
    """
    if not request.user.je_volonter:
        return HttpResponseForbidden('Samo volonteri mogu da se odjave.')
    akcija = get_object_or_404(Akcija, pk=id_akc)
    prijava = Prijava.objects.filter(
        korisnik=request.user.volonter_profil, akcija=akcija
    ).first()
    if prijava and prijava.status != Prijava.Status.ODBIJENA:
        prijava.delete()
    return render(request, '_prijava_sidebar.html', {
        'akcija': akcija,
        'moja_prijava': _moja_prijava(request.user, akcija),
    })


def _uskoro(request):
    """Privremeni placeholder dok se ne implementiraju odgovarajući commitovi."""
    return render(request, 'uskoro.html')
