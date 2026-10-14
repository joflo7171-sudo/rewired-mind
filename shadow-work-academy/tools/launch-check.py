#!/usr/bin/env python3
"""Fails (exit 1) while any launch blocker remains in the shipped files."""
import glob, os, re, sys, zipfile
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
bad = []
site = glob.glob(os.path.join(root, 'site', '*.html'))
for f in site:
    t = open(f).read()
    if 'checkout.invalid' in t: bad.append(f'{os.path.relpath(f, root)}: checkout URL is still the placeholder')
    if re.search(r'LEGAL REVIEW REQUIRED', t): bad.append(f'{os.path.relpath(f, root)}: legal-review marker present (remove after counsel approves)')
    if re.search(r'PLACEHOLDER|TODO|FIXME|lorem ipsum', t, re.I): bad.append(f'{os.path.relpath(f, root)}: placeholder text')
for f in glob.glob(os.path.join(root, 'content', '*.js')) + glob.glob(os.path.join(root, 'app', '*.js')) + [os.path.join(root, 'package', 'START-HERE.html')]:
    if re.search(r'PLACEHOLDER|TODO|FIXME|lorem ipsum', open(f).read(), re.I): bad.append(f'{os.path.relpath(f, root)}: placeholder text')
# ---- domain and separation checks on the production build ----
DOMAIN = 'shadowworkacademy.org'
dist = os.path.join(root, 'dist', 'site')
if not os.path.isdir(dist): bad.append('dist/site missing: run tools/package.py')
else:
    allowed_rm = re.compile(r'rewiredmind\.org')  # brand link and support@ address are intentional
    for f in glob.glob(os.path.join(dist, '*')):
        if not os.path.isfile(f) or f.endswith(('.png', '.pdf', '.woff2')): continue
        t = open(f, errors='ignore').read(); name = os.path.relpath(f, root)
        if re.search(r'rewiredmind\.org/shadow-work-academy', t): bad.append(f'{name}: old domain path rewiredmind.org/shadow-work-academy still present')
        for m in re.finditer(r'https?://[^\s"<>\']*rewiredmind\.org[^\s"<>\']*', t):
            if m.group(0).rstrip('/') != 'https://rewiredmind.org': bad.append(f'{name}: unexpected rewiredmind.org link {m.group(0)} (only the brand home link is intended)')
        if f.endswith('.html'):
            c = re.search(r'<link rel="canonical" href="([^"]+)"', t)
            if not c or not c.group(1).startswith(f'https://{DOMAIN}/'): bad.append(f'{name}: canonical is not on {DOMAIN}')
            o = re.search(r'property="og:url" content="([^"]+)"', t)
            if not o or not o.group(1).startswith(f'https://{DOMAIN}/'): bad.append(f'{name}: og:url is not on {DOMAIN}')
    for n in ('sitemap.xml', 'robots.txt'):
        t = open(os.path.join(dist, n)).read()
        if DOMAIN not in t: bad.append(f'{n}: does not reference {DOMAIN}')
    idx = open(os.path.join(dist, 'index.html')).read()
    co = re.search(r'https://[^\s"<>]*(?:gumroad\.com|checkout\.invalid)[^\s"<>]*', idx)
    if co and DOMAIN in co.group(0): bad.append('checkout URL must not be on the website domain')
    if not co: bad.append('no checkout URL found in index.html')
if bad: print('LAUNCH BLOCKERS:'); [print(' -', b) for b in bad]; sys.exit(1)
print('launch-check: no placeholder blockers found (this does NOT verify checkout, email or legal approval)')
