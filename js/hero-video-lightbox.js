/* Hero video lightbox for the API App product pages.
 *
 * Works on the .zc-hero-video block (one .zc-vid.zc-wide 16:9 player and one .zc-vid.zc-tall 9:16 player,
 * Wistia <wistia-player> web components). Clicking a player moves it into a centred full-screen overlay and
 * starts playback. Close with the button, a click on the backdrop, or Esc.
 *
 * Deep links open the overlay on load:
 *   ?video=wide | ?video=vertical | ?video=1 (the variant that suits the screen)
 *   #video | #video-wide | #video-vertical
 * Browsers block audible autoplay without a click, so a deep link plays muted and Wistia shows its unmute button.
 *
 * The player is moved, not cloned: Wistia re-initialises it on the move, so playback starts from 0:00.
 * It is moved to <body> because the hero's ancestors create stacking contexts that would keep a fixed
 * overlay underneath the page.
 */
(function () {
  if (window.__apiantHeroLightbox) return;
  window.__apiantHeroLightbox = true;

  var css =
    ".zc-catch{position:absolute;inset:0;z-index:4;cursor:zoom-in;background:transparent;border-radius:12px}" +
    ".zc-vid.zc-lb .zc-catch{display:none}" +
    ".zc-hero-video.zc-lbwrap{position:fixed;inset:0;margin:0;z-index:100000;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.88);animation:zcFade .3s ease}" +
    ".zc-hero-video .zc-vid.zc-lb{display:block!important;width:min(92vw,calc(88vh * 16 / 9));max-width:none;margin:0;animation:zcIn .35s cubic-bezier(.22,1,.36,1)}" +
    ".zc-hero-video .zc-tall.zc-lb{width:min(92vw,calc(88vh * 9 / 16))}" +
    "@keyframes zcFade{from{opacity:0}to{opacity:1}}" +
    "@keyframes zcIn{from{opacity:0;transform:scale(.9)}to{opacity:1;transform:scale(1)}}" +
    ".zc-lb-x{position:absolute;top:14px;right:22px;font-size:40px;line-height:1;font-weight:300;color:#fff;background:none;border:0;cursor:pointer;padding:4px 8px}";
  var st = document.createElement("style");
  st.setAttribute("data-apiant", "hero-video-lightbox");
  st.textContent = css;
  document.head.appendChild(st);

  var cur = null, home = null, wrap = null;

  // play() can resolve before the player is ready, or be refused (autoplay policy). Retry until it is playing,
  // muting after a few refusals so a deep link without a click still plays.
  function go(p, n) {
    if (!cur || !p || p.state === "playing" || n > 40) return;
    if (n > 6) { try { p.muted = true; } catch (e) {} }
    try { var r = p.play(); if (r && r.catch) r.catch(function () {}); } catch (e) {}
    setTimeout(function () { go(p, n + 1); }, 400);
  }

  function open(v) {
    if (cur) return;
    home = document.createElement("div");
    home.style.height = v.offsetHeight + "px";
    v.parentNode.insertBefore(home, v);
    wrap = document.createElement("div");
    wrap.className = "zc-hero-video zc-lbwrap";
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-modal", "true");
    wrap.setAttribute("aria-label", "Video");
    var x = document.createElement("button");
    x.type = "button";
    x.className = "zc-lb-x";
    x.setAttribute("aria-label", "Close video");
    x.innerHTML = "&times;";
    x.addEventListener("click", close);
    wrap.addEventListener("click", function (e) { if (e.target === wrap) close(); });
    wrap.appendChild(x);
    v.classList.add("zc-lb");
    wrap.appendChild(v);
    document.body.appendChild(wrap);
    document.documentElement.style.overflow = "hidden";
    cur = v;
    go(v.querySelector("wistia-player"), 0);
    x.focus();
  }

  function close() {
    if (!cur) return;
    var p = cur.querySelector("wistia-player");
    try { p.pause(); } catch (e) {}
    cur.classList.remove("zc-lb");
    home.parentNode.insertBefore(cur, home);
    home.remove();
    wrap.remove();
    home = wrap = null;
    document.documentElement.style.overflow = "";
    var c = cur.querySelector(".zc-catch");
    cur = null;
    if (c) c.focus({ preventScroll: true });
  }

  function init() {
    document.querySelectorAll(".zc-hero-video .zc-vid").forEach(function (v) {
      if (v.querySelector(".zc-catch")) return;
      var c = document.createElement("div");
      c.className = "zc-catch";
      c.setAttribute("role", "button");
      c.setAttribute("tabindex", "0");
      c.setAttribute("aria-label", "Play video full size");
      c.addEventListener("click", function () { open(v); });
      c.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(v); }
      });
      v.appendChild(c);
      // The end-of-film CTA (pricing anchor or demo popup) must land on the page, not behind the overlay.
      v.querySelectorAll(".zc-cta").forEach(function (a) {
        a.addEventListener("click", function () { if (cur) close(); }, true);
      });
    });

    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });

    var q = (location.search.match(/[?&](?:video|play)=([a-z0-9]+)/i) || [])[1];
    if (!q) {
      var h = location.hash.match(/^#(?:video|play)(?:-([a-z0-9]+))?$/i);
      if (h) q = h[1] || "1";
    }
    if (!q) return;
    q = q.toLowerCase();
    var auto = function () {
      var sel = /^(wide|widescreen|desktop|landscape|16x9)$/.test(q) ? ".zc-wide"
              : /^(vertical|tall|mobile|portrait|9x16)$/.test(q) ? ".zc-tall" : null;
      var t = null;
      if (sel) {
        t = document.querySelector(".zc-hero-video " + sel);
      } else {
        var vs = document.querySelectorAll(".zc-hero-video .zc-vid");
        for (var i = 0; i < vs.length; i++) { if (vs[i].offsetParent !== null) { t = vs[i]; break; } }
      }
      if (t) open(t);
    };
    if (window.customElements) customElements.whenDefined("wistia-player").then(auto); else auto();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
