"""AI Workflow Library content (original). Each workflow: id, title, when, inputs, prompt, review, sheet."""

GUARDRAILS = [
    "AI drafts; you decide. Read every draft before you send it.",
    "Never paste passwords, door/lockbox codes, alarm codes, payment card numbers or ID numbers into an AI tool.",
    "Share only what the message needs: first name and job details are usually enough.",
    "AI must not make legal, safety, tax, accounting, insurance, hiring, pay or regulatory decisions. Those prompts are deliberately excluded — ask a qualified professional.",
    "AI can be confidently wrong. Check prices, dates, times and promises against your workbook before sending.",
    "Do not let AI invent reviews, testimonials, guarantees, certifications or before/after results.",
    "Follow the rules of each platform (Google, Facebook, Instagram) and local rules on texting and emailing customers.",
]

BUSINESS_PROFILE = """MY BUSINESS PROFILE (paste once at the start of a chat, then reuse)
Business name: [Your Business Name]
Owner / signature name: [Your first name]
Services: [e.g., standard, deep, move-in/move-out, short-term rental turnovers, small offices]
Service area: [towns / neighborhoods]
Booking link or phone: [link or number]
Tone: [e.g., warm, clear, professional — no slang, no exclamation overload]
Things we never promise: [e.g., stain removal guarantees, same-day service]
Our policies (summarized in my own words): [cancellation notice, payment timing, pets, supplies]"""

