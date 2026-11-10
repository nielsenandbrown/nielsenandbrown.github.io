"""Copy the shared head, nav and footer into every page of the site.

    python3 scripts/site/sync_shell.py              # every page
    python3 scripts/site/sync_shell.py faq.html     # just these

Each page marks where the shared parts go with comment pairs:

    <!-- shell:head -->...<!-- /shell:head -->
    <!-- shell:nav -->...<!-- /shell:nav -->
    <!-- shell:footer -->...<!-- /shell:footer -->

Whatever sits between a pair is replaced with scripts/preview/partials/<name>.html,
so edit the partial and rerun this rather than editing pages one by one.
The nav link for the current page gets aria-current="page".
"""
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PARTIALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partials')

# Every page that carries the shell markers (the template in partials/ is not a page).
pages = [os.path.abspath(a) for a in sys.argv[1:]] or sorted(
    f for f in glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'services', '*.html'))
    if '<!-- shell:head -->' in open(f, encoding='utf8').read())
parts = {n: open(os.path.join(PARTIALS, n + '.html'), encoding='utf8').read().strip() for n in ('head', 'nav', 'footer')}

def relative(doc, depth):
    """Root file paths ("/assets/x.css") become relative ("../assets/x.css") so a
    page opened straight from disk still gets its styles and images. Links to
    pages ("/pricing", "/#contact") stay as root, extensionless routes, matching
    the canonical URLs. Write root paths in pages and partials."""
    up = '../' * depth
    def fix(m):
        attr, path, frag = m.group(1), m.group(2), m.group(3) or ''
        if path == '/' or '.' not in os.path.basename(path):   # a page route, not a file
            return m.group(0)
        return f'{attr}="{up}{path.lstrip("/")}{frag}"'
    return re.sub(r'\b(href|src)="(/(?!/)[^"#?]*)(#[^"]*)?"', fix, doc)


for path in pages:
    doc = open(path, encoding='utf8').read()
    route = '/' + os.path.relpath(path, ROOT)[:-len('.html')]
    if route == '/index':
        route = '/'
    for name, body in parts.items():
        if name == 'nav':
            body = body.replace(f'<a href="{route}">', f'<a href="{route}" aria-current="page">')
        pattern = re.compile(rf'(<!-- shell:{name} -->).*?(<!-- /shell:{name} -->)', re.S)
        if not pattern.search(doc):
            raise SystemExit(f'{os.path.relpath(path, ROOT)}: missing <!-- shell:{name} --> markers')
        doc = pattern.sub(lambda m: m.group(1) + '\n' + body + '\n' + m.group(2), doc)
    doc = relative(doc, os.path.relpath(path, ROOT).count('/'))
    open(path, 'w', encoding='utf8').write(doc)
    print('synced', os.path.relpath(path, ROOT))
