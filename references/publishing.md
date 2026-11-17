# Build, test, publish and update

## Build

```bash
python3 <skill-dir>/scripts/build_dashboard.py plan.json --check      # validate only
python3 <skill-dir>/scripts/build_dashboard.py plan.json -o dashboard.html
```

The output is one self-contained page: the template with the plan inside a
`<script type="application/json" id="plan-data">` block. It loads nothing from other sites.

## Test

```bash
python3 <skill-dir>/scripts/smoke_test.py dashboard.html
```

It stands in for every Claude capability and clicks through ticking, the self-check, Explain it
simply, read-along, notes with headings and Contents, Help me build, the Final check and its "Study
this" link, then checks for page errors and sideways scrolling at phone width. Fix anything that
fails before publishing. If Playwright isn't installed and can't be installed, say the page wasn't
browser-tested.

## Publish with an Artifact tool

When the session has a tool that publishes Artifact pages (the Artifact tool in Claude apps):

1. Load the artifact-capabilities skill if the session offers it, then publish `dashboard.html` as a
   new artifact.
2. Declare exactly these capabilities, and use the latest runtime version (`contract: "latest"`) so
   the natural voices are available:

   ```json
   {"db": {}, "sample": {"images": true}, "dictation": {}, "assets": {}, "tts": {}}
   ```

3. Use a short generic icon word such as "calendar" or "book".
4. After publishing, read the progress collection once with the artifact database tool to confirm
   saving works (an empty or missing document is fine for a brand new page).

The page itself never needs editing. Everything it shows comes from the plan.

## Without an Artifact tool

Deliver `dashboard.html` as a file. Opened in a browser, the checklist, calendar, readiness, All
days, Project and the Final check work and save in that browser. The Claude-powered features hide
themselves. Say this plainly in the hand-off.

## Update an existing dashboard

1. Get the current plan. If you don't have `plan.json`, read the published page and copy the JSON
   from its `plan-data` block.
2. Edit the plan. Keep `meta.storageKey`, `meta.progressDoc` and every existing item id exactly as
   they are, or saved ticks, notes and screenshots will no longer line up. New items get new ids.
3. Validate, rebuild, test, and publish to the same artifact URL. Leave capabilities out of the
   publish call so the stored set carries forward.

## Moving the dates

To shift the whole plan (they started late), change every day's `d` by the same number of days and
update each MM-DD in `readiness.groups[].rows[].days`, `exam.questions[].d` and the milestone labels.
Item ids stay the same, so progress carries over.
