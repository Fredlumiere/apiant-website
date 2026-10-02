/* APIANT.AI launch bar: hide it once a visitor dismisses it, and keep --aai-h on <html>
   equal to the bar's height so the sticky headers in css/launch.css sit just below it.
   Loaded directly after the bar markup so a dismissed bar is hidden before the rest of the
   page paints. Storage can throw (private mode, blocked site data); the bar then just shows. */
(function () {
  var KEY = 'apiant_aai_bar_dismissed';
  var bar = document.getElementById('aai-bar');
  if (!bar) return;
  var root = document.documentElement;
  function sync() { root.style.setProperty('--aai-h', bar.offsetHeight + 'px'); }
  try { if (localStorage.getItem(KEY) === '1') { bar.classList.add('is-hidden'); return; } } catch (e) {}
  sync();
  if (window.ResizeObserver) new ResizeObserver(sync).observe(bar);
  else window.addEventListener('resize', sync);
  var x = bar.querySelector('.aai-bar-x');
  if (!x) return;
  x.addEventListener('click', function () {
    bar.classList.add('is-hidden');
    root.style.setProperty('--aai-h', '0px');
    try { localStorage.setItem(KEY, '1'); } catch (e) {}
  });
})();
