"""Builds QUICK-START-GUIDE.pdf, FULL-USER-GUIDE.pdf and AI-WORKFLOW-LIBRARY.pdf."""
import sys, os
from pdfkit_simple import render
import content_ai as AI
import build_workbook as B

OUT = sys.argv[1]

DISCLAIMER = [
    ("h2", "Plain-language disclaimer"),
    ("p", "This product is a set of spreadsheet tools, templates and writing prompts that help you organize a cleaning business. "
          "It is not legal, tax, accounting, payroll, employment, insurance, safety or regulatory advice, and it does not replace a qualified professional."),
    ("bul", [
        "<b>Prices and profits are estimates.</b> The calculators turn YOUR assumptions into numbers. They do not know your local market, and the example "
        "assumptions included are starting points, not recommended or market rates.",
        "<b>No earnings promises.</b> Using this system does not guarantee more customers, revenue or profit. The demo business and all its numbers are fictional.",
        "<b>Templates need your review.</b> Policy, proposal and agreement-style templates are customizable starting points. Have anything you will rely on legally "
        "reviewed by a qualified professional where you operate.",
        "<b>Taxes, mileage, payroll and worker classification</b> rules vary by location. Confirm them with a qualified professional.",
        "<b>Safety:</b> always follow product labels, safety data sheets and local requirements. Checklists in this kit are quality checklists, not safety programs.",
        "<b>AI tools</b> can produce wrong or made-up information. Review every draft. Do not paste sensitive data (access codes, payment details, ID numbers) into AI tools.",
        "<b>Privacy:</b> you are responsible for how you collect, store and use customer information and for getting permission before sharing photos of customers' homes.",
    ]),
]

# ---------------------------------------------------------------- QUICK START
quick = [
    ("h1", "Up and running in 30 minutes"),
    ("p", "Welcome. This system runs a cleaning business from first inquiry to final payment: leads, quotes, jobs, recurring visits, "
          "your team, quality checks, payments, expenses and profit — all in one connected workbook that works in Microsoft Excel and Google Sheets."),
    ("h2", "What's in the box"),
    ("table", ([["File / folder", "What it is"],
                ["CLEANING-BUSINESS-AI-GROWTH-OS-DEMO.xlsx", "A fully working example business with fictional data. Explore it first — nothing you do here matters."],
                ["CLEANING-BUSINESS-AI-GROWTH-OS-CLEAN.xlsx", "The same system with no sample records. This becomes YOUR business file."],
                ["QUICK-START-GUIDE.pdf", "This guide."],
                ["FULL-USER-GUIDE.pdf", "Every module explained, plus assumptions, resetting, troubleshooting and FAQs."],
                ["AI-WORKFLOW-LIBRARY.pdf", "18 copy-and-paste AI workflows for messages, quotes, reviews and marketing."],
                ["CLIENT-FORMS/", "14 editable customer and staff documents (Word + PDF)."],
                ["MARKETING-KIT/", "Editable flyer, door hanger, cards, social templates and post copy."]], [0.42, 0.58])),
    ("h2", "Step 0 — Open the right file"),
    ("bul", ["<b>Excel (desktop or Microsoft 365):</b> open the CLEAN file and choose <i>Save As</i> to keep an untouched backup.",
             "<b>Google Sheets:</b> upload the CLEAN file to Google Drive, open it, then <i>File → Save as Google Sheets</i>. Work in the Google Sheets copy.",
             "<b>Apple Numbers</b> is not supported (several formulas and dropdowns behave differently)."]),
    ("h2", "The 5 setup steps"),
    ("num", [
        "<b>SETTINGS</b> — Type your business name, phone, email and booking link. Then replace the example cost assumptions: worker pay rate, "
        "extra labor cost %, supplies per labor hour, vehicle cost per mile, card fee %, target margin and minimum job price. Leave the <i>as-of date</i> blank.",
        "<b>STAFF &amp; TASKS</b> — Add every person who cleans (including yourself if you do) with their pay rate. Names feed every Worker dropdown.",
        "<b>PRICING</b> — Adjust the billing rate per labor hour and the time assumptions for each cleaning type. Watch the rate card at the bottom update. "
        "Keep adjusting until those prices reflect how you want to price in your market.",
        "<b>CUSTOMERS &amp; PROPERTIES</b> — Add your current customers, then one row per property with square feet, bedrooms and bathrooms "
        "(these create the automatic time estimate on every job).",
        "<b>RECURRING &amp; JOBS</b> — Add recurring plans, then upcoming jobs. Pick the Plan ID on recurring visits so the system tracks what's due next.",
    ]),
    ("tip", "Test it: open QUOTE BUILDER and price a home you know well. If the result looks wrong, change the PRICING assumptions — not the formulas."),
    ("h2", "Your daily 10-minute routine"),
    ("table", ([["When", "Do this", "Where"],
                ["Morning", "Check the ACTION CENTER: follow-ups due, unpaid jobs, recurring visits to book.", "DASHBOARD"],
                ["New inquiry", "Add a row, reply with AI Workflow 01, set Next Follow-Up.", "LEADS"],
                ["Quote", "Price it, copy the summary into AI Workflow 02, enter Quote Value.", "QUOTE BUILDER → LEADS"],
                ["Booked", "Stage = Booked; add customer + property; add the job.", "LEADS → CUSTOMERS → JOBS"],
                ["After each job", "Status = Completed, actual hours; log payment and miles.", "JOBS, REVENUE, MILEAGE"],
                ["Happy customer", "Send a review request (Workflow 07).", "REVIEWS"],
                ["Weekly", "Book recurring visits due; review SCHEDULE; plan marketing (Workflow 18).", "SCHEDULE, RECURRING"],
                ["Monthly", "Review profit by service and worker; adjust pricing if margins are below target.", "MONTHLY, PROFITABILITY"]],
               [0.16, 0.58, 0.26])),
    ("h2", "Five rules that keep it working"),
    ("bul", ["Type only in white cells. Gray cells and ⚙ columns are automatic.",
             "Use the dropdowns — they keep the sheets connected.",
             "Keep customer names, property labels and staff names unique (add an initial if two match).",
             "Need more rows? Type in the next empty row; there's room for 1,500 jobs and payments. See the User Guide to extend.",
             "Back up weekly: File → Save a copy (Excel) or File → Make a copy (Google Sheets)."]),
] + DISCLAIMER

