// OperatorGrid digital delivery (Option A): verify a Stripe Checkout Session, then issue a
// short-lived signed link to the product ZIP, which is bundled privately with the function
// (never in /public).
// No third-party dependencies: uses Node's built-in fetch and crypto.
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function config(env = process.env) {
  return {
    stripeKey: env.STRIPE_SECRET_KEY || "",          // restricted key: read access to Checkout Sessions, PaymentIntents, Charges
    priceId: env.STRIPE_PRICE_ID || "",              // price_... for the $149 one-time price
    signingSecret: env.DOWNLOAD_SIGNING_SECRET || "", // long random string (32+ characters)
    windowDays: Number(env.DOWNLOAD_WINDOW_DAYS || 30),     // how long after purchase a buyer can self-serve downloads
    linkMinutes: Number(env.DOWNLOAD_LINK_MINUTES || 15),   // lifetime of each signed download link
    zipName: env.PRODUCT_ZIP_NAME || "OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.3.zip",
    zipPath: env.PRODUCT_ZIP_PATH || "",
    stripeApi: env.STRIPE_API_BASE || "https://api.stripe.com",
  };
}

const SESSION_RE = /^cs_(test|live)_[A-Za-z0-9]{10,250}$/;

export function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" },
  });
}

/** Returns { ok: true, sessionId } or { ok: false, status, reason }. */
export async function verifySession(sessionId, c, now = Date.now()) {
  if (!c.stripeKey || !c.priceId || !c.signingSecret || c.signingSecret.length < 32) {
    return { ok: false, status: 503, reason: "not_configured" };
  }
  if (!sessionId || !SESSION_RE.test(sessionId)) return { ok: false, status: 400, reason: "invalid_session" };
  const keyIsLive = /^(sk|rk)_live_/.test(c.stripeKey);
  if (keyIsLive !== sessionId.startsWith("cs_live_")) return { ok: false, status: 400, reason: "invalid_session" };

  const url = `${c.stripeApi}/v1/checkout/sessions/${encodeURIComponent(sessionId)}` +
    `?expand[]=line_items&expand[]=payment_intent.latest_charge`;
  let res;
  try {
    res = await fetch(url, { headers: { authorization: `Bearer ${c.stripeKey}` } });
  } catch {
    return { ok: false, status: 502, reason: "stripe_unreachable" };
  }
  if (res.status === 404) return { ok: false, status: 404, reason: "not_found" };
  if (!res.ok) return { ok: false, status: 502, reason: "stripe_error" };
  const s = await res.json();

  if (s.mode !== "payment" || s.status !== "complete" || s.payment_status !== "paid") {
    return { ok: false, status: 402, reason: "not_paid" };
  }
  const items = (s.line_items && s.line_items.data) || [];
  if (!items.some((li) => li.price && li.price.id === c.priceId)) {
    return { ok: false, status: 403, reason: "wrong_product" };
  }
  if (!s.created || s.created * 1000 < now - c.windowDays * 86400000) {
    return { ok: false, status: 410, reason: "window_expired" };
  }
  const pi = s.payment_intent && typeof s.payment_intent === "object" ? s.payment_intent : null;
  const ch = pi && pi.latest_charge && typeof pi.latest_charge === "object" ? pi.latest_charge : null;
  if (ch && (ch.refunded || ch.amount_refunded > 0 || ch.disputed)) {
    return { ok: false, status: 403, reason: "refunded" };
  }
  return { ok: true, sessionId };
}

function hmac(secret, data) {
  return crypto.createHmac("sha256", secret).update(data).digest("base64url");
}

export function signLink(sessionId, c, now = Date.now()) {
  const exp = Math.floor(now / 1000) + c.linkMinutes * 60;
  const t = hmac(c.signingSecret, `${sessionId}.${exp}`);
  const q = new URLSearchParams({ s: sessionId, e: String(exp), t });
  return { url: `/api/download?${q}`, expiresAt: exp };
}

export function checkLink(s, e, t, c, now = Date.now()) {
  if (!c.signingSecret || c.signingSecret.length < 32) return { ok: false, status: 503, reason: "not_configured" };
  if (!s || !SESSION_RE.test(s) || !/^\d{9,11}$/.test(e || "") || !t) return { ok: false, status: 400, reason: "invalid_link" };
  const expected = Buffer.from(hmac(c.signingSecret, `${s}.${e}`));
  const given = Buffer.from(String(t));
  if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) {
    return { ok: false, status: 403, reason: "invalid_link" };
  }
  if (Number(e) * 1000 < now) return { ok: false, status: 410, reason: "link_expired" };
  return { ok: true };
}

export function findZip(c) {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const candidates = [
    c.zipPath,
    path.join(process.cwd(), "private", c.zipName),
    process.env.LAMBDA_TASK_ROOT ? path.join(process.env.LAMBDA_TASK_ROOT, "private", c.zipName) : "",
    path.join(here, "..", "..", "private", c.zipName),
    path.join(here, "private", c.zipName),
  ].filter(Boolean);
  return candidates.find((p) => fs.existsSync(p)) || null;
}
