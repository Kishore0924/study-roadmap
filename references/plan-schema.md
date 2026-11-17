# Plan JSON schema

One JSON file describes the whole roadmap. `scripts/build_dashboard.py` checks it and puts it into
the template. Short keys (`th`, `k`, `m` and so on) match what the template reads, so keep them
exactly. `examples/llm-security-5-day.json` is a complete, valid example.

## Top level

```json
{
  "meta": {},
  "learner": {},
  "glossary": [],
  "phases": [],
  "skills": {},
  "days": [],
  "readiness": {},
  "project": {},
  "exam": {"questions": []},
  "setup": []
}
```

## meta

| Field | Required | What it does |
| --- | --- | --- |
| `title` | yes | Page title and big heading, for example "SecAI+ Prep" |
| `subtitle` | no | One line under the title, for example "CompTIA SecAI+ (CY0-001) · exam Fri, Feb 12 · plan runs Jan 4 to Feb 11" |
| `goalDate` | no | YYYY-MM-DD of the exam, start date or goal. Defaults to the last plan day |
| `goalChip` | no | Label on the goal day in the calendar: "Exam", "Start", "Goal" |
| `countdownLabel` | no | Tile label before the goal: "Days to exam" |
| `afterGoalLabel` | no | Tile label after the goal date when the plan continues past it, shown with "Day N": "At the new job" |
| `goalLabel` | no | Tile label on and after the goal day when the plan ends there: "Exam day" |
| `lastWeekLabel` | no | Label for the final calendar week, for example "First week at the new job" |
| `lightDayLabel` | no | Pill text for days marked `ev: 1`, for example "Evening" |
| `searchHint` | no | Placeholder for the All days search box |
| `storageKey` | no | Browser storage key. Set it once (for example "study-roadmap-secai-2027") and never change it |
| `progressDoc` | no | Database document for progress. Default "progress/main". Never change it once published |
| `legendNote` | no | Small print under the Setup tab |
| `examStyle` | no | One sentence added to the prompt that writes fresh exam sets, for example "Match CompTIA's performance-based scenario style." |
| `projectTab` | no | Name of the Project tab. Default "Project" |

## learner

All optional. Used only inside the prompts the dashboard sends to Claude.

```json
{"name": "Sam", "profile": "a help desk technician preparing for CompTIA Security+",
 "goal": "passing the CompTIA Security+ SY0-701 exam",
 "background": "They know Windows support and basic networking, but scripting is new to them."}
```

`profile` completes the sentence "Sam is ...". `goal` completes "Their goal: ...". Leave `name` empty
for a neutral dashboard.

## glossary

10 to 30 key terms, spelled the way they should appear in notes: `["IAM", "OAuth 2.0", "kubectl"]`.

## phases

```json
[{"n": 1, "title": "Foundations", "range": "Jan 4 to 10", "tags": ["Threats and attacks", "Security controls"]}]
```

`n` is a number starting at 1. Every day's `ph` must match one.

## skills

An object of short keys to labels, 4 to 12 entries: `{"net": "Networking", "iam": "Identity and access"}`.
Days list the keys they train in `sk`.

## days

One per calendar day, in order, less than a year in total.

```json
{
  "d": "2027-01-04", "ph": 1, "sk": ["net"], "th": "How networks really move data",
  "why": "Every attack and control later assumes you can picture this.",
  "tag": "Holiday", "ev": 1,
  "items": [
    {"id": "a1", "k": "watch", "t": "Computer Networking Course", "s": "First two hours only. Focus on the OSI layers.", "m": 60, "u": "https://...", "yt": 1},
    {"id": "a2", "k": "lab", "t": "Packet Tracer basics", "s": "Build the two-router lab.", "m": 45, "u": "https://..."},
    {"id": "a3", "k": "build", "t": "Draw your home network", "s": "Every device, subnet and route, on one page.", "m": 30},
    {"id": "a4", "k": "read", "t": "RFC 1918 summary", "s": "Private address ranges.", "m": 10, "u": "https://...", "opt": 1}
  ],
  "q": "Why can't two devices on different subnets talk without a router?",
  "a": "A device sends traffic outside its own subnet to its default gateway. Without a router, nothing forwards it between networks."
}
```

| Item field | Meaning |
| --- | --- |
| `id` | Unique short id across the whole plan (letters, digits, `-`, `_`). Never change it after publishing |
| `k` | `watch`, `lab`, `build` or `read` |
| `t` | Title |
| `s` | One line on what to focus on |
| `m` | Minutes, a positive number |
| `u` | Link, https only. Optional for Build items |
| `yt` | `1` when the link is a YouTube search rather than one exact video |
| `opt` | `1` for optional items, which don't count toward hours |

`tag` (a short pill such as "Holiday" or "Exam day") and `ev` (a lighter day) are optional.

## readiness

```json
{
  "tab": "Exam readiness", "kpi": "Exam readiness", "kpiSub": "objectives you rate confident",
  "intro": "Every exam objective, what it looks like in practice, and the proof you'll have.",
  "jobLabel": "In practice", "proofLabel": "Proof you'll have",
  "groups": [{"title": "Domain 1: General security concepts (12%)", "rows": [
    {"id": "o1.1", "t": "Compare security controls", "jd": "Compare and contrast various types of security controls.",
     "job": "You can say which control type fits a risk and why.", "proof": "Your controls table and the day 3 lab.",
     "days": ["01-04", "01-06"]}
  ]}]
}
```

`jd` holds the official wording of the objective or job line. `days` uses MM-DD and must be plan days.

## project (optional)

Leave it out, or set it to `{}`, for no Project tab.

```json
{"name": "home-lab", "description": "Shown on the Project tab.",
 "brief": "a small home lab with ... Stack: ... (sent to the build guide, so be concrete)",
 "milestones": [["Jan 6", "Firewall rules in place", ["c3"]], ["Jan 9", "Logs flowing to the SIEM", ["f2", "f3"]]]}
```

Each milestone lists the Build item ids that complete it.

## exam

```json
{"questions": [
  {"d": "01-04", "it": "a2", "q": "A user can reach sites by IP but not by name. What failed?",
   "o": ["DHCP", "DNS", "ARP", "NAT"], "a": 1,
   "why": "Name resolution is DNS. Reaching an IP directly proves routing works."}
]}
```

`d` is the day (MM-DD), `it` an item on that day, `o` exactly 4 options, `a` the index of the right
one (0 to 3). Write 50.

## setup

Cards for the Setup tab. A "How to use this dashboard" card is added automatically.

```json
[{"title": "Accounts you need", "items": ["[Microsoft Learn](https://learn.microsoft.com/) (free)", "A free GitHub account"]},
 {"title": "If you fall behind", "text": "Drop optional items first, then ..."}]
```

Links use `[label](https://...)`. Good cards: accounts you need, how the time is laid out, keeping
costs near zero, exam-day logistics, what to do if you fall behind, the daily rhythm, and the
documents each day uses when they uploaded material.
