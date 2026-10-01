// GET /api/download?s=cs_...&e=<unix>&t=<hmac>  ->  the product ZIP (only with a valid, unexpired signature)
import fs from "node:fs";
import { config as readConfig, checkLink, findZip, json } from "../lib/delivery.mjs";

export default async (req) => {
  if (req.method !== "GET") return json(405, { ok: false, reason: "method_not_allowed" });
  const c = readConfig();
  const q = new URL(req.url).searchParams;
  const v = checkLink(q.get("s"), q.get("e"), q.get("t"), c);
  if (!v.ok) return json(v.status, { ok: false, reason: v.reason });
  const p = findZip(c);
  if (!p) return json(500, { ok: false, reason: "file_missing" });
  const body = fs.readFileSync(p);
  return new Response(body, {
    status: 200,
    headers: {
      "content-type": "application/zip",
      "content-length": String(body.length),
      "content-disposition": `attachment; filename="${c.zipName}"`,
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
    },
  });
};

export const config = { path: "/api/download" };
