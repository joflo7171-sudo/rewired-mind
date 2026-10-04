# QA Report — Cleaning Business AI Growth OS

**Date:** 2026-10-01 · **Build:** v1.0 (unpublished) · **Result: 53 of 53 automated tests passed, 0 failed.**

## How testing was done

- **Calculation engine:** each workbook copy was fully recalculated in LibreOffice Calc 24.2 (headless), then every formula cell was scanned for errors (`#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`).
- **Independent verification:** the test script (`cleaning-business-ai-growth-os-build/qa.py`) rebuilds the expected numbers **in Python from the raw sample data**, without using the spreadsheet formulas. It then compares those numbers with what the workbook calculated: every job's hours, costs, profit, margin and payment status, monthly totals, every dashboard tile, CRM statuses, recurring due dates and the schedule.
- **Scenario tests:** copies of the DEMO were edited the way a user would edit them (changing a lead's stage, adding a customer, property, job and payment in the next empty rows, running four different quotes, deleting all sample data). Each copy was then recalculated and checked again.
- **Visual checks:** the sheets, guides, forms and marketing templates were rendered to PDF/PNG and inspected page by page.
- **Spelling:** all text in the workbook (1,074 distinct words) and in every PDF was checked with `aspell` (en). The only words flagged were legitimate terms (walkthrough, lockbox, MINIFS, Airbnb, ChatGPT, etc.).

| Item | DEMO | CLEAN |
|---|---|---|
| Formulas | 62,232 | 62,229 |
| Formula errors after recalculation | 0 | 0 |
| Tabs | 23 (22 modules + QC CHECKLISTS) | 23 |
| Dropdown rules | 65 | 65 |
| Internal navigation links | 84 | 84 |
| Charts | 4 | 4 |

## Automated test results

| # | Test | Result |
|---|---|---|
| 1 | DEMO recalculates with zero formula errors | ✅ PASS |
| 2 | CLEAN (blank state) recalculates with zero formula errors | ✅ PASS |
| 3 | All 22 modules present as tabs (+QC CHECKLISTS) | ✅ PASS |
| 4 | All 84 internal navigation links point to existing tabs | ✅ PASS |
| 5 | 65 dropdown rules reference valid lists | ✅ PASS |
| 6 | Key columns have dropdowns (stage, status, customer, service, worker, etc.) | ✅ PASS |
| 7 | Filters enabled on every log table | ✅ PASS |
| 8 | Charts present on DASHBOARD (2), MONTHLY (1), PROFITABILITY (1) | ✅ PASS |
| 9 | Automatic-column formulas are identical (row-relative) from first to last row | ✅ PASS |
| 10 | JOBS: hours, labor, supplies, vehicle, fees, gross profit, margin, paid, balance, payment status match independent model (307 jobs) | ✅ PASS |
| 11 | JOBS: empty rows show blanks (no zeros/errors) | ✅ PASS |
| 12 | MONTHLY: revenue and jobs completed per month match independent totals | ✅ PASS |
| 13 | MONTHLY: leads and booked leads per month match | ✅ PASS |
| 14 | MONTHLY: overhead uses only categories flagged as overhead (Sep) | ✅ PASS |
| 15 | MONTHLY: gross profit = revenue − labor − supplies − vehicle − fees | ✅ PASS |
| 16 | MONTHLY: operating profit = gross profit − overhead | ✅ PASS |
| 17 | DASHBOARD revenue tile = MONTHLY reporting-month revenue | ✅ PASS |
| 18 | DASHBOARD jobs-completed tile = September completed jobs | ✅ PASS |
| 19 | DASHBOARD conversion rate = booked ÷ new leads (reporting month) | ✅ PASS |
| 20 | DASHBOARD average quote | ✅ PASS |
| 21 | DASHBOARD unpaid balance tile = sum of completed-job balances | ✅ PASS |
| 22 | DASHBOARD jobs next 7 days | ✅ PASS |
| 23 | DASHBOARD active recurring plans | ✅ PASS |
| 24 | DASHBOARD recurring monthly value | ✅ PASS |
| 25 | DASHBOARD follow-ups due = overdue/due-today leads + open log items | ✅ PASS |
| 26 | DASHBOARD pipeline-by-stage counts match leads | ✅ PASS |
| 27 | LEADS: booking outcome and follow-up status correct for every lead | ✅ PASS |
| 28 | LEADS: booked lead not in CUSTOMERS is flagged 'Add to CUSTOMERS' | ✅ PASS |
| 29 | RECURRING: visits completed, next due date and booking status correct for every plan | ✅ PASS |
| 30 | SCHEDULE: overdue recurring plan appears in 'needs booking' list | ✅ PASS |
| 31 | SCHEDULE: each day lists exactly that day's jobs in start-time order, with correct daily counts | ✅ PASS |
| 32 | QUOTE BUILDER demo: estimated hours 7.50 | ✅ PASS |
| 33 | QUOTE BUILDER demo: price before tax $522.50 | ✅ PASS |
| 34 | QUOTE BUILDER demo: direct costs $283.37 / gross profit $239.13 | ✅ PASS |
| 35 | QUOTE BUILDER demo: overhead share = 9.25 h × $5 = $46.25; profit after overhead $192.88 | ✅ PASS |
| 36 | QUOTE BUILDER demo: break-even $276.23 and target-margin price $569.47 | ✅ PASS |
| 37 | QUOTE scenario: Standard weekly, 1,600 sq ft, light condition, 1 worker, 15% tax, cash | ✅ PASS |
| 38 | QUOTE scenario: Commercial, 6,000 sq ft, 4 restrooms, heavy, overrides (hours 5, rate $60), $25 discount | ✅ PASS |
| 39 | QUOTE scenario: Move-out, very heavy, 2 add-ons x2, biweekly frequency (discount applies to base only) | ✅ PASS |
| 40 | QUOTE scenario: Tiny job hits minimum price ($120 floor) | ✅ PASS |
| 41 | Scenario recalculates with zero errors | ✅ PASS |
| 42 | CRM: changing a lead's Stage to Booked flips outcome to 'Booked' and stops follow-up | ✅ PASS |
| 43 | CRM: dashboard pipeline/booked counts update after stage change | ✅ PASS |
| 44 | Added rows: new job flows to dashboard revenue (+$200) and jobs completed (+1) | ✅ PASS |
| 45 | Added rows: new job gets auto estimate from new property (2,000 sq ft 3/2 standard = 3.42 h), partial payment status, balance $50 | ✅ PASS |
| 46 | Added rows: new customer shows 1 completed job, $200 lifetime revenue, 'Collect balance' action | ✅ PASS |
| 47 | Added rows: unpaid job appears in FOLLOW-UPS unpaid list | ✅ PASS |
| 48 | Added rows: new job appears on SCHEDULE for Wednesday Sep 30 | ✅ PASS |
| 49 | Sample-data removal: clearing all white input columns leaves zero formula errors | ✅ PASS |
| 50 | Sample-data removal: every dashboard tile shows 0 or blank | ✅ PASS |
| 51 | CLEAN file: every dashboard tile shows 0 or blank | ✅ PASS |
| 52 | CLEAN file contains no sample records in any log | ✅ PASS |
| 53 | CLEAN file: as-of date and reporting month blank (uses today) | ✅ PASS |

### Coverage against the brief

| Brief asked to test | Covered by tests |
|---|---|
| Formulas | 1–2, 9–16 |
| Dropdowns | 5–6 |
| Filters | 7 |
| Quote calculations | 32–40 |
| Gross profit calculations / margins | 10, 15–16, 32–40 |
| CRM status changes | 27–28, 42–43 |
| Dashboard totals | 17–26 |
| Recurring jobs | 23–24, 29–30 |
| Schedules | 30–31, 48 |
| Charts | 8 (presence and valid references), plus visual render |
| Blank states | 11, 49–53 |
| Added rows | 44–48 |
| Sample-data removal | 49–52 |
| Links between sections | 4, 10, 44–48 (data flows between sheets) |

*Test numbers refer to the table above.*

## Issues found during testing and fixed

| Issue | Fix |
|---|---|
| The LibreOffice install in the build environment was missing Calc and Writer, so recalculation hung. | Installed the free Calc, Writer and Impress packages. Recalculation now takes about 14 seconds for the full DEMO. |
| The "vs last month" caption showed "-0%". | Changed the number format to show "0%". |
| The navigation arrow glyph (▶) rendered as an emoji box in some apps. | Replaced it with plain text arrows (→ ←). |
| The demo data didn't show an overdue recurring visit. | Adjusted one sample plan so the "needs booking" alert can be seen. |
| Column widths in the Word forms were ignored when converting to PDF. | Fixed the table grid widths. |
| Guide headings sometimes ended up alone at the bottom of a page. | Headings now stay with the content that follows. |
| The quote engine had no overhead allocation (competitor gap). | Added an optional overhead-per-labor-hour setting and a "profit after overhead share" line (test 35). |
| Three early quote-test failures | Caused by the test script itself (leftover demo add-ons, and rounding differences between Python and Excel). The workbook was correct. The tests were fixed and use a 5¢ tolerance. |

## Known limitations (not defects, but disclose or fix before launch)

1. **Not yet opened in real Microsoft Excel or Google Sheets.** All calculation testing used LibreOffice's engine. The functions used (SUMIFS, COUNTIFS, INDEX/MATCH, IFERROR, EDATE, EOMONTH, MINIFS/MAXIFS with the `_xlfn` prefix) are standard in Excel 2019+/365 and Google Sheets, but **open both files in Excel and in Google Sheets before selling** (about 20 minutes). → Recommended pre-launch step.
2. **Requires Excel 2019 or newer** (MINIFS/MAXIFS). Excel 2016 will show `#NAME?` in the First/Last Job and Next Visit columns. This is documented in the guide.
3. **Tab links on START HERE and the DASHBOARD don't work in Google Sheets** (Google uses a different link format). Users can click the sheet tabs instead. This is documented.
4. **No cached values in the delivered files.** The workbook calculates when it is opened, so a file *preview* (email attachment preview, Mac Quick Look) shows empty cells until the file is opened in Excel or Google Sheets.
5. **The SCHEDULE shows up to 10 jobs per day.** More than that still lives in JOBS.
6. **Multi-person jobs** use the lead worker's pay rate for all labor hours (approximation, documented).
7. **Conversion rate is cohort-based** (leads added in the month ÷ those that eventually booked), so the current month always looks lower until those leads close.
8. **Capacity:** about 1,500 jobs/payments/trips (roughly 4–5 years for a 1–5 person business). The guide explains how to extend it.
9. **Sorting:** the filter buttons are always safe. Sorting part of a table (not the whole table) can scramble rows, as in any spreadsheet. This is documented.
10. **No video walkthrough yet.** Competing premium products rely on video onboarding (see PRICING-VALIDATION.md).

## v1.0.1 re-test (2026-10-01): OperatorGrid cleanup
- **Metadata:** every Word, PowerPoint and Excel file and every PDF now lists **OperatorGrid** as author/creator (PDF producer too). The generator fingerprints are removed: python-docx, python-pptx, Openpyxl, "Steve Canny", ReportLab, LibreOffice and Microsoft-template application names. Template leftovers are removed too: 7 Apple printer-settings parts and 22 template thumbnails.
- **Functionality unchanged:** the JOBS worksheet XML is byte-identical before and after cleaning, and the full suite re-ran on the cleaned workbooks: **53/53 passed, 0 formula errors**.
- **Guide wording:** the AI-assistant brand examples are replaced with "These workflows can be used with most general-purpose AI assistants."
- **Buyer ZIP audit** (`cleaning-business-ai-growth-os-build/audit_zip.py`) covered 24 Office files (618 internal parts), 25 PDFs (62 pages) and READ-ME-FIRST.txt. It checked:
  - forbidden brand, tool and private terms
  - emails (only `@example.com`) and URLs (only standard document-schema namespaces)
  - phone numbers (only the fictional 555 range)
  - external relationships and links, macros, data connections, OLE/embedded objects and ActiveX
  - attached templates and external formula references
  - PDF JavaScript, launch actions, URI links, embedded files and XMP metadata

  **Result: 0 problems.** The same audit run on the old v1.0 ZIP reports 291 problems, which confirms the checks work.
- Every file in the rebuilt ZIP opens in its native library, and sample conversions succeed.
- **Still outstanding:** testing in real Microsoft Excel and Google Sheets (see `LAUNCH-KIT/EXCEL-SHEETS-TEST-CHECKLIST.md`).

## v1.0.2 (2026-10-01): pre-test hardening
- **Bug found and fixed (CLEAN workbook only):** SETTINGS!B14 (AsOf), B16 (ReportMonth) and B17 (ReportYear) had no formulas in the CLEAN file. The build script defined them only for the DEMO.
  - **Effect:** the system date read as zero, so the dashboard showed "January 1900", jobs dated today didn't count in the reporting month, and overdue follow-up flags never triggered.
  - **Fix:** the formulas are now written to both files (`build_workbook.py`, settings writer).
  - **Scope of change:** the DEMO workbook is byte-identical to v1.0.1. The CLEAN workbook changed only in the SETTINGS sheet and the style table (date formats for the 3 restored cells).
- **Saved results added:** every formula cell now carries its calculated result (DEMO 62,232; CLEAN 62,232), taken from a full recalculation of the same files.
  - **Why:** Excel Protected View and file previews no longer show an empty workbook.
  - **Formula text** is identical to the pre-cache build in every cell. Excel and Sheets still recalculate fully on open.
  - **CLEAN previews** show the build date (Oct 1, 2026) until the file is opened for editing, at which point it shows today.
- **New regression tests:**
  - CLEAN system date equals today, and the reporting month and year are correct.
  - The 3 CLEAN SETTINGS formula cells exist.
  - First CLEAN job dated today: 3.42 estimated hours, Unpaid status, dashboard revenue $200 and 1 job completed.
- **Results:** 56/56 automated tests passed. 43/43 schema-checkable parts in each workbook are valid against the ISO/ECMA OOXML schemas. The buyer-ZIP audit found 0 problems.
- **Still outstanding:** real Microsoft Excel and Google Sheets testing. It wasn't possible here: there's no Excel in this environment, and the Drive connector can't upload binary files of this size.

## v1.0.3 (2026-10-01): Google Sheets dropdown fix
- **Found by the real Google Sheets test of v1.0.2:**
  - **Calculations:** every calculated value matched.
  - **Dropdowns:** only 2 of the 65 dropdowns survived Google's conversion.
- **Root cause:** list dropdowns that pull from a range were stored with a leading `=` (for example `='SETTINGS'!$F$5:$F$24`). That isn't the standard file form. Google Sheets silently drops such dropdowns; LibreOffice tolerated them.
- **How it was proven:** two small test workbooks were uploaded and converted by Google.
  - 8 storage variants without `=` were all kept, including named ranges, cross-sheet ranges and sheet names containing `&`.
  - With the same dropdown written with and without `=`, only the one without `=` was kept.
- **Fix:** `build_workbook.py` no longer adds `=` to dropdown sources (7 lines).
- **Scope of change:** the only change in both workbooks is the removed `=` in the 65 dropdown definitions. Every formula, cached value, chart, format, name and link is byte-identical to v1.0.2.
- **Results:**
  - 56/56 automated tests passed.
  - All 23 worksheets in each workbook are schema-valid.
  - LibreOffice keeps all 65 dropdowns.
  - The buyer-ZIP audit found 0 problems.
  - The ZIP's 50 files are identical to v1.0.2 except the 2 workbooks and the READ-ME version line.
  - Delivery tests: 15/15 unit and 34/34 browser checks passed.
- **Known Google Sheets limitation (cosmetic, not changed):** Google Sheets doesn't allow named ranges in conditional formatting. So 5 amber "below target margin" highlight rules, which use `TargetMargin`, are dropped in Sheets.
  - Values and the "Margin check" text still work.
  - Excel and LibreOffice show the highlight.
- **Confirmed in real Google Sheets (2026-10-04):** the real v1.0.3 DEMO and CLEAN files pass, read-only and cell by cell against the build.
  - 65/65 dropdowns, covering all 29,954 cells.
  - 62,232/62,232 formulas, with 0 error cells.
  - Charts, names, links, filters, frozen panes and merges all kept.
  - DEMO: Revenue $6,070, Margin 42.7%, Quote $522.50.
  - CLEAN: only the 5 TODAY cells differ, because Google uses the local time zone.
  - Details: `operatorgrid-launch/09-GOOGLE-SHEETS-VALIDATION-PLAN.md`, section 0.
- **Still outstanding:**
  - the Sheets interaction tests;
  - real Microsoft Excel testing.
