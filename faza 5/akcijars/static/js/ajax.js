// Autor: Stefan Grujičić 0030/2023
// ── AkcijaRS Ajax helper ─────────────────────────────────────────────────────
//
// Django postavlja kolačić "csrftoken" pri svakom učitavanju stranice.
// Svaki POST/PUT/PATCH/DELETE zahtev mora da nosi taj token u zaglavlju
// X-CSRFToken da bi prošao CSRF middleware.

function getCsrfToken() {
  // document.cookie je niz: "csrftoken=abc123; sessionid=xyz"
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

// Wrapper oko fetch() koji automatski:
//   • dodaje Content-Type / Accept: application/json
//   • za POST/PUT/PATCH/DELETE ubacuje X-CSRFToken zaglavlje
//   • za ne-2xx odgovor baca Error sa server porukom
async function apiFetch(url, options = {}) {
  const method = (options.method || 'GET').toUpperCase();

  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  };

  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    headers['X-CSRFToken'] = getCsrfToken();
  }

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      message = data.error || data.detail || message;
    } catch (_) { /* odgovor nije JSON */ }
    throw new Error(message);
  }

  return response.json();
}
