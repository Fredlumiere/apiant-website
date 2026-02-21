/**
 * Demo form reveal for API App product pages.
 * Uses capturing phase to intercept clicks before Webflow's
 * smooth-scroll handler can process the #Demo anchor.
 *
 * On load, fetches /admin/config.json and sets the demo iframe
 * src from config.demos[filename].demoUrl. Falls back to the
 * existing HTML src if the fetch fails or no entry is found.
 */
(function() {

  // --- Dynamic demo URL loading from config ---
  document.addEventListener('DOMContentLoaded', function() {
    fetch('/admin/config.json')
      .then(function(response) {
        if (!response.ok) {
          throw new Error('Config fetch failed: ' + response.status);
        }
        return response.json();
      })
      .then(function(config) {
        if (!config || !config.demos) return;

        // Extract filename without extension from the current path.
        // e.g. /apipartners/mindbody/mindbody-shopify-integration-and-automation-apiant.html
        // becomes "mindbody-shopify-integration-and-automation-apiant"
        var pathname = window.location.pathname;
        var parts = pathname.split('/');
        var lastSegment = parts[parts.length - 1] || '';
        var filename = lastSegment.replace(/\.html$/, '');

        if (!filename) return;

        var entry = config.demos[filename];
        if (!entry || !entry.demoUrl) return;

        var iframe = document.querySelector('.demo-embed iframe');
        if (iframe) {
          iframe.setAttribute('src', entry.demoUrl);
        }
      })
      .catch(function() {
        // Graceful degradation: keep whatever src is already in the HTML.
      });
  });

  // --- Click handlers for demo reveal / dismiss ---

  // Capture phase fires before Webflow's bubbling handlers
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a[href="#Demo"]');
    if (!link) return;
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    var hero = document.querySelector('.section.white-hero');
    if (hero) hero.classList.add('demo-active');
    return false;
  }, true);

  document.addEventListener('click', function(e) {
    var back = e.target.closest('.demo-back-link');
    if (!back) return;
    e.preventDefault();
    var hero = document.querySelector('.section.white-hero');
    if (hero) hero.classList.remove('demo-active');
  }, true);
})();
