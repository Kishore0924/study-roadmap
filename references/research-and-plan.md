# Research and plan design

## Research before you write anything

- **Uploaded documents come first.** Read every one fully. Use them to set the scope, the objectives
  and the order of topics. Where they disagree with a website, follow the documents and tell the
  person about the difference. Add their sections as study items, for example
  "Read: Study guide, Chapter 4, pages 88 to 112", with realistic minutes. Draw self-check and Final
  check questions from them too. List which documents each day uses in a Setup card.
- **Certification:** find the official exam objectives (domains, sub-objectives and weights), the
  current exam code and version, the number of questions, the time limit and the passing score, from
  the vendor's own site. Every objective must be covered by at least one day.
- **Job:** read the job description line by line. Every duty and requirement becomes a readiness row
  and is covered by at least one day.
- **Subject:** agree on 4 to 10 concrete outcomes ("can write a Dockerfile that passes a scan") and
  treat them as the objectives.
- **Resources:** video and interactive first, then short reading, matched to the style they picked.
  Prefer free and official sources: vendor training, DeepLearning.AI, Anthropic Academy, PortSwigger
  Web Security Academy, Microsoft Learn, AWS Skill Builder, Google Cloud Skills Boost, freeCodeCamp,
  The Odin Project, Khan Academy, MIT OpenCourseWare, GitHub Skills, TryHackMe, Hack The Box Academy,
  Exercism, and similar, as relevant.
- **Verify every link.** Never invent a URL. When you can't confirm an exact YouTube video, use a
  YouTube search link (`https://www.youtube.com/results?search_query=...`) and set `"yt": 1`.
- **Gap audit before writing the plan:** list each objective and the days that will cover it. Fix any
  objective with no day, and any day that serves no objective.

## Design the plan

- One entry per calendar day from the start date to the end date, grouped into 2 to 5 phases. Give
  each phase a short title, a range ("Jan 4 to 10") and 3 to 6 tags (the objectives it serves).
- Each day has a theme (`th`), one line on why it matters (`why`), 3 to 6 items, one self-check
  question (`q`) and the key points of a good answer (`a`).
- Each item has a type (`watch`, `lab`, `build` or `read`), a title, one line on what to focus on,
  realistic minutes, a link (except most Build items), and `"opt": 1` if it's optional.
- Daily minutes, not counting optional items, must match the hours they chose for weekdays and
  weekends, within about 15 minutes. Optional items are extras for fast days.
- Order inside a day: watch, then lab, then build, then read, so the hands-on work comes while it's fresh.
- Mark holidays and special days with a short `tag`, and lighter days (a busy week, evenings only)
  with `"ev": 1` and a `meta.lightDayLabel` such as "Evening".
- The last days are review plus practice under exam conditions. A Sunday or end-of-week item that
  revisits that week's self-checks is a good habit.
- **Project:** if they want one, design a small project that grows one Build item at a time, with
  milestones that each point at the Build item that completes them. For theory-heavy goals, Build
  items are practice tasks instead: scenario write-ups, flashcard sets, mini case studies.
- **Readiness map:** one row per objective or job line, with the original wording (`jd`), what it
  looks like in practice in one plain sentence (`job`), the proof they'll have by the end (`proof`),
  and the days that cover it (`days`, as MM-DD).
- **Skills:** 4 to 12 skill areas; every day lists the skill keys it trains, which drives the
  coverage bars.
- **Glossary:** 10 to 30 key terms spelled correctly. The notes clean-up uses it to repair dictation.

## The 50 Final check questions

Write them now, at build time, so the exam is instant and uses no extra Claude usage.

- Cover every day, in proportion to the official domain weights where they exist.
- Scenario-based where the real exam is, otherwise practical understanding, never trivia or exact
  course wording.
- Exactly 4 options, exactly one correct, wrong options that are plausible, and an explanation of
  why the right answer is right (`why`, one or two sentences).
- Spread the correct answer evenly across A to D (about 12 or 13 each).
- Map each question to the day (`d`, MM-DD) and the exact item (`it`) that teaches it, and check the
  item really is on that day. The build script checks this too.
- Questions under 40 words, options under 18 words.

## Writing style for everything in the plan

- Plain, friendly, specific. Talk to the learner as "you".
- Sentence case. No em dashes, no arrow symbols, no emoji.
- Every "why" says what the day unlocks, not a summary of the items.
