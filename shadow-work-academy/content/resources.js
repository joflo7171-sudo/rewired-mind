SWA.meta = {
  name: "The Shadow Work Academy",
  tagline: "From self-doubt to self-trust.",
  version: "1.0",
  storageKey: "swa.v1",
  supportEmail: "support@rewiredmind.org"
};

SWA.values = ["Honesty","Kindness","Courage","Growth","Curiosity","Calm","Family","Friendship","Independence","Creativity","Health","Reliability","Fairness","Freedom","Learning","Respect","Faith / meaning","Adventure","Craftsmanship","Generosity","Security","Balance"];

SWA.resources = [
  { id: "quickstart", title: "Quick-Start Guide", file: "01-quick-start-guide.pdf", type: "guide",
    blurb: "How the academy works, a suggested two-to-six week pace, and how to look after yourself while you do the work.",
    sections: [
      { h: "Welcome", p: ["The Shadow Work Academy is a structured, self-paced program of six modules. Each one has a lesson, a scenario, reflection questions, a worksheet, a real-world action, and a recap. It is a self-reflection tool, not therapy or medical advice."] },
      { h: "How to move through it", list: ["Plan on 45–60 minutes per module for the lesson and worksheet, plus a week of practice for the action step.", "A comfortable pace is one module per week (six weeks). Two weeks per module is also fine.", "Do the modules in order; each one builds on the last.", "Answer in your own words. Short, honest answers are better than polished ones.", "You can skip any prompt that feels like too much right now."] },
      { h: "Using the interactive academy", list: ["Open START-HERE.html from your download folder and choose Open the Academy, in a modern browser: Chrome, Safari, Firefox or Edge.", "Your answers are saved in your browser on this device. Nothing is sent anywhere by the academy itself.", "Because answers live in that one browser, use the Backup button on the Progress page regularly to save a file copy. Clearing browser data will erase unsaved answers.", "Use the Print button on any module to get a clean worksheet, or use the PDF workbook if you prefer paper."] },
      { h: "Taking care of yourself", p: ["Stop whenever you need to. If you feel overwhelmed, take a break, talk to someone you trust, or contact a licensed mental health professional. If you may be in danger or thinking about harming yourself, contact local emergency services or a crisis line in your country right away."] }
    ]
  },
  { id: "selfworth", title: "Self-Worth Reflection Exercises", file: "02-self-worth-reflection-exercises.pdf", type: "prompts",
    blurb: "Eight short exercises to return to whenever your sense of worth gets tied to performance or approval.",
    prompts: [
      "The Condition Check: Finish the sentence “I feel worthwhile when ______” five different ways. Which ones are conditions you could loosen?",
      "Evidence File: List ten things you did in the past year that reflect your values, regardless of the outcome.",
      "The Friend Test: Write what you would say to a friend in your exact situation, then address it to yourself.",
      "Comparison as Information: Name someone you compare yourself to. What quality are you drawn to? What is one small way to practice it?",
      "Receiving Well: Next time you are complimented, say only “Thank you.” Afterwards, note what the urge to deflect felt like.",
      "Own Read First: Before asking for reassurance, write what you already believe about the situation.",
      "Rest Without Earning It: Schedule 30 minutes of rest that must not be productive. Record what comes up.",
      "Good-Enough Standard: For one task this week, decide ahead of time what “good enough” looks like and stop there."
    ]
  },
  { id: "tracker", title: "Trigger & Pattern Tracker", file: "03-trigger-and-pattern-tracker.pdf", type: "table", rows: 14,
    blurb: "Log triggers as they happen to see your recurring patterns clearly.",
    columns: [
      { id: "date", label: "Date" }, { id: "trigger", label: "Trigger" }, { id: "feeling", label: "Feeling & body sensation" },
      { id: "reaction", label: "What I did" }, { id: "story", label: "Story I told myself" }, { id: "intensity", label: "Intensity (0–10)" }, { id: "need", label: "Possible need underneath" }
    ]
  },
  { id: "innercritic", title: "Inner-Critic Reflection Worksheet", file: "04-inner-critic-reflection-worksheet.pdf", type: "ref", ref: { module: 3 },
    blurb: "An eight-step guide for separating facts from assumptions and writing a balanced response. Reusable as often as you like." },
  { id: "pleasingaudit", title: "People-Pleasing Audit", file: "05-people-pleasing-audit.pdf", type: "ref", ref: { module: 4 },
    blurb: "A seven-item audit plus a pattern map of the relationships where you stretch yourself most." },
  { id: "scripts", title: "Boundary-Setting Scripts Library", file: "06-boundary-scripts-library.pdf", type: "scripts",
    blurb: "Sixteen ready-to-adapt scripts for work, family, friendships, and relationships, plus a space to write your own." },
  { id: "values", title: "Personal Values & Needs Worksheet", file: "07-values-and-needs-worksheet.pdf", type: "values",
    blurb: "Choose your core values, identify your needs, and connect both to specific daily choices." },
  { id: "weekly", title: "Weekly Reflection & Progress Tracker", file: "08-weekly-reflection-tracker.pdf", type: "weekly", weeks: 12,
    blurb: "A twelve-week tracker for your weekly ten-to-fifteen-minute review." },
  { id: "actionplan", title: "Personal Self-Trust Action Plan", file: "09-self-trust-action-plan.pdf", type: "ref", ref: { module: 6 },
    blurb: "Your one-page plan: key insights, if–then actions, a recovery step, and a review routine." }
];

SWA.weeklyPrompts = [
  { id: "wins", label: "One thing I handled well" },
  { id: "tried", label: "What I tried this week (pause, boundary, balanced thought…)" },
  { id: "hard", label: "A moment that was hard, and what I noticed" },
  { id: "learned", label: "What I learned about my pattern" },
  { id: "next", label: "One adjustment for next week" }
];

SWA.needs = ["Rest","Quiet / alone time","Honest communication","Predictability","Connection","Autonomy","Appreciation","Play / fun","Movement","Creative expression","Support","Clear expectations","Financial stability","Meaning / purpose"];
