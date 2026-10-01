# getoperatorgrid.com — preview build (NOT PUBLISHED)

Static, dependency-free sales site for **Cleaning Business AI Growth OS** by OperatorGrid.

- **Status:** local preview only. Not deployed, DNS untouched, no payment processor connected, no live checkout, no discounts.
- **Price shown:** $149 one-time (USD).
- **Product file this page sells:** `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.2.zip` (not hosted here; delivery is set up with the payment provider at launch).

## Preview locally
```
cd operatorgrid-site
python3 -m http.server 8765
# open http://127.0.0.1:8765/
```

## Structure
| Path | Purpose |
|---|---|
| `index.html` | Sales page (12 sections) + SEO meta + JSON-LD (Organization, WebSite, Product/Offer, FAQPage) |
| `terms.html`, `privacy.html`, `refunds.html` | **Placeholders only.** The owner must supply the real text before launch. |
| `404.html` | Not-found page |
| `assets/css/site.css` | All styles (system fonts, no external requests) |
| `assets/js/checkout.js` | **The single place to connect checkout.** `CHECKOUT_URL` is empty, so purchase buttons stay inactive. |
| `assets/img/` | WebP screenshots (from the approved store images) + Open Graph image |
| `robots.txt` | PREVIEW: `Disallow: /`. Swap to the launch version shown in the file. |
| `sitemap.xml` | Ready for launch |
| `_headers` | Security/cache headers for Netlify or Cloudflare Pages (ignored by other hosts) |
| `favicon.svg` | OperatorGrid grid mark |

## Hosting later (owner approval required)
Any static host works: Netlify, Cloudflare Pages, Vercel or GitHub Pages. Publish the `operatorgrid-site/` folder as the site root, then point `getoperatorgrid.com` at that host using the host's DNS instructions. Use a dedicated project or repository; do **not** deploy from the Rewired Mind site.

See `LAUNCH-CHECKLIST.md` for everything required before going live.
