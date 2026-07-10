import json
import math
import re

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST


# SSU 3, otvoreno pitanje 2 — dozvoljena slova (uklj. srpske), cifre, razmaci.
_DOZVOLJEN_UPIT = re.compile(r'^[a-zA-ZčćžšđČĆŽŠĐ0-9 ]*$')

# SSU 3, 2.2.6 — dozvoljeni radijusi pretrage po lokaciji (km); podrazumevano 25.
_RADIUSI = (5, 10, 25, 50)


def _parsiraj_koord(vrednost):
    """Parsira string koordinate u float; vraća None za prazan/neispravan unos."""
    if not vrednost:
        return None
    try:
        return float(vrednost)
    except (TypeError, ValueError):
        return None


def _parsiraj_radius(vrednost):
    """Radijus pretrage u km; vraća podrazumevanih 25 za nevalidan unos."""
    try:
        r = int(vrednost)
    except (TypeError, ValueError):
        return 25
    return r if r in _RADIUSI else 25


def _haversine_km(lat1, lng1, lat2, lng2):
    """Rastojanje između dve tačke na Zemlji (haversine formula), u kilometrima."""
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(d_lng / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


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

from .emails import (
    posalji_izmenu_akcije,
    posalji_obavestenje_volonterima,
    posalji_odbijanje_naloga,
    posalji_odbijanje_prijave,
    posalji_odobrenje_naloga,
    posalji_otkazivanje_akcije,
    posalji_potvrdu_registracije,
    posalji_prihvatanje_prijave,
)
from .forms import (
    AkcijaForm,
    ClanakForma,
    KomentarForm,
    PrijavaForm,
    RegistracijaForm,
    SponzorskaPonudaForm,
)
from .models import (
    Akcija,
    Clanak,
    FotografijaAkcije,
    KategorijaAkcije,
    KategorijaClanka,
    Komentar,
    Korisnik,
    OrganizatorProfil,
    Prijava,
    SlikaClanka,
    SponzorProfil,
    SponzorskaPonuda,
)


def home(request):
    """Stub početna stranica — sadržaj dodaje Novak/Maša u kasnijim commitima."""
    return render(request, 'home.html')


def _pocetna_za_korisnika(korisnik):
    """
    Vraća naziv rute lične stranice u zavisnosti od uloge (SSU 2, 2.2.1).
    """
    if korisnik.je_admin:
        return 'admin_panel'
    if korisnik.je_sponzor:
        return 'sponzor_panel'
    if korisnik.je_volonter:
        return 'volonter_panel'
    if korisnik.je_organizator:
        return 'organizator_panel'
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

    # SSU 3, 2.2.6 — pretraga po lokaciji. Google Places (client-side) daje
    # koordinate izabranog mesta; radijus filtriramo haversine formulom na
    # serveru. Akcije bez koordinata se izostavljaju iz geo-pretrage.
    lok = request.GET.get('lok', '').strip()[:120]
    lat = _parsiraj_koord(request.GET.get('lat'))
    lng = _parsiraj_koord(request.GET.get('lng'))
    radius = _parsiraj_radius(request.GET.get('radius'))
    lokacija_aktivna = lat is not None and lng is not None

    # SSU 3, 2.2.8 — sortiranje. 'najblize' je dostupno samo kada je izabrana
    # lokacija; 'slobodna_mesta' zavisi od modela Prijava (#15) i za sada je u
    # UI-u kao disabled opcija.
    poredak = {
        'datum_kacenja': '-datum_kreiranja',
        'datum_odrzavanja': '-datum',
    }.get(sortiranje, '-datum_kreiranja')

    akcije = akcije.distinct().order_by(poredak)

    if lokacija_aktivna:
        # Materijalizujemo listu, računamo distancu i zadržavamo akcije unutar
        # radijusa. „Najbliže" (2.2.8) sortira po izračunatoj distanci.
        stavke = []
        for akc in akcije:
            if not akc.ima_koordinate:
                continue
            d = _haversine_km(lat, lng, akc.geo_sirina, akc.geo_duzina)
            if d <= radius:
                akc.distanca = round(d, 1)
                stavke.append(akc)
        if sortiranje == 'najblize':
            stavke.sort(key=lambda a: a.distanca)
        # SSU 3, otvoreno pitanje 1 — numActionsPerPage = 9.
        paginator = Paginator(stavke, 9)
    else:
        # SSU 3, otvoreno pitanje 1 — numActionsPerPage = 9.
        paginator = Paginator(akcije, 9)

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
        'filteri': {
            'q': q, 'kategorija': kategorija, 'status': status, 'datum': datum,
            'lok': lok, 'lat': request.GET.get('lat', ''),
            'lng': request.GET.get('lng', ''), 'radius': radius,
        },
        'radiusi': _RADIUSI,
        'lokacija_aktivna': lokacija_aktivna,
        'sortiranje': sortiranje,
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, '_akcije_grid.html', kontekst)
    return render(request, 'akcije.html', kontekst)

