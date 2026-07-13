# Autor: Novak Stijepic 0124/2023
"""
Selenium WebDriver UI tests for SSU 18 — Accepting and rejecting volunteers
(implemented by Maša Nikolić — cross-testing).

Drives the action detail page (``/akcije/<id>/``), where the owning organizer
sees a management panel with pending volunteer applications. The Accept/Reject
buttons post over AJAX (``static/js/detalj.js``) and re-render the panel, so the
tests wait for the panel to update and then assert the persisted state.
"""
from uuid import uuid4

from django.test import override_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from main.models import Akcija, Prijava
from main.tests._helpers import organizator, volonter, akcija, prijava
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')  # no Google Maps load in tests
class PotvrdaVolonteraUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org_email = f'org.{s}@akcija.rs'
        self.org = organizator(self.org_email)
        self.vol = volonter(f'vol.{s}@akcija.rs')
        self.akc = akcija(self.org, 'Akcija SSU18')
        self.prijava = prijava(self.vol, self.akc)

    def test_prihvatanje_menja_status_2_2_1(self):
        """2.2.1 — organizer accepts the application; its status becomes „prihvacena"."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik(f'.btn-prihvati[data-korisnik-id="{self.vol.pk}"]')
        # After the AJAX refresh the accept button for this volunteer is gone.
        WebDriverWait(self.br, 10).until(
            lambda d: not d.find_elements(
                By.CSS_SELECTOR,
                f'.btn-prihvati[data-korisnik-id="{self.vol.pk}"]'))
        self.cekaj_tekst('#org-vol', 'Prihvaćen')

        self.assertEqual(
            Prijava.objects.get(pk=self.prijava.pk).status,
            Prijava.Status.PRIHVACENA)

    def test_prihvatanje_poslednjeg_mesta_popunjava_akciju_2_2_4(self):
        """2.2.4 — accepting the last free slot marks the action as „popunjena"."""
        self.akc.max_br_volontera = 1
        self.akc.save(update_fields=['max_br_volontera'])
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik(f'.btn-prihvati[data-korisnik-id="{self.vol.pk}"]')
        # Once full, the panel shows the "no more volunteers" notice.
        self.cekaj_tekst('#org-vol', 'Nije moguće prihvatiti više volontera')

        self.assertEqual(
            Akcija.objects.get(pk=self.akc.pk).status, Akcija.Status.POPUNJENA)

    def test_odbijanje_menja_status_2_2_2(self):
        """2.2.2 — organizer rejects the application; its status becomes „odbijena"."""
        self.login(self.org_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.klik(f'.btn-odbij[data-korisnik-id="{self.vol.pk}"]')
        WebDriverWait(self.br, 10).until(
            lambda d: not d.find_elements(
                By.CSS_SELECTOR,
                f'.btn-odbij[data-korisnik-id="{self.vol.pk}"]'))

        self.assertEqual(
            Prijava.objects.get(pk=self.prijava.pk).status,
            Prijava.Status.ODBIJENA)

    def test_drugi_organizator_ne_vidi_panel_2_4(self):
        """2.4 — a different organizer opening the action sees no management panel."""
        drugi_email = f'drugi.{uuid4().hex[:6]}@akcija.rs'
        organizator(drugi_email)
        self.login(drugi_email)
        self.idi(f'/akcije/{self.akc.pk}/')
        self.cekaj('.action-sidebar')  # detail page loaded
        self.assertEqual(
            len(self.br.find_elements(By.CSS_SELECTOR, '#org-panel')), 0)
        self.assertEqual(
            Prijava.objects.get(pk=self.prijava.pk).status,
            Prijava.Status.NA_CEKANJU)
