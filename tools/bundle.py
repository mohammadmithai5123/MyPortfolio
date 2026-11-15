"""Builds the fast, cache-friendly production files in assets/dist/ (no third-party tools needed).

    assets/dist/vendor.min.js   gsap + ScrollTrigger + Lenis (self-hosted, same-origin)
    assets/dist/app.min.js      config + i18n + data + main
    assets/dist/style.min.css   fonts.css + style.css

usage:  python tools/bundle.py .
Edit the readable sources in assets/css, assets/js; then run tools/build.py (bundle + pages).
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
P = lambda *a: os.path.join(ROOT, *a)
read = lambda p: open(p, encoding='utf-8').read()


def strip_js(src):
    """Very conservative: only removes whole-line comments, indentation and blank lines."""
    if '`' in src:                       # template literals: leave untouched, safety first
        return src
    src = re.sub(r'^\s*/\*.*?\*/\s*$', '', src, flags=re.S | re.M) if False else src
    out, in_block = [], False
    for line in src.split('\n'):
        t = line.strip()
        if in_block:
            if '*/' in t:
                in_block = False
            continue
        if t.startswith('/*') and not t.startswith('/*!'):
            if '*/' not in t:
                in_block = True
            continue
        if not t or t.startswith('//'):
            continue
        out.append(t)
    return '\n'.join(out)


def min_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    parts = re.split(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', css)   # keep quoted strings untouched
    for i in range(0, len(parts), 2):
        s = parts[i]
        s = re.sub(r'\s+', ' ', s)
        s = re.sub(r'\s*([{};,>])\s*', r'\1', s)
        s = re.sub(r':\s+', ':', s)
        s = s.replace(';}', '}')
        parts[i] = s
    return ''.join(parts).strip()


os.makedirs(P('assets', 'dist'), exist_ok=True)

# ---- vendor
vendor = []
for n in ('gsap.min.js', 'ScrollTrigger.min.js'):
    vendor.append(read(P('assets', 'vendor', n)))
lenis = re.sub(r'//# sourceMappingURL=.*', '', read(P('assets', 'vendor', 'lenis.min.js')))
vendor.append('(function(){' + lenis + '})();')
v = '\n;'.join(vendor)
open(P('assets', 'dist', 'vendor.min.js'), 'w', encoding='utf-8', newline='\n').write(v)

# ---- app
app = '\n;'.join(strip_js(read(P('assets', 'js', n))) for n in ('config.js', 'i18n.js', 'data.js', 'main.js'))
open(P('assets', 'dist', 'app.min.js'), 'w', encoding='utf-8', newline='\n').write(app)

# ---- css
css = min_css(read(P('assets', 'css', 'fonts.css')) + '\n' + read(P('assets', 'css', 'style.css')))
open(P('assets', 'dist', 'style.min.css'), 'w', encoding='utf-8', newline='\n').write(css)

for n in ('vendor.min.js', 'app.min.js', 'style.min.css'):
    print('%-16s %6.1f KB' % (n, os.path.getsize(P('assets', 'dist', n)) / 1024))
