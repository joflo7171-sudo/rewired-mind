# Stripe Managed Payments: setup checklist

**Product:** Cleaning Business AI Growth OS · **Price:** $149.00 USD one-time · **Discounts:** none · **Delivery:** `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.2.zip` (or the rebuilt version that carries the real support email)

**Status: NOTHING CREATED.** No account, product, price, payment link or checkout exists. Account steps need your identity, business, tax and bank details, so only you can do them.

> **About these facts:** Stripe's documentation site was blocked from this environment. The details below come from search results (late 2026). **Verify each one in your Stripe dashboard and docs** before relying on it:
> - Managed Payments makes Stripe/Link the **merchant of record**, handling global indirect tax (sales tax, VAT, GST), fraud prevention, dispute responses and transaction-level customer support.
> - It works with **Stripe Checkout and Payment Links**, and supports **one-time digital products** such as templates and e-books.
> - Products **must have an eligible product tax code**. Without one, a sale falls back to standard processing (no merchant-of-record coverage).
> - It's available to businesses in supported countries (reported: US, Canada, UK and most of the EU), and isn't available to Connect/platform-controlled accounts.
> - **Fee (reported):** an extra **3.5%** per successful transaction on top of standard processing. That's about **6.4% + $0.30** for a US seller, so on $149 roughly **$9.84 in fees, about $139.16 net** (estimate; confirm).
> - **Stripe does not deliver files.** You need a delivery method (section 6).

---

## 0. Before you start (gates)
- [ ] v1.0.2 passes real **Excel and Google Sheets** testing
- [ ] **support@getoperatorgrid.com** is working and tested (`01-SUPPORT-EMAIL-SETUP.md`)
- [ ] **Refund Policy**, **Terms of Sale** and **Privacy Policy** are final and approved (drafts 02–04)
- [ ] The website is **reachable at getoperatorgrid.com** in "pre-launch mode": checkout inactive, noindex still on. Stripe usually reviews your website during activation; it typically looks for a product description, price, refund policy, terms, privacy policy and contact details. This step means publishing the site, so it needs your separate approval.

## 1. Account (you)
- [ ] Create or sign in to a Stripe account dedicated to OperatorGrid. Use a separate account from any other brand.
- [ ] Business type: [sole proprietor / LLC]; legal name; address; phone
- [ ] Tax ID (SSN or EIN) and identity verification
- [ ] Bank account for payouts
- [ ] **Public details:** business name `OperatorGrid`; website `https://getoperatorgrid.com`; support email `support@getoperatorgrid.com`; support URL `https://getoperatorgrid.com/#support`
- [ ] **Statement descriptor:** e.g. `OPERATORGRID` (≤22 characters). Under Managed Payments the statement may also show Link, so check what customers will see.
- [ ] Turn on 2-step authentication for the Stripe login

## 2. Enable Managed Payments (you)
- [ ] In the Dashboard, find **Managed Payments**, review and accept its terms, and confirm the account is eligible
- [ ] Note who handles **refund requests and disputes** under Managed Payments, and make sure your Refund Policy matches

## 3. Product and price: build in TEST mode first
- [ ] Product name: `Cleaning Business AI Growth OS`
- [ ] Description (short): "A connected cleaning business management system for Excel and Google Sheets. One-time digital download."
- [ ] Image: `LAUNCH-KIT/images/01-cover-1280x720.png`
- [ ] **Product tax code:** choose the eligible category that best fits *downloadable digital templates/software for business use*. See Stripe's help article "Selecting the right Product Tax Code for Managed Payments". Don't guess: if two codes seem to fit, ask Stripe support.
- [ ] Price: **$149.00 USD, one-time** (not recurring)
- [ ] **Tax behavior:** decide **inclusive** (customer pays exactly $149) or **exclusive** (tax added on top where applicable). Then update the website's "$149 one-time · USD" line to match, e.g. "plus applicable tax".
- [ ] Do not create coupons or promotion codes

