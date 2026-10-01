# Support email setup: support@getoperatorgrid.com

**Status: NOT CREATED.** No mailbox exists and no DNS record has been changed. The website and the buyer ZIP keep their support placeholders until every test in section 5 passes.

## 1. What this address must do
| Requirement | Why |
|---|---|
| **Receive** mail at support@getoperatorgrid.com | Buyer questions, refund requests, "file won't open" reports |
| **Send/reply as** support@getoperatorgrid.com, not from a personal address | Professional, consistent with the brand. It also keeps your personal identity and other brands separate. |
| Land in the inbox, not spam (SPF, DKIM and DMARC pass) | Replies to customers must arrive |
| Usable on your phone | Fast responses before and after launch |
| Kept fully separate from Rewired Mind and your other brands | Your brand-separation rule |

## 2. Provider options (pick one; nothing has been purchased)
| Option | Cost | Send as support@ | Notes |
|---|---|---|---|
| **A. Your domain registrar's included email** (if your registrar bundles a mailbox) | Often $0 with the domain | Yes | Check your registrar's dashboard first. This is the simplest option if it's available. |
| **B. Zoho Mail free plan** (custom domain) | $0 *(verify the current plan limits on Zoho's site)* | Yes (web and mobile app) | A good no-cost choice. The free plan has historically had restrictions (e.g. on IMAP or forwarding), so check before choosing. |
| **C. Google Workspace or Microsoft 365** | Paid monthly per user | Yes | The most polished option, but a recurring cost that needs your approval. |
| **D. Forward-only routing** (e.g. Cloudflare Email Routing or registrar forwarding) to an existing inbox | $0 | **Not by itself.** Sending as support@ needs an outgoing mail server for the domain. | Receive-only isn't enough for support replies, so don't use this alone. |

**Recommendation:** A if your registrar includes a mailbox, otherwise B. Both cost $0 and both can send as support@. Move to C later if volume justifies it.

## 3. DNS records you will add (only when you're ready; no changes have been made)
The exact values come from the provider you pick. The record **types** are always:

| Record | Host / name | Purpose |
|---|---|---|
| **TXT** (verification) | `@` or as instructed | Proves you own the domain to the mail provider |
| **MX** (usually 2–3 records with priorities) | `@` | Routes incoming mail to the provider |
| **TXT, SPF** | `@` | Authorizes the provider to send for the domain, e.g. `v=spf1 include:<provider-domain> ~all`. Only **one** SPF record is allowed per domain. If the payment or host provider ever sends mail as your domain, add it to the same record. |
| **TXT or CNAME, DKIM** | `<selector>._domainkey` | Cryptographic signing of outgoing mail (the provider generates it) |
| **TXT, DMARC** | `_dmarc` | Start with `v=DMARC1; p=none; rua=mailto:support@getoperatorgrid.com`. After 2–4 weeks of passing reports, tighten to `p=quarantine`. |

Important:
- Find out **where your DNS is hosted** (registrar or another DNS provider) before adding anything.
- When the website is hosted later, the web records (A/CNAME) get added **alongside** these mail records. Never replace the MX/TXT records when connecting the website.
- If you ever move nameservers, copy every mail record over first.

## 4. Mailbox settings
- **Display name:** `OperatorGrid Support`
- **Signature (draft):**
  > OperatorGrid Support
  > getoperatorgrid.com
- **Auto-reply (optional, draft):** "Thanks for contacting OperatorGrid. We've received your message and reply within [X business days]." Only promise a response time you can keep.
- **2-step verification** on the mailbox account, using a password you don't use anywhere else.
- **Folders/labels:** Pre-sale · Order help · Refunds · Bug reports

## 5. Tests before the address is used anywhere (all must pass)
| # | Test | Pass condition |
|---|---|---|
| 1 | Send **to** support@ from an outside Gmail account | Arrives in the inbox within minutes |
| 2 | Send to support@ from an outside Outlook/Hotmail account | Arrives |
| 3 | **Reply from** support@ to both | Arrives in their **inbox, not spam**, showing "OperatorGrid Support" |
| 4 | Open the received message's headers (in Gmail: "Show original") | SPF = PASS, DKIM = PASS, DMARC = PASS |
| 5 | Send one message to a free deliverability checker (e.g. mail-tester.com) | Score of 9/10 or higher, or the issues it lists are fixed |
| 6 | Send and receive on your phone | Works |
| 7 | Send a test with a ~3 MB attachment | Received (customers may send screenshots) |

## 6. Only after all tests pass: replace the placeholders
| Location | Placeholder |
|---|---|
| `operatorgrid-site/index.html` FAQ "How do I get support?" | `[Support email added after…]` |
| `operatorgrid-site/index.html` Support section | `[support email, added once…]` |
| Legal pages (privacy, refunds, terms) | `[support email]` contact lines |
| `READ-ME-FIRST.txt` inside the buyer ZIP | `Support: [your support email]` |
| Stripe account → Public details → Support email | Set to support@getoperatorgrid.com |

Changing READ-ME-FIRST.txt changes the ZIP, so the ZIP must be **rebuilt and re-audited** (the workbooks stay unchanged). I can do that once you confirm the tests passed.
