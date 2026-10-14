# Gumroad setup and test-purchase checklist

I have **no access to Gumroad** and this environment cannot reach it, so nothing below has been executed. Gumroad's menu names change; where I am unsure of an exact setting I say so. Do not publish, change price, or run a paid test until you have decided to.

## 0. Before you start
- [ ] Decide which store: the repo's quiz funnel links to `therewiredmind.gumroad.com`; a Drive doc mentions `confidencefixhub.gumroad.com`. Use the one you want this product under.
- [ ] Approve the price ($197 was the brief; see the value-for-price flag in `LAUNCH-READINESS.md`).
- [ ] Check Gumroad's current fee schedule and who handles sales tax/VAT for your buyers' regions.

## 1. Create the product (leave it **unpublished** / draft)
| Field | Value |
|---|---|
| Type | Digital product |
| Name | The Shadow Work Academy |
| Price | $197 (one-time, USD) — only after you approve |
| Summary / tagline | From self-doubt to self-trust. A six-module, self-paced shadow work program with a printable workbook. |
| File | Upload `dist/The-Shadow-Work-Academy.zip` (1.8 MB). Rebuild first if anything changed: `python3 tools/package.py` |
| Cover/thumbnail | Use `site/img/preview-dashboard.png` (a real screenshot) |
| Refund policy setting | Set to match `site/refund.html` (30-day). If Gumroad's available windows differ, change `refund.html` to match — a mismatch is a trust and legal risk. |

### Product description (copy-ready; matches the sales page)
> **The Shadow Work Academy** is a six-module, self-paced program for people who say yes too fast, criticize themselves too hard, and need approval to feel okay. It combines written lessons, real-life scenarios, guided reflection, worksheets, a real-world action step, and a recap in every module.
>
> **What you get (digital download):**
> - The interactive Academy: six modules you open in your web browser (works offline)
> - The 60-page printable Complete Academy Workbook (PDF)
> - Nine supporting resources (PDF): Quick-Start Guide, Self-Worth Reflection Exercises, Trigger & Pattern Tracker, Inner-Critic Worksheet, People-Pleasing Audit, Boundary-Setting Scripts Library (16 scripts), Values & Needs Worksheet, 12-week Weekly Reflection Tracker, Self-Trust Action Plan
>
> **Not included:** therapy or medical advice, live coaching, a community, an online login or cloud sync, or a printed book.
>
> **You need:** a phone, tablet or computer with a current browser, the ability to unzip a file, and a PDF reader. About 45–60 minutes per module.
>
> Your reflections are saved in your own browser on your own device; nothing is uploaded. This is an educational self-reflection program, not therapy. See the disclaimer and refund policy at shadowworkacademy.org.

### Receipt / delivery message (paste into the product's receipt or content text, wherever Gumroad provides it)
> Thank you! To get started: (1) Download the ZIP. (2) Unzip it (Windows: right-click → Extract All; Mac: double-click). (3) Open START-HERE.html and choose "Open the Academy". (4) Begin with Module 1. Back up your answers from the Progress page now and then — they are stored in your browser. Questions or trouble opening the files: support@rewiredmind.org.

If the product settings offer a post-purchase redirect, point it to `https://shadowworkacademy.org/thank-you.html` (the page tells buyers what to do next and does **not** contain the files). If not, rely on the receipt message above.

## 2. Replace the placeholder URLs
```
python3 tools/configure.py --checkout https://YOURSTORE.gumroad.com/l/YOURPRODUCT
python3 tools/launch-check.py        # must show no checkout placeholder
NODE_PATH=<playwright> node tools/qa.js
```
This rewrites the 7 purchase links, the structured data and the nav button, then rebuilds `dist/`.

## 3. Test-purchase checklist (record what you see — paste results back to me)
Use a method that does not charge a real customer. Options (confirm what Gumroad allows): a 100%-off offer code on the unpublished product, or a real low-cost test purchase from a second email followed by a refund (may incur fees — your call). Use a private window and a different email than the seller account.

**Checkout**
- [ ] Button on the sales page opens the *correct* product (name, $197, description, cover image).
- [ ] Price, currency, tax line and refund wording match the site (`refund.html`).
- [ ] Complete a test order.

**Confirmation and delivery**
- [ ] A receipt email arrives. Time to arrive: ____ . Lands in inbox / spam / promotions? ____
- [ ] Email contains a working download link and the instructions text.
- [ ] Download the ZIP: size ≈ 1.8 MB, name `The-Shadow-Work-Academy.zip`.
- [ ] Redirect/thank-you page (if used) loads and its wording matches what actually happened.

**Extraction and first use (do each on at least: Windows or Mac desktop, and a phone)**
- [ ] ZIP extracts with the built-in tool; folder `The-Shadow-Work-Academy` contains `START-HERE.html` and `Academy/`.
- [ ] START-HERE opens in the browser; "Open the Academy" works; the PDF link works.
- [ ] Browsers: Chrome ☐ Safari ☐ Firefox ☐ Edge ☐ iOS Safari ☐ Android Chrome ☐
- [ ] Turn off Wi-Fi: Academy still works, answers still save.
- [ ] Complete a module, mark complete, reload: progress remains.
- [ ] Progress → Download backup → Erase → Restore: answers return.
- [ ] Open every PDF (workbook + 9). Print one worksheet page.
- [ ] Note whether answers persist after closing and reopening the browser, and after moving the folder (expected: lost unless restored from backup — this is warned about).

**After**
- [ ] Refund the test order; confirm refund email and that access is revoked/handled as you expect.
- [ ] Email support@rewiredmind.org; confirm it is received and who answers.
- [ ] Only then: publish the product (your decision), deploy the site, and re-run `tools/qa.js` against the live URL.
