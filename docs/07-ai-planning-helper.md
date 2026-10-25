# Your AI Planning Helper

Using AI as a low-energy co-planner: what it's for, what it's not for, and
copy-paste prompts.

## The right job for an AI helper

For ADHD/low-energy work, AI is best as a **planning clerk and body double** —
not a boss. That distinction is the whole chapter:

- A planner clerk turns "the kitchen is knocked over" into slices with decision
  lists (see [Task Slicing](02-task-slicing.md)).
- A planner clerk drafts the guilt-free rest menu, the energy pricing, and the
  day plan, then *waits for you to pick*.
- A body double sits, witnesses, stamps. ([Body Doubling](03-body-doubling.md))
- A boss orders you around, sets your goals, scolds, adds moral judgment to
  task frames. **That's not the job.** If an AI is acting like a boss, tell it
  so — or close it.

You are the planner. The AI organizes and itemizes. It should never assign
shame and should never invent work you didn't choose.

## What never goes in a chat with an AI

- Med decisions, doses, or anything medical. AI is not your clinician. Education
  only, never advice — that rule applies to this whole manual too.
- Names and details of other people (employer drama, kids' medical stuff).
- Financial account numbers, passwords, ID numbers.
- Anything you'd hate to paste into a stranger's notebook.

Local-first reminder: many tools don't train on your chats, but you can't
always verify it. Assume your words could be seen; write accordingly, plans not
secrets.

## The prompt library

Copy-paste these. Bracketed parts are yours to fill in. They're deliberately
short and Directive-Free: every prompt keeps you in the planner's chair.

### Prompt 1: The Slicing Clerk

```
Slice this chore for me. Do NOT coach me or add tasks I didn't list.

Chore: [the thing that's knocking me down]

Rules for your slices:
- Each slice: 2-10 minutes of physical motion, no decisions required,
  visible point at which you stop.
- List them numbered.
- After the list, add ONE line: what a 2-minute version of slice 1 is.
- Do not add motivational text.
```

### Prompt 2: The Energy Clerk (day plan)

```
Be my planning clerk. Do not be my coach.

Battery today: [e.g. 45%]
Chores I might do: [list, 1 line each]
Fixed stuff: [meds, school pickup, work hours]

Act like this:
- Price each chore in energy units 1-10 based on the description, and note
  which ones have "toll costs" above their minute count.
- Propose ONE anchor task and 1-3 slices for today at about a quarter of my
  battery, total plan <= 80% of battery.
- Ask me to confirm or veto the plan in one short sentence.
```

### Prompt 3: The Rest Menu

```
Give me a menu of 5 options for legitimate 20-minute rest for someone whose
battery is at [X]% tonight. No screens-only list, no chores. Each option:
one sentence, zero guilt-tripping, mentions what rest feels like afterwards.
```

### Prompt 4: The Body Double

```
Be my body double for the next [10] minutes while I do [task]. Rules:
- Do not suggest anything.
- Do not narrate.
- After the time, ask ONE question: "Done, parked, or need more?"
```

### Prompt 5: The Restart Ritual Clerk

```
Help me restart after a crash. Strict rules:
- No guilt, no "just," no questions about why I stopped.
- Step 1 only: help me DECLARE AMNESTY on my old task list. Print a short
  amnesty statement for me to read aloud.
- Then ask today's battery % and propose ONE anchor task.
- Nothing else today.
```

## Prompt hygiene at 30% battery

When your brain is mush, prompts feel impossible to write. Two fixes:

1. **Save this page.** The library above is your prompt address book. Fill
   brackets, hit send. No composing needed.
2. **Mush-mode words are fine.** "kitchen wrecked dishes everywhere no laundry
   help slice" is a 100% valid prompt. The AI handles messy input; that's its
   superpower. Don't waste battery on grammar.

## When the AI gets it wrong

It will, sometimes, in one specific predictable way: it will *add work*.
Extra tasks, "consider also...", guilt-adjacent language in a list header.
Standard corrections:

- "Remove every task I didn't mention."
- "Remove all motivational language."
- "Cut the plan to what's doable at 40%, not 80%."

If it keeps acting like a boss after two corrections: close it and use the
worksheet version. The paper tools in this manual never add work, never give
tone problems, and they run on nothing but you.

## Comparison to the chore planner app

| Job | Chore planner app | AI chat helper |
|-----|-------------------|----------------|
| Store chores, track done | Yes (its main job) | No |
| Slice / price / plan | Templates only | On demand, anywhere |
| Body double | No | Yes (Prompt 4) |
| Privacy | Local-first | Send only plans, not secrets |
| Needs (y)our energy | One number per day | One sentence per session |

They're teammates: the app is the ledger, the AI is the clerk. The worksheets
are the paper fallback — print them once (see
[Worksheets](07-worksheets.md)) and no bad day can unplug them.
