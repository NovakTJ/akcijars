# Autor: Novak Stijepic 0124/2023
"""
Selenium WebDriver UI tests for SSU 9 — Sending recommendations to users
(implemented by Milica Milošević — cross-testing).

Exercises the opt-in toggle on the volunteer panel „Podešavanja" tab. Flipping
the switch fires an AJAX call (``toggle_preporuke``) and updates a status line;
the tests wait for that confirmation and then assert the persisted preference.
"""
from uuid import uuid4

from django.test import override_settings

from main.tests._helpers import volonter, organizator
from ._baza import SeleniumBazniTest


@override_settings(GOOGLE_MAPS_API_KEY='')
class PreporukeToggleUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.vol_email = f'vol.{s}@akcija.rs'
        self.vol = volonter(self.vol_email)

    def _otvori_podesavanja(self):
        """Log in the volunteer, open the panel and switch to the settings tab."""
        self.login(self.vol_email)
        self.idi('/volonter-panel/')
        self.klik('[data-tab="podesavanja"]')
        self.cekaj('#chk-preporuke')

    def test_volonter_aktivira_preporuke_2_2_2(self):
        """2.2.2 — toggling the switch on records opt-in and confirms in the UI."""
        self._otvori_podesavanja()
        # The checkbox itself is visually hidden; click the visible slider label.
        self.klik('#slider-preporuke')
        self.cekaj_tekst('#preporuke-status', 'Preporuke su uključene.')

        self.vol.volonter_profil.refresh_from_db()
        self.assertTrue(self.vol.volonter_profil.prima_preporuke)

    def test_volonter_deaktivira_preporuke_2_2_3(self):
        """2.2.3 — toggling the switch off records the change and confirms it."""
        self.vol.volonter_profil.prima_preporuke = True
        self.vol.volonter_profil.save(update_fields=['prima_preporuke'])

        self._otvori_podesavanja()
        self.klik('#slider-preporuke')
        self.cekaj_tekst('#preporuke-status', 'Preporuke su isključene.')

        self.vol.volonter_profil.refresh_from_db()
        self.assertFalse(self.vol.volonter_profil.prima_preporuke)

    def test_ne_volonter_ne_pristupa_panelu_2_4(self):
        """2.4 — a non-volunteer cannot reach the volunteer panel (redirected)."""
        org_email = f'org.{uuid4().hex[:6]}@akcija.rs'
        organizator(org_email)
        self.login(org_email)
        self.idi('/volonter-panel/')
        self.assertNotIn('/volonter-panel', self.br.current_url)
