/*
  Compare switch: one control, used by the homepage selector and by the competitor
  name in each /compare/ page's H1. Loaded on both, so there is a single definition
  of the behaviour rather than one copy per page.

  MARKUP CONTRACT

    <div class="cmpsw cmpsw--pill" data-cmpsw>
      <h3>Some heading text
        <button class="cmpsw-btn" type="button" aria-expanded="false">Label<svg/></button>
      </h3>
      <span class="cmpsw-menu">
        <a href="/compare/prismatic">Prismatic<span class="cmpsw-n">60</span></a>
        ...
        <a class="cmpsw-all" href="/compare/">All comparisons</a>
      </span>
    </div>

  WHY THE MENU IS A SIBLING OF THE HEADING AND NOT INSIDE IT. The first version of the
  homepage selector nested a details element in the heading so it would open without
  JavaScript. The consequence was that every competitor name in the menu became part of
  the heading's own text: the h3 read "How does APIANT compare with pick a platform
  Prismatic60 caps Zapier60 caps ..." to anything reading text rather than pixels. A
  heading is the strongest on-page signal there is and it is not a place to keep a link
  list. The heading now holds only the button, so its text stays exactly what it says on
  screen, and the price of that is this file: the open and close is ours to run.

  The competitors are real anchors, not select options, so all of them ship in the HTML
  where crawlers and answer engines can read them, and each compare page links to every
  other one. The select this replaced built its options in script and emitted no links
  at all.
*/
(function () {
  'use strict';

  function wire(root) {
    var btn = root.querySelector('.cmpsw-btn');
    var menu = root.querySelector('.cmpsw-menu');
    if (!btn || !menu) return;

    function set(open) {
      menu.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      set(btn.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('click', function (e) {
      if (!root.contains(e.target)) set(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
        set(false);
        btn.focus();
      }
    });

    /* Pick up any competitor added to competitors.json after this page shipped, so a
       ninth comparison needs no edit to the homepage or to the eight existing pages.
       Only ever appends: the hard-coded entries stay the crawlable floor if the fetch
       fails, and a page never links to itself. */
    /* Which page are we on? Read it from the markup. Deriving it from
       location.pathname works for the live extensionless URLs and fails for any
       other path shape, which put the current competitor in its own menu. */
    var self = root.getAttribute('data-cmpsw-self')
           || (location.pathname.match(/\/compare\/([a-z0-9.-]+?)(?:\.html)?$/) || [])[1]
           || '';
    var all = menu.querySelector('.cmpsw-all');
    fetch('/compare/competitors.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (list) {
        if (!Array.isArray(list)) return;
        var have = {};
        Array.prototype.forEach.call(menu.querySelectorAll('a[href^="/compare/"]'), function (a) {
          have[a.getAttribute('href').replace('/compare/', '').replace(/\.html$/, '')] = 1;
        });
        list.forEach(function (c) {
          if (!c || c.live === false || !c.slug) return;
          if (have[c.slug] || c.slug === self) return;
          var a = document.createElement('a');
          a.href = '/compare/' + c.slug;
          a.textContent = c.name || c.slug;
          if (all) menu.insertBefore(a, all); else menu.appendChild(a);
        });
      })
      .catch(function () {});
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-cmpsw]'), wire);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
