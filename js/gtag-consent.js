/**
 * APIANT Google Tag + Consent Mode v2 bootstrap.
 * Must load in <head> BEFORE cookie-consent.js so consent defaults are set
 * prior to any measurement. Google receives cookieless modeled pings until
 * the visitor grants consent via the banner; cookie-consent.js then calls
 * gtag('consent','update',...) to promote to full tracking.
 */
(function () {
  'use strict';

  var GA_ID = 'G-G902ZQ3PZZ';

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'denied',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });

  gtag('set', 'url_passthrough', true);
  gtag('set', 'ads_data_redaction', true);

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  gtag('js', new Date());
  gtag('config', GA_ID, { anonymize_ip: true });
})();
