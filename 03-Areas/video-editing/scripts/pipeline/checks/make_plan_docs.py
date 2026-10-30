# Merges a plan's section files into beats.json and builds the readable one-page plan (summary, coloured sections, a row per beat, hero thumbnails).
# Usage: python make_plan_docs.py --config plan.json --sections-dir <sections> --words cut_words.json --sents sentences.json --xml cut.xml --captures captures.json --sections-json sections.json --out <dir> [--frames <dir>]
# Promoted from video 4 on 2026-10-30.
"""make_plan_docs.py - merges a plan's section files and builds the readable plan (Editor, 2026-10-26).

Section files <group>.json, sections coloured like the Resolve sections (sections.json), plan_check.py's results
in the summary, hero thumbnails from frames/ when they exist. The per-video wording (title, plan name, subtitle,
part labels, capture note) comes from the --config json (video 4's: examples/video4_plan.json).

Writes into --out:
  beats.json            every beat in timeline order (+ "file": its section file, "hero": frame if one exists)
  <plan_name>.html      one page: summary, then a row per beat under coloured section headers
Re-run after any section edit or when frames/ gets new stills.
"""
import argparse, json, os, html, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_check as pc

FRAMES = None  # set in main()
FPS_TC = 24  # Resolve shows 23.976 timelines with 24-frame timecode
RESOLVE = {"Orange": "#EB6E01", "Apricot": "#FFA833", "Yellow": "#E2A92B", "Lime": "#9FC613", "Olive": "#5F9932",
           "Green": "#448F65", "Teal": "#00989A", "Navy": "#15627E", "Blue": "#4495E3", "Purple": "#8B5FBF",
           "Violet": "#C150A0", "Pink": "#E980C4", "Tan": "#B9AF97", "Beige": "#C4915E", "Brown": "#996633",
           "Chocolate": "#8C5A3F"}
LIGHT = {"Yellow", "Lime", "Tan", "Pink", "Apricot", "Beige"}
KIND = {"demo": ("Live demo", "#1f6feb"), "capture": ("Capture", "#0e7c86"), "mograph": ("Motion graphic", "#8250df"),
        "broll": ("B-roll", "#bc4c00"), "aroll-fx": ("A-roll + graphic", "#6e7781"), "none": ("A-roll", "#afb8c1")}
STATUS = {"have": "#2da44e", "capture": "#0969da", "build": "#8250df", "flow": "#bf3989"}


def tc(f):
    return f"{f // (FPS_TC * 60)}:{(f // FPS_TC) % 60:02d}:{f % FPS_TC:02d}"


def one(x):
    if isinstance(x, list):
        x = " / ".join(one(i) for i in x)
    elif isinstance(x, dict):
        x = "; ".join(f"{k}: {one(v)}" for k, v in x.items())
    return str(x or "").replace("\r", " ").strip()


def esc(x):
    return html.escape(one(x)).replace("\n", "<br>")


def frame_for(bid):
    if not os.path.isdir(FRAMES):
        return None
    hits = sorted(f for f in os.listdir(FRAMES)
                  if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
                  and (f.startswith(bid + ".") or f.startswith(bid + "_") or f.startswith(bid + " ")))
    return "frames/" + hits[0] if hits else None


