/* Nielsen & Brown preview site: shared behaviour for every page.
   Campaign attribution, cookie consent with GA4 Consent Mode, interaction
   events and the mobile menu. Ported from the live index.html. */

// ── Campaign attribution ──────────────────────────────────
// Captured first-touch per session so a hop to another page does not lose it.
// sessionStorage only, cleared when the tab closes, used to tell you where an
// enquiry came from. Not analytics, so it is not gated on consent.
window.nbAttribution = (function () {
  var KEYS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','account_id'];
  var STORE = 'nb-attrib';
  var data = null;
  try { var st = sessionStorage.getItem(STORE); if (st) data = JSON.parse(st); } catch (e) {}
  var p = new URLSearchParams(window.location.search), incoming = {}, any = false;
  KEYS.forEach(function (k) { var v = p.get(k); if (v) { incoming[k] = v.slice(0,200); any = true; } });
  if (any && !data) {
    data = incoming;
    try { sessionStorage.setItem(STORE, JSON.stringify(data)); } catch (e) {}
  }
  function d() { return data || {}; }
  return {
    get: d,
    summary:  function () { return d().utm_source ? [d().utm_source, d().utm_medium].filter(Boolean).join(' / ') : 'Direct or organic'; },
    campaign: function () { return [d().utm_campaign, d().utm_term, d().utm_content].filter(Boolean).join(' — ') || 'Not set'; },
    account:  function () { return d().account_id || 'Not set'; },
    appendTo: function (url) {
      var k = Object.keys(d()); if (!k.length) return url;
      return url + (url.indexOf('?') === -1 ? '?' : '&') +
        k.map(function (x) { return x + '=' + encodeURIComponent(d()[x]); }).join('&');
    }
  };
})();

document.querySelectorAll('a[href^="https://score.nielsenandbrown.com"]').forEach(function (el) {
  el.setAttribute('href', window.nbAttribution.appendTo(el.getAttribute('href')));
});

// ── Cookie consent + GA4 Consent Mode ─────────────────────
(function () {
  var banner = document.getElementById('cookie-consent');
  if (!banner) return;
  var KEY = 'nb-consent';
  function grant() {
    if (typeof gtag === 'function') {
      gtag('consent', 'update', { 'analytics_storage': 'granted' });
      gtag('config', 'G-V9Q0XLTP7Q');
    }
  }
  function revoke() {
    if (typeof gtag === 'function') {
      gtag('consent', 'update', { 'analytics_storage': 'denied', 'ad_storage': 'denied' });
    }
  }
  // Cookie, not localStorage: localStorage is per-subdomain, so the score app
  // could not read the decision and would ask a second time.
  function readCookie() {
    var m = document.cookie.match(/(?:^|;\s*)nb-consent=(granted|denied)/);
    return m ? m[1] : null;
  }
  // The domain attribute is only valid on the real host. Setting it anywhere
  // else (localhost, a preview URL) makes the browser reject the cookie
  // silently, so scope it only when we are actually on the live domain.
  function cookieDomain() {
    return /(^|\.)nielsenandbrown\.com$/.test(location.hostname)
      ? ';domain=.nielsenandbrown.com' : '';
  }
  function writeCookie(v) {
    document.cookie = 'nb-consent=' + v + cookieDomain() +
      ';path=/;max-age=31536000;SameSite=Lax' +
      (location.protocol === 'https:' ? ';Secure' : '');
  }
  var stored = readCookie();
  if (!stored) {
    try {
      var legacy = localStorage.getItem(KEY);
      if (legacy === 'granted' || legacy === 'denied') {
        stored = legacy; writeCookie(legacy); localStorage.removeItem(KEY);
      }
    } catch (e) {}
  }
  if (stored === 'granted') { grant(); }
  else if (stored !== 'denied') { banner.classList.add('visible'); }

  document.getElementById('consent-accept').addEventListener('click', function () {
    writeCookie('granted');
    grant(); banner.classList.remove('visible');
  });
  document.getElementById('consent-decline').addEventListener('click', function () {
    writeCookie('denied');
    // Revoke immediately, so analytics stop even if the user had accepted earlier this session.
    revoke(); banner.classList.remove('visible');
  });

  // "Cookie settings" in the footer reopens the banner so the choice can be changed.
  var settings = document.getElementById('cookie-settings-link');
  if (settings) {
    settings.addEventListener('click', function (e) {
      e.preventDefault();
      banner.classList.add('visible');
      document.getElementById('consent-accept').focus();
    });
  }
})();

