/* CalendarConnect auto-load booking widget — v3.2
 *
 * Drop-in replacement for the v3.1 apiant_form.js button embed. On page load it
 * POSTs to the event's Web Service automation, which syncs each host's Mindbody
 * availability into Calendly and returns that event's booking URL. The Calendly
 * inline embed is then rendered, so a visitor only ever sees genuinely bookable
 * slots without clicking anything.
 *
 * Page snippet:
 *
 *   <div data-calendarconnect-event
 *        data-endpoint="https://dev.apiant.com/automation_webservice/_<automation-uuid>"></div>
 *   <script src="calendarconnect-widget.js" defer></script>
 *
 * Attributes on the mount element:
 *   data-endpoint        (required) the event automation's Web Service URL
 *   data-show-details    "true" shows Calendly's own event description panel
 *                        inside the embed; "false" (default) lets the host page
 *                        carry the details and keeps the widget scrollbar-free
 *   data-height          explicit embed height; defaults to 1000px with the
 *                        Calendly details panel, 760px without it
 *   data-refresh         "false" hides the Refresh times button (default shown)
 *   data-cache-minutes   reuse the previous booking URL for N minutes within the
 *                        same tab instead of re-syncing. Default 0 = every load
 *                        runs a live sync. NOTE: each live sync is ~1 billable
 *                        Mindbody call per host on the event.
 *
 * COST: with data-cache-minutes="0" every page view spends MBO calls, including
 * bots and idle refreshes. Set a cache window before using this on a page with
 * real traffic.
 */
