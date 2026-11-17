# What the dashboard does

Use this to write the hand-off message and to answer questions about the dashboard. Every feature
is already in the template. Nothing here needs to be built.

## Tabs

- **Dashboard:** summary tiles (days to go, hours done, items done, pace against the plan, readiness
  plus the last Final check score), a calendar strip with a progress ring per day, the selected day,
  and side panels for phase progress, "Up next" and skill coverage.
- **Readiness:** every objective or job line with what it looks like in practice, the proof they'll
  have, a coverage bar, a self-rating (Not yet, Getting there, Confident) and links to its days.
- **Final check:** the 50-question exam (see below).
- **All days:** search, filters by type, optional items on or off, and Hide finished.
- **Project:** milestones that tick themselves as Build items are done. Hidden when the plan has no project.
- **Setup:** the plan's own cards plus a short guide to every feature.

## On every day

- **Checklist** with Reminders-style round checkboxes, type chips, minutes and links.
- **Self-check:** 5 short questions a day, one at a time. The first is from the plan; Claude writes
  the other 4 the first time, and they're kept. Type or speak an answer, then Check my answer for a
  verdict and short bullets: what's right, what's wrong, what's missing, one line to remember, and a
  model answer. Read and Read all read aloud.
- **Explain it simply:** a chat box that accepts screenshots (paste, drag, or Add image). Answers
  like you're 5, then "In real terms", then a quick check question. Every answer has Add to notes.
- **Read-along** in natural Claude voices (Buttery, Airy, Glassy, Rounded) with a Try voice button,
  speed from 0.8x to 1.4x, sentence highlighting, Pause, Resume, tap a sentence to jump, and an option
  to read new answers aloud automatically. Falls back to the device's voices where Claude voices
  aren't available.
- **Notes:** a draft box that saves itself, voice input, screenshots, and Clean up with AI, which
  fixes misheard words, corrects mistakes from its own knowledge, lists every change, and suggests
  missing points separately with an Add button. Save note files the draft under a topic. See notes
  opens a side panel where every note has an AI-written heading and a Contents menu jumps between them.
- **Help me build** on Build items: plans the build as 4 to 8 small steps, then teaches each one
  (what we're doing, why, exact commands with Copy buttons, what happened, how to check it, what to
  do if it breaks), with a question box per step and a My computer setting so commands match.

## Final check

- 50 questions written at build time, so starting it is instant.
- One question at a time with a numbered grid; answers save, so they can leave and come back.
- Results: a readiness percentage and level (85 and up Ready, 70 to 84 Almost ready, 50 to 69
  Getting there, below 50 Not ready yet), scores by phase, days to revisit, and every miss with the
  right answer, why, and a "Study this" link that opens that exact day and highlights the item.
- Retake, a history of attempts, and "Write a new set of 50" for fresh questions from Claude.

## Saving

Progress, notes, screenshots, quiz answers, build guides and exam attempts save to the artifact's
database and sync across devices. A copy is kept in the browser as a backup.

## Limits to mention in the hand-off

- Claude features (self-check reviews, Explain it simply, Clean up, headings, build guides, new exam
  sets) use the person's own Claude usage and ask permission the first time.
- Voice input and the natural Claude voices work in Chrome, Edge and the Claude desktop app's main
  window. Elsewhere, reading aloud uses the device's voices and voice input uses the computer's own
  dictation (Windows: Win+H, Mac: press Fn twice).
- Screenshot storage makes the dashboard shareable only inside the person's organization.
- Opened as a plain HTML file outside Claude, the checklist, calendar, readiness and Final check
  work and save in that browser, but the Claude-powered features are hidden.
