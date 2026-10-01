// End-to-end buyer flow in a real browser against a local stand-in host + mock Stripe.
// Run (from operatorgrid-site/): node tests/e2e-local.mjs
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { startMockStripe, PRICE } from "./mock-stripe.mjs";

const PW = process.env.PLAYWRIGHT_MODULE || "/opt/node22/lib/node_modules/playwright/index.mjs";
const { chromium } = await import(PW);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const ZIP = "OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.3.zip";
const KEY = "rk_test_mockkey";
const mock = await startMockStripe(KEY);
Object.assign(process.env, { STRIPE_SECRET_KEY: KEY, STRIPE_PRICE_ID: PRICE, DOWNLOAD_SIGNING_SECRET: "y".repeat(40),
  STRIPE_API_BASE: mock.base, PRODUCT_ZIP_NAME: ZIP, PRODUCT_ZIP_PATH: path.join(ROOT, "private", ZIP) });
const verify = (await import("../netlify/functions/verify-session.mjs")).default;
const download = (await import("../netlify/functions/download.mjs")).default;

const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml", ".webp": "image/webp", ".jpg": "image/jpeg", ".txt": "text/plain", ".xml": "application/xml" };
const host = http.createServer(async (req, res) => {
  const u = new URL(req.url, "http://localhost");
  const fn = u.pathname === "/api/verify-session" ? verify : u.pathname === "/api/download" ? download : null;
  if (fn) {
    const r = await fn(new Request("http://localhost" + req.url, { method: req.method }));
    res.writeHead(r.status, Object.fromEntries(r.headers));
    return res.end(Buffer.from(await r.arrayBuffer()));
  }
  const p = path.normalize(path.join(ROOT, "public", u.pathname === "/" ? "index.html" : u.pathname));
  if (!p.startsWith(path.join(ROOT, "public")) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end("not found"); }
  res.writeHead(200, { "content-type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});
await new Promise((r) => host.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${host.address().port}`;

const results = [];
const check = (name, ok, detail = "") => { results.push({ name, ok }); console.log(`${ok ? "PASS" : "FAIL"} ${name}${ok ? "" : "  -> " + detail}`); };
const want = crypto.createHash("sha256").update(fs.readFileSync(path.join(ROOT, "private", ZIP))).digest("hex");

const browser = await chromium.launch();
for (const [label, vp, mobile] of [["desktop", { width: 1366, height: 860 }, false], ["mobile", { width: 390, height: 844 }, true]]) {
  const ctx = await browser.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, acceptDownloads: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errors.push(m.text()); });

  await page.goto(`${BASE}/thank-you.html?session_id=cs_test_paid0000000000`);
  await page.waitForSelector('[data-state="ok"].on', { timeout: 5000 });
  check(`${label}: paid order shows the download state`, await page.isVisible("#dl"));
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("#dl")]);
  const saved = await dl.path();
  const got = crypto.createHash("sha256").update(fs.readFileSync(saved)).digest("hex");
  check(`${label}: downloaded file name is the product ZIP`, dl.suggestedFilename() === ZIP, dl.suggestedFilename());
  check(`${label}: downloaded ZIP is byte-identical to the approved build (SHA-256)`, got === want, got);
  check(`${label}: link lifetime shown (minutes)`, Number(await page.textContent("#mins")) >= 14);
  await page.screenshot({ path: `/tmp/lot/siteqa/thankyou-${label}-ok.png`, fullPage: true });

  for (const [q, expect] of [
    ["", "We couldn't find your order"],
    ["?session_id=cs_test_refunded000000", "This order was refunded"],
    ["?session_id=cs_test_unpaid00000000", "Payment not completed"],
    ["?session_id=cs_test_old00000000000", "This download page has expired"],
    ["?session_id=cs_test_doesnotexist00", "We couldn't find your order"],
    ["?session_id=<script>alert(1)</script>", "We couldn't find your order"],
  ]) {
    await page.goto(`${BASE}/thank-you.html${q}`);
    await page.waitForSelector('[data-state="error"].on', { timeout: 5000 });
    const title = await page.textContent("#err-title");
    check(`${label}: ${q || "(no session)"} -> "${expect}", no download button visible`, title === expect && !(await page.isVisible("#dl")), title);
  }
  if (label === "mobile") await page.screenshot({ path: `/tmp/lot/siteqa/thankyou-mobile-error.png`, fullPage: true });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check(`${label}: no horizontal overflow`, overflow === 0, String(overflow));
  check(`${label}: thank-you page is noindex`, (await page.getAttribute('meta[name="robots"]', "content")) === "noindex, nofollow");
  check(`${label}: no page/console errors`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}

// not-configured state (e.g. preview deploy without keys)
const savedKey = process.env.STRIPE_SECRET_KEY; delete process.env.STRIPE_SECRET_KEY;
{
  const ctx = await browser.newContext(); const page = await ctx.newPage();
  await page.goto(`${BASE}/thank-you.html?session_id=cs_test_paid0000000000`);
  await page.waitForSelector('[data-state="error"].on');
  check("no keys configured -> 'Downloads aren't connected yet'", (await page.textContent("#err-title")) === "Downloads aren't connected yet");
  await ctx.close();
}
process.env.STRIPE_SECRET_KEY = savedKey;

// the ZIP must never be reachable as a public file
for (const p of [`/${ZIP}`, `/private/${ZIP}`, `/../private/${ZIP}`, `/assets/${ZIP}`, "/netlify.toml", "/netlify/functions/download.mjs"]) {
  const r = await fetch(BASE + p);
  check(`public URL ${p} is not served (404)`, r.status === 404, String(r.status));
}
// main site regression: checkout still inactive
{
  const ctx = await browser.newContext(); const page = await ctx.newPage();
  await page.goto(BASE + "/");
  const hrefs = await page.$$eval("[data-checkout]", (a) => a.map((x) => x.getAttribute("href")));
  check("homepage purchase buttons still inactive (no external checkout URL)", hrefs.every((h) => h === "#pricing" || h === "#"), hrefs.join(","));
  await ctx.close();
}
await browser.close(); host.close(); mock.server.close();
const failed = results.filter((r) => !r.ok).length;
console.log(`\n${results.length - failed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
