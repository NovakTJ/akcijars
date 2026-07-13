# Autor: Novak Stijepic 0124/2023
"""
Selenium WebDriver UI tests for SSU 14 — Managing actions and articles
(implemented by Stefan Grujičić — cross-testing).

Drives the admin panel (``/admin-panel/``): the administrator approves or
deletes pending actions and articles. Each button opens a confirmation modal and
the AJAX response removes the row from the table without a reload, so the tests
wait for the row to disappear and then assert the database state.
"""
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from main.models import Akcija, Clanak
from main.tests._helpers import administrator, akcija, clanak, organizator, volonter
from ._baza import SeleniumBazniTest


class AdminUpravljanjeUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.admin_email = f'admin.{s}@akcija.rs'
        administrator(self.admin_email)
        self.org = organizator(f'org.{s}@akcija.rs')

    def _cekaj_nestanak(self, css):
        """Wait until no element matches the given CSS selector."""
        WebDriverWait(self.br, 10).until(
            lambda d: not d.find_elements(By.CSS_SELECTOR, css))

    def test_odobravanje_akcije_2_2_1(self):
        """2.2.1 — admin approves a pending action; its status becomes „odobrena"."""
        akc = akcija(self.org, 'Akcija na čekanju', Akcija.Status.NA_CEKANJU)
        self.login(self.admin_email)
        self.idi('/admin-panel/')
        self.klik('[data-tab="akcije"]')
        self.klik(f'tr[data-akcija-id="{akc.id_akc}"] .btn-primary')  # Odobri
        self.klik('#modal-odobri-akciju .btn-primary')                # confirm

        self._cekaj_nestanak(f'[data-akcija-id="{akc.id_akc}"]')
        self.assertEqual(
            Akcija.objects.get(pk=akc.pk).status, Akcija.Status.ODOBRENA)

    def test_brisanje_akcije_2_2_2(self):
        """2.2.2 — admin deletes a pending action; it is removed from the database."""
        akc = akcija(self.org, 'Akcija za brisanje', Akcija.Status.NA_CEKANJU)
        self.login(self.admin_email)
        self.idi('/admin-panel/')
        self.klik('[data-tab="akcije"]')
        self.klik(f'tr[data-akcija-id="{akc.id_akc}"] .btn-danger')   # Obriši
        self.klik('#modal-obrisi-akciju .btn-danger')                 # confirm

        self._cekaj_nestanak(f'[data-akcija-id="{akc.id_akc}"]')
        self.assertFalse(Akcija.objects.filter(pk=akc.pk).exists())

    def test_odobravanje_clanka_2_2_4(self):
        """2.2.4 — admin publishes a pending article; its status becomes „objavljen"."""
        cla = clanak(self.org, 'Članak na čekanju', Clanak.Status.NA_CEKANJU)
        self.login(self.admin_email)
        self.idi('/admin-panel/')
        self.klik('[data-tab="clanci"]')
        self.klik(f'tr[data-clanak-id="{cla.id_cla}"] .btn-primary')  # Objavi
        self.klik('#modal-odobri-clanak .btn-primary')                # confirm

        self._cekaj_nestanak(f'[data-clanak-id="{cla.id_cla}"]')
        self.assertEqual(
            Clanak.objects.get(pk=cla.pk).status, Clanak.Status.OBJAVLJEN)

    def test_brisanje_clanka_2_2_5(self):
        """2.2.5 — admin deletes a pending article; it is removed from the database."""
        cla = clanak(self.org, 'Članak za brisanje', Clanak.Status.NA_CEKANJU)
        self.login(self.admin_email)
        self.idi('/admin-panel/')
        self.klik('[data-tab="clanci"]')
        self.klik(f'tr[data-clanak-id="{cla.id_cla}"] .btn-danger')   # Obriši
        self.klik('#modal-obrisi-clanak .btn-danger')                 # confirm

        self._cekaj_nestanak(f'[data-clanak-id="{cla.id_cla}"]')
        self.assertFalse(Clanak.objects.filter(pk=cla.pk).exists())

    def test_ne_admin_ne_pristupa_panelu_2_4(self):
        """2.4 — a non-admin cannot reach the admin panel (redirected)."""
        vol_email = f'vol.{uuid4().hex[:6]}@akcija.rs'
        volonter(vol_email)
        self.login(vol_email)
        self.idi('/admin-panel/')
        self.assertNotIn('/admin-panel', self.br.current_url)