def main():
    global FRAMES
    ap = argparse.ArgumentParser(description="Merge a plan's section files into beats.json and one readable html page.")
    pc.add_args(ap)
    ap.add_argument("--sections-json", required=True, help="sections.json: colour + title per section, in section order")
    ap.add_argument("--out", required=True, help="folder for beats.json and the html")
    ap.add_argument("--frames", help="hero stills folder (default: <out>/frames)")
    ARGS = ap.parse_args()
    pc.configure(ARGS)
    CFG = pc.CFG
    TITLE, PLAN = CFG["title"], CFG.get("plan_name", "Visual plan")
    OUT = ARGS.out
    os.makedirs(OUT, exist_ok=True)
    FRAMES = ARGS.frames or os.path.join(OUT, "frames")
    R = pc.check()
    beats, groups = pc.load()
    caps = json.load(open(pc.CAPS, encoding="utf-8"))
    alias = {}
    for c in caps["captures"]:
        alias[c["id"]] = c["id"]
        for v in (c.get("sec_ids") or {}).values():
            alias[v] = c["id"]
    secj = json.load(open(ARGS.sections_json, encoding="utf-8"))
    colours = [s["colour"] for s in secj]
    titles = [s["title"] for s in secj]

    # merge
    used_caps, bld, flow, have = {}, set(), set(), 0
    for b in beats:
        b["file"] = b.pop("_g")
        fr = frame_for(b["id"])
        if fr:
            b["hero"] = fr
        for a in b.get("assets") or []:
            if not isinstance(a, dict):
                continue
            p_ = one(a.get("path"))
            for tok in re.findall(r"CAP-[A-Z0-9]+(?:-\d+)?", p_):
                if tok in alias:
                    used_caps.setdefault(alias[tok], set()).add(b["id"])
            bld.update(re.findall(r"BLD-[A-Z0-9]+-\d+", p_))
            flow.update(re.findall(r"FLOW-[A-Z0-9]+-\d+", p_))
            if a.get("status") == "have":
                have += 1
    json.dump(beats, open(os.path.join(OUT, "beats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    vis = [b for b in beats if b["kind"] != "none"]
    kinds = Counter(b["kind"] for b in beats)
    heroes = [b for b in beats if b.get("hero")]
    unused = [c for c in caps["captures"] if c["id"] not in used_caps]
    needed = [c for c in caps["captures"] if c["id"] in used_caps]
    calls = [c for c in caps["captures"] if c.get("samuel_call")]
    nums = [n for n in caps.get("numbers", [])  # flags only: what differs from a source or isn't verified
            if not str(n.get("status", "")).lower().startswith(("match", "internal", "n/a", "ok"))]
    notes = [(b["id"], n) for b in beats for n in (b.get("assembler_note") or [])]
    P = R["parts"]

    H = []
    a = H.append
    a("<!doctype html><html lang='en'><head><meta charset='utf-8'>")
    a(f"<title>{html.escape(PLAN)} - {html.escape(TITLE)}</title>")
    a("""<style>
body{font:14px/1.45 Inter,Segoe UI,Arial,sans-serif;margin:0;background:#f6f8fa;color:#1f2328}
.wrap{max-width:1680px;margin:0 auto;padding:24px}
h1{font-size:26px;margin:0 0 4px} .sub{color:#57606a;margin:0 0 18px}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 16px}
.card{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:12px 16px;min-width:150px}
.card b{display:block;font-size:24px} .card span{color:#57606a;font-size:12px}
.box{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:12px 16px;margin:0 0 14px}
.box h2{font-size:16px;margin:0 0 8px} .box ul{margin:4px 0 0 18px;padding:0}
table{border-collapse:collapse;width:100%;background:#fff;table-layout:fixed}
th,td{border:1px solid #d0d7de;padding:8px;vertical-align:top;text-align:left;overflow-wrap:anywhere;word-break:break-word}
th{background:#24292f;color:#fff;position:sticky;top:0;z-index:2;font-size:12px}
tr.sec td{font-weight:700;font-size:16px;padding:10px 12px}
tr.aroll td{background:#f6f8fa;color:#57606a}
.tc{font-family:Consolas,monospace;font-size:12px;white-space:nowrap}
.id{font-weight:700;font-size:13px}
.k{display:inline-block;color:#fff;border-radius:4px;padding:1px 6px;font-size:11px;font-weight:600;margin:0 4px 4px 0}
.c{display:inline-block;max-width:100%;background:#eaeef2;border-radius:4px;padding:1px 6px;font-size:11px;margin:0 4px 4px 0;font-family:Consolas,monospace}
.alex{font-style:italic} .small{font-size:12px;color:#57606a} .motion{font-size:12px}
.ost{font-weight:600}
img.hero{width:100%;max-width:320px;border-radius:4px;border:1px solid #d0d7de;display:block;margin:0 0 6px}
details summary{cursor:pointer;color:#0969da;font-size:12px}
.ok{color:#1a7f37;font-weight:600} .warn{color:#9a6700;font-weight:600}
</style></head><body><div class='wrap'>""")
    a(f"<h1>{html.escape(PLAN)} &middot; {html.escape(TITLE)}</h1>")
    a(CFG["subtitle"])
    a("<div class='cards'>")
    for v, lab in ((len(beats), "beats"), (len(vis), "visuals"), (kinds.get("demo", 0) + kinds.get("capture", 0), "live demos / captures"),
                   (kinds.get("mograph", 0), "motion graphics"), (kinds.get("broll", 0), "B-roll"),
                   (kinds.get("aroll-fx", 0), "A-roll + graphic"), (kinds.get("none", 0), "A-roll breaths"),
                   (f"{R['coverage_total']} %", "of the cut under visuals"),
                   (len(needed), f"captures needed (of {len(caps['captures'])} listed)"), (len(bld), "builds (BLD)"),
                   (len(flow), "Flow B-roll"), (len(heroes), "hero frames")):
        a(f"<div class='card'><b>{v}</b><span>{html.escape(lab)}</span></div>")
    a("</div>")

    # coverage and check
    a("<div class='box'><h2>Coverage and plan check</h2><ul>")
    for name, lab in CFG["part_labels"].items():
        p = P[name]
        cls = "ok" if p["ok"] else "warn"
        a(f"<li>{lab}: <span class='{cls}'>{p['coverage']} %</span> under visuals (target {'about ' if name == 'body' else 'at least '}{p['target']} %), "
          f"plain A-roll over {p['limit']} f: {esc(p['plain_over_limit'] or 'none')}</li>")
    clean = all(not R[k] for k in ("holes", "double_frames", "overlaps", "seams", "duplicate_ids", "schema",
                                   "sec_code_mismatch", "sents_outside_beat", "capture_ids_unknown", "starts_off_word"))
    a(f"<li>Every frame 0-{pc.TOTAL} sits in exactly one beat; no overlaps, no gaps, group seams meet, every visual starts on its word or a cut: "
      f"<span class='{'ok' if clean else 'warn'}'>{'yes' if clean else 'NO, see plan_check.py'}</span></li>")
    a(f"<li>A-roll slivers left for the Editor's call ({len(R['slivers'])}): {esc(R['slivers'] or 'none')}</li>")
    a(f"<li>Edge fixes made at assembly: {len(notes)} edits on {len({i for i, _ in notes})} beats (each beat says so in its notes).</li>")
    a("</ul></div>")

    # Samuel's calls
    a("<div class='box'><h2>Decisions waiting on Samuel</h2><ul>")
    for c in calls:
        moot = " <span class='small'>(not used by the plan: no call needed unless he wants it back)</span>" if c in unused else ""
        a(f"<li><b>{esc(c['id'])}</b> {esc(c['name'])}: {esc(c['samuel_call'])}{moot}</li>")
    for n in nums:
        a(f"<li><b>{esc(n.get('id'))}</b> ({esc(n.get('sentences'))}) Alex: \"{esc(n.get('alex'))}\" &middot; source: {esc(n.get('source'))} &middot; "
          f"{esc(n.get('status'))}: {esc(n.get('action'))}</li>")
    a("</ul></div>")

    # captures
    a("<div class='box'><h2>Captures needed</h2><p class='small'>Full URLs, access and method: <a href='CAPTURE LIST.md'>CAPTURE LIST.md</a>. "
      + CFG.get("captures_note", "") + "</p><ul>")
    for c in needed:
        a(f"<li><b>{esc(c['id'])}</b> [{esc(c['priority'])}, {esc(c['kind'])}] {esc(c['name'])} &middot; <span class='small'>beats {esc(', '.join(sorted(used_caps[c['id']])))}</span></li>")
    if unused:
        a("<li class='small'>Listed but not used by any beat: " + esc(", ".join(f"{c['id']} {c['name']}" for c in unused)) + "</li>")
    a("</ul></div>")

    # table
    a("<table><colgroup><col style='width:110px'><col style='width:15%'><col style='width:24%'><col style='width:12%'>"
      "<col style='width:24%'><col style='width:14%'></colgroup>")
    a("<thead><tr><th>Beat &middot; timecode</th><th>Alex says</th><th>The visual</th><th>On screen</th><th>Motion</th><th>CAP / assets</th></tr></thead><tbody>")
    for i, (code, s0, s1) in enumerate(pc.SECTIONS):
        col = colours[i] if i < len(colours) else "Blue"
        bg = RESOLVE.get(col, "#4495E3")
        fg = "#1f2328" if col in LIGHT else "#fff"
        bs = [b for b in beats if b.get("sec") == code]
        cov = sum(b["end"] - b["start"] for b in bs if b["kind"] != "none")
        span = (max(b["end"] for b in bs) - min(b["start"] for b in bs)) if bs else 1
        a(f"<tr class='sec'><td colspan='6' style='background:{bg};color:{fg}'>{esc(code)} &middot; {esc(titles[i] if i < len(titles) else code)} "
          f"<span style='font-weight:400;font-size:13px'>&middot; {tc(s0)}-{tc(s1)} &middot; {len(bs)} beats &middot; {100 * cov / span:.0f} % visuals &middot; {col}</span></td></tr>")
        for b in bs:
            k, kc = KIND.get(b["kind"], (b["kind"], "#6e7781"))
            rowc = " class='aroll'" if b["kind"] == "none" else ""
            d = b["end"] - b["start"]
            a(f"<tr{rowc}><td><div class='id'>{esc(b['id'])}</div><div class='tc'>{tc(b['start'])}-{tc(b['end'])}</div>"
              f"<div class='small'>f {b['start']}-{b['end']}<br>{d} f &middot; {d / pc.FPS:.1f} s<br>{esc(' '.join(b.get('sents') or []))}</div></td>")
            a(f"<td class='alex'>{esc(b.get('alex'))}</td>")
            cell = ""
            if b.get("hero"):
                cell += f"<a href='{html.escape(b['hero'])}'><img class='hero' src='{html.escape(b['hero'])}' alt='{esc(b['id'])}'></a>"
            cell += f"<span class='k' style='background:{kc}'>{esc(k)}</span>"
            if one(b.get("construct")) and one(b.get("construct")).upper() != "NONE":
                cell += f"<span class='c'>{esc(b['construct'])}</span>"
            if one(b.get("family")):
                cell += f"<span class='c'>{esc(b['family'])}</span>"
            cell += f"<div>{esc(b.get('visual'))}</div>"
            if one(b.get("why")):
                cell += f"<div class='small'><b>Why:</b> {esc(b['why'])}</div>"
            more = [(lab, b.get(f)) for f, lab in (("reuses", "Reuses"), ("layers", "Layers"), ("track", "Track"), ("sfx", "SFX (after approval)"),
                                                   ("risk", "Risk / fallback"), ("assembler_note", "Assembly edits")) if one(b.get(f)) and one(b.get(f)).lower() != "none"]
            if more:
                cell += "<details><summary>reuses, layers, SFX, risk</summary><div class='small'>" + "".join(
                    f"<p><b>{lab}:</b> {esc(v)}</p>" for lab, v in more) + "</div></details>"
            a(f"<td>{cell}</td>")
            a(f"<td class='ost'>{esc(b.get('text'))}</td>")
            a(f"<td class='motion'>{esc(b.get('motion'))}</td>")
            ac = ""
            for x in b.get("assets") or []:
                if isinstance(x, dict):
                    st = one(x.get("status"))
                    path = one(x.get("path"))
                    shown = os.path.basename(path.rstrip("\\/")) if (":" in path or "\\" in path) else path
                    ac += (f"<div style='margin:0 0 6px'><span class='k' style='background:{STATUS.get(st, '#6e7781')}'>{esc(st)}</span>"
                           f"<span class='c' title='{html.escape(path)}'>{html.escape(shown[:80])}</span><div class='small'>{esc(x.get('what'))}</div></div>")
                else:
                    ac += f"<div class='small'>{esc(x)}</div>"
            a(f"<td>{ac}</td></tr>")
    a("</tbody></table>")
    a("<p class='small'>Sources: <a href='PLAN BRIEF.md'>PLAN BRIEF.md</a> (the rules), <a href='CAPTURE LIST.md'>CAPTURE LIST.md</a>, "
      "PLAN gNN.md and REVIEW gNN.md per group, <a href='beats.json'>beats.json</a>. Checked with <code>plan_check.py</code>.</p>")
    a("</div></body></html>")
    open(os.path.join(OUT, PLAN + ".html"), "w", encoding="utf-8").write("\n".join(H))
    print(f"beats={len(beats)} visuals={len(vis)} demos={kinds.get('demo', 0) + kinds.get('capture', 0)} coverage={R['coverage_total']}% "
          f"captures_needed={len(needed)}/{len(caps['captures'])} unused={[c['id'] for c in unused]} bld={len(bld)} flow={len(flow)} "
          f"heroes={len(heroes)} calls={len(calls)} number_flags={len(nums)} assembly_edits={len(notes)}")


if __name__ == "__main__":
    main()
