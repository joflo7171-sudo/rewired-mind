# Google Sheets validation: plan and expected values (waiting for uploads)

**Status: NOT RUN.** As of this update, neither workbook is in Google Drive yet; only the v1.0.2 ZIP is.

## Your step
1. Unzip `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.2.zip`.
2. Upload **`CLEANING-BUSINESS-AI-GROWTH-OS-DEMO.xlsx`** and **`CLEANING-BUSINESS-AI-GROWTH-OS-CLEAN.xlsx`** to Google Drive, individually.
3. Open each one and choose **File → Save as Google Sheets**. Keep the default names; they start "CLEANING-BUSINESS-AI-GROWTH-OS".
4. Tell me they're ready.

## What I'll check through the Drive connector (read-only; nothing in your Drive gets edited)
| Check | How |
|---|---|
| Error sweep on every tab | Read the converted sheets and search for `#REF!`, `#VALUE!`, `#NAME?`, `#DIV/0!`, `#N/A`, `#ERROR!` |
| DEMO DASHBOARD | Revenue **$6,070** · Gross Profit **$2,590** · Margin **42.7%** · Op. Profit **$1,987** · Collected **$5,335** · Unpaid **$1,080** · Leads/Quotes/Booked **13/5/1** · Conversion **7.7%** · Follow-ups due **12** · Jobs **35** · Active plans **10** · Recurring MV **$3,985** · Rating **4.5** · Reactivate **7** · "Completed jobs not fully paid" **8** |
| DEMO QUOTE BUILDER | G7 **7.50** · G16 **$522.50** · G26 **$283.37** · G28 **$239.13** · G29 **45.8%** · G32 **$276.23** · G33 **$569.47** · G37 **$192.88** |
| DEMO other tabs | MONTHLY year totals **$54,360 / 290 jobs / $17,716 operating profit** · PROFITABILITY Standard Clean **16 jobs / $3,100 / $1,195 / 38.5%** · R-001 **Sep 22, 2026 · Overdue — book now** · C-001 **34 jobs / $6,225** · SCHEDULE jobs row **1,0,1,1,4,0,1** · FOLLOW-UPS first lead **Sage Sterling, Overdue**, first unpaid **J-0273 $150** |
| CLEAN | SETTINGS system date = **today**, reporting month = **this month**, reporting year = **this year**; all dashboard tiles 0 or "–"; no `#` errors |

## Limits of a read-only check
- **Interaction tests** need cell edits:
  - Standard Clean quote → **$299.50**
  - L-0064 → Booked → **15.4%** conversion
  - $150 payment on J-0273 → **$930** unpaid
  - a CLEAN job dated today → **3.42** hours, **Unpaid**, **$200** revenue

  The Drive connector can read but **cannot edit cells**, so you make those edits (about 5 minutes, steps in `cleaning-business-ai-growth-os/LAUNCH-KIT/EXCEL-SHEETS-TEST-CHECKLIST.md` Part B). I then re-read the sheet and confirm the results.
- **Dropdowns, charts, conditional formatting and tab links** are visual. The text the connector returns doesn't show them reliably, so you confirm those by eye (checklist items 51–53).
- **Large tabs:** the connector may shorten very large tabs (JOBS and REVENUE have 1,500 prepared rows). Where that happens, I'll verify through the dashboard, MONTHLY and PROFITABILITY values, which summarize every row.

## How differences are classified
- **Functional problem:** a wrong value, an error, or a feature that doesn't work. Fixed in the workbook and fully re-tested.
- **Cosmetic difference:** a color, chart style or formatting change with correct values. Documented, not fixed unless important.
- **Documented limitation:** known platform behavior, e.g. tab-link buttons in Google Sheets. Already noted in the guide.

Already expected in Sheets:
- Tab-link buttons may not jump between tabs (documented limitation).
- The amber "below target margin" highlight may not appear (cosmetic).
