from django.shortcuts import render


def home(request):
    """Stub početna stranica — sadržaj dodaje Novak/Maša u kasnijim commitima."""
    return render(request, 'home.html')


def _uskoro(request):
    """Privremeni placeholder dok se ne implementiraju odgovarajući commitovi."""
    return render(request, 'uskoro.html')
