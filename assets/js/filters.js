/* キャラクターフィルタリング */
(() => {
  const btns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.char-card');

  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      cards.forEach(card => {
        if (filter === 'all' || card.dataset.type === filter || card.dataset.faction === filter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
})();
