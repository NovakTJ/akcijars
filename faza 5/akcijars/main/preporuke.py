"""
Generisanje preporuka akcija na osnovu lokacije (SSU 9 / FZ 5.9).

Preporuke se prave od trenutno otvorenih akcija koje se nalaze u blizini
lokacija prethodnih akcija na kojima je volonter učestvovao. Rastojanje se
računa haversine formulom nad koordinatama (Google Maps / Places daje
koordinate pri kreiranju akcije).
"""
import math

from .models import Akcija, Prijava


def _haversine_km(lat1, lng1, lat2, lng2):
    """Rastojanje između dve tačke na Zemlji (haversine), u kilometrima."""
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(d_lng / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


def generisi_preporuke(volonter, max_km=25, limit=5):
    """
    Vraća listu preporučenih akcija za volontera (SSU 9, 2.2.1–2.2.4).

    Kriterijum: otvorena (aktivna) akcija čija je lokacija unutar ``max_km``
    od lokacije bar jedne prethodne akcije na kojoj je volonter učestvovao
    (prihvaćena prijava). Rezultat je sortiran po rastojanju (najbliže prvo)
    i ograničen na ``limit`` akcija. Prazna lista znači „nema preporuka"
    (2.2.4 — u tom slučaju se email ne šalje).

    Svaka vraćena akcija dobija atribut ``distanca`` (km) radi prikaza u mejlu.
    """
    # Lokacije prethodnih akcija volontera (samo one sa koordinatama).
    prethodne = (
        Akcija.objects
        .filter(prijave__korisnik=volonter,
                prijave__status=Prijava.Status.PRIHVACENA,
                geo_sirina__isnull=False, geo_duzina__isnull=False)
        .distinct()
    )
    tacke = [(a.geo_sirina, a.geo_duzina) for a in prethodne]
    if not tacke:
        return []

    # Akcije na koje je volonter već prijavljen (bilo koji status) — preskačemo.
    vec_prijavljen = set(
        Prijava.objects.filter(korisnik=volonter).values_list('akcija_id', flat=True)
    )

    kandidati = (
        Akcija.objects
        .filter(status=Akcija.Status.AKTIVNA,
                geo_sirina__isnull=False, geo_duzina__isnull=False)
        .exclude(pk__in=vec_prijavljen)
        .select_related('organizator', 'kategorija')
    )

    preporuke = []
    for akc in kandidati:
        d = min(_haversine_km(akc.geo_sirina, akc.geo_duzina, lat, lng)
                for lat, lng in tacke)
        if d <= max_km:
            akc.distanca = round(d, 1)
            preporuke.append(akc)

    preporuke.sort(key=lambda a: a.distanca)
    return preporuke[:limit]