@login_required
def kreiraj_akciju(request):
    """
    Kreiranje akcije (SSU 5).

    Preduslov (2.4): korisnik je ulogovan u ulogu organizatora. Kreirana akcija
    dobija status „na čekanju" i čeka odobrenje administratora (2.5).
    """
    if not request.user.je_organizator or not request.user.je_odobren:
        return redirect('home')

    if request.method == 'POST':
        form = AkcijaForm(request.POST, request.FILES)
        if form.is_valid():
            # 2.2.1 — uspešno kreiranje: akcija se čuva sa statusom „na čekanju"
            # i vezuje za ulogovanog organizatora.
            akcija = form.save(commit=False)
            akcija.organizator = request.user.organizator_profil
            akcija.status = Akcija.Status.NA_CEKANJU
            akcija.save()
            messages.success(
                request,
                'Akcija je uspešno kreirana i čeka odobrenje administratora.',
            )
            return redirect('moje_akcije')
    else:
        form = AkcijaForm()

    return render(request, 'kreiraj_akciju.html', {'form': form})


@login_required
def moje_akcije(request):
    """
    Lista akcija ulogovanog organizatora (SSU 5 — stranica „Moje akcije").

    Odredište preusmerenja nakon uspešnog kreiranja akcije; prikazuje i akcije
    koje još čekaju odobrenje administratora.
    """
    if not request.user.je_organizator:
        return redirect('home')

    akcije = (
        Akcija.objects
        .filter(organizator=request.user.organizator_profil)
        .select_related('kategorija', 'organizator')
        .order_by('-datum_kreiranja')
    )
    return render(request, 'moje_akcije.html', {
        'akcije': akcije,
        'br_akcija': akcije.count(),
    })


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
    kontekst = {
        'akcija': akcija,
        'moja_prijava': _moja_prijava(request.user, akcija),
        'prihvaceni_sponzori': SponzorskaPonuda.objects.filter(
            akcija=akcija, status=SponzorskaPonuda.Status.PRIHVACENA,
        ).select_related('sponzor'),
    }
    if _je_organizator_akcije(request.user, akcija):
        kontekst.update(_org_kontekst(akcija))
        kontekst.update(_org_ponude_kontekst(akcija))
        kontekst['prikazi_org_panel'] = True
        kontekst['izmeni_forma'] = AkcijaForm(instance=akcija)  # SSU 10 — tab „Izmeni akciju"
    if request.user.is_authenticated and request.user.je_sponzor and request.user.je_odobren:
        moja_ponuda = SponzorskaPonuda.objects.filter(
            sponzor=request.user.sponzor_profil, akcija=akcija
        ).first()
        kontekst['ponuda_forma'] = SponzorskaPonudaForm(initial={'akcija': akcija})
        kontekst['moja_ponuda'] = moja_ponuda
    return render(request, 'detalj_akcije.html', kontekst)


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


def _je_organizator_akcije(korisnik, akcija):
    return (
        korisnik.is_authenticated
        and korisnik.je_organizator
        and akcija.organizator_id == korisnik.pk
    )


def _je_otkazana(akcija):
    """
    Otkazana akcija je „zamrznuta" (SSU 10, 2.2.9): nad njom nisu moguće izmene,
    prihvatanje/odbijanje volontera i sponzora, slanje obaveštenja ni nove
    sponzorske ponude. SSU-ovi to eksplicitno ne pominju — poslovno pravilo.
    """
    return akcija.status == Akcija.Status.OTKAZANA


def _org_kontekst(akcija):
    """Kontekst za _org_prijave.html panel."""
    prijave = akcija.prijave.select_related('korisnik__korisnik')
    return {
        'akcija': akcija,
        'prijave_na_cekanju': prijave.filter(status=Prijava.Status.NA_CEKANJU),
        'prijave_prihvacene': prijave.filter(status=Prijava.Status.PRIHVACENA),
    }


def _org_ponude_kontekst(akcija):
    """Kontekst za _org_ponude.html panel (SSU 17)."""
    ponude = akcija.sponzorske_ponude.select_related('sponzor')
    na_cekanju = ponude.filter(status=SponzorskaPonuda.Status.NA_CEKANJU)
    return {
        'akcija': akcija,
        'ponude_na_cekanju': na_cekanju,
        'ponude_prihvacene': ponude.filter(status=SponzorskaPonuda.Status.PRIHVACENA),
        'ponude_odbijene': ponude.filter(status=SponzorskaPonuda.Status.ODBIJENA),
        'br_ponuda_na_cekanju': na_cekanju.count(),
    }


def _org_ajax_odgovor(request, akcija):
    """
    Zajednički Ajax odgovor za prihvati/odbij: HTML fragmenti za org panel i
    za sidebar (progres i status akcije mogu da se menjaju istovremeno).
    """
    panel = render_to_string('_org_prijave.html', _org_kontekst(akcija), request=request)
    sidebar = render_to_string('_prijava_sidebar.html', {
        'akcija': akcija,
        'moja_prijava': _moja_prijava(request.user, akcija),
    }, request=request)
    return JsonResponse({'panel': panel, 'sidebar': sidebar})


