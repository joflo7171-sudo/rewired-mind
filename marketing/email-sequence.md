# Rewired Mind: Post-Quiz Email Sequence (Brevo)

**Goal:** turn quiz subscribers into first buyers ($9 Anxiety Exit) and then Transformation System buyers ($97).
**Trigger:** contact added to the "Rewired Mind Quiz" list. **Sender:** Rewired Mind. **Length:** 7 emails over 10 days.
**Exit rule:** remove from the sequence on purchase (Gumroad -> Brevo tag/list via Zapier), then move to the buyer upsell track.

> Known gap: the quiz sends only EMAIL to Brevo, not the result type (`archetype`). This sequence is therefore one path for everyone.
> Fix later (small change to `index.html`): pass the result as a Brevo attribute, then split Awakened/Builder -> $97 first, Rising/Warrior -> $9 first.

Links (UTMs follow the existing quiz convention):
- Free Reset PDF: https://rewiredmind.org/Rewired-Mind-Free-7-Day-Confidence-Reset.pdf
- Anxiety Exit ($9): https://therewiredmind.gumroad.com/l/qecbe?utm_source=email&utm_medium=sequence&utm_campaign=post_quiz&utm_content=eN
- Transformation System ($97): https://therewiredmind.gumroad.com/l/transformation-system?utm_source=email&utm_medium=sequence&utm_campaign=post_quiz&utm_content=eN
(replace `eN` with the email number so sales can be attributed per email)

Footer on every email: unsubscribe link + "Educational content, not medical or mental-health treatment."

---

## Email 1 - Day 0 (immediately)
**Subject:** Your 7-day reset (start with Day 1 tonight)
**Preview:** Takes 5 minutes. Here's your download.

Hey,

You finished the quiz. Most people don't, so that already says something about you.

Your free 7-Day Confidence Reset is here: [DOWNLOAD THE RESET]

Do Day 1 tonight. It takes about 5 minutes and the goal is small: notice one moment today where your mind talked you out of something.

That's all. Noticing is the first step because you can't change a pattern you can't see.

Reply and tell me what you noticed. I read every one.

- Rewired Mind

---

## Email 2 - Day 1
**Subject:** Confidence isn't the problem
**Preview:** It's the loop that runs before you act.

Here's what I see over and over:

Someone wants to speak up. Before they do, their mind runs a loop. "What if it comes out wrong? What will they think? Maybe next time."

By the time the loop finishes, the moment has passed. Then comes the regret.

That's not a confidence problem. It's an overthinking loop that happens *before* confidence gets a chance to show up.

Tomorrow's reset day shows you how to interrupt it. Today, just catch it once. When you feel the loop start, say to yourself: "That's the loop."

Naming it takes away a lot of its power.

- Rewired Mind

P.S. Did you do Day 1? Reply with one word: yes or no. No judgment either way.

---

## Email 3 - Day 3
**Subject:** The 2 a.m. loop
**Preview:** If your mind won't shut off, read this.

You're tired. You should be asleep. Instead you're replaying a conversation from three days ago, rewriting what you should have said.

Sound familiar?

That loop feels like problem-solving. It isn't. Real problem-solving ends with a next step. A loop just repeats.

I built **The Anxiety Exit** for exactly this. It's a short, practical guide to stopping anxious thought loops and acting from calm self-trust, one step at a time.

It's $9.

[GET THE ANXIETY EXIT - $9]

If you only try one thing this week, try this.

- Rewired Mind

---

## Email 4 - Day 4
**Subject:** What "just stop overthinking" gets wrong
**Preview:** Telling yourself to stop makes it worse.

"Just stop overthinking."

If that worked, nobody would still be doing it.

Trying to force a thought away usually makes it louder. What works is giving your mind a different instruction: a specific, small next action it can follow instead.

That's the core idea inside The Anxiety Exit: you don't fight the loop, you exit it with a step.

[SEE THE ANXIETY EXIT - $9]

Nine dollars is the price of a coffee. If it helps you break even one loop, it's paid for itself.

- Rewired Mind

---

## Email 5 - Day 6
**Subject:** The gap between knowing and doing
**Preview:** You already know what to do. So why don't you?

Most people who take a quiz like yours already know what they want: speak up more, trust themselves, stop second-guessing.

Knowing isn't the gap. Doing it consistently, especially on hard days, is.

That's what the **Rewired Mind Transformation System** is for. It's a complete 3-phase program:

- **Reset** - clear the mental noise and the old patterns
- **Accelerate** - build confident action with practical daily steps
- **Lock It In** - make it automatic so it holds on bad days, not only good ones

$131 of tools, $97 together.

[SEE THE TRANSFORMATION SYSTEM - $97]

- Rewired Mind

---

## Email 6 - Day 8
**Subject:** Which one is right for you?
**Preview:** A simple way to choose.

Two options, one simple rule:

**If your biggest problem is the mental loop** (overthinking, anxiety spirals, can't switch off):
-> **The Anxiety Exit, $9.** Start here. [LINK]

**If you want the full change** (confidence that holds up under pressure, not just calm in the moment):
-> **The Transformation System, $97.** Reset, Accelerate, Lock It In. [LINK]

Not sure? Start with the $9. You can always go further later.

- Rewired Mind

---

## Email 7 - Day 10
**Subject:** Last note from me (for now)
**Preview:** Where this goes if nothing changes.

This is the last email in this series.

If you do nothing, here's the likely path: the same loops, the same hesitation, the same "next time." Nothing wrong with you. It's just a pattern that keeps running until something interrupts it.

You've already taken the first steps: the quiz and the reset. The next step is yours:

- Break the loop: [THE ANXIETY EXIT - $9]
- Rebuild the pattern: [THE TRANSFORMATION SYSTEM - $97]

Either way, thanks for reading. I'll keep sending useful ideas about confidence and overthinking. Reply anytime.

- Rewired Mind

---

## Measure (Brevo + Gumroad)
Per email: open rate, click rate, Gumroad sales by `utm_content`. After ~500 subscribers, keep the top 2 emails by sales per send, rewrite the bottom 2, and test subject lines on Emails 3 and 5.
No testimonials or results claims are included on purpose; add real ones when you have them.
