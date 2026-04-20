/* forum-post.js
   Intercepts the "Post to Builder Community" button in cq-step-forum.
   1. Submits the integration-need text to the save-forum-request edge function,
      which persists it and fans out to Discord server-side. No secrets on the client.
   2. Opens the Discord invite link in a new tab.
   3. Persists the draft in sessionStorage so nothing is lost.
*/
(function () {
  'use strict';

  var DISCORD   = 'https://discord.gg/tx5PankREq';
  var DRAFT_KEY = 'cq_forum_draft';

  /* -- helpers -------------------------------------------------- */

  function submitForumRequest(text) {
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
          company_type: window.CQ_COMPANY_TYPE || '',
          turnstile_token: (function(){var w=window.turnstile;if(!w)return '';var t=w.getResponse()||'';try{w.reset()}catch(e){}return t;})()
        })
      });
    } catch (_) { /* silent */ }
  }

  /* -- init ----------------------------------------------------- */

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

      // 1. Persist to DB and fan out to Discord server-side
      submitForumRequest(text);

      // 2. Open Discord invite link
      window.open(DISCORD, '_blank', 'noopener');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
