# Autor: Milica Milošević 0357/2023
# Autor: Maša Nikolić 2023/0089
# Autor: Stefan Grujičić 0030/2023
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import (
    Korisnik,
    VolonterProfil,
    OrganizatorProfil,
    SponzorProfil,
    AdministratorProfil,
    KategorijaAkcije,
    Akcija,
    FotografijaAkcije,
    Prijava,
    SponzorskaPonuda,
    KategorijaClanka,
    Clanak,
    SlikaClanka,
)


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    model = Korisnik

    list_display = ('email', 'ime', 'prezime', 'uloga_display', 'status_badge', 'is_active', 'datum_registracije')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'ime', 'prezime', 'korisnicko_ime')
    ordering = ('-datum_registracije',)
    readonly_fields = ('datum_registracije', 'last_login')

    fieldsets = (
        ('Kredencijali', {'fields': ('email', 'password')}),
        ('Lični podaci', {'fields': ('korisnicko_ime', 'ime', 'prezime')}),
        ('Sistemske privilegije', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datumi', {'fields': ('datum_registracije', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'korisnicko_ime', 'ime', 'prezime', 'password1', 'password2'),
        }),
    )

    @admin.display(description='Uloga')
    def uloga_display(self, obj):
        if obj.je_admin:
            return 'Administrator'
        if obj.je_organizator:
            return 'Organizator'
        if obj.je_sponzor:
            return 'Sponzor'
        if obj.je_volonter:
            return 'Volonter'
        return '—'

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.je_volonter or obj.je_admin:
            return mark_safe('<span style="color:green">✔ Aktivan</span>')
        if obj.je_organizator:
            status = obj.organizator_profil.status
        elif obj.je_sponzor:
            status = obj.sponzor_profil.status
        else:
            return '—'

        if status == 'odobren':
            return mark_safe('<span style="color:green">✔ Odobren</span>')
        if status == 'odbijen':
            return mark_safe('<span style="color:red">✗ Odbijen</span>')
        return mark_safe('<span style="color:orange">⏳ Na čekanju</span>')

    actions = ['odobri_naloge', 'odbij_naloge', 'deaktiviraj_naloge']

    @admin.action(description='Odobri označene organizatore/sponzore')
    def odobri_naloge(self, request, queryset):
        updated = 0
        for user in queryset:
            if user.je_organizator and user.organizator_profil.status == OrganizatorProfil.Status.NA_CEKANJU:
                user.organizator_profil.status = OrganizatorProfil.Status.ODOBREN
                user.organizator_profil.save()
                updated += 1
            elif user.je_sponzor and user.sponzor_profil.status == SponzorProfil.Status.NA_CEKANJU:
                user.sponzor_profil.status = SponzorProfil.Status.ODOBREN
                user.sponzor_profil.save()
                updated += 1
        self.message_user(request, f'{updated} nalog(a) je odobren(o).')

    @admin.action(description='Odbij označene organizatore/sponzore')
    def odbij_naloge(self, request, queryset):
        updated = 0
        for user in queryset:
            if user.je_organizator and user.organizator_profil.status == OrganizatorProfil.Status.NA_CEKANJU:
                user.organizator_profil.status = OrganizatorProfil.Status.ODBIJEN
                user.organizator_profil.save()
                updated += 1
            elif user.je_sponzor and user.sponzor_profil.status == SponzorProfil.Status.NA_CEKANJU:
                user.sponzor_profil.status = SponzorProfil.Status.ODBIJEN
                user.sponzor_profil.save()
                updated += 1
        self.message_user(request, f'{updated} nalog(a) je odbijen(o).')

    @admin.action(description='Deaktiviraj označene korisnike')
    def deaktiviraj_naloge(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} nalog(a) je deaktiviran(o).')


@admin.register(VolonterProfil)
class VolonterProfilAdmin(admin.ModelAdmin):
    list_display = ('korisnik', 'ukupno_sati', 'prima_preporuke')
    search_fields = ('korisnik__ime', 'korisnik__prezime', 'korisnik__email')
    list_filter = ('prima_preporuke',)


