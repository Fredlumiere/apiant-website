/**
 * Demo form reveal for API App product pages.
 * Uses capturing phase to intercept clicks before Webflow's
 * smooth-scroll handler can process the #Demo anchor.
 */
(function() {
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
