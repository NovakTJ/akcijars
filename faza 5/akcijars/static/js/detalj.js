// ── Detalj akcije: Ajax prijava/odjava volontera (SSU 6) ────────────────────
//
// Klik na #btn-prijavi / #btn-odjavi šalje POST na odgovarajući endpoint.
// Server vraća HTML fragment sidebar kartice; menjamo innerHTML kontejnera.
// Dugmad su unutar kontejnera, pa event delegation na kontejneru radi i posle
// zamene HTML-a (nova dugmad dolaze u novom fragmentu).

(function () {
  const container = document.getElementById('prijava-container');
  if (!container) return;

  function getCsrfToken() {
    const m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  async function posalji(url) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      container.innerHTML = await response.text();
    } catch (err) {
      console.error('Prijava/odjava nije uspela:', err);
    }
  }

  container.addEventListener('click', (e) => {
    if (e.target.closest('#btn-prijavi')) {
      e.preventDefault();
      posalji(container.dataset.prijaviUrl);
    } else if (e.target.closest('#btn-odjavi')) {
      e.preventDefault();
      posalji(container.dataset.odjaviUrl);
    }
  });

  // Sponzorska ponuda (SSU 7) — Ajax submit forme
  const ponudaContainer = document.getElementById('sponzor-ponuda-container');
  if (ponudaContainer) {
    ponudaContainer.addEventListener('submit', async (e) => {
      if (!e.target.closest('#form-ponuda')) return;
      e.preventDefault();
      const form = e.target.closest('#form-ponuda');
      const url = ponudaContainer.dataset.ponudaUrl;
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': getCsrfToken(), 'X-Requested-With': 'XMLHttpRequest' },
          body: new FormData(form),
        });
        if (!response.ok) throw new Error('HTTP ' + response.status);
        ponudaContainer.outerHTML = await response.text();
      } catch (err) {
        console.error('Slanje ponude nije uspelo:', err);
      }
    });
  }

  // Organizator panel (SSU 18) — Prihvati / Odbij prijave
  const orgPanel = document.getElementById('org-panel');
  if (orgPanel) {
    const panelContent = document.getElementById('org-panel-content');
    const akcijaId = orgPanel.dataset.akcijaId;

    async function odluciOPrijavi(action, korisnikId) {
      const url = `/akcije/${akcijaId}/prijave/${korisnikId}/${action}/`;
      try {
        const data = await apiFetch(url, { method: 'POST' });
        if (data.panel !== undefined) panelContent.innerHTML = data.panel;
        if (data.sidebar !== undefined) container.innerHTML = data.sidebar;
      } catch (err) {
        console.error(`${action} nije uspelo:`, err);
      }
    }

    orgPanel.addEventListener('click', (e) => {
      const prihvati = e.target.closest('.btn-prihvati');
      if (prihvati) {
        e.preventDefault();
        odluciOPrijavi('prihvati', prihvati.dataset.korisnikId);
        return;
      }
      const odbij = e.target.closest('.btn-odbij');
      if (odbij) {
        e.preventDefault();
        odluciOPrijavi('odbij', odbij.dataset.korisnikId);
      }
    });
  }
})();
