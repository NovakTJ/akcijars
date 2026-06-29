from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Privremeni placeholderi da bi se zajednički navbar/footer iz base.html
    # ispravno renderovao. Zameniti pravim view-ovima u odgovarajućim commitovima:
    #   registracija -> commit #5 (Novak); prijava, odjava -> commit #7 (Novak);
    #   akcije, clanci -> Mašini commitovi.
    # VAŽNO: kad dodaješ pravi view, IZMENI ovu liniju (zadrži isto name=),
    # ne dodaj novi path() sa istim name= — Django ne prijavljuje grešku, već
    # tiho koristi poslednji path sa tim imenom, pa {% url %} pokazuje na pogrešnu rutu.
    path('registracija/', views._uskoro, name='registracija'),
    path('prijava/', views._uskoro, name='prijava'),
    path('odjava/', views._uskoro, name='odjava'),
    path('akcije/', views._uskoro, name='akcije'),
    path('clanci/', views._uskoro, name='clanci'),
]