(function () {
  "use strict";

  var CALENDLY_JS = "https://assets.calendly.com/assets/external/widget.js";
  var calendlyLoading = false;

  function injectStyles() {
    if (document.getElementById("cc_widget_styles")) { return; }
    var css = document.createElement("style");
    css.id = "cc_widget_styles";
    css.textContent = [
      ".cc-widget{position:relative}",
      ".cc-toolbar{display:flex;justify-content:flex-end;align-items:center;margin-bottom:10px;min-height:32px}",
      ".cc-stamp{font-size:12px;color:#5b6b7b;margin-right:auto}",
      ".cc-refresh{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:7px 14px;font-size:13px;",
      "font-weight:600;color:#0b1f33;cursor:pointer;display:inline-flex;align-items:center;gap:7px}",
      ".cc-refresh:hover{border-color:#ff5a1f;color:#ff5a1f}",
      ".cc-refresh:disabled{opacity:.5;cursor:default}",
      ".cc-loading{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;color:#5b6b7b}",
      ".cc-spinner{width:44px;height:44px;border:4px solid #e2e8f0;border-top-color:#ff5a1f;border-radius:50%;",
      "animation:ccspin .9s linear infinite;margin-bottom:18px}",
      "@keyframes ccspin{to{transform:rotate(360deg)}}",
      ".cc-loading .cc-msg{font-size:15px;font-weight:600;color:#1f2933}",
      ".cc-loading .cc-sub{font-size:13px;margin-top:6px}",
      ".cc-error{padding:40px 20px;text-align:center;color:#5b6b7b}",
      ".cc-error strong{display:block;color:#1f2933;margin-bottom:8px}"
    ].join("");
    document.head.appendChild(css);
  }

  function loadCalendlyScript(onReady) {
    if (window.Calendly) { onReady(); return; }
    if (calendlyLoading) {
      var wait = setInterval(function () {
        if (window.Calendly) { clearInterval(wait); onReady(); }
      }, 60);
      return;
    }
    calendlyLoading = true;
    var s = document.createElement("script");
    s.src = CALENDLY_JS;
    s.async = true;
    s.onload = onReady;
    document.head.appendChild(s);
  }

  function mount(el) {
    var endpoint = el.getAttribute("data-endpoint");
    if (!endpoint) { return; }   // misconfigured mount: stay silent, leave the page intact

    var showDetails  = el.getAttribute("data-show-details") === "true";
    var height       = el.getAttribute("data-height") || (showDetails ? "1000px" : "760px");
    var wantRefresh  = el.getAttribute("data-refresh") !== "false";
    var cacheMinutes = parseFloat(el.getAttribute("data-cache-minutes") || "0") || 0;
    var cacheKey     = "cc_widget:" + endpoint;

    el.className = el.className ? el.className + " cc-widget" : "cc-widget";
    el.innerHTML =
      '<div class="cc-toolbar"><span class="cc-stamp"></span>' +
      (wantRefresh ? '<button class="cc-refresh" type="button" title="Re-check live availability">&#x21bb; Refresh times</button>' : "") +
      "</div><div class=\"cc-body\"></div>";

    var body    = el.querySelector(".cc-body");
    var stamp   = el.querySelector(".cc-stamp");
    var refresh = el.querySelector(".cc-refresh");

    function showLoading() {
      body.innerHTML =
        '<div class="cc-loading"><div class="cc-spinner"></div>' +
        '<div class="cc-msg">Checking live availability…</div>' +
        '<div class="cc-sub">Pulling real-time openings from the studio calendar</div></div>';
    }

    function showError() {
      body.innerHTML =
        '<div class="cc-error"><strong>We couldn’t load live times.</strong>' +
        "Please try Refresh, or check back in a moment.</div>";
    }

    function embed(url, syncedAt) {
      var params = "hide_gdpr_banner=1" + (showDetails ? "" : "&hide_event_type_details=1");
      var full = url + (url.indexOf("?") > -1 ? "&" : "?") + params;

      // Create the holder only AFTER Calendly's widget.js is present, then init it
      // ourselves. Ordering matters: widget.js auto-initializes every
      // ".calendly-inline-widget[data-url]" element it finds, but only during its
      // own one-time scan at script-load. The previous version created the holder
      // first (with class AND data-url) and then also called initInlineWidget, so
      // on a cold load the scan and our call each built an iframe, giving two
      // stacked embeds in one holder. Building the holder inside this callback means the
      // scan has already run and can never see it, so exactly one embed is created,
      // on first load and on every Refresh. data-url is omitted for the same
      // reason; initInlineWidget receives the URL directly.
      loadCalendlyScript(function () {
        body.innerHTML = "";
        var holder = document.createElement("div");
        holder.className = "calendly-inline-widget";
        holder.style.minWidth = "320px";
        holder.style.height = height;
        body.appendChild(holder);

        if (window.Calendly && window.Calendly.initInlineWidget) {
          window.Calendly.initInlineWidget({ url: full, parentElement: holder });
        }

        stamp.textContent = "Times updated " + new Date(syncedAt).toLocaleTimeString();
      });
    }

    function readCache() {
      if (!cacheMinutes) { return null; }
      try {
        var raw = window.sessionStorage.getItem(cacheKey);
        if (!raw) { return null; }
        var hit = JSON.parse(raw);
        if (Date.now() - hit.at > cacheMinutes * 60000) { return null; }
        return hit;
      } catch (e) { return null; }
    }

    function writeCache(url, at) {
      if (!cacheMinutes) { return; }
      try {
        window.sessionStorage.setItem(cacheKey, JSON.stringify({ url: url, at: at }));
      } catch (e) { /* private mode / quota — just skip caching */ }
    }

    function load(force) {
      if (!force) {
        var hit = readCache();
        if (hit) { embed(hit.url, hit.at); return; }
      }
      if (refresh) { refresh.disabled = true; }
      showLoading();

      // No Content-Type header keeps this a "simple" CORS request, so the browser
      // skips the preflight the platform's OPTIONS response does not answer.
      // cb defeats any intermediary caching of the endpoint.
      fetch(endpoint + "?cb=" + Date.now(), { method: "POST", body: "{}" })
        .then(function (r) { return r.text(); })
        .then(function (text) {
          var data = JSON.parse(text);
          if (!data.booking_url) { throw new Error("no booking_url in response"); }
          var at = Date.now();
          writeCache(data.booking_url, at);
          embed(data.booking_url, at);
        })
        .catch(function () { showError(); })
        .then(function () { if (refresh) { refresh.disabled = false; } });
    }

    if (refresh) {
      refresh.addEventListener("click", function () { load(true); });
    }
    load(false);
  }

  function init() {
    var mounts = document.querySelectorAll("[data-calendarconnect-event]");
    if (!mounts.length) { return; }
    injectStyles();
    for (var i = 0; i < mounts.length; i++) { mount(mounts[i]); }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
