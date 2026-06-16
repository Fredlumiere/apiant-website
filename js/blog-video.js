/**
 * APIANT Blog: custom video player.
 *
 * Upgrades every `.blog-video` embed (a YouTube iframe in the post body)
 * into a branded poster with a hi-tech animated placeholder. The real
 * YouTube iframe is NOT loaded until the visitor clicks play (perf +
 * privacy), at which point the video opens in a fullscreen overlay and
 * closes on Escape, the close button, or when the video ends.
 *
 * Ported from the lumieremedia VideoPlayer (React) to vanilla JS for the
 * static blog, with an APIANT look (dark + green, node-network animation).
 */
(function () {
  var REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ACCENT = '#1ab759';

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ---- hi-tech node-network animation drawn on the poster canvas ----
  function startFx(canvas) {
    if (!canvas || REDUCED) return null;
    var ctx = canvas.getContext('2d');
    var nodes = [];
    var raf = null, running = false, w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);

    function resize() {
      var r = canvas.getBoundingClientRect();
      w = r.width; h = r.height;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.max(14, Math.min(40, Math.round(w / 26)));
      nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
        });
      }
    }

    function frame() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;
      }
      // links
      for (var a = 0; a < nodes.length; a++) {
        for (var b = a + 1; b < nodes.length; b++) {
          var dx = nodes[a].x - nodes[b].x, dy = nodes[a].y - nodes[b].y;
          var d = Math.sqrt(dx * dx + dy * dy);
          if (d < 110) {
            ctx.strokeStyle = 'rgba(26,183,89,' + (0.18 * (1 - d / 110)).toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(nodes[a].x, nodes[a].y);
            ctx.lineTo(nodes[b].x, nodes[b].y);
            ctx.stroke();
          }
        }
      }
      // nodes
      ctx.fillStyle = 'rgba(26,183,89,0.55)';
      for (var k = 0; k < nodes.length; k++) {
        ctx.beginPath();
        ctx.arc(nodes[k].x, nodes[k].y, 1.6, 0, Math.PI * 2);
        ctx.fill();
      }
      raf = requestAnimationFrame(frame);
    }

    function play() { if (!running) { running = true; frame(); } }
    function pause() { running = false; if (raf) cancelAnimationFrame(raf); }

    resize();
    window.addEventListener('resize', function () { resize(); });
    // Only animate while the poster is on screen.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { e.isIntersecting ? play() : pause(); });
      }, { threshold: 0.1 }).observe(canvas);
    } else { play(); }
    return { play: play, pause: pause };
  }

  // ---- fullscreen playback overlay ----
  function openFullscreen(videoId, title) {
    var wrapper = document.createElement('div');
    wrapper.className = 'apiant-video-fs';

    var iframe = document.createElement('iframe');
    iframe.id = 'apiant-video-iframe';
    iframe.title = title;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    iframe.src = 'https://www.youtube.com/embed/' + videoId +
      '?autoplay=1&rel=0&modestbranding=1&controls=1&iv_load_policy=3&color=white&enablejsapi=1&origin=' +
      encodeURIComponent(window.location.origin);
    wrapper.appendChild(iframe);
    document.body.appendChild(wrapper);
    document.body.style.overflow = 'hidden';

    function cleanup() {
      document.body.style.overflow = '';
      if (document.fullscreenElement) {
        document.exitFullscreen().then(function () { wrapper.remove(); }).catch(function () { wrapper.remove(); });
      } else { wrapper.remove(); }
      document.removeEventListener('fullscreenchange', onFsChange);
      document.removeEventListener('webkitfullscreenchange', onFsChange);
      document.removeEventListener('keydown', onKey);
      window.removeEventListener('message', onMessage);
    }
    function onFsChange() { if (!document.fullscreenElement && !document.webkitFullscreenElement) cleanup(); }
    function onKey(e) { if (e.key === 'Escape') cleanup(); }
    function onMessage(e) {
      if (e.origin.indexOf('youtube') === -1) return;
      try {
        var d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data;
        if (d && d.event === 'onStateChange' && d.info === 0) cleanup(); // ended
      } catch (err) { /* not a JSON message */ }
    }

    iframe.addEventListener('load', function () {
      try {
        iframe.contentWindow.postMessage(
          JSON.stringify({ event: 'listening', id: 'apiant-video-iframe' }),
          'https://www.youtube.com'
        );
      } catch (err) { /* ignore */ }
    });

    document.addEventListener('fullscreenchange', onFsChange);
    document.addEventListener('webkitfullscreenchange', onFsChange);
    document.addEventListener('keydown', onKey);
    window.addEventListener('message', onMessage);

    var closeBtn = document.createElement('button');
    closeBtn.className = 'apiant-video-fs__close';
    closeBtn.setAttribute('aria-label', 'Close video');
    closeBtn.innerHTML = '&#x2715;';
    closeBtn.onclick = cleanup;
    wrapper.appendChild(closeBtn);

    var fs = wrapper.requestFullscreen || wrapper.webkitRequestFullscreen;
    if (fs) { fs.call(wrapper).catch(function () { /* keep fixed overlay */ }); }
  }

  // ---- enhance each embed ----
  function enhance(box) {
    var iframe = box.querySelector('iframe');
    if (!iframe) return;
    var src = iframe.getAttribute('src') || '';
    var m = src.match(/embed\/([A-Za-z0-9_-]+)/);
    if (!m) return;
    var videoId = m[1];
    var title = iframe.getAttribute('title') || 'Watch the walkthrough';

    box.classList.add('apiant-video');
    box.innerHTML = '';

    var poster = document.createElement('button');
    poster.type = 'button';
    poster.className = 'apiant-video__poster';
    poster.setAttribute('aria-label', 'Play: ' + title);
    poster.innerHTML =
      '<canvas class="apiant-video__fx" aria-hidden="true"></canvas>' +
      '<div class="apiant-video__scrim"></div>' +
      '<div class="apiant-video__title">' + escapeHtml(title) + '</div>' +
      '<div class="apiant-video__center"><span class="apiant-video__play">' +
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7L8 5z"/></svg></span></div>' +
      '<div class="apiant-video__bar">' +
        '<span class="apiant-video__brand">APIANT</span>' +
        '<span class="apiant-video__cta">Watch the walkthrough</span>' +
      '</div>';
    box.appendChild(poster);

    poster.addEventListener('click', function () { openFullscreen(videoId, title); });
    startFx(poster.querySelector('canvas'));
  }

  function init() {
    var boxes = document.querySelectorAll('.blog-video');
    for (var i = 0; i < boxes.length; i++) enhance(boxes[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
