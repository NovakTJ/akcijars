# Autor: Milica Milošević 0357/2023
# Autor: Maša Nikolić 2023/0089
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
    path('akcije/kreiraj/', views.kreiraj_akciju, name='kreiraj_akciju'),
    path('moje-akcije/', views.moje_akcije, name='moje_akcije'),
    path('akcije/<int:id_akc>/', views.detalj_akcije, name='detalj_akcije'),
    path('akcije/<int:id_akc>/prijavi/', views.prijavi_se, name='prijavi_se'),
    path('akcije/<int:id_akc>/odjavi/', views.odjavi_se, name='odjavi_se'),
    path('akcije/<int:id_akc>/prijave/<int:id_kor>/prihvati/', views.prihvati_prijavu, name='prihvati_prijavu'),
    path('akcije/<int:id_akc>/prijave/<int:id_kor>/odbij/', views.odbij_prijavu, name='odbij_prijavu'),
    path('akcije/<int:id_akc>/ponuda/', views.posalji_ponudu, name='posalji_ponudu'),
    path('akcije/<int:id_akc>/ponude/<int:ponuda_id>/prihvati/', views.prihvati_ponudu, name='prihvati_ponudu'),
    path('akcije/<int:id_akc>/ponude/<int:ponuda_id>/odbij/', views.odbij_ponudu, name='odbij_ponudu'),
    # SSU 8 — slanje obaveštenja prihvaćenim volonterima (Ajax)
    path('akcije/<int:id_akc>/obavestenje/', views.posalji_obavestenje, name='posalji_obavestenje'),
    # SSU 10 — ažuriranje i otkazivanje akcije (Ajax)
    path('akcije/<int:id_akc>/izmeni/', views.izmeni_akciju, name='izmeni_akciju'),
    path('akcije/<int:id_akc>/otkazi/', views.otkazi_akciju, name='otkazi_akciju'),
    path('clanci/', views.lista_clanaka, name='clanci'),
    path('clanci/kreiraj/', views.kreiraj_clanak, name='kreiraj_clanak'),

    path('clanci/<int:id_cla>/', views.detalj_clanka, name='detalj_clanka'),
    path('clanci/<int:id_cla>/komentari/', views.ajax_dodaj_komentar, name='ajax_dodaj_komentar'),

    # SSU 15 — volonterski panel
    path('volonter-panel/', views.volonter_panel, name='volonter_panel'),
    # SSU 9 — opt-in za email preporuke akcija (Ajax)
    path('volonter/preporuke/', views.toggle_preporuke, name='toggle_preporuke'),

    # SSU 16 — sponzorski panel
    path('sponzor-panel/', views.sponzor_panel, name='sponzor_panel'),

    # Organizatorski panel
    path('organizator-panel/', views.organizator_panel, name='organizator_panel'),

    # SSU 13 — admin panel i Ajax endpointi za upravljanje nalozima
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('ajax/odobri-nalog/', views.ajax_odobri_nalog, name='ajax_odobri_nalog'),
    path('ajax/odbij-nalog/', views.ajax_odbij_nalog, name='ajax_odbij_nalog'),
    path('ajax/ukloni-korisnika/', views.ajax_ukloni_korisnika, name='ajax_ukloni_korisnika'),

    # Admin: upravljanje akcijama i člancima na čekanju
    path('ajax/odobri-akciju/', views.ajax_odobri_akciju, name='ajax_odobri_akciju'),
    path('ajax/obrisi-akciju/', views.ajax_obrisi_akciju, name='ajax_obrisi_akciju'),
    path('ajax/odobri-clanak/', views.ajax_odobri_clanak, name='ajax_odobri_clanak'),
    path('ajax/obrisi-clanak/', views.ajax_obrisi_clanak, name='ajax_obrisi_clanak'),
]
