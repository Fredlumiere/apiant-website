/**
 * APIANT Website Internationalization
 * Language detection, auto-redirect, and language switcher
 */
(function() {
  'use strict';

  var SUPPORTED = ['en','es','fr','zh','hi','ar','he','bn','pt','ru','ja','de','ko','it','nl','tr','pl','vi','th','id','sv'];
  var NAMES = {
    en:'English', es:'Español', fr:'Français', zh:'\u4e2d\u6587',
    hi:'\u0939\u093f\u0928\u094d\u0926\u0940', ar:'\u0627\u0644\u0639\u0631\u0628\u064a\u0629',
    he:'\u05e2\u05d1\u05e8\u05d9\u05ea',
    bn:'\u09ac\u09be\u0982\u09b2\u09be', pt:'Português', ru:'\u0420\u0443\u0441\u0441\u043a\u0438\u0439',
    ja:'\u65e5\u672c\u8a9e', de:'Deutsch', ko:'\ud55c\uad6d\uc5b4',
    it:'Italiano', nl:'Nederlands', tr:'Türkçe', pl:'Polski',
    vi:'Tiếng Việt', th:'\u0e44\u0e17\u0e22', id:'Bahasa Indonesia', sv:'Svenska'
  };
  var CODES = {
    en:'EN', es:'ES', fr:'FR', zh:'ZH', hi:'HI', ar:'AR', he:'HE', bn:'BN',
    pt:'PT', ru:'RU', ja:'JA', de:'DE', ko:'KO', it:'IT', nl:'NL',
    tr:'TR', pl:'PL', vi:'VI', th:'TH', id:'ID', sv:'SV'
  };

  var STORAGE_KEY = 'apiant_lang';
  var REDIRECT_KEY = 'apiant_redirected';

  function getCurrentLang() {
    var m = window.location.pathname.match(/^\/(es|fr|zh|hi|ar|he|bn|pt|ru|ja|de|ko|it|nl|tr|pl|vi|th|id|sv)\//);
    return m ? m[1] : 'en';
  }

  function getPreferredLang() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored && SUPPORTED.indexOf(stored) !== -1) return stored;

    var langs = navigator.languages || [navigator.language || 'en'];
    for (var i = 0; i < langs.length; i++) {
      var tag = langs[i].toLowerCase();
      // Exclude Traditional Chinese variants
      if (/^zh-(tw|hk|hant)/.test(tag)) continue;
      var primary = tag.split('-')[0];
      if (SUPPORTED.indexOf(primary) !== -1) return primary;
    }
    return 'en';
  }

  function buildLocalizedUrl(lang) {
    var path = window.location.pathname;
    var current = getCurrentLang();

    // Strip existing lang prefix
    if (current !== 'en') {
      path = path.replace(new RegExp('^/' + current + '/'), '/');
    }

    if (lang === 'en') return path + window.location.search + window.location.hash;
    return '/' + lang + path + window.location.search + window.location.hash;
  }

  function autoRedirect() {
    if (getCurrentLang() !== 'en') {
      // User is on a localized page, remember they chose that language
      sessionStorage.setItem(REDIRECT_KEY, '1');
      return;
    }
    if (localStorage.getItem(STORAGE_KEY)) return;
    if (window.location.search.indexOf('noredirect') !== -1) return;
    if (sessionStorage.getItem(REDIRECT_KEY)) return;
    // Only redirect on the very first page of the session
    if (document.referrer && new URL(document.referrer).hostname === window.location.hostname) {
      // User navigated from another page on this site, do not redirect
      sessionStorage.setItem(REDIRECT_KEY, '1');
      return;
    }

    var preferred = getPreferredLang();
    if (preferred !== 'en') {
      sessionStorage.setItem(REDIRECT_KEY, '1');
      window.location.replace(buildLocalizedUrl(preferred));
    } else {
      sessionStorage.setItem(REDIRECT_KEY, '1');
    }
  }

  function switchLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang);
    window.location.href = buildLocalizedUrl(lang);
  }

  // Paths that are NOT localized (no /{lang}/ copy exists) or must never
  // be rewritten. Matched against the start of a root-relative href.
  var NO_LOCALE = /^\/(editor|admin|api|webhook|oauth|css|js|images|videos|fonts|appResources|sitemap|robots|blog\/feed\.xml|blog\/search-index\.json)\b/;

  /**
   * Site-wide language stickiness: when on a localized page, rewrite
   * internal absolute links (/foo) to carry the current /{lang}/ prefix
   * so navigating between sections (marketing <-> blog, plus the blog
   * nav's absolute links) keeps the visitor in their language.
   *
   * Relative links (for-saas, platform/) already resolve correctly
   * inside /{lang}/ and are left untouched. Already-prefixed links,
   * external links, anchors, mailto/tel, and NO_LOCALE paths are skipped.
   */
  function localizeInternalLinks() {
    var lang = getCurrentLang();
    if (lang === 'en') return;
    var prefix = '/' + lang;
    var alreadyPrefixed = new RegExp('^/(' + SUPPORTED.join('|') + ')(/|$)');
    var anchors = document.querySelectorAll('a[href]');
    for (var i = 0; i < anchors.length; i++) {
      var a = anchors[i];
      var href = a.getAttribute('href');
      // Only same-site root-relative paths ("/something"). Skips
      // external, protocol-relative (//), anchors (#), mailto:, tel:.
      if (!href || href.charAt(0) !== '/' || href.charAt(1) === '/') continue;
      if (alreadyPrefixed.test(href)) continue;
      if (NO_LOCALE.test(href)) continue;
      // Language switchers point at other locales on purpose. Their
      // English option is the unprefixed root path; prefixing it would
      // trap the visitor in the current locale.
      if (a.closest('.blog-lang-switcher-dropdown, .lang-switcher-dropdown')) continue;
      a.setAttribute('href', prefix + href);
    }
  }

  function initSwitcher() {
    var containers = document.querySelectorAll('.lang-switcher-dropdown');
    var current = getCurrentLang();

    containers.forEach(function(dd) {
      var html = '';
      SUPPORTED.forEach(function(code) {
        var cls = code === current ? ' class="lang-option active"' : ' class="lang-option"';
        html += '<a' + cls + ' href="' + buildLocalizedUrl(code) + '" data-lang="' + code + '">' +
                '<span class="lang-option-code">' + CODES[code] + '</span>' +
                '<span class="lang-option-name">' + NAMES[code] + '</span></a>';
      });
      dd.innerHTML = html;

      dd.querySelectorAll('.lang-option').forEach(function(el) {
        el.addEventListener('click', function(e) {
          e.preventDefault();
          switchLang(el.getAttribute('data-lang'));
        });
      });
    });

    // Toggle button
    document.querySelectorAll('.lang-switcher-btn').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var dd = btn.parentElement.querySelector('.lang-switcher-dropdown');
        if (dd) dd.classList.toggle('open');
      });
    });

    // Close on outside click
    document.addEventListener('click', function() {
      document.querySelectorAll('.lang-switcher-dropdown.open').forEach(function(d) {
        d.classList.remove('open');
      });
    });

    // Set current label
    document.querySelectorAll('.lang-switcher-current').forEach(function(el) {
      el.textContent = CODES[current];
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initSwitcher(); localizeInternalLinks(); autoRedirect();
    });
  } else {
    initSwitcher();
    localizeInternalLinks();
    autoRedirect();
  }

  window.APIANT_i18n = { switchLang: switchLang, getCurrentLang: getCurrentLang, SUPPORTED: SUPPORTED, NAMES: NAMES };
})();
