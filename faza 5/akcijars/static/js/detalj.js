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
})();
