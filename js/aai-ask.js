/* APIANT.AI ask box (css/aai-ask.css): one GA4 event when the form is submitted.
   The form itself is a plain POST to app.apiant.ai/chat/start and works without this.
   gtag is the queue js/gtag-consent.js defines, so the event is held until consent. */
(function () {
  var forms = document.querySelectorAll('form[data-aai-event]');
  Array.prototype.forEach.call(forms, function (f) {
    f.addEventListener('submit', function () {
      if (typeof window.gtag !== 'function') return;
      var apps = f.querySelector('input[name="apps"]');
      var box = f.querySelector('textarea[name="text"]');
      try {
        window.gtag('event', f.getAttribute('data-aai-event'), {
          vertical: apps ? apps.value : '',
          text_length: box ? box.value.length : 0,
          page_path: location.pathname
        });
      } catch (e) {}
    });
  });
})();
