# Launch readiness — The Shadow Work Academy

Status as of 2026-10-14. **Not launch-ready.** The product and package are tested; checkout, delivery, hosting and legal approval are not done and need you.

Legend: ✅ verified by test in this environment · ⚠️ partly verified · ❌ not verified (needs your account or manual action).

## 1. Customer-journey audit

| # | Step | Status | What was actually checked / what is missing |
|---|---|---|---|
| 1 | Land on sales page | ⚠️ | Rendered locally from `dist/site` in Chromium at 1280 px and 375 px: one H1, no horizontal overflow, all images load, axe-core finds no serious/critical accessibility violations. ❌ Not hosted anywhere yet, so real load speed, DNS/SSL and search indexing are untested. |
| 2 | Understand product and contents | ✅ (copy) | Claims were cross-checked against the build by test: workbook page count (60), 16 scripts, 9 supporting resources, 12-week tracker, $197 price, 6 modules. Subjective clarity needs your own read. |
| 3 | Click purchase button | ❌ | All purchase buttons point to `https://checkout.invalid/shadow-work-academy` (a deliberately non-working placeholder). No Gumroad product exists yet. |
| 4 | Complete a test purchase | ❌ | Blocked. I have no Gumroad access and this environment cannot reach gumroad.com. See `docs/GUMROAD-SETUP-AND-TEST-PURCHASE.md`. |
| 5 | Receive confirmation email | ❌ | Unknown until step 4. The thank-you page wording assumes Gumroad emails the download link; confirm in the test. |
| 6 | Download and extract ZIP | ⚠️ | The real ZIP (`dist/The-Shadow-Work-Academy.zip`, 1.8 MB) extracts cleanly with `unzip` on Linux, contains exactly the expected 27 files, no dev files. ❌ Windows Explorer, macOS Archive Utility, iOS Files and Android extraction not tested. |
| 7 | Open the Academy offline | ✅/⚠️ | Extracted copy, `file://`, Chromium **offline mode**: loads, saves, persists after reload, resources render. Network audit: the Academy makes **zero** network requests (fonts are now bundled). ❌ Safari, iOS Safari, Firefox, Edge not tested; `localStorage` under `file://` behaves differently by browser. |
| 8 | Access all PDFs and resources | ✅/⚠️ | All 10 PDFs open from the library links, fonts embedded, no blank pages, no ink in margins, every one of 256 content text blocks present in the workbook, contact sheets of all 60 pages reviewed by eye. ❌ Not opened in Acrobat/Preview/phone readers. |

## 2. Test results (final run)

* `node tools/qa.js` against the **extracted customer ZIP** and `dist/site`: **281 passed, 0 failed, 0 warnings.**
* `python3 tools/pdfcheck.py`: **all passed** (10 PDFs, 60-page workbook).
* `python3 tools/launch-check.py`: **fails on purpose** until the placeholder checkout URL is replaced and legal markers are removed.

### The earlier "176 / 177"
The single failure was a **test artifact, not a product defect**: the check asked every image to be loaded, but images below the fold use `loading="lazy"` and had not been scrolled into view. The new suite scrolls first. Re-running the full suite after fixes surfaced six *different* issues in the stricter version of the tests; their causes:
1. "No network/tracking APIs" — false positive: the word "analytics" in the privacy copy ("does not include any analytics"). Regex tightened.
2. "No scarcity/guarantee language" — false positive: "secure checkout" matched "cure". Fixed with a word boundary.
3. Lesson length — my threshold (450 words) was arbitrary. Real lesson lengths: M1 645, M2 520, M3 480, M4 443, M5 437, M6 427 words. Threshold now 400 (not a stub). **The content-depth question is real; see §4.**
4. **Keyboard focus — a genuine bug, now fixed:** on first page load the app moved focus into the content area, so the first Tab skipped the skip-link and navigation. Focus now moves only after in-app navigation.
Also fixed during review (found by looking at the PDFs, which automated checks missed): weekly-tracker cards split across pages, a leftover disclosure triangle in the PDF, an almost-empty "Resource Library" divider page, an orphaned table heading, and the sales page claiming 63 pages when the workbook is 60 (page-count claims are now generated from the built PDF and tested).

