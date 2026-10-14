#!/usr/bin/env python3
"""Builds dist/The-Shadow-Work-Academy.zip (the customer deliverable) and dist/site (deployable sales site)."""
import os, shutil, zipfile
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dist = os.path.join(root, 'dist'); shutil.rmtree(dist, ignore_errors=True); os.makedirs(dist)
top = 'The-Shadow-Work-Academy'
# bundle fonts into the site copy (repo keeps one source in fonts/)
shutil.rmtree(os.path.join(root, 'site', 'fonts'), ignore_errors=True); shutil.copytree(os.path.join(root, 'fonts'), os.path.join(root, 'site', 'fonts'))
# keep marketing claims in sync with the built workbook
import re, subprocess
wb = os.path.join(root, 'resources', '00-complete-academy-workbook.pdf')
pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', wb], capture_output=True, text=True).stdout).group(1))
ip = os.path.join(root, 'site', 'index.html'); t = open(ip).read()
t2 = re.sub(r'(?<![\w-])\d+\+?-page printable', f'{pages}-page printable', re.sub(r'(?<![\w-])\d+\+? pages, PDF', f'{pages} pages, PDF', re.sub(r'<strong>\d+-page</strong>', f'<strong>{pages}-page</strong>', t)))
if t2 != t: open(ip, 'w').write(t2); print('synced workbook page count in site/index.html ->', pages)
z = zipfile.ZipFile(os.path.join(dist, top + '.zip'), 'w', zipfile.ZIP_DEFLATED)
z.write(os.path.join(root, 'package/START-HERE.html'), f'{top}/START-HERE.html')
for d in ('app', 'content', 'fonts'):
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if f == 'print.html': continue
            p = os.path.join(dp, f); z.write(p, f'{top}/Academy/' + os.path.relpath(p, root))
for f in sorted(os.listdir(os.path.join(root, 'resources'))):
    z.write(os.path.join(root, 'resources', f), f'{top}/Academy/resources/{f}')
z.close()
shutil.copytree(os.path.join(root, 'site'), os.path.join(dist, 'site'))
print('built', os.listdir(dist))
