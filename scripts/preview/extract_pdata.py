"""Write the engagement product data from preview.html to pdata.json (needs node)."""
import re, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
s = open(ROOT + 'preview.html', encoding='utf8').read()
i = s.index('var P = {'); j = s.index('\n};', i) + 3
arrays = re.findall(r"var (NEXT|ACCEL|CORE|AFTER)\s*=\s*(\[[^\]]*\]);", s)
js = s[i:j] + '\n' + '\n'.join(f'var {a} = {b};' for a, b in arrays) + \
     '\nconsole.log(JSON.stringify({P,NEXT,ACCEL,CORE,AFTER}));'
out = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout
open(os.path.join(HERE, 'pdata.json'), 'w').write(out)
print('pdata.json written')
