/* forum-post.js
   Intercepts the "Post on Community Forum" button in cq-step-forum.
   1. Saves the integration-need text to Supabase (if available).
   2. Opens a pre-filled Discourse new-topic in a new tab.
   3. Persists the draft in sessionStorage so nothing is lost.
*/
(function () {
  'use strict';

  var DISCOURSE   = 'https://forum.apiant.com';
  var CATEGORY_ID = 23;                       // "Connector Wanted"
  var DRAFT_KEY   = 'cq_forum_draft';

  /* ── helpers ──────────────────────────────────────────────── */

  function titleFrom(text) {
    var first = text.split(/[.\n]/)[0].trim();
    if (first.length > 80) first = first.substring(0, 77) + '...';
    return first || 'Integration Request';
  }

  function saveToDB(text) {
    var url = window.CQ_SUPABASE_URL;
    if (!url) return;

    var src = document.querySelector('input[name="Source-Page"]');
    try {
      fetch(url + '/functions/v1/save-forum-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          integration_need: text,
          source_page: src ? src.value : location.pathname,
          domain: window.CQ_VERIFIED_DOMAIN || '',
          company_type: window.CQ_COMPANY_TYPE || ''
        })
      });
    } catch (_) { /* silent */ }
  }

  /* ── init ─────────────────────────────────────────────────── */

  function init() {
    var step = document.getElementById('cq-step-forum');
    if (!step) return;

    var ta  = document.getElementById('cq-integration-need');
    var btn = step.querySelector('.apiant-popup-submit');
    if (!ta || !btn) return;

    // Restore draft
    var saved = sessionStorage.getItem(DRAFT_KEY);
    if (saved && !ta.value) ta.value = saved;

    // Auto-save while typing
    ta.addEventListener('input', function () {
      sessionStorage.setItem(DRAFT_KEY, ta.value);
    });

    // Intercept click
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      var text = ta.value.trim();
      if (!text) { ta.focus(); return; }

      // 1. Persist to DB
      saveToDB(text);

      // 2. Open Discourse with pre-filled topic
      var href = DISCOURSE + '/new-topic?title=' +
        encodeURIComponent(titleFrom(text)) +
        '&body=' + encodeURIComponent(text) +
        '&category_id=' + CATEGORY_ID;

      window.open(href, '_blank', 'noopener');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
