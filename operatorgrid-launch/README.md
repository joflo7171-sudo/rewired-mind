# OperatorGrid: launch readiness pack (internal; nothing here is published)

| File | Purpose |
|---|---|
| `01-SUPPORT-EMAIL-SETUP.md` | Requirements, DNS record types and tests for support@getoperatorgrid.com |
| `02-PRIVACY-POLICY-DRAFT.md` | Privacy Policy draft (owner and professional review) |
| `03-REFUND-POLICY-DRAFT.md` | Refund Policy draft: Option A (14-day) or Option B (technical issues only) |
| `04-TERMS-OF-SALE-DRAFT.md` | Terms of Sale draft, including the single-business license |
| `05-STRIPE-MANAGED-PAYMENTS-SETUP.md` | Account → product → price → Payment Link → delivery → go-live checklist |
| `06-TEST-PURCHASE-CHECKLIST.md` | Full test-purchase checklist (sections A–I) |

## Current state
- **Product:** v1.0.2 (DEMO + CLEAN). 56/56 internal tests pass and the buyer-ZIP audit is clean. **Not yet tested in real Excel or Google Sheets.**
- **Website:** preview only, in `operatorgrid-site/`. noindex is on, robots.txt blocks crawling, the sitemap is not submitted, checkout is inactive and the support and legal pages are placeholders.
- **Payments:** nothing created.
- **Email:** nothing created.
- **DNS:** untouched.

## Safe launch order
1. Real Excel + Google Sheets test of v1.0.2 → fix any genuine bug → re-test
2. Create the support mailbox → add its DNS records → pass every test in `01` section 5
3. Approve the refund policy option, privacy policy and terms (professional review recommended)
4. Fill the support email and approved policies into the website and READ-ME → rebuild and re-audit the ZIP
5. Choose a host. Deploy the site at getoperatorgrid.com in **pre-launch mode**: noindex on, checkout inactive. This is a publish step and needs your approval.
6. Stripe account and verification → enable Managed Payments → product, price and Payment Link **in test mode**
7. Build the delivery method (Option A) and connect it in test mode
8. Run the full test-purchase checklist in test mode
9. Recreate in live mode → paste the live link into `checkout.js` → optional owner smoke test (buy, then refund)
10. Switch to live: remove noindex and the preview bar, swap robots.txt, submit the sitemap
