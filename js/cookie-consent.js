/**
 * APIANT Cookie Consent Banner
 * Self-hosted, GDPR/CCPA compliant cookie consent management.
 * Controls loading of Google Analytics, Smartlook, HubSpot, and Facebook Pixel.
 */
(function() {
  'use strict';

  var COOKIE_NAME = 'apiant_cc';
  var COOKIE_DAYS = 365;

  var ANALYTICS_COOKIES = ['_ga', '_ga_G902ZQ3PZZ', '_ga_R3WL536TPE', 'SL_C_23361dd035530_SID'];
  var FUNCTIONAL_COOKIES = ['hubspotutk', 'messagesUtk'];
  var ADVERTISING_COOKIES = ['_fbp'];

  // Track which scripts have been loaded this session
  var loaded = { analytics: false, functional: false, advertising: false };

  function getConsent() {
    var match = document.cookie.match(new RegExp('(?:^|;\\s*)' + COOKIE_NAME + '=([^;]*)'));
    var raw = match ? match[1] : null;
    var fromCookie = !!raw;
    if (!raw) {
      // Cookie gone but the choice may survive in localStorage: see setConsent.
      try { raw = localStorage.getItem(COOKIE_NAME); } catch (e) { raw = null; }
    }
    if (!raw) return null;
    var parsed;
    try { parsed = JSON.parse(decodeURIComponent(raw)); } catch (e) { return null; }
    // Recovered from the mirror: rewrite the cookie so the rest of the code, and any
    // server-side reader, sees it as normal.
    if (!fromCookie && parsed) { setConsent(parsed); }
    return parsed;
  }

  function setConsent(obj) {
    obj.essential = true;
    obj.ts = Date.now();
    var val = encodeURIComponent(JSON.stringify(obj));
    var d = new Date();
    d.setTime(d.getTime() + COOKIE_DAYS * 86400000);
    // Secure matters on Safari, which is stricter about SameSite cookies without it.
    var secure = location.protocol === 'https:' ? ';Secure' : '';
    document.cookie = COOKIE_NAME + '=' + val + ';expires=' + d.toUTCString() +
      ';path=/;SameSite=Lax' + secure;
    // Mirror to localStorage. Safari's tracking prevention caps a JS-set cookie at
    // seven days, so on iPhone the banner returns weekly even though we asked for a
    // year. The mirror gives getConsent a second place to look. Wrapped because
    // localStorage throws, not returns null, in some privacy modes.
    try { localStorage.setItem(COOKIE_NAME, val); } catch (e) {}
  }

  function deleteCookie(name) {
    var domains = ['.apiant.com', 'apiant.com', location.hostname];
    domains.forEach(function(d) {
      document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=' + d;
    });
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
  }

  function deleteCookies(list) {
    list.forEach(function(name) { deleteCookie(name); });
  }

  // --- Script loaders ---

  function loadGA() {
    if (loaded.analytics) return;
    loaded.analytics = true;
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        analytics_storage: 'granted',
        ad_storage: 'granted',
        ad_user_data: 'granted',
        ad_personalization: 'granted',
        functionality_storage: 'granted',
        personalization_storage: 'granted'
      });
    }
  }

  function denyGA() {
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied'
      });
    }
  }

  function loadSmartlook() {
    if (window.smartlook) return;
    window.smartlook = function() { window.smartlook.api.push(arguments); };
    window.smartlook.api = [];
    var s = document.createElement('script');
    s.async = true;
    s.type = 'text/javascript';
    s.charset = 'utf-8';
    s.src = 'https://rec.smartlook.com/recorder.js';
    document.head.appendChild(s);
    window.smartlook('init', '61b74e67b734857ecfff330d0bf2543efa3e601e');
    window.smartlook('record', { forms: true, numbers: true, emails: false, ips: true });
  }

  function loadHubSpot() {
    if (loaded.functional) return;
    loaded.functional = true;
    // Tracking only: keep the conversations chat widget from loading on any page.
    window.hsConversationsSettings = window.hsConversationsSettings || {};
    window.hsConversationsSettings.loadImmediately = false;
    var s = document.createElement('script');
    s.async = true;
    s.defer = true;
    s.id = 'hs-script-loader';
    s.src = 'https://js.hs-scripts.com/5004658.js';
    s.type = 'text/javascript';
    document.body.appendChild(s);
  }

  function loadFBPixel() {
    if (loaded.advertising || window.fbq) return;
    loaded.advertising = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
  }

  // --- Apply consent ---

  function applyConsent(consent) {
    if (!consent) return;

    if (consent.analytics) {
      loadGA();
      loadSmartlook();
    } else {
      denyGA();
      deleteCookies(ANALYTICS_COOKIES);
    }

    if (consent.functional) {
      loadHubSpot();
    } else {
      deleteCookies(FUNCTIONAL_COOKIES);
    }

    if (consent.advertising) {
      loadFBPixel();
    } else {
      deleteCookies(ADVERTISING_COOKIES);
    }
  }

  // --- Banner UI ---

  function createBanner() {
    // Overlay
    var overlay = document.createElement('div');
    overlay.className = 'cc-overlay cc-visible';
    overlay.addEventListener('click', function() { /* don't close on overlay click */ });

    // Banner
    var banner = document.createElement('div');
    banner.className = 'cc-banner cc-visible';
    banner.innerHTML =
      '<div class="cc-inner">' +
        '<div class="cc-text">' +
          '<p>Essential cookies keep the site working. With your consent we also use analytics, functional and advertising cookies. See our <a href="/cookie-policy.html">Cookie Policy</a> for details.</p>' +
          '<div class="cc-prefs" id="cc-prefs">' +
            '<div class="cc-cats">' +
              ccCat('essential', 'Essential', 'Login sessions and core site functionality. Always on.', true, true) +
              ccCat('analytics', 'Analytics', 'Google Analytics and Smartlook help us understand how you use the site.', false, false) +
              ccCat('functional', 'Functional', 'HubSpot powers visitor identification and form interactions.', false, false) +
              ccCat('advertising', 'Advertising', 'Facebook Pixel measures ad campaign effectiveness.', false, false) +
            '</div>' +
            '<button class="cc-btn cc-btn-save" id="cc-save">Save Preferences</button>' +
          '</div>' +
        '</div>' +
        '<div class="cc-buttons">' +
          '<button class="cc-btn cc-btn-prefs" id="cc-prefs-btn">Preferences</button>' +
          '<button class="cc-btn cc-btn-reject" id="cc-reject">Reject All</button>' +
          '<button class="cc-btn cc-btn-accept" id="cc-accept">Accept All</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);
    document.body.appendChild(banner);

    // Event handlers
    document.getElementById('cc-accept').addEventListener('click', function() {
      var c = { essential: true, analytics: true, functional: true, advertising: true };
      setConsent(c);
      applyConsent(c);
      hideBanner(banner, overlay);
    });

    document.getElementById('cc-reject').addEventListener('click', function() {
      var c = { essential: true, analytics: false, functional: false, advertising: false };
      setConsent(c);
      applyConsent(c);
      hideBanner(banner, overlay);
    });

    document.getElementById('cc-prefs-btn').addEventListener('click', function() {
      var prefs = document.getElementById('cc-prefs');
      prefs.classList.toggle('cc-open');
      this.textContent = prefs.classList.contains('cc-open') ? 'Hide Preferences' : 'Preferences';
    });

    document.getElementById('cc-save').addEventListener('click', function() {
      var c = {
        essential: true,
        analytics: !!document.getElementById('cc-analytics').checked,
        functional: !!document.getElementById('cc-functional').checked,
        advertising: !!document.getElementById('cc-advertising').checked
      };
      setConsent(c);
      applyConsent(c);
      hideBanner(banner, overlay);
    });

    return { banner: banner, overlay: overlay };
  }

  function ccCat(id, name, desc, checked, disabled) {
    return '<div class="cc-cat">' +
      '<div class="cc-cat-info"><div class="cc-cat-name">' + name + '</div><div class="cc-cat-desc">' + desc + '</div></div>' +
      '<label class="cc-toggle"><input type="checkbox" id="cc-' + id + '"' +
      (checked ? ' checked' : '') + (disabled ? ' disabled' : '') +
      '><span class="cc-toggle-track"><span class="cc-toggle-knob"></span></span></label>' +
    '</div>';
  }

  function hideBanner(banner, overlay) {
    banner.classList.remove('cc-visible');
    overlay.classList.remove('cc-visible');
    setTimeout(function() {
      if (banner.parentNode) banner.parentNode.removeChild(banner);
      if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
    }, 300);
  }

  // --- Public API ---

  var currentBanner = null;

  window.ccShowBanner = function() {
    // Remove existing banner if any
    var existing = document.querySelector('.cc-banner');
    if (existing) existing.parentNode.removeChild(existing);
    var existingOverlay = document.querySelector('.cc-overlay');
    if (existingOverlay) existingOverlay.parentNode.removeChild(existingOverlay);

    var ui = createBanner();
    currentBanner = ui;

    // Restore current preferences in toggles
    var consent = getConsent();
    if (consent) {
      var ids = ['analytics', 'functional', 'advertising'];
      ids.forEach(function(id) {
        var el = document.getElementById('cc-' + id);
        if (el) el.checked = !!consent[id];
      });
      // Open prefs panel when reopening
      document.getElementById('cc-prefs').classList.add('cc-open');
      document.getElementById('cc-prefs-btn').textContent = 'Hide Preferences';
    }
  };

  // --- Init ---

  function init() {
    var consent = getConsent();
    if (consent) {
      // Returning visitor: apply saved consent (loads scripts or deletes cookies)
      applyConsent(consent);
    } else {
      // First visit: show banner
      createBanner();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
