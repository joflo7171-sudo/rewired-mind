// Renders printable HTML views to PDFs with Chromium. Usage: node tools/build-pdfs.js
const { chromium } = require('playwright');
const path = require('path');
const root = path.resolve(__dirname, '..');
const jobs = [{ only: 'workbook', file: '00-complete-academy-workbook.pdf' }, { only: 'sample', file: '../site/downloads/module-1-free-sample.pdf' }];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + root + '/app/print.html?only=workbook', { waitUntil: 'networkidle' });
  (await p.evaluate(() => SWA.resources.map(r => ({ id: r.id, file: r.file })))).forEach(r => jobs.push({ only: r.id, file: r.file }));
  for (const j of jobs) {
    await p.goto('file://' + root + '/app/print.html?only=' + j.only, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(root, 'resources', j.file), format: 'Letter', printBackground: true, margin: { top: '0.75in', bottom: '0.8in', left: '0.75in', right: '0.75in' }, displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: '<div style="font:8px Inter,sans-serif;color:#777;width:100%;text-align:center">The Shadow Work Academy · Educational self-reflection, not therapy · <span class="pageNumber"></span></div>' });
    console.log('built', j.file);
  }
  await b.close();
})();
