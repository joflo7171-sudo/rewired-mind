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
if bad: print('LAUNCH BLOCKERS:'); [print(' -', b) for b in bad]; sys.exit(1)
print('launch-check: no placeholder blockers found (this does NOT verify checkout, email or legal approval)')
