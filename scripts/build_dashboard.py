#!/usr/bin/env python3
"""Build a Study Roadmap dashboard from a plan JSON file.

    python3 build_dashboard.py plan.json -o dashboard.html
    python3 build_dashboard.py plan.json --check          # validate only

Checks the plan against the rules in references/plan-schema.md, prints a short report,
and writes a single self-contained HTML page (the template with the plan inside it).
Exit code 1 means the plan has errors that must be fixed first.
"""
import argparse, datetime as dt, html, json, pathlib, re, sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE.parent / "assets" / "dashboard-template.html"
KINDS = {"watch", "lab", "build", "read"}
BANNED = {"\u2014": "em dash", "\u2192": "arrow", "\u2190": "arrow", "\u21d2": "arrow", "->": "arrow", "=>": "arrow"}


def walk_strings(node, path="plan"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")


def validate(plan):
    errors, warnings = [], []
    err = errors.append
    warn = warnings.append

    meta = plan.get("meta") or {}
    if not meta.get("title"):
        err("meta.title is required")
    days = plan.get("days") or []
    if not days:
        err("days must have at least one day")
        return errors, warnings

    phases = plan.get("phases") or []
    phase_ids = {p.get("n") for p in phases}
    if not phases:
        err("phases must have at least one phase")
    skills = plan.get("skills") or {}

    seen_dates, item_ids, item_kind, day_of_item = [], set(), {}, {}
    prev = None
    for i, d in enumerate(days):
        where = f"days[{i}]"
        try:
            date = dt.date.fromisoformat(d.get("d", ""))
        except ValueError:
            err(f"{where}.d must be a YYYY-MM-DD date")
            continue
        if prev and date <= prev:
            err(f"{where}.d {date} is not after the previous day")
        elif prev and (date - prev).days > 1:
            warn(f"{where}: gap of {(date - prev).days - 1} day(s) before {date}")
        prev = date
        seen_dates.append(d["d"])
        if d.get("ph") not in phase_ids:
            err(f"{where}.ph {d.get('ph')!r} is not a phase number")
        for k in ("th", "why"):
            if not d.get(k):
                err(f"{where}.{k} is required")
        if not d.get("q") or not d.get("a"):
            warn(f"{where}: no self-check question (q) or key points (a)")
        for sk in d.get("sk") or []:
            if sk not in skills:
                err(f"{where}.sk {sk!r} is not a key in skills")
        items = d.get("items") or []
        if not items:
            err(f"{where} has no items")
        for j, it in enumerate(items):
            w = f"{where}.items[{j}]"
            iid = it.get("id")
            if not iid or not re.fullmatch(r"[A-Za-z0-9_-]{1,24}", str(iid)):
                err(f"{w}.id must be a short id (letters, digits, - or _)")
            elif iid in item_ids:
                err(f"{w}.id {iid!r} is used twice")
            item_ids.add(iid)
            item_kind[iid] = it.get("k")
            day_of_item[iid] = d["d"][5:]
            if it.get("k") not in KINDS:
                err(f"{w}.k must be one of {sorted(KINDS)}")
            if not it.get("t"):
                err(f"{w}.t (title) is required")
            if not isinstance(it.get("m"), (int, float)) or it.get("m") <= 0:
                err(f"{w}.m (minutes) must be a positive number")
            u = it.get("u")
            if u and not re.match(r"https?://", u):
                err(f"{w}.u must start with https://")
            if not u and it.get("k") != "build":
                warn(f"{w} has no link")

    if len(seen_dates) >= 2:
        span = (dt.date.fromisoformat(seen_dates[-1]) - dt.date.fromisoformat(seen_dates[0])).days
        if span >= 365:
            err("the plan must span less than a year (days are matched by month and day)")
    md = {x[5:] for x in seen_dates}
    goal = meta.get("goalDate")
    if goal:
        try:
            dt.date.fromisoformat(goal)
        except ValueError:
            err("meta.goalDate must be a YYYY-MM-DD date")

    rdy = plan.get("readiness") or {}
    rows = [r for g in rdy.get("groups") or [] for r in g.get("rows") or []]
    if not rows:
        err("readiness.groups needs at least one row (one per objective or requirement)")
    covered = Counter()
    rids = set()
    for r in rows:
        w = f"readiness row {r.get('id')!r}"
        if not r.get("id") or r["id"] in rids:
            err(f"{w}: id missing or repeated")
        rids.add(r.get("id"))
        for k in ("t", "jd", "job", "proof"):
            if not r.get(k):
                err(f"{w}.{k} is required")
        if not r.get("days"):
            err(f"{w} has no days (every objective must be covered)")
        for k in r.get("days") or []:
            if k not in md:
                err(f"{w}.days {k!r} is not a plan day (use MM-DD)")
            covered[k] += 1

    proj = plan.get("project")
    if proj and proj.get("name"):
        for x in proj.get("milestones") or []:
            ids = x[2] if isinstance(x, list) else x.get("items", [])
            for iid in ids:
                if iid not in item_ids:
                    err(f"project milestone {x!r} points to unknown item {iid!r}")

    qs = (plan.get("exam") or {}).get("questions") or []
    if len(qs) < 10:
        err(f"exam.questions has {len(qs)} questions; write 50 (at least 10)")
    elif len(qs) != 50:
        warn(f"exam.questions has {len(qs)} questions; 50 is the standard")
    ans = Counter()
    for i, q in enumerate(qs):
        w = f"exam.questions[{i}]"
        if q.get("d") not in md:
            err(f"{w}.d {q.get('d')!r} is not a plan day (MM-DD)")
        elif q.get("it") not in item_ids or day_of_item.get(q.get("it")) != q.get("d"):
            err(f"{w}.it {q.get('it')!r} is not an item on day {q.get('d')}")
        if not isinstance(q.get("o"), list) or len(q["o"]) != 4 or not all(isinstance(o, str) and o for o in q["o"]):
            err(f"{w}.o must be 4 non-empty options")
        if q.get("a") not in (0, 1, 2, 3):
            err(f"{w}.a must be 0, 1, 2 or 3")
        else:
            ans[q["a"]] += 1
        if not q.get("q") or not q.get("why"):
            err(f"{w} needs q and why")
    if qs and ans and max(ans.values()) - min(ans.get(k, 0) for k in range(4)) > max(3, len(qs) // 8):
        warn(f"correct answers are unevenly spread across A to D: {dict(sorted(ans.items()))}")
    exam_days = Counter(q.get("d") for q in qs)
    missing_days = [k for k in sorted(md) if k not in exam_days]
    if qs and missing_days and len(missing_days) > len(md) // 4:
        warn(f"{len(missing_days)} days have no Final check question")

    for path, text in walk_strings(plan):
        for bad, name in BANNED.items():
            if bad in text and not (bad in ("->", "=>") and ("http" in text or "`" in text)):
                err(f"{path} contains an {name} ({bad!r}); rewrite it in plain words")
                break
    return errors, warnings


def report(plan):
    days = plan["days"]
    core = [it for d in days for it in d["items"] if not it.get("opt")]
    mins = sum(it["m"] for it in core)
    qs = (plan.get("exam") or {}).get("questions") or []
    spread = Counter("ABCD"[q["a"]] for q in qs if q.get("a") in (0, 1, 2, 3))
    rows = [r for g in plan["readiness"]["groups"] for r in g["rows"]]
    return (f"{len(days)} days, {days[0]['d']} to {days[-1]['d']} · {len(core)} core items, "
            f"{round(mins / 60, 1)} hours · {len(rows)} readiness rows · "
            f"{len(qs)} exam questions (answers {dict(sorted(spread.items()))})")


def build(plan, template):
    title = plan["meta"]["title"]
    data = json.dumps(plan, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    out = template.replace("{{TITLE}}", html.escape(title)).replace("{{PLAN_JSON}}", data)
    if "{{" in out.split("<script>")[0]:
        raise SystemExit("template placeholders left unfilled")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan")
    ap.add_argument("-o", "--out")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args()
    plan = json.loads(pathlib.Path(a.plan).read_text(encoding="utf-8"))
    errors, warnings = validate(plan)
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"\n{len(errors)} error(s). Fix the plan and run again.")
        sys.exit(1)
    print("ok:", report(plan))
    if a.check:
        return
    out = pathlib.Path(a.out or (pathlib.Path(a.plan).with_suffix(".html")))
    out.write_text(build(plan, pathlib.Path(a.template).read_text(encoding="utf-8")), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