render(os.path.join(OUT, "QUICK-START-GUIDE.pdf"), "Quick Start Guide", "Set up your system in 30 minutes and run your day in 10.", quick)

# ---------------------------------------------------------------- FULL USER GUIDE
mods = []
MOD_DOC = {
    "START HERE": ("Your home page: setup steps, a clickable map of every module, the color legend and golden rules.", "Nothing.", "Links to every tab."),
    "DASHBOARD": ("One-screen view of the business for the reporting month: money, pipeline, operations, reputation, an Action Center and two trend charts.",
                  "Nothing — change the reporting month in SETTINGS.",
                  "Every tile and chart. 'vs last month' compares with the previous month of the same year."),
    "LEADS": ("Lead CRM and sales pipeline with 8 stages: New Lead, Contacted, Quote Requested, Quote Sent, Follow-Up, Booked, Recurring Client, Lost/Declined.",
              "Date, name, contact details, source, requested service, quote value, stage, last contact, next follow-up, lost reason, notes.",
              "Booking outcome (Open/Booked/Lost), follow-up status (Overdue / Due today / Due soon / Scheduled / Set date), days since added, "
              "and an 'Add to CUSTOMERS' reminder for booked leads that aren't in your customer list yet."),
    "CUSTOMERS": ("Your customer list and history.", "Name (unique), contact details, type, source, preferred contact, status, notes.",
                  "First/last job, completed jobs, lifetime revenue, balance due, recurring plan?, days since last job, suggested next action "
                  "(Collect balance, Book first job, Reactivate, Ask for review, Offer recurring plan) and referrals given."),
    "PROPERTIES": ("Property details for each customer location.", "Address/label (unique), customer, area, type, square feet, bedrooms, bathrooms, pets, access instructions, parking, special requests.",
                   "Completed jobs, last clean, average price. Square feet, bedrooms and bathrooms drive the automatic time estimate in JOBS."),
    "QUOTE BUILDER": ("Prices one job and shows the profit before you send the quote.",
                      "Cleaning type, square feet, bedrooms, bathrooms, condition, frequency, workers, optional hour/rate/supply overrides, pay rate, miles, travel time, up to 6 add-ons, discount, optional tax %, card payment yes/no.",
                      "Estimated hours, time on site, base price, frequency discount, add-ons, price before tax, tax, customer total, labor, travel, vehicle, supplies, add-on costs, "
                      "payment fee, total direct costs, gross profit, margin, revenue and profit per labor hour, break-even price, price needed for your target margin, "
                      "monthly value if recurring, a margin check, an optional overhead share with profit after overhead, and a ready-to-copy quote summary."),
    "PRICING": ("All pricing assumptions in one place, plus a rate card.",
                "Per cleaning type: billing rate per labor hour, square feet cleaned per labor hour, minutes per bedroom and bathroom, setup minutes, supplies multiplier. "
                "Condition multipliers, frequency discounts and spacing, add-on prices/times/costs. Add new service types in the blank rows.",
                "Example hours for a 2,000 sq ft 3/2 home, and a rate card for eight home sizes at the condition and frequency you choose."),
    "JOBS": ("The operational heart: every job, one row.", "Date, start time, customer, property, service, plan ID (recurring), lead worker, crew size, optional estimated hours, actual hours, "
             "price before tax, tax %, optional supplies cost, status (Scheduled/Completed/Cancelled/Rescheduled/No-Show), notes.",
             "Automatic hour estimate, hours used, invoice total, paid, balance, payment status, pay rate, labor cost, supplies cost, miles and vehicle cost "
             "(from MILEAGE), payment fees (from REVENUE), estimated gross profit and margin, revenue per labor hour, hours over/under estimate, QC score, and helper columns."),
    "RECURRING": ("Recurring service plans.", "Customer, property, service, frequency, price per visit, usual worker, start date, preferred day/time, plan status, notes.",
                  "Visits completed, last visit, next booked visit, next visit due, days until due, booking status (Booked / Due this week — book / Overdue — book now / Upcoming), monthly and annual value."),
    "SCHEDULE": ("A weekly calendar built from JOBS.", "Optionally a date in the week you want to see (blank = this week).",
                 "Up to 10 jobs per day in start-time order with customer, service, worker and job ID; daily job count, labor hours and revenue; recurring visits that need booking."),
    "STAFF & TASKS": ("Team roster and task assignments.", "Staff: name, role, pay rate, contact, status, start date. Tasks: task, assigned to, job ID, due date, priority, status, notes.",
                      "Each worker's jobs, labor hours and revenue for the reporting month, average QC score and issues logged; task due flags."),
    "REVENUE": ("Payments received.", "Payment date, job ID, amount, tip, method, invoice/ref number, notes.",
                "Customer and service (from JOBS), estimated processing fee (methods marked 'Yes' in SETTINGS), month. Payments flow back to JOBS as Paid / Partial / Unpaid."),
    "EXPENSES": ("Business spending.", "Date, category, vendor, description, amount, paid with, optional job ID, receipt saved?, notes.",
                 "Whether the category counts as overhead, month."),
    "PROFITABILITY": ("Where you make and lose money.", "Choose the period: Reporting month, Year to date or All time.",
                      "By service type, by worker and by customer type: jobs, revenue, labor, supplies, vehicle, fees, gross profit, margin, average price, labor hours, "
                      "revenue and profit per labor hour, jobs below target, jobs losing money, average hours over/under estimate; plus a chart."),
    "MILEAGE": ("Trip log.", "Date, optional job ID, purpose, from, to, odometer start/end OR miles, driver/vehicle.",
                "Miles used, cost at your rate, month. Trips with a job ID add vehicle cost to that job."),
    "SUPPLIES": ("Inventory and reorder alerts.", "Item, category, unit, unit cost, on hand, reorder level, supplier, last purchased, notes.", "Stock value and Reorder/OK flag."),
    "FOLLOW-UPS": ("Your follow-up command center.", "Your own follow-up log: due date, contact, type, related ID, channel, AI workflow to use, status, notes.",
                   "Top 15 leads to follow up (soonest first) and top 15 unpaid completed jobs (oldest first); due flags on your log."),
    "REVIEWS": ("Review requests and replies.", "Customer, job ID, date requested, platform, status, date received, rating, replied?, notes.",
                "Days waiting and an action (Send reminder / Reply to review / Close out)."),
    "REFERRALS": ("Referral tracking.", "Date, referred by, new contact, phone/email, status, reward/thank-you, reward status, notes.",
                  "Revenue from the referred customer (when their name matches CUSTOMERS/JOBS)."),
    "QUALITY CONTROL": ("Inspection log and issue/rework log.", "Inspections: date, job ID, checklist, inspector, items checked, items passed, issues, rework needed, rework date, resolved. "
                        "Issues (row 311+): date, job ID, reported by, type, what happened, action, fix date, status, cost of fix, resolved date.",
                        "Customer and worker (from JOBS), score, Pass/Fail against your passing score, rework status, days open."),
    "QC CHECKLISTS": ("Six printable checklists: Residential Standard, Deep Clean, Move-In/Move-Out, Airbnb Turnover, Commercial, Final Inspection.",
                      "Mark items Yes / No / N/A; edit task wording to match your standards.", "A score for each checklist."),
    "MONTHLY": ("Twelve-month performance for the reporting year.", "Nothing.",
                "Sales, operations, money (revenue, labor, supplies, vehicle, fees, gross profit, overhead, estimated operating profit, margins, collections, spending) and growth metrics, plus a chart."),
    "SETTINGS": ("Business details, assumptions, targets, dates and every dropdown list.",
                 "Business profile, as-of date (normally blank), reporting month, labor/supply/vehicle/fee/tax assumptions, targets and rules, editable lists.",
                 "System date, reporting month and year. Lists marked LOCKED are used by formulas — don't rename them."),
}
for name, _tab in B.SHEETS:
    purpose, you, auto = MOD_DOC[name]
    mods += [("h3", name), ("table", ([["Purpose", "You enter", "Automatic"], [purpose, you, auto]], [0.26, 0.37, 0.37]))]

