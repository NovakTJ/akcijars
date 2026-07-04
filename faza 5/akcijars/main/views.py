import json
import re

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
    posalji_odbijanje_naloga,
    posalji_odbijanje_prijave,
    posalji_odobrenje_naloga,
    posalji_potvrdu_registracije,
    posalji_prihvatanje_prijave,
)
from .forms import PrijavaForm, RegistracijaForm, SponzorskaPonudaForm
from .models import (
    Akcija,
    Clanak,
    KategorijaAkcije,
    KategorijaClanka,
    Korisnik,
    OrganizatorProfil,
    Prijava,
    SponzorProfil,
    SponzorskaPonuda,
)


def home(request):
    """Stub početna stranica — sadržaj dodaje Novak/Maša u kasnijim commitima."""
    return render(request, 'home.html')


def _pocetna_za_korisnika(korisnik):
    """
    Vraća naziv rute lične stranice u zavisnosti od uloge (SSU 2, 2.2.1).

    Kontrolne table po ulogama (volonter/organizator/sponzor/admin) — uvode se
    prave rute kako odgovarajući paneli budu gotovi.
    """
    if korisnik.je_admin:
        return 'admin_panel'
    if korisnik.je_sponzor:
        return 'sponzor_panel'
    if korisnik.je_volonter:
        return 'volonter_panel'
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
    })


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

    return render(request, 'admin_panel.html', {
        'zahtevi': zahtevi,
        'korisnici': korisnici,
        'br_zahteva': len(zahtevi),
        'br_korisnika': korisnici.count(),
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
        'message': f'Nalog za „{korisnik.get_full_name()}“ je odobren. Email je poslat.',
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
        'message': f'Zahtev za „{korisnik.get_full_name()}“ je odbijen.',
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
        'message': f'Nalog korisnika „{ime}“ je uklonjen.',
    })
