// GET /api/verify-session?session_id=cs_...  ->  { ok, download_url, expires_at } or { ok:false, reason }
import { config as readConfig, verifySession, signLink, json } from "../lib/delivery.mjs";

export default async (req) => {
  if (req.method !== "GET") return json(405, { ok: false, reason: "method_not_allowed" });
  const c = readConfig();
  const sessionId = new URL(req.url).searchParams.get("session_id") || "";
  const v = await verifySession(sessionId, c);
  if (!v.ok) return json(v.status, { ok: false, reason: v.reason });
  const link = signLink(sessionId, c);
  return json(200, { ok: true, download_url: link.url, expires_at: link.expiresAt, file_name: c.zipName });
};

export const config = { path: "/api/verify-session" };
