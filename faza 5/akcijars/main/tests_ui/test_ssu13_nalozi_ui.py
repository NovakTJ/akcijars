# Autor: Maša Nikolić 2023/0089
"""
Selenium WebDriver UI testovi za SSU 13 — Upravljanje korisničkim nalozima
(implementirao Stefan Grujičić — ukrštanje).
"""
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from main.models import OrganizatorProfil
from main.tests._helpers import administrator, organizator, volonter
from ._baza import SeleniumBazniTest


class AdminNaloziUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.admin_email = f'admin.{s}@akcija.rs'
        administrator(self.admin_email)
        self.org = organizator(f'org.{s}@akcija.rs',
                               status=OrganizatorProfil.Status.NA_CEKANJU)

    def test_admin_odobrava_nalog(self):
        """Admin klikne „Odobri" → potvrdi u modalu → zahtev nestaje bez reload-a, nalog je odobren."""
        self.login(self.admin_email)
        self.idi('/admin-panel/')
        self.klik('#pregled-zahtevi-lista .btn-primary')   # dugme „Odobri"
        self.klik('#modal-odobri .btn-primary')            # potvrda u modalu
        # Ajax uklanja karticu zahteva iz DOM-a
        WebDriverWait(self.br, 10).until(
            lambda d: not d.find_elements(By.CSS_SELECTOR, f'[data-zahtev-id="{self.org.pk}"]'))
        self.assertEqual(
            OrganizatorProfil.objects.get(korisnik=self.org).status,
            OrganizatorProfil.Status.ODOBREN,
        )

    def test_ne_admin_ne_pristupa_panelu(self):
        """Volonter ne može da otvori admin panel — preusmeren je."""
        vol_email = f'vol.{uuid4().hex[:6]}@akcija.rs'
        volonter(vol_email)
        self.login(vol_email)
        self.idi('/admin-panel/')
        self.assertNotIn('/admin-panel', self.br.current_url)
