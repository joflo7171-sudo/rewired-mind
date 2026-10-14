# The Shadow Work Academy — Handover

Everything lives in `shadow-work-academy/`. Nothing outside this folder was changed (the existing Rewired Mind site `index.html`, quiz funnel, and media are untouched).

## Stage 1 finding: Cash Command OS could not be inspected
`cashcommandos.com` does not resolve from this build environment (DNS failure; outbound traffic is proxied) and the repo contains only the Rewired Mind site, so **no Cash Command OS source, page, or checkout setup was seen.** The structure, UX and delivery model here follow your brief, not the reference. The only existing pattern found and reused: Rewired Mind sells through Gumroad (`therewiredmind.gumroad.com`) and uses `support@rewiredmind.org`.
To close the gap, send either the Cash Command OS project files, or page screenshots/exported HTML, plus how it delivers files today.

## What was built
| Path | What |
|---|---|
| `content/module1-6.js`, `content/resources.js` | Single source of truth for all course text, worksheets, scripts, resource definitions (~7,000 words) |
| `app/` | Interactive Academy (static HTML/JS/CSS, no server): welcome, dashboard, 6 modules, worksheets, completion + insight capture, progress, resource library, backup/restore/erase, help & privacy |
| `app/print.html` + `tools/build-pdfs.js` | Renders PDFs from the same content |
| `resources/` | Complete Workbook (63 pp) + 9 PDF resources |
| `site/` | Sales site: `index.html`, refund, terms, privacy, disclaimer, thank-you, sitemap, robots, free Module 1 sample PDF, real screenshots |
| `package/START-HERE.html` | Customer start page inside the ZIP |
| `dist/The-Shadow-Work-Academy.zip` | **The customer deliverable** (upload to Gumroad) |
| `dist/site/` | Deployable copy of the sales site |

Rebuild: `node tools/build-pdfs.js && node tools/screenshots.js && python3 tools/package.py` (needs Node + Playwright with Chromium, Python 3, poppler for screenshots).

## Key decisions
- **Formats:** interactive HTML (works offline) + PDF. Not Excel/Sheets: the product is reflection and reading, not calculation.
- **Privacy model:** answers are stored in the customer's browser (localStorage) on their device. The Academy files contain no analytics, forms or upload code (verified by reading the code). Google Fonts load when online; this is disclosed. A backup/restore file is provided because browser data can be cleared.
- **Delivery:** Gumroad ZIP download. The paid content is deliberately **not** hosted online, because a public static URL cannot be access-controlled. A hosted members area would need a real auth platform (later option).
- **Checkout:** Gumroad, kept separate from your other products.

## Testing done (automated, headless Chromium)
177 checks, 176 pass. Covered: unzipped package opened via `file://`; all 6 modules have all 7 sections; answers persist across reload; completion + dashboard progress; backup file contents; restore; erase; 10 PDF links resolve; tracker/weekly pages; no console errors; no horizontal overflow at 375px (app and site); every internal site link/anchor; one H1 per page; image alt text. The one reported failure is a test artifact (lazy-loaded images aren't loaded in that check); I confirmed separately that all 7 site images load after scrolling.

**Not tested / not possible here:** the live Gumroad checkout, purchase email, ZIP download from Gumroad, real Safari/iOS/Firefox rendering, screen-reader testing, and a formal WCAG audit. Payment and automated delivery are **not verified**.

## What you must do before launch
1. **Create the Gumroad product** ($197), upload `dist/The-Shadow-Work-Academy.zip`, set the description to match the site, set the receipt/redirect to the thank-you page, and enable a refund contact. Then replace the placeholder URL `https://therewiredmind.gumroad.com/l/shadow-work-academy` throughout `site/*.html` (`grep -r gumroad site/`) and re-run `tools/package.py`.
2. **Make a test purchase** (Gumroad test mode / 100% coupon): confirm the email, download, unzip, open START-HERE.html, and the receipt wording.
3. **Legal approval.** Refund (30 days is my proposal), terms, privacy and disclaimer are drafts, flagged with comments in the HTML. Have a lawyer review for your jurisdiction. Confirm tax/VAT handling.
4. **Founder section:** I used only brand-level information. Add your name, story, and photo if you want a personal intro; I invented no credentials.
5. **Hosting and domain:** decide where the site lives (I assumed `rewiredmind.org/shadow-work-academy/` for canonical/sitemap URLs; change if not). Do not change DNS until you decide. Add Meta Pixel/analytics only if you want them, and update the privacy policy when you do.
6. **Review the content yourself**, especially safety wording, and consider having a licensed clinician review before launch. I made no scientific-efficacy claims, testimonials, or user counts.
7. Pricing: $197 is untested. Consider a lower entry offer or a pre-launch to validate demand.

## Known limitations
- No cross-device sync; backup file is the transfer method.
- PDF fields are blank write-in boxes, not fillable form fields (the online versions are the editable form).
- Fonts require internet for the intended look; offline fallback is Georgia/system sans.
