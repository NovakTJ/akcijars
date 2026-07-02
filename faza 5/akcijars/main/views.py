from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .emails import posalji_potvrdu_registracije
from .forms import PrijavaForm, RegistracijaForm
from .models import Akcija, KategorijaAkcije


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

    q = request.GET.get('q', '').strip()
    kategorija = request.GET.get('kategorija', '').strip()
    status = request.GET.get('status', '').strip()
    datum = request.GET.get('datum', '').strip()

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

    # ako treba da se menja broj akcija po strani samo promeni broj na kraju sledeceg reda
    paginator = Paginator(akcije.distinct().order_by('-datum_kreiranja'), 18)
    strana = paginator.get_page(request.GET.get('page'))

    kontekst = {
        'akcije': strana.object_list,
        'strana': strana,
        'kategorije': KategorijaAkcije.objects.all(),
        'statusi': [
            (Akcija.Status.AKTIVNA, Akcija.Status.AKTIVNA.label),
            (Akcija.Status.POPUNJENA, Akcija.Status.POPUNJENA.label),
            (Akcija.Status.ZAVRSENA, Akcija.Status.ZAVRSENA.label),
            (Akcija.Status.OTKAZANA, Akcija.Status.OTKAZANA.label),
        ],
        'filteri': {'q': q, 'kategorija': kategorija, 'status': status, 'datum': datum},
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, '_akcije_grid.html', kontekst)
    return render(request, 'akcije.html', kontekst)

def _uskoro(request):
    """Privremeni placeholder dok se ne implementiraju odgovarajući commitovi."""
    return render(request, 'uskoro.html')
