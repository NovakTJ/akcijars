from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

from .emails import posalji_potvrdu_registracije
from .forms import PrijavaForm, RegistracijaForm


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


def _uskoro(request):
    """Privremeni placeholder dok se ne implementiraju odgovarajući commitovi."""
    return render(request, 'uskoro.html')
