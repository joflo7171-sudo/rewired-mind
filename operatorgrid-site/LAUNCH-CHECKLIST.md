# getoperatorgrid.com — Launch checklist (nothing below has been done)

Every item needs owner approval. The site stays in preview until all **Blockers** are complete.

## Blockers
1. **Product testing:** v1.0.3 passes real Microsoft Excel and Google Sheets testing (`cleaning-business-ai-growth-os/LAUNCH-KIT/EXCEL-SHEETS-TEST-CHECKLIST.md`). The page states "Excel 2019+ / Microsoft 365 & Google Sheets", so that claim must be verified before publishing.
2. **Support email:** create the branded mailbox, send and receive a test message, then replace the 3 support placeholders (`public/index.html` FAQ + Support section, `public/thank-you.html`) and `READ-ME-FIRST.txt` in the ZIP. Rebuild and re-audit the ZIP.
3. **Refund policy:** the owner writes it to match the payment provider's rules. Replace the FAQ placeholder and `refunds.html`.
4. **Terms of Sale and Privacy Policy:** the owner supplies the text (professional review recommended) for `terms.html` and `privacy.html`.
5. **Payment setup (Stripe Managed Payments):** the owner creates and verifies the account and a **$149 one-time** product (no coupons), and sets up delivery of the v1.0.2 ZIP after payment.
   - Complete a **test-mode purchase end to end**, including receiving the download.
   - Then paste the live checkout URL into `public/assets/js/checkout.js` → `CHECKOUT_URL`.
6. **Hosting:** choose a static host and deploy `operatorgrid-site/` using `netlify.toml` (or the equivalent for another host). Copy the approved ZIP into `private/` and set the environment variables listed in `netlify.toml`. Point `getoperatorgrid.com` DNS at it, enable HTTPS, and verify both `www` and the bare domain.

## Switch from preview to live
- [ ] Remove `<meta name="robots" content="noindex, nofollow">` from `index.html`, `terms.html`, `privacy.html`, `refunds.html` and `404.html`.
- [ ] Replace `public/robots.txt` with the launch version shown in its comments, **plus** `Disallow: /thank-you.html` and `Disallow: /api/`.
- [ ] Keep `thank-you.html` noindex permanently.
- [ ] Remove the yellow "Preview build" bar from every page.
- [ ] Remove the `.placeholder` spans once their content exists.
- [ ] Confirm the JSON-LD `availability` (InStock) is true only once checkout is live.
- [ ] Submit `sitemap.xml` in Google Search Console.

## Recommended (not blockers)
- A 3–5 minute demo video embedded in the "See it in action" section.
- Privacy-friendly analytics, if wanted. Update the privacy policy to match.
- A favicon PNG/ICO set for older browsers. The SVG works in all modern ones.

## Must stay true after launch
- $149 one-time. No crossed-out prices, countdowns, fake scarcity, fake reviews, fake logos, sales counts or earnings claims.
- Only add testimonials from real buyers, with written permission.