## 4. Payment Link (test mode)
- [ ] New Payment Link for the $149 price with **Managed Payments enabled** on the link
- [ ] **Quantity:** fixed at 1 (don't let customers adjust it)
- [ ] **Promotion codes:** OFF
- [ ] Collect: email (required); billing address/country as Managed Payments requires
- [ ] **Require agreement to Terms of Sale:** ON (it uses the terms URL from your public details)
- [ ] **After payment:** redirect to `https://getoperatorgrid.com/thank-you.html?session_id={CHECKOUT_SESSION_ID}` (Option A delivery), or show a confirmation message with the download link (Option B delivery)
- [ ] Copy the **test** link URL. It's only for testing and never goes into `checkout.js`.

## 5. Customer emails (you)
- [ ] Settings → Customer emails: **successful payment** and **refund** emails ON, then check how they look under Managed Payments (they may be Link-branded)
- [ ] Add the OperatorGrid logo and brand color (#0F4C5C) where branding settings allow

## 6. Digital delivery: choose one (Stripe won't do this for you)
| | Option A: verified download (recommended) | Option B: link on the confirmation screen |
|---|---|---|
| How | After payment, Stripe redirects to `thank-you.html`. A small serverless function checks the Checkout Session with Stripe (paid, $149 product), then gives a **short-lived signed link** to the ZIP stored in **private** storage. | The Payment Link confirmation message shows an unguessable download URL. |
| Pros | Only paying customers can download. Refunded sessions can be blocked. | No code. Fastest to set up. |
| Cons | Needs a little code, a host with serverless functions (free tiers exist), a Stripe API key and a webhook secret | The link can be shared. You can't revoke it per customer. |
| Who builds it | I can build and test it in Stripe **test mode** once you provide **test-mode** keys | You paste the link |

**Either way:** the ZIP must **not** be placed in the public website folder. Keep re-download requests going to support@ (or, with Option A, the thank-you link can work again for [X] days).

## 7. Webhook (Option A only)
- [ ] Endpoint: `https://getoperatorgrid.com/.netlify/functions/stripe-webhook` (or the equivalent for your host). Event: `checkout.session.completed`, plus `charge.refunded` to block downloads after a refund.
- [ ] Store the signing secret and the API key as **host environment variables**, never in the website files or the repository.

## 8. Test everything
- [ ] Run **every** step of `06-TEST-PURCHASE-CHECKLIST.md` in test mode.

## 9. Go live (only with your explicit approval)
- [ ] Recreate or copy the product, price and Payment Link in **live mode** (test-mode objects don't work live). Re-check: $149, one-time, quantity 1, promo codes off, tax code, terms required, redirect.
- [ ] Paste the **live** Payment Link URL into `operatorgrid-site/assets/js/checkout.js` → `CHECKOUT_URL`
- [ ] Optional live smoke test: buy once with your own card, confirm delivery, then refund. Payment processing fees on a refunded live charge are usually not returned, so this costs a few dollars; it's your call.
- [ ] Switch the site from preview to live (see `operatorgrid-site/LAUNCH-CHECKLIST.md`)

### Sources (search results; re-verify)
- [Stripe Managed Payments overview](https://stripe.com/managed-payments) · [Stripe pricing](https://stripe.com/pricing)
- [Managed Payments docs](https://docs.stripe.com/payments/managed-payments) · [Eligibility](https://docs.stripe.com/payments/managed-payments/eligibility) · [Use Payment Links](https://docs.stripe.com/payments/managed-payments/use-payment-links)
- [Changelog: Managed Payments on Payment Links](https://docs.stripe.com/changelog/dahlia/2026-03-25/adds-support-for-managed-payments-on-payment-links?locale=en-GB)
- [Selecting the right Product Tax Code for Managed Payments](https://support.stripe.com/questions/selecting-the-right-product-tax-code-for-managed-payments)
- [Fulfill orders (Checkout)](https://docs.stripe.com/checkout/fulfillment) · [Payment Links post-payment](https://docs.stripe.com/payment-links/post-payment.md) · [Receipts](https://docs.stripe.com/receipts)
- Fee analyses: [checkoutpage.com](https://checkoutpage.com/blog/stripe-managed-payments) · [dodopayments.com](https://dodopayments.com/blogs/stripe-managed-payments-fees-explained) · [userjot.com](https://userjot.com/blog/stripe-managed-payments-for-saas)
