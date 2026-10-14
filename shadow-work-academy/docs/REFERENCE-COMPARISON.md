# Reference comparison: Cash Command OS

## What I could and could not inspect
| Item | Access | Result |
|---|---|---|
| `https://cashcommandos.com/` (retried several times, also `www.`, via WebFetch and curl) | ❌ | DNS does not resolve from this environment (`ENOTFOUND`); outbound access is allow-listed. Gumroad, rewiredmind.org and the other domains also failed, so this is the environment, not necessarily the site. |
| Cash Command OS **product file** | ✅ | Found in your Google Drive: `Cash-Command-OS-Complete.xlsx` (135 KB, created 2026-10-09). Opened and inspected. |
| Cash Command OS sales page: structure, copy, screenshots, FAQ, checkout, delivery email | ❌ | Not in Drive or Gmail (searched both). No Gumroad emails found. |
| Backlink tracker sheet mentioning Cash Command OS | ✅ | Only outreach tracking; no site source. |

**I therefore cannot compare the two sales pages, and I am not claiming The Shadow Work Academy matches the reference.** I only compared the *products*.

## What the Cash Command OS product is (from the workbook)
A 14-tab Excel workbook, a 13-week cash forecast for service businesses: Start Here, Dashboard (2 charts), Setup, Cash In, Cash Out, Receivables, Payables, Forecast, Actuals, Scenarios, Decisions, 12-Month Outlook, Review System, Checks. About 3,200 live formulas. Patterns visible in it:
1. A **Start Here** tab with numbered setup steps, a colour key (yellow = type here, grey = calculated), a 5-minute weekly routine, and an explicit "planning tool only, not advice" disclaimer.
2. **Fictional sample data** ("Northline Creative") so the user sees it working, plus instructions to clear it.
3. A **Checks** tab ("ALL CHECKS PASS") and plain-language status messages when an input is wrong.
4. A **weekly review routine** as the habit that makes it useful.
5. Calculated cells protected without a password.

## What I applied (only where it materially helps this product)
| Reference pattern | Shadow Work Academy equivalent |
|---|---|
| Sample data so the first use is not a blank page | **Worked examples** (clearly fictional) for the Module 1, 3 and 5 worksheets, in the app and workbook |
| Start Here + routine | `START-HERE.html`, Quick-Start Guide, weekly tracker, module action steps |
| Disclaimer up front | Present in START-HERE, every module, every PDF footer, and the site |
| Self-checks | Not applicable (no calculations). The backup/restore and storage-blocked warning serve the "tell me when something is wrong" role |
| Excel/Sheets format | Deliberately not used: this product is reading and reflection, not calculation |

Nothing was copied: no finance content, branding or visuals.

## Recommendation, limited by what I have seen
The reference product has a tangible, measurable output (a cash number), so a sales page can show a screenshot of a result. The Academy's output is personal and qualitative, which makes the **free Module 1 sample** and real screenshots of worksheets the honest equivalent of "see it work". The strongest conversion lever I can recommend without having seen the reference page is an **email-gated sample** (feeds the Rewired Mind list, your stated priority) — it needs your approval and a privacy-policy update, so I have not built it.

## New finding: where the reference lives
Your Netlify account has a project `cash-command-os` whose primary URL is `https://cashcommandos.com` (Netlify Forms enabled; current deploy ready). So the reference sales site is a Netlify-hosted site, not something I can reach from here. The read-only Netlify tools I have do not expose file contents. Fastest way to unblock the comparison: in Netlify open the `cash-command-os` project → Deploys → the current deploy → download the deploy (or give me the source repo/zip), or save full-page desktop and mobile screenshots.

## What I need to finish this comparison
Any one of: the cashcommandos.com HTML (browser "Save page as…"), full-page screenshots of desktop and mobile, the site source/repo, plus its product description, FAQ, and the Gumroad (or other) delivery email. Then I can compare section order, above-the-fold clarity, proof elements, pricing presentation, FAQ and checkout flow, and recommend only changes that materially help.
