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
