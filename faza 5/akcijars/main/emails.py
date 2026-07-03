"""
Slanje email obaveštenja korisnicima (FZ 4.3.2 — Email API).

Za sada se koristi samo za potvrdu registracije (SSU 1, 2.2.1 / 2.2.2), ali je
modul predviđen da okupi i ostala obaveštenja (prijave na akcije, preporuke...).
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def posalji_potvrdu_registracije(korisnik, uloga):
    """
    Šalje korisniku email potvrdu uspešne registracije.

    Sadržaj se razlikuje za volontera (može odmah da se prijavi) i za
    organizatora/sponzora (nalog čeka odobrenje administratora).

    Vraća broj poslatih poruka (0 ili 1). Greška u slanju se ne propagira:
    registracija je u tom trenutku već uspela i ne sme da padne zbog
    nedostupnog email servisa.
    """
    ceka_odobrenje = uloga in ('organizator', 'sponzor')
    kontekst = {
        'korisnik': korisnik,
        'ceka_odobrenje': ceka_odobrenje,
    }

    naslov = 'Dobrodošli na AkcijaRS — potvrda registracije'
    tekst = render_to_string('emails/potvrda_registracije.txt', kontekst)
    html = render_to_string('emails/potvrda_registracije.html', kontekst)

    poruka = EmailMultiAlternatives(
        subject=naslov,
        body=tekst,
        to=[korisnik.email],
    )
    poruka.attach_alternative(html, 'text/html')
    return poruka.send(fail_silently=True)


def posalji_odobrenje_naloga(korisnik):
    """Obaveštava organizatora/sponzora da je nalog odobren (SSU 13, 2.2.1 korak 7)."""
    from django.core.mail import send_mail
    send_mail(
        subject='AkcijaRS — Vaš nalog je odobren',
        message=(
            f'Poštovani/a {korisnik.get_full_name()},\n\n'
            'Vaš nalog na platformi AkcijaRS je odobren od strane administratora.\n'
            'Sada se možete prijaviti i koristiti sve funkcionalnosti sistema.\n\n'
            'Srdačan pozdrav,\nTim AkcijaRS'
        ),
        from_email=None,
        recipient_list=[korisnik.email],
        fail_silently=True,
    )


def posalji_odbijanje_naloga(korisnik):
    """Obaveštava organizatora/sponzora da je zahtev odbijen (SSU 13, 2.2.2 korak 7)."""
    from django.core.mail import send_mail
    send_mail(
        subject='AkcijaRS — Zahtev za nalog odbijen',
        message=(
            f'Poštovani/a {korisnik.get_full_name()},\n\n'
            'Nažalost, zahtev za kreiranje naloga na platformi AkcijaRS nije odobren.\n'
            'Za dodatne informacije kontaktirajte administratore sistema.\n\n'
            'Srdačan pozdrav,\nTim AkcijaRS'
        ),
        from_email=None,
        recipient_list=[korisnik.email],
        fail_silently=True,
    )


def _posalji_odgovor_na_prijavu(prijava, naslov, template_base):
    """Zajednička logika za slanje mejla o odluci organizatora (SSU 18)."""
    volonter = prijava.korisnik.korisnik
    kontekst = {'volonter': volonter, 'akcija': prijava.akcija}

    tekst = render_to_string(f'emails/{template_base}.txt', kontekst)
    html = render_to_string(f'emails/{template_base}.html', kontekst)

    poruka = EmailMultiAlternatives(
        subject=naslov,
        body=tekst,
        to=[volonter.email],
    )
    poruka.attach_alternative(html, 'text/html')
    return poruka.send(fail_silently=True)


def posalji_prihvatanje_prijave(prijava):
    """Obaveštava volontera da je njegova prijava prihvaćena (SSU 18, 2.2.1)."""
    return _posalji_odgovor_na_prijavu(
        prijava,
        naslov=f'Prijava prihvaćena — {prijava.akcija.naziv}',
        template_base='prihvatanje_prijave',
    )


def posalji_odbijanje_prijave(prijava):
    """Obaveštava volontera da njegova prijava nije prihvaćena (SSU 18, 2.2.2)."""
    return _posalji_odgovor_na_prijavu(
        prijava,
        naslov=f'Odgovor na prijavu — {prijava.akcija.naziv}',
        template_base='odbijanje_prijave',
    )
