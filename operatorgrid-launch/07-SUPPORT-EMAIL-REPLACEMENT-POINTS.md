# support@getoperatorgrid.com: exact replacement points (PREPARED, NOT APPLIED)

**Apply only after every test in `01-SUPPORT-EMAIL-SETUP.md` section 5 passes.** Until then, all of these stay as placeholders.

## A. Buyer ZIP (requires a rebuild + re-audit → new ZIP version)
| File (inside ZIP) | Current text | Replace with |
|---|---|---|
| `Cleaning-Business-AI-Growth-OS/READ-ME-FIRST.txt`, last line | `Support: [your support email]` | `Support: support@getoperatorgrid.com` |

- **Rebuild procedure:**
  1. Change only READ-ME-FIRST.txt; the workbooks stay byte-identical.
  2. Bump the version to **v1.0.3** in the READ-ME title line and the ZIP filename.
  3. Run `audit_zip.py` (it must report 0 problems) and record the new SHA-256.
  4. Copy the new ZIP into `operatorgrid-site/private/`.
  5. Set `PRODUCT_ZIP_NAME` on the host.
  6. Update `LAUNCH-PLAN.md` and the test checklists to the new filename.
- The audit script currently flags any `support@getoperatorgrid` address as a problem, as a safety catch. Relax that rule in the same change, and only once the mailbox has been tested.

## B. Website (`operatorgrid-site/public/`)
| File | Location | Current placeholder |
|---|---|---|
| `index.html` | FAQ → "How do I get support?" | `[Support email added after the branded mailbox is set up and tested.]` |
| `index.html` | Support section (`#support`), "Contact us at …" | `[support email, added once the branded mailbox is set up and tested]` |
| `thank-you.html` | Error panel, "Need help? Contact …" | `[support email, added once the branded mailbox is set up and tested]` |
| `terms.html` | Contact section, once the approved Terms replace the placeholder page | `[support email]` |
| `privacy.html` | Sections 5 and 10, once the approved policy replaces the placeholder page | `[support email]` |
| `refunds.html` | Option A or B text, once approved | `[support email]` |

- Use a `mailto:support@getoperatorgrid.com` link in the FAQ, the Support section and the thank-you page.
- Remove the `.placeholder` styling from those spots.
- Optional, for structured data: add `"email": "support@getoperatorgrid.com"` to the Organization entry in `index.html`.

## C. Policy drafts (`operatorgrid-launch/`)
| File | Placeholders |
|---|---|
| `02-PRIVACY-POLICY-DRAFT.md` | sections 5 and 10 |
| `03-REFUND-POLICY-DRAFT.md` | the option you choose (A or B) |
| `04-TERMS-OF-SALE-DRAFT.md` | sections 3 and 10 |

## D. Outside the repository (you)
- Stripe → Settings → Public details → **Support email** = support@getoperatorgrid.com
- Stripe customer-email settings, if a reply-to address is offered

## E. After applying
- Re-run the website QA: no `[support` text left, and every `mailto:` link works.
- Re-run both delivery test suites against the new ZIP name (15 unit tests + 34 browser checks).
- Send one test message through each `mailto:` link.
