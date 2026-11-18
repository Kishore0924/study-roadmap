#!/usr/bin/env python3
"""Smoke-test a built dashboard in a headless browser before publishing.

    python3 smoke_test.py dashboard.html [--shots out_dir]

Wraps the page with stand-ins for every Claude capability (sample, tts, dictation off, db off),
then ticks an item, runs the self-check, asks the helper, reads an answer aloud, saves a note,
opens the notes panel and its Contents menu, plans a build guide, takes the Final check,
follows a "Study this" link, and checks phone width on several days.
Needs Playwright for Python with Chromium. Exit code 1 means something failed.
"""
import json, os, pathlib, sys, tempfile

STUB = r"""
const ANSWER = "Think of it like the keys to a building. Each person gets only the keys they need.\n\n- One point.\n- Another point.\n\nIn real terms:\nA precise sentence.\n\nQuick check: what is least privilege?";
const S = async (input, opts) => { await new Promise(r=>setTimeout(r,20)); const t = typeof input==="string" && input.includes("Now teach step") ? "What we're doing:\nSet up.\nDo this:\n1. Run it.\n```bash\necho hi\n```\nThis prints hi." : ANSWER; if(opts && opts.onText) opts.onText({text:t, delta:t}); return {text:t, truncated:false}; };
S.json = async (input) => {
  const s = typeof input==="string" ? input : JSON.stringify(input);
  await new Promise(r=>setTimeout(r,30));
  if(s.includes("short topic headings")){ const ids=[...s.matchAll(/^\[(n\d+)\]/gm)].map(m=>m[1]); return {headings: ids.map(id=>({id, heading:"Heading "+id}))}; }
  if(s.includes("multiple-choice exam questions")){ const m=[...s.matchAll(/Day (\d\d-\d\d):[^\n]*\n  Items: \[([^\]]+)\]/g)]; const n=Number((s.match(/Write (\d+) multiple/)||[])[1]||10); return {questions:Array.from({length:n},(_,i)=>{ const x=m[i%m.length]; return {q:"Generated "+i,options:["w","x","y","z"],answer:i%4,why:"because",day:x[1],item:x[2]}; })}; }
  if(s.includes("self-check questions")) return {questions:[{q:"Q2",a:"k"},{q:"Q3",a:"k"},{q:"Q4",a:"k"},{q:"Q5",a:"k"}]};
  if(s.includes("Review a short answer")) return {verdict:"partial",right:["good start"],wrong:["mixed up X"],missing:["Y"],tip:"remember Z",model:"model answer"};
  if(s.includes("cleaning up notes")) return {notes:"Title:\n- point one\n- point two", changes:["a to b (misheard)"], suggestions:["add c"]};
  if(s.includes("Plan this build")) return {goal:"Build it", big_picture:"Like lego. Real terms.", you_need:["Python"], steps:[{title:"Set up",summary:"Install"},{title:"Write code",summary:"Code"}]};
  return {};
};
S.limits = async () => ({images:null});
const LH=[], PH=[]; let cur=null;
function play(r){ const step=()=>{ if(cur!==r||r.paused) return; const l=r.lines[r.k]; if(!l){ cur=null; r.res({playedMs:1}); return; } if(r.ms===0) LH.forEach(h=>h({line:r.k,id:l.id})); PH.forEach(h=>h({ms:r.ms,line:r.k,id:l.id})); r.ms+=100; if(r.ms>l.text.length*70){ r.k++; r.ms=0; } r.t=setTimeout(step,10); }; step(); }
const T={ speak(w,o){ const lines=typeof w==="string"?[{text:w}]:w; if(cur){ const x=cur; cur=null; clearTimeout(x.t); x.rej({code:"stopped",reason:"replaced"}); } return new Promise((res,rej)=>{ const r={lines,k:0,ms:0,res,rej,paused:false}; cur=r; setTimeout(()=>play(r),5); }); },
  async stop(){ if(cur){ const x=cur; cur=null; clearTimeout(x.t); x.rej({code:"stopped",reason:"stopped"}); } }, async pause(){ if(cur){ cur.paused=true; clearTimeout(cur.t);} }, async resume(){ if(cur&&cur.paused){ cur.paused=false; play(cur);} },
  async setRate(){}, active(){ return !!cur; }, async voices(){ return ["buttery","airy","glassy","rounded"]; }, onState(){ return ()=>{}; }, onLine(h){ LH.push(h); return ()=>{}; }, onPosition(h){ PH.push(h); return ()=>{}; } };
window.claude={use: async n => n==="sample" ? S : n==="tts" ? T : null};
"""
SKELETON = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><script>{stub}</script>{page}</body></html>'


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    page = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    shots = pathlib.Path(sys.argv[sys.argv.index("--shots") + 1]) if "--shots" in sys.argv else None
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("skip: Playwright for Python is not installed (pip install playwright, then playwright install chromium)")
        return
    tmp = pathlib.Path(tempfile.mkdtemp()) / "page.html"
    tmp.write_text(SKELETON.replace("{stub}", STUB).replace("{page}", page), encoding="utf-8")
    fails, log = [], []
    check = lambda ok, what: (log.append(("ok  " if ok else "FAIL") + " " + what), None if ok else fails.append(what))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page(viewport={"width": 1280, "height": 1000})
        p.set_default_timeout(5000)
        errs = []
        p.on("pageerror", lambda e: errs.append(str(e)))
        p.route("**/*", lambda r: r.abort() if not r.request.url.startswith("file:") else r.continue_())
        p.goto(tmp.as_uri()); p.wait_for_timeout(600)
        p.evaluate("showTab('dash'); selectDay(0)"); p.wait_for_timeout(100)
        box = p.locator("#dayItems input[type=checkbox]").first
        before = box.is_checked(); box.click(); p.wait_for_timeout(50)
        check(box.is_checked() != before, "ticking an item")
        box.click()
        p.fill("#quizA", "my answer"); p.click("[data-qact='check']"); p.wait_for_timeout(250)
        check(p.locator("#quiz .fb-v").count() == 1, "self-check review")
        p.click("[data-qact='next']"); p.wait_for_timeout(250)
        check(p.locator("#quiz .quiz-q").count() == 1, "self-check writes the next questions")
        p.fill("#askq", "Explain this simply"); p.click("#askSend"); p.wait_for_timeout(300)
        check(p.locator("#askLog .bub.ai").count() >= 1, "Explain it simply answers")
        p.click("[data-ra='play']"); p.wait_for_timeout(300)
        check(p.locator("#askLog .s.on").count() == 1, "read-along highlights a sentence")
        p.click("[data-ra='stop']")
        p.fill("#note", "rent an essay notes"); p.click("#tidy"); p.wait_for_timeout(300)
        check(p.input_value("#note").startswith("Title"), "Clean up with AI")
        p.click("#noteSave"); p.wait_for_timeout(300)
        key = p.evaluate("Object.keys(state.inotes)[0]")
        p.evaluate(f"openNotesPanel({json.dumps(key)})"); p.wait_for_timeout(300)
        check(p.locator("#ndBody .ncard-t").count() >= 1 and not p.locator("#ndBody .ncard-t.pend").count(), "saved note gets a heading")
        p.click("#ndTocBtn"); p.wait_for_timeout(50)
        check(p.locator("#ndToc [data-ndgo]").count() >= 1, "Contents menu lists headings")
        if shots: p.screenshot(path=str(shots / "notes.png"))
        p.keyboard.press("Escape"); p.keyboard.press("Escape"); p.wait_for_timeout(50)
        bid = p.evaluate("(DAYS.flatMap(d=>d.items).find(i=>i.k==='build')||{}).id || ''")
        if bid:
            p.evaluate(f"selectDay(idxOfItem[{json.dumps(bid)}])"); p.wait_for_timeout(100)
            p.click(f"[data-guide='{bid}']"); p.wait_for_timeout(100)
            if p.locator("[data-gact='plan']").count(): p.click("[data-gact='plan']"); p.wait_for_timeout(300)
            check(p.locator("#gdBody .gs").count() >= 1, "Help me build plans the steps")
            p.keyboard.press("Escape")
        p.click("#t-exam"); p.wait_for_timeout(50); p.click("[data-exact='start-core']"); p.wait_for_timeout(80)
        ans = p.evaluate("EXAM_CORE.map(q=>q.a)")
        for i, a in enumerate(ans):
            p.click(f"[data-exgo='{i}']"); p.check(f"#exam input[name='exq'][value='{a if i else (a + 1) % 4}']")
        p.click("[data-exact='submit']"); p.wait_for_timeout(100)
        if p.locator("[data-exact='confirm']").count(): p.click("[data-exact='confirm']"); p.wait_for_timeout(100)
        check(p.locator("#exam .ex-miss").count() == 1, "Final check scores and lists the miss")
        if shots: p.screenshot(path=str(shots / "final-check.png"))
        p.locator("#exam .ex-miss .nbtn").first.click(); p.wait_for_timeout(300)
        check(p.locator(".item.flash").count() == 1, "Study this link opens the exact item")
        for t in ["role", "all", "setup"] + (["proj"] if p.is_visible("#t-proj") else []):
            p.click("#t-" + t); p.wait_for_timeout(80)
        check(not errs, "no page errors" + (": " + "; ".join(errs[:3]) if errs else ""))
        m = b.new_page(viewport={"width": 390, "height": 844})
        m.route("**/*", lambda r: r.abort() if not r.request.url.startswith("file:") else r.continue_())
        m.goto(tmp.as_uri()); m.wait_for_timeout(500)
        n = m.evaluate("DAYS.length")
        widths = []
        for i in sorted({0, n // 3, (2 * n) // 3, n - 1}):
            m.evaluate(f"showTab('dash'); selectDay({i})"); m.wait_for_timeout(60)
            widths.append(m.evaluate("document.documentElement.scrollWidth"))
        check(max(widths) <= 390, f"no sideways scroll at 390px wide {widths}")
        b.close()
    print("\n".join(log))
    if fails:
        print(f"\n{len(fails)} check(s) failed.")
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
