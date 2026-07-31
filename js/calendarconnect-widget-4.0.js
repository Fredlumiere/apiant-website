/* CalendarConnect auto-load booking widget — v4.0 (localisable build)
 *
 * Same behaviour as test/apiant-gym-demo/calendarconnect-widget.js: on page load
 * it POSTs to the event's Web Service automation, which syncs each host's
 * Mindbody availability into Calendly and returns that event's booking URL, then
 * renders Calendly's inline embed. No button, no stale form instance id.
 *
 * This build adds label attributes so the visible strings can be set per page.
 * Defaults are English; the Optiforme demo pages set French.
 *
 * Page snippet:
 *
 *   <div data-calendarconnect-event
 *        data-endpoint="https://apiant.com/automation_webservice/_<automation-uuid>"></div>
 *   <script src="calendarconnect-widget.js" defer></script>
 *
 * Behaviour attributes:
 *   data-endpoint        (required) the event automation's Web Service URL
 *   data-show-details    "true" shows Calendly's own event description panel
 *   data-height          embed height; defaults 1000px with details, 760px without
 *   data-refresh         "false" hides the refresh button
 *   data-cache-minutes   reuse the last result for N minutes in this tab. Default 0
 *                        = every load runs a live sync (~1 billable Mindbody call
 *                        per host on the event). Set non-zero on customer sites.
 *
 * Label attributes (all optional):
 *   data-label-loading, data-label-loading-sub, data-label-refresh,
 *   data-label-updated, data-label-error-title, data-label-error-body
 */
(function () {
  "use strict";

  var CALENDLY_JS = "https://assets.calendly.com/assets/external/widget.js";
  var calendlyLoading = false;

  var DEFAULT_LABELS = {
    loading:    "Checking live availability…",
    loadingSub: "Pulling real-time openings from the studio calendar",
    refresh:    "Refresh times",
    updated:    "Times updated",
    errorTitle: "We couldn’t load live times.",
    errorBody:  "Please try again, or check back in a moment."
  };

  function injectStyles() {
    if (document.getElementById("cc_widget_styles")) { return; }
    var css = document.createElement("style");
    css.id = "cc_widget_styles";
    css.textContent = [
      ".cc-widget{position:relative}",
      ".cc-toolbar{display:flex;justify-content:flex-end;align-items:center;margin-bottom:10px;min-height:32px}",
      ".cc-stamp{font-size:12px;color:#61676f;margin-right:auto}",
      ".cc-refresh{background:#fff;border:1px solid #e6e9ed;border-radius:8px;padding:7px 14px;font-size:13px;",
      "font-weight:600;color:#16181c;cursor:pointer;display:inline-flex;align-items:center;gap:7px}",
      ".cc-refresh:hover{border-color:#8cc63f;color:#6fa32c}",
      ".cc-refresh:disabled{opacity:.5;cursor:default}",
      ".cc-loading{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;color:#61676f}",
      ".cc-spinner{width:44px;height:44px;border:4px solid #e6e9ed;border-top-color:#8cc63f;border-radius:50%;",
      "animation:ccspin .9s linear infinite;margin-bottom:18px}",
      "@keyframes ccspin{to{transform:rotate(360deg)}}",
      ".cc-loading .cc-msg{font-size:15px;font-weight:600;color:#16181c;text-align:center}",
      ".cc-loading .cc-sub{font-size:13px;margin-top:6px;text-align:center}",
      ".cc-error{padding:40px 20px;text-align:center;color:#61676f}",
      ".cc-error strong{display:block;color:#16181c;margin-bottom:8px}"
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

    function label(attr, fallback) {
      var v = el.getAttribute("data-label-" + attr);
      return (v === null || v === "") ? fallback : v;
    }
    var L = {
      loading:    label("loading",     DEFAULT_LABELS.loading),
      loadingSub: label("loading-sub", DEFAULT_LABELS.loadingSub),
      refresh:    label("refresh",     DEFAULT_LABELS.refresh),
      updated:    label("updated",     DEFAULT_LABELS.updated),
      errorTitle: label("error-title", DEFAULT_LABELS.errorTitle),
      errorBody:  label("error-body",  DEFAULT_LABELS.errorBody)
    };

    var showDetails  = el.getAttribute("data-show-details") === "true";
    var height       = el.getAttribute("data-height") || (showDetails ? "1000px" : "760px");
    var wantRefresh  = el.getAttribute("data-refresh") !== "false";
    var cacheMinutes = parseFloat(el.getAttribute("data-cache-minutes") || "0") || 0;
    var cacheKey     = "cc_widget:" + endpoint;

    function esc(s) {
      return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    el.className = el.className ? el.className + " cc-widget" : "cc-widget";
    el.innerHTML =
      '<div class="cc-toolbar"><span class="cc-stamp"></span>' +
      (wantRefresh
        ? '<button class="cc-refresh" type="button">&#x21bb; ' + esc(L.refresh) + "</button>"
        : "") +
      '</div><div class="cc-body"></div>';

    var body    = el.querySelector(".cc-body");
    var stamp   = el.querySelector(".cc-stamp");
    var refresh = el.querySelector(".cc-refresh");

    function showLoading() {
      body.innerHTML =
        '<div class="cc-loading"><div class="cc-spinner"></div>' +
        '<div class="cc-msg">' + esc(L.loading) + "</div>" +
        '<div class="cc-sub">' + esc(L.loadingSub) + "</div></div>";
    }

    function showError() {
      body.innerHTML =
        '<div class="cc-error"><strong>' + esc(L.errorTitle) + "</strong>" +
        esc(L.errorBody) + "</div>";
    }

    function embed(url, syncedAt) {
      var params = "hide_gdpr_banner=1" + (showDetails ? "" : "&hide_event_type_details=1");
      var full = url + (url.indexOf("?") > -1 ? "&" : "?") + params;

      // Holder is created only AFTER widget.js is present, and carries no
      // data-url: widget.js auto-initialises ".calendly-inline-widget[data-url]"
      // during a single scan at its own load, so building it here — and passing
      // the URL to initInlineWidget directly — guarantees exactly one embed.
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
        stamp.textContent = L.updated + " " + new Date(syncedAt).toLocaleTimeString();
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
      } catch (e) { /* private mode / quota — skip caching */ }
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
