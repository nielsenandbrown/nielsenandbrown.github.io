"""Serve the site locally the way GitHub Pages does: /how-we-work -> how-we-work.html."""
import http.server, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + '.html'):
            return p + '.html'
        return p

print(f'Open http://localhost:{PORT}/preview.html   (Ctrl+C to stop)')
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
