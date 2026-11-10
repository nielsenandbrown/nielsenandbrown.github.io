# Site build notes

Every page (`index.html`, the top-level pages and `services/*.html`) is
hand-written HTML sharing one stylesheet and one script:

- `assets/site/site.css`: shared styles, including the phone-only patterns
  (`.m-swipe`, `.m-collapse`, `.m-chips`, `.m-table`, `.m-hide` / `.m-only`)
- `assets/site/site.js`: campaign attribution, cookie consent + GA4 Consent
  Mode, interaction events, mobile menu, sticky call to action, YouTube videos

The shared head, nav and footer live in `partials/` and are copied into each page
between `<!-- shell:... -->` markers. Edit the partial, then run:

```
python3 scripts/site/sync_shell.py              # every page
python3 scripts/site/sync_shell.py faq.html     # just these
```

Write paths in pages and partials as root paths (`/assets/...`, `/pricing`).
The sync keeps page links as root, extensionless routes (matching the canonical
URLs) and makes file paths relative, so a page opened straight from disk still
gets its styles.

New pages start from `partials/page-template.html`; add them to `sitemap.xml`.

To view locally (extensionless routes work, like GitHub Pages):

```
python3 scripts/site/serve.py
```

then open http://localhost:8000/

Canonical URLs use `https://nielsenandbrown.com` (no www: the www host redirects).
Old homepage anchors (`/#diagnostic-assessment`, `/#faq` and so on) are forwarded
to their new pages by a small script at the end of `index.html`.
