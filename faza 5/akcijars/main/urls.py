from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registracija/', views.registracija, name='registracija'),
    path('prijava/', views.prijava, name='prijava'),
    path('odjava/', views.odjava, name='odjava'),

    # Privremeni placeholderi da bi se zajednički navbar/footer iz base.html
    # ispravno renderovao. Zameniti pravim view-ovima u odgovarajućim commitovima:
    #   akcije, clanci -> Mašini commitovi.
    # VAŽNO: kad dodaješ pravi view, IZMENI ovu liniju (zadrži isto name=),
    # ne dodaj novi path() sa istim name= — Django ne prijavljuje grešku, već
    # tiho koristi poslednji path sa tim imenom, pa {% url %} pokazuje na pogrešnu rutu.
    path('akcije/', views.lista_akcija, name='akcije'),
    path('akcije/<int:id_akc>/', views.detalj_akcije, name='detalj_akcije'),
    path('akcije/<int:id_akc>/prijavi/', views.prijavi_se, name='prijavi_se'),
    path('akcije/<int:id_akc>/odjavi/', views.odjavi_se, name='odjavi_se'),
    path('clanci/', views._uskoro, name='clanci'),

    # SSU 13 — admin panel i Ajax endpointi za upravljanje nalozima
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('ajax/odobri-nalog/', views.ajax_odobri_nalog, name='ajax_odobri_nalog'),
    path('ajax/odbij-nalog/', views.ajax_odbij_nalog, name='ajax_odbij_nalog'),
    path('ajax/ukloni-korisnika/', views.ajax_ukloni_korisnika, name='ajax_ukloni_korisnika'),
]
