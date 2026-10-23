# Decision Report: Which business, and why

*Prepared 2026-10-23. Nothing here is a result; no customer has been contacted, no sale has occurred.*

## Verdict
**Your starting hypothesis (missed-call / AI-receptionist revenue recovery for home-service contractors) is rejected as a standalone business.** The software contractors already pay for now sells it as a cheap add-on, so a newcomer has no pricing power.

**Winner: "Estimate Desk" — a managed service that follows up on unsold estimates for independent residential HVAC contractors, paid by a small fixed fee plus a commission on jobs it helps close.** Fallback if its pilots fail: Candidate C (invoice follow-up for specialty subcontractors).

Evidence quality is the main weakness: almost every number below is vendor-published. Independent proof does not exist yet. The pilot is what generates it.

## Evidence (source → what it proves → label)
Labels: **V** verified in a source I saw (secondary unless stated) · **I** inference · **A** unverified assumption · **T** needs a test.

| # | Claim | Source | What it proves | Label |
|---|---|---|---|---|
| 1 | Jobber sells an AI Receptionist at $29/mo (30 conversations, $0.79 overage); included free on its Plus plan; it texts back callers who hang up | [Jobber help center](https://help.getjobber.com/en/articles/receptionistpowered-by-jobber-ai/) (via search; a second Jobber article says 100 conversations, so limits conflict) | Missed-call recovery is commoditized inside the software contractors already own. Price ceiling is tiny. | V |
| 2 | Housecall Pro offers 24/7 AI call answering as a paid add-on; base plans listed ~$59–$329/mo; add-on price not published | [Housecall Pro](https://www.housecallpro.com/features/ai-team/) (via search) | Same: incumbents bundle it. | V |
| 3 | Standalone text-back tools ~$15–$100/mo; AI receptionists from ~$49/mo (Rosie); human answering from ~$250/mo for 50 min (Ruby) | Third-party comparison blogs, partly vendor-written ([example](https://www.getaira.io/blog/missed-call-text-back)) | Customers do pay for call handling, but at prices a reseller can't build a business on. | V (weak) |
| 4 | Booking rate on inbound calls: ~38% HVAC; 24% for shops under 5 techs vs 59% for 25+ techs (2022 data) | [ServiceTitan blog](https://www.servicetitan.com/blog/data-call-booking-rates) (via search; I did not open the page) | Small shops leave a lot of demand unconverted — headroom exists. Does **not** isolate estimates. | V (weak) |
| 5 | Contractors pay ~$69 (plumbing) / ~$80 (HVAC) per Google Local Services lead; HVAC Google Ads blended CPL ~$104 (816 contractors, Jan 2026) | [Media Captain](https://themediacaptain.com/google-local-service-ad-statistics/), [The Ad Spend](https://theadspend.com/blog/google-ads-search-hvac) | Every unsold estimate already carried real acquisition cost. | V (vendor data) |
| 6 | Contractor marketing retainers ~$1,500–$8,000/mo; reactivation/follow-up products listed at $297–$599/mo | [ClicksGeek](https://clicksgeek.com/lead-generation-service-cost/) and vendor pages (via search) | Contractors already pay for adjacent services; a $750–$1,000 fee is inside the observed range. | V (vendor list prices) |
| 7 | Unsold-estimate recovery of 15–30% and 2x close-rate gains after follow-up | Vendor blogs ([example](https://ustechautomations.com/resources/blog/home-services-chase-unsigned-estimates-with-timed-followups-recipe-2026)) | **Nothing reliable.** Unsourced marketing claims. | A / T |
| 8 | Subcontractors wait ~51 days (Billd 2026, 600+ respondents) / 59% wait 46+ days (Siteline 2026, ~500 finance pros) | [Siteline](https://www.siteline.com/blog/youre-not-behind-the-whole-industry-is-built-this-way) and Billd, via search | Candidate C's problem is real and urgent (commercial, not residential). | V |
| 9 | Outsourced AR follow-up: VA $1,000–$2,500/mo; hybrid models 25–35% of recovered old debt | Vendor pages ([Stealth Agents](https://stealthagents.com/alternatives/alternatives-to-a-collection-agency)) | Candidate C has observable retainer pricing. | V (vendor) |

**Could not obtain:** Census County Business Patterns counts (the sandbox blocked api.census.gov and direct vendor sites, so I relied on search summaries). I give **no market size**. Pull NAICS 238220 establishment counts on data.census.gov before any claim about market size.

**Main inference (I):** a contractor who already paid ~$100 to generate a lead and then sent an estimate is more likely to pay for follow-up than for cold marketing. Nobody has confirmed this. It is the first thing the discovery calls must test.

## Ranking (my judgment scores, 1–5, not data)
| Criterion | A: Missed-call/AI receptionist | **B: Estimate Desk** | C: Invoice follow-up |
|---|---|---|---|
| 1 Evidence customers spend | 4 | 3 | 3 |
| 2 First customer fast | 3 | 4 | 3 |
| 3 Capital needed | 5 | 5 | 5 |
| 4 Recurring revenue & margin | 2 | 4 | 4 |
| 5 Measurable value | 3 | 5 | 5 |
| 6 Competition / acquisition difficulty | 1 | 3 | 3 |
| 7 Hireable / automatable | 4 | 4 | 4 |
| 8 Risk / legal / owner involvement | 4 | 3 | 2 |
| 9 Long-term company value | 1 | 3 | 4 |
| **Total** | **27** | **34** | **33** |

B beats C by one point, which is within my scoring noise. B wins on tie-breakers: the buyer is the owner (one decision-maker), results are visible in the contractor's own quote system, and the legal exposure is lower than collections. C is the better long-term company if B fails.

## Primary risks
1. **The core number is unproven.** If few unsold estimates close on follow-up, there is no business. The model's conservative case needs ~9 clients for $1,000/mo profit.
2. **Attribution disputes.** Commission only works if the contractor's own system proves the job closed after our touch.
3. **Texting/calling law (TCPA, state laws).** See `03-prospecting-and-outreach-kit.md`. Not legal advice; get an attorney to review the contract and scripts.
4. **Software encroachment.** Jobber/Housecall automate quote follow-up. We must win on human judgment and persistence, not automation.
5. **Owner-time ceiling.** Until a coordinator is hired, delivery hours cap you at roughly 8–10 clients.

## What is still uncertain
Real close rates on follow-up; real average job value; whether owners will accept commissions; whether HVAC owners respond to cold outreach; competitor local agencies' actual follow-up pricing; market size.
