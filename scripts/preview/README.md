# Preview site (new branding)

`preview.html` and the `preview-*.html` pages (plus `services/preview-*.html`) are
the new-brand version of the site. They are hand-written HTML sharing one
stylesheet and one script:

- `assets/preview/site.css`: shared styles
- `assets/preview/site.js`: campaign attribution, cookie consent + GA4 Consent
  Mode, interaction events, mobile menu

The shared head, nav and footer live in `partials/` and are copied into each page
between `<!-- shell:... -->` markers. Edit the partial, then run:

```
python3 scripts/preview/sync_shell.py            # every preview page
python3 scripts/preview/sync_shell.py preview-faq.html
```

New pages start from `partials/page-template.html`.

To view locally (extensionless routes work, like GitHub Pages):

```
python3 scripts/preview/serve.py
```

then open http://localhost:8000/preview

Do not run the older `build_preview.py` / `build_pages.py` / `extract_pdata.py`:
they generate the previous restructure from `test.html` and would overwrite
`preview.html`.

## Rollout checklist (copying preview over the live pages)

1. `preview.html` → `index.html`, each `preview-X.html` → `X.html`,
   `services/preview-X.html` → `services/X.html`.
2. Replace preview routes in the partials and in each page's own links:
   `/preview#` → `/#`, `/preview"` → `/"`, `/preview-X` → `/X`,
   `/services/preview-X` → `/services/X`. Pages are written with root paths;
   `sync_shell.py` rewrites them to relative file paths (`preview-faq.html`,
   `../assets/...`) so the pages also work opened straight from disk. Update
   its `relative()` step if you want extensionless links on the live site.
3. In `partials/head.html`, set robots to `index, follow`, then re-run
   `sync_shell.py` on the renamed pages (update its glob first).
4. Canonical and og:url tags already point at the live routes on
   `https://nielsenandbrown.com` (no www: the www host redirects).
5. Add a `sitemap.xml` and `robots.txt`.
