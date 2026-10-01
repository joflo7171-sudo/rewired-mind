# Stripe TEST-MODE runbook: proving the secure delivery before any real sale

**Scope:** Stripe **test mode only**. No live keys, no live checkout, no DNS change, noindex stays on, no discounts, price stays $149.

**Status:** the secure download system has been tested **only against simulated Stripe data** (15 unit tests + 34 browser checks). It is **not production-ready** until every item in section 5 passes against a real Stripe test-mode transaction.

## 1. Prerequisites (you)
- [ ] A Stripe account exists. Test mode is available right away, before live activation.
- [ ] Managed Payments is enabled (or available in test mode). If it isn't available in test mode, run this once with standard test-mode Checkout to verify delivery, and note that the Managed Payments specifics stay unverified.
- [ ] A **non-public test deploy** of `operatorgrid-site/` is available. Options:
  - a Netlify deploy on its default `*.netlify.app` URL (password-protected if your plan allows), with noindex on and no custom domain; or
  - a local run with the Netlify CLI (`netlify dev`) plus a tunnel, if you prefer nothing hosted.

  Either way, **getoperatorgrid.com DNS is not touched.**

## 2. Test-mode objects (you, in the Stripe Dashboard with Test mode ON)
- [ ] **Product:** `Cleaning Business AI Growth OS` with an eligible product tax code (see `05` section 3)
- [ ] **Price:** **$149.00 USD, one-time**. Note the `price_...` ID.
- [ ] **Payment Link:**
  - quantity fixed at 1, promotion codes OFF, terms acceptance ON;
  - Managed Payments ON (if available);
  - after payment, redirect to `https://<test-deploy-url>/thank-you.html?session_id={CHECKOUT_SESSION_ID}`.
- [ ] **Restricted key** (test): **read** permission on Checkout Sessions, PaymentIntents and Charges only. Copy the `rk_test_...` key.
- [ ] **A second test Price** (any amount, one-time). It's only for the "wrong product" check and must never be linked from the site.

## 3. Test deploy configuration (you set the values; I can walk you through it)
Set these environment variables on the test deploy **only**:

| Variable | Value |
|---|---|
| `STRIPE_SECRET_KEY` | `rk_test_...` (**never** a live key during this runbook) |
| `STRIPE_PRICE_ID` | the test `price_...` for $149 |
| `DOWNLOAD_SIGNING_SECRET` | a random string of 32+ characters |
| `PRODUCT_ZIP_NAME` | `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.3.zip` (or v1.0.4 once the support email is in) |

Copy the approved ZIP into `private/` before deploying. Record its SHA-256 (v1.0.3 = `632ee970b498a78c3236a7e689967481fc7f71193a125b85ba3110a792570d35`).

**Do not paste the test Payment Link into `public/assets/js/checkout.js`.** Open it directly from the Dashboard so the site's buttons stay inactive.

## 4. Test cards (test mode; any future expiry, any CVC, any postcode)
| Card | Use |
|---|---|
| `4242 4242 4242 4242` | Successful payment |
| `4000 0025 0000 3155` | 3-D Secure authentication |
| `4000 0000 0000 0002` | Declined |
| `4000 0000 0000 9995` | Insufficient funds |
| `4000 0000 0000 0259` | Payment succeeds, then a **dispute** is created automatically |

Confirm these on Stripe's testing page. Managed Payments may handle disputes differently, so record what actually happens.

## 5. Production-readiness proof (all must PASS)
| # | Requirement | Procedure | Pass condition |
|---|---|---|---|
| 1 | **Paid-session verification** | Pay with 4242 via the test Payment Link | Lands on thank-you.html, shows "Your Cleaning Business AI Growth OS is ready" |
| 2 | **Exact approved ZIP delivered** | Click "Download the ZIP" and compute SHA-256 of the saved file (`shasum -a 256 <file>` on Mac, `certutil -hashfile <file> SHA256` on Windows) | Equals the recorded hash; filename correct; opens; 50 files |
| 3 | **Correct-product verification** | Temporarily set `STRIPE_PRICE_ID` to the **second** test price, redeploy, reload the thank-you link from #1 | Shows "We couldn't match this order", no download. Then restore the $149 price ID. |
| 4 | **Unpaid / declined** | Pay with 0002 and 9995; also open thank-you.html with a made-up `session_id=cs_test_...` | No download in any case |
| 5 | **Refund detection** | Refund the #1 payment in the Dashboard (or via the Managed Payments refund route), then reload its thank-you link | "This order was refunded", no download. A link generated **before** the refund stops working once its 15 minutes run out. |
| 6 | **Dispute behavior** | Pay with 0259, wait for the dispute to appear, then reload that order's thank-you link | "This order was refunded" message (disputed orders are blocked), no download. Record how Managed Payments shows the dispute. |
| 7 | **30-day access window** | Temporarily set `DOWNLOAD_WINDOW_DAYS=0` and redeploy. Reload a paid order's link. Then restore 30. | "This download page has expired", no download. After restoring, the same order downloads again. |
| 8 | **Expiring download link** | Temporarily set `DOWNLOAD_LINK_MINUTES=1` and redeploy. Get a link, wait 2 minutes, then click it. Restore 15. | The expired link returns an error. Reloading the thank-you page gives a fresh, working link. |
| 9 | **Tampered link** | Change one character of the `t=` value in a download URL | Refused |
| 10 | **ZIP not public** | Try `/<zip name>`, `/private/<zip name>` and `/assets/<zip name>` on the test deploy | All 404 |
| 11 | **Receipt + refund emails** | Check the test buyer's inbox (test-mode emails may only go to verified addresses; note what Stripe sends) | Received or noted |
| 12 | **Mobile** | Repeat #1–#2 on an iPhone and an Android phone | Works |
| 13 | **Managed Payments data shape** | In the Dashboard, open the test session and confirm a PaymentIntent and Charge are attached | Present. If not, the refund/dispute check needs adjusting; report it to me before going further. |

Record PASS or FAIL for each, with screenshots. Then run the full `06-TEST-PURCHASE-CHECKLIST.md`.

**Only when all 13 pass is the delivery system production-ready.**

## 6. Clean-up after the test run
- Restore `DOWNLOAD_WINDOW_DAYS=30`, `DOWNLOAD_LINK_MINUTES=15` and the $149 test `STRIPE_PRICE_ID`.
- Keep the test deploy private, or delete it.
- Keep the test key **only** on the test deploy. Rotate it if it was ever pasted anywhere else.
- Live keys and the live Payment Link are a **separate, owner-approved step** (see `05` section 9).
