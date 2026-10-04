/* Progressive enhancement: navigation and content remain usable without JS. */
(() => {
  'use strict';
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const menuButton = document.querySelector('[data-home-menu]');
  const navigation = document.getElementById('home-navigation');
  if (menuButton && navigation) {
    const desktop = window.matchMedia('(min-width: 1280px)');
    navigation.dataset.enhanced = '';
    menuButton.hidden = false;
    const setMenu = (open, restoreFocus = false) => {
      navigation.classList.toggle('is-open', open);
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.querySelector('span').textContent = open ? 'Close' : 'Menu';
      if (restoreFocus) menuButton.focus();
    };
    menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && navigation.classList.contains('is-open')) setMenu(false, true);
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.home-header')) setMenu(false);
    });
    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) setMenu(false);
    });
    desktop.addEventListener('change', () => setMenu(false));
  }

  const carousel = document.querySelector('[data-home-carousel]');
  const slides = carousel ? [...carousel.querySelectorAll('[data-home-slide]')] : [];
  if (slides.length > 1) {
    const controls = carousel.querySelector('[data-home-controls]');
    const dots = [...carousel.querySelectorAll('[data-home-dot]')];
    const pause = carousel.querySelector('[data-home-pause]');
    const status = carousel.querySelector('[data-home-status]');
    let current = 0;
    let paused = motion.matches;
    let hovered = false;
    let inView = true;
    let timer;
    let pauseIntent = null;
    controls.hidden = false;
    const refreshTimer = () => {
      window.clearInterval(timer);
      status.setAttribute('aria-live', paused ? 'polite' : 'off');
      if (!paused && !hovered && inView && !document.hidden) {
        timer = window.setInterval(() => show(current + 1), 6500);
      }
    };
    const updatePause = () => {
      pause.textContent = paused ? 'Play' : 'Pause';
      pause.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
      refreshTimer();
    };
    const show = index => {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, i) => {
        slide.classList.toggle('is-active', i === current);
        slide.setAttribute('aria-hidden', String(i !== current));
        slide.inert = i !== current;
      });
      dots.forEach((dot, i) => {
        if (i === current) dot.setAttribute('aria-current', 'true');
        else dot.removeAttribute('aria-current');
      });
      status.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    };
    const manual = index => { paused = true; show(index); updatePause(); };
    carousel.querySelector('[data-home-prev]').addEventListener('click', () => manual(current - 1));
    carousel.querySelector('[data-home-next]').addEventListener('click', () => manual(current + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => manual(i)));
    // Capture pointer intent before focusin pauses the carousel.
    pause.addEventListener('pointerdown', () => { pauseIntent = !paused; });
    pause.addEventListener('pointercancel', () => { pauseIntent = null; });
    pause.addEventListener('click', () => {
      paused = pauseIntent === null ? !paused : pauseIntent;
      pauseIntent = null;
      updatePause();
    });
    controls.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        manual(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    // Keyboard focus stops rotation until the visitor explicitly presses Play.
    carousel.addEventListener('focusin', () => { paused = true; updatePause(); });
    carousel.addEventListener('mouseenter', () => { hovered = true; refreshTimer(); });
    carousel.addEventListener('mouseleave', () => { hovered = false; refreshTimer(); });
    document.addEventListener('visibilitychange', refreshTimer);
    motion.addEventListener('change', () => { if (motion.matches) { paused = true; updatePause(); } });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting;
        refreshTimer();
      }).observe(carousel);
    }
    show(0);
    updatePause();
  }

  // Only two photographic compositions reveal; content is never hidden by default.
  if ('IntersectionObserver' in window && !motion.matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('home-reveal-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('[data-home-reveal]').forEach(element => observer.observe(element));
  }
})();
