# Product Inventory — Cleaning Business AI Growth OS v1.0

Status: **v1.0.1 (OperatorGrid) — built, tested and audited; not published. Proposed price $149 one-time, no discounts.**

## 1. Workbooks
| File | Contents |
|---|---|
| `CLEANING-BUSINESS-AI-GROWTH-OS-DEMO.xlsx` | Full system with a fictional sample business (Jan–Oct 2026): 76 leads, 30 customers, 32 properties, 307 jobs, 12 recurring plans, 4 staff, 7 tasks, 282 payments, 104 expenses, 299 trips, 16 supply items, 8 follow-ups, 22 review requests, 7 referrals, 48 inspections, 6 issues. The as-of date is fixed at Sep 30, 2026 so the demo always looks current. 62,232 formulas. |
| `CLEANING-BUSINESS-AI-GROWTH-OS-CLEAN.xlsx` | The same system with all sample records removed. The as-of date is blank, so it uses today's date. Example assumptions are kept (clearly labelled) along with checklists and lists. 62,229 formulas. |

### Tabs (22 modules + checklists)
| # | Tab | Module |
|---|---|---|
| 1 | START HERE | Start Here |
| 2 | DASHBOARD | Executive Dashboard (24 KPI tiles, Action Center with 10 alerts, pipeline table, 2 charts) |
| 3 | LEADS | Lead CRM + 8-stage sales pipeline (500 rows) |
| 4 | CUSTOMERS | Customers (400) |
| 5 | PROPERTIES | Properties (400) |
| 6 | QUOTE BUILDER | Quote Builder + Profit Engine |
| 7 | PRICING | Pricing Calculator (types, condition, frequency, add-ons, rate card) |
| 8 | JOBS | Jobs (1,500) |
| 9 | RECURRING | Recurring Jobs (150 plans) |
| 10 | SCHEDULE | Weekly Schedule + recurring visits needing booking |
| 11 | STAFF & TASKS | Staff (20) / Task Assignments (200) |
| 12 | REVENUE | Revenue / payments (1,500) |
| 13 | EXPENSES | Expenses (1,000) |
| 14 | PROFITABILITY | Job Profitability by service, worker and customer type + chart |
| 15 | MILEAGE | Mileage (1,500) |
| 16 | SUPPLIES | Supplies (100) |
| 17 | FOLLOW-UPS | Follow-Ups (auto lead and unpaid lists + 300-row log) |
| 18 | REVIEWS | Reviews (500) |
| 19 | REFERRALS | Referrals (200) |
| 20 | QUALITY CONTROL | Quality Control: inspections (300) + issue/rework log (150) |
| 21 | QC CHECKLISTS | Six checklists: residential, deep, move-in/out, Airbnb turnover, commercial, final inspection |
| 22 | MONTHLY | Monthly Performance (32 metrics × 12 months + chart) |
| 23 | SETTINGS | Settings: business profile, dates, 9 cost assumptions, 6 targets/rules, 32 dropdown lists |

## 2. Guides (PDF)
| File | Pages |
|---|---|
| `QUICK-START-GUIDE.pdf` | 4 |
| `FULL-USER-GUIDE.pdf` | 11: setup, every module, calculations, changing assumptions, resetting sample data, extending rows, troubleshooting, AI instructions, FAQ, disclaimer |
| `AI-WORKFLOW-LIBRARY.pdf` | 13: ground rules, business profile prompt, 18 workflows, what AI should not do |

## 3. CLIENT-FORMS (14 templates, each as editable .docx + printable .pdf)
01 Client Intake Form · 02 Property Walkthrough · 03 Quote/Estimate · 04 Proposal (template, needs professional review) · 05 Welcome Guide · 06 Job Checklist · 07 Invoice · 08 Receipt · 09 Review Request · 10 Referral Request · 11 Rescheduling & Cancellation Policy TEMPLATE (needs professional review) · 12 Complaint Resolution Form · 13 Quality Inspection Form · 14 Employee Job Sheet

## 4. MARKETING-KIT
| File | Designs |
|---|---|
| `editable-pptx/01-Service-Flyer-8.5x11.pptx` | 1 |
| `editable-pptx/02-Door-Hanger-4.25x11.pptx` | 2 (front/back) |
| `editable-pptx/03-Referral-Card-3.5x2.pptx` | 2 (front/back) |
| `editable-pptx/04-Review-Card-3.5x2.pptx` | 2 (front/back) |
| `editable-pptx/05-Social-Squares-1080x1080.pptx` | 5: before/after, recurring promo, new-client promo, tip post, real-review spotlight |
| `editable-pptx/06-Story-1080x1920.pptx` | 1 |
| `editable-pptx/07-Google-Business-Post-Images-1200x900.pptx` | 3 |
| `MARKETING-COPY-TEMPLATES.docx` | 6 Google Business Profile posts, 6 Facebook/Instagram captions, recurring and new-client promotion copy, print notes |
| `preview-pdf/` | PDF previews of all of the above |

No stock photos, purchased fonts or third-party assets were used. All designs are built from shapes and Arial, with photo placeholders.

## 5. Business documents (internal — do not ship to customers)
`MARKET-RESEARCH.md` · `QA-REPORT.md` · `PRICING-VALIDATION.md` · `PRODUCT-LISTING-DRAFT.md` · `PRODUCT-INVENTORY.md` · `README.md`

## 6. Source / rebuild scripts (internal)
Folder `../cleaning-business-ai-growth-os-build/`: `build_workbook.py`, `demo_data.py`, `build_guides.py`, `content_ai.py`, `pdfkit_simple.py`, `build_forms.py`, `build_marketing.py`, `qa.py`. Every deliverable can be regenerated from these scripts.

## Customer download package (when approved)
Ship: both .xlsx files, the 3 guide PDFs, `CLIENT-FORMS/`, `MARKETING-KIT/`.
Do **not** ship: the .md business documents or the build folder.

## Launch kit (internal, not shipped)
`LAUNCH-KIT/OperatorGrid-Cleaning-Business-AI-Growth-OS-v1.0.1.zip` (buyer download) · `LAUNCH-KIT/images/` (cover, thumbnail, 6 gallery images) · `LAUNCH-KIT/LAUNCH-PLAN.md` · `LAUNCH-KIT/EXCEL-SHEETS-TEST-CHECKLIST.md`.
Additional build scripts: `clean_meta.py` (OperatorGrid metadata, fingerprint removal), `audit_zip.py` (buyer-ZIP audit), `build_launch_images.py`.