## 3. Changes made in this pass
* **Visual polish pass** (sales site only, content and claims unchanged): layered hero with real screenshots, refined type/cards/pricing, reveal-on-scroll that is reduced-motion and print safe, mobile header fix. Added `site/_headers` (strict CSP, no third parties) and `site/404.html` for hosting.
* Added short, clearly-labelled fictional **worked examples** for the Module 1, 3 and 5 worksheets (the reference product ships sample data; this is the equivalent onboarding aid). Also in the PDF workbook.
* Sales page: "at a glance" strip, **What you need to get started**, **What is not included**, softened competitor comparison ("many… often…"), no unsupported claims.
* **Bundled the fonts** (SIL OFL licensed, licenses included in `fonts/`). Result: no third-party request at all from the Academy; offline look matches online; privacy copy simplified and now accurate.
* START-HERE and in-app Help warn: don't move/rename the folder after starting (browsers key saved answers to the file location); back up first.
* Domain: canonical, sitemap, robots and OG URLs now use `https://shadowworkacademy.org/` (config only; nothing deployed, no DNS touched).
* New tools: `tools/qa.js`, `tools/pdfcheck.py`, `tools/launch-check.py`, `tools/configure.py`.

## 4. Prioritised launch blockers

**P0 — cannot launch without these**
1. **Create the Gumroad product** and replace the placeholder URL. Files: `site/index.html` (7 links + JSON-LD), `site/refund.html`, `site/terms.html`, `site/privacy.html`, `site/disclaimer.html`, `site/thank-you.html` (nav button). Command: `python3 tools/configure.py --checkout <URL>`.
2. **Which Gumroad store?** The repo's quiz uses `therewiredmind.gumroad.com`; your Drive doc "Rewired Mind — Gumroad Sales Copy" says `confidencefixhub.gumroad.com`. I can't tell which is current. Confirm before creating the product.
3. **End-to-end test purchase** (checklist in `docs/GUMROAD-SETUP-AND-TEST-PURCHASE.md`). Nothing about checkout, email or delivery is verified until this is done.
4. **Legal review** of refund, terms, privacy, disclaimer (`docs/LEGAL-AND-TRUST-REVIEW.md`), including your approval of the 30-day refund promise. Then remove the `LEGAL REVIEW REQUIRED` comments.
5. **Connect the domain and host the site.** Verified: `shadowworkacademy.org` is **not** connected to any of your 10 Netlify sites, and I cannot check who controls its DNS. Follow `docs/DOMAIN-SETUP.md` (new Netlify project, DNS records, HTTPS). I did not deploy or touch DNS.
5b. **Brand/trademark review of "The Shadow Work Academy"** before launch or ad spend (`docs/LEGAL-AND-TRUST-REVIEW.md` §E). I could not find the existing use you mentioned; please send the link.
6. **Price decision** (see below). Not a blocker to *building*, a blocker to *launching sensibly*.

**P1 — should be done before driving traffic**
7. Manual cross-browser/device pass (Safari, iOS, Firefox, Windows/Mac unzip). Checklist is in the Gumroad doc.
8. Professional (ideally clinician) read of the course content and safety wording.
9. Decide on measurement (the site has **no analytics**; see `docs/LAUNCH-EXPERIMENT.md`). Adding any requires your approval and a privacy-policy update.
10. Founder/brand section: currently brand-level only.
11. Cash Command OS **sales page** comparison (not accessible; see `docs/REFERENCE-COMPARISON.md`).

**P2 — nice to have**
12. A "welcome email" in Gumroad with the three start steps; a version number in the ZIP name for support.
13. Print stylesheet for the sales legal pages; per-module audio/video (see price discussion).

### Honest value-for-price flag ($197)
Lesson text totals about **2,950 words**; the whole course including scenarios, reflections, worksheets and resources is roughly 6,000 words plus the printable workbook, trackers and 16 scripts. It is clean and useful, but a self-guided text/PDF program on a topic with many free alternatives will be a hard sell at $197 to cold traffic. The one Rewired Mind price visible in your Drive sales-copy doc is $9, so $197 is a very large step for your existing audience. Recommendation: validate at **$47–$97** first (see experiment), or add depth (audio walk-throughs, longer lessons, more worked examples) before pushing $197. I have not changed the price.

## 5. Actions only you can take
1. Confirm the Gumroad store; create the product at the price you approve; upload the ZIP; paste the copy from the Gumroad doc.
2. Run the test purchase and report what the email and download actually look like.
3. Approve/obtain legal review; approve the refund promise.
4. Point `shadowworkacademy.org` at hosting and approve a deploy (I can prepare and, with your approval, run a deploy through Netlify if you want that host).
5. Decide on price and the launch experiment; decide on analytics.
6. Send the Cash Command OS sales-page files/screenshots if you want that comparison.
