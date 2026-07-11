// Autor: Stefan Grujičić 0030/2023
// Ajax dodavanje komentara na članak (SSU 12)
// AJAX_URL mora biti definisan pre učitavanja ovog fajla (injektuje ga template).

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('submit-comment');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    const input = document.getElementById('comment-input');
    const errEl = document.getElementById('comment-error');
    const sucEl = document.getElementById('comment-success');
    const tekst = input.value.trim();

    errEl.style.display = 'none';
    sucEl.style.display = 'none';

    if (!tekst) {
      errEl.innerHTML = '<i class="bi bi-exclamation-circle"></i> Komentar ne može biti prazan!';
      errEl.style.display = 'flex';
      return;
    }

    btn.disabled = true;
    try {
      const data = await apiFetch(AJAX_URL, {
        method: 'POST',
        body: JSON.stringify({ tekst }),
      });

      input.value = '';
      document.getElementById('comments-list').innerHTML = data.html;
      document.querySelectorAll('#comment-count, #comment-count-2').forEach(
        el => (el.textContent = data.br_komentara)
      );

      sucEl.innerHTML = '<i class="bi bi-check-circle-fill"></i> Komentar je uspešno objavljen.';
      sucEl.style.display = 'flex';
      setTimeout(() => (sucEl.style.display = 'none'), 3000);
    } catch (err) {
      errEl.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${err.message}`;
      errEl.style.display = 'flex';
    } finally {
      btn.disabled = false;
    }
  });
});
