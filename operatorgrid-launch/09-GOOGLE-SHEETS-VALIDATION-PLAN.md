# Google Sheets validation: results

## 0. v1.0.3 final result (2026-10-04): PASS
The real v1.0.3 workbooks were converted by Google Sheets in your Drive. I exported Google's recalculated copies and compared them cell by cell with the approved v1.0.3 build, read-only.

| Check | DEMO (`v1.0.3 - …-DEMO`) | CLEAN (`v1.0.3 - …-CLEAN`) |
|---|---|---|
| Dropdowns: definitions and covered cells | **65 / 65**, all 29,954 cells, same list source | **65 / 65**, all 29,954 cells, same list source |
| Formulas still live formulas | 62,232 / 62,232 | 62,232 / 62,232 |
| Formula results identical to the build | **62,232 / 62,232** | 62,227 / 62,232 (the 5 TODAY-driven cells; see section 1) |
| Spreadsheet error cells | **0** | **0** |
| Charts / named ranges / tab links | 4 / 25 / 84, all kept | 4 / 25 / 84, all kept |
| Filters / frozen panes / merged cells | 14 / 21 / 184, all kept | 14 / 21 / 184, all kept |
| Key values | DASHBOARD Revenue (B6) **$6,070** · Gross Margin (F6) **42.7%** · QUOTE BUILDER G16 **$522.50** | System date today (local time zone) · reporting month and year correct · dashboard blank |

**Notes:**
- Google lists 63 dropdown entries, not 65, because it merged 2 pairs of identical dropdowns. Every original cell is still covered.
- The amber "below target margin" highlight is still a known cosmetic Google limitation (section 1).
- **Still open:** the interaction tests (section 2, steps 4–6) and real Microsoft Excel testing.

---

## v1.0.2 results (2026-10-01), kept for history

**Tested:** v1.0.2 DEMO and CLEAN, converted to Google Sheets in your Drive. I read them by exporting Google's own recalculated copy, so the values below are Google's results, not cached values.

**Verdict:**
- **Calculations: PASS.**
- **Dropdowns: FAIL in v1.0.2 → fixed in v1.0.3**, confirmed on the real v1.0.3 files (section 0).
- **Interaction tests: NOT RUN.** They need cell edits, which the connector can't make.

## 1. Results on v1.0.2 as converted by Google
| Check | DEMO | CLEAN | Class |
|---|---|---|---|
| Formula results identical to the verified values | **62,232 / 62,232** | 62,227 / 62,232 | — |
| The 5 CLEAN differences | — | All are TODAY-driven. Google uses your local time zone (Sep 30) while the build used UTC (Oct 1). | Correct behavior |
| `#REF!` `#VALUE!` `#NAME?` `#DIV/0!` `#N/A` `#ERROR!` | 0 | 0 | — |
| Formulas still live formulas | 62,232 | 62,232 | — |
| 13,069 formulas stored as single-cell array formulas | Same results | Same results | Storage detail only |
| Charts | 4 / 4 | 4 / 4 | — |
| Named ranges | 25 / 25 | 25 / 25 | — |
| Internal tab links | 84 / 84 kept | 84 / 84 kept | — |
| Filters, frozen panes, merged cells | 14 / 21 / 184, all kept | Same | — |
| Conditional formatting | 68 / 73 | 68 / 73 | **Cosmetic** |
| Dropdowns | **2 / 65** | **2 / 65** | **Functional → fixed in v1.0.3** |

**DEMO key values, recalculated by Google:**
- Revenue **$6,070**
- Margin **42.7%**
- Quote **$522.50**
- All the other expected DASHBOARD, QUOTE BUILDER, MONTHLY, PROFITABILITY, RECURRING, CUSTOMERS, SCHEDULE and FOLLOW-UPS values match.

**CLEAN:**
- The system date is today, and the reporting month and year are this month and year.
- The dashboard is blank or 0.
- There are no errors.

### Cosmetic difference: 5 amber "below target margin" highlights
- **Cause:** Google Sheets doesn't allow named ranges (`TargetMargin`) in conditional-format rules, so it drops them.
- **Impact:** values are unaffected, and the QUOTE BUILDER "Margin check" text still says "Below your target margin".
- **Decision:** not changed. A workaround (INDIRECT) would touch working Excel formatting for a cosmetic gain.

### Functional problem: range dropdowns lost
- **Symptom:** 63 dropdowns disappeared, for example lead source, cleaning type, job status, payment method and the quote inputs. Only the two typed lists ("Yes,No" and "Yes,No,N/A") survived.
- **Root cause:** the builder stored range dropdowns with a leading `=`. Google drops those.
- **Proof:** two small, clearly labeled test files were uploaded, converted, checked and then moved to the Drive trash.
  - 8 variants without `=` (cross-sheet, named range, quoted sheet names with `&`, same-sheet, list) were **all kept**.
  - With the same dropdown written with and without `=`, **only the version without `=` was kept**.
- **Fix:** **v1.0.3** removes the `=`. That is the only change inside both workbooks: every formula, value, chart, format, name and link is byte-identical.
- **Re-test:**
  - 56/56 automated tests pass.
  - The schema check is valid.
  - LibreOffice keeps 65/65 dropdowns.
  - The ZIP audit is clean.
  - Delivery tests pass: 15/15 unit and 34/34 browser.

## 2. Your next step (about 10 minutes)
1. Unzip **`OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.3.zip`**.
2. Upload the DEMO and CLEAN `.xlsx` files to Drive, then open each and choose **File → Save as Google Sheets**.
3. Delete or ignore the older v1.0.2 Sheets so the copies aren't confused.
4. In the **DEMO** Sheet, make these edits (checklist items 28, 36 and 37). Use the dropdowns, which also proves they work.

   | Edit | Expected result |
   |---|---|
   | QUOTE BUILDER B9 → **Standard Clean** | G16 **$299.50** |
   | LEADS, L-0064 Sage Sterling: Stage → **Booked** | DASHBOARD Conversion **15.4%** |
   | REVENUE row 287: Payment Date 9/30/2026, Job **J-0273**, Amount **150**, Method **Cash** | Unpaid Balances **$930** |

5. In the **CLEAN** Sheet, do checklist item 43: add one STAFF name, one CUSTOMER and one PROPERTY (2,000 sq ft, 3 bd, 2 ba), then one JOB dated **today** (Standard Clean, price 200, Status Completed).
   - Expected: Auto Est. Hrs **3.42**
   - Payment Status **Unpaid**
   - DASHBOARD Revenue **$200**
6. Tell me they're ready. I'll confirm 65/65 dropdowns and all of the results above by reading the Sheets.

## 3. Still outstanding after that
- A **real Microsoft Excel** test (there is no Excel here). Use `cleaning-business-ai-growth-os/LAUNCH-KIT/EXCEL-SHEETS-TEST-CHECKLIST.md`.
