/**
 * Phone Verification Enhancement
 * - IP geolocation to detect country
 * - Searchable country dropdown with flag + dial code
 * - Auto-prefill country code in phone input
 * - Reorder SMS vs WhatsApp based on US/Canada vs international
 */
(function() {
  'use strict';

  // ===== COUNTRY DATA: [ISO alpha-2, Name, Dial Code] =====
  var C = [
    ['US','United States','+1'],['CA','Canada','+1'],['GB','United Kingdom','+44'],
    ['AU','Australia','+61'],['DE','Germany','+49'],['FR','France','+33'],
    ['IN','India','+91'],['BR','Brazil','+55'],['MX','Mexico','+52'],
    ['JP','Japan','+81'],['KR','South Korea','+82'],['CN','China','+86'],
    ['IT','Italy','+39'],['ES','Spain','+34'],['NL','Netherlands','+31'],
    ['SE','Sweden','+46'],['NO','Norway','+47'],['DK','Denmark','+45'],
    ['FI','Finland','+358'],['CH','Switzerland','+41'],['AT','Austria','+43'],
    ['BE','Belgium','+32'],['PT','Portugal','+351'],['IE','Ireland','+353'],
    ['NZ','New Zealand','+64'],['SG','Singapore','+65'],['HK','Hong Kong','+852'],
    ['TW','Taiwan','+886'],['IL','Israel','+972'],['AE','UAE','+971'],
    ['SA','Saudi Arabia','+966'],['ZA','South Africa','+27'],['NG','Nigeria','+234'],
    ['KE','Kenya','+254'],['GH','Ghana','+233'],['EG','Egypt','+20'],
    ['PH','Philippines','+63'],['TH','Thailand','+66'],['VN','Vietnam','+84'],
    ['MY','Malaysia','+60'],['ID','Indonesia','+62'],['PK','Pakistan','+92'],
    ['BD','Bangladesh','+880'],['LK','Sri Lanka','+94'],['NP','Nepal','+977'],
    ['AR','Argentina','+54'],['CL','Chile','+56'],['CO','Colombia','+57'],
    ['PE','Peru','+51'],['VE','Venezuela','+58'],['EC','Ecuador','+593'],
    ['UY','Uruguay','+598'],['PY','Paraguay','+595'],['BO','Bolivia','+591'],
    ['CR','Costa Rica','+506'],['PA','Panama','+507'],['GT','Guatemala','+502'],
    ['HN','Honduras','+504'],['SV','El Salvador','+503'],['NI','Nicaragua','+505'],
    ['DO','Dominican Republic','+1'],['PR','Puerto Rico','+1'],['JM','Jamaica','+1'],
    ['TT','Trinidad & Tobago','+1'],['CU','Cuba','+53'],['HT','Haiti','+509'],
    ['PL','Poland','+48'],['CZ','Czech Republic','+420'],['SK','Slovakia','+421'],
    ['HU','Hungary','+36'],['RO','Romania','+40'],['BG','Bulgaria','+359'],
    ['HR','Croatia','+385'],['RS','Serbia','+381'],['SI','Slovenia','+386'],
    ['UA','Ukraine','+380'],['RU','Russia','+7'],['BY','Belarus','+375'],
    ['LT','Lithuania','+370'],['LV','Latvia','+371'],['EE','Estonia','+372'],
    ['GR','Greece','+30'],['TR','Turkey','+90'],['CY','Cyprus','+357'],
    ['MT','Malta','+356'],['IS','Iceland','+354'],['LU','Luxembourg','+352'],
    ['LI','Liechtenstein','+423'],['MC','Monaco','+377'],['AD','Andorra','+376'],
    ['QA','Qatar','+974'],['KW','Kuwait','+965'],['BH','Bahrain','+973'],
    ['OM','Oman','+968'],['JO','Jordan','+962'],['LB','Lebanon','+961'],
    ['IQ','Iraq','+964'],['IR','Iran','+98'],['AF','Afghanistan','+93'],
    ['MA','Morocco','+212'],['TN','Tunisia','+216'],['DZ','Algeria','+213'],
    ['LY','Libya','+218'],['SD','Sudan','+249'],['ET','Ethiopia','+251'],
    ['TZ','Tanzania','+255'],['UG','Uganda','+256'],['RW','Rwanda','+250'],
    ['SN','Senegal','+221'],['CI','Ivory Coast','+225'],['CM','Cameroon','+237'],
    ['CD','DR Congo','+243'],['AO','Angola','+244'],['MZ','Mozambique','+258'],
    ['ZW','Zimbabwe','+263'],['BW','Botswana','+267'],['NA','Namibia','+264'],
    ['MU','Mauritius','+230'],['MG','Madagascar','+261'],['MM','Myanmar','+95'],
    ['KH','Cambodia','+855'],['LA','Laos','+856'],['BN','Brunei','+673'],
    ['MN','Mongolia','+976'],['KZ','Kazakhstan','+7'],['UZ','Uzbekistan','+998'],
    ['GE','Georgia','+995'],['AM','Armenia','+374'],['AZ','Azerbaijan','+994'],
    ['FJ','Fiji','+679'],['PG','Papua New Guinea','+675'],['WS','Samoa','+685'],
    ['TO','Tonga','+676'],['GU','Guam','+1'],['VI','US Virgin Islands','+1'],
    ['BS','Bahamas','+1'],['BB','Barbados','+1'],['BZ','Belize','+501'],
    ['GY','Guyana','+592'],['SR','Suriname','+597']
  ];

  // ===== STATE =====
  var geo = { country: 'US', dialCode: '+1', loaded: false };

  // ===== UTILITY =====
  function flag(code) {
    return code.toUpperCase().replace(/./g, function(c) {
      return String.fromCodePoint(0x1F1E6 + c.charCodeAt(0) - 65);
    });
  }

  function findCountry(code) {
    code = (code || 'US').toUpperCase();
    for (var i = 0; i < C.length; i++) {
      if (C[i][0] === code) return C[i];
    }
    return C[0];
  }

  // ===== IP GEOLOCATION =====
  // Use api.country.is which serves proper CORS headers. ipapi.co previously
  // used here does not allow apiant.com origins, which produced console errors
  // on every page that loaded this script. Silent fallback to US on any error.
  function fetchGeo() {
    fetch('https://api.country.is/', { mode: 'cors' })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(d) {
        if (d && d.country) {
          geo.country = d.country.toUpperCase();
          var match = findCountry(geo.country);
          geo.dialCode = match ? match[2] : '+1';
          geo.loaded = true;
          selectCountry(geo.country, true);
        } else {
          selectCountry('US', true);
        }
      })
      .catch(function() {
        selectCountry('US', true);
      });
  }

  // ===== INJECT STYLES =====
  function injectStyles() {
    var css = [
      '.cq-phone-wrapper{display:flex;gap:0;align-items:stretch;margin-top:4px;}',
      '.cq-country-btn{display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);border-right:none;border-radius:8px 0 0 8px;padding:0 12px;cursor:pointer;white-space:nowrap;font-family:"DM Sans",sans-serif;font-size:14px;color:#f7f8f8;min-width:95px;position:relative;transition:background 0.15s;}',
      '.cq-country-btn:hover{background:rgba(255,255,255,0.07);}',
      '.cq-country-btn .cq-flag{font-size:18px;line-height:1;}',
      '.cq-country-btn .cq-dial{color:rgba(255,255,255,0.6);font-size:13px;}',
      '.cq-country-btn .cq-chev{width:10px;height:10px;color:rgba(255,255,255,0.3);transition:transform 0.2s;flex-shrink:0;}',
      '.cq-country-btn.open .cq-chev{transform:rotate(180deg);}',
      '.cq-phone-wrapper input[type="tel"]{border-radius:0 8px 8px 0!important;flex:1;min-width:0;}',
      '.cq-country-dd{position:absolute;top:calc(100% + 4px);left:0;width:300px;max-height:320px;background:#1a1a1a;border:1px solid rgba(255,255,255,0.15);border-radius:10px;overflow:hidden;z-index:9999;display:none;flex-direction:column;box-shadow:0 8px 32px rgba(0,0,0,0.6);}',
      '.cq-country-dd.open{display:flex;}',
      '.cq-country-dd input{padding:10px 14px;border:none;border-bottom:1px solid rgba(255,255,255,0.08);background:transparent;color:#f7f8f8;font-size:14px;font-family:"DM Sans",sans-serif;outline:none;width:100%;box-sizing:border-box;}',
      '.cq-country-dd input::placeholder{color:rgba(255,255,255,0.3);}',
      '.cq-country-list{overflow-y:auto;max-height:260px;}',
      '.cq-country-list::-webkit-scrollbar{width:5px;}',
      '.cq-country-list::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:3px;}',
      '.cq-country-item{display:flex;align-items:center;gap:10px;padding:8px 14px;cursor:pointer;font-size:14px;font-family:"DM Sans",sans-serif;color:rgba(255,255,255,0.7);transition:background 0.1s;}',
      '.cq-country-item:hover{background:rgba(255,255,255,0.06);color:#f7f8f8;}',
      '.cq-country-item.selected{background:rgba(26,183,89,0.1);color:#1ab759;}',
      '.cq-country-item .cq-ci-flag{font-size:16px;line-height:1;flex-shrink:0;}',
      '.cq-country-item .cq-ci-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
      '.cq-country-item .cq-ci-dial{color:rgba(255,255,255,0.3);font-size:13px;flex-shrink:0;}',
      '.cq-otp-secondary{opacity:0.45;transition:opacity 0.2s;}',
      '.cq-otp-secondary:hover{opacity:0.75;}',
      '.cq-otp-secondary .apiant-popup-qual-label{font-size:13px!important;}',
      '.cq-otp-primary{transition:opacity 0.2s;}'
    ].join('\n');
    var s = document.createElement('style');
    s.textContent = css;
    document.head.appendChild(s);
  }

  // ===== COUNTRY SELECTOR =====
  function buildSelector() {
    var phoneInput = document.getElementById('cq-phone');
    if (!phoneInput) return;
    var field = phoneInput.closest('.apiant-popup-field');
    if (!field) return;

    // Already built?
    if (document.getElementById('cq-country-btn')) return;

    // Create wrapper
    var wrapper = document.createElement('div');
    wrapper.className = 'cq-phone-wrapper';

    // Country button
    var btn = document.createElement('div');
    btn.className = 'cq-country-btn';
    btn.id = 'cq-country-btn';
    btn.innerHTML =
      '<span class="cq-flag" id="cq-geo-flag">' + flag('US') + '</span>' +
      '<span class="cq-dial" id="cq-geo-dial">+1</span>' +
      '<svg class="cq-chev" viewBox="0 0 20 20" fill="none"><path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    // Dropdown
    var dd = document.createElement('div');
    dd.className = 'cq-country-dd';
    dd.id = 'cq-country-dd';

    var search = document.createElement('input');
    search.type = 'text';
    search.placeholder = 'Search countries...';
    search.id = 'cq-country-search';
    dd.appendChild(search);

    var list = document.createElement('div');
    list.className = 'cq-country-list';
    list.id = 'cq-country-list';
    dd.appendChild(list);
    btn.appendChild(dd);

    // Insert wrapper
    phoneInput.parentNode.insertBefore(wrapper, phoneInput);
    wrapper.appendChild(btn);
    wrapper.appendChild(phoneInput);

    // Update placeholder
    phoneInput.placeholder = '(555) 000-0000';
    phoneInput.maxLength = 20;

    // Populate
    populateList('');

    // Events
    btn.addEventListener('click', function(e) {
      if (e.target === search || e.target.closest('.cq-country-list')) return;
      toggleDropdown();
    });

    search.addEventListener('input', function() {
      populateList(search.value.trim().toLowerCase());
    });

    search.addEventListener('click', function(e) { e.stopPropagation(); });
    search.addEventListener('keydown', function(e) { e.stopPropagation(); });

    document.addEventListener('click', function(e) {
      if (!btn.contains(e.target)) closeDropdown();
    });
  }

  function populateList(filter) {
    var list = document.getElementById('cq-country-list');
    if (!list) return;
    list.innerHTML = '';

    for (var i = 0; i < C.length; i++) {
      var c = C[i];
      if (filter) {
        var match = c[1].toLowerCase().indexOf(filter) !== -1 ||
                    c[0].toLowerCase() === filter ||
                    c[2].indexOf(filter) !== -1;
        if (!match) continue;
      }
      var item = document.createElement('div');
      item.className = 'cq-country-item' + (c[0] === geo.country ? ' selected' : '');
      item.setAttribute('data-code', c[0]);
      item.innerHTML =
        '<span class="cq-ci-flag">' + flag(c[0]) + '</span>' +
        '<span class="cq-ci-name">' + c[1] + '</span>' +
        '<span class="cq-ci-dial">' + c[2] + '</span>';
      (function(code) {
        item.addEventListener('click', function(e) {
          e.stopPropagation();
          selectCountry(code, false);
          closeDropdown();
          var phone = document.getElementById('cq-phone');
          if (phone) phone.focus();
        });
      })(c[0]);
      list.appendChild(item);
    }
  }

  function selectCountry(code, isInitial) {
    var country = findCountry(code);
    geo.country = code;
    geo.dialCode = country[2];

    // Update button display
    var flagEl = document.getElementById('cq-geo-flag');
    var dialEl = document.getElementById('cq-geo-dial');
    if (flagEl) flagEl.textContent = flag(code);
    if (dialEl) dialEl.textContent = country[2];

    // Update selected state in dropdown
    var items = document.querySelectorAll('.cq-country-item');
    for (var i = 0; i < items.length; i++) {
      if (items[i].getAttribute('data-code') === code) {
        items[i].classList.add('selected');
      } else {
        items[i].classList.remove('selected');
      }
    }

    // Reorder OTP methods
    reorderOTP(code);
  }

  function toggleDropdown() {
    var dd = document.getElementById('cq-country-dd');
    var btn = document.getElementById('cq-country-btn');
    if (!dd) return;
    var isOpen = dd.classList.contains('open');
    if (isOpen) {
      closeDropdown();
    } else {
      dd.classList.add('open');
      if (btn) btn.classList.add('open');
      var search = document.getElementById('cq-country-search');
      if (search) {
        search.value = '';
        populateList('');
        setTimeout(function() { search.focus(); }, 50);
      }
    }
  }

  function closeDropdown() {
    var dd = document.getElementById('cq-country-dd');
    var btn = document.getElementById('cq-country-btn');
    if (dd) dd.classList.remove('open');
    if (btn) btn.classList.remove('open');
  }

  // ===== OTP METHOD REORDERING =====
  function reorderOTP(countryCode) {
    var isNA = (countryCode === 'US' || countryCode === 'CA');

    // Find SMS and WhatsApp option elements by their onclick content
    var container = document.querySelector('#cq-verify-send .apiant-popup-qual-options');
    if (!container) return;

    var smsEl = null, waEl = null;
    var options = container.querySelectorAll('.apiant-popup-qual-option');
    for (var i = 0; i < options.length; i++) {
      var oc = options[i].getAttribute('onclick') || '';
      if (oc.indexOf("'sms'") !== -1) smsEl = options[i];
      if (oc.indexOf("'whatsapp'") !== -1) waEl = options[i];
    }
    if (!smsEl || !waEl) return;

    if (isNA) {
      // SMS first (prominent), WhatsApp second (subtle)
      container.insertBefore(smsEl, container.firstChild);
      smsEl.classList.add('cq-otp-primary');
      smsEl.classList.remove('cq-otp-secondary');
      smsEl.style.display = '';
      waEl.classList.add('cq-otp-secondary');
      waEl.classList.remove('cq-otp-primary');
      waEl.style.display = '';
    } else {
      // WhatsApp only, hide SMS for international
      container.insertBefore(waEl, container.firstChild);
      waEl.classList.add('cq-otp-primary');
      waEl.classList.remove('cq-otp-secondary');
      waEl.style.display = '';
      smsEl.style.display = 'none';
    }
  }

  // ===== PREPEND DIAL CODE ON SEND =====
  function prependDialCode() {
    var phone = document.getElementById('cq-phone');
    if (!phone) return;
    var val = phone.value.trim();
    if (val && !val.startsWith('+')) {
      phone.value = geo.dialCode + ' ' + val;
    }
  }

  function patchSendOTP() {
    // Wait for the page's inline script to define cqSendOTP
    if (typeof window.cqSendOTP !== 'function') {
      setTimeout(patchSendOTP, 100);
      return;
    }
    var orig = window.cqSendOTP;
    window.cqSendOTP = function(method) {
      prependDialCode();
      orig(method);
    };
  }

  // ===== RESET HOOK =====
  // When popup resets (re-opens), rebuild country state
  function hookPopupReset() {
    var origOpen = window.openPopup;
    if (typeof origOpen !== 'function') {
      setTimeout(hookPopupReset, 100);
      return;
    }
    // The page already wraps openPopup for CQ reset.
    // We hook into the verify step becoming active to restore phone state.
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(m) {
        if (m.target.id === 'cq-step-verify' && m.target.classList.contains('active')) {
          // Restore phone field to clean state with country code
          var phone = document.getElementById('cq-phone');
          if (phone && !phone.value) {
            phone.placeholder = '(555) 000-0000';
          }
          // Re-apply OTP ordering
          reorderOTP(geo.country);
        }
      });
    });
    var verifyStep = document.getElementById('cq-step-verify');
    if (verifyStep) {
      observer.observe(verifyStep, { attributes: true, attributeFilter: ['class'] });
    }
  }

  // ===== INIT =====
  function init() {
    injectStyles();
    buildSelector();
    fetchGeo();
    patchSendOTP();
    hookPopupReset();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
