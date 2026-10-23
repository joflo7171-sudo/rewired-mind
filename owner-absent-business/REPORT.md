# Owner-Absent Business: Research Report

Prepared 2026-10-23. Companion workbook: `owner_absent_acquisition_model.xlsx` (rebuild with `build_model.py`).

## 0. What this report is and is not

- **Not verified:** I could not open Empire Flippers, BizBuySell, Acquire.com or Flippa. The sandbox's network policy blocks those hosts (DNS failure and HTTP 403 on the proxy tunnel). Everything below comes from web-search summaries, mostly secondary sources.
- **No vetted opportunities.** The three "leads" in section 4 are search-snippet fragments. No seller was contacted, no document was seen, and no earnings were confirmed.
- **Modeled numbers are assumptions.** The workbook inputs (yellow cells) are not market data. They show what a deal must look like, not what a deal exists.
- Sources: [BizBuySell Q2/Q3 2026 Insight](https://finviz.com/news/404656/bizbuysell-releases-q3-2026-insight-report), [Empire Flippers annual-multiples notice](https://empireflippers.com/switching-to-annual-multiples/), [Empire Flippers scoreboard](https://empireflippers.com/scoreboard/), [SBA 7(a) equity-injection summary](https://angelinvestorsnetwork.com/capital-raising/sba-7a-acquisition-financing-rules-2026), [NerdWallet SBA rates](https://www.nerdwallet.com/business/loans/learn/sba-loan-rates), [BLS general/operations manager pay (aggregator)](https://wagedex.com/card/general-and-operations-managers), [search-fund outcome data (secondary)](https://www.viaductus.de/en-US/knowledge/business-succession/search-funds/success-rates).

## 1. The core arithmetic

Reported by search results:

| Fact | Value | Confidence |
|---|---|---|
| Average cash-flow multiple, small businesses (BizBuySell Q2 2026) | ~2.7x | Medium (averages, all sizes) |
| Median sale price / median cash flow (Q2 2026) | ~$349k / ~$156k | Medium |
| SBA 7(a) cash injection for an acquisition | at least 10% of project cost | Medium (lender blogs, not SBA text) |
| SBA variable rate cap, loans over $350k | prime (7.0%) + 3.0% = 10.0% | Medium (Sep 2026 table) |
| General/operations manager median pay | ~$105.8k (May 2025) | Medium (aggregator citing BLS) |
| Empire Flippers typical multiple | ~26x monthly profit, i.e. ~2.2x annual | Low (scoreboard may be stale; EF moved to annual multiples Sept 2026) |

**What follows from them** (workbook tab `Required_SDE`, $100k loaded manager, 20% down, 10.25% over 10 years, 5% reserve):

| Purchase multiple | Verified SDE needed for $12k/mo cash | Price | Owner cash |
|---|---|---|---|
| 2.5x | ~$388k | ~$0.97M | ~$194k |
| 3.0x | ~$432k | ~$1.29M | ~$259k |
| 3.5x | ~$487k | ~$1.70M | ~$341k |
| 4.0x | ~$558k | ~$2.23M | ~$446k |

**The median small business cannot do this.** At ~$156k cash flow, a $100k manager leaves about $50k before debt, and debt on a ~$350k price is about $45k a year. That is roughly break-even. A business that only makes sense with you working in it does not become passive by hiring a manager.

## 2. Ownership models compared

| Model | Fits the brief? | Why |
|---|---|---|
| **C. Local/service business with an existing GM** (priced about $1M–$2.5M) | **Best fit, if one is found and verified** | Employees, customers and procedures already exist. Risk is key-person dependence and the GM's loyalty. |
| **B. Subscription/software with outsourced support** | Possible, but harder to buy at this size | Small SaaS is usually founder-run. Acquire.com-style listings are mostly owner-operated, and my one source's figures did not reconcile internally. Treat multiples as unverified. |
| **A. Online business (content, ecommerce, apps)** | Weak | Most are owner-managed or contractor-managed. "Fully managed" claims need a team roster and a 90-day owner time log. Platform risk (Google, Amazon) is large. |
| **D. Professionally managed assets** | Only route that is truly hands-off | Needs about $2.4M at 6% or about $3.6M at 4% for $144k/yr pre-tax. Higher-yield private credit (7–12% claimed) carries default and liquidity risk. No guarantee of income. |

## 3. Capital scenarios (workbook tab `Capital_Tiers`)

- **Under about $50k:** the goal is not feasible as an owner-absent business. Saying otherwise would depend on unpaid labor or unrealistic returns.
- **$50k–$150k:** you can buy a business, but it will be a small owner-operator business, not an absentee one.
- **$150k–$500k:** the first tier where the math can work, via one managed business at about $1M–$2.5M with SBA financing. High variance. Approval is not assumed.
- **$500k–$2M:** lower leverage, or two businesses, or a larger company. More resilient.
- **$2M+:** the investment route becomes credible.

## 4. Specific leads (unverified; for screening practice only)

Source: BizBuySell search snippets, not opened or confirmed.

| Lead | What the snippet said | What I computed (tab `Lead_Evaluator`) | Verdict |
|---|---|---|---|
| Absentee liquor store, Cheshire CT | ~$200.7k cash flow, ask ~$860k | 4.3x. If a $85k manager is not already deducted: ~$5k a year after debt | Fails as stated, unless the cash flow is already after a manager and the price is negotiated down. |
| Sacramento-area pizza franchise | ask $300k, manager paid $78–80k, owner financing | Cash flow not shown | Cannot evaluate. Franchise royalties and franchisor transfer approval are the first questions. |
| Queens NY burger shop | ~$160k "net", manager in place | Ask not shown | Cannot evaluate. Even if net is after the manager, the owner's cash after debt depends entirely on price. |

I do **not** have three vetted opportunities, so I cannot honestly rank them. All three sit in the restaurant/retail category, which is operationally hard to leave to a manager.

## 5. Recommended path (conditional)

**Preferred:** acquire one established, manager-run business with **verified SDE of roughly $400k–$550k**, priced around 3x, financed with SBA 7(a) plus a seller note, with a documented GM and a 60–180 day seller transition. Candidate categories to screen: B2B recurring services, maintenance and compliance services, and property-adjacent services. Avoid restaurants, retail and single-customer businesses.

**Why not the others:** online businesses (A) are usually operator-dependent; small SaaS (B) has founder dependence and unverified multiples; investment assets (D) are safest but need several times the capital for the same income.

**Honest caveat on lenders:** whether an SBA lender will finance a buyer who plans to be absentee is **unconfirmed** in my sources. Lenders often want the buyer to be active, and 20%+ owners must personally guarantee. Ask before spending on diligence.

## 6. Owner-absent operating plan

| Role | Who does it | Rough cost |
|---|---|---|
| General manager (daily operations, hiring, vendors) | Hired or retained employee | $85k–$120k loaded |
| Bookkeeping and monthly close | Outsourced bookkeeper | ~$6k–$15k/yr (estimate) |
| Sales and customer service | Existing staff | Already in the cost base |
| Legal, banking authority, taxes, major hires, debt covenants, approving large spend | **You** | Legal and CPA fees ~$5k–$15k/yr (estimate) |

**Time reality:** 15 minutes a week is a steady-state aspiration, not a starting point. Plan on several hours a week for 6–12 months while you check the GM, the books and the bank, then perhaps 1–3 hours a month with a monthly dashboard. Emergencies take more.

## 7. Scenarios for one business (tab `Scenarios`, seller claim $300k SDE)

| | Conservative | Base | Optimistic |
|---|---|---|---|
| Verified SDE | $255k | $285k | $300k |
| Price | $1.05M | $0.90M | $0.78M |
| Owner cash in | $263k | $180k | $94k |
| Cash after manager and debt, per month | **-$1.1k** | **~$4.6k** | **~$15.2k** |
| Take-home after tax (30% assumed), per month | -$1.1k | ~$3.5k | ~$10.8k |
| Debt coverage | 0.90x | 1.48x | 2.67x |

The optimistic case assumes the manager's pay is already inside the reported SDE and the price is 2.6x. Those two assumptions drive the result, which is why they are the first things to verify.

At about $4k a month of base-case cash per business, **reaching $12k a month would take about three such businesses or one much larger one.** These are projections, not guaranteed income.

## 8. Due diligence

See tab `Due_Diligence`. Walk away if tax returns and P&Ls disagree, bank deposits don't match revenue, the seller personally sells or services the core work, the GM is unpaid-for-market or a relative, one customer exceeds 20% of revenue, the lease or license can't transfer, or profit after a market-rate GM is below about 1.5x debt service.

## 9. Final answers

1. **Best realistic path:** buy one manager-run business with about $400k–$550k verified SDE through a broker with SBA financing. Fall back to professionally managed assets if you have $2M+.
2. **Capital:** about $190k–$450k of your own cash for that deal ($0.97M–$2.2M price). Under about $150k, this goal is not feasible.
3. **Evidence it makes money:** none yet. No listing was verified. You need 3 years of filed tax returns, bank statements, and an independent quality-of-earnings review.
4. **What you pay others to do:** a GM ($85k–$120k loaded), a bookkeeper and a CPA/attorney. Expect to do the final checks yourself at first.
5. **Monthly profit left:** about -$1k to $15k pre-tax per business, with a base case near $4.6k. $12k a month is possible but not the typical outcome.
6. **Biggest ways to lose money:** overpaying on inflated add-backs, the GM leaving, customer concentration, debt service exceeding cash flow, and a lender declining an absentee buyer.
7. **First decision:** the maximum amount of cash you can lose without hurting your life. If it is under about $150k, don't buy; if it is above, authorize the next research step.

## 10. Next steps (all need your approval)

1. Tell me your loss-tolerant capital ceiling.
2. Give me listing pages or exports (the sandbox cannot reach the marketplaces), or approve a different research route.
3. I will screen real listings with the workbook and draft diligence requests for you to review before anything is sent.