@login_required
@require_POST
def prihvati_prijavu(request, id_akc, id_kor):
    """Organizator prihvata prijavu (SSU 18, 2.2.1 i 2.2.4)."""
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return HttpResponseForbidden('Samo organizator akcije može ovo da uradi.')
    if akcija.status in (Akcija.Status.POPUNJENA, Akcija.Status.ZAVRSENA, Akcija.Status.OTKAZANA):
        # SSU 18, 2.2.5 — poruka ide korisniku kroz UI (renderujemo je u panelu).
        return _org_ajax_odgovor(request, akcija)
    prijava = get_object_or_404(
        Prijava, akcija=akcija, korisnik_id=id_kor, status=Prijava.Status.NA_CEKANJU
    )
    prijava.status = Prijava.Status.PRIHVACENA
    prijava.save(update_fields=['status'])
    posalji_prihvatanje_prijave(prijava)
    # SSU 18, 2.2.4 — akcija se automatski prebacuje u „popunjena" pri
    # prihvatanju poslednjeg volontera.
    if akcija.broj_prihvacenih >= akcija.max_br_volontera:
        akcija.status = Akcija.Status.POPUNJENA
        akcija.save(update_fields=['status'])
    return _org_ajax_odgovor(request, akcija)


@login_required
@require_POST
def odbij_prijavu(request, id_akc, id_kor):
    """Organizator odbija prijavu (SSU 18, 2.2.2)."""
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return HttpResponseForbidden('Samo organizator akcije može ovo da uradi.')
    if _je_otkazana(akcija):
        # Otkazana akcija je zamrznuta — poruka se prikazuje kroz UI panel.
        return _org_ajax_odgovor(request, akcija)
    prijava = get_object_or_404(
        Prijava, akcija=akcija, korisnik_id=id_kor, status=Prijava.Status.NA_CEKANJU
    )
    prijava.status = Prijava.Status.ODBIJENA
    prijava.save(update_fields=['status'])
    posalji_odbijanje_prijave(prijava)
    return _org_ajax_odgovor(request, akcija)


@login_required
@require_POST
def prihvati_ponudu(request, id_akc, ponuda_id):
    """Organizator prihvata sponzorsku ponudu (SSU 17)."""
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return JsonResponse({'error': 'Samo organizator akcije može ovo da uradi.'}, status=403)
    if _je_otkazana(akcija):
        return JsonResponse({'error': 'Akcija je otkazana.'}, status=400)
    try:
        ponuda = SponzorskaPonuda.objects.get(pk=ponuda_id, akcija=akcija)
    except SponzorskaPonuda.DoesNotExist:
        return JsonResponse({'error': 'Ponuda ne postoji ili je već obrađena.'}, status=404)
    if ponuda.status != SponzorskaPonuda.Status.NA_CEKANJU:
        return JsonResponse({'error': 'Ponuda je već obrađena.'}, status=400)
    ponuda.status = SponzorskaPonuda.Status.PRIHVACENA
    ponuda.save(update_fields=['status'])
    ctx = _org_ponude_kontekst(akcija)
    return JsonResponse({
        'ponude': render_to_string('_org_ponude.html', ctx, request=request),
        'br_na_cekanju': ctx['br_ponuda_na_cekanju'],
    })


