from django.conf import settings


def google_maps(request):
    """
    Čini Google Maps API ključ dostupnim u svim template-ima (FZ 4.3.1).

    Ključ se u template-u koristi kao „gate": `{% if GOOGLE_MAPS_API_KEY %}`.
    Ako nije postavljen, mapa se ne učitava i stranice rade bez JS grešaka
    (fallback na tekstualni prikaz lokacije).
    """
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
