/* Progressive enhancement: content stays visible without JavaScript or observers. */
(() => {
  document.body.classList.add('about-js');
  // The base template owns toggling; keep its state accessible on this page.
  const button = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (button && menu) {
    const syncMenu = () => {
      const open = !menu.classList.contains('hidden');
      button.setAttribute('aria-expanded', String(open));
      button.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    button.setAttribute('aria-controls', menu.id);
    syncMenu();
    button.addEventListener('click', syncMenu);
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !menu.classList.contains('hidden')) {
        button.click();
        button.focus();
      }
    });
  }
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (motion.matches || !('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      if (!motion.matches) {
        entry.target.classList.add('about-reveal');
        // Release the animation transform so later pointer interactions stay free.
        entry.target.addEventListener('animationend', () => {
          entry.target.classList.remove('about-reveal');
        }, { once: true });
      }
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('[data-about-reveal]').forEach((item) => observer.observe(item));
  motion.addEventListener('change', (event) => {
    if (!event.matches) return;
    observer.disconnect();
    document.querySelectorAll('.about-reveal').forEach((item) => item.classList.remove('about-reveal'));
  });
})();
