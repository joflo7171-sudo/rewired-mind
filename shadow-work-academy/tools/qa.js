// Launch QA. Tests the ACTUAL customer ZIP (extracted to a temp dir) and the built sales site.
// Usage: NODE_PATH=<dir with playwright> [AXE=<path to axe.min.js>] node tools/qa.js
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os'), { execSync, spawnSync } = require('child_process');
const root = path.resolve(__dirname, '..');
const zip = path.join(root, 'dist/The-Shadow-Work-Academy.zip');
const site = path.join(root, 'dist/site');
const tmp = fs.mkdtempSync(path.join(process.env.QA_TMP || os.tmpdir(), 'swa-qa-'));
execSync(`unzip -q "${zip}" -d "${tmp}"`);
const pkg = path.join(tmp, 'The-Shadow-Work-Academy');
const app = 'file://' + pkg + '/Academy/app/index.html';
let fails = 0, passes = 0; const warns = [];
const ok = (c, m) => { if (c) passes++; else { fails++; console.log('FAIL ' + m); } };
const warn = m => { warns.push(m); console.log('WARN ' + m); };
const read = f => fs.readFileSync(f, 'utf8');
const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);

(async () => {
  // ---------- 1. package hygiene ----------
  const files = walk(pkg).map(f => path.relative(pkg, f)).sort();
  console.log('ZIP entries (' + files.length + '):\n  ' + files.join('\n  '));
  const expected = ['START-HERE.html', 'Academy/app/index.html', 'Academy/app/app.js', 'Academy/app/styles.css', ...[1,2,3,4,5,6].map(n => `Academy/content/module${n}.js`), 'Academy/content/resources.js', 'Academy/resources/00-complete-academy-workbook.pdf'];
  expected.forEach(f => ok(files.includes(f), 'package contains ' + f));
  ok(files.filter(f => /resources\/0[1-9]-.*\.pdf$/.test(f)).length === 9, 'package contains exactly 9 supporting-resource PDFs');
  ok(!files.some(f => /print\.html|\.git|node_modules|\.DS_Store|\.map$|tools\/|package\/|dist\/|\.py$|\.md$|\.log$|\.env|\.key$|secret/i.test(f)), 'no development/secret files in package');
  ok(files.every(f => !f.startsWith('/') && !f.includes('..')), 'no absolute/traversal paths');
  const zsize = fs.statSync(zip).size; ok(zsize < 10e6, `ZIP size ${(zsize/1e6).toFixed(2)} MB (< 10 MB)`);
  const sh = read(pkg + '/START-HERE.html');
  [...sh.matchAll(/href="([^"]+)"/g)].forEach(m => ok(fs.existsSync(path.join(pkg, m[1])), 'START-HERE link resolves: ' + m[1]));
  ok(/do not move or rename/i.test(sh), 'START-HERE warns not to move the folder');

  // ---------- 2. privacy claims vs code ----------
  const shipped = files.filter(f => /\.(js|html|css)$/.test(f)).map(f => [f, read(path.join(pkg, f))]);
  const netApis = /\b(fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket|EventSource|importScripts|<form|<iframe|navigator\.geolocation|document\.cookie|indexedDB|gtag\(|fbq\(|dataLayer|google-analytics|googletagmanager|pixel)/i;
  shipped.forEach(([f, t]) => ok(!netApis.test(t), 'no network/tracking APIs in ' + f));
  const urls = new Set(); shipped.forEach(([f, t]) => (t.match(/https?:\/\/[^\s"'<>)]+/g) || []).forEach(u => urls.add(u.replace(/^(https?:\/\/[^/]+).*/, '$1'))));
  console.log('External hosts referenced by shipped files:', [...urls].join(', '));
  ok(urls.size === 0 || [...urls].every(u => /www\.w3\.org/.test(u)), 'shipped Academy files reference NO external hosts (found: ' + [...urls].join(', ') + ')');
  ok(/localStorage/.test(read(pkg + '/Academy/app/app.js')), 'answers use localStorage (as disclosed)');

  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1200, height: 800 } });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/fonts|net::ERR|Failed to load resource/.test(m.text())) errs.push(m.text()); });
  const reqs = []; ctx.on('request', r => reqs.push(r.method() + ' ' + r.url()));

  // ---------- 3. app functional ----------
  await p.goto(app);
  ok((await p.locator('h1').innerText()) === 'From self-doubt to self-trust.', 'welcome renders');
  await p.fill('#nm', 'Test'); await p.click('#begin'); await p.waitForURL(/module\/1/);
  for (const id of ['m1r1','m1r5','m1w_pattern','m1w_name','m1act','m1insight']) await p.fill('#f_' + id, 'answer ' + id);
  await p.fill('textarea[data-k="m1tbl.0.trigger"]', 'trigger row');
  await p.check('#doneBox'); await p.waitForTimeout(500);
  for (let n = 1; n <= 6; n++) {
    await p.goto(app + '#/module/' + n);
    for (const sec of ['lesson','scenario','reflect','worksheet','action','recap','complete']) ok(await p.locator('#' + sec).count() === 1, `module ${n} has #${sec}`);
    ok(await p.locator('#lesson h3').count() >= 5, `module ${n} lesson has >=5 sections`);
    ok(await p.locator('#reflect textarea').count() === 5, `module ${n} has 5 reflection questions`);
    ok((await p.locator('#lesson').innerText()).split(/\s+/).length > 400, `module ${n} lesson > 400 words (not a stub)`);
  }
  for (const n of [1, 3, 5]) { await p.goto(app + '#/module/' + n); ok(await p.locator('details.example').count() === 1, `module ${n} has worked example`); }
  await p.goto(app + '#/module/5'); ok(await p.locator('.script').count() === 16, 'module 5 shows 16 scripts');
  await p.goto(app + '#/module/4'); await p.check('input[name="m4w_audit.0"][value="4"]', { force: true }); await p.waitForTimeout(400);
  ok((await p.locator('#auditTotal_m4w_audit').innerText()).includes('4'), 'audit total updates');
  await p.goto(app + '#/module/2'); await p.check('input[data-k="m2w_conditions.1"]'); await p.waitForTimeout(400);
  await p.goto(app + '#/module/1'); await p.reload();
  ok((await p.inputValue('#f_m1r1')) === 'answer m1r1', 'answer persists after reload');
  ok(await p.isChecked('#doneBox'), 'completion persists');
  await p.goto(app + '#/dashboard'); ok((await p.locator('.bar').getAttribute('aria-valuenow')) === '17', 'dashboard 17% after 1/6');
  ok((await p.locator('h1').innerText()).includes('Test'), 'dashboard greets by name');
  await p.goto(app + '#/progress'); ok((await p.content()).includes('answer m1insight'), 'insight shown on progress');
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#exp')]); const bk = path.join(tmp, 'backup.json'); await dl.saveAs(bk);
  const j = JSON.parse(read(bk)); ok(j.a.m1r1 === 'answer m1r1' && j.done['1'] && j.a['m2w_conditions.1'] === true, 'backup file has answers, completion, checkbox');
  p.once('dialog', d => d.accept()); await p.click('#wipe'); await p.waitForTimeout(500);
  await p.goto(app + '#/module/1'); ok((await p.inputValue('#f_m1r1')) === '', 'erase removes answers');
  await p.goto(app + '#/dashboard'); ok((await p.locator('.bar').getAttribute('aria-valuenow')) === '0', 'erase resets progress');
  await p.goto(app + '#/progress'); await p.setInputFiles('#imp', bk); await p.waitForTimeout(900);
  await p.goto(app + '#/module/1'); ok((await p.inputValue('#f_m1r1')) === 'answer m1r1', 'restore brings answers back');
  await p.goto(app + '#/progress'); fs.writeFileSync(path.join(tmp, 'bad.json'), '{"nope":1}'); await p.setInputFiles('#imp', path.join(tmp, 'bad.json')); await p.waitForTimeout(500);
  ok((await p.locator('#impMsg').innerText()).includes('not a valid'), 'invalid backup file is rejected with a message');
  await p.goto(app + '#/resources');
  const hrefs = await p.$$eval('a[href$=".pdf"]', a => a.map(x => x.getAttribute('href'))); ok(hrefs.length === 10, '10 PDF links in library');
  hrefs.forEach(h => ok(fs.existsSync(path.resolve(pkg + '/Academy/app', h)), 'pdf link resolves ' + h));
  for (const id of ['quickstart','selfworth','tracker','scripts','values','weekly']) { await p.goto(app + '#/resource/' + id); ok(await p.locator('h1').count() === 1, 'resource page ' + id); }
  await p.goto(app + '#/resource/tracker'); ok(await p.locator('textarea').count() === 98, 'tracker has 98 cells');
  await p.goto(app + '#/resource/weekly'); ok(await p.locator('details.week').count() === 12, '12 weekly entries');
  await p.goto(app + '#/help'); ok((await p.content()).includes('support@rewiredmind.org'), 'help shows support email');
  ok(errs.length === 0, 'no console/page errors in app: ' + JSON.stringify(errs));

  // network audit (online run): only file:// and Google Fonts; no POSTs
  const bad = reqs.filter(r => !/^GET (file:|data:)/.test(r));
  ok(bad.length === 0, 'network audit: the Academy made NO requests except to local files. Offenders: ' + JSON.stringify(bad.slice(0, 5)));

  // ---------- 4. offline ----------
  const octx = await b.newContext({ offline: true, viewport: { width: 1200, height: 800 } }); const op = await octx.newPage(); const oerr = [];
  op.on('pageerror', e => oerr.push(e.message));
  await op.goto(app); await op.click('#begin'); await op.waitForURL(/module\/1/);
  await op.fill('#f_m1r1', 'offline answer'); await op.waitForTimeout(500); await op.reload();
  ok((await op.inputValue('#f_m1r1')) === 'offline answer', 'OFFLINE: app loads, saves and persists with no network');
  await op.goto(app + '#/resource/scripts'); ok(await op.locator('.script').count() === 16, 'OFFLINE: resources render');
  ok(oerr.length === 0, 'OFFLINE: no JS errors ' + JSON.stringify(oerr));
  await octx.close();

  // ---------- 5. storage blocked ----------
  const sctx = await b.newContext({ viewport: { width: 1200, height: 800 } });
  await sctx.addInitScript(() => { const t = () => { throw new DOMException('blocked', 'SecurityError'); }; Object.defineProperty(window, 'localStorage', { get: t }); });
  const sp = await sctx.newPage(); const serr = []; sp.on('pageerror', e => serr.push(e.message));
  await sp.goto(app + '#/dashboard'); await sp.waitForTimeout(300);
  ok((await sp.locator('.warn').count()) === 1, 'blocked storage: warning banner shown');
  await sp.goto(app + '#/module/1'); await sp.fill('#f_m1r1', 'x'); ok((await sp.inputValue('#f_m1r1')) === 'x' && serr.length === 0, 'blocked storage: app still usable, no crash ' + JSON.stringify(serr));
  await sctx.close();

  // ---------- 6. keyboard ----------
  const kctx = await b.newContext({ viewport: { width: 1200, height: 800 } }); const kp = await kctx.newPage();
  await kp.goto(app + '#/welcome'); await kp.keyboard.press('Tab');
  ok(await kp.evaluate(() => document.activeElement.className === 'skip'), 'keyboard: first Tab lands on skip link');
  await kp.focus('#nm'); await kp.keyboard.press('Tab'); ok(await kp.evaluate(() => document.activeElement.id === 'begin'), 'keyboard: Tab reaches Begin button');
  await kp.keyboard.press('Enter'); await kp.waitForURL(/module\/1/); ok(true, 'keyboard: Enter starts Module 1');
  await kctx.close();

  // ---------- 7. responsive (app) ----------
  const m = await ctx.newPage(); await m.setViewportSize({ width: 375, height: 760 });
  for (const h of ['#/welcome','#/dashboard','#/module/1','#/module/4','#/module/5','#/resources','#/resource/tracker','#/resource/weekly','#/progress','#/help']) { await m.goto(app + h); await m.waitForTimeout(150); ok(await m.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'app no h-overflow @375 ' + h); }

  // ---------- 8. accessibility (axe-core) ----------
  const axePath = process.env.AXE; let axeSrc = axePath && fs.existsSync(axePath) ? read(axePath) : null;
  if (!axeSrc) warn('axe-core not found (set AXE=...); automated accessibility scan skipped');
  async function axe(page, label) {
    if (!axeSrc) return;
    await page.evaluate(axeSrc);
    const r = await page.evaluate(() => axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] } }));
    const hard = r.violations.filter(v => ['serious', 'critical'].includes(v.impact));
    ok(hard.length === 0, `axe ${label}: ${hard.map(v => v.id + '(' + v.nodes.length + ')').join(', ') || 'no serious/critical violations'}`);
    r.violations.filter(v => !['serious', 'critical'].includes(v.impact)).forEach(v => warn(`axe ${label}: ${v.impact} ${v.id} x${v.nodes.length}`));
  }
  for (const h of ['#/welcome','#/dashboard','#/module/1','#/module/4','#/module/5','#/resources','#/resource/tracker','#/resource/values','#/progress','#/help']) { await p.setViewportSize({ width: 1200, height: 800 }); await p.goto(app + h); await p.waitForTimeout(250); await axe(p, 'app ' + h); }

  // ---------- 9. sales site ----------
  const wbPages = +/Pages:\s+(\d+)/.exec(execSync(`pdfinfo "${pkg}/Academy/resources/00-complete-academy-workbook.pdf"`).toString())[1];
  const stp = await ctx.newPage(); const sterr = []; stp.on('pageerror', e => sterr.push(e.message));
  for (const pg of ['index','refund','terms','privacy','disclaimer','thank-you']) {
    const f = 'file://' + site + '/' + pg + '.html'; await stp.setViewportSize({ width: 1280, height: 900 }); await stp.goto(f);
    ok(await stp.locator('h1').count() === 1, pg + ': exactly one h1');
    ok(await stp.evaluate(() => [...document.images].every(i => i.hasAttribute('alt'))), pg + ': all images have alt');
    ok(await stp.evaluate(() => !!document.documentElement.lang && !!document.title), pg + ': lang and title set');
    const links = await stp.$$eval('a[href]', a => a.map(x => x.getAttribute('href')).filter(h => !/^(https?:|mailto:|#)/.test(h)));
    links.forEach(l => ok(fs.existsSync(path.join(site, l.split('#')[0] || 'index.html')), pg + ': link ' + l));
    for (const a of await stp.$$eval('a[href^="#"],a[href*=".html#"]', a => a.map(x => x.getAttribute('href').split('#')[1]).filter(Boolean))) ok(await stp.locator('#' + a).count() > 0, pg + ': anchor #' + a);
    await stp.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await stp.waitForTimeout(300);
    ok(await stp.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0)), pg + ': all images load (after scroll)');
    await axe(stp, 'site ' + pg);
    await stp.setViewportSize({ width: 375, height: 800 }); await stp.goto(f);
    ok(await stp.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), pg + ': no h-overflow @375');
  }
  const html = read(site + '/index.html');
  const title = /<title>([^<]*)/.exec(html)[1].replace(/&amp;/g, '&'), desc = /name="description" content="([^"]*)/.exec(html)[1];
  ok(title.length <= 65, `title length ${title.length} <= 65`); ok(desc.length <= 160 && desc.length >= 110, `meta description length ${desc.length}`);
  ok(/<link rel="canonical"/.test(html), 'canonical present');
  [...html.matchAll(/<script type="application\/ld\+json">([^<]*)<\/script>/g)].forEach((m2, i) => { try { JSON.parse(m2[1]); ok(true, ''); } catch (e) { ok(false, 'JSON-LD #' + i + ' invalid'); } });
  ok(new RegExp(`<strong>${wbPages}-page</strong>`).test(html), `claim "${wbPages}-page" matches the actual workbook (${wbPages} pages)`);
  ok((html.match(/(\d+)-page printable/g) || []).every(s => s.startsWith(wbPages + '-')), 'all "N-page printable" claims match workbook');
  ok(/\b16 (boundary )?scripts/i.test(html) || /\(16 scripts\)/.test(html), 'claim: 16 scripts');
  ok(/<strong>9<\/strong> supporting resources/.test(html), 'claim: 9 supporting resources');
  ok(/12-week/.test(html), 'claim: 12-week tracker');
  ok(/\$197/.test(html) && !/\$19[0-6]|\$19[8-9]/.test(html), 'price $197 consistent');
  ok(!/guarantee|clinically proven|proven to|\bcure\b|heal your|testimonial|customers say|as seen|limited time|only \d+ left|hurry|countdown/i.test(html.replace(/not guarantee|no guarantee|guaranteed outcomes?|cannot promise|Promised results/gi, '')), 'no scarcity/proof/guarantee language on sales page');
  ok(sterr.length === 0, 'no site JS errors');
  await b.close();
  console.log(`\nRESULT: ${passes} passed, ${fails} failed, ${warns.length} warnings`);
  fs.rmSync(tmp, { recursive: true, force: true });
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error('QA crashed:', e); process.exit(2); });
