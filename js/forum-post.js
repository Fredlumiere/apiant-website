/* forum-post.js
   Intercepts the "Post to Builder Community" button in cq-step-forum.
   1. Saves the integration-need text to Supabase (if available).
   2. Posts to #connector-wanted via Discord webhook.
   3. Opens the Discord invite link in a new tab.
   4. Persists the draft in sessionStorage so nothing is lost.
*/
(function () {
  'use strict';

  var DISCORD     = 'https://discord.gg/tx5PankREq';
  var WEBHOOK_URL = 'https://discord.com/api/webhooks/1481786224808034478/QAP-n5R0Cvjud5hDQ6mSuxJ2BpkeNzDRZXy18tXb6Kr_rnd01uWEEg2doL9wmzr0hE1o';
  var DRAFT_KEY   = 'cq_forum_draft';

  /* -- helpers -------------------------------------------------- */

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

  function postToDiscord(text) {
    var domain = window.CQ_VERIFIED_DOMAIN || 'unknown';
    var companyType = window.CQ_COMPANY_TYPE || 'unknown';
    var src = document.querySelector('input[name="Source-Page"]');
    var page = src ? src.value : location.pathname;

    var embed = {
      title: 'New Connector Request',
      description: text,
      color: 0x1ab759,
      fields: [
        { name: 'Company Domain', value: domain, inline: true },
        { name: 'Company Type', value: companyType, inline: true },
        { name: 'Source Page', value: page, inline: false }
      ],
      timestamp: new Date().toISOString()
    };

    try {
      fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: 'APIANT Website',
          embeds: [embed]
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

      // 1. Persist to DB
      saveToDB(text);

      // 2. Post to #connector-wanted on Discord
      postToDiscord(text);

      // 3. Open Discord invite link
      window.open(DISCORD, '_blank', 'noopener');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
