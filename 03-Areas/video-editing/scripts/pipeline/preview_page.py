r"""preview_page.py - Samuel's preview gate: one HTML page per section with every motion-graphic beat as a short
rendered clip beside its script line, Approve / Note per beat, and a button that saves his notes as JSON
(Editor, 2026-10-28; pipeline step 7 in 00-System/model-routing.md -> Audit 2026-10-28).

  python preview_page.py build --beats <beats.json> --section <sec> --comps <comps dir> --docs <job Docs dir>
                         [--kits <kits dir>] [--render] [--wait 3600] [--kinds motion-graphic,overlay,aroll-fx]
                         [--from-render <full timeline render.mp4>] [--res 960x540] [--pad 12]
  python preview_page.py read <notes.json>          what he approved and noted, one line per beat (for the Editor)

Page and clips: <Docs>\Preview <sec> (Editor)\preview_<sec>.html, clips\<beat>_<hash>.mp4 (hash of the manifest and
its .setting files, so a rebuilt beat gets a new clip and an unchanged one is never rendered twice).
Clips come from the render queue (--render submits the missing ones and waits; the queue must be running), or with
--from-render they are cut from an existing render of the timeline (a beat already on it). Screen recordings,
captures, UI demos and B-roll are left out: only beats whose kind is in --kinds and whose manifest holds a comp.
Notes: the page keeps them in the browser while he works; "Save notes" writes preview_<sec>_notes.json (into the
folder he picks where the browser allows it, else Downloads). Read them back with `read`.
"""
import os, sys, json, glob, hashlib, html, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FPS = 23.976
KINDS = ("motion-graphic", "overlay", "aroll-fx")
FFMPEG = "ffmpeg"


