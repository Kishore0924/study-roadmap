---
name: study-roadmap
description: Turns any certification, job role or subject into a personal day-by-day study roadmap, delivered as an interactive Apple-style dashboard with progress rings, an AI tutor that explains like you're 5, daily self-checks, voice notes with AI clean-up, step-by-step build guides, natural read-aloud and a 50-question final exam that links every miss to the day to revisit. Use when someone wants a study plan, exam prep, a learning roadmap, an onboarding or new-job ramp-up, or a study tracker, for example "help me prepare for CompTIA SecAI+", "make me a 6-week plan to learn Kubernetes" or "ramp me up for my new role".
---

# Study Roadmap

You turn a goal (a certification, a new job, or a subject) into a researched day-by-day plan, then
publish it as a polished interactive dashboard. The dashboard is already built: `assets/dashboard-template.html`
has every feature and the design. Your job is the plan. You research, write one JSON file, and the
build script puts it into the template. Never hand-write the dashboard's HTML or CSS.

Files in this skill:

| Path | Use it for |
| --- | --- |
| `references/intake.md` | The questions to ask first, as clickable choices |
| `references/research-and-plan.md` | How to research and design the plan, the readiness map and the 50 exam questions |
| `references/plan-schema.md` | Every field of the plan JSON, with an example |
| `references/features.md` | What the dashboard does, for your hand-off message and for answering questions |
| `references/publishing.md` | Building, testing, publishing, updating, and the fallback when Artifacts aren't available |
| `scripts/build_dashboard.py` | Validates the plan and builds the page: `python3 scripts/build_dashboard.py plan.json -o dashboard.html` |
| `scripts/smoke_test.py` | Clicks through every feature in a headless browser: `python3 scripts/smoke_test.py dashboard.html` |
| `examples/llm-security-5-day.json` | A small, complete, valid plan to copy the shape from |

## Workflow

### 1. Ask first, with clickable choices

Read `references/intake.md` and follow it. Use your multiple-choice question tool (AskUserQuestion,
or whatever the app provides) for every question that has sensible options, so the person clicks
instead of typing. The only typed answers are the exact name of what they're preparing for (or a
pasted job description) and anything they pick "Other" for. Skip any question their message already
answers. Don't start researching until you know the goal, the dates and the daily hours.

If they want to upload study material, wait until they say they're done, then read every file fully.

### 2. Research

Follow `references/research-and-plan.md`. In short: official objectives or the job description
first, every objective covered by at least one day, video and hands-on resources before reading,
every link verified, and never an invented URL. Uploaded documents outrank websites.

### 3. Write the plan JSON

Write `plan.json` in your working folder following `references/plan-schema.md`, and copy the shape
of `examples/llm-security-5-day.json`. Write all 50 Final check questions now, each mapped to the day
and item that teaches it. Then validate:

```bash
python3 <skill-dir>/scripts/build_dashboard.py plan.json --check
```

Fix every ERROR and read every warning. Repeat until it prints `ok:`.

### 4. Build and test

```bash
python3 <skill-dir>/scripts/build_dashboard.py plan.json -o dashboard.html
python3 <skill-dir>/scripts/smoke_test.py dashboard.html
```

The smoke test needs Playwright for Python. If it isn't available, say so in your hand-off rather
than claiming the page was tested.

### 5. Publish

Follow `references/publishing.md`. With an Artifact publishing tool, publish `dashboard.html` as a
new artifact with these capabilities, on the latest runtime version:

```json
{"db": {}, "sample": {"images": true}, "dictation": {}, "assets": {}, "tts": {}}
```

Without one, deliver `dashboard.html` as a file and explain which features need the Claude app.

### 6. Hand off

In a few short lines: what the plan covers (days, hours, phases), how to use the dashboard (tick
items, self-check, Explain it simply, notes, Help me build, Final check), and the limits from
`references/features.md`. Offer to adjust the plan. Don't paste the whole plan into the chat.

## Rules

- Never use em dashes or arrow symbols anywhere: plan text, prompts or replies. The build script
  rejects them.
- Plain, friendly language. Sentence case for titles and buttons.
- Never invent a URL, a statistic, an exam fact or a resource. When an exact video can't be
  verified, use a YouTube search link and set `"yt": 1` on the item.
- Keep the person's data private. The plan holds no email address, no IDs and nothing they didn't
  choose to share.
- To change an existing dashboard later, edit the same `plan.json`, keep `meta.storageKey` and
  `meta.progressDoc` unchanged and every existing item id, rebuild, and publish to the same URL. Then
  their ticks, notes and screenshots carry over. See `references/publishing.md`.
