/**
 * APIANT Blog: client-side search + load-more pagination for the hub
 * and category pages.
 *
 * Behavior:
 *   - On load: hides cards past the page size, shows a "Load more" button
 *   - When the search input has >=2 chars: replace the visible card grid
 *     with Fuse.js fuzzy results from /blog/search-index.json
 *   - When the input is cleared: restore the paginated view
 *
 * Locale-aware: if served from /{lang}/blog/..., we link results to the
 * locale-prefixed post URLs. The search-index.json lives at the English
 * /blog/search-index.json (titles/excerpts are English; the post pages
 * themselves are localized).
 */
(function () {
  var PAGE_SIZE = 12;
  var SEARCH_INDEX_URL = '/blog/search-index.json';

  var LANGUAGES = [
    { code: 'en', native: 'EN', name: 'English' },
    { code: 'es', native: 'ES', name: 'Español' },
    { code: 'fr', native: 'FR', name: 'Français' },
    { code: 'de', native: 'DE', name: 'Deutsch' },
    { code: 'it', native: 'IT', name: 'Italiano' },
    { code: 'pt', native: 'PT', name: 'Português' },
    { code: 'nl', native: 'NL', name: 'Nederlands' },
    { code: 'pl', native: 'PL', name: 'Polski' },
    { code: 'sv', native: 'SV', name: 'Svenska' },
    { code: 'ru', native: 'RU', name: 'Русский' },
    { code: 'tr', native: 'TR', name: 'Türkçe' },
    { code: 'ar', native: 'AR', name: 'العربية' },
    { code: 'he', native: 'HE', name: 'עברית' },
    { code: 'hi', native: 'HI', name: 'हिन्दी' },
    { code: 'bn', native: 'BN', name: 'বাংলা' },
    { code: 'th', native: 'TH', name: 'ไทย' },
    { code: 'vi', native: 'VI', name: 'Tiếng Việt' },
    { code: 'id', native: 'ID', name: 'Bahasa Indonesia' },
    { code: 'ja', native: 'JA', name: '日本語' },
    { code: 'ko', native: 'KO', name: '한국어' },
    { code: 'zh', native: 'ZH', name: '中文' },
  ];

  // Detect locale prefix from URL: /es/blog/... -> "es", /blog/... -> ""
  function detectLocale() {
    var m = window.location.pathname.match(/^\/([a-z]{2})\/blog\//);
    return m ? m[1] : '';
  }

  var locale = detectLocale();

  // -------- language dropdown population --------
  (function buildLangSwitcher() {
    var btn = document.querySelector('.blog-lang-switcher-btn');
    var dd = document.querySelector('.blog-lang-switcher-dropdown');
    var current = document.querySelector('.blog-lang-switcher-current');
    if (!btn || !dd) return;

    var activeCode = locale || 'en';
    if (current) current.textContent = (activeCode || 'en').toUpperCase();

    function buildLocalizedPath(targetCode) {
      var path = window.location.pathname;
      // Strip existing locale prefix if any.
      path = path.replace(/^\/[a-z]{2}\//, '/');
      if (targetCode === 'en') return path;
      return '/' + targetCode + path;
    }

    dd.innerHTML = LANGUAGES.map(function (lng) {
      var cls = lng.code === activeCode ? ' class="current"' : '';
      return '<a href="' + buildLocalizedPath(lng.code) + '"' + cls +
        '>' + lng.native + ' &middot; ' + lng.name + '</a>';
    }).join('');

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      dd.classList.toggle('open');
      btn.setAttribute('aria-expanded', dd.classList.contains('open'));
    });
    document.addEventListener('click', function () {
      dd.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    });
  })();
  function localizeHref(href) {
    if (!locale) return href;
    if (href.indexOf('/' + locale + '/') === 0) return href;
    if (href.indexOf('/blog') === 0) return '/' + locale + href;
    return href;
  }

  // -------- pagination on server-rendered cards --------
  var grid = document.querySelector('.blog-grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.blog-card'));
  var totalCards = cards.length;

  function paginate() {
    if (totalCards <= PAGE_SIZE) {
      removeLoadMore();
      return;
    }
    var shown = parseInt(grid.dataset.shown || '0', 10) || PAGE_SIZE;
    cards.forEach(function (c, i) {
      c.style.display = i < shown ? '' : 'none';
    });
    var loadMore = ensureLoadMore();
    if (shown >= totalCards) {
      removeLoadMore();
    } else {
      loadMore.textContent = 'Show more (' + (totalCards - shown) + ' remaining)';
    }
  }

  function ensureLoadMore() {
    var existing = document.getElementById('blog-load-more');
    if (existing) return existing;
    var btn = document.createElement('button');
    btn.id = 'blog-load-more';
    btn.className = 'blog-load-more';
    btn.type = 'button';
    btn.addEventListener('click', function () {
      var shown = parseInt(grid.dataset.shown || String(PAGE_SIZE), 10);
      grid.dataset.shown = String(Math.min(shown + PAGE_SIZE, totalCards));
      paginate();
    });
    grid.parentNode.insertBefore(btn, grid.nextSibling);
    return btn;
  }

  function removeLoadMore() {
    var existing = document.getElementById('blog-load-more');
    if (existing) existing.remove();
  }

  // Initial render
  grid.dataset.shown = String(PAGE_SIZE);
  paginate();

  // -------- search --------
  var searchInput = document.getElementById('blog-search-input');
  if (!searchInput) return;

  var fuse = null;
  var index = null;
  var loaded = false;

  function loadIndex() {
    if (loaded) return Promise.resolve();
    return fetch(SEARCH_INDEX_URL, { credentials: 'omit' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        index = data;
        fuse = new Fuse(data, {
          keys: [
            { name: 'title', weight: 0.5 },
            { name: 'excerpt', weight: 0.25 },
            { name: 'category_name', weight: 0.1 },
            { name: 'tag_names', weight: 0.15 },
          ],
          threshold: 0.35,
          ignoreLocation: true,
          minMatchCharLength: 2,
        });
        loaded = true;
      })
      .catch(function (e) {
        console.error('Search index load failed', e);
      });
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var featured = document.querySelector('.blog-featured');

  // -------- client-side tag pill rendering --------
  // Build the tag-pill row from the data-tags on the visible cards so
  // the locale auto-regen step can never strip it.
  (function buildTagPills() {
    var container = document.querySelector('.blog-tag-filter');
    if (!container) return;
    var categorySlug = container.dataset.category || '';
    var tagFreq = {};
    var tagNames = {};
    // Aggregate from search-index later if available; for now use card tags.
    cards.forEach(function (c) {
      var tags = (c.dataset.tags || '').split(' ').filter(Boolean);
      tags.forEach(function (t) {
        tagFreq[t] = (tagFreq[t] || 0) + 1;
      });
    });
    // Pretty name lookup: fetch from search-index for proper labels with spaces/cases
    loadIndex().then(function () {
      if (Array.isArray(index)) {
        index.forEach(function (p) {
          (p.tags || []).forEach(function (slug, i) {
            if (!(slug in tagNames)) {
              var name = (p.tag_names && p.tag_names[i]) || slug;
              tagNames[slug] = name;
            }
          });
        });
      }
      renderTagPills();
    });
    function renderTagPills() {
      var sorted = Object.keys(tagFreq).sort(function (a, b) {
        return (tagNames[a] || a).toLowerCase().localeCompare((tagNames[b] || b).toLowerCase());
      });
      var html = sorted.map(function (slug) {
        var name = tagNames[slug] || slug;
        var href = categorySlug
          ? '/blog/category/' + categorySlug + '?tag=' + slug
          : '/blog/?tag=' + slug;
        return '<a class="blog-tag-pill" data-tag="' + escapeHtml(slug) +
          '" href="' + escapeHtml(href) + '">#' + escapeHtml(name) + '</a>';
      }).join('');
      container.innerHTML = html;
      // Wire clicks
      container.querySelectorAll('.blog-tag-pill').forEach(function (pill) {
        pill.addEventListener('click', function (e) {
          e.preventDefault();
          var tag = pill.dataset.tag;
          var current = new URLSearchParams(window.location.search).get('tag');
          var next = current === tag ? '' : tag;
          var url = new URL(window.location.href);
          if (next) url.searchParams.set('tag', next);
          else url.searchParams.delete('tag');
          window.history.replaceState(null, '', url.toString());
          if (next) applyTagFilter(next);
          else restorePaginated();
        });
      });
      // Re-apply existing filter (e.g. on deep-link)
      var initialTag = new URLSearchParams(window.location.search).get('tag');
      if (initialTag) {
        container.querySelectorAll('.blog-tag-pill').forEach(function (p) {
          p.classList.toggle('active', p.dataset.tag === initialTag);
        });
      }
    }
  })();

  function renderResults(results) {
    if (featured) featured.style.display = 'none';
    grid.innerHTML = '';
    if (results.length === 0) {
      grid.innerHTML = '<div class="blog-empty"><h2>No matches</h2><p>Try a broader keyword.</p></div>';
      removeLoadMore();
      return;
    }
    var html = results.map(function (r) {
      var p = r.item || r; // Fuse wraps in {item, score}
      var heroHtml = p.hero_image_url
        ? '<div class="blog-card-image"><img alt="' + escapeHtml(p.title) + '" loading="lazy" src="' + escapeHtml(p.hero_image_url) + '"/></div>'
        : '<div class="blog-card-image"></div>';
      return '<a class="blog-card" href="' + escapeHtml(localizeHref(p.url)) + '">' +
        heroHtml +
        '<div class="blog-card-body">' +
        '<div class="blog-category-chip">' + escapeHtml(p.category_name) + '</div>' +
        '<h3 class="blog-card-title">' + escapeHtml(p.title) + '</h3>' +
        '<p class="blog-card-excerpt">' + escapeHtml(p.excerpt) + '</p>' +
        '</div></a>';
    }).join('');
    grid.innerHTML = html;
    removeLoadMore();
  }

  function restorePaginated() {
    if (featured) featured.style.display = '';
    // Rebuild the original card list from the snapshot
    grid.innerHTML = '';
    cards.forEach(function (c) { grid.appendChild(c); });
    grid.dataset.shown = String(PAGE_SIZE);
    paginate();
  }

  function onInput(e) {
    var q = (e.target.value || '').trim();
    if (q.length < 2) {
      restorePaginated();
      return;
    }
    loadIndex().then(function () {
      if (!fuse) return;
      var results = fuse.search(q).slice(0, 50);
      renderResults(results);
    });
  }

  searchInput.addEventListener('input', onInput);

  // -------- ?tag= filter (category pages) --------
  // When the URL carries ?tag=foo, filter the server-rendered cards to
  // those whose data-tags attribute contains the tag slug. No fetch
  // needed; the cards already know their own tag set.
  function applyTagFilter(tagSlug) {
    if (!tagSlug) return;
    var anyMatch = false;
    cards.forEach(function (c) {
      var tags = (c.dataset.tags || '').split(' ').filter(Boolean);
      var match = tags.indexOf(tagSlug) !== -1;
      c.style.display = match ? '' : 'none';
      if (match) anyMatch = true;
    });
    removeLoadMore();
    if (featured) featured.style.display = 'none';
    document.querySelectorAll('.blog-tag-pill').forEach(function (p) {
      p.classList.toggle('active', p.dataset.tag === tagSlug);
    });
    if (!anyMatch) {
      grid.innerHTML = '<div class="blog-empty"><h2>No posts with this tag here</h2><p>Try removing the tag filter.</p></div>';
    }
  }

  // Wire tag pill clicks to do in-place filtering instead of navigating.
  document.querySelectorAll('.blog-tag-pill').forEach(function (pill) {
    pill.addEventListener('click', function (e) {
      e.preventDefault();
      var tag = pill.dataset.tag;
      var current = new URLSearchParams(window.location.search).get('tag');
      var next = current === tag ? '' : tag;
      var url = new URL(window.location.href);
      if (next) url.searchParams.set('tag', next);
      else url.searchParams.delete('tag');
      window.history.replaceState(null, '', url.toString());
      if (next) applyTagFilter(next);
      else restorePaginated();
    });
  });

  // -------- query-string deep links --------
  var params = new URLSearchParams(window.location.search);
  var initialQ = params.get('q');
  var initialTag = params.get('tag');
  if (initialQ) {
    searchInput.value = initialQ;
    onInput({ target: searchInput });
  } else if (initialTag) {
    applyTagFilter(initialTag);
  }
})();
