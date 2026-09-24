# Rich results checkpoint — 2026-09-24 (source implementation)

## State
- Repo: `joflo7171-sudo/rewiredmind-home` (access restored this session)
- **Live production = locked branch deploy of `schema-fixes` @ be15510** (Netlify deploy 6ab52d0fb39ec60008b8f226), not `main` (21fc04d, older snapshot).
- Cleanup branch: `product-rich-results-source-fix` @ 6fd6436, **based on be15510** so the live fixes are kept (Confidence Reset review/aggregateRating removal, `/reset` redirect → lowercase PDF). A branch built from `main` would have brought both back.
- Old branch `product-rich-results-cleanup` (PR #2): superseded. It was built from `main`, rewrote Book offers into `workExample` and changed `netlify.toml`, all outside this batch. Don't merge it.

## Changes (9 pages, 18 fields; JSON-LD only)
Removed `Offer.shippingDetails` ($0 USD, 0-day handling/transit) from every Amazon offer, plus the books2read offer on the Dating Guide. Nothing replaced them.
Kept Gumroad `shippingDetails` on owned digital downloads (8 pages marked no-fix, plus Confidence Reset and Transformation System).

## Edition URL inconsistencies
1. The Confidence Habit paperback: the schema uses `amazon.com/dp/B0HCRJXJM6`. The visible link goes to the same ASIN but adds Amazon Attribution `maas` params. Resolved with no change: both land on the same edition. The clean URL stays in the schema, and the tracked visible link stays so analytics keep working.
2. **Open.** A systematic schema-vs-visible diff found no second mismatch on the 9 pages, and the original checkpoint listing it wasn't available. Needs the original note.

## Direct-PDF offers: left unmarked (unverified)
- Dating Guide: Gumroad $14.99
- Stop Overthinking: Gumroad $2.99
- Confidence Habit: Gumroad $3.99

therewiredmind.gumroad.com is blocked by the environment's egress policy, so price, currency and availability couldn't be checked live.

## Validation
- JSON-LD parses on all 17 book pages plus /books/, /, /merch (PASS)
- The only semantic diff from live is the 18 removed shippingDetails (PASS)
- Non-JSON-LD HTML is byte-identical to live source on every page (PASS)
- Every remaining Offer has price, priceCurrency, availability and url; no Review or AggregateRating present (PASS)
- Branch preview (expected): https://product-rich-results-source-fix--rewiredmind-home.netlify.app. **Unverified**: *.netlify.app and rewiredmind.org are egress-blocked from this environment.

## Follow-ups (not in this batch)
- anxious-texting, decision-paralysis-in-love and the-jealousy-spiral show a visible Kindle edition with no Offer
- Production stays locked. No publish or promote. Fourthwall on hold.
