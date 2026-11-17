# Intake: the questions to ask first

Ask with the app's multiple-choice question tool (AskUserQuestion in Claude apps). It takes up to 4
questions per call, 2 to 4 options each, and always adds an "Other" box for a typed answer, so never
add an "Other" option yourself. Put your recommended option first and add "(Recommended)" to it when
one choice is clearly better for most people. If no question tool exists, ask the same questions in
one short plain-text message with lettered options.

Skip any question the person has already answered. Work out real calendar dates yourself (today's
date is in your context) and show them in the options, for example "Next Monday (Jan 11)".

## Step A: the one typed answer

If they haven't named their goal yet, ask in one short line:

> What are you preparing for? Name the certification (with the exam code if you know it), the job or
> role, or the subject you want to learn.

For a job, also ask them to paste the job description. For a subject, ask what they want to be able
to do by the end, in one sentence.

## Step B: round 1, one question-tool call

1. **Start** (header "Start"): "When do you want to start?"
   Options: Today (date) · Tomorrow (date) · Next Monday (date)
2. **Timeline** (header "Timeline"): "How long until your exam or goal date?"
   Options: 2 weeks · 4 weeks · 6 weeks · 8 weeks. Each description shows the end date.
   If they already have an exam booked, they type the date under Other.
3. **Weekdays** (header "Weekdays"): "How much time can you study on weekdays?"
   Options: About 1 hour · About 2 hours · 3 to 4 hours · 5 hours or more
4. **Weekends** (header "Weekends"): "And on weekends?"
   Options: Same as weekdays · More, I can go longer · Less than weekdays · No study on weekends

## Step C: round 2, one question-tool call

1. **Level** (header "Level"): "Where are you starting from?"
   Options: New to this · Some experience · Experienced, leveling up
   Descriptions say what each means for the plan: more fundamentals, a balance, or depth and speed.
2. **Style** (header "Style", multiSelect true): "How do you like to learn? Pick all that apply."
   Options: Videos · Hands-on labs · Reading · Practice questions
3. **Project** (header "Project"): "Do you want a hands-on project that grows through the plan?"
   Options: Yes, build something as I go (Recommended for technical topics) · No, labs and practice
   questions are enough
4. **Material** (header "Material"): "Do you have study material to upload before I build the plan?"
   Options: Yes, I'll upload it now · No, find the best resources for me
   Descriptions give examples: official exam objectives PDF, a study guide or book chapters, course
   slides, your notes, practice tests, a job description, team docs.

If they pick "Yes, I'll upload it now", reply in one line asking them to upload everything and say
"done". Wait for that before researching.

## Optional: round 3, only when it changes the plan

Ask only if it matters for this goal, in one question-tool call:

- **Name** (header "Name"): "What should the dashboard call you?" Options: their first name if you
  know it · No name, keep it neutral. Used in the helper's prompts, never shown publicly.
- **Avoid** (header "Avoid", multiSelect): things to leave out, such as paid courses, long books,
  cloud accounts that cost money, or late-night sessions.

## After the answers

Restate the plan in two or three lines (goal, dates, hours per weekday and weekend, style), then
start researching. Don't ask for confirmation unless something is contradictory, such as 40 hours of
official training squeezed into one week.
