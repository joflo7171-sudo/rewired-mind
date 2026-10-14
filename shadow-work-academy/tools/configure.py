#!/usr/bin/env python3
"""Set launch URLs in the sales site, then rebuild dist/.

  python3 tools/configure.py --checkout https://YOURSTORE.gumroad.com/l/YOURPRODUCT
  python3 tools/configure.py --site-base https://rewiredmind.org/shadow-work-academy/

Replaces the current value everywhere under site/. Run tools/launch-check.py afterwards.
"""
import argparse, glob, os, re, subprocess, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ap = argparse.ArgumentParser()
ap.add_argument('--checkout'); ap.add_argument('--site-base')
a = ap.parse_args()
files = glob.glob(os.path.join(root, 'site', '*.html')) + [os.path.join(root, 'site', n) for n in ('robots.txt', 'sitemap.xml')]
def current(pattern, text):
    m = re.search(pattern, text); return m.group(0) if m else None
all_text = ''.join(open(f).read() for f in files)
if a.checkout:
    if not re.match(r'^https://[^\s"<>]+$', a.checkout): sys.exit('checkout URL must be an https URL')
    old = current(r'https://[^\s"<>]*(?:checkout\.invalid|gumroad\.com/l/)[^\s"<>]*', all_text)
    if not old: sys.exit('no existing checkout URL found')
    for f in files:
        t = open(f).read(); open(f, 'w').write(t.replace(old, a.checkout))
    print('checkout:', old, '->', a.checkout)
if a.site_base:
    if not a.site_base.endswith('/'): sys.exit('site base must end with /')
    old = current(r'https://[^\s"<>]*/shadow-work-academy/', all_text)
    for f in files:
        t = open(f).read(); open(f, 'w').write(t.replace(old, a.site_base))
    print('site base:', old, '->', a.site_base)
subprocess.check_call([sys.executable, os.path.join(root, 'tools', 'package.py')])
