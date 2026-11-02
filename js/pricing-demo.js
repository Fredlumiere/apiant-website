/* Pricing demo mode for the API App product pages.
 *
 * Prices are hidden from visitors. Elements marked .pricing-demo-only (the pricing
 * calculator) show only when demo mode is on in this browser.
 *
 * Turn on:  open any API App page with ?pricing=<demo code>   (the code is not stored here,
 *           only its SHA-256 hash; ask Fred for it). It stays on in this browser until turned off.
 * Turn off: the "Hide pricing" pill at the bottom left, or ?pricing=off.
 *
 * This hides prices from ordinary visitors; it is not access control. The calculator is still
 * in the page source.
 */
(function () {
  var KEY = 'apiant.pricingDemo';
  var HASH = '87cc91ecaba3b3f4bf720e86af1e27db044a60ed6fd5a48c51504202f74e46c4';
  var root = document.documentElement;

  var style = document.createElement('style');
  style.setAttribute('data-apiant', 'pricing-demo-css');
  style.textContent =
    'html:not(.pricing-demo) .pricing-demo-only{display:none!important}' +
    '.pricing-demo-pill{position:fixed;left:16px;bottom:16px;z-index:2147483000;display:flex;gap:8px;align-items:center;' +
    'background:#111;color:#fff;font:600 12px/1 Inter,Arial,sans-serif;padding:8px 10px 8px 12px;border-radius:999px;' +
    'box-shadow:0 4px 16px rgba(0,0,0,.25)}' +
    '.pricing-demo-pill button{background:#1ab759;color:#fff;border:0;border-radius:999px;padding:6px 10px;font:inherit;cursor:pointer}';
  (document.head || root).appendChild(style);

  function get() { try { return localStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  function set(on) { try { on ? localStorage.setItem(KEY, '1') : localStorage.removeItem(KEY); } catch (e) {} }

  function pill() {
    if (document.querySelector('.pricing-demo-pill')) return;
    var p = document.createElement('div');
    p.className = 'pricing-demo-pill';
    p.innerHTML = '<span>Pricing visible (demo)</span><button type="button">Hide pricing</button>';
    p.querySelector('button').addEventListener('click', function () { set(false); apply(false); });
    document.body.appendChild(p);
  }
  function apply(on) {
    root.classList.toggle('pricing-demo', on);
    if (on) {
      if (document.body) pill(); else document.addEventListener('DOMContentLoaded', pill);
    } else {
      var p = document.querySelector('.pricing-demo-pill');
      if (p) p.remove();
    }
  }
  function cleanUrl() {
    try {
      var u = new URL(location.href);
      u.searchParams.delete('pricing');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch (e) {}
  }

  apply(get());

  var code = null;
  try { code = new URL(location.href).searchParams.get('pricing'); } catch (e) {}
  if (code === null) return;
  cleanUrl();
  if (code === 'off') { set(false); apply(false); return; }
  if (!(window.crypto && crypto.subtle && window.TextEncoder)) return;
  crypto.subtle.digest('SHA-256', new TextEncoder().encode(code)).then(function (buf) {
    var hex = Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
    if (hex === HASH) {
      set(true);
      apply(true);
    }
  });
})();
