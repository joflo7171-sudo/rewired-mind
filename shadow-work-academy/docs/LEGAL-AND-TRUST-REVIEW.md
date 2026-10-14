# Trust and safety review — items for you and a professional

I am not a lawyer. The four policy pages are good-faith drafts (`site/refund.html`, `terms.html`, `privacy.html`, `disclaimer.html`) and carry `LEGAL REVIEW REQUIRED` comments. `launch-check.py` fails until those are removed.

## A. Questions for qualified counsel
1. **Refund promise** (30 days, no questions). Is it consistent with Gumroad's terms, consumer law in your target countries (e.g. EU/UK withdrawal rights for digital content), and your tax setup?
2. **Terms**: license wording, limitation of liability, governing law/venue (not specified), entity name (the pages say "Rewired Mind"; use your legal entity).
3. **Privacy policy**: required content for your audience (GDPR/UK GDPR, CCPA/CPRA, etc.), controller identity and address, retention for support email, children's wording (currently "adults, not directed to under 18").
4. **Health-adjacent positioning**: whether any wording could be read as a health claim or implied treatment. I used "educational self-reflection", "not therapy", no outcome claims.
5. **Use of the term "shadow work" / Jung reference**: disclaimer states it is "not a clinical Jungian program" and makes no scientific-validation claim.

## B. Sales-page claims audit (`site/index.html`)
| Claim | Evidence | Status |
|---|---|---|
| 6 modules; lesson, scenario, reflection, worksheet, action, recap, completion record | Tested per module (`qa.js`) | ✅ |
| 60-page printable workbook | Generated from the built PDF and tested | ✅ |
| 9 supporting resources / 16 scripts / 12-week tracker | Tested | ✅ |
| "Works offline" | Tested in offline Chromium on the extracted ZIP | ✅ (other browsers untested) |
| Answers stay on your device; nothing uploaded | Zero network requests in audit; no network APIs in shipped code | ✅ (see §C) |
| "Instant download", "secure checkout by Gumroad" | Depends on Gumroad | ❌ unverified until test purchase |
| "Refund within 30 days" | Needs your approval + Gumroad setting | ❌ |
| Free Module 1 sample | Exists at `site/downloads/module-1-free-sample.pdf` (7 pp) | ✅ |
| "Founding price" | Implies the price may rise. Keep only if you really intend to raise it; otherwise say "$197". | ⚠️ your call |
| Comparison table vs "many journals" | Worded as general ("often…"); no named competitors | ✅ low risk |
| Testimonials, user counts, credentials, results, scarcity, countdowns | None present (tested) | ✅ |
| Founder/brand section | Brand-level only | ✅ |

## C. Privacy statements vs actual behaviour
| Statement (site `privacy.html`, `index.html`, app Help) | What the code does | Verified by |
|---|---|---|
| Answers are saved in the browser's local storage on the device | `localStorage` key `swa.v1` in `app/app.js` | code read + persistence tests |
| The Academy does not upload answers; no analytics | No `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, forms, iframes, cookies, analytics or pixels in any shipped file | automated scan of the extracted ZIP |
| The Academy makes no network requests | Network audit of a full session: only `file://` requests (fonts are bundled) | Playwright request log |
| Works offline | Loads, saves, persists with network disabled | offline test |
| Data can be lost if browser data is cleared / folder moved | True; backup/restore provided and warned | backup/restore/erase tests |
| Backup file contains everything written | Full JSON of state, tested | test |
| Sales site has no analytics/pixels/third-party scripts | True today (fonts bundled) | grep + network review |

Caveats: (1) The statements describe the files as shipped. If you later add analytics, a Meta Pixel (the main Rewired Mind site has one) or an email-capture form to the sales site, update the policy first. (2) Browsers can sync or back up local storage in ways outside our control; the policy says only that *we* don't upload it. (3) Anyone with access to the device/browser profile can read the answers; this is disclosed.

## D. Content safety review (recommended)
The lessons include crisis wording ("contact local emergency services… not a substitute for professional care") in Module 1, Module 5 (safety/abuse) and the Quick-Start Guide, and every page footer says "not therapy". I recommend a licensed clinician read the full content, especially Modules 1, 4 and 5, before launch. I made no claims about efficacy or research.

## E. Brand and trademark review of "The Shadow Work Academy" (before launch, before ad spend)
**See `docs/TRADEMARK-AND-COPYRIGHT-CHECK.md`. Corrects an earlier version of this section.** A fuller search found (1) an existing business, Pete Isaia, using the exact name "The Shadow Work Academy" for paid shadow-work courses, and (2) a U.S. registration for SHADOW WORK (Reg. 1,840,946, Shadow Work Licensing, LLC) covering teaching classes and seminars in psychological self-improvement, plus pending ORIGINAL SHADOW WORK applications. Treat the name as **high risk**; get an attorney clearance and prepare a fallback name before creating the Gumroad product or spending on ads. This is not legal advice; registry data came from search summaries and must be verified at the USPTO.
