// Autor: Maša Nikolić 2023/0089
// ── Lista akcija: Ajax filtriranje bez reload-a (SSU 3) ─────────────────────
//
// Presrećemo submit forme i promene svakog input/select-a, gradimo URL sa
// aktuelnim filterima, i preko fetch-a pozivamo isti view koji za Ajax zahtev
// vraća samo _akcije_grid.html fragment. Zamenjujemo unutrašnjost kontejnera
// i menjamo URL u pregledaču (bez reload-a) da bi share/refresh radili.

(function () {
  const form = document.getElementById('filter-form');
  const container = document.getElementById('akcije-container');
  if (!form || !container) return;

  async function primeniFiltere(page) {
    const params = new URLSearchParams(new FormData(form));
    if (page) params.set('page', page);
    const query = params.toString();
    const url = window.location.pathname + (query ? '?' + query : '');

    try {
      const response = await fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      container.innerHTML = await response.text();
      history.replaceState(null, '', url);
    } catch (err) {
      console.error('Filtriranje nije uspelo:', err);
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    primeniFiltere();
  });

  function resetujFiltere() {
    form.reset();
    form.querySelectorAll('select').forEach((s) => (s.value = ''));
    primeniFiltere();
  }

  const clearBtn = document.getElementById('clear-all');
  if (clearBtn) {
    clearBtn.addEventListener('click', (e) => {
      e.preventDefault();
      resetujFiltere();
    });
  }

  form.querySelectorAll('select, input[type="date"]').forEach((el) => {
    el.addEventListener('change', primeniFiltere);
  });

  let debounce;
  form.querySelector('input[name="q"]').addEventListener('input', () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => primeniFiltere(), 300);
  });

  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.page-btn[data-page]');
    if (btn && !btn.disabled) {
      e.preventDefault();
      primeniFiltere(btn.dataset.page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    if (e.target.closest('#reset-filters')) {
      e.preventDefault();
      resetujFiltere();
    }
  });

  // Sort select je unutar container-a (menja se pri svakom Ajax osvežavanju),
  // pa listener ide na container preko delegacije.
  container.addEventListener('change', (e) => {
    if (e.target.matches('select[name="sort"]')) primeniFiltere();
  });
})();