// ── GA4 interaction events (no-op until consent grants) ───
window.nbTrack = function (name, params) {
  if (typeof gtag === 'function') { gtag('event', name, params || {}); }
};
(function () {
  var track = window.nbTrack;

  // CTA clicks: pass the link's destination (e.g. "contact") so reports show
  // what the user was reaching for, not just the button label.
  document.querySelectorAll('[data-ga]').forEach(function (el) {
    el.addEventListener('click', function () {
      var href = el.getAttribute('href') || '';
      var hash = href.indexOf('#');
      var destination = hash !== -1 ? href.slice(hash + 1) : '';
      track(el.getAttribute('data-ga'), destination ? { destination: destination } : {});
    });
  });

  document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
    el.addEventListener('click', function () { track('email_click'); });
  });
  document.querySelectorAll('a[href*="linkedin.com"]').forEach(function (el) {
    el.addEventListener('click', function () { track('linkedin_click'); });
  });

  // Outbound link tracking, captured by hostname so it is easy to read in GA.
  document.querySelectorAll('a[href^="http"]').forEach(function (el) {
    var href = el.getAttribute('href') || '';
    if (href.indexOf('nielsenandbrown.com') !== -1 && href.indexOf('score.') === -1) return;
    if (href.indexOf('linkedin.com') !== -1) return;
    el.addEventListener('click', function () {
      var hostname = '';
      try { hostname = new URL(href).hostname.replace(/^www\./, ''); } catch (e) {}
      track('outbound_click', { link_url: href, link_domain: hostname });
    });
  });

  var form = document.getElementById('contact-form');
  if (form) {
    var started = false;
    form.addEventListener('focusin', function () {
      if (!started) { started = true; track('form_start'); }
    });
  }

  // Section views: fire once when a major section first comes into view, so we
  // can see how far down the page visitors get. Sections opt in with data-track.
  if ('IntersectionObserver' in window) {
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var id = entry.target.id;
        if (entry.isIntersecting && !seen[id]) {
          seen[id] = true;
          track('section_view', { section_id: id });
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    document.querySelectorAll('[data-track][id]').forEach(function (el) { io.observe(el); });
  }
})();

// ── Mobile menu ───────────────────────────────────────────
(function () {
  var nav = document.querySelector('.nav'), btn = document.getElementById('menu-btn');
  if (!nav || !btn) return;
  function set(open) {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    btn.textContent = open ? 'Close' : 'Menu';
  }
  btn.addEventListener('click', function () { set(!nav.classList.contains('open')); });
  nav.querySelectorAll('.nav-links a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { set(false); btn.focus(); } });
})();

// ── YouTube videos ────────────────────────────────────────
// Any <button data-yt="VIDEO_ID"> shows our own poster image and only loads
// YouTube when pressed, so nothing is sent to YouTube before then. Add the
// class "portrait" to the button for a 9:16 video.
(function () {
  document.querySelectorAll('button[data-yt]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      window.nbTrack('video_play', { video_id: id });
      // YouTube refuses to play embeds that can't say which site they are on
      // (error 153), which is always the case for a page opened from disk.
      if (location.protocol === 'file:') {
        window.open('https://www.youtube.com/watch?v=' + id, '_blank', 'noopener');
        return;
      }
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&playsinline=1&rel=0&origin=' + encodeURIComponent(location.origin);
      f.title = btn.getAttribute('data-title') || 'Video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      f.allowFullscreen = true;
      var box = document.createElement('div');
      box.className = btn.className;
      box.appendChild(f);
      btn.replaceWith(box);
    });
  });
})();
