(() => {
  const shell = document.querySelector('[data-indra-shell]');
  if (!shell) return;

  const toggle = shell.querySelector('[data-paper-theme-toggle]');
  const storedTheme = window.localStorage.getItem('research-paper-theme');
  if (storedTheme === 'dark') {
    shell.dataset.paperTheme = 'dark';
    if (toggle) toggle.setAttribute('aria-pressed', 'true');
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      const dark = shell.dataset.paperTheme !== 'dark';
      if (dark) {
        shell.dataset.paperTheme = 'dark';
        window.localStorage.setItem('research-paper-theme', 'dark');
      } else {
        delete shell.dataset.paperTheme;
        window.localStorage.setItem('research-paper-theme', 'light');
      }
      toggle.setAttribute('aria-pressed', String(dark));
      toggle.textContent = dark ? '밝은 화면' : '어두운 화면';
    });
  }

  shell.querySelectorAll('[data-paper-carousel]').forEach((carousel) => {
    const track = carousel.querySelector('[data-carousel-track]');
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    if (!track) return;

    const step = () => Math.max(track.clientWidth * 0.78, 280);
    previous?.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
    next?.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
  });

  const scrollTop = shell.querySelector('[data-scroll-top]');
  const updateScrollTop = () => {
    if (!scrollTop) return;
    scrollTop.classList.toggle('is-visible', window.scrollY > 700);
  };
  window.addEventListener('scroll', updateScrollTop, { passive: true });
  updateScrollTop();
  scrollTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();
