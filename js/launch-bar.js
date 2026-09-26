/* APIANT.AI launch bar: hide it once a visitor dismisses it. Loaded directly after
   the bar markup so a dismissed bar is hidden before the rest of the page paints.
   Storage can throw (private mode, blocked site data); the bar then just shows. */
(function () {
  var KEY = 'apiant_aai_bar_dismissed';
  var bar = document.getElementById('aai-bar');
  if (!bar) return;
  try { if (localStorage.getItem(KEY) === '1') { bar.classList.add('is-hidden'); return; } } catch (e) {}
  var x = bar.querySelector('.aai-bar-x');
  if (!x) return;
  x.addEventListener('click', function () {
    bar.classList.add('is-hidden');
    try { localStorage.setItem(KEY, '1'); } catch (e) {}
  });
})();
