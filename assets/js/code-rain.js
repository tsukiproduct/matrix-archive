/* ============================================
   MATRIX CODE RAIN — Restrained, performance-aware
   Not the obvious imitation. Sparse, slow, almost still.
   ============================================ */
(() => {
  const canvas = document.getElementById('code-rain');
  if (!canvas) return;

  const ctx = canvas.getContext('2d', { alpha: true });
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ<>{}[]/\\='.split('');

  let cols, drops, fontSize = 14;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    cols = Math.floor(canvas.width / fontSize);
    drops = new Array(cols).fill(0).map(() =>
      Math.random() * canvas.height / fontSize
    );
  }
  resize();
  window.addEventListener('resize', resize);

  let lastFrame = 0;
  const FRAME_INTERVAL = 80; // slow, ~12fps. Atmospheric, not busy.

  function draw(now) {
    if (now - lastFrame < FRAME_INTERVAL) {
      requestAnimationFrame(draw);
      return;
    }
    lastFrame = now;

    // Fade previous frame — gentle, leaves long trails
    ctx.fillStyle = 'rgba(10, 15, 10, 0.08)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#4ade80';
    ctx.font = fontSize + 'px JetBrains Mono, monospace';

    for (let i = 0; i < drops.length; i++) {
      // Only update some columns each frame — sparse aesthetic
      if (Math.random() > 0.7) continue;

      const ch = chars[Math.floor(Math.random() * chars.length)];
      ctx.fillText(ch, i * fontSize, drops[i] * fontSize);

      if (drops[i] * fontSize > canvas.height && Math.random() > 0.98) {
        drops[i] = 0;
      }
      drops[i] += 0.5;
    }

    requestAnimationFrame(draw);
  }

  // Respect reduced motion
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    requestAnimationFrame(draw);
  }
})();