full = [
    ("h1", "Full User Guide"),
    ("p", "This guide explains how the system is organized, how every module works, how to change assumptions, how to reset or extend the workbook, "
          "and how to fix common problems. Keep the DEMO file open next to this guide — every feature described here is visible in it."),
    ("h2", "1. How the system fits together"),
    ("p", "Information is entered once and reused everywhere. The customer journey flows left to right:"),
    ("table", ([["Stage", "Module", "Feeds"],
                ["Lead", "LEADS", "Dashboard pipeline, conversion rate, follow-up lists"],
                ["Quote", "QUOTE BUILDER + PRICING", "Quote value in LEADS; prices in JOBS and RECURRING"],
                ["Customer", "CUSTOMERS + PROPERTIES", "Dropdowns in JOBS/RECURRING; automatic time estimates"],
                ["Work", "JOBS, RECURRING, SCHEDULE, STAFF & TASKS", "Revenue, labor cost, schedule, worker output"],
                ["Quality", "QUALITY CONTROL + QC CHECKLISTS", "QC score per job and worker; issue tracking"],
                ["Payment", "REVENUE, EXPENSES, MILEAGE", "Paid/unpaid status, job profit, overhead"],
                ["Growth", "REVIEWS, REFERRALS, FOLLOW-UPS", "Next actions, reputation metrics"],
                ["Decisions", "DASHBOARD, PROFITABILITY, MONTHLY", "What to fix, raise, repeat or stop"]], [0.14, 0.38, 0.48])),
    ("h3", "Color legend"),
    ("bul", ["<b>White cells</b> — type here.", "<b>Cream cells</b> — key settings and calculator inputs.",
             "<b>Gray cells / ⚙ headers</b> — automatic formulas. Don't type in them.",
             "<b>Red</b> needs attention · <b>Amber</b> below target or due soon · <b>Green</b> good / done."]),
    ("h2", "2. Setup in detail"),
    ("h3", "Excel"),
    ("bul", ["Works in Excel 2019, 2021 and Microsoft 365 (Windows and Mac). The MINIFS/MAXIFS functions used for first/last job dates need Excel 2019 or newer.",
             "If Excel shows 'Protected View', click <i>Enable Editing</i> so formulas calculate.",
             "Formulas recalculate automatically. If numbers look stale, press F9 (Windows) or Cmd + = (Mac)."]),
    ("h3", "Google Sheets"),
    ("bul", ["Upload the CLEAN file to Drive → open → <i>File → Save as Google Sheets</i>.",
             "The clickable tab links on START HERE and DASHBOARD may not work in Google Sheets — use the tabs along the bottom instead.",
             "Charts convert automatically; if a chart looks different, double-click it to adjust colors."]),
    ("h3", "Recommended order"),
    ("num", ["SETTINGS: business details and assumptions.", "STAFF & TASKS: your team and pay rates.", "PRICING: rates, times, add-ons; check the rate card.",
             "CUSTOMERS, then PROPERTIES.", "RECURRING plans.", "JOBS: upcoming jobs (and past jobs if you want history).",
             "SUPPLIES (optional) and QC CHECKLISTS (edit to match your standards)."]),
    ("h2", "3. Every module explained"),
] + mods + [
    ("h2", "4. How the numbers are calculated"),
    ("h3", "Estimated labor hours"),
    ("p", "Hours = (square feet ÷ square feet per labor hour + bedrooms × minutes per bedroom ÷ 60 + bathrooms × minutes per bathroom ÷ 60 + setup minutes ÷ 60) × condition multiplier. "
          "Add-on minutes are added on top. Labor hours are total person-hours; time on site = labor hours ÷ number of workers."),
    ("h3", "Price"),
    ("p", "Base price = the greater of your minimum job price and (estimated hours × billing rate). The frequency discount applies to the base price only. "
          "Then add-ons are added and your manual discount subtracted. Tax is added only if you enter a tax %."),
    ("h3", "Costs and profit"),
    ("bul", ["Labor cost = labor hours × pay rate × (1 + extra labor cost %).",
             "Paid travel (quote only) = travel minutes ÷ 60 × workers × pay rate × (1 + extra labor %).",
             "Vehicle cost = miles × your cost per mile.",
             "Supplies = labor hours × supplies per labor hour × the service's supplies multiplier (or your override).",
             "Payment fee = customer total × card fee % (quotes) or payments made with fee-bearing methods (jobs).",
             "Gross profit = price before tax − all direct costs above. Gross margin = gross profit ÷ price before tax.",
             "Break-even price = the price at which gross profit is zero. Target-margin price = the price that would hit your target margin.",
             "Overhead share (quote only, optional) = labor hours × the overhead-per-labor-hour rate in SETTINGS. Leave it at 0 to ignore.",
             "Estimated operating profit (MONTHLY) = job gross profit − overhead expenses (categories marked Overhead in SETTINGS)."]),
    ("note", "Why some expense categories are NOT overhead: staff pay, job supplies, fuel and merchant fees are already estimated inside each job's cost. "
             "Counting them again as overhead would double-count them. You can change any category's flag in SETTINGS."),
    ("h2", "5. Changing assumptions"),
    ("bul", ["<b>Pay, extra labor %, supplies, vehicle, fees, tax, target margin, minimum price:</b> SETTINGS (cream cells).",
             "<b>Billing rates, speed, room minutes, setup time, supplies multiplier:</b> PRICING section 1.",
             "<b>Condition multipliers:</b> PRICING section 2. <b>Recurring discounts and visit spacing:</b> section 3. <b>Add-ons:</b> section 4.",
             "<b>One quote only:</b> use the override cells in QUOTE BUILDER — they don't change your saved assumptions.",
             "<b>Lists</b> (lead sources, expense categories, payment methods, etc.): SETTINGS → type in the blank rows of any list that isn't LOCKED.",
             "Changing an assumption updates all automatic estimates, including past jobs that don't have actual hours or a typed supplies cost."]),
    ("tip", "Calibrate with real data: after 10–20 jobs, compare 'Hours Over/Under' on PROFITABILITY. If a service always runs over, lower its square feet per labor hour on PRICING."),
    ("h2", "6. Resetting sample data"),
    ("p", "The simplest way to start fresh is to use the CLEAN file — it's identical to the demo without sample records. To empty the DEMO (or reset your own file):"),
    ("num", ["Save a copy first.",
             "On each log tab (LEADS, CUSTOMERS, PROPERTIES, JOBS, RECURRING, STAFF & TASKS, REVENUE, EXPENSES, MILEAGE, SUPPLIES, FOLLOW-UPS, REVIEWS, REFERRALS, QUALITY CONTROL), "
             "select the WHITE input columns from row 5 down and press Delete. Do not delete rows, and do not clear gray ⚙ columns or the ID column.",
             "On STAFF & TASKS also clear the task table (row 31 down); on QUALITY CONTROL also clear the issue log (row 312 down); on FOLLOW-UPS clear the log from row 25.",
             "In SETTINGS, clear the as-of date and reporting month so the system uses today's date, and replace the business profile.",
             "Clear QUOTE BUILDER customer, address and add-on rows."]),
    ("p", "All automatic columns return to blank and the dashboard shows dashes. This was tested: clearing every input column leaves zero formula errors."),
    ("h2", "7. Adding rows and growing"),
    ("bul", ["Capacity: 500 leads, 400 customers, 400 properties, 1,500 jobs, 150 recurring plans, 1,500 payments, 1,000 expenses, 1,500 trips, "
             "300 inspections, 150 issues, 500 review requests, 200 referrals.",
             "To extend a log: select the entire last row, copy, and paste it into the rows below. Then extend any ranges that reference the log by "
             "inserting rows <i>inside</i> the table (right-click a row number above the last row → Insert) — Excel and Google Sheets then grow every connected range automatically.",
             "Sorting: select the whole table (header row down to the last row) before sorting, or just use the filter buttons, which are always safe.",
             "Adding a service type: type it in a blank row of PRICING section 1 with its rate and times — it appears in every Service dropdown and on PROFITABILITY."]),
    ("h2", "8. Troubleshooting"),
    ("table", ([["Problem", "Likely cause and fix"],
                ["Dropdown doesn't show a customer/property/worker", "The name isn't in CUSTOMERS / PROPERTIES / STAFF yet, or it's past the list capacity. Add it there first."],
                ["Job shows no automatic hours", "Property not chosen, not found, or missing square feet. Check the PROPERTIES row."],
                ["REVENUE says 'Job ID not found'", "The Job ID was typed instead of picked. Use the dropdown or copy it from JOBS column A."],
                ["Job shows Unpaid although it was paid", "Payment logged against a different Job ID, or the job price includes tax that wasn't collected. Compare Invoice Total and Paid in JOBS."],
                ["Dashboard shows dashes everywhere", "Reporting month in SETTINGS has no data, or the as-of date is still set to the demo date. Clear both cells."],
                ["Recurring plan says 'Set start date'", "Enter a Start Date on the plan."],
                ["Visit not on SCHEDULE", "Status is Cancelled or Rescheduled, the date is in another week, or the day already has 10 jobs."],
                ["#N/A, #VALUE! or #NAME? appears", "A formula cell was typed over or deleted. Copy the same column's formula from a working row above and paste it back. "
                 "#NAME? in old Excel versions means MINIFS/MAXIFS aren't supported — use Excel 2019+ or Google Sheets."],
                ["Numbers look wrong after editing PRICING", "Check you didn't type text (e.g., '$50 ') into a number cell. Re-type the number."],
                ["File feels slow", "Normal on very old computers with large logs. Close other workbooks; in Excel use Formulas → Calculation Options → Automatic."]],
               [0.34, 0.66])),
    ("h2", "9. Using the AI workflows"),
    ("p", "The AI-WORKFLOW-LIBRARY.pdf contains 18 prompts. These workflows can be used with most general-purpose AI assistants. "
          "No paid AI API or plug-in is required — you copy, paste and fill in the brackets."),
    ("num", ["Paste your Business Profile (page 2 of the library) at the start of a new chat.",
             "Copy the workflow prompt, replace every [bracket] with real details, and send it.",
             "Edit the draft — check names, prices, dates and promises against the workbook.",
             "Send it yourself and log the action (the library shows which sheet to update)."]),
    ("note", "AI helps with communication and organization only. It must not make legal, safety, tax, accounting, insurance, hiring, pay or regulatory decisions."),
    ("h2", "10. FAQ"),
    ("table", ([["Question", "Answer"],
                ["Does it work on a phone?", "Viewing works in the Excel and Google Sheets apps. Data entry is easiest on a computer or tablet."],
                ["Can several people use it?", "Yes in Google Sheets (share the file) or Excel for the web/OneDrive. Avoid two people editing the same row at once."],
                ["Does it send texts or emails?", "No. It tells you who to contact and the AI workflows help you write the message; you send it from your own phone or email."],
                ["Does it replace accounting software?", "No. It's a management system. Give your accountant your REVENUE and EXPENSES logs or use accounting software for tax records."],
                ["Is the pricing 'correct' for my area?", "The system can't know that. It calculates prices from your assumptions so you can see time, cost and profit before you quote."],
                ["Can I change colors or labels?", "Yes. Change any formatting freely. Avoid renaming tabs or LOCKED list values — formulas use them."]],
               [0.3, 0.7])),
] + DISCLAIMER

