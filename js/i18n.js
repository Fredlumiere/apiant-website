/**
 * APIANT Website Internationalization
 * Language detection, auto-redirect, and language switcher
 */
(function() {
  'use strict';

  var SUPPORTED = ['en','es','fr','zh','hi','ar','bn','pt','ru','ja','de','ko','it','nl','tr','pl','vi','th','id','sv'];
  var NAMES = {
    en:'English', es:'Español', fr:'Français', zh:'\u4e2d\u6587',
    hi:'\u0939\u093f\u0928\u094d\u0926\u0940', ar:'\u0627\u0644\u0639\u0631\u0628\u064a\u0629',
    bn:'\u09ac\u09be\u0982\u09b2\u09be', pt:'Português', ru:'\u0420\u0443\u0441\u0441\u043a\u0438\u0439',
    ja:'\u65e5\u672c\u8a9e', de:'Deutsch', ko:'\ud55c\uad6d\uc5b4',
    it:'Italiano', nl:'Nederlands', tr:'Türkçe', pl:'Polski',
    vi:'Tiếng Việt', th:'\u0e44\u0e17\u0e22', id:'Bahasa Indonesia', sv:'Svenska'
  };
  var CODES = {
    en:'EN', es:'ES', fr:'FR', zh:'ZH', hi:'HI', ar:'AR', bn:'BN',
    pt:'PT', ru:'RU', ja:'JA', de:'DE', ko:'KO', it:'IT', nl:'NL',
    tr:'TR', pl:'PL', vi:'VI', th:'TH', id:'ID', sv:'SV'
  };

  var STORAGE_KEY = 'apiant_lang';
  var REDIRECT_KEY = 'apiant_redirected';

  function getCurrentLang() {
    var m = window.location.pathname.match(/^\/(es|fr|zh|hi|ar|bn|pt|ru|ja|de|ko|it|nl|tr|pl|vi|th|id|sv)\//);
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
    if (getCurrentLang() !== 'en') return;
    if (localStorage.getItem(STORAGE_KEY) === 'en') return;
    if (window.location.search.indexOf('noredirect') !== -1) return;
    if (sessionStorage.getItem(REDIRECT_KEY)) return;

    var preferred = getPreferredLang();
    if (preferred !== 'en') {
      sessionStorage.setItem(REDIRECT_KEY, '1');
      window.location.replace(buildLocalizedUrl(preferred));
    }
  }

  function switchLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang);
    window.location.href = buildLocalizedUrl(lang);
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
    document.addEventListener('DOMContentLoaded', function() { initSwitcher(); autoRedirect(); });
  } else {
    initSwitcher();
    autoRedirect();
  }

  window.APIANT_i18n = { switchLang: switchLang, getCurrentLang: getCurrentLang, SUPPORTED: SUPPORTED, NAMES: NAMES };
})();
