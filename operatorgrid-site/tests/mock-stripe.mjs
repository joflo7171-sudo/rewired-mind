// Minimal mock of the Stripe API endpoint used by the delivery functions (test-only).
import http from "node:http";

export const PRICE = "price_test_og149";
const now = () => Math.floor(Date.now() / 1000);

function session(id, o = {}) {
  return {
    id, object: "checkout.session", mode: "payment", status: "complete", payment_status: "paid",
    created: now() - 3600, amount_total: 14900, currency: "usd",
    line_items: { object: "list", data: [{ price: { id: PRICE } }] },
    payment_intent: { id: "pi_x", status: "succeeded", latest_charge: { id: "ch_x", refunded: false, amount_refunded: 0, disputed: false } },
    ...o,
  };
}

export const SESSIONS = {
  cs_test_paid0000000000: session("cs_test_paid0000000000"),
  cs_test_unpaid00000000: session("cs_test_unpaid00000000", { status: "open", payment_status: "unpaid" }),
  cs_test_wrongprice0000: session("cs_test_wrongprice0000", { line_items: { data: [{ price: { id: "price_other" } }] } }),
  cs_test_old00000000000: session("cs_test_old00000000000", { created: now() - 40 * 86400 }),
  cs_test_refunded000000: session("cs_test_refunded000000", { payment_intent: { latest_charge: { refunded: true, amount_refunded: 14900 } } }),
  cs_test_partialrefund0: session("cs_test_partialrefund0", { payment_intent: { latest_charge: { refunded: false, amount_refunded: 5000 } } }),
  cs_test_disputed000000: session("cs_test_disputed000000", { payment_intent: { latest_charge: { refunded: false, amount_refunded: 0, disputed: true } } }),
};

export function startMockStripe(expectedKey) {
  const log = [];
  const server = http.createServer((req, res) => {
    log.push({ url: req.url, auth: req.headers.authorization });
    const m = req.url.match(/^\/v1\/checkout\/sessions\/([^?]+)/);
    if (req.headers.authorization !== `Bearer ${expectedKey}`) { res.writeHead(401); return res.end("{}"); }
    if (!m || !SESSIONS[decodeURIComponent(m[1])]) {
      res.writeHead(404, { "content-type": "application/json" });
      return res.end(JSON.stringify({ error: { type: "invalid_request_error" } }));
    }
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify(SESSIONS[decodeURIComponent(m[1])]));
  });
  return new Promise((resolve) => server.listen(0, "127.0.0.1", () => resolve({ server, log, base: `http://127.0.0.1:${server.address().port}` })));
}
