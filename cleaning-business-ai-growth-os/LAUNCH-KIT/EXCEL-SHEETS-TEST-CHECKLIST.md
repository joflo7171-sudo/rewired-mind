# Excel + Google Sheets Test Checklist — Cleaning Business AI Growth OS v1.0.1

**Why:** all formula testing so far ran in LibreOffice Calc (53/53 automated tests passed). Before taking money, confirm the same results in **real Microsoft Excel** and **real Google Sheets**. Allow about 45 minutes in total.

**Files:** use the copies **inside** `OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.1.zip` (unzip first). Work on copies so the originals stay untouched.

**How to record:** mark each line ✅ / ❌. For any ❌, take a screenshot showing the cell and the formula bar.

Expected values come from the DEMO file, whose as-of date is fixed at **Sep 30, 2026**, so they don't change with today's date.

---

## Part A — Microsoft Excel (2019, 2021 or Microsoft 365, desktop)

### A1. Opening and safety
- [ ] 1. Open `CLEANING-BUSINESS-AI-GROWTH-OS-DEMO.xlsx`. If a yellow *Protected View* bar appears, click **Enable Editing**.
- [ ] 2. **No** macro warning appears. There should be none, because the file has no macros.
- [ ] 3. **No** "update links / external content" prompt appears. *Data → Edit Links* should be greyed out or empty.
- [ ] 4. **No** repair prompt such as "We found a problem with some content…".
- [ ] 5. *File → Info → Properties*: Author shows **OperatorGrid**.

### A2. Error sweep
- [ ] 6. On each of the 23 tabs, press **Ctrl+F**, search for `#`, set *Look in: Values*, and click **Find All**. The result must find **no** cells showing `#NAME?`, `#VALUE!`, `#REF!`, `#DIV/0!` or `#N/A`.
  - `#NAME?` usually means an Excel version older than 2019 (MINIFS/MAXIFS). Note your Excel version if you see it.

### A3. DASHBOARD values (reporting month September 2026)
| # | Tile | Expected |
|---|---|---|
| 7 | Revenue | **$6,070** |
| 8 | Job Gross Profit | **$2,590** |
| 9 | Gross Margin | **42.7%** |
| 10 | Est. Operating Profit | **$1,987** |
| 11 | Payments Collected | **$5,335** |
| 12 | Unpaid Balances (all) | **$1,080** |
| 13 | New Leads / Quotes Given / Leads Booked | **13 / 5 / 1** |
| 14 | Conversion Rate | **7.7%** |
| 15 | Follow-Ups Due Now | **12** |
| 16 | Jobs Completed | **35** |
| 17 | Active Recurring Plans / Recurring Monthly Value | **10 / $3,985** |
| 18 | Average Rating | **4.5** |
| 19 | Customers to Reactivate | **7** |
| 20 | Action Center: "Completed jobs not fully paid" | **8** |
| 21 | Both charts (Revenue & job gross profit by month; Leads by stage) display with bars | — |

### A4. QUOTE BUILDER (demo quote: Deep Clean, 2,200 sq ft, 3 bd / 2.5 ba)
| # | Cell | Expected |
|---|---|---|
| 22 | G7 Estimated labor hours | **7.50** |
| 23 | G16 Price before tax | **$522.50** |
| 24 | G26 Total direct costs | **$283.37** |
| 25 | G28 Gross profit / G29 Gross margin | **$239.13 / 45.8%** |
| 26 | G32 Break-even / G33 Target-margin price | **$276.23 / $569.47** |
| 27 | G37 Profit after overhead share | **$192.88** |

- [ ] 28. **Scenario A:** change **B9 Cleaning type** to *Standard Clean* using the dropdown. Expect G7 **3.79**, G16 **$299.50**, G26 **$172.97**, G28 **$126.53**, G29 **42.2%**, and G35 reads "Below your target margin". Press **Ctrl+Z** to undo afterwards.

### A5. Other modules
- [ ] 29. **MONTHLY**, Year Total column: Revenue **$54,360**, Jobs completed **290**, Estimated operating profit **$17,716**.
- [ ] 30. **PROFITABILITY**, Standard Clean row (period = Reporting month): Jobs **16**, Revenue **$3,100**, Gross Profit **$1,195**, Margin **38.5%** (amber).
- [ ] 31. **RECURRING**, R-001 (Lane Ivers): Next Visit Due **Sep 22, 2026**, Booking Status **"Overdue — book now"** (red).
- [ ] 32. **CUSTOMERS**, C-001 Lane Ivers: Completed Jobs **34**, Lifetime Revenue **$6,225**. Also confirm the First Job / Last Job dates show (this tests MINIFS/MAXIFS).
- [ ] 33. **SCHEDULE** heading reads "Week of Sep 28, 2026", and the Jobs row reads **1, 0, 1, 1, 4, 0, 1** (Mon→Sun).
- [ ] 34. **FOLLOW-UPS**: first lead **Sage Sterling — Overdue**; first unpaid job **J-0273, Parker Lockhart, $150**.
- [ ] 35. **JOBS** J-0001: Payment Status **Paid**, Gross Profit **$179.56**, Margin **39.9%**.

