// Captures real previews of the academy UI and workbook for the sales site.
const { chromium } = require('playwright');
const path = require('path'); const { execSync } = require('child_process');
const root = path.resolve(__dirname, '..'); const url = 'file://' + root + '/app/index.html';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1.5 });
  const p = await ctx.newPage();
  await p.goto(url + '#/welcome'); await p.waitForTimeout(600);
  await p.screenshot({ path: root + '/site/img/preview-welcome.png' });
  // sample data so dashboard shows realistic state without claiming customer data
  await p.goto(url + '#/dashboard'); await p.waitForTimeout(400);
  await p.screenshot({ path: root + '/site/img/preview-dashboard.png' });
  await p.goto(url + '#/module/1'); await p.waitForTimeout(500);
  await p.screenshot({ path: root + '/site/img/preview-module-lesson.png' });
  await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}.top,.toc{position:static!important}' });
  const box = await p.locator('#worksheet').boundingBox();
  await p.screenshot({ path: root + '/site/img/preview-worksheet.png', fullPage: true, clip: { x: 0, y: box.y - 20, width: 1200, height: 800 } });
  await p.goto(url + '#/resources'); await p.waitForTimeout(400);
  await p.screenshot({ path: root + '/site/img/preview-resources.png' });
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 780 });
  await m.goto(url + '#/module/5'); await m.waitForTimeout(500);
  await m.screenshot({ path: root + '/site/img/preview-mobile.png' });
  await b.close();
  const wb = root + '/resources/00-complete-academy-workbook.pdf';
  const pageWith = (needle) => { for (let i = 1; i < 70; i++) { const t = execSync(`pdftotext -f ${i} -l ${i} "${wb}" -`).toString(); if (t.includes(needle)) return i; } throw new Error('page not found ' + needle); };
  for (const [pg, name] of [[1,'workbook-cover'],[pageWith('Meet Your Shadow'),'workbook-module'],[pageWith('Looking across your three rows'),'workbook-worksheet']])
    execSync(`pdftoppm -r 70 -png -singlefile -f ${pg} -l ${pg} "${root}/resources/00-complete-academy-workbook.pdf" "${root}/site/img/${name}"`);
  console.log('done');
})();
