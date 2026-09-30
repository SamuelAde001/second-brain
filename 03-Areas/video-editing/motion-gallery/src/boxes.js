// BOXES — B01..B08. Containers that hold a list, a comparison, a conversation or a set of results.

D("B01", {
  name: "Checklist box, upcoming rows blurred", cat: "box", loop: 6.4,
  use: "<b>“In this video” and agenda beats.</b> All rows show at once but blurred; each one sharpens as he says it and its number turns orange. Signposting, the Route Rise guide's retention device.",
  ref: { id: "I10", label: "Visual Inspo #10 · best editor 38" },
  recipe: ["#2d2c2b", "#FF5A1F", "#FD9457", "#ffffff"],
  fusion: "Glass Rectangle + a second Rectangle outline with a gradient → NeoGlow for the rim. Rows: Rectangles with Blur keyed 9 → 0 on the word. Star: Polygon (4 points) + NeoGlow.",
}, (S) => {
  const { el, W, A, F, pop, tt, prog, ringMask } = S;
  S.ground("warm", { grid: true });
  const X = 500, Y = 120, BW = 920, BH = 840;
  const box = W(null, X, Y, BW, BH);
  const rimG = "linear-gradient(160deg, #FFC19C, #FF5A1F 28%, rgba(255,90,31,.12) 58%, rgba(255,90,31,.65))";
  const glow = el(box, "abs", Object.assign({ inset: "-12px", borderRadius: "60px", padding: "12px", filter: "blur(16px)", background: rimG }, ringMask));
  el(box, "abs m-dark", { inset: 0, borderRadius: "48px" });
  el(box, "abs", Object.assign({ inset: "-3px", borderRadius: "51px", padding: "3px", background: rimG }, ringMask));
  el(box, "abs caps", { left: "64px", top: "56px", fontSize: "28px", fontWeight: 800, letterSpacing: ".24em", color: "#FD9457" }, "In this video");
  el(box, "abs", { left: "64px", right: "64px", top: "108px", height: "1.5px", background: "linear-gradient(90deg, rgba(253,148,87,.6), transparent)" });
  F((t) => { glow.style.opacity = (0.55 + 0.3 * Math.sin(t * 2.2)).toFixed(3); });
  const rows = ["Why Apollo *stopped working*", "The *skill* I built instead", "How it *finds* accounts", "What it *costs* you"];
  rows.forEach((r, i) => {
    const rw = W(box, 50, 150 + i * 162, BW - 100, 134);
    el(rw, "abs row m-glass", { inset: 0, borderRadius: "30px", padding: "0 120px 0 40px", fontSize: "43px", fontWeight: 700, letterSpacing: "-.01em", whiteSpace: "nowrap" }, `<span>${tt(r, "#FD9457")}</span>`);
    const nb = W(rw, BW - 100 - 100, 31, 72, 72);
    const nc = el(nb, "abs center num", { inset: 0, borderRadius: "50%", fontSize: "34px", fontWeight: 850, background: "#fff", color: "#1B0903", boxShadow: "0 8px 20px rgba(0,0,0,.35)" }, String(i + 1));
    const a = 0.5 + i * 0.12, on = 1.1 + i * 1.0;
    A(rw, { o: [[a, 0], [a + 0.3, 1, "out"]], y: [[a, 40], [a + 0.45, 0, "expo"]], blur: [[a, 14], [a + 0.4, 9], [on, 9], [on + 0.35, 0, "out"]], br: [[a, 0.5], [on, 0.5], [on + 0.35, 1, "out"]] });
    A(nb, { s: [[on, 1], [on + 0.12, 1.28, "out"], [on + 0.4, 1, "back"]] });
    F((t) => { const lit = t >= on + 0.08; nc.style.background = lit ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#fff"; nc.style.color = lit ? "#fff" : "#1B0903"; });
  });
  const sp = W(null, X - 78, Y - 78, 156, 156);
  sp.innerHTML = `<svg width="156" height="156" viewBox="0 0 150 150" style="filter:drop-shadow(0 0 16px rgba(255,120,60,.9))"><defs><linearGradient id="b01s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE0CC"/><stop offset=".5" stop-color="#FD9457"/><stop offset="1" stop-color="#FF5A1F"/></linearGradient></defs><path d="M75 4 C80 56 94 70 146 75 C94 80 80 94 75 146 C70 94 56 80 4 75 C56 70 70 56 75 4Z" fill="url(#b01s)"/></svg>`;
  pop(sp, 0.55, { s0: 0, ease: "back2", dur: 0.6 });
  A(sp, { rz: [[0.55, -90], [1.2, 0, "expo"], [6.4, 40, "lin"]] });
  A(box, { s: [[0.2, 0.94], [0.8, 1, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]], blur: [[0.2, 12], [0.6, 0, "out"]] });
});

D("B02", {
  name: "Window compare, theirs vs yours", cat: "box", loop: 6.2,
  use: "<b>Before/after, template vs real.</b> One window, two panels. Theirs goes grey and gets the ✗; yours gets a drawn orange frame, a ✓ and a marker on the words that matter.",
  ref: { id: "I61", label: "Visual Inspo #61 · Andy Stauring's editor" },
  recipe: ["#1c1c1c", "#ffffff", "#FF5A1F", "#8C8C8C"],
  fusion: "Window: dark Rectangle + title bar Rectangle + three Ellipses. Panels: grey and white Rectangles. Frame: Polyline rectangle with Write-On + NeoGlow. Theirs: Saturation 0 + Brightness keyed down.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, prog, ripple } = S;
  S.ground("graphite", { grid: "dots" });
  const X = 210, Y = 120, WW = 1500, WH = 840;
  const win = W(null, X, Y, WW, WH);
  const body = el(win, "abs m-dark clip", { inset: 0, borderRadius: "34px" });
  const bar = el(body, "abs row", { left: 0, right: 0, top: 0, height: "78px", padding: "0 30px", gap: "14px", background: "rgba(255,255,255,.04)", borderBottom: "1px solid rgba(255,255,255,.07)" });
  ["#FF5A1F", "#FD9457", "#6a6a6a"].forEach((c) => el(bar, "", { width: "22px", height: "22px", borderRadius: "50%", background: c }));
  el(bar, "abs center", { left: 0, right: 0, top: 0, bottom: 0, fontSize: "26px", fontWeight: 600, color: "#9a9a9a" }, "Cold email · first line");
  const P = 580, PH = 560, py = 190, lx = 110, rx = WW - 110 - P;
  el(body, "abs caps", { left: lx + "px", top: "124px", fontSize: "28px", fontWeight: 800, letterSpacing: ".2em", color: "#8C8C8C" }, "Theirs");
  el(body, "abs caps", { left: rx + "px", top: "124px", fontSize: "28px", fontWeight: 800, letterSpacing: ".2em", color: "#FF5A1F" }, "Yours");
  const lp = W(body, lx, py, P, PH);
  el(lp, "abs", { inset: 0, borderRadius: "30px", background: "#2a2a2a", border: "1.5px solid rgba(255,255,255,.06)", padding: "54px 50px", fontSize: "38px", fontWeight: 550, lineHeight: 1.35, color: "#bdbdbd" },
    'Hi <span style="background:#3d3d3d;border-radius:8px;padding:0 8px;color:#e0e0e0">{first_name}</span>,<br><br>I noticed your company is growing and wanted to reach out about our solution…');
  const rp = W(body, rx, py, P, PH);
  el(rp, "abs m-paper", { inset: 0, borderRadius: "30px", padding: "54px 50px", fontSize: "40px", fontWeight: 600, lineHeight: 1.35 },
    'Saw you\'re <span style="position:relative;z-index:0;display:inline-block;white-space:nowrap">hiring 3 SDRs.<i class="hl" style="position:absolute;left:-6px;right:-6px;bottom:4px;height:22px;border-radius:6px;background:rgba(253,148,87,.55);z-index:-1;transform-origin:left;transform:scaleX(0)"></i></span><br><br>How long until a new rep books a first meeting?');
  const vs = W(body, WW / 2 - 42, py + PH / 2 - 42, 84, 84);
  el(vs, "abs center m-grey caps", { inset: 0, borderRadius: "50%", fontSize: "28px", fontWeight: 850 }, "vs");
  const svg = S.svg(body, WW, WH);
  svg.style.filter = "drop-shadow(0 0 10px rgba(255,90,31,.85))";
  const fr = S.path(svg, S.rr(rx - 8, py - 8, P + 16, PH + 16, 38), { color: "#FF5A1F", width: 6 });
  S.drawOn(fr, 1.5, 2.1, "io");
  const ok = W(body, rx + P - 44, py - 34, 84, 84);
  el(ok, "abs center", { inset: 0, borderRadius: "50%", background: "#fff", boxShadow: "0 0 0 5px #FF5A1F, 0 10px 24px rgba(0,0,0,.4)" }, icon("check", 48, "#FF5A1F", 3.4));
  const no = W(body, lx + P - 44, py - 34, 84, 84);
  el(no, "abs center", { inset: 0, borderRadius: "50%", background: "#3a3a3a", boxShadow: "0 0 0 5px #1c1c1c" }, icon("x", 42, "#d0d0d0", 3.2));
  A(win, { s: [[0.2, 0.93], [0.8, 1, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]], blur: [[0.2, 12], [0.6, 0, "out"]] });
  neo(lp, 0.6, { ang: 180, dist: 80 });
  neo(rp, 0.9, { ang: 0, dist: 80 });
  pop(vs, 1.1, { s0: 0.3 });
  pop(ok, 2.15, { s0: 0.1, ease: "back2" }); ripple(body, rx + P - 2, py + 8, 84, 2.2, "#FF5A1F");
  A(lp, { br: [[2.3, 1], [2.8, 0.55]], sat: [[2.3, 1], [2.8, 0]], s: [[2.3, 1], [2.8, 0.97]] });
  pop(no, 2.4, { s0: 0.1, ease: "back2" });
  const hl = rp.querySelector(".hl");
  F((t) => { hl.style.transform = `scaleX(${prog(t, 2.6, 3.0, "out").toFixed(3)})`; });
});

D("B03", {
  name: "Bento grid of results", cat: "box", loop: 6.4,
  use: "<b>Results and proof in one frame.</b> Tiles of different sizes and fills snap in, the numbers count, the chart draws, then one light sweep crosses the whole grid.",
  ref: { web: "Web · Dribbble dark bento grids" },
  recipe: ["#FF5A1F", "#ffffff", "#FD9457", "#2d2c2b"],
  fusion: "Each tile its own Rectangle + Merge (orange, white, light orange, glass). Counters: Text+ with a number modifier. Chart: Polyline Write-On over a gradient-filled Polygon. One NeoLightSweep over the merged grid.",
}, (S) => {
  const { el, W, A, pop, icon, count, sweep } = S;
  S.ground("warm", { grid: true });
  const tiles = [];
  const tile = (x, y, w, h, cls, delay) => { const t = W(null, x, y, w, h); const b = el(t, "abs clip " + cls, { inset: 0, borderRadius: "34px" }); pop(t, delay, { s0: 0.86, dur: 0.55 }); tiles.push([b, x]); return b; };
  const t1 = tile(250, 140, 680, 490, "m-ember", 0.3);
  el(t1, "abs center", { left: "44px", top: "40px", width: "76px", height: "76px", borderRadius: "22px", background: "rgba(255,255,255,.2)" }, icon("building", 42, "#fff", 2.2));
  const n1 = el(t1, "abs num", { left: "44px", bottom: "112px", fontSize: "184px", fontWeight: 900, letterSpacing: "-.045em", lineHeight: 1 }, "0");
  el(t1, "abs caps", { left: "50px", bottom: "58px", fontSize: "30px", fontWeight: 800, letterSpacing: ".14em", color: "rgba(255,255,255,.85)" }, "Accounts researched");
  const t2 = tile(950, 140, 720, 235, "m-paper", 0.42);
  const n2 = el(t2, "abs num", { left: "44px", top: "36px", fontSize: "120px", fontWeight: 900, color: "#FF5A1F", letterSpacing: "-.04em", lineHeight: 1 }, "0");
  el(t2, "abs caps", { left: "48px", bottom: "36px", fontSize: "28px", fontWeight: 800, letterSpacing: ".14em", color: "#1B0903" }, "Demos booked");
  el(t2, "abs center", { right: "40px", top: "40px", width: "96px", height: "96px", borderRadius: "28px", background: "#FFF0E6" }, icon("calendar", 52, "#FF5A1F", 2.2));
  const t3 = tile(950, 395, 350, 235, "m-peach", 0.54);
  const n3 = el(t3, "abs num", { left: "36px", top: "34px", fontSize: "96px", fontWeight: 900, letterSpacing: "-.04em", lineHeight: 1 }, "0");
  el(t3, "abs caps", { left: "40px", bottom: "34px", fontSize: "24px", fontWeight: 800, letterSpacing: ".14em" }, "B2B clients");
  const t4 = tile(1320, 395, 350, 235, "m-dark", 0.66);
  el(t4, "abs center", { left: 0, right: 0, top: "36px", height: "110px" }, icon("spark", 96, "#FF5A1F", 2.6));
  el(t4, "abs center caps", { left: 0, right: 0, bottom: "34px", fontSize: "24px", fontWeight: 800, letterSpacing: ".14em", color: "#bdbdbd" }, "Built with Claude");
  const t5 = tile(250, 650, 1420, 290, "m-dark", 0.78);
  el(t5, "abs caps", { left: "48px", top: "40px", fontSize: "28px", fontWeight: 800, letterSpacing: ".14em", color: "#bdbdbd" }, "Pipeline");
  const n5 = el(t5, "abs num", { left: "44px", top: "80px", fontSize: "84px", fontWeight: 900, letterSpacing: "-.03em", color: "#fff" }, "$0");
  const svg = S.svg(t5, 1420, 290);
  svg.innerHTML = `<defs><linearGradient id="b03a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF5A1F" stop-opacity=".45"/><stop offset="1" stop-color="#FF5A1F" stop-opacity="0"/></linearGradient></defs>
    <path class="area" d="M48 250 C 200 238, 300 196, 430 206 S 700 140, 860 150 S 1130 80, 1372 64 L1372 290 L48 290 Z" fill="url(#b03a)" opacity="0"/>
    <path class="line" d="M48 250 C 200 238, 300 196, 430 206 S 700 140, 860 150 S 1130 80, 1372 64" fill="none" stroke="#FF5A1F" stroke-width="6" stroke-linecap="round" style="filter:drop-shadow(0 0 10px rgba(255,90,31,.8))"/>`;
  S.drawOn(svg.querySelector(".line"), 1.2, 2.4, "io");
  S.fade(svg.querySelector(".area"), 1.8, 0.7);
  count(n1, 0.6, 2.0, 0, 3655);
  count(n2, 0.7, 1.9, 0, 58);
  count(n3, 0.8, 1.9, 0, 250, (v) => Math.round(v) + "+");
  count(n5, 1.2, 2.4, 0, 7.83, (v) => "$" + v.toFixed(2) + "M");
  tiles.forEach(([b, x]) => { S.addSweep(b); sweep(b, 2.6 + ((x - 250) / 1420) * 0.45, 0.8); });
});

D("B04", {
  name: "Chat that builds bubble by bubble", cat: "box", loop: 6.4,
  use: "<b>Conversations: DMs, replies, objections.</b> Typing dots, then each bubble pops from its corner. Orange is us, grey is them. On a light ground to break the dark run.",
  ref: { id: "I52", label: "Visual Inspo #52, #122 · the mock chat in 4 AI Tools (approved)" },
  recipe: ["#ffffff", "#FF5A1F", "#F1EAE5", "#1B0903"],
  fusion: "White Rectangle card on a cream Background. Bubbles: Rectangles with one small corner, pivot on that corner, back-ease Size. Typing: three Ellipses with offset sine Y.",
}, (S) => {
  const { el, W, A, F, icon, prog } = S;
  S.ground("cream", { grid: true });
  const X = 560, Y = 80, CW = 800, CH = 920;
  const card = W(null, X, Y, CW, CH);
  const c = el(card, "abs m-paper clip", { inset: 0, borderRadius: "48px", boxShadow: "0 40px 90px rgba(120,50,20,.2), 0 0 0 1.5px rgba(90,30,8,.05)" });
  const hd = el(c, "abs row", { left: 0, right: 0, top: 0, height: "150px", padding: "0 40px", gap: "24px", borderBottom: "1.5px solid #F1E7E1" });
  el(hd, "center m-peach", { width: "96px", height: "96px", borderRadius: "50%", fontSize: "36px", fontWeight: 850 }, "SL");
  el(hd, "col", { gap: "6px" }, '<b style="font-size:38px;font-weight:800;color:#1B0903">Sarah Lee</b><span style="font-size:26px;font-weight:550;color:#8c7f78">VP Sales · Northwind</span>');
  el(hd, "row", { marginLeft: "auto", gap: "10px", fontSize: "24px", fontWeight: 600, color: "#8c7f78" }, '<i style="width:14px;height:14px;border-radius:50%;background:#FF5A1F;display:block"></i>online');
  const bub = (side, y, text, t0) => {
    const b = el(c, "abs fx", Object.assign({ top: y + "px", maxWidth: "580px", transformOrigin: side === "r" ? "100% 100%" : "0% 100%" }, side === "r" ? { right: "36px" } : { left: "36px" }));
    el(b, "", { padding: "22px 30px", borderRadius: side === "r" ? "34px 34px 10px 34px" : "34px 34px 34px 10px", background: side === "r" ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#F1EAE5", color: side === "r" ? "#fff" : "#1B0903", fontSize: "34px", fontWeight: 550, lineHeight: 1.26, boxShadow: side === "r" ? "0 10px 24px rgba(255,90,31,.25)" : "none" }, text);
    A(b, { s: [[t0, 0.5], [t0 + 0.4, 1, "back"]], o: [[t0, 0], [t0 + 0.12, 1, "out"]] });
  };
  const typing = (y, t0, t1) => {
    const d = el(c, "abs row", { left: "36px", top: y + "px", gap: "10px", padding: "26px 30px", borderRadius: "34px 34px 34px 10px", background: "#F1EAE5" });
    const ds = [0, 1, 2].map(() => el(d, "", { width: "16px", height: "16px", borderRadius: "50%", background: "#b8a89f" }));
    F((t) => { const on = t > t0 && t < t1; d.style.opacity = on ? 1 : 0; ds.forEach((k, i) => { k.style.transform = `translateY(${(-7 * Math.max(0, Math.sin(t * 9 - i * 0.9))).toFixed(1)}px)`; }); });
  };
  bub("r", 190, "Saw Northwind is hiring 3 SDRs. How long until a new rep books a first meeting?", 0.6);
  typing(400, 1.15, 1.75); bub("l", 400, "Honestly, too long.", 1.75);
  typing(512, 2.0, 2.55); bub("l", 512, "Ramping new SDRs is our biggest problem this quarter.", 2.55);
  bub("r", 680, "What if the research was done before day one?", 3.3);
  const seen = el(c, "abs", { right: "44px", top: "830px", fontSize: "24px", fontWeight: 600, color: "#b3a59d" }, "Seen");
  F((t) => { seen.style.opacity = prog(t, 3.9, 4.2).toFixed(3); });
  A(card, { y: [[0.2, 80], [0.8, 0, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]], blur: [[0.2, 10], [0.6, 0, "out"]] });
});

D("B05", {
  name: "Tabbed box, steps 1–4", cat: "box", loop: 6.4,
  use: "<b>Walking through a process step by step</b> without leaving the frame. The orange tab moves along, the content inside swaps. One box can carry a whole section.",
  ref: { id: "I101", label: "Visual Inspo #100, #101 · Nate Herk's editor" },
  recipe: ["#2d2c2b", "#FF5A1F", "#ffffff", "#8C8C8C"],
  fusion: "Box + four tab Rectangles; active colour keyed per tab. Indicator bar: Transform X on an expo spline. Content: one Merge per step, crossfaded with a Dissolve or opacity keys.",
}, (S) => {
  const { el, W, A, F, neo, icon, prog, lerp, E } = S;
  S.ground("warm", { grid: true });
  const X = 330, Y = 270, BW = 1260, BH = 600;
  const steps = [["Define", "Who you sell to", "target"], ["Research", "Who is buying right now", "search"], ["Angle", "Why them, why now", "message"], ["Build", "Claude does the rest", "spark"]];
  const at = (t) => S.clamp(Math.floor((t - 0.8) / 1.1), 0, 3);
  const tabs = steps.map(([n], i) => {
    const w = W(null, X + 30 + i * 300, Y - 92, 280, 104);
    const b = el(w, "abs row caps", { inset: 0, borderRadius: "30px 30px 0 0", padding: "0 0 12px 26px", gap: "16px", fontSize: "30px", fontWeight: 800, letterSpacing: ".04em" });
    const nc = el(b, "center num", { width: "52px", height: "52px", borderRadius: "50%", fontSize: "26px", fontWeight: 850 }, String(i + 1));
    el(b, "", {}, n);
    neo(w, 0.25 + i * 0.08, { dist: 40, blur: 10 });
    return { b, nc };
  });
  const box = W(null, X, Y, BW, BH);
  el(box, "abs m-dark", { inset: 0, borderRadius: "36px", borderTopLeftRadius: "12px" });
  const ind = el(box, "abs", { top: "0px", height: "5px", width: "280px", borderRadius: "3px", background: "linear-gradient(90deg,#FD9457,#FF5A1F)", boxShadow: "0 0 16px rgba(255,90,31,.8)" });
  const pages = steps.map(([n, sub, ic], i) => {
    const g = W(box, 0, 0, BW, BH);
    const ring = el(g, "abs center", { left: "110px", top: "150px", width: "250px", height: "250px", borderRadius: "50%", border: "4px solid #FF5A1F", boxShadow: "0 0 40px rgba(255,90,31,.45), inset 0 0 30px rgba(255,90,31,.25)", background: "radial-gradient(closest-side, rgba(255,90,31,.14), transparent)" }, icon(ic, 120, "#fff", 2));
    el(g, "abs caps", { left: "440px", top: "170px", fontSize: "28px", fontWeight: 800, letterSpacing: ".24em", color: "#FD9457" }, `Step ${i + 1} of 4`);
    el(g, "abs", { left: "436px", top: "220px", fontSize: "96px", fontWeight: 850, letterSpacing: "-.025em", color: "#fff" }, n);
    el(g, "abs", { left: "440px", top: "340px", fontSize: "44px", fontWeight: 550, color: "#bdbdbd" }, sub);
    const a = 0.8 + i * 1.1;
    const last = i === 3;
    A(g, { o: last ? [[a, 0], [a + 0.25, 1, "out"]] : [[a, 0], [a + 0.25, 1, "out"], [a + 1.0, 1], [a + 1.1, 0, "in"]], x: [[a, 60], [a + 0.45, 0, "expo"]], blur: [[a, 12], [a + 0.35, 0, "out"]] });
    A(ring, { s: [[a, 0.7], [a + 0.5, 1, "back"]] });
    return g;
  });
  F((t) => {
    const k = t < 0.8 ? -1 : at(t);
    tabs.forEach(({ b, nc }, i) => {
      const on = i === k;
      b.style.background = on ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#2B2B2B";
      b.style.color = on ? "#fff" : "#9a9a9a";
      nc.style.background = on ? "#fff" : "#3d3d3d"; nc.style.color = on ? "#FF5A1F" : "#bdbdbd";
    });
    const kk = Math.max(0, k), p = prog(t, 0.8 + kk * 1.1, 0.8 + kk * 1.1 + 0.4, "expo");
    const from = Math.max(0, kk - 1);
    ind.style.left = (30 + lerp(from, kk, kk === 0 ? 1 : p) * 300).toFixed(1) + "px";
    ind.style.opacity = prog(t, 0.7, 0.9).toFixed(3);
  });
  A(box, { y: [[0.2, 60], [0.75, 0, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]] });
});

D("B06", {
  name: "Receipt that prints, then a stamp", cat: "box", loop: 6.4,
  use: "<b>Costs, stacks, what you're paying.</b> A receipt feeds out line by line, the total counts up, and a stamp slams it (REPLACED, CANCELLED, PAID). On a light-orange ground.",
  ref: { web: "Web · receipt print micro-animations" },
  recipe: ["#FD9457", "#ffffff", "#FF5A1F", "#1B0903"],
  fusion: "Receipt: white Rectangle with a zigzag bottom (Polygon mask), Transform Y stepped out of a slot Rectangle and masked at the slot line. Stamp: Text+ in a double outline, Size 2.4 → 1 in 4 frames + camera shake.",
}, (S) => {
  const { el, W, A, F, prog, lerp, count, hash } = S;
  S.ground("peach", { grid: true });
  const rw = el(null, "abs", { left: "660px", top: "86px", width: "600px", height: "900px" });
  el(null, "abs", { left: "590px", top: "66px", width: "740px", height: "40px", borderRadius: "20px", background: "#2A0E04", boxShadow: "inset 0 7px 12px rgba(0,0,0,.65), 0 2px 0 rgba(255,255,255,.4)" });
  const zig = "conic-gradient(from -45deg at bottom, #0000, #000 1deg 89deg, #0000 90deg) bottom/40px 20px repeat-x, linear-gradient(#000 0 0) top/100% calc(100% - 19px) no-repeat";
  const paper = el(rw, "abs", { inset: 0, background: "linear-gradient(180deg,#FFFFFF,#FBF7F4)", WebkitMask: zig, mask: zig, color: "#1B0903", padding: "56px 56px 0" });
  const sh = el(rw, "abs", { left: "10px", right: "10px", top: "30px", bottom: "10px", boxShadow: "0 30px 60px rgba(120,40,0,.28)", zIndex: -1 });
  paper.innerHTML = `
    <div style="text-align:center;font-size:50px;font-weight:900;letter-spacing:.1em">YOUR STACK</div>
    <div style="text-align:center;font-size:22px;font-weight:600;letter-spacing:.24em;color:#9b8b82;margin-top:10px">MONTHLY · SAMPLE</div>
    <div style="border-top:3px dashed #e3d6ce;margin:34px 0 26px"></div>
    ${[["Lead database", "$99"], ["Enrichment", "$149"], ["Sequencer", "$97"], ["Research time", "20 h"]].map(([a, b]) => `<div style="display:flex;justify-content:space-between;font-size:34px;font-weight:600;margin:0 0 22px"><span>${a}</span><span style="font-variant-numeric:tabular-nums">${b}</span></div>`).join("")}
    <div style="border-top:3px dashed #e3d6ce;margin:30px 0 26px"></div>
    <div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:40px;font-weight:900;letter-spacing:.08em;color:#FF5A1F">TOTAL</span><span class="tot num" style="font-size:78px;font-weight:900;letter-spacing:-.03em">$0</span></div>
    <div style="display:flex;gap:5px;justify-content:center;margin-top:46px;height:74px">${Array.from({ length: 38 }, (_, i) => `<i style="display:block;width:${[3, 6, 4, 8, 3][i % 5]}px;background:#1B0903"></i>`).join("")}</div>`;
  count(paper.querySelector(".tot"), 1.25, 2.0, 0, 345, (v) => "$" + Math.round(v));
  const st = el(rw, "abs center caps", { left: "96px", top: "606px", width: "420px", height: "150px", border: "8px double #FF5A1F", borderRadius: "18px", color: "#FF5A1F", fontSize: "72px", fontWeight: 900, letterSpacing: ".08em", opacity: 0 }, "Replaced");
  F((t) => {
    // header prints first: the paper feeds a little and is revealed top-down in printer steps
    const q = prog(t, 0.4, 2.2, "io"), stepped = Math.floor(q * 36) / 36;
    const ty = lerp(-24, 0, stepped);
    const rot = -2.2 * prog(t, 2.35, 2.8, "back");
    const drop = 22 * prog(t, 2.35, 2.8, "back");
    const shake = t > 3.0 && t < 3.3 ? (hash(Math.floor(t * 60)) - 0.5) * 16 * (1 - (t - 3.0) / 0.3) : 0;
    rw.style.transform = `translate(${shake.toFixed(1)}px, ${(ty + drop).toFixed(1)}px) rotate(${rot.toFixed(2)}deg)`;
    rw.style.clipPath = t > 2.3 ? "none" : `inset(${(-ty).toFixed(1)}px -200px ${(900 - 900 * stepped).toFixed(1)}px -200px)`;
    const s = t < 2.95 ? 0 : lerp(2.4, 1, prog(t, 2.95, 3.1, "in"));
    st.style.opacity = t < 2.95 ? 0 : Math.min(1, (t - 2.95) / 0.08).toFixed(3);
    st.style.transform = `rotate(-14deg) scale(${(s || 1).toFixed(3)})`;
    sh.style.opacity = prog(t, 2.2, 2.6).toFixed(3);
  });
});

D("B07", {
  name: "Leaderboard that re-sorts", cat: "box", loop: 6.4,
  use: "<b>Rankings and “which one wins”.</b> Rows land in one order, then the winner climbs to the top, turns orange and gets the crown. Movement tells the story.",
  ref: { web: "Web · Dribbble leaderboard shots" },
  recipe: ["#1c1c1c", "#FF5A1F", "#FD9457", "#8C8C8C"],
  fusion: "Box + four row Rectangles; each row's Transform Y keyed between slots (150 px apart). Winner: colour crossfade + crown Polygon pop. Bars: Rectangle Size X keyed.",
}, (S) => {
  const { el, W, A, F, pop, icon, prog, lerp } = S;
  S.ground("graphite", { grid: "dots" });
  const X = 440, Y = 110, BW = 1040, BH = 860;
  const box = W(null, X, Y, BW, BH);
  el(box, "abs m-dark", { inset: 0, borderRadius: "40px" });
  el(box, "abs", { left: "54px", top: "48px", fontSize: "46px", fontWeight: 800, letterSpacing: "-.01em" }, "Which tool wins?");
  el(box, "abs caps", { right: "54px", top: "62px", fontSize: "24px", fontWeight: 800, letterSpacing: ".2em", color: "#8C8C8C" }, "Ranked");
  el(box, "abs", { left: "54px", right: "54px", top: "130px", height: "1.5px", background: "rgba(255,255,255,.08)" });
  const data = [["Clay", "C", "#FD9457", 0.78, 0, 1], ["Railway", "R", "#8C8C8C", 0.62, 1, 2], ["Claude", "", "#FF5A1F", 0.55, 2, 0], ["Wispr Flow", "W", "#ffffff", 0.4, 3, 3]];
  const slot = (k) => 170 + k * 160;
  data.forEach(([name, letter, col, score, from, to], i) => {
    const r = W(box, 40, slot(from), BW - 80, 136);
    const bgc = el(r, "abs", { inset: 0, borderRadius: "30px", background: "rgba(255,255,255,.05)", border: "1.5px solid rgba(255,255,255,.07)" });
    const win = el(r, "abs m-ember", { inset: 0, borderRadius: "30px", opacity: 0 });
    const rank = el(r, "abs num", { left: "34px", top: "30px", fontSize: "66px", fontWeight: 900, letterSpacing: "-.04em", color: "rgba(255,255,255,.22)", width: "70px" }, "#" + (from + 1));
    el(r, "abs center", { left: "126px", top: "24px", width: "88px", height: "88px", borderRadius: "50%", background: col, color: "#1B0903", fontSize: "40px", fontWeight: 900, boxShadow: "0 8px 20px rgba(0,0,0,.35)" }, letter || icon("spark", 50, "#fff", 2.8));
    el(r, "abs", { left: "244px", top: "42px", fontSize: "44px", fontWeight: 750, whiteSpace: "nowrap" }, name);
    const tr = el(r, "abs", { right: "40px", top: "60px", width: "300px", height: "16px", borderRadius: "8px", background: "rgba(255,255,255,.08)" });
    const fill = el(tr, "abs", { left: 0, top: 0, bottom: 0, borderRadius: "8px", background: to === 0 ? "#fff" : col === "#ffffff" ? "#bdbdbd" : col });
    const t0 = 0.3 + i * 0.12;
    const dy = slot(to) - slot(from);
    A(r, { x: [[t0, 140], [t0 + 0.5, 0, "expo"]], o: [[t0, 0], [t0 + 0.2, 1, "out"]], blur: [[t0, 12], [t0 + 0.4, 0, "out"]], y: [[1.9, 0], [2.6, dy, "io"]], s: to === 0 ? [[1.9, 1], [2.25, 1.05], [2.6, 1, "out"]] : [[0, 1]] });
    if (to === 0) r.style.zIndex = 2;
    F((t) => {
      const w = to === 0 ? lerp(score, 0.96, prog(t, 2.5, 3.0, "out")) : score;
      fill.style.width = (300 * w * prog(t, t0 + 0.2, t0 + 1.0, "out")).toFixed(1) + "px";
      const k = t < 2.3 ? from : to;
      rank.textContent = "#" + (k + 1);
      if (to === 0) { win.style.opacity = prog(t, 2.35, 2.7).toFixed(3); rank.style.color = t > 2.4 ? "rgba(255,255,255,.55)" : "rgba(255,255,255,.22)"; }
    });
    if (to === 0) {
      const cr = W(r, 142, -40, 56, 56);
      el(cr, "abs center", { inset: 0 }, icon("crown", 56, "#FFE3D2", 2.4, "#FD9457"));
      pop(cr, 2.65, { s0: 0.1, ease: "back2" });
    }
  });
  A(box, { s: [[0.15, 0.95], [0.7, 1, "expo"]], o: [[0.15, 0], [0.4, 1, "out"]] });
});

D("B08", {
  name: "Quote box with a marker highlight", cat: "box", loop: 6.4,
  use: "<b>Quotes from articles, clients, or his own key line.</b> Cream card, a big orange quote mark drops in, words land one by one and a marker hits the key word.",
  ref: { id: "B6", label: "Best editor 6 · the highlighter marks already approved in Taking a Step Back" },
  recipe: ["#FFE5D4", "#FF5A1F", "#FD9457", "#1B0903"],
  fusion: "Cream Rectangle + DropShadow. Quote mark: Text+ “ at 360 pt, gradient fill. Words: Text+ with Follower (per-word delay). Marker: light-orange Rectangle behind the word, Size X 0 → 1.",
}, (S) => {
  const { el, W, A, F, neo, prog } = S;
  S.ground("warm", { grid: true });
  const X = 240, Y = 230, BW = 1440, BH = 610;
  const box = W(null, X, Y, BW, BH);
  el(box, "abs m-cream", { inset: 0, borderRadius: "44px" });
  const text = "Nobody reads your email. They read their *problem* in it.";
  const p = el(box, "abs", { left: "120px", right: "120px", top: "130px", fontSize: "80px", fontWeight: 750, lineHeight: 1.16, letterSpacing: "-.02em", color: "#1B0903" });
  text.split(" ").forEach((w, i) => {
    const key = w.startsWith("*");
    const clean = w.replace(/\*/g, "");
    const s = el(p, "fx", { display: "inline-block", marginRight: "22px", position: "relative", zIndex: 0, color: key ? "#1B0903" : "#1B0903" }, clean + (key ? '<i class="hl" style="position:absolute;left:-10px;right:-10px;bottom:6px;height:34px;border-radius:8px;background:rgba(253,148,87,.75);z-index:-1;transform-origin:left;transform:scaleX(0)"></i>' : ""));
    neo(s, 0.8 + i * 0.13, { dist: 36, blur: 10 });
  });
  const hl = p.querySelector(".hl");
  F((t) => { hl.style.transform = `scaleX(${prog(t, 2.45, 2.85, "out").toFixed(3)})`; });
  const tag = W(box, 120, BH - 130, 360, 64);
  el(tag, "abs row m-ember caps", { inset: 0, borderRadius: "32px", padding: "0 30px", fontSize: "26px", fontWeight: 800, letterSpacing: ".1em", whiteSpace: "nowrap" }, "— Name, Role");
  neo(tag, 2.9, { ang: 180, dist: 40, blur: 8 });
  const q = W(null, X + 40, Y - 190, 260, 300);
  el(q, "abs gtext", { left: 0, top: 0, fontSize: "380px", fontWeight: 900, lineHeight: 1 }, "“");
  A(q, { y: [[0.45, -80], [0.95, 0, "back"]], rz: [[0.45, -25], [0.95, 0, "back"]], o: [[0.45, 0], [0.6, 1, "out"]] });
  A(box, { y: [[0.2, 70], [0.75, 0, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]], blur: [[0.2, 10], [0.6, 0, "out"]] });
});
