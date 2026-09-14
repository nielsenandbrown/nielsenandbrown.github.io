# Restructure preview build

Generates `preview.html` and the eight new routes from `test.html`, per
`nb-landing-page-restructure-spec.md`. Run from anywhere, in this order:

```
python3 scripts/preview/build_preview.py
python3 scripts/preview/extract_pdata.py
python3 scripts/preview/build_pages.py
```

At rollout, set `HOME = '/'` in `build_pages.py` before the last step. The
rest of the rollout checklist is in STYLE.md.

To view locally:

```
python3 scripts/preview/serve.py
```

then open http://localhost:8000/preview.html
