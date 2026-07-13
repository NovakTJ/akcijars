# Autor: Novak Stijepic 0124/2023
"""
Selenium WebDriver UI tests for SSU 16 — Tracking sponsor participation
(implemented by Stefan Grujičić — cross-testing).

Loads the sponsor panel (``/sponzor-panel/``) in a real browser and checks the
header statistics (total contribution and counters) and access control. The
panel is server-rendered, so assertions read the header numbers directly.
"""
from uuid import uuid4

from main.models import Akcija, SponzorskaPonuda
from main.tests._helpers import akcija, organizator, ponuda, sponzor, volonter
from ._baza import SeleniumBazniTest


class SponzorPanelUITest(SeleniumBazniTest):
    def setUp(self):
        s = uuid4().hex[:6]
        self.spon_email = f'spon.{s}@akcija.rs'
        self.spon = sponzor(self.spon_email)
        self.org = organizator(f'org.{s}@akcija.rs')

    def test_sponzor_vidi_panel_2_2(self):
        """2.2 — a logged-in sponsor opens the panel and sees the sponsor badge."""
        self.login(self.spon_email)
        self.idi('/sponzor-panel/')
        self.cekaj('.panel-page')
        # The badge label is uppercased via CSS, so compare case-insensitively.
        self.assertIn('sponzor', self.tekst('.panel-role-badge').lower())

    def test_prazan_panel_2_2_3(self):
        """2.2.3 — a sponsor with no offers sees all counters and contribution at 0."""
        self.login(self.spon_email)
        self.idi('/sponzor-panel/')
        self.cekaj('.panel-page')
        # .green = total contribution, .teal = number of supported (accepted) actions
        self.assertEqual(self.tekst('.panel-stat-num.green'), '0')
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '0')

    def test_prihvacena_ponuda_2_2_1(self):
        """2.2.1 — an accepted offer counts towards supported actions and contribution."""
        akc = akcija(self.org, 'Prihvaćena akcija', Akcija.Status.AKTIVNA)
        ponuda(self.spon, akc, vrednost=700,
               status=SponzorskaPonuda.Status.PRIHVACENA)
        self.login(self.spon_email)
        self.idi('/sponzor-panel/')
        self.cekaj('.panel-page')
        self.assertEqual(self.tekst('.panel-stat-num.green'), '700')
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '1')

    def test_vise_prihvacenih_se_sabira_2_2_1(self):
        """2.2.1 — the total contribution is the sum of all accepted offers."""
        a1 = akcija(self.org, 'A1', Akcija.Status.AKTIVNA)
        a2 = akcija(self.org, 'A2', Akcija.Status.AKTIVNA)
        ponuda(self.spon, a1, vrednost=300,
               status=SponzorskaPonuda.Status.PRIHVACENA)
        ponuda(self.spon, a2, vrednost=450,
               status=SponzorskaPonuda.Status.PRIHVACENA)
        self.login(self.spon_email)
        self.idi('/sponzor-panel/')
        self.cekaj('.panel-page')
        self.assertEqual(self.tekst('.panel-stat-num.green'), '750')
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '2')

    def test_doprinos_racuna_samo_prihvacene_2_2_2(self):
        """2.2.2 — pending and rejected offers do not count towards the contribution."""
        a1 = akcija(self.org, 'Prihvaćena', Akcija.Status.AKTIVNA)
        a2 = akcija(self.org, 'Na čekanju', Akcija.Status.AKTIVNA)
        a3 = akcija(self.org, 'Odbijena', Akcija.Status.AKTIVNA)
        ponuda(self.spon, a1, vrednost=1000, status=SponzorskaPonuda.Status.PRIHVACENA)
        ponuda(self.spon, a2, vrednost=800, status=SponzorskaPonuda.Status.NA_CEKANJU)
        ponuda(self.spon, a3, vrednost=600, status=SponzorskaPonuda.Status.ODBIJENA)
        self.login(self.spon_email)
        self.idi('/sponzor-panel/')
        self.cekaj('.panel-page')
        self.assertEqual(self.tekst('.panel-stat-num.green'), '1000')
        self.assertEqual(self.tekst('.panel-stat-num.teal'), '1')

    def test_volonter_preusmeren_na_home_2_4(self):
        """2.4 — a volunteer is not a sponsor and is redirected to the home page."""
        vol_email = f'vol.{uuid4().hex[:6]}@akcija.rs'
        volonter(vol_email)
        self.login(vol_email)
        self.idi('/sponzor-panel/')
        self.assertNotIn('/sponzor-panel', self.br.current_url)
