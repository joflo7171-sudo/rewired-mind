#!/usr/bin/env python3
"""Builds dist/The-Shadow-Work-Academy.zip (the customer deliverable) and dist/site (deployable sales site)."""
import os, shutil, zipfile
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dist = os.path.join(root, 'dist'); shutil.rmtree(dist, ignore_errors=True); os.makedirs(dist)
top = 'The-Shadow-Work-Academy'
z = zipfile.ZipFile(os.path.join(dist, top + '.zip'), 'w', zipfile.ZIP_DEFLATED)
z.write(os.path.join(root, 'package/START-HERE.html'), f'{top}/START-HERE.html')
for d in ('app', 'content'):
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if f == 'print.html': continue
            p = os.path.join(dp, f); z.write(p, f'{top}/Academy/' + os.path.relpath(p, root))
for f in sorted(os.listdir(os.path.join(root, 'resources'))):
    z.write(os.path.join(root, 'resources', f), f'{top}/Academy/resources/{f}')
z.close()
shutil.copytree(os.path.join(root, 'site'), os.path.join(dist, 'site'))
print('built', os.listdir(dist))
