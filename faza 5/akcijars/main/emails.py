# Autor: Milica Milošević 0357/2023
# Autor: Maša Nikolić 2023/0089
# Autor: Stefan Grujičić 0030/2023
# Autor: Novak Stijepic 0124/2023
"""
Slanje emasnicimail obaveštenja kori (FZ 4.3.2 — Email API).

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
    """Zajednička logika za slanje mejla o odluci organizatora; vraća broj poslatih poruka."""
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
    """Obaveštava volontera da je njegova prijava prihvaćena; vraća broj poslatih poruka."""
    return _posalji_odgovor_na_prijavu(
        prijava,
        naslov=f'Prijava prihvaćena — {prijava.akcija.naziv}',
        template_base='prihvatanje_prijave',
    )


def posalji_odbijanje_prijave(prijava):
    """Obaveštava volontera da njegova prijava nije prihvaćena; vraća broj poslatih poruka."""
    return _posalji_odgovor_na_prijavu(
        prijava,
        naslov=f'Odgovor na prijavu — {prijava.akcija.naziv}',
        template_base='odbijanje_prijave',
    )


def _posalji_odgovor_na_ponudu(ponuda, naslov, template_base):
    """Zajednička logika za slanje mejla sponzoru o odluci organizatora (SSU 17); vraća broj poslatih poruka."""
    kontekst = {'sponzor': ponuda.sponzor, 'akcija': ponuda.akcija, 'ponuda': ponuda}

    tekst = render_to_string(f'emails/{template_base}.txt', kontekst)
    html = render_to_string(f'emails/{template_base}.html', kontekst)

    poruka = EmailMultiAlternatives(
        subject=naslov,
        body=tekst,
        to=[ponuda.sponzor.korisnik.email],
    )
    poruka.attach_alternative(html, 'text/html')
    return poruka.send(fail_silently=True)


def posalji_prihvatanje_ponude(ponuda):
    """Obaveštava sponzora da je njegova ponuda za sponzorstvo prihvaćena; vraća broj poslatih poruka."""
    return _posalji_odgovor_na_ponudu(
        ponuda,
        naslov=f'Ponuda prihvaćena — {ponuda.akcija.naziv}',
        template_base='prihvatanje_ponude',
    )


def posalji_odbijanje_ponude(ponuda):
    """Obaveštava sponzora da njegova ponuda za sponzorstvo nije prihvaćena; vraća broj poslatih poruka."""
    return _posalji_odgovor_na_ponudu(
        ponuda,
        naslov=f'Odgovor na ponudu — {ponuda.akcija.naziv}',
        template_base='odbijanje_ponude',
    )


def posalji_obavestenje_volonterima(akcija, poruka, primaoci):
    """
    Šalje obaveštenje organizatora prihvaćenim volonterima akcije (SSU 8, 2.2.1).

    ``primaoci`` je iterable ``Korisnik`` objekata (prihvaćeni volonteri), a
    ``poruka`` slobodan tekst koji je organizator uneo. Svakom volonteru se
    šalje zaseban email (bez izlaganja tuđih adresa). Vraća broj uspešno
    poslatih poruka. Greške pri slanju se ne propagiraju (fail_silently).
    """
    poslato = 0
    for volonter in primaoci:
        kontekst = {'volonter': volonter, 'akcija': akcija, 'poruka': poruka}

        tekst = render_to_string('emails/obavestenje_volonterima.txt', kontekst)
        html = render_to_string('emails/obavestenje_volonterima.html', kontekst)

        email = EmailMultiAlternatives(
            subject=f'Obaveštenje — {akcija.naziv}',
            body=tekst,
            to=[volonter.email],
        )
        email.attach_alternative(html, 'text/html')
        poslato += email.send(fail_silently=True)
    return poslato


def _posalji_svim_prijavljenima(akcija, primaoci, naslov, template_base):
    """Zajednička logika za obaveštenje svih prijavljenih volontera akcije (SSU 10)."""
    poslato = 0
    for volonter in primaoci:
        kontekst = {'volonter': volonter, 'akcija': akcija}
        tekst = render_to_string(f'emails/{template_base}.txt', kontekst)
        html = render_to_string(f'emails/{template_base}.html', kontekst)
        email = EmailMultiAlternatives(subject=naslov, body=tekst, to=[volonter.email])
        email.attach_alternative(html, 'text/html')
        poslato += email.send(fail_silently=True)
    return poslato


def posalji_izmenu_akcije(akcija, primaoci):
    """Obaveštava prijavljene volontere da je akcija izmenjena (SSU 10, 2.2.1 korak 7)."""
    return _posalji_svim_prijavljenima(
        akcija, primaoci,
        naslov=f'Izmena akcije — {akcija.naziv}',
        template_base='izmena_akcije',
    )


def posalji_otkazivanje_akcije(akcija, primaoci):
    """Obaveštava prijavljene volontere da je akcija otkazana (SSU 10, 2.2.9 korak 8)."""
    return _posalji_svim_prijavljenima(
        akcija, primaoci,
        naslov=f'Akcija otkazana — {akcija.naziv}',
        template_base='otkazivanje_akcije',
    )


def posalji_preporuke(volonter, akcije):
    """
    Šalje volonteru email sa preporučenim akcijama (SSU 9, 2.2.1).

    Ako je ``akcije`` prazno, email se ne šalje (SSU 9, 2.2.4). Vraća broj
    poslatih poruka (0 ili 1).
    """
    if not akcije:
        return 0
    korisnik = volonter.korisnik
    kontekst = {'korisnik': korisnik, 'akcije': akcije}

    tekst = render_to_string('emails/preporuke.txt', kontekst)
    html = render_to_string('emails/preporuke.html', kontekst)

    email = EmailMultiAlternatives(
        subject='AkcijaRS — preporučene akcije za vas',
        body=tekst,
        to=[korisnik.email],
    )
    email.attach_alternative(html, 'text/html')
    return email.send(fail_silently=True)