render(os.path.join(OUT, "FULL-USER-GUIDE.pdf"), "Full User Guide", "Every module, every calculation, setup, resetting and troubleshooting.", full)

# ---------------------------------------------------------------- AI LIBRARY
ai = [("h1", "AI Workflow Library"),
      ("p", "18 practical workflows for the messages and marketing a cleaning business writes every week. Each one tells you when to use it, "
            "what details to gather, the prompt to copy, what to check before sending, and where to record the result in your workbook."),
      ("p", "Works with any general AI assistant. No paid API, plug-in or automation tool is required."),
      ("h2", "Ground rules"), ("bul", AI.GUARDRAILS),
      ("h2", "Step 1 — Your business profile"),
      ("p", "Fill this in once, save it in a note, and paste it at the start of each AI chat. It makes every draft sound like your business."),
      ("prompt", AI.BUSINESS_PROFILE),
      ("h2", "Workflow index"),
      ("table", ([["#", "Workflow", "Use it when"]] + [[w["id"], w["title"], w["when"]] for w in AI.W], [0.06, 0.3, 0.64])),
      ("break", None)]
for w in AI.W:
    ai += [("h2", f"{w['id']}  ·  {w['title']}"),
           ("table", ([["When to use", "Gather first"], [w["when"], w["inputs"]]], [0.5, 0.5])),
           ("prompt", w["prompt"]),
           ("tip", f"<b>Check before sending:</b> {w['review']}<br/><b>Record it:</b> {w['sheet']}")]
ai += [("h2", "What AI should not do for you"),
       ("p", "These workflows deliberately exclude decisions that need professional judgment or legal responsibility. Don't use AI to decide:"),
       ("bul", ["Contract terms, liability, cancellation-fee enforceability or anything legal.",
                "Taxes, deductions, sales-tax rules, payroll or worker classification.",
                "Insurance coverage, damage claims or refunds tied to claims.",
                "Chemical mixing, safety procedures or regulatory compliance.",
                "Hiring, firing, pay rates or discipline decisions."]),
       ("p", "Use AI to organize your thinking and draft communication; make the decision yourself, with professional advice where needed.")] + DISCLAIMER
render(os.path.join(OUT, "AI-WORKFLOW-LIBRARY.pdf"), "AI Workflow Library", "18 copy-and-paste workflows for leads, quotes, reviews, referrals and marketing.", ai)
print("guides built")