def tc(f):
    s = f / FPS
    return "%d:%04.1f" % (s // 60, s % 60)


def _folders(beat, comps):
    out = []
    for name in (beat.get("built") or []) + [beat["id"]]:
        m = os.path.join(comps, name, "manifest.json")
        if os.path.exists(m) and m not in out:
            out.append(m)
    return out


def _hash(mpath):
    h = hashlib.sha1(open(mpath, "rb").read())
    for o in json.load(open(mpath, encoding="utf-8")):
        p = o.get("setting") or o.get("path")
        if p and os.path.exists(p):
            h.update(("%s%d" % (p, os.path.getmtime(p))).encode())
    return h.hexdigest()[:8]


def _span(mpath):
    ops = [o for o in json.load(open(mpath, encoding="utf-8")) if o.get("op") in ("comp", "media")]
    S = min(int(o["start"]) for o in ops)
    return S, max(int(o["start"]) + int(o["D"]) for o in ops) - S, any(o.get("op") == "comp" for o in ops)


def collect(beats, section, comps, kinds):
    rows = []
    for b in beats:
        if b.get("sec") != section or b.get("kind") not in kinds:
            continue
        for m in _folders(b, comps):
            S, D, has_comp = _span(m)
            if has_comp:
                rows.append({"beat": os.path.basename(os.path.dirname(m)), "plan": b["id"], "kind": b["kind"],
                             "family": b.get("family", ""), "alex": b.get("alex", ""), "visual": b.get("visual", ""),
                             "manifest": m, "S": S, "D": D, "hash": _hash(m)})
    return sorted(rows, key=lambda r: r["S"])


def cut_from_render(src, r, dst, pad, res):
    a = max(0.0, (r["S"] - pad) / FPS)
    d = (r["D"] + 2 * pad) / FPS
    cmd = [FFMPEG, "-y", "-v", "error", "-ss", "%.3f" % a, "-i", src, "-t", "%.3f" % d, "-vf",
           "scale=%d:%d" % tuple(res), "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-c:a", "aac", "-b:a",
           "128k", "-movflags", "+faststart", dst]
    return subprocess.run(cmd, capture_output=True, text=True).returncode == 0 and os.path.exists(dst)


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Preview gate %(sec)s</title>
<style>
:root{--bg:#0d0f12;--card:#161a20;--line:#262c35;--ink:#eef1f5;--dim:#8d97a5;--ok:#3ecf8e;--note:#f5b942;--acc:#7cc4ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 Inter,Segoe UI,system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:#0d0f12ee;backdrop-filter:blur(6px);border-bottom:1px solid var(--line);
padding:12px 16px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
h1{font-size:17px;margin:0}.count{color:var(--dim)}.count b{color:var(--ink)}
button{font:inherit;border:1px solid var(--line);background:#1f2530;color:var(--ink);border-radius:6px;padding:7px 12px;cursor:pointer}
button:hover{border-color:var(--acc)}#save{background:var(--acc);color:#071018;border-color:var(--acc);font-weight:600}
main{max-width:1180px;margin:0 auto;padding:16px}
.beat{display:grid;grid-template-columns:minmax(0,560px) minmax(0,1fr);gap:18px;background:var(--card);border:1px solid var(--line);
border-radius:10px;padding:14px;margin:0 0 16px}.beat.approved{border-color:var(--ok)}.beat.noted{border-color:var(--note)}
video{width:100%%;border-radius:6px;background:#000;aspect-ratio:16/9}.missing{aspect-ratio:16/9;display:grid;place-items:center;
color:var(--dim);border:1px dashed var(--line);border-radius:6px;text-align:center;padding:12px}
.id{font-weight:700;font-size:16px}.meta{color:var(--dim);font-size:13px;margin:2px 0 10px}
.alex{font-size:18px;line-height:1.4;margin:0 0 10px}.alex:before{content:"\201C"}.alex:after{content:"\201D"}
details{color:var(--dim);font-size:13px;margin-bottom:10px}textarea{width:100%%;min-height:70px;background:#0f1318;color:var(--ink);
border:1px solid var(--line);border-radius:6px;padding:8px;font:inherit}.row{display:flex;gap:8px;margin:8px 0}
.on-ok{background:var(--ok);color:#06140d;border-color:var(--ok);font-weight:600}.on-note{background:var(--note);color:#1a1205;border-color:var(--note);font-weight:600}
.help{color:var(--dim);font-size:13px}
@media (max-width:820px){.beat{grid-template-columns:1fr}}
</style></head><body>
<header><h1>Preview gate: %(sec)s</h1><span class="count" id="count"></span><span style="flex:1"></span>
<span class="help">Space plays the beat under the mouse. A = approve, N = note.</span><button id="save">Save notes</button></header>
<main>
<p class="help">%(intro)s</p>
%(cards)s
</main>
<script>
const SEC=%(sec_js)s, MADE=%(made_js)s, KEY="preview_"+SEC+"_"+MADE;
const beats=[...document.querySelectorAll(".beat")];
let st={};try{st=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){st={}}
function keep(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
function paint(){let a=0,n=0;beats.forEach(b=>{const s=st[b.id]||{};b.classList.toggle("approved",s.status==="approved");
b.classList.toggle("noted",s.status==="note");b.querySelector(".ok").classList.toggle("on-ok",s.status==="approved");
b.querySelector(".nt").classList.toggle("on-note",s.status==="note");const t=b.querySelector("textarea");if(t&&t.value!==(s.note||""))t.value=s.note||"";
if(s.status==="approved")a++;if(s.status==="note")n++});
document.getElementById("count").innerHTML="<b>"+beats.length+"</b> beats &middot; <b>"+a+"</b> approved &middot; <b>"+n+"</b> with notes &middot; <b>"+(beats.length-a-n)+"</b> open"}
beats.forEach(b=>{const id=b.id;b.querySelector(".ok").onclick=()=>{st[id]={...(st[id]||{}),status:"approved"};keep();paint()};
b.querySelector(".nt").onclick=()=>{st[id]={...(st[id]||{}),status:"note"};keep();paint();b.querySelector("textarea").focus()};
b.querySelector("textarea").oninput=e=>{st[id]={...(st[id]||{}),note:e.target.value,status:e.target.value.trim()?"note":(st[id]||{}).status};keep();paint()}});
let hover=null;beats.forEach(b=>{b.onmouseenter=()=>hover=b});
document.addEventListener("keydown",e=>{if(e.target.tagName==="TEXTAREA"||!hover)return;const v=hover.querySelector("video");
if(e.code==="Space"&&v){e.preventDefault();v.paused?v.play():v.pause()}if(e.key==="a")hover.querySelector(".ok").click();
if(e.key==="n"){e.preventDefault();hover.querySelector(".nt").click()}});
document.getElementById("save").onclick=async()=>{const out={section:SEC,page_made:MADE,saved:new Date().toISOString(),
beats:beats.map(b=>({beat:b.id,plan:b.dataset.plan,clip:b.dataset.clip,status:(st[b.id]||{}).status||"open",note:(st[b.id]||{}).note||""}))};
const text=JSON.stringify(out,null,1),name="preview_"+SEC+"_notes.json";
try{if(window.showSaveFilePicker){const h=await showSaveFilePicker({suggestedName:name,types:[{description:"JSON",accept:{"application/json":[".json"]}}]});
const w=await h.createWritable();await w.write(text);await w.close();alert("Saved "+name);return}}catch(e){if(e.name==="AbortError")return}
const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([text],{type:"application/json"}));a.download=name;a.click()};
paint();
</script></body></html>
"""

CARD = """<section class="beat" id="%(beat)s" data-plan="%(plan)s" data-clip="%(clip)s">
<div>%(media)s</div>
<div><div class="id">%(beat)s</div><div class="meta">%(tc)s &middot; %(dur).1f s &middot; %(kind)s %(family)s</div>
<p class="alex">%(alex)s</p><details><summary>What it should show</summary>%(visual)s</details>
<div class="row"><button class="ok">Approve</button><button class="nt">Note</button></div>
<textarea placeholder="What to change (it goes on the review card and into the fix spec)"></textarea></div>
</section>"""


def build(argv):
    g = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
    beats = json.load(open(g("--beats"), encoding="utf-8"))
    sec, comps, docs = g("--section"), g("--comps"), g("--docs")
    kinds = tuple(g("--kinds", ",".join(KINDS)).split(","))
    res = [int(v) for v in g("--res", "960x540").split("x")]
    pad = int(g("--pad", 12))
    folder = os.path.join(docs, "Preview %s (Editor)" % sec)
    clips = os.path.join(folder, "clips")
    os.makedirs(clips, exist_ok=True)
    rows = collect(beats, sec, comps, kinds)
    for r in rows:
        r["clip_name"] = "%s_%s" % (r["beat"], r["hash"])
        hit = glob.glob(os.path.join(clips, r["clip_name"] + ".*"))
        r["clip"] = os.path.basename(hit[0]) if hit else ""
        r["err"] = ""
    todo = [r for r in rows if not r["clip"]]
    if todo and g("--from-render"):
        for r in todo:
            dst = os.path.join(clips, r["clip_name"] + ".mp4")
            if cut_from_render(g("--from-render"), r, dst, pad, res):
                r["clip"] = os.path.basename(dst)
            else:
                r["err"] = "cut from render failed"
        todo = [r for r in rows if not r["clip"]]
    if todo and "--render" in argv:
        import render_queue as rq
        Q = rq.qdirs(rq.kits_dir(argv))
        if not rq.alive(Q):
            print("render queue is not running: start `render_queue.py run --kits ...` first"); return 2
        ids = {}
        for r in todo:
            i, d = rq.submit(Q, {"id": "preview_" + r["clip_name"], "kind": "clip", "manifest": r["manifest"],
                                 "out": clips, "name": r["clip_name"], "pad": pad, "res": res, "audio": True,
                                 "owner": "preview_page"})
            ids[i] = r
        print("queued %d clips; waiting" % len(ids), flush=True)
        got = rq.wait_done(Q, list(ids), int(g("--wait", 3600)))
        for i, r in ids.items():
            d = got.get(i)
            if d and d.get("ok") and d.get("files"):
                r["clip"] = os.path.basename(d["files"][0])
            else:
                r["err"] = "; ".join((d or {}).get("errors", ["not rendered yet"]))[:200]
    cards = []
    for r in rows:
        media = ('<video src="clips/%s" controls preload="metadata" playsinline></video>' % html.escape(r["clip"])
                 if r["clip"] else '<div class="missing">No clip yet%s</div>' % (
                     "<br>" + html.escape(r["err"]) if r["err"] else ""))
        cards.append(CARD % {"beat": html.escape(r["beat"]), "plan": html.escape(r["plan"]), "clip": html.escape(r["clip"]),
                             "media": media, "tc": tc(r["S"]), "dur": r["D"] / FPS, "kind": html.escape(r["kind"]),
                             "family": html.escape(r["family"]), "alex": html.escape(r["alex"]),
                             "visual": html.escape(r["visual"])})
    made = time.strftime("%Y-%m-%d %H:%M")
    intro = ("Every motion-graphic beat of this section, as rendered, with half a second of A-roll either side and "
             "Alex's sound. Screen recordings, captures and B-roll are not here. Approve what can go on the timeline as "
             "it is; for anything else press Note and say what to change. Then Save notes and tell the Editor.")
    page = PAGE % {"sec": html.escape(sec), "intro": intro, "cards": "\n".join(cards), "sec_js": json.dumps(sec),
                   "made_js": json.dumps(made)}
    out = os.path.join(folder, "preview_%s.html" % sec)
    open(out, "w", encoding="utf-8").write(page)
    json.dump(rows, open(os.path.join(folder, "preview_%s_beats.json" % sec), "w", encoding="utf-8"), indent=1)
    have = sum(1 for r in rows if r["clip"])
    print("preview page: %d beats, %d clips, %d missing -> %s" % (len(rows), have, len(rows) - have, out))
    return 0 if have == len(rows) else 1


def read(path):
    d = json.load(open(path, encoding="utf-8"))
    n = {}
    for b in d["beats"]:
        n[b["status"]] = n.get(b["status"], 0) + 1
    print("%s, saved %s: %s" % (d["section"], d.get("saved"), ", ".join("%d %s" % (v, k) for k, v in sorted(n.items()))))
    for b in d["beats"]:
        if b["status"] != "approved":
            print("%-10s %-8s %s" % (b["beat"], b["status"], b["note"].replace("\n", " / ")))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["build"]:
        sys.exit(build(a[1:]))
    if a[:1] == ["read"]:
        sys.exit(read(a[1]))
    print(__doc__)
