# Autor: Novak Stijepic 0124/2023
"""
Selenium WebDriver UI tests for SSU 3 — Browsing and searching actions
(implemented by Maša Nikolić — cross-testing).

Drives the real ``/akcije/`` page through headless Chrome. The list filters and
paginates over AJAX (``static/js/akcije.js``), so every assertion waits for the
``#akcije-container`` fragment to refresh instead of a full page reload.

NOTE: location/geo search (SSU 3, 2.2.6) is only rendered when
``GOOGLE_MAPS_API_KEY`` is set, so it is out of scope for the UI layer and stays
covered by the unit tests. Everything else from the unit suite is mirrored here.
"""
from uuid import uuid4

from django.test import override_settings
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from main.models import Akcija
from main.tests._helpers import organizator, akcija, kat_akcije
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')  # hide the location filter in tests
class ListaAkcijaUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.org = organizator(f'org.{s}@akcija.rs', naziv='Zeleni Beograd')
        self.org2 = organizator(f'org2.{s}@akcija.rs', naziv='Novosadski centar')

    def _naslovi_kartica(self):
        """Titles of the action cards currently rendered in the grid."""
        return [e.text for e in self.br.find_elements(
            By.CSS_SELECTOR, '#actions-grid .card-title')]

    def test_osnovni_prikaz_stranice_2_2(self):
        """2.2 — the actions page loads and lists an existing action."""
        akcija(self.org, 'Osnovna SSU3 akcija')
        self.idi('/akcije/')
        self.cekaj('#akcije-container')
        self.assertIn('Osnovna SSU3 akcija', self._naslovi_kartica())

    def test_pretraga_po_nazivu_2_2_2(self):
        """2.2.2 — typing a name query keeps the match and drops the rest."""
        akcija(self.org, 'Čišćenje parka Košutnjak')
        akcija(self.org, 'Podela paketa')
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        polje = self.br.find_element(By.CSS_SELECTOR, '#filter-form input[name="q"]')
        polje.send_keys('Košutnjak')
        # AJAX filtering is debounced; wait for the grid to converge.
        self.cekaj_tekst('#actions-grid', 'Čišćenje parka Košutnjak')
        self.assertNotIn('Podela paketa', self.tekst('#actions-grid'))

    def test_pretraga_po_organizatoru_2_2_2(self):
        """2.2.2 — a query matching an organizer name finds its actions."""
        akcija(self.org2, 'Radionica reciklaže')
        akcija(self.org, 'Sadnja drveća')
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        polje = self.br.find_element(By.CSS_SELECTOR, '#filter-form input[name="q"]')
        polje.send_keys('Novosadski')
        self.cekaj_tekst('#actions-grid', 'Radionica reciklaže')
        self.assertNotIn('Sadnja drveća', self.tekst('#actions-grid'))

    def test_neispravan_upit_se_odbija_2_2_11(self):
        """2.2.11 — forbidden characters show a warning and keep all actions."""
        akcija(self.org, 'Prva vidljiva akcija')
        akcija(self.org2, 'Druga vidljiva akcija')
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        polje = self.br.find_element(By.CSS_SELECTOR, '#filter-form input[name="q"]')
        polje.send_keys('@#$')
        self.cekaj_tekst(
            '#akcije-container .alert-warning',
            'U upitu su dozvoljeni samo slova, cifre i razmaci.',
        )
        naslovi = self._naslovi_kartica()
        self.assertIn('Prva vidljiva akcija', naslovi)
        self.assertIn('Druga vidljiva akcija', naslovi)

    def test_filter_po_kategoriji_2_2_3(self):
        """2.2.3 — selecting a category narrows the list."""
        eko = kat_akcije('SSU3 UI ekologija')
        hum = kat_akcije('SSU3 UI humanitarno')
        akcija(self.org, 'Eko akcija', kat=eko)
        akcija(self.org, 'Humanitarna akcija', kat=hum)
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        Select(self.br.find_element(
            By.CSS_SELECTOR, '#filter-form select[name="kategorija"]')
        ).select_by_visible_text('SSU3 UI ekologija')
        self.cekaj_tekst('#actions-grid', 'Eko akcija')
        self.assertNotIn('Humanitarna akcija', self.tekst('#actions-grid'))

    def test_filter_po_statusu_2_2_4(self):
        """2.2.4 — selecting a status narrows the list."""
        akcija(self.org, 'Popunjena akcija', Akcija.Status.POPUNJENA)
        akcija(self.org, 'Aktivna akcija', Akcija.Status.AKTIVNA)
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        Select(self.br.find_element(
            By.CSS_SELECTOR, '#filter-form select[name="status"]')
        ).select_by_value(Akcija.Status.POPUNJENA)
        self.cekaj_tekst('#actions-grid', 'Popunjena akcija')
        self.assertNotIn('Aktivna akcija', self.tekst('#actions-grid'))

    def test_sortiranje_po_slobodnim_mestima_2_2_8(self):
        """2.2.8 — sorting by free slots puts the roomier action first."""
        akcija(self.org, 'Manja akcija', max_vol=2)
        akcija(self.org, 'Veca akcija', max_vol=8)
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        # The sort <select> lives inside the AJAX-refreshed container.
        Select(self.br.find_element(
            By.CSS_SELECTOR, '#akcije-container select[name="sort"]')
        ).select_by_value('slobodna_mesta')
        self.cekaj_tekst('#actions-grid', 'Veca akcija')
        self.assertEqual(self._naslovi_kartica()[0], 'Veca akcija')

    def test_paginacija_prikazuje_devet_po_strani_2_2_9(self):
        """2.2.9 — first page shows 9 cards, second page shows the remainder."""
        # Unique token so only these 11 actions are paginated, independent of
        # any other data present in the shared test database for this class.
        token = 'PGN' + uuid4().hex[:6].upper()
        for i in range(11):
            akcija(self.org, f'{token} akcija {i:02d}')
        self.idi('/akcije/')
        self.cekaj('#akcije-container')

        # Narrow the list to just this token via the AJAX search box.
        polje = self.br.find_element(By.CSS_SELECTOR, '#filter-form input[name="q"]')
        polje.send_keys(token)

        def _naslovi_elem(d):
            return d.find_elements(By.CSS_SELECTOR, '#actions-grid .card-title')

        # The search is debounced; wait until the filter has actually applied —
        # page 1 shows exactly 9 cards and every one of them is a token action.
        # (Waiting only for count == 9 is not enough: the unfiltered list already
        # shows 9 cards, so we must confirm the grid really reflects the token.)
        def _filtrirano(d):
            try:
                titles = _naslovi_elem(d)
                return (len(titles) == 9 and all(
                    token in t.get_attribute('textContent') for t in titles))
            except StaleElementReferenceException:
                return False

        WebDriverWait(self.br, 15).until(_filtrirano)

        # Click the numbered "2" button (its text is exactly "2"), not the ›
        # arrow which shares data-page="2". Use textContent (not .text) because
        # .text can return "" for elements below the fold. Delegated AJAX then
        # swaps the grid.
        dugme = next(
            b for b in self.br.find_elements(
                By.CSS_SELECTOR, '#pagination .page-btn[data-page="2"]')
            if b.get_attribute('textContent').strip() == '2')
        self.br.execute_script('arguments[0].scrollIntoView({block:"center"});', dugme)
        self.br.execute_script('arguments[0].click();', dugme)

        # Wait until page 2 is active AND only the 2 leftover cards are shown
        # (both together, to avoid reading the grid mid-transition). The AJAX
        # swap replaces #akcije-container, so guard against stale references.
        def _stranica_dva(d):
            try:
                aktivni = d.find_elements(
                    By.CSS_SELECTOR, '#pagination .page-btn.active')
                return (bool(aktivni)
                        and aktivni[0].get_attribute('textContent').strip() == '2'
                        and len(_naslovi_elem(d)) == 2)
            except StaleElementReferenceException:
                return False

        WebDriverWait(self.br, 15).until(_stranica_dva)
        self.assertEqual(len(self._naslovi_kartica()), 2)
