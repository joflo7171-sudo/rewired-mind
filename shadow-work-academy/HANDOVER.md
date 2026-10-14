# The Shadow Work Academy — handover

Everything is in `shadow-work-academy/`. The existing Rewired Mind site, quiz funnel and media were not modified (`git diff` shows no change outside this folder). Nothing has been deployed, published, purchased, or changed in DNS or Netlify.

**Status: built and tested; not launch-ready.** Detail: `docs/LAUNCH-READINESS.md`.

## What exists
| Path | What |
|---|---|
| `content/` | Course text for 6 modules, worksheets, scripts, resource definitions (single source of truth) |
| `app/` | Interactive Academy (static HTML/JS/CSS; works offline; answers kept in the browser; zero network requests) |
| `fonts/` | Bundled Cormorant Garamond + Inter (SIL OFL, licenses included) |
| `resources/` | 60-page workbook + 9 resource PDFs |
| `site/` | Sales site for **https://shadowworkacademy.org/** (+ legal pages, thank-you, 404, `_headers`, sitemap, robots, free Module 1 sample) |
| `dist/The-Shadow-Work-Academy.zip` | **Customer deliverable** (upload to Gumroad) |
| `dist/site/` | Deployable site build |
| `tools/` | `package.py` (build), `qa.js` (tests the extracted ZIP and site), `pdfcheck.py`, `launch-check.py` (fails until blockers are cleared), `configure.py` (set checkout URL / site domain), `build-pdfs.js`, `screenshots.js` |
| `docs/` | `LAUNCH-READINESS.md`, `DOMAIN-SETUP.md`, `GUMROAD-SETUP-AND-TEST-PURCHASE.md`, `LEGAL-AND-TRUST-REVIEW.md`, `REFERENCE-COMPARISON.md`, `LAUNCH-EXPERIMENT.md` |

Rebuild: `NODE_PATH=<playwright> node tools/build-pdfs.js && python3 tools/package.py`. Test: `NODE_PATH=<playwright> AXE=<axe.min.js> node tools/qa.js`.

## Latest test results
`tools/qa.js` (extracted customer ZIP + built site): **281 passed, 0 failed** (repeated runs). `tools/pdfcheck.py`: all passed. `tools/launch-check.py`: **fails on purpose** (checkout placeholder, legal markers). Not tested: live checkout, purchase email, Gumroad download, Safari/iOS/Firefox, Windows/Mac/phone unzip, Acrobat/Preview.

## Domain: https://shadowworkacademy.org/ (primary)
Done in code: canonical, `og:url`, `og:image`, structured data, sitemap, robots and internal links use the new domain. Old `rewiredmind.org/shadow-work-academy` references: **none** in the production build. Intentional `rewiredmind.org` uses only: the "A product of Rewired Mind" link and `support@rewiredmind.org`. `launch-check.py` enforces all of this and that the checkout URL is **never on the website domain** (it must be a Gumroad URL; paid files are never hosted on the site).

Verified: the domain is **not connected** to any of your 10 Netlify sites (read-only check), and **I cannot tell whether you control its DNS** (this environment cannot reach it; no registrar access).

Steps (full detail and sources in `docs/DOMAIN-SETUP.md`; all need your approval and none have been done):
1. Confirm registrar, who holds the nameservers, existing records (MX, parked A/AAAA, CAA), auto-renew/lock.
2. Create a **new Netlify project** (e.g. `shadow-work-academy`), deploy `dist/site/` only after the Gumroad URL and legal approvals are in. Keep `rewiredmind-home`/quiz untouched.
3. Add `shadowworkacademy.org` (apex primary) and `www` (redirect to apex).
4. DNS, either Netlify DNS (change nameservers) or external DNS: apex ALIAS/ANAME → `apex-loadbalancer.netlify.com` (or A `75.2.60.5` if no ALIAS support), `www` CNAME → `<project>.netlify.app`; delete conflicting parked/AAAA records; keep MX.
5. HTTPS: Netlify issues a free Let's Encrypt certificate after DNS verifies; enable Force HTTPS; allow `letsencrypt.org` if a CAA record exists; add HSTS only after both hostnames work.
6. Run the verification checklist in `docs/DOMAIN-SETUP.md` §6; rollback is §7.

## Brand/trademark flag: HIGH RISK, decide before launch
Full detail: `docs/TRADEMARK-AND-COPYRIGHT-CHECK.md` (not legal advice; registry facts come from search summaries, verify at the USPTO).
* **Existing use of the exact name:** Pete Isaia operates "The Shadow Work Academy" (`peteisaia.com/academy`, `isaiacoaching.com/academy`), selling shadow-work courses online. Likelihood of confusion looks high.
* **Registered mark:** SHADOW WORK, U.S. Reg. 1,840,946 (1994, renewed), owner Shadow Work Licensing, LLC, for teaching classes and seminars in psychological self-improvement; pending ORIGINAL SHADOW WORK applications (2024). Several other "shadow work" filings exist, so the term is crowded and contested.
* **Copyright:** the name is not copyrightable; the course text is original (spot searches found no matching text), but AI-drafted text may have weaker copyright protection, so add human authorship and discuss with counsel.
* **Recommendation:** do not create the Gumroad product, deploy the domain, or spend on ads until an attorney clears or replaces the name. A rename is cheap now; I can prepare a rename script when you choose a name. The domain `shadowworkacademy.org` may itself need to be dropped.

## Remaining launch blockers (priority order)
**P0**
1. Confirm which Gumroad store (`therewiredmind` in the quiz funnel vs `confidencefixhub` in a Drive doc), create the product **unpublished**, then `python3 tools/configure.py --checkout <URL>`. Placeholder currently `https://checkout.invalid/shadow-work-academy` in `site/index.html`, `404.html`, `disclaimer.html`, `refund.html`, `terms.html`, `privacy.html`, `thank-you.html`.
2. End-to-end test purchase: email, download, unzip, open, refund (`docs/GUMROAD-SETUP-AND-TEST-PURCHASE.md`). Nothing about checkout/delivery is verified until then.
3. Legal review of refund/terms/privacy/disclaimer and your approval of the 30-day refund; then remove the `LEGAL REVIEW REQUIRED` comments.
4. **Brand/trademark clearance: elevated to the top blocker** (above). Everything else is wasted if the name changes.
5. Domain ownership/DNS confirmation and hosting (above).
6. Price decision: lessons total ~2,950 words (~6,000 words with all course text); $197 is a hard sell to cold traffic and the only Rewired Mind price I can see is $9. Test $47–$97 first or add depth (`docs/LAUNCH-EXPERIMENT.md`).

**P1**
7. Manual browser/device pass (Safari, iOS, Firefox; Windows/Mac/phone unzip).
8. Clinician read of the course content and safety wording.
9. Analytics decision (none today; adding any needs approval and a privacy-policy update).
10. Founder/brand section (brand-level only today).
11. Cash Command OS sales-page comparison: the reference is your Netlify project `cash-command-os` (`cashcommandos.com`); download its deploy or share the source/screenshots (`docs/REFERENCE-COMPARISON.md`).

## Actions only you can take
Approve/perform: Gumroad product + test purchase; legal and trademark review; domain/DNS confirmation and any DNS change; Netlify project creation and first deploy; price decision; analytics decision; publishing.
