// Autor: Milica Milošević 0357/2023
// Autor: Maša Nikolić 2023/0089
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

  // Organizator panel (SSU 17, SSU 18) — tab switching + Prihvati/Odbij
  const orgPanel = document.getElementById('org-panel');
  if (!orgPanel) return;

  const akcijaId = orgPanel.dataset.akcijaId;

  // ── Tab switching ────────────────────────────────────────────────────────

  function switchOrgTab(activeId) {
    ['org-vol', 'org-sp', 'org-obavestenje', 'org-izmeni'].forEach(id => {
      const el  = document.getElementById(id);
      const btn = document.getElementById('otab-' + id);
      if (el)  el.style.display = id === activeId ? '' : 'none';
      if (btn) {
        btn.style.borderBottomColor = id === activeId ? 'var(--teal)' : 'transparent';
        btn.style.color             = id === activeId ? 'var(--teal)' : 'var(--text-muted)';
      }
    });
  }

  // ── Prijave volontera (SSU 18) ───────────────────────────────────────────

  async function odluciOPrijavi(action, korisnikId) {
    const url = `/akcije/${akcijaId}/prijave/${korisnikId}/${action}/`;
    try {
      const data = await apiFetch(url, { method: 'POST' });
      if (data.panel !== undefined) {
        document.getElementById('org-vol').innerHTML = data.panel;
      }
      if (data.sidebar !== undefined) container.innerHTML = data.sidebar;
    } catch (err) {
      console.error(`${action} nije uspelo:`, err);
    }
  }

  // ── Sponzorske ponude (SSU 17) ───────────────────────────────────────────

  async function odluciOPonudi(action, ponudaId) {
    const url = `/akcije/${akcijaId}/ponude/${ponudaId}/${action}/`;
    try {
      const data = await apiFetch(url, { method: 'POST' });
      if (data.ponude !== undefined) {
        document.getElementById('org-sp').innerHTML = data.ponude;
      }
      const badge = document.getElementById('org-sp-badge');
      if (badge && data.br_na_cekanju !== undefined) {
        if (data.br_na_cekanju > 0) {
          badge.textContent = data.br_na_cekanju;
          badge.style.display = '';
        } else {
          badge.style.display = 'none';
        }
      }
    } catch (err) {
      const spPanel = document.getElementById('org-sp');
      if (spPanel) {
        const msg = document.createElement('div');
        msg.className = 'alert alert-error';
        msg.style.marginBottom = '16px';
        msg.innerHTML = `<i class="bi bi-exclamation-circle"></i> <span>${err.message}</span>`;
        spPanel.insertBefore(msg, spPanel.firstChild);
        setTimeout(() => msg.remove(), 5000);
      }
    }
  }

  // ── Slanje obaveštenja volonterima (SSU 8) ───────────────────────────────

  function prikaziObavestenjeRezultat(tip, tekst) {
    const box = document.getElementById('obavestenje-rezultat');
    if (!box) return;
    const klasa = tip === 'ok' ? 'alert-success' : 'alert-error';
    const ikona = tip === 'ok' ? 'check-circle-fill' : 'exclamation-circle';
    box.innerHTML = `<div class="alert ${klasa}" style="display:flex;margin-bottom:16px;">`
      + `<i class="bi bi-${ikona}"></i> <span>${tekst}</span></div>`;
  }

  async function posaljiObavestenje(forma) {
    const textarea = document.getElementById('obavestenje-tekst');
    const dugme = document.getElementById('btn-posalji-obavestenje');
    const poruka = (textarea?.value || '').trim();

    // SSU 8, 2.2.2 — prazna poruka se ne šalje (provera i na klijentu i na serveru).
    if (!poruka) {
      prikaziObavestenjeRezultat('greska', 'Unesite tekst poruke.');
      textarea?.focus();
      return;
    }

    if (dugme) dugme.disabled = true;
    try {
      const data = await apiFetch(`/akcije/${akcijaId}/obavestenje/`, {
        method: 'POST',
        body: JSON.stringify({ poruka }),
      });
      prikaziObavestenjeRezultat('ok', data.poruka || 'Obaveštenje je poslato.');
      if (textarea) textarea.value = '';
    } catch (err) {
      prikaziObavestenjeRezultat('greska', err.message);
    } finally {
      if (dugme) dugme.disabled = false;
    }
  }

  // ── Izmena i otkazivanje akcije (SSU 10) ─────────────────────────────────

  async function sacuvajIzmene(forma) {
    const dugme = document.getElementById('btn-sacuvaj-izmene');
    if (dugme) dugme.disabled = true;
    try {
      // Multipart (slike) — ne ide kroz apiFetch (JSON), već običan fetch sa FormData.
      const response = await fetch(`/akcije/${akcijaId}/izmeni/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken(), 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(forma),
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      // Server vraća osvežen fragment (sa greškama ili porukom o uspehu).
      const panel = document.getElementById('org-izmeni');
      if (panel) panel.innerHTML = await response.text();
    } catch (err) {
      console.error('Čuvanje izmena nije uspelo:', err);
      if (dugme) dugme.disabled = false;
    }
  }

  async function otkaziAkciju() {
    // SSU 10, 2.2.9 korak 5 — potvrda pre otkazivanja.
    if (!confirm('Da li ste sigurni da želite da otkažete ovu akciju? '
                 + 'Svi prijavljeni volonteri biće obavešteni emailom.')) return;
    try {
      await apiFetch(`/akcije/${akcijaId}/otkazi/`, { method: 'POST' });
      window.location.reload();  // status se menja na više mesta na strani
    } catch (err) {
      alert(err.message);
    }
  }

  orgPanel.addEventListener('submit', (e) => {
    if (e.target.closest('#obavestenje-forma')) {
      e.preventDefault();
      posaljiObavestenje(e.target.closest('#obavestenje-forma'));
    } else if (e.target.closest('#izmeni-forma')) {
      e.preventDefault();
      sacuvajIzmene(e.target.closest('#izmeni-forma'));
    }
  });

  // ── Delegirani click handler ─────────────────────────────────────────────

  orgPanel.addEventListener('click', (e) => {
    const tabBtn = e.target.closest('[data-tab-target]');
    if (tabBtn) {
      e.preventDefault();
      switchOrgTab(tabBtn.dataset.tabTarget);
      return;
    }

    if (e.target.closest('#btn-otkazi-akciju')) {
      e.preventDefault();
      otkaziAkciju();
      return;
    }

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
      return;
    }

    const prihvatiPonudu = e.target.closest('.btn-prihvati-ponudu');
    if (prihvatiPonudu) {
      e.preventDefault();
      odluciOPonudi('prihvati', prihvatiPonudu.dataset.ponudaId);
      return;
    }
    const odbijPonudu = e.target.closest('.btn-odbij-ponudu');
    if (odbijPonudu) {
      e.preventDefault();
      odluciOPonudi('odbij', odbijPonudu.dataset.ponudaId);
    }
  });
})();
