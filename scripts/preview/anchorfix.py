OLD = """    var startY = window.scrollY;
    document.fonts.ready.then(function () {
      if (Math.abs(window.scrollY - startY) > 40) return;   // they scrolled, leave it
      target.scrollIntoView();
    });
  })();"""
NEW = """    // A change in scroll position is not evidence the visitor moved: the
    // browser's own smooth scroll to the hash is still running when the fonts
    // arrive. Only real input counts.
    var moved = false;
    ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) {
      window.addEventListener(ev, function () { moved = true; }, { once: true, passive: true });
    });
    document.fonts.ready.then(function () {
      // wait for the initial scroll to settle (position unchanged for ~150ms,
      // capped at 2.5s), then place the target against the settled layout
      var last = -1, still = 0, start = Date.now();
      (function settle() {
        if (moved) return;
        if (window.scrollY === last) still++; else { still = 0; last = window.scrollY; }
        if (still < 9 && Date.now() - start < 2500) return requestAnimationFrame(settle);
        target.scrollIntoView({ behavior: 'instant', block: 'start' });
      })();
    });
  })();"""
