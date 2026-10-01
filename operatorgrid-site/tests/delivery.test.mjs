// Run: node --test tests/   (from operatorgrid-site/)
import { test, before, after } from "node:test";
import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { startMockStripe, PRICE } from "./mock-stripe.mjs";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const ZIP = "OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.2.zip";
const KEY = "rk_test_mockkey";
let mock, verify, download;

const setEnv = (o) => { for (const [k, v] of Object.entries(o)) v === undefined ? delete process.env[k] : (process.env[k] = v); };
const call = async (fn, url, method = "GET") => fn(new Request("http://localhost" + url, { method }));

before(async () => {
  mock = await startMockStripe(KEY);
  setEnv({ STRIPE_SECRET_KEY: KEY, STRIPE_PRICE_ID: PRICE, DOWNLOAD_SIGNING_SECRET: "x".repeat(40),
           STRIPE_API_BASE: mock.base, PRODUCT_ZIP_NAME: ZIP, PRODUCT_ZIP_PATH: path.join(ROOT, "private", ZIP) });
  verify = (await import("../netlify/functions/verify-session.mjs")).default;
  download = (await import("../netlify/functions/download.mjs")).default;
});
after(() => mock.server.close());

const reason = async (r) => (await r.json()).reason;

test("paid session -> signed link -> ZIP identical to approved file", async () => {
  const r = await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000");
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.ok(d.ok && d.download_url.startsWith("/api/download?"));
  assert.equal(r.headers.get("cache-control"), "no-store");
  const z = await call(download, d.download_url);
  assert.equal(z.status, 200);
  assert.equal(z.headers.get("content-type"), "application/zip");
  assert.match(z.headers.get("content-disposition"), new RegExp(`attachment; filename="${ZIP}"`));
  const got = Buffer.from(await z.arrayBuffer());
  const want = fs.readFileSync(path.join(ROOT, "private", ZIP));
  assert.equal(crypto.createHash("sha256").update(got).digest("hex"), crypto.createHash("sha256").update(want).digest("hex"));
  const last = mock.log.at(-1);
  assert.equal(last.auth, `Bearer ${KEY}`);
  assert.match(last.url, /expand%5B%5D=line_items|expand\[\]=line_items/);
});

for (const [id, status, why] of [
  ["cs_test_unpaid00000000", 402, "not_paid"],
  ["cs_test_wrongprice0000", 403, "wrong_product"],
  ["cs_test_old00000000000", 410, "window_expired"],
  ["cs_test_refunded000000", 403, "refunded"],
  ["cs_test_partialrefund0", 403, "refunded"],
  ["cs_test_disputed000000", 403, "refunded"],
  ["cs_test_doesnotexist00", 404, "not_found"],
]) {
  test(`denied: ${id} -> ${status} ${why}`, async () => {
    const r = await call(verify, `/api/verify-session?session_id=${id}`);
    assert.equal(r.status, status);
    assert.equal(await reason(r), why);
  });
}

test("denied: missing / malformed / injection-style session ids", async () => {
  for (const q of ["", "?session_id=", "?session_id=abc", "?session_id=cs_test_short", "?session_id=cs_test_aaaaaaaaaaaa/../../x", "?session_id=pi_123456789012345"]) {
    const r = await call(verify, `/api/verify-session${q}`);
    assert.equal(r.status, 400, q);
    assert.equal(await reason(r), "invalid_session");
  }
});

test("denied: live session id with a test key (mode mismatch)", async () => {
  const r = await call(verify, "/api/verify-session?session_id=cs_live_paid0000000000");
  assert.equal(r.status, 400);
});

test("download: tampered, foreign-session, expired and malformed links are refused", async () => {
  const d = await (await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000")).json();
  const u = new URL("http://x" + d.download_url);
  const t = u.searchParams.get("t");
  const tampered = new URLSearchParams({ s: u.searchParams.get("s"), e: u.searchParams.get("e"), t: t.slice(0, -2) + (t.endsWith("AA") ? "BB" : "AA") });
  assert.equal((await call(download, `/api/download?${tampered}`)).status, 403);
  const otherSession = new URLSearchParams({ s: "cs_test_refunded000000", e: u.searchParams.get("e"), t });
  assert.equal((await call(download, `/api/download?${otherSession}`)).status, 403);
  const laterExp = new URLSearchParams({ s: u.searchParams.get("s"), e: String(Number(u.searchParams.get("e")) + 3600), t });
  assert.equal((await call(download, `/api/download?${laterExp}`)).status, 403);
  // genuinely expired (signed in the past)
  const { signLink, config } = await import("../netlify/lib/delivery.mjs");
  const old = signLink("cs_test_paid0000000000", config(), Date.now() - 60 * 60 * 1000);
  const r = await call(download, old.url);
  assert.equal(r.status, 410);
  assert.equal(await reason(r), "link_expired");
  assert.equal((await call(download, "/api/download")).status, 400);
});

test("not configured (no keys) -> 503 not_configured, never a file", async () => {
  const saved = { k: process.env.STRIPE_SECRET_KEY, s: process.env.DOWNLOAD_SIGNING_SECRET };
  setEnv({ STRIPE_SECRET_KEY: undefined });
  let r = await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000");
  assert.equal(r.status, 503); assert.equal(await reason(r), "not_configured");
  setEnv({ STRIPE_SECRET_KEY: saved.k, DOWNLOAD_SIGNING_SECRET: "tooshort" });
  r = await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000");
  assert.equal(r.status, 503);
  r = await call(download, "/api/download?s=cs_test_paid0000000000&e=9999999999&t=abc");
  assert.equal(r.status, 503);
  setEnv({ DOWNLOAD_SIGNING_SECRET: saved.s });
});

test("only GET is allowed", async () => {
  assert.equal((await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000", "POST")).status, 405);
  assert.equal((await call(download, "/api/download", "POST")).status, 405);
});

test("missing ZIP file -> 500 file_missing (no crash, no other file served)", async () => {
  const d = await (await call(verify, "/api/verify-session?session_id=cs_test_paid0000000000")).json();
  const saved = process.env.PRODUCT_ZIP_PATH;
  setEnv({ PRODUCT_ZIP_PATH: undefined, PRODUCT_ZIP_NAME: "does-not-exist.zip" });
  const r = await call(download, d.download_url);
  assert.equal(r.status, 500);
  setEnv({ PRODUCT_ZIP_PATH: saved, PRODUCT_ZIP_NAME: ZIP });
});

test("the ZIP is not inside the public folder", () => {
  const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? walk(path.join(d, e.name)) : [e.name]);
  assert.ok(!walk(path.join(ROOT, "public")).some((n) => n.toLowerCase().endsWith(".zip")));
});