W = [
    dict(id="01", title="Reply to a new lead",
         when="Within 15 minutes of a new inquiry (form, text, DM or voicemail). Speed matters more than perfection.",
         inputs="Lead's first name, how they contacted you, what they asked for, property details they gave, your next available openings.",
         prompt="""Act as the friendly office manager for my cleaning business. Use my business profile above.
A new lead just contacted us. Write a reply I can send by [text / email].

Lead details:
- First name: [name]
- Contacted us via: [channel]
- What they asked: [paste their message]
- Property details they gave: [size, bedrooms, bathrooms, pets, condition — or "not given"]
- My next openings: [days/times]

Requirements:
1. Thank them by first name and confirm what they need in one sentence.
2. If size, bedrooms, bathrooms, cleaning type or frequency are missing, ask for ONLY the missing items, as a short numbered list.
3. Offer two specific appointment windows from my openings.
4. Do not quote a price yet unless I included one here.
5. Under 90 words for a text, under 150 for email. End with my first name.
Give me two versions: one warm, one more concise.""",
         review="Openings are real; no price promised by accident; nothing you can't deliver.",
         sheet="Log the lead in LEADS (Stage = New Lead → Contacted). Set Next Follow-Up for tomorrow."),
    dict(id="02", title="Turn customer details into a quote draft",
         when="After you price the job in QUOTE BUILDER and want a clear written quote.",
         inputs="The QUOTE SUMMARY text from QUOTE BUILDER (row 39), what's included, add-ons, and how long the quote is valid.",
         prompt="""Use my business profile above. Turn the job summary below into a clear, friendly written quote I can email.

Job summary from my quote calculator:
[paste the QUOTE SUMMARY text]

What's included in this service (my checklist): [paste or summarize]
Not included: [e.g., inside oven unless added, exterior windows, biohazard]
Quote valid until: [date]
How to book: [link / reply / call]

Format:
- Subject line
- 2-sentence intro using their first name
- "Your clean includes" (bullets, max 8)
- Price block: price before tax, any discounts, tax line ONLY if I listed one, total
- What happens next (3 steps)
- Sign-off with my first name
Use ONLY the prices I gave you. Do not add, round or change any number. If something is unclear, write [CHECK] instead of guessing.""",
         review="Every number matches QUOTE BUILDER exactly. Remove any [CHECK] markers after you fix them.",
         sheet="LEADS: enter Quote Value, set Stage = Quote Sent, set Next Follow-Up in 2 days."),
    dict(id="03", title="Quote follow-up",
         when="2 days after sending a quote with no booking yet.",
         inputs="First name, service quoted, the quote total, any concern they mentioned, one open appointment.",
         prompt="""Use my business profile. Write a short follow-up to a customer who received a quote but hasn't booked.

- First name: [name]
- Service quoted: [service] for [price]
- Sent on: [date]
- Anything they mentioned (concern, timing, budget): [notes or "nothing"]
- An opening I can offer: [day/time]

Rules: helpful, never pushy; one sentence that re-states the value in their terms; offer the opening; invite questions; under 70 words. No fake urgency, no discounts unless I list one here: [discount or "none"].
Give me a text version and an email version.""",
         review="No pressure tactics; any discount is one you actually approve.",
         sheet="LEADS: update Last Contact and Next Follow-Up (+3 days). Stage = Follow-Up."),
    dict(id="04", title="No-response follow-up (last touch)",
         when="After 2–3 unanswered follow-ups. Closes the loop politely and keeps the door open.",
         inputs="First name, what they asked about, how many times you've followed up.",
         prompt="""Use my business profile. Write a final, polite check-in to a lead who hasn't replied after [number] messages.
They asked about: [service].
Goals: make it easy to say "not now" or "yes"; no guilt; mention they can reach us any time; under 50 words.
Offer one line they can reply with, e.g., "Reply 1 to book, 2 for later."
Write 2 options.""",
         review="Short and respectful. After this, stop messaging unless they reply.",
         sheet="If no reply in 5 days: Stage = Lost/Declined, Lost Reason = No response."),
    dict(id="05", title="Appointment confirmation",
         when="When a job is booked, and again the day before.",
         inputs="First name, service, date, arrival window, cleaner name, prep notes, how payment works.",
         prompt="""Use my business profile. Write (a) a booking confirmation and (b) a day-before reminder for this job:
- First name: [name]
- Service: [service] at [street name only — no full address]
- Date and arrival window: [date, window]
- Cleaner(s): [first names]
- Prep we ask for: [e.g., pets secured, clutter picked up, parking]
- Payment: [how/when, as I describe it]

Each message under 70 words, friendly, with a clear way to reschedule. Do NOT include door codes, lockbox codes or alarm details.""",
         review="Date/time match JOBS. No access codes in any message.",
         sheet="JOBS: confirm Date, Start Time, Worker, Status = Scheduled."),
    dict(id="06", title="Rescheduling message",
         when="You need to move a job (illness, weather, overbooking) or the customer asks to.",
         inputs="Who is rescheduling, reason (brief, honest), two new options, any goodwill gesture you approve.",
         prompt="""Use my business profile. Write a message to reschedule a cleaning.
- First name: [name]
- Original appointment: [date/time]
- Who requested the change: [us / customer]
- Reason (keep it brief and honest): [reason]
- New options: [option 1], [option 2]
- Goodwill gesture (only if I list one): [e.g., none / small credit]
Apologize once if we caused it, offer the two options, ask them to reply with their choice. Under 80 words.
If the customer is changing late, refer to my policy in neutral words: [paste your policy summary] — do not add fees I haven't listed.""",
         review="Policy wording matches YOUR written policy. No new fees invented.",
         sheet="JOBS: set old row Status = Rescheduled; add a new row with the new date."),
    dict(id="07", title="Review request",
         when="Same day or next day after a job that went well (QC pass, happy customer).",
         inputs="First name, one specific thing done well, your review link.",
         prompt="""Use my business profile. Write a short review request to a customer after a cleaning.
- First name: [name]
- One specific thing we did well or they mentioned: [detail]
- Review link: [link]
Rules: thank them; mention the specific detail; ask if they'd share their experience; include the link; under 60 words.
Do NOT offer any reward, discount or entry in exchange for a review, and do not ask only for 5-star reviews.
Give a text and an email version.""",
         review="No incentive for reviews; ask for honest feedback only.",
         sheet="REVIEWS: add a row (Status = Requested). The Action column tells you when to remind."),
    dict(id="08", title="Respond to a review",
         when="Within 48 hours of any review — positive, mixed or negative.",
         inputs="The review text, star rating, what actually happened (facts only).",
         prompt="""Use my business profile. Draft a public reply to this review.
Rating: [stars]
Review text: [paste]
What actually happened (private facts for context — do NOT repeat personal details publicly): [notes]

Rules:
- Positive review: thank them by first name, mention one detail, 2–3 sentences.
- Mixed or negative: thank them, acknowledge the experience without arguing, give no private details, invite them to contact [phone/email] to make it right. 3–4 sentences.
- Never admit legal fault or discuss damage claims, insurance or refunds publicly — say we'll follow up directly.
- No keywords stuffing, no copy-paste feel.""",
         review="Calm, short, no private details, no admissions or promises about claims.",
         sheet="REVIEWS: You Replied? = Yes. Log any problem in QUALITY CONTROL → Issue Log."),
    dict(id="09", title="Referral request",
         when="After a 5-star review, a compliment, or the 3rd–4th recurring visit.",
         inputs="First name, what they like about the service, your referral thank-you (if any).",
         prompt="""Use my business profile. Write a referral request to a happy customer.
- First name: [name]
- What they've told us they like: [detail]
- Our thank-you for referrals (only if I offer one, in my words): [e.g., a service credit / none]
Make it easy: one sentence they can forward to a friend, plus how the friend should mention them. Under 80 words. No pressure.""",
         review="The thank-you matches what you actually offer, and any rules you set.",
         sheet="FOLLOW-UPS: log it. When a referral arrives, add it to REFERRALS."),
    dict(id="10", title="Reactivate a past customer",
         when="CUSTOMERS shows 'Reactivate' (no job for 90+ days by default).",
         inputs="First name, last service and date, anything new you offer, upcoming openings.",
         prompt="""Use my business profile. Write a friendly check-in to a past customer we haven't cleaned for since [month].
- First name: [name]
- Last service: [service]
- Something useful or new (optional): [e.g., seasonal deep clean, new recurring slots]
- Openings: [dates]
Tone: genuine, no guilt-tripping, under 70 words. Offer one easy next step. If I list an offer, include it exactly: [offer or "none"].""",
         review="Only real offers. Respect anyone who asked not to be contacted.",
         sheet="FOLLOW-UPS: Type = Reactivation. Update CUSTOMERS notes with the result."),
    dict(id="11", title="Google Business Profile post",
         when="Weekly. Keeps your profile active and gives searchers a reason to call.",
         inputs="Topic (tip, service spotlight, seasonal offer, team highlight), service area, call to action.",
         prompt="""Use my business profile. Write 3 Google Business Profile posts (each 80–150 words) about: [topic].
Each post: a useful local-sounding opening line, one practical tip or benefit, a clear call to action ([Book / Call / Learn more]) and the service area.
No phone numbers inside the text, no exaggerated claims ("best in town"), no made-up statistics or awards. Suggest a photo idea for each.""",
         review="Claims are true; photos are your own (with permission if people/homes are shown).",
         sheet="Track bookings that mention Google in LEADS → Lead Source."),
    dict(id="12", title="Facebook post",
         when="2–3 times a week; local groups only where the group rules allow business posts.",
         inputs="Post goal (trust, booking, recurring, referral), topic, any offer, photo you have.",
         prompt="""Use my business profile. Write 3 Facebook posts for my cleaning business.
Goal: [trust / bookings / recurring plans / referrals]
Topic: [e.g., 5-minute bathroom reset, what a deep clean includes, meet our team lead]
Offer (only if real): [offer or "none"]
Each post: a hook line that names a specific situation, 3–5 short lines of value, one call to action. Conversational, local, no hashtag spam (max 2).""",
         review="Offer details and dates are correct.",
         sheet="Use LEADS → Lead Source = Facebook so you can measure results on MONTHLY."),
    dict(id="13", title="Instagram caption",
         when="With every before/after, team or tip post.",
         inputs="What the photo/video shows, the room/problem, what you did, call to action.",
         prompt="""Use my business profile. Write 3 Instagram captions for a post that shows: [describe photo/video].
Each caption: first line under 10 words that stops the scroll; 2–4 short lines on what was done and why it matters; a call to action ([link in bio / DM "CLEAN"]); 5–8 relevant hashtags mixing local and service tags.
Do not claim results the photo doesn't show. No customer names or addresses.""",
         review="You have the customer's permission to share photos of their home.",
         sheet="Track DMs as leads in LEADS (Source = Instagram)."),
    dict(id="14", title="Answer a service FAQ",
         when="A customer asks a question you answer often (supplies, pets, keys, what's included).",
         inputs="The question, your actual policy or practice in plain words.",
         prompt="""Use my business profile. A customer asked: "[question]".
Our actual practice (use only this, don't add details): [your answer in rough notes]
Write a clear, friendly answer under 90 words. If my notes don't cover something they asked, write [ASK OWNER] instead of guessing.
Then turn it into a reusable FAQ entry (question + 2–3 sentence answer) for my website.""",
         review="Matches your policy exactly; remove [ASK OWNER] after deciding.",
         sheet="Save good answers in your website FAQ and SETTINGS notes."),
    dict(id="15", title="Commercial cleaning proposal draft",
         when="An office, clinic, studio or retail space asks for a proposal.",
         inputs="Business type, size, restrooms, frequency, scope from your walkthrough, price from QUOTE BUILDER, start date.",
         prompt="""Use my business profile. Draft a professional cleaning proposal.
Client: [business name, contact first name]
Space: [type], [sq ft], [restrooms], [special areas]
Visit frequency and timing: [e.g., 3x weekly after 6 PM]
Scope from my walkthrough: [paste notes]
Price per visit and monthly estimate (from my calculator): [numbers]
Start date: [date]

Sections: 1) Summary, 2) Scope of work by area (bullets), 3) Schedule, 4) Pricing (use my numbers exactly), 5) Supplies & equipment (as I describe), 6) Quality checks and how to reach us, 7) Next steps.
Mark anything that needs a contract term, insurance detail or legal language as [OWNER/PROFESSIONAL TO COMPLETE] — do not write those terms yourself.""",
         review="Prices match QUOTE BUILDER. Contract, insurance and legal terms are completed by you with professional advice where needed.",
         sheet="LEADS: Stage = Quote Sent. If won, add to CUSTOMERS, PROPERTIES and RECURRING."),
    dict(id="16", title="Employee task instructions",
         when="Turning your notes into a clear job sheet or task for a cleaner.",
         inputs="Job details (service, rooms, special requests), customer preferences, priorities. No access codes.",
         prompt="""Rewrite my rough notes into clear task instructions for a cleaner.
Job: [service], [rooms / areas]
Customer preferences: [e.g., unscented products, skip office]
Priorities if time runs short: [1, 2, 3]
My notes: [paste]

Format: numbered steps by room, a "Do NOT" list, a "Before you leave" checklist, and a line to report problems to [owner/phone].
Plain language, short sentences. Don't add chemical-mixing instructions or safety rules — I'll attach our own product labels/safety sheets.""",
         review="Instructions match your service standard; access details stay out of the document.",
         sheet="STAFF & TASKS: add the task. Attach the CLIENT-FORMS Employee Job Sheet."),
    dict(id="17", title="Customer complaint response",
         when="A customer reports a missed area, late arrival, damage concern or billing question.",
         inputs="The complaint (their words), facts you know, what you can offer (re-clean window, call).",
         prompt="""Use my business profile. Draft a reply to this customer concern.
Their message: [paste]
Facts I know: [what happened, job date, cleaner]
What I can offer (only these): [e.g., re-clean within 24–48 hours / a call today]

Rules: thank them; acknowledge their experience without arguing; say exactly what happens next and when; keep it under 120 words.
If the concern involves damage, injury, a refund demand or anything legal/insurance-related: do NOT admit fault or promise payment — say we're looking into it and will contact them by [time]. Flag it to me with [OWNER REVIEW].""",
         review="Offer is one you approved. Damage/insurance matters handled by you, with professional advice if needed.",
         sheet="QUALITY CONTROL → Issue Log: record it, the action and the resolved date."),
    dict(id="18", title="Weekly marketing ideas",
         when="Monday planning. Pairs well with your MONTHLY and DASHBOARD numbers.",
         inputs="Last week's leads by source, open recurring slots, season/events, one goal.",
         prompt="""Act as a practical marketing assistant for a local cleaning business. Use my business profile.
This week's facts (from my dashboard): leads [number], top lead source [source], open recurring slots [number], season/local events [notes].
Goal this week: [e.g., fill 3 recurring slots / get 5 reviews / reach property managers]
Give me: 5 low-cost actions ranked by likely impact for that goal, each with the exact first step, time needed, and how I'll measure it in my workbook (which sheet/column). Avoid paid ads unless I ask. No guaranteed results.""",
         review="Pick 1–2 actions, not 5. Measure them on the DASHBOARD next Monday.",
         sheet="FOLLOW-UPS: schedule the actions; check MONTHLY → Lead Source results."),
]