@login_required
@require_POST
def odbij_ponudu(request, id_akc, ponuda_id):
    """Organizator odbija sponzorsku ponudu (SSU 17)."""
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return JsonResponse({'error': 'Samo organizator akcije može ovo da uradi.'}, status=403)
    if _je_otkazana(akcija):
        return JsonResponse({'error': 'Akcija je otkazana.'}, status=400)
    try:
        ponuda = SponzorskaPonuda.objects.get(pk=ponuda_id, akcija=akcija)
    except SponzorskaPonuda.DoesNotExist:
        return JsonResponse({'error': 'Ponuda ne postoji ili je već obrađena.'}, status=404)
    if ponuda.status != SponzorskaPonuda.Status.NA_CEKANJU:
        return JsonResponse({'error': 'Ponuda je već obrađena.'}, status=400)
    ponuda.status = SponzorskaPonuda.Status.ODBIJENA
    ponuda.save(update_fields=['status'])
    ctx = _org_ponude_kontekst(akcija)
    return JsonResponse({
        'ponude': render_to_string('_org_ponude.html', ctx, request=request),
        'br_na_cekanju': ctx['br_ponuda_na_cekanju'],
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


@login_required
@require_POST
def posalji_ponudu(request, id_akc):
    """Sponzor šalje ponudu za akciju (SSU 7, 2.2.1)."""
    if not request.user.je_sponzor:
        return HttpResponseForbidden('Samo sponzori mogu da pošalju ponudu.')
    if not request.user.je_odobren:
        return HttpResponseForbidden('Vaš nalog još nije odobren.')
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if _je_otkazana(akcija):
        return HttpResponseForbidden('Akcija je otkazana.')
    form = SponzorskaPonudaForm(request.POST)
    if form.is_valid():
        ponuda = form.save(commit=False)
        ponuda.sponzor = request.user.sponzor_profil
        ponuda.akcija = akcija
        ponuda.save()
        return render(request, '_sponzor_ponuda.html', {
            'akcija': akcija,
            'moja_ponuda': ponuda,
            'ponuda_forma': SponzorskaPonudaForm(initial={'akcija': akcija}),
        })
    return render(request, '_sponzor_ponuda.html', {
        'akcija': akcija,
        'moja_ponuda': None,
        'ponuda_forma': form,
    })


@login_required
@require_POST
def posalji_obavestenje(request, id_akc):
    """
    Organizator šalje obaveštenje prihvaćenim volonterima akcije (SSU 8, 2.2.1).

    Prima JSON telo ``{"poruka": "..."}``. Prazna poruka se odbija (SSU 8,
    2.2.2). Vraća JSON sa brojem obaveštenih volontera.
    """
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return JsonResponse({'error': 'Samo organizator akcije može ovo da uradi.'}, status=403)
    if _je_otkazana(akcija):
        return JsonResponse({'error': 'Akcija je otkazana — slanje obaveštenja nije moguće.'}, status=400)

    podaci, greska = _parse_ajax_body(request)
    if greska:
        return greska

    poruka = (podaci.get('poruka') or '').strip()
    if not poruka:
        # SSU 8, 2.2.2 — sistem zahteva unos teksta poruke.
        return JsonResponse({'error': 'Unesite tekst poruke.'}, status=400)

    prijave = (
        akcija.prijave
        .filter(status=Prijava.Status.PRIHVACENA)
        .select_related('korisnik__korisnik')
    )
    primaoci = [prijava.korisnik.korisnik for prijava in prijave]
    if not primaoci:
        return JsonResponse({'error': 'Nema prihvaćenih volontera za slanje.'}, status=400)

    poslato = posalji_obavestenje_volonterima(akcija, poruka, primaoci)
    return JsonResponse({
        'ok': True,
        'poslato': poslato,
        'poruka': f'Obaveštenje je poslato prijavljenim volonterima ({poslato}).',
    })


def _prijavljeni_korisnici(akcija):
    """
    Korisnici svih prijavljenih volontera akcije osim odbijenih (SSU 10) —
    njih obaveštavamo o izmeni/otkazivanju akcije.
    """
    prijave = (
        akcija.prijave
        .exclude(status=Prijava.Status.ODBIJENA)
        .select_related('korisnik__korisnik')
    )
    return [prijava.korisnik.korisnik for prijava in prijave]


def _sacuvaj_fotografije(akcija, files):
    """Čuva otpremljene fotografije pre/posle akcije (SSU 10, 2.2.1)."""
    nove = (
        [FotografijaAkcije(akcija=akcija, slika=f, tip=FotografijaAkcije.Tip.PRE)
         for f in files.getlist('slike_pre')]
        + [FotografijaAkcije(akcija=akcija, slika=f, tip=FotografijaAkcije.Tip.POSLE)
           for f in files.getlist('slike_posle')]
    )
    if nove:
        FotografijaAkcije.objects.bulk_create(nove)


@login_required
@require_POST
def izmeni_akciju(request, id_akc):
    """
    Ažuriranje akcije (SSU 10, 2.2.1). Organizator menja podatke svoje akcije;
    prijavljeni volonteri se obaveštavaju emailom. Vraća HTML fragment forme
    (sa greškama po scenarijima 2.2.2–2.2.7, ili sa porukom o uspehu).
    """
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return HttpResponseForbidden('Samo organizator akcije može ovo da uradi.')
    if _je_otkazana(akcija):
        # Zamrznuta akcija — vraćamo fragment koji prikazuje da izmena nije moguća.
        return render(request, '_org_izmeni.html', {
            'akcija': akcija,
            'izmeni_forma': AkcijaForm(instance=akcija),
        })

    forma = AkcijaForm(request.POST, request.FILES, instance=akcija)
    if forma.is_valid():
        forma.save()
        _sacuvaj_fotografije(akcija, request.FILES)
        # SSU 10, 2.2.1 korak 7 — obavesti prijavljene volontere o izmenama.
        posalji_izmenu_akcije(akcija, _prijavljeni_korisnici(akcija))
        return render(request, '_org_izmeni.html', {
            'akcija': akcija,
            'izmeni_forma': AkcijaForm(instance=akcija),
            'izmena_uspeh': True,
        })
    return render(request, '_org_izmeni.html', {
        'akcija': akcija,
        'izmeni_forma': forma,
    })


@login_required
@require_POST
def otkazi_akciju(request, id_akc):
    """
    Otkazivanje akcije (SSU 10, 2.2.9). Status prelazi u „Otkazana", a svi
    prijavljeni volonteri se obaveštavaju emailom. Potvrdu traži klijent.
    """
    akcija = get_object_or_404(Akcija, pk=id_akc)
    if not _je_organizator_akcije(request.user, akcija):
        return JsonResponse({'error': 'Samo organizator akcije može ovo da uradi.'}, status=403)
    if akcija.status == Akcija.Status.OTKAZANA:
        return JsonResponse({'error': 'Akcija je već otkazana.'}, status=400)

    primaoci = _prijavljeni_korisnici(akcija)
    akcija.status = Akcija.Status.OTKAZANA
    akcija.save(update_fields=['status'])
    # SSU 10, 2.2.9 korak 8 — obavesti prijavljene volontere o otkazivanju.
    posalji_otkazivanje_akcije(akcija, primaoci)
    return JsonResponse({'ok': True, 'poruka': 'Akcija je otkazana.'})


def lista_clanaka(request):
    """
    Javna lista objavljenih članaka sa filterima (SSU 4).

    Prikazuju se samo članci sa status='objavljen'. Autori vide svoje na čekanju
    i odbijene članke na sopstvenom profilu (poseban commit).
    """
    clanci = (
        Clanak.objects
        .select_related('autor', 'kategorija')
        .filter(status=Clanak.Status.OBJAVLJEN)
    )

    q = request.GET.get('q', '').strip()[:64]
    kategorija = request.GET.get('kategorija', '').strip()

    # SSU 4, 2.2.7 — neispravan upit se odbija, prikazuje se početni prikaz.
    greska_upita = ''
    if q and not _DOZVOLJEN_UPIT.match(q):
        greska_upita = 'U upitu su dozvoljeni samo slova, cifre i razmaci.'
        q = ''

    if q:
        clanci = clanci.filter(naslov__icontains=q) | clanci.filter(
            autor__naziv_organizacije__icontains=q
        )
    if kategorija:
        clanci = clanci.filter(kategorija_id=kategorija)

    # SSU 4, otvoreno pitanje 1 — numArticlesPerPage = 9.
    paginator = Paginator(clanci.distinct().order_by('-datum_kreiranja'), 9)
    strana = paginator.get_page(request.GET.get('page'))

    kontekst = {
        'clanci': strana.object_list,
        'strana': strana,
        'brojevi_paginacije': _brojevi_paginacije(strana),
        'greska_upita': greska_upita,
        'kategorije': KategorijaClanka.objects.all(),
        'filteri': {'q': q, 'kategorija': kategorija},
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, '_clanci_grid.html', kontekst)
    return render(request, 'clanci.html', kontekst)


def detalj_clanka(request, id_cla):
    """Detalj objavljenog članka sa listom komentara (SSU 12)."""
    clanak = get_object_or_404(
        Clanak.objects.select_related('autor', 'kategorija').prefetch_related('slike'),
        pk=id_cla,
        status=Clanak.Status.OBJAVLJEN,
    )
    komentari = clanak.komentari.select_related('korisnik').order_by('-datum_komentara')
    forma = KomentarForm() if request.user.is_authenticated else None
    return render(request, 'detalj_clanka.html', {
        'clanak': clanak,
        'komentari': komentari,
        'forma': forma,
        'br_komentara': komentari.count(),
    })


@login_required
@require_POST
def ajax_dodaj_komentar(request, id_cla):
    """Ajax endpoint za dodavanje komentara na članak (SSU 12)."""
    clanak = get_object_or_404(Clanak, pk=id_cla, status=Clanak.Status.OBJAVLJEN)
    podaci, err = _parse_ajax_body(request)
    if err:
        return err
    tekst = podaci.get('tekst', '') if podaci else ''
    forma = KomentarForm({'tekst': tekst})
    if not forma.is_valid():
        greske = forma.errors.get('tekst', [])
        poruka = greske[0] if greske else 'Komentar ne može biti prazan!'
        return JsonResponse({'error': poruka}, status=400)
    komentar = forma.save(commit=False)
    komentar.korisnik = request.user
    komentar.clanak = clanak
    komentar.save()
    komentari = clanak.komentari.select_related('korisnik').order_by('-datum_komentara')
    html = render_to_string('_komentari.html', {'komentari': komentari}, request=request)
    return JsonResponse({
        'html': html,
        'br_komentara': komentari.count(),
    })


@login_required
def sponzor_panel(request):
    """Sponzorski panel (SSU 16)."""
    if not request.user.je_sponzor:
        return redirect('home')

    sponzor = request.user.sponzor_profil
    ponude = SponzorskaPonuda.objects.filter(
        sponzor=sponzor
    ).select_related('akcija', 'akcija__organizator')

    prihvacene = ponude.filter(status=SponzorskaPonuda.Status.PRIHVACENA)
    na_cekanju = ponude.filter(status=SponzorskaPonuda.Status.NA_CEKANJU)
    odbijene = ponude.filter(status=SponzorskaPonuda.Status.ODBIJENA)

    ukupan_doprinos = prihvacene.aggregate(total=Sum('vrednost'))['total'] or 0

    return render(request, 'sponzor_panel.html', {
        'ponude_prihvacene': prihvacene,
        'ponude_na_cekanju': na_cekanju,
        'ponude_odbijene': odbijene,
        'ukupan_doprinos': ukupan_doprinos,
        'br_prihvacenih': prihvacene.count(),
        'br_na_cekanju': na_cekanju.count(),
        'br_odbijenih': odbijene.count(),
    })


@login_required
def volonter_panel(request):
    """Volonterski panel (SSU 15)."""
    if not request.user.je_volonter:
        return redirect('home')

    volonter = request.user.volonter_profil
    prijave = Prijava.objects.filter(
        korisnik=volonter
    ).select_related('akcija', 'akcija__organizator', 'akcija__kategorija')

    zavrsene_akcije = [Akcija.Status.ZAVRSENA, Akcija.Status.OTKAZANA]

    tekuce = prijave.filter(
        status__in=[Prijava.Status.NA_CEKANJU, Prijava.Status.PRIHVACENA]
    ).exclude(akcija__status__in=zavrsene_akcije)

    istorija = prijave.filter(
        Q(status=Prijava.Status.ODBIJENA) |
        Q(akcija__status__in=zavrsene_akcije)
    )

    ukupno_sati = prijave.filter(
        status=Prijava.Status.PRIHVACENA
    ).aggregate(total=Sum('br_sati'))['total'] or 0

    na_cekanju = tekuce.filter(status=Prijava.Status.NA_CEKANJU)

    return render(request, 'volonter_panel.html', {
        'tekuce_prijave': tekuce,
        'istorija_prijava': istorija,
        'ukupno_sati': ukupno_sati,
        'br_tekucih': tekuce.count(),
        'br_istorija': istorija.count(),
        'br_na_cekanju': na_cekanju.count(),
        'prima_preporuke': volonter.prima_preporuke,  # SSU 9 — opt-in za preporuke
    })


@login_required
@require_POST
def toggle_preporuke(request):
    """
    Volonter uključuje/isključuje email preporuke akcija (SSU 9, 2.2.2 / 2.2.3).
    Prima JSON telo ``{"prima_preporuke": true|false}``.
    """
    if not request.user.je_volonter:
        return JsonResponse({'error': 'Samo volonteri mogu da menjaju ovu opciju.'}, status=403)

    podaci, greska = _parse_ajax_body(request)
    if greska:
        return greska

    volonter = request.user.volonter_profil
    volonter.prima_preporuke = bool(podaci.get('prima_preporuke'))
    volonter.save(update_fields=['prima_preporuke'])
    return JsonResponse({'ok': True, 'prima_preporuke': volonter.prima_preporuke})


def _organizator_panel_kontekst(org, forma_clanka=None):
    """Zajednički kontekst za organizator_panel.html (koristi ga i kreiraj_clanak view)."""
    akcije = (
        Akcija.objects
        .filter(organizator=org)
        .select_related('kategorija')
        .order_by('-datum_kreiranja')
    )

    prijave_na_cekanju = (
        Prijava.objects
        .filter(akcija__organizator=org, status=Prijava.Status.NA_CEKANJU)
        .select_related('korisnik__korisnik', 'akcija')
        .order_by('-datum_prijave')
    )

    ponude_na_cekanju = (
        SponzorskaPonuda.objects
        .filter(akcija__organizator=org, status=SponzorskaPonuda.Status.NA_CEKANJU)
        .select_related('sponzor', 'akcija')
        .order_by('-datum_slanja')
    )

    clanci = (
        Clanak.objects
        .filter(autor=org)
        .select_related('kategorija')
        .order_by('-datum_kreiranja')
    )

    ukupan_br_volontera = Prijava.objects.filter(
        akcija__organizator=org,
        status=Prijava.Status.PRIHVACENA,
    ).count()

    ukupan_doprinos = SponzorskaPonuda.objects.filter(
        akcija__organizator=org,
        status=SponzorskaPonuda.Status.PRIHVACENA,
    ).aggregate(total=Sum('vrednost'))['total'] or 0

    return {
        'akcije': akcije,
        'prijave_na_cekanju': prijave_na_cekanju,
        'ponude_na_cekanju': ponude_na_cekanju,
        'clanci': clanci,
        'ukupan_br_akcija': akcije.count(),
        'ukupan_br_volontera': ukupan_br_volontera,
        'ukupan_doprinos': ukupan_doprinos,
        'br_prijava_na_cekanju': prijave_na_cekanju.count(),
        'br_ponuda_na_cekanju': ponude_na_cekanju.count(),
        'forma_clanka': forma_clanka if forma_clanka is not None else ClanakForma(),
    }


@login_required
def organizator_panel(request):
    """Organizatorski panel."""
    if not request.user.je_organizator or not request.user.je_odobren:
        return redirect('home')

    return render(
        request,
        'organizator_panel.html',
        _organizator_panel_kontekst(request.user.organizator_profil),
    )


def _uskoro(request):
    """Privremeni placeholder dok se ne implementiraju odgovarajući commitovi."""
    return render(request, 'uskoro.html')


# ── SSU 13 — Upravljanje korisničkim nalozima ────────────────────────────────

def admin_panel(request):
    """
    Admin kontrolna tabla (SSU 13).

    Pristup samo za administratore; svi ostali se preusmeravaju na početnu.
    """
    if not request.user.is_authenticated or not request.user.je_admin:
        return redirect('home')

    org_zahtevi = (
        OrganizatorProfil.objects
        .filter(status=OrganizatorProfil.Status.NA_CEKANJU)
        .select_related('korisnik')
        .order_by('korisnik__datum_registracije')
    )
    sponzor_zahtevi = (
        SponzorProfil.objects
        .filter(status=SponzorProfil.Status.NA_CEKANJU)
        .select_related('korisnik')
        .order_by('korisnik__datum_registracije')
    )

    zahtevi = (
        [{'korisnik': p.korisnik, 'tip': 'organizator', 'tip_display': 'Organizator',
          'naziv_org': p.naziv_organizacije, 'br_tel': p.br_telefona}
         for p in org_zahtevi]
        + [{'korisnik': p.korisnik, 'tip': 'sponzor', 'tip_display': 'Sponzor',
            'naziv_org': p.naziv_organizacije, 'br_tel': p.br_telefona}
           for p in sponzor_zahtevi]
    )

    korisnici = (
        Korisnik.objects
        .prefetch_related(
            'volonter_profil', 'organizator_profil',
            'sponzor_profil', 'administrator_profil',
        )
        .order_by('-datum_registracije')
    )

    akcije_na_cekanju = (
        Akcija.objects
        .filter(status=Akcija.Status.NA_CEKANJU)
        .select_related('organizator', 'kategorija')
        .order_by('datum_kreiranja')
    )
    clanci_na_cekanju = (
        Clanak.objects
        .filter(status=Clanak.Status.NA_CEKANJU)
        .select_related('autor', 'kategorija')
        .order_by('datum_kreiranja')
    )

    return render(request, 'admin_panel.html', {
        'zahtevi': zahtevi,
        'korisnici': korisnici,
        'br_zahteva': len(zahtevi),
        'br_korisnika': korisnici.count(),
        'akcije_na_cekanju': akcije_na_cekanju,
        'clanci_na_cekanju': clanci_na_cekanju,
        'br_akcija_na_cekanju': akcije_na_cekanju.count(),
        'br_clanaka_na_cekanju': clanci_na_cekanju.count(),
    })


# ── SSU 26 — Ajax endpointi za admin panel ───────────────────────────────────

def _parse_ajax_body(request):
    """Parsira JSON telo Ajax zahteva; vraća (dict, None) ili (None, JsonResponse greška)."""
    try:
        return json.loads(request.body), None
    except (json.JSONDecodeError, ValueError):
        return None, JsonResponse({'error': 'Neispravan zahtev.'}, status=400)


def _admin_check(request):
    """Vraća None ako je korisnik admin, inače JsonResponse 403."""
    if not request.user.is_authenticated or not request.user.je_admin:
        return JsonResponse({'error': 'Nemate pristup.'}, status=403)
    return None


@require_POST
def ajax_odobri_nalog(request):
    """
    Odobrava nalog organizatora ili sponzora (SSU 13, 2.2.1).

    Prima JSON: {"korisnik_id": <int>}
    Vraća JSON: {"success": true, "message": "..."}
    """
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        korisnik_id = int(podaci['korisnik_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        korisnik = Korisnik.objects.get(pk=korisnik_id)
    except Korisnik.DoesNotExist:
        return JsonResponse({'error': 'Korisnik ne postoji.'}, status=404)

    if korisnik.je_organizator and korisnik.organizator_profil.status == OrganizatorProfil.Status.NA_CEKANJU:
        korisnik.organizator_profil.status = OrganizatorProfil.Status.ODOBREN
        korisnik.organizator_profil.save(update_fields=['status'])
    elif korisnik.je_sponzor and korisnik.sponzor_profil.status == SponzorProfil.Status.NA_CEKANJU:
        korisnik.sponzor_profil.status = SponzorProfil.Status.ODOBREN
        korisnik.sponzor_profil.save(update_fields=['status'])
    else:
        return JsonResponse({'error': 'Nalog nije na čekanju.'}, status=400)

    posalji_odobrenje_naloga(korisnik)
    return JsonResponse({
        'success': True,
        'message': f'Nalog za „{korisnik.get_full_name()}" je odobren. Email je poslat.',
    })


@require_POST
def ajax_odbij_nalog(request):
    """
    Odbija zahtev za nalog (SSU 13, 2.2.2).

    Prima JSON: {"korisnik_id": <int>}
    Vraća JSON: {"success": true, "message": "..."}
    """
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        korisnik_id = int(podaci['korisnik_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        korisnik = Korisnik.objects.get(pk=korisnik_id)
    except Korisnik.DoesNotExist:
        return JsonResponse({'error': 'Korisnik ne postoji.'}, status=404)

    if korisnik.je_organizator and korisnik.organizator_profil.status == OrganizatorProfil.Status.NA_CEKANJU:
        korisnik.organizator_profil.status = OrganizatorProfil.Status.ODBIJEN
        korisnik.organizator_profil.save(update_fields=['status'])
    elif korisnik.je_sponzor and korisnik.sponzor_profil.status == SponzorProfil.Status.NA_CEKANJU:
        korisnik.sponzor_profil.status = SponzorProfil.Status.ODBIJEN
        korisnik.sponzor_profil.save(update_fields=['status'])
    else:
        return JsonResponse({'error': 'Nalog nije na čekanju.'}, status=400)

    posalji_odbijanje_naloga(korisnik)
    return JsonResponse({
        'success': True,
        'message': f'Zahtev za „{korisnik.get_full_name()}" je odbijen.',
    })


@require_POST
def ajax_ukloni_korisnika(request):
    """
    Uklanja nalog korisnika (SSU 13, 2.2.3).

    Prima JSON: {"korisnik_id": <int>}
    Vraća JSON: {"success": true, "message": "..."}
    """
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        korisnik_id = int(podaci['korisnik_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    if request.user.pk == korisnik_id:
        return JsonResponse({'error': 'Ne možete ukloniti sopstveni nalog.'}, status=400)

    try:
        korisnik = Korisnik.objects.get(pk=korisnik_id)
    except Korisnik.DoesNotExist:
        return JsonResponse({'error': 'Korisnik ne postoji.'}, status=404)

    ime = korisnik.get_full_name()
    korisnik.delete()
    return JsonResponse({
        'success': True,
        'message': f'Nalog korisnika „{ime}" je uklonjen.',
    })


# ── Admin: upravljanje akcijama ──────────────────────────────────────────────

@require_POST
def ajax_odobri_akciju(request):
    """Odobrava akciju na cekanju (menja status u odobrena)."""
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        akcija_id = int(podaci['akcija_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        akcija = Akcija.objects.get(pk=akcija_id)
    except Akcija.DoesNotExist:
        return JsonResponse({'error': 'Akcija ne postoji.'}, status=404)

    if akcija.status != Akcija.Status.NA_CEKANJU:
        return JsonResponse({'error': 'Akcija nije na čekanju.'}, status=400)

    akcija.status = Akcija.Status.ODOBRENA
    akcija.save(update_fields=['status'])
    return JsonResponse({
        'success': True,
        'message': f'Akcija „{akcija.naziv}" je odobrena.',
    })


@require_POST
def ajax_obrisi_akciju(request):
    """Briše akciju na čekanju."""
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        akcija_id = int(podaci['akcija_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        akcija = Akcija.objects.get(pk=akcija_id, status=Akcija.Status.NA_CEKANJU)
    except Akcija.DoesNotExist:
        return JsonResponse({'error': 'Akcija ne postoji ili nije na čekanju.'}, status=404)

    naziv = akcija.naziv
    akcija.delete()
    return JsonResponse({
        'success': True,
        'message': f'Akcija „{naziv}" je obrisana.',
    })


# ── Admin: upravljanje člancima ──────────────────────────────────────────────

@require_POST
def ajax_odobri_clanak(request):
    """Objavljuje članak na čekanju (menja status u 'objavljen')."""
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        clanak_id = int(podaci['clanak_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        clanak = Clanak.objects.get(pk=clanak_id)
    except Clanak.DoesNotExist:
        return JsonResponse({'error': 'Članak ne postoji.'}, status=404)

    if clanak.status != Clanak.Status.NA_CEKANJU:
        return JsonResponse({'error': 'Članak nije na čekanju.'}, status=400)

    clanak.status = Clanak.Status.OBJAVLJEN
    clanak.save(update_fields=['status'])
    return JsonResponse({
        'success': True,
        'message': f'Članak „{clanak.naslov}" je objavljen.',
    })


@require_POST
def ajax_obrisi_clanak(request):
    """Briše članak na čekanju."""
    if err := _admin_check(request):
        return err

    podaci, err = _parse_ajax_body(request)
    if err:
        return err

    try:
        clanak_id = int(podaci['clanak_id'])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)

    try:
        clanak = Clanak.objects.get(pk=clanak_id, status=Clanak.Status.NA_CEKANJU)
    except Clanak.DoesNotExist:
        return JsonResponse({'error': 'Članak ne postoji ili nije na čekanju.'}, status=404)

    naslov = clanak.naslov
    clanak.delete()
    return JsonResponse({
        'success': True,
        'message': f'Članak „{naslov}" je obrisan.',
    })


# SSU 22 — Kreiranje članka od strane organizatora (inline forma u organizator panelu).

@login_required
def kreiraj_clanak(request):
    """
    Prima POST iz forme unutar organizator panela (tab „Moji članci").
    GET preusmerava na panel — nema zasebne stranice.
    """
    if not request.user.je_organizator or not request.user.je_odobren:
        return redirect('home')

    org = request.user.organizator_profil

    if request.method != 'POST':
        return redirect('organizator_panel')

    forma = ClanakForma(request.POST, request.FILES)
    if forma.is_valid():
        clanak = forma.save(commit=False)
        clanak.autor = org
        # status ostaje NA_CEKANJU (default) — admin odobrava kroz SSU 13.
        clanak.save()

        dodatne = request.FILES.getlist('dodatne_slike')
        if dodatne:
            SlikaClanka.objects.bulk_create([
                SlikaClanka(clanak=clanak, slika=f) for f in dodatne
            ])

        return redirect('organizator_panel')

    # Neuspešna validacija — vraćamo panel sa otvorenom formom i greškama.
    kontekst = _organizator_panel_kontekst(org, forma_clanka=forma)
    kontekst['otvori_formu_clanka'] = True
    return render(request, 'organizator_panel.html', kontekst)
