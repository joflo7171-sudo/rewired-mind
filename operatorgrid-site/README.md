# getoperatorgrid.com — preview build (NOT PUBLISHED)

Static, dependency-free sales site for **Cleaning Business AI Growth OS** by OperatorGrid.

- **Status:** local preview only. Not deployed, DNS untouched, no payment processor connected, no live checkout, no discounts.
- **Price shown:** $149 one-time (USD).
- **Product file this page sells:** `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.2.zip` (not hosted here; delivery is set up with the payment provider at launch).

## Preview locally
```
cd operatorgrid-site/public
python3 -m http.server 8765
# open http://127.0.0.1:8765/
```
The download functions need the test harness (below) or a Netlify deploy.

## Structure
| Path | Purpose |
|---|---|
| `public/` | **Everything served publicly** (the files below) |
| `public/index.html` | Sales page (12 sections) + SEO meta + JSON-LD (Organization, WebSite, Product/Offer, FAQPage) |
| `public/terms.html`, `public/privacy.html`, `public/refunds.html` | **Placeholders only.** The owner must supply the real text before launch. |
| `public/404.html` | Not-found page |
| `public/assets/css/site.css` | All styles (system fonts, no external requests) |
| `public/assets/js/checkout.js` | **The single place to connect checkout.** `CHECKOUT_URL` is empty, so purchase buttons stay inactive. |
| `public/assets/img/` | WebP screenshots (from the approved store images) + Open Graph image |
| `public/robots.txt` | PREVIEW: `Disallow: /`. Swap to the launch version shown in the file. |
| `public/sitemap.xml` | Ready for launch |
| `public/_headers` | Security/cache headers for Netlify or Cloudflare Pages (ignored by other hosts) |
| `public/favicon.svg` | OperatorGrid grid mark |
| `public/thank-you.html` | Post-checkout download page (always noindex). Verifies the purchase, then shows a 15-minute signed download link. |
| `netlify/functions/verify-session.mjs` | `/api/verify-session`: checks the Stripe Checkout Session (paid, the $149 price, within 30 days, not refunded or disputed) |
| `netlify/functions/download.mjs` | `/api/download`: serves the ZIP only with a valid, unexpired signed link |
| `netlify/lib/delivery.mjs` | Shared verification and signing logic. No third-party packages. |
| `private/` | Product ZIP bundled into the functions only (git-ignored; copy the approved ZIP in at deploy) |
| `netlify.toml` | Publish `public/`, functions config, `included_files` for the ZIP, required environment variables |
| `tests/` | `node --test tests/delivery.test.mjs` (15 unit tests) and `node tests/e2e-local.mjs` (34 browser checks) using a mock Stripe API |

## Hosting later (owner approval required)
Any static host works: Netlify, Cloudflare Pages, Vercel or GitHub Pages. Deploy `operatorgrid-site/` with `netlify.toml` (publish directory `public/`, functions in `netlify/functions/`), then point `getoperatorgrid.com` at that host using the host's DNS instructions. Use a dedicated project or repository; do **not** deploy from the Rewired Mind site.

See `LAUNCH-CHECKLIST.md` for everything required before going live.
