# Test purchase checklist: Cleaning Business AI Growth OS ($149)

Run it fully in **Stripe test mode** first, then repeat sections A–E once in live mode only if you approve a live smoke test.
For each item, record PASS or FAIL, the date, the device/browser, and a screenshot for any FAIL.

**Stripe test cards** (test mode only, any future expiry, any CVC, any postcode):

| Card | Behavior |
|---|---|
| `4242 4242 4242 4242` | Succeeds |
| `4000 0025 0000 3155` | Requires 3-D Secure authentication |
| `4000 0000 0000 0002` | Declined (generic) |
| `4000 0000 0000 9995` | Declined (insufficient funds) |

Confirm these on Stripe's testing page. Managed Payments test-mode behavior may differ.

---

### A. Checkout page
- [ ] A1. From getoperatorgrid.com, each purchase button (hero, Quote & Profit section, pricing card) opens the **same** checkout
- [ ] A2. Product name reads exactly "Cleaning Business AI Growth OS", with the OperatorGrid name or logo shown
- [ ] A3. Product image and description display correctly
- [ ] A4. **No** quantity selector, **no** promotion-code field, **no** crossed-out or "sale" price
- [ ] A5. The Terms of Sale checkbox or link is present, and the link opens `/terms.html`
- [ ] A6. Merchant-of-record wording (Link/Stripe) appears as expected, and matches the Terms of Sale and Privacy Policy

### B. Price
- [ ] B1. The price shows **$149.00 USD, one-time**, with no "per month" or "per year"
- [ ] B2. Tax: with a US address (e.g. a state that taxes digital goods) and a non-taxing state, the tax line matches your chosen **inclusive or exclusive** setting
- [ ] B3. With a non-US address (e.g. a UK or EU postcode), VAT behaves as expected under Managed Payments
- [ ] B4. The total charged matches the total displayed

### C. Payment success (card 4242…)
- [ ] C1. Payment completes and you land on the expected page (the thank-you page for Option A, or the confirmation message for Option B)
- [ ] C2. The payment appears in the Stripe Dashboard (test mode) as **Succeeded, $149.00**, with the correct product and customer email
- [ ] C3. 3-D Secure card (3155): the authentication challenge appears; approving it succeeds and failing it doesn't charge

### D. Customer email and receipt
- [ ] D1. A receipt email arrives at the test buyer's address within minutes (check spam too)
- [ ] D2. The receipt shows the product name, $149.00, the date, the tax line if any, and the merchant shown (Link/Stripe/OperatorGrid as configured)
- [ ] D3. The receipt is viewable or downloadable as a PDF from the link in the email
- [ ] D4. The support contact on or near the receipt is support@getoperatorgrid.com, not a personal address

### E. File delivery and ZIP download
- [ ] E1. The download is available right after payment (Option A: the thank-you page shows a working button; Option B: the confirmation message shows the link)
- [ ] E2. The downloaded file is named `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.x.zip` and is the **approved current build**. Its SHA-256 matches the hash recorded at release.
- [ ] E3. The ZIP opens on Windows and Mac. It contains 51 files in the `Cleaning-Business-AI-Growth-OS/` folder, and READ-ME-FIRST.txt shows the **real** support email.
- [ ] E4. The DEMO workbook opens in Excel (numbers visible, including in Protected View) and in Google Sheets
- [ ] E5. **Option A only:**
  - visiting `thank-you.html` with **no** or a **made-up** `session_id` gives **no** download;
  - a session for an unpaid or failed payment gives **no** download;
  - the signed link expires as configured.
- [ ] E6. **Option A only:** the same buyer can re-open their thank-you link within the allowed window and download again
- [ ] E7. The ZIP **cannot** be found at any public URL on the website (try `/Cleaning-Business-AI-Growth-OS.zip`, `/downloads/` and similar)

### F. Refund flow
- [ ] F1. Issue a **full refund** for a test payment in the Dashboard (or through the Managed Payments refund process, if it differs)
- [ ] F2. The payment shows **Refunded** and the amount is correct
- [ ] F3. The customer receives a **refund email** that matches the Refund Policy wording
- [ ] F4. **Option A only:** after the refund, the download link for that session no longer works
- [ ] F5. The Refund Policy page (`/refunds.html`) matches what actually happened (time window, method)
- [ ] F6. Note how a buyer requests a refund under Managed Payments (Link support vs your support@), and make sure the website says the same thing

### G. Failed payments
- [ ] G1. Declined card (0002): a clear error shows, **no** charge succeeds, **no** receipt is sent, **no** download is offered
- [ ] G2. Insufficient funds (9995): same as G1
- [ ] G3. After a decline, retrying with 4242 succeeds in the same session without creating a duplicate charge
- [ ] G4. Closing the checkout tab mid-payment and returning to the site: no charge, no download
- [ ] G5. **Option A only:** a failed or incomplete session can't be used on the thank-you page

### H. Mobile checkout
- [ ] H1. **iPhone, Safari:** the full purchase works, the checkout page fits the screen, and Apple Pay appears if enabled and eligible
- [ ] H2. **Android, Chrome:** the full purchase works, and Google Pay appears if enabled and eligible
- [ ] H3. The download on a phone works (on iPhone the ZIP may open in the Files app), and the instructions on the thank-you page tell buyers to open the workbooks on a computer for best results
- [ ] H4. The website's purchase buttons are easy to tap at phone width (already checked in preview at 390 px)

### I. Duplicates and edge cases
- [ ] I1. Double-clicking the pay button doesn't create two charges
- [ ] I2. A buyer who purchases twice can be refunded for the duplicate (under the Refund Policy)
- [ ] I3. The browser back button from the thank-you page doesn't re-charge

### Sign-off
| Mode | Tester | Date | Result |
|---|---|---|---|
| Test mode | | | |
| Live smoke test (optional, owner-approved) | | | |

**The $149 checkout may be switched on only after every item above is PASS in test mode and the real Excel/Google Sheets product test has passed.**