@admin.register(OrganizatorProfil)
class OrganizatorProfilAdmin(admin.ModelAdmin):
    list_display = ('naziv_organizacije', 'korisnik', 'br_telefona', 'status')
    search_fields = ('naziv_organizacije', 'korisnik__ime', 'korisnik__email')
    list_filter = ('status',)


@admin.register(SponzorProfil)
class SponzorProfilAdmin(admin.ModelAdmin):
    list_display = ('naziv_organizacije', 'korisnik', 'br_telefona', 'status')
    search_fields = ('naziv_organizacije', 'korisnik__ime', 'korisnik__email')
    list_filter = ('status',)


@admin.register(AdministratorProfil)
class AdministratorProfilAdmin(admin.ModelAdmin):
    list_display = ('korisnik',)
    search_fields = ('korisnik__ime', 'korisnik__prezime', 'korisnik__email')


@admin.register(KategorijaAkcije)
class KategorijaAkcijeAdmin(admin.ModelAdmin):
    """Admin prikaz kategorija akcija."""

    list_display = ('naziv',)
    search_fields = ('naziv',)


class FotografijaAkcijeInline(admin.TabularInline):
    model = FotografijaAkcije
    extra = 1


@admin.register(Akcija)
class AkcijaAdmin(admin.ModelAdmin):
    """Admin prikaz akcija sa filterima, pretragom i inline fotografijama."""

    list_display = ('naziv', 'organizator', 'kategorija', 'datum', 'vreme', 'lokacija', 'status')
    list_filter = ('status', 'kategorija', 'datum')
    search_fields = ('naziv', 'lokacija', 'organizator__naziv_organizacije')
    ordering = ('-datum_kreiranja',)
    readonly_fields = ('datum_kreiranja',)
    inlines = [FotografijaAkcijeInline]


@admin.register(FotografijaAkcije)
class FotografijaAkcijeAdmin(admin.ModelAdmin):
    list_display = ('id_fot', 'akcija', 'tip', 'slika')
    list_filter = ('tip',)
    search_fields = ('akcija__naziv',)


@admin.register(Prijava)
class PrijavaAdmin(admin.ModelAdmin):
    """Admin prikaz prijava volontera na akcije."""

    list_display = ('korisnik', 'akcija', 'status', 'datum_prijave', 'br_sati')
    list_filter = ('status', 'datum_prijave')
    search_fields = ('korisnik__korisnik__ime', 'korisnik__korisnik__prezime', 'akcija__naziv')


@admin.register(SponzorskaPonuda)
class SponzorskaPonudaAdmin(admin.ModelAdmin):
    list_display = ('sponzor', 'akcija', 'vrednost', 'status', 'datum_slanja')
    list_filter = ('status', 'datum_slanja')
    search_fields = ('sponzor__naziv_organizacije', 'akcija__naziv')
    readonly_fields = ('datum_slanja',)
    ordering = ('-datum_slanja',)


@admin.register(KategorijaClanka)
class KategorijaClankaAdmin(admin.ModelAdmin):
    """Admin prikaz kategorija članaka."""

    list_display = ('naziv',)
    search_fields = ('naziv',)


class SlikaClankaInline(admin.TabularInline):
    """Inline za dodavanje slika u okviru članka."""

    model = SlikaClanka
    extra = 1


@admin.register(Clanak)
class ClanakAdmin(admin.ModelAdmin):
    """Admin prikaz članaka sa filterima, pretragom i inline slikama."""

    list_display = ('naslov', 'autor', 'kategorija', 'status', 'datum_kreiranja')
    list_filter = ('status', 'kategorija', 'datum_kreiranja')
    search_fields = ('naslov', 'autor__naziv_organizacije')
    ordering = ('-datum_kreiranja',)
    readonly_fields = ('datum_kreiranja',)
    inlines = [SlikaClankaInline]


@admin.register(SlikaClanka)
class SlikaClankaAdmin(admin.ModelAdmin):
    """Admin prikaz slika članaka."""

    list_display = ('id_sli', 'clanak', 'slika')
    search_fields = ('clanak__naslov',)


