/**
 * APIANT Blog: subtle full-page particle background.
 *
 * Recreates the old blog hero's particles.js effect, adapted for the dark
 * theme and applied behind the whole page (#blog-particles is a fixed,
 * pointer-events:none canvas at z-index -1). Drift-only: interactivity is
 * disabled because the canvas sits behind the content.
 *
 * Respects prefers-reduced-motion and thins the field on small screens so
 * it never costs readability or mobile performance.
 */
(function () {
  var host = document.getElementById('blog-particles');
  if (!host || typeof particlesJS === 'undefined') return;

  // Accessibility: honor reduced-motion by drawing nothing.
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  var w = window.innerWidth || document.documentElement.clientWidth;
  // Thin the field on phones/tablets; keep it light everywhere.
  var count = w < 600 ? 22 : (w < 1024 ? 40 : 60);

  // Brand green on the dark canvas, low opacity so body text stays readable.
  var ACCENT = '#1ab759';

  particlesJS('blog-particles', {
    particles: {
      number: { value: count, density: { enable: true, value_area: 900 } },
      color: { value: ACCENT },
      shape: { type: 'circle' },
      opacity: { value: 0.35, random: true, anim: { enable: false } },
      size: { value: 3, random: true },
      line_linked: {
        enable: true,
        distance: 130,
        color: ACCENT,
        opacity: 0.18,
        width: 1,
      },
      move: {
        enable: true,
        speed: 0.6,
        direction: 'top-right',
        random: false,
        straight: false,
        out_mode: 'out',
        bounce: false,
      },
    },
    // Behind content + pointer-events:none, so no hover/click interactivity.
    interactivity: {
      detect_on: 'canvas',
      events: { onhover: { enable: false }, onclick: { enable: false }, resize: true },
    },
    retina_detect: true,
  });
})();