### A6. Interaction tests
- [ ] 36. **Scenario B (CRM):** on **LEADS**, row for **L-0064 Sage Sterling**, change Stage to **Booked**. Expect on DASHBOARD: Leads Booked **2**, Conversion **15.4%**, Follow-Ups Due Now **11**, Action Center "Booked leads missing from CUSTOMERS" **2**. On LEADS that row shows Follow-Up Status "—" and Customer Record "Add to CUSTOMERS". Undo afterwards.
- [ ] 37. **Scenario C (payment):** on **REVENUE**, first empty row (**row 287**), enter Payment Date **9/30/2026**, Job ID **J-0273** (dropdown), Amount **150**, Method **Cash**. Expect DASHBOARD Unpaid Balances **$930**, Payments Collected **$5,485**, "Completed jobs not fully paid" **7**; JOBS J-0273 Payment Status **Paid**; FOLLOW-UPS first unpaid job becomes **J-0275**. Undo afterwards.
- [ ] 38. Dropdowns open and list values on: LEADS Stage, JOBS Customer / Property / Service / Worker / Status, REVENUE Job ID.
- [ ] 39. Filter buttons work on LEADS and JOBS (filter Stage = Overdue-status rows, then clear).
- [ ] 40. Click 3–4 links on START HERE (e.g. QUOTE BUILDER →, JOBS →). Each should jump to that tab.
- [ ] 41. Conditional colors appear: red "Overdue" in LEADS, green "Paid" / red "Unpaid" in JOBS.

### A7. CLEAN file
- [ ] 42. Open `CLEANING-BUSINESS-AI-GROWTH-OS-CLEAN.xlsx`. It opens with no prompts, START HERE says "CLEAN FILE", and every DASHBOARD tile shows "–" or 0 with **no** `#` errors.
- [ ] 43. In CLEAN: add one STAFF name, one CUSTOMER, one PROPERTY (2,000 sq ft, 3 bd, 2 ba), and one JOB dated **today** (Standard Clean, price 200, Status Completed). JOBS should show Auto Est. Hrs **3.42**, Payment Status **Unpaid**, and DASHBOARD Revenue **$200**.

### A8. Save round-trip
- [ ] 44. Save the DEMO as a new file, close it, and reopen it. Values are unchanged and no repair prompt appears.

---

## Part B — Google Sheets
1. Upload `CLEANING-BUSINESS-AI-GROWTH-OS-DEMO.xlsx` to Google Drive and open it.
2. Choose **File → Save as Google Sheets**, then work in the new Google Sheets copy.

- [ ] 45. Conversion finishes with no "some features could not be converted" warning. If a warning appears, record its exact text.
- [ ] 46. Error sweep: on each tab, **Ctrl+F** for `#` finds **no** `#NAME?`, `#ERROR!`, `#REF!`, `#VALUE!` or `#N/A`.
- [ ] 47. Repeat checks **7–20** (DASHBOARD values).
- [ ] 48. Repeat checks **22–28** (QUOTE BUILDER, including Scenario A).
- [ ] 49. Repeat checks **29–35** (other modules).
- [ ] 50. Repeat **Scenario B (36)** and **Scenario C (37)**.
- [ ] 51. Dropdowns (38) and filters (39) work.
- [ ] 52. Charts on DASHBOARD, MONTHLY and PROFITABILITY display. Colors may differ slightly; that's acceptable.
- [ ] 53. *Known limitation:* the clickable links on START HERE / DASHBOARD may **not** jump between tabs in Google Sheets. This is documented in the guide and isn't a failure. Record what happens.
- [ ] 54. Repeat **42–43** with the CLEAN file converted to Google Sheets.

---

## Pass criteria
- **Pass:** every value matches (±$1 for rounding display), zero `#` errors, no repair, macro or external-link prompts in Excel, and the scenarios behave as described.
- **Fail:** send the screenshots. Fixes will be made and the tests re-run before any sales page or checkout is created.

| Environment | Version tested | Result | Tester / date |
|---|---|---|---|
| Excel (Windows or Mac) | | | |
| Google Sheets | | | |
