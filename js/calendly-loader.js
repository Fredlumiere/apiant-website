/*
 * calendly-loader.js
 *
 * Lazy-loads Calendly inline widgets. Pages no longer hardcode scheduling
 * URLs (they were being scraped from page source for spam bookings). Instead
 * they ship a placeholder:
 *
 *   <div class="calendly-lazy" data-calendly-event="crmconnect"
 *        data-calendly-params="hide_event_type_details=1&hide_gdpr_banner=1&a3=Mindbody and HubSpot"
 *        style="min-width:320px;height:100%;"></div>
 *
 * When the placeholder becomes visible (demo popup opened, or scrolled into
 * view), the scheduling URL is fetched from the get-calendly-url edge function
 * and the Calendly widget is injected.
 */
(function () {
  var SUPABASE_URL = 'https://kereljzjgeerrdnssttu.supabase.co';
  var WIDGET_JS = 'https://assets.calendly.com/assets/external/widget.js';
  var widgetScriptPromise = null;

  function loadWidgetScript() {
    if (window.Calendly && window.Calendly.initInlineWidget) {
      return Promise.resolve();
    }
    if (!widgetScriptPromise) {
      widgetScriptPromise = new Promise(function (resolve, reject) {
        var s = document.createElement('script');
        s.src = WIDGET_JS;
        s.async = true;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    return widgetScriptPromise;
  }

  function activate(el) {
    if (el.getAttribute('data-calendly-loaded')) return;
    el.setAttribute('data-calendly-loaded', '1');

    var eventKey = el.getAttribute('data-calendly-event') || 'crmconnect';
    fetch(SUPABASE_URL + '/functions/v1/get-calendly-url?event=' + encodeURIComponent(eventKey))
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (!data || !data.url || !/^https:\/\/calendly\.com\//.test(data.url)) return;
        var params = el.getAttribute('data-calendly-params') || '';
        var url = data.url + (params ? (data.url.indexOf('?') > -1 ? '&' : '?') + params : '');
        return loadWidgetScript().then(function () {
          if (!(window.Calendly && window.Calendly.initInlineWidget)) return;
          window.Calendly.initInlineWidget({ url: url, parentElement: el });
        });
      })
      .catch(function () { /* scheduler simply stays empty; contact paths remain */ });
  }

  function init() {
    var els = document.querySelectorAll('.calendly-lazy');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      for (var i = 0; i < els.length; i++) activate(els[i]);
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          io.unobserve(entry.target);
          activate(entry.target);
        }
      });
    });
    for (var j = 0; j < els.length; j++) io.observe(els[j]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
