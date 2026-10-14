# Domain setup: shadowworkacademy.org

> **Hold:** the name, and therefore this domain, has an unresolved trademark risk (`TRADEMARK-AND-COPYRIGHT-CHECK.md`). Do not deploy or point DNS until counsel advises.

Intended primary domain: **https://shadowworkacademy.org/** (apex, no `www`). Nothing in this document has been executed. I have not changed DNS, deployed, published, or purchased anything.

## 1. What I verified (read-only) and what I could not

| Question | Answer | How |
|---|---|---|
| Is the code configured for the new domain? | ✅ Yes | Canonical, `og:url`, `og:image`, sitemap, robots and structured data on every page use `https://shadowworkacademy.org/`. `tools/launch-check.py` enforces this. |
| Any old-domain references in the production build? | ✅ None | No `rewiredmind.org/shadow-work-academy` anywhere in `dist/site`. The only `rewiredmind.org` references left are intentional: the "A product of Rewired Mind" link to `https://rewiredmind.org` and the `support@rewiredmind.org` address. |
| Is the domain connected to hosting? | ❌ **No evidence it is** | Your Netlify account (team "Rewired Mind", you are Owner) has 10 sites; none uses `shadowworkacademy.org` (primary URLs seen: `rewiredmind.org`, `quiz.rewiredmind.org`, `cashcommandos.com`, `getoperatorgrid.com`, `badgeworksstudio.com`, and several `*.netlify.app`). The read tools do not list alias domains or DNS zones, so a domain alias or DNS zone I can't see is possible but unlikely. |
| Do you control its DNS? | ❓ **Unknown, I cannot check** | This environment cannot resolve or reach the domain (outbound proxy denies it) and I have no registrar access. Confirm in §2. |
| Is the site live there? | ❌ No | The domain returned nothing from here; no deploy exists. |
| Checkout/delivery separate from the website domain? | ✅ By design | Purchase links go to Gumroad (a different host) and `launch-check.py` fails if the checkout URL is ever on `shadowworkacademy.org`. The site only hosts the sales pages, legal pages, a free sample PDF and a thank-you page; **the paid files are never hosted on the website**. |
| Rewired Mind site and quiz funnel untouched? | ✅ | `git diff` shows no file outside `shadow-work-academy/` changed. No Netlify site was modified. |

## 2. Questions to answer first
1. **Where is the domain registered**, and are you logged in as the owner (registrar account, 2FA, WHOIS contact)?
2. **Who hosts its DNS right now?** (Registrar's default nameservers, Cloudflare, Netlify DNS?) Look at the domain's NS records at your registrar.
3. Are there **existing records** (MX for email forwarding, parked-page A/AAAA, CAA) that must be kept or removed?
4. Is **domain auto-renew** on, and is the registrar lock/transfer-lock on?

## 3. Recommended hosting: a new, separate Netlify project
This mirrors how your other products are hosted (each product its own Netlify project, e.g. `cash-command-os` → `cashcommandos.com`) and keeps `rewiredmind-home` and the quiz untouched.
1. **Approval needed from you** before I (or you) create it. Create project `shadow-work-academy`, deploy the contents of `dist/site/` (built by `python3 tools/package.py`; includes `_headers` with a strict Content-Security-Policy and `404.html`). Deploy only after the Gumroad URL and legal approvals are in (`LAUNCH-READINESS.md`).
2. Add the custom domain `shadowworkacademy.org` in the project's domain settings, and add `www.shadowworkacademy.org`. Set the **apex as primary** and let `www` redirect to it (the site's canonical URLs assume the apex).
3. Configure DNS using **one** of:

### Option A: Netlify DNS (simplest, Netlify manages records)
At the registrar, change the nameservers to the four Netlify provides in the domain panel. Then re-create any records you need to keep (e.g. MX). Changes at the registrar can take up to 48 hours.

### Option B: keep DNS where it is (external DNS)
Per Netlify's documentation ([Configure external DNS](https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/)); confirm the exact values in your Netlify domain panel before entering them:

| Host | Type | Value |
|---|---|---|
| `@` (apex) | **ALIAS / ANAME / flattened CNAME** if your DNS provider supports it | `apex-loadbalancer.netlify.com` |
| `@` (apex) | **A** (only if no ALIAS support) | `75.2.60.5` |
| `www` | **CNAME** | `<your-project-name>.netlify.app` |

Rules: an apex cannot be a plain CNAME. **Delete conflicting records** (registrar parked-page A records, any AAAA/IPv6 record: Netlify's load-balancer IP does not support IPv6). Keep MX/TXT records that email depends on. Netlify notes that using the apex with external DNS does not get direct-DNS CDN routing; if performance matters later, consider Option A or a `www` primary.

## 4. HTTPS
* Netlify provisions a free TLS certificate (Let's Encrypt) automatically once DNS points at it; no purchase needed. In the domain panel use **Verify DNS** then **Provision certificate**, and turn on **Force HTTPS**.
* If the domain has a **CAA** record, it must allow `letsencrypt.org`, or issuance fails.
* Add an **HSTS** header only *after* HTTPS works on both apex and `www` (it is deliberately not in `_headers` yet, because enabling it early can lock browsers out if something is misconfigured).

## 5. Email
This setup does not touch email. Support stays on `support@rewiredmind.org`. Do not remove existing MX records on `shadowworkacademy.org`. If you later want `support@shadowworkacademy.org`, that needs its own mail setup (MX, SPF, DKIM, DMARC) and a copy change in the site, legal pages, START-HERE and the Gumroad text. Until then, no mail-related DNS records are required.

## 6. Verification checklist after DNS is changed (with your approval)
- [ ] `dig +short NS shadowworkacademy.org` and `dig +short A shadowworkacademy.org` show the intended provider/IP; `dig +short CNAME www.shadowworkacademy.org` shows the Netlify name.
- [ ] `curl -I https://shadowworkacademy.org/` → `200`, valid certificate; `http://` redirects to `https://`; `www` redirects to the apex.
- [ ] `curl -I https://shadowworkacademy.org/404-test` → custom 404 page.
- [ ] View source: canonical/`og:url` point at the apex; `https://shadowworkacademy.org/sitemap.xml` and `/robots.txt` load.
- [ ] Response headers include the CSP from `_headers`; the site still renders (no blocked resources in the browser console).
- [ ] Re-run `node tools/qa.js` with the site base pointed at the live URL, and click the real checkout button.
- [ ] Add the property in Google Search Console and submit the sitemap (optional; no tracking added to the site).
- [ ] Confirm `rewiredmind.org` and `quiz.rewiredmind.org` still load exactly as before.

## 7. Rollback
Remove the custom domain from the Netlify project (or restore the previous DNS records you noted before changing them). Nothing else depends on this domain.

## 8. If the domain ever changes again
`python3 tools/configure.py --site-base https://NEWDOMAIN/` rewrites canonical, `og:*`, sitemap, robots and structured data, then rebuilds. `tools/launch-check.py` then verifies it (update the `DOMAIN` constant in that file).
