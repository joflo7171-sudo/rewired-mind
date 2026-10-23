"""Builds the owner-absent acquisition workbook. All inputs are ASSUMPTIONS, not market data."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()
B = Font(bold=True)
INP = PatternFill("solid", fgColor="FFF2CC")   # yellow = editable input
HDR = PatternFill("solid", fgColor="D9E1F2")


def hdr(ws, row, vals):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = B
        c.fill = HDR
        c.alignment = Alignment(wrap_text=True, vertical="top")


# ---------------- Scenario sheet ----------------
ws = wb.active
ws.title = "Scenarios"
ws["A1"] = "Single-business model: what does the owner actually keep? (ASSUMPTIONS - yellow cells editable)"
ws["A1"].font = B
hdr(ws, 3, ["Line", "Conservative", "Base", "Optimistic", "Note"])
rows = [
    ("Seller-reported SDE / cash flow ($/yr)", 300000, 300000, 300000, "Seller claim. NOT verified."),
    ("Haircut after quality-of-earnings review", 0.15, 0.05, 0.0, "Add-backs, owner pay, one-offs, cash-basis issues."),
    ("Verified SDE ($/yr)", "=B4*(1-B5)", "=C4*(1-C5)", "=D4*(1-D5)", ""),
    ("Purchase multiple of seller SDE", 3.5, 3.0, 2.6, "BizBuySell Q2-2026 avg cash-flow multiple ~2.7x (all sizes); managed/larger deals price higher."),
    ("Purchase price ($)", "=B4*B7", "=C4*C7", "=D4*D7", "Price is set off the seller's number."),
    ("Replacement manager - loaded cost ($/yr)", 120000, 100000, 85000, "BLS general/ops manager median ~$105.8k (May 2025); + ~20% burden for real GM."),
    ("Is manager already inside SDE? (1=yes, 0=no)", 0, 0, 1, "SDE normally ADDS BACK owner pay. If a manager already runs it, cost may already be deducted. Verify."),
    ("Capex / working-capital reserve (% of verified SDE)", 0.08, 0.05, 0.03, ""),
    ("Cash down incl. closing & working capital (% of price)", 0.25, 0.20, 0.12, "SBA SOP 50 10 8 requires >=10% cash injection on acquisitions."),
    ("Loan interest rate", 0.105, 0.1025, 0.10, "SBA 7(a) variable cap = prime(7.0%) + 3.0% for >$350k (NerdWallet Sep-2026 table). Verify with lender."),
    ("Loan term (years)", 10, 10, 10, ""),
    ("Owner cash invested ($)", "=B8*B12", "=C8*C12", "=D8*D12", ""),
    ("Loan amount ($)", "=B8-B15", "=C8-C15", "=D8-D15", "Not assumed approvable - lender decides."),
    ("Annual debt service ($)", "=-PMT(B13/12,B14*12,B16)*12", "=-PMT(C13/12,C14*12,C16)*12", "=-PMT(D13/12,D14*12,D16)*12", ""),
    ("Operating profit before manager ($/yr)", "=B6-B11*B6", "=C6-C11*C6", "=D6-D11*D6", "Verified SDE less reserve."),
    ("Profit after paying manager ($/yr)", "=B18-B9*(1-B10)", "=C18-C9*(1-C10)", "=D18-D9*(1-D10)", ""),
    ("Cash after debt service ($/yr)", "=B19-B17", "=C19-C17", "=D19-D17", "Pre-tax distributable cash."),
    ("  per month ($)", "=B20/12", "=C20/12", "=D20/12", "Target in brief: $12,000"),
    ("Est. taxable income ($)", "=B19-B16*B13-(B8-B11)*0+(-B8/15*0.9)", "=C19-C16*C13-C8/15*0.9", "=D19-D16*D13-D8/15*0.9", "Less interest and ~15-yr goodwill amortisation on 90% of price (simplified)."),
    ("Blended tax rate (assumption)", 0.30, 0.30, 0.30, "Fed+state+SE mix varies. Not tax advice."),
    ("Est. tax ($)", "=MAX(0,B22)*B23", "=MAX(0,C22)*C23", "=MAX(0,D22)*D23", ""),
    ("Owner take-home after tax ($/yr)", "=B20-B24", "=C20-C24", "=D20-D24", ""),
    ("  per month ($)", "=B25/12", "=C25/12", "=D25/12", ""),
    ("Cash-on-cash return on owner cash", "=B25/B15", "=C25/C15", "=D25/D15", ""),
    ("Debt service coverage (profit after mgr / debt)", "=B19/B17", "=C19/C17", "=D19/D17", "Lenders typically want >=1.25x; I did not verify each lender's floor."),
]
for i, r in enumerate(rows):
    rr = 4 + i
    for j, v in enumerate(r, 1):
        c = ws.cell(row=rr, column=j, value=v)
        if j in (2, 3, 4) and not (isinstance(v, str) and v.startswith("=")):
            c.fill = INP
ws["B22"] = "=B19-B16*B13-B8/15*0.9"  # clean formula (replaces placeholder)
for r in range(4, 31):
    for col in "BCD":
        c = ws[f"{col}{r}"]
        lab = ws[f"A{r}"].value or ""
        if any(k in lab for k in ["Haircut", "%", "rate", "return"]) and "multiple" not in lab:
            c.number_format = "0.0%"
        elif "multiple" in lab or "Debt service coverage" in lab:
            c.number_format = '0.00"x"'
        elif "years" in lab or "Is manager" in lab:
            c.number_format = "0"
        else:
            c.number_format = "#,##0"
ws.column_dimensions["A"].width = 52
for col in "BCD":
    ws.column_dimensions[col].width = 15
ws.column_dimensions["E"].width = 80

# ---------------- Required SDE solver ----------------
s2 = wb.create_sheet("Required_SDE")
s2["A1"] = "How big must the business be to leave $12,000/month cash AFTER manager + debt?"
s2["A1"].font = B
s2["A2"] = "Closed form: SDE = (Target + Manager) / (1 - reserve% - multiple x (1-down%) x debt-factor). Manager assumed NOT inside SDE."
inputs = [("Target cash after manager & debt ($/yr)", 144000), ("Manager loaded cost ($/yr)", 100000),
          ("Reserve % of SDE", 0.05), ("Down % of price", 0.20), ("Interest rate", 0.1025), ("Term (yrs)", 10)]
for i, (k, v) in enumerate(inputs):
    s2.cell(row=4 + i, column=1, value=k)
    c = s2.cell(row=4 + i, column=2, value=v)
    c.fill = INP
s2["A10"] = "Annual debt factor per $1 borrowed"
s2["B10"] = "=-PMT(B8/12,B9*12,1)*12"
hdr(s2, 12, ["Purchase multiple", "Required verified SDE ($/yr)", "Implied price ($)", "Owner cash needed ($)", "Loan ($)", "Check: cash after debt ($/yr)"])
for i, m in enumerate([2.0, 2.5, 3.0, 3.5, 4.0, 4.5]):
    r = 13 + i
    s2.cell(row=r, column=1, value=m).fill = INP
    s2.cell(row=r, column=2, value=f"=($B$4+$B$5)/(1-$B$6-A{r}*(1-$B$7)*$B$10)")
    s2.cell(row=r, column=3, value=f"=B{r}*A{r}")
    s2.cell(row=r, column=4, value=f"=C{r}*$B$7")
    s2.cell(row=r, column=5, value=f"=C{r}-D{r}")
    s2.cell(row=r, column=6, value=f"=B{r}-$B$6*B{r}-$B$5-E{r}*$B$10")
    for col in range(2, 7):
        s2.cell(row=r, column=col).number_format = "#,##0"
s2["B7"].number_format = s2["B6"].number_format = s2["B8"].number_format = "0.00%"
s2["B4"].number_format = s2["B5"].number_format = "#,##0"
s2["B10"].number_format = "0.0000"
for col, w in zip("ABCDEF", [44, 26, 18, 20, 16, 26]):
    s2.column_dimensions[col].width = w

# ---------------- Capital tiers ----------------
s3 = wb.create_sheet("Capital_Tiers")
hdr(s3, 1, ["Owner cash available", "What is realistically available", "What is NOT realistic", "Monthly cash it can plausibly produce (illustrative, pre-tax)"])
tiers = [
    ("$0 - $10k", "Nothing that meets the brief. Only options: save, or sweat-equity (which you've ruled out).",
     "Buying any business; SBA loans (10% cash injection minimum); 'seller finance 100%' deals are rare and unverifiable.",
     "$0 owner-absent. Money invested at ~4-8% yields $30-$80/mo per $10k."),
    ("$10k - $50k", "Small online asset or tiny micro-SaaS purchase - but these are owner-operated at that size. Public index/dividend funds.",
     "A business that pays a manager AND debt. Anything 'managed' at this price is typically managed by the seller.",
     "<$300/mo as an investor. As an owner you would be the operator."),
    ("$50k - $150k", "Down payment on a ~$250k-$750k small business via SBA 7(a) + seller note. Business has ~$80k-$250k SDE: enough for ONE owner-operator, not owner + manager + debt.",
     "A $12k/mo owner-absent outcome. After a ~$100k manager there is little left.",
     "Roughly $0-$4k/mo after manager and debt in the base case (see Scenarios)."),
    ("$150k - $500k", "Down payment (15-25%) on a $1M-$2.5M business with $350k-$800k SDE and a real GM in place. First tier where the brief is mathematically possible.",
     "Buying with 100% leverage; assuming approval; tolerating a weak GM / key-man risk.",
     "Base case ~ $8k-$14k/mo pre-tax if verified SDE ~ $450k-$550k at ~3x. High variance."),
    ("$500k - $2M", "Buy 1-2 businesses outright or with low leverage; or buy a larger (~$1M+ EBITDA) company; or co-invest as limited partner with an operator.",
     "Treating it as passive: someone still must run it and you must monitor it.",
     "Low-leverage version of above; less risk of ruin, lower return on cash."),
    ("$2M+ (investment route, D)", "Professionally managed assets: public REITs/dividend funds (~3.5-6% yield per sources), private credit (7-12% claimed, default risk), direct real-estate with a property manager.",
     "'Guaranteed' income. Principal can fall; 'passive' funds still need your selection & tax work.",
     "$12k/mo = $144k/yr needs ~$2.4M at 6%, ~$3.6M at 4%, ~$1.2-2.1M at 7-12% private-credit claims (higher loss risk)."),
]
for i, t in enumerate(tiers):
    for j, v in enumerate(t, 1):
        c = s3.cell(row=2 + i, column=j, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
for col, w in zip("ABCD", [22, 60, 55, 55]):
    s3.column_dimensions[col].width = w

# ---------------- Lead evaluator ----------------
s4 = wb.create_sheet("Lead_Evaluator")
s4["A1"] = "Unverified leads from search-result snippets (not vetted, not contacted). Paste real listing numbers into yellow cells."
s4["A1"].font = B
hdr(s4, 3, ["Lead", "Asking price", "Seller cash flow ($/yr)", "Manager cost already deducted? (1/0)", "Manager cost if not ($/yr)",
            "Multiple", "Cash flow after manager", "Debt service (80% @10.25%/10y)", "Cash after debt ($/yr)", "per month", "Status"])
leads = [
    ("Absentee liquor store, Cheshire CT (BizBuySell snippet)", 860000, 200700, 0, 85000, "Ask and cash flow from snippet only; manager treatment unknown."),
    ("Sacramento-area pizza franchise, manager ~$78-80k (BizBuySell snippet)", 300000, None, 1, 0, "Cash flow not shown. Franchise fees/royalties and franchisor approval to check."),
    ("Queens NY burger shop, absentee w/ manager, ~$160k net (snippet)", None, 160000, 1, 0, "Ask not shown."),
]
for i, (n, ask, cf, inc, mgr, note) in enumerate(leads):
    r = 4 + i
    s4.cell(row=r, column=1, value=n)
    for col, v in ((2, ask), (3, cf), (4, inc), (5, mgr)):
        c = s4.cell(row=r, column=col, value=v)
        c.fill = INP
    s4.cell(row=r, column=6, value=f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),B{r}/C{r},"n/a")')
    s4.cell(row=r, column=7, value=f'=IF(ISNUMBER(C{r}),C{r}-IF(D{r}=1,0,E{r}),"n/a")')
    s4.cell(row=r, column=8, value=f'=IF(ISNUMBER(B{r}),-PMT(0.1025/12,120,B{r}*0.8)*12,"n/a")')
    s4.cell(row=r, column=9, value=f'=IF(AND(ISNUMBER(G{r}),ISNUMBER(H{r})),G{r}-H{r},"n/a")')
    s4.cell(row=r, column=10, value=f'=IF(ISNUMBER(I{r}),I{r}/12,"n/a")')
    s4.cell(row=r, column=11, value=note)
    for col in (2, 3, 5, 7, 8, 9, 10):
        s4.cell(row=r, column=col).number_format = "#,##0"
    s4.cell(row=r, column=6).number_format = '0.00"x"'
s4.column_dimensions["A"].width = 62
for col in range(2, 11):
    s4.column_dimensions[get_column_letter(col)].width = 17
s4.column_dimensions["K"].width = 70

# ---------------- Due diligence ----------------
s5 = wb.create_sheet("Due_Diligence")
hdr(s5, 1, ["Area", "Document / test", "Invalidates the deal if..."])
dd = [
    ("Earnings", "3 yrs federal tax returns (as filed) + P&Ls + bank statements; independent quality-of-earnings (QoE)", "Tax returns and P&L disagree by >10% with no clean explanation; add-backs are mostly personal/undocumented."),
    ("Earnings", "Monthly bank deposits vs reported revenue; processor (Stripe/Square/PayPal) reports", "Deposits < reported revenue, or heavy cash revenue that is not banked."),
    ("Owner dependence", "Seller's weekly calendar; who holds client/vendor relationships, licenses, keys, passwords", "Seller personally sells, services or supervises core work; customers name the seller as the reason they buy."),
    ("Management", "Org chart, W-2/1099 roster, tenure, pay, non-competes; interview GM (with seller consent)", "GM is a family member, underpaid vs market (will leave/need raise), or has no authority/bank access."),
    ("Management", "Replacement-cost quote: market salary for GM + bonus + burden", "Profit after market-rate GM is below ~1.5x debt service."),
    ("Customers", "Customer list by revenue (top 10), churn/cohort data, contract terms, refunds/chargebacks", "Any customer >20% of revenue without contract; churn rising; refund rate high."),
    ("Operations", "SOPs, training docs, software/vendor contracts, equipment list and condition", "No documented procedures: tribal knowledge lives in seller's head."),
    ("Legal", "Entity docs, licenses, litigation search, liens (UCC), lease assignment, franchise approval", "Lease not assignable, license not transferable, active claims, franchisor refuses transfer."),
    ("Debt / structure", "Lender term sheet, DSCR calc, seller-note terms, earn-out clauses", "Financing is assumed rather than committed; DSCR <1.25x after market GM."),
    ("Transition", "Seller transition period (60-180 days) & non-compete agreement in writing", "Seller refuses transition/non-compete or wants to exit immediately."),
]
for i, t in enumerate(dd):
    for j, v in enumerate(t, 1):
        s5.cell(row=2 + i, column=j, value=v).alignment = Alignment(wrap_text=True, vertical="top")
for col, w in zip("ABC", [20, 70, 70]):
    s5.column_dimensions[col].width = w

wb.save("/home/user/rewired-mind/owner-absent-business/owner_absent_acquisition_model.xlsx")
print("saved")
