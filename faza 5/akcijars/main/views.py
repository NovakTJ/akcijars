from django.shortcuts import render


def home(request):
    """Stub početna stranica — sadržaj dodaje Novak/Maša u kasnijim commitima."""
    return render(request, 'home.html')
