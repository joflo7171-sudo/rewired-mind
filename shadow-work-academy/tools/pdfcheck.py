#!/usr/bin/env python3
"""PDF QA on the extracted customer package. Usage: pdfcheck.py <extracted Academy/resources dir> <content dir>
Checks: page counts, embedded fonts, blank pages, ink in outer margins (clipping/overflow), text completeness vs. source content."""
import glob, os, re, subprocess, sys, tempfile, json
from PIL import Image
res, content = sys.argv[1], sys.argv[2]
fails = 0
def ok(c, m):
    global fails
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: fails += 1
def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('—', '-').replace('–', '-').replace(' ', ' ')
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
pdfs = sorted(glob.glob(os.path.join(res, '*.pdf')))
ok(len(pdfs) == 10, f'10 PDFs present (found {len(pdfs)})')
tmp = tempfile.mkdtemp()
for pdf in pdfs:
    name = os.path.basename(pdf)
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    fonts = subprocess.run(['pdffonts', pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    ok(all(re.search(r'\byes\s+(yes|no)\s+(yes|no)', l) for l in fonts if l.strip()), f'{name}: {pages} pages, all {len(fonts)} fonts embedded')
    base = os.path.join(tmp, name[:-4])
    subprocess.run(['pdftoppm', '-r', '50', '-png', pdf, base], check=True, capture_output=True)
    blank, edge = [], []
    for png in sorted(glob.glob(base + '-*.png')):
        im = Image.open(png).convert('L'); w, h = im.size
        px = im.load()
        dark = sum(1 for y in range(h) for x in range(w) if px[x, y] < 235)
        pg = int(re.search(r'-(\d+)\.png$', png).group(1))
        if dark / (w * h) < 0.002: blank.append(pg)
        # outer 0.4in strip at 50dpi = 20px on left/right (content margin is 0.75in)
        m = 20
        edge_ink = sum(1 for y in range(h) for x in list(range(0, m)) + list(range(w - m, w)) if px[x, y] < 200)
        if edge_ink > 30: edge.append(pg)
    ok(not blank, f'{name}: no blank pages' + (f' (blank: {blank})' if blank else ''))
    ok(not edge, f'{name}: no ink in outer margins (no clipping/overflow)' + (f' (pages: {edge})' if edge else ''))
# content completeness: every sentence-ish chunk from the modules must appear in the workbook text
wb = [p for p in pdfs if '00-complete' in p][0]
txt = norm(subprocess.run(['pdftotext', '-layout', wb, '-'], capture_output=True, text=True).stdout)
strings = json.loads(subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dump-strings.js'), content], capture_output=True, text=True, check=True).stdout)
miss = []
for s in strings:
    chunk = norm(s)
    if chunk and chunk[:60] not in txt: miss.append(s[:70])
ok(not miss, f'workbook contains all {len(strings)} long text blocks from the source content' + (f' (missing: {miss[:5]})' if miss else ''))
# per-module page headings
for n in range(1, 7):
    ok(f'module {n} of 6' in txt, f'workbook has Module {n} heading')
print('PDF FAILURES:', fails) if fails else print('PDF CHECKS: ALL PASSED')
sys.exit(1 if fails else 0)
