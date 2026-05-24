/* Save language choice when user clicks the language toggle */
(() => {
  const link = document.querySelector('[data-lang-switch]');
  if (!link) return;
  link.addEventListener('click', () => {
    try {
      const lang = link.getAttribute('data-lang-switch');
      localStorage.setItem('matrix-archive-lang', lang);
    } catch (e) { /* private mode etc. */ }
  });
})();
