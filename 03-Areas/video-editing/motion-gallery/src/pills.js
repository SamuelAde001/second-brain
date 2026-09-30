// PILLS — P01..P13. Every design: D(code, meta, (S) => build). Stage is 1920x1080. Sample copy only.

D("P01", {
  name: "Medallion pills", cat: "pill", loop: 6.2,
  use: "<b>A list beside the speaker.</b> 3–4 steps, each with its own icon. The medallion lands and spins in, then the pill grows out of it. Zigzag keeps it from reading like a table.",
  ref: { id: "I3", label: "Visual Inspo #3 · Andy Stauring's editor" },
  recipe: ["#3a3a3a", "#ffffff", "#FF5A1F", "#FD9457"],
  fusion: "Pill: Rectangle mask (corner 1.0) over a blurred A-roll copy + NeoBevel. Medallion: Ellipse + DropShadow, NeoGlow on the orange ring. Reveal: key the pill mask's Width from the medallion side.",
}, (S) => {
  const { el, W, A, neo, pop, icon, clip, sweep, float } = S;
  S.ground("aroll");
  const items = [["building", "FIND THE", "ACCOUNTS"], ["eye", "READ THE", "SIGNALS"], ["user", "PICK THE", "PERSON"], ["pen", "WRITE THE", "ANGLE"]];
  items.forEach(([ic, a, b], i) => {
    const left = i % 2 === 0, M = 140, H = 118, PW = 420;
    const g = W(null, left ? 1330 : 1385, 150 + i * 200, PW + M / 2, M);
    const pill = el(g, "abs m-dark clip", { left: (left ? M / 2 : 0) + "px", top: (M - H) / 2 + "px", width: PW + "px", height: H + "px", borderRadius: H / 2 + "px" });
    const tx = el(pill, "abs center caps", { inset: 0, padding: left ? "0 28px 0 96px" : "0 96px 0 28px", flexDirection: "column", fontSize: "34px", fontWeight: 800, lineHeight: 1.04, textAlign: "center", letterSpacing: "-.005em" }, `<span>${a}</span><span style="color:#FD9457">${b}</span>`);
    const med = W(g, left ? 0 : PW - M / 2, 0, M, M);
    el(med, "abs center m-paper", { inset: 0, borderRadius: "50%", boxShadow: "0 0 0 5px #FF5A1F, 0 0 36px rgba(255,90,31,.6), 0 18px 40px rgba(0,0,0,.45)" }, icon(ic, 62, "#FF5A1F", 2.2));
    const t0 = 0.35 + i * 0.45;
    pop(med, t0, { s0: 0.2, dur: 0.55, ease: "back2" });
    A(med, { rz: [[t0, left ? -120 : 120], [t0 + 0.6, 0, "expo"]] });
    clip(pill, left ? [0, PW, 0, 0] : [0, 0, 0, PW], [0, 0, 0, 0], t0 + 0.18, t0 + 0.78, H / 2, "expo");
    neo(tx, t0 + 0.32, { ang: left ? 180 : 0, dist: 60, blur: 12 });
    S.addSweep(pill); sweep(pill, t0 + 0.95, 0.9);
    float(g, 3, 1.4, i * 1.3);
  });
});

D("P02", {
  name: "Pill with a status tag", cat: "pill", loop: 6,
  use: "<b>Two claims set against each other.</b> The tag hanging off the pill says what kind of claim it is: short term vs long term, old vs new, theirs vs yours.",
  ref: { id: "I14", label: "Visual Inspo #14 · Andy Stauring's editor" },
  recipe: ["#ffffff", "#9E350F", "#3a3a3a", "#FD9457"],
  fusion: "Two Rectangle pills (corner 1.0), tag = smaller Rectangle merged on top, offset to the lower-left edge. Tag drop: Transform Y with a back-ease spline. Sonar: Ellipse outlines scaled + faded.",
}, (S) => {
  const { el, W, A, F, neo, icon, sweep, prog } = S;
  S.ground("warm", { grid: true });
  const rings = el(null, "abs", { left: "0", top: "0", width: "1920px", height: "1080px" });
  [360, 620, 880, 1140].forEach((d) => el(rings, "abs", { left: 960 - d / 2 + "px", top: 520 - d / 2 + "px", width: d + "px", height: d + "px", borderRadius: "50%", border: "1.5px solid rgba(255,140,90,.09)" }));
  const pulse = el(rings, "abs", { left: "960px", top: "520px", width: "10px", height: "10px", borderRadius: "50%", border: "2px solid rgba(255,120,70,.5)" });
  F((t) => { const q = ((t + 10) % 2.4) / 2.4, d = 300 + q * 1100; Object.assign(pulse.style, { width: d + "px", height: d + "px", left: 960 - d / 2 + "px", top: 520 - d / 2 + "px", opacity: ((1 - q) * 0.6).toFixed(3) }); });
  const tag = (x, y, cls, badge, txt) => {
    const w = W(null, x, y, null, 66);
    el(w, "row " + cls, { height: "66px", borderRadius: "33px", padding: "0 26px 0 10px", gap: "14px", fontSize: "25px", fontWeight: 800, letterSpacing: ".06em", whiteSpace: "nowrap" }, badge + txt);
    return w;
  };
  const a = W(null, 300, 560, 700, 130);
  el(a, "abs center m-deep clip caps", { inset: 0, borderRadius: "65px", fontSize: "60px", fontWeight: 850, letterSpacing: "-.01em" }, 'NOT A&nbsp;<span style="color:#fff">TOOL</span>');
  const ta = tag(344, 664, "m-grey", `<span class="center" style="width:46px;height:46px;border-radius:50%;background:#FF5A1F">${icon("alert", 30, "#fff", 3.2)}</span>`, "SHORT TERM");
  const b = W(null, 920, 300, 700, 130);
  const bp = el(b, "abs center m-paper clip caps", { inset: 0, borderRadius: "65px", fontSize: "60px", fontWeight: 850, letterSpacing: "-.01em" }, 'A&nbsp;<span style="color:#FF5A1F">SYSTEM</span>');
  const tb = tag(964, 404, "m-peach", `<span class="center" style="width:46px;height:46px;border-radius:50%;background:#fff">${icon("check", 30, "#FF5A1F", 3.4)}</span>`, "LONG TERM");
  neo(a, 0.3, { ang: 180, dist: 160, blur: 20 });
  A(ta, { y: [[0.8, -34], [1.25, 0, "back2"]], o: [[0.8, 0], [0.95, 1, "out"]] });
  neo(b, 1.3, { ang: 0, dist: 160, blur: 20 });
  A(tb, { y: [[1.8, -34], [2.25, 0, "back2"]], o: [[1.8, 0], [1.95, 1, "out"]] });
  const ab = ta.querySelector(".center");
  F((t) => { ab.style.transform = `scale(${(1 + 0.09 * Math.max(0, Math.sin(t * 5))).toFixed(3)})`; ab.style.boxShadow = `0 0 ${(10 + 14 * Math.max(0, Math.sin(t * 5))).toFixed(1)}px rgba(255,90,31,.8)`; });
  S.addSweep(bp); sweep(bp, 2.4, 1);
  A(a, { br: [[2.3, 1], [2.8, 0.72]] });
});

D("P03", {
  name: "Ghost-numeral chapter pill", cat: "pill", loop: 6,
  use: "<b>Chapter or step markers on the A-roll.</b> The big faded number rolls 00 → 01 like a counter, then the step name lands. Swap the number per chapter.",
  ref: { id: "I40", label: "Visual Inspo #40 and #58 · Andy Stauring's editor" },
  recipe: ["#591E0B", "#C44617", "#FD9457", "#ffffff"],
  fusion: "Rectangle (corner 0.3) with a deep-orange gradient + 1 px light-orange border. Numeral: Text+ at 25% opacity, masked by the pill; the roll is Text+ Y offset. Word reveal: NeoAnim.",
}, (S) => {
  const { el, W, A, F, neo, clip, sweep, prog } = S;
  S.ground("aroll");
  const X = 230, Y = 810, PW = 920, H = 150;
  const w = W(null, X, Y, PW, H);
  const p = el(w, "abs m-deep clip", { inset: 0, borderRadius: "36px", border: "1.5px solid rgba(253,148,87,.55)" });
  const reel = el(p, "abs col num", { left: "30px", top: "0px", fontSize: "190px", fontWeight: 900, letterSpacing: "-.06em", lineHeight: "190px", color: "rgba(255,196,160,.26)" }, "<span>00</span><span>01</span>");
  F((t) => { reel.style.transform = `translateY(${(-20 - 190 * prog(t, 0.75, 1.25, "back")).toFixed(1)}px)`; reel.style.opacity = prog(t, 0.45, 0.7); });
  const lab = W(p, 272, 28, 520, 30);
  el(lab, "abs caps", { fontSize: "24px", fontWeight: 750, letterSpacing: ".2em", color: "#FD9457", whiteSpace: "nowrap" }, "Chapter 1");
  const words = "Define the audience".split(" ");
  const line = el(p, "abs row", { left: "270px", top: "60px", gap: "16px", fontSize: "60px", fontWeight: 750, letterSpacing: "-.015em", whiteSpace: "nowrap" });
  words.forEach((wd, i) => { const s = el(line, "fx", { display: "inline-block" }, wd); neo(s, 0.85 + i * 0.09, { dist: 50, blur: 12 }); });
  const bar = el(p, "abs", { left: "272px", top: "130px", height: "6px", borderRadius: "3px", background: "linear-gradient(90deg,#FD9457,#FF5A1F)", boxShadow: "0 0 14px rgba(255,90,31,.7)" });
  F((t) => { bar.style.width = (170 * prog(t, 1.2, 1.7, "expo")).toFixed(1) + "px"; });
  clip(p, [0, PW, 0, 0], [0, 0, 0, 0], 0.3, 0.85, 36, "expo");
  neo(lab, 0.7, { dist: 30, blur: 8 });
  S.addSweep(p); sweep(p, 1.7, 1);
  F((t) => { reel.style.translate = `${(Math.sin(t * 0.9) * 6).toFixed(2)}px 0`; });
});

D("P04", {
  name: "Corner-badge pills", cat: "pill", loop: 6.2,
  use: "<b>Questions, warnings, confirmations.</b> The badge pops on the corner after the pill lands, with a ripple. ? for a question, ! for a problem, ✓ for proof.",
  ref: { id: "I11", label: "Visual Inspo #1, #11 · best editor 31" },
  recipe: ["#FFE5D4", "#2A2A2A", "#FF5A1F", "#ffffff"],
  fusion: "Cream Rectangle (corner 1.0) + DropShadow. Badge: Ellipse with a white stroke, pops on a back-ease scale. Ripple: Ellipse outline scaling 1 → 2.3 while fading.",
}, (S) => {
  const { el, W, A, pop, icon, tt, ripple, float } = S;
  S.ground("aroll");
  const specs = [
    { x: 110, y: 150, w: 650, txt: "WHY DO REPLIES *DIE*?", ic: "question", bg: "#2A2A2A", col: "#fff", ring: "rgba(255,255,255,.95)" },
    { x: 1160, y: 430, w: 680, txt: "YOU'RE BURNING *LEADS*", ic: "alert", bg: "#FF5A1F", col: "#fff", ring: "rgba(255,255,255,.95)" },
    { x: 700, y: 860, w: 540, txt: "SIGNAL *VERIFIED*", ic: "check", bg: "#fff", col: "#FF5A1F", ring: "#FF5A1F" },
  ];
  specs.forEach((s, i) => {
    const t0 = 0.3 + i * 0.95;
    const w = W(null, s.x, s.y, s.w, 118);
    el(w, "abs center m-cream caps", { inset: 0, borderRadius: "59px", fontSize: "42px", fontWeight: 850, letterSpacing: "-.01em", whiteSpace: "nowrap" }, `<span>${tt(s.txt, "#FF5A1F")}</span>`);
    const bw = W(w, s.w - 58, -30, 76, 76);
    el(bw, "abs center", { inset: 0, borderRadius: "50%", background: s.bg, boxShadow: `0 0 0 4px ${s.ring}, 0 10px 24px rgba(0,0,0,.35)` }, icon(s.ic, 44, s.col, 3.2));
    pop(w, t0, { s0: 0.82, dur: 0.5 });
    pop(bw, t0 + 0.32, { s0: 0, dur: 0.45, ease: "back2", blur: 0 });
    ripple(w, s.w - 20, 8, 76, t0 + 0.4, s.bg === "#fff" ? "#FF5A1F" : "rgba(255,255,255,.85)");
    float(w, 3, 1.3, i * 2);
  });
});

D("P05", {
  name: "Dynamic Island notification", cat: "pill", loop: 6,
  use: "<b>A result landing:</b> a reply, a booked call, money in. A black capsule at the top grows into the message, holds, and shrinks back, the way the iPhone does it.",
  ref: { web: "Web · Dribbble, Apple Dynamic Island shape-morph shots" },
  recipe: ["#050505", "#ffffff", "#FF5A1F", "#8C8C8C"],
  fusion: "One Rectangle: key Width, Height and Corner Radius together on a spring spline. Content in a separate Merge that fades in after the grow. Keep the capsule pure black.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, prog, lerp, E } = S;
  S.ground("aroll");
  const isl = el(null, "abs m-black clip", {});
  const dot = el(isl, "abs", { width: "16px", height: "16px", borderRadius: "50%", background: "#FF5A1F", boxShadow: "0 0 12px #FF5A1F", right: "26px", top: "27px" });
  const body = el(isl, "abs row", { left: "0", top: "0", width: "900px", height: "164px", padding: "0 34px 0 26px", gap: "26px" });
  const av = W(body, 26, 26, 112, 112);
  el(av, "abs center m-ember", { inset: 0, borderRadius: "50%", fontSize: "42px", fontWeight: 850 }, "SL");
  const col = el(body, "abs col", { left: "166px", top: "34px", gap: "10px" });
  el(col, "", { fontSize: "29px", fontWeight: 600, color: "#9d9d9d", whiteSpace: "nowrap" }, "Sarah Lee · Northwind");
  el(col, "", { fontSize: "46px", fontWeight: 750, color: "#fff", whiteSpace: "nowrap", letterSpacing: "-.01em" }, "“Honestly, too long.”");
  const ic = W(body, 900 - 34 - 84, 40, 84, 84);
  el(ic, "abs center", { inset: 0, borderRadius: "50%", background: "rgba(255,90,31,.16)", border: "2px solid rgba(255,90,31,.6)" }, icon("mail", 42, "#FF5A1F", 2.2));
  F((t) => {
    const grow = t < 0.9 ? 0 : t < 4.3 ? E.spring(Math.min(1, (t - 0.9) / 0.75)) : 1 - prog(t, 4.3, 4.8, "io");
    const w = lerp(230, 900, grow), h = lerp(70, 164, grow);
    const y = t < 5.1 ? lerp(-90, 56, prog(t, 0.2, 0.55, "out")) : lerp(56, -120, prog(t, 5.1, 5.5, "in"));
    Object.assign(isl.style, { width: w.toFixed(1) + "px", height: h.toFixed(1) + "px", left: (960 - w / 2).toFixed(1) + "px", top: y.toFixed(1) + "px", borderRadius: (h / 2).toFixed(1) + "px", boxShadow: `0 20px 60px rgba(0,0,0,.55), 0 0 ${(70 * grow).toFixed(0)}px rgba(255,90,31,${(0.28 * grow).toFixed(3)})` });
    dot.style.opacity = (1 - prog(t, 0.9, 1.05)) * (0.6 + 0.4 * Math.sin(t * 8)) + prog(t, 4.6, 4.8) * (0.6 + 0.4 * Math.sin(t * 8));
    body.style.opacity = (prog(t, 1.25, 1.55) * (1 - prog(t, 4.05, 4.3))).toFixed(3);
  });
  pop(av, 1.25, { s0: 0.4, dur: 0.5 });
  neo(col, 1.35, { ang: 180, dist: 40, blur: 10 });
  pop(ic, 1.55, { s0: 0.3, dur: 0.5 });
});

D("P06", {
  name: "Liquid-glass logo pill", cat: "pill", loop: 6,
  use: "<b>Tool names and logos over the A-roll.</b> Clear glass that bends the picture behind it, lands like a drop of water and catches a glint. A small link pill can follow.",
  ref: { id: "I29", label: "Web · 2026 liquid-glass trend · Visual Inspo #29" },
  recipe: ["rgba(255,255,255,.5)", "#ffffff", "#FF5A1F", "#FD9457"],
  fusion: "Copy of the A-roll, Transform size 1.12 about the pill centre + slight blur, masked by a Rectangle (corner 1.0). Rim: the mask's edge through NeoBevel. Glint: NeoLightSweep. Drop: Transform size with squash/stretch keys.",
}, (S) => {
  const { el, W, A, F, neo, icon, sweep } = S;
  S.ground("aroll", { push: false });
  const X = 640, Y = 790, PW = 640, H = 156;
  const w = W(null, X, Y, PW, H);
  el(w, "abs", { inset: 0, borderRadius: H / 2 + "px", boxShadow: "0 26px 60px rgba(0,0,0,.35)" });
  const lens = el(w, "abs clip", { inset: 0, borderRadius: H / 2 + "px" });
  el(lens, "abs", { left: -X + "px", top: -Y + "px", width: "1920px", height: "1080px", backgroundImage: `url(${(window.ASSETS || {}).aroll || ""})`, backgroundSize: "cover", backgroundPosition: "center", transformOrigin: `${X + PW / 2}px ${Y + H / 2}px`, transform: "scale(1.14)", filter: "blur(2.5px) saturate(1.35) brightness(1.1)" });
  el(lens, "abs", { inset: 0, background: "linear-gradient(180deg, rgba(255,255,255,.2), rgba(255,255,255,.04) 55%, rgba(255,255,255,.12))" });
  el(lens, "abs", { inset: 0, borderRadius: "inherit", boxShadow: "inset 0 2.5px 1px rgba(255,255,255,.8), inset 0 -2px 1px rgba(255,255,255,.3), inset 0 -20px 30px rgba(0,0,0,.14), inset 0 14px 26px rgba(255,255,255,.16), inset 3px 0 6px rgba(255,255,255,.2)" });
  const spec = el(lens, "abs", { left: "56px", top: "10px", width: "300px", height: "44px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,255,255,.6), rgba(255,255,255,0))" });
  F((t) => { spec.style.transform = `translateX(${(Math.sin(t * 0.8) * 26).toFixed(1)}px)`; });
  const ct = el(lens, "abs row", { inset: 0, justifyContent: "center", gap: "26px" });
  const ci = el(ct, "center", { width: "92px", height: "92px", borderRadius: "50%", background: "linear-gradient(180deg,#FF8750,#FF5A1F)", boxShadow: "inset 0 2px 0 rgba(255,230,210,.6), 0 8px 20px rgba(160,40,0,.35)" }, icon("spark", 54, "#fff", 2.8));
  el(ct, "tshadow", { fontSize: "74px", fontWeight: 750, letterSpacing: "-.02em", color: "#fff" }, "Claude");
  S.addSweep(lens, "hard"); sweep(lens, 1.35, 0.9);
  A(w, { s: [[0.3, 0.22], [0.8, 1, "back"]], sx: [[0.3, 0.6], [0.55, 1.1], [0.8, 0.96], [1.0, 1]], sy: [[0.3, 1.35], [0.55, 0.88], [0.8, 1.04], [1.0, 1]], o: [[0.3, 0], [0.4, 1, "out"]] });
  neo(ct, 0.62, { dist: 24, blur: 10 });
  const lk = W(null, X + PW - 330, Y + H + 18, 330, 54);
  el(lk, "abs row m-glass", { inset: 0, borderRadius: "27px", gap: "10px", padding: "0 20px", fontSize: "24px", fontWeight: 650, whiteSpace: "nowrap" }, icon("link", 26, "#FD9457", 2.4) + "Link in description");
  neo(lk, 1.8, { dist: 30, blur: 8 });
  A(ci, { rz: [[0.6, -90], [1.2, 0, "expo"]] });
});

D("P07", {
  name: "Border-beam pill", cat: "pill", loop: 6,
  use: "<b>Naming a system or a key idea.</b> A dark pill with a comet of orange light running round its edge the whole time it's on screen. It stays alive while he talks.",
  ref: { id: "I113", label: "Visual Inspo #113 · web border-beam trend" },
  recipe: ["#111111", "#FF5A1F", "#FD9457", "#3a3a3a"],
  fusion: "Pill Rectangle; beam = a thin outline (Rectangle with Border Width) masked by a rotating Triangle/Wedge mask, then NeoGlow. Rotate the wedge 360° over ~2.4 s, linear.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, prog } = S;
  S.ground("graphite", { grid: "dots" });
  const halo = el(null, "abs", { left: "460px", top: "300px", width: "1000px", height: "480px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,90,31,.2), transparent)" });
  F((t) => { halo.style.opacity = (0.65 + 0.35 * Math.sin(t * 1.7)) * prog(t, 0.4, 1.0); });
  const X = 490, Y = 440, PW = 940, H = 176;
  const w = W(null, X, Y, PW, H);
  const mask = { WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)", WebkitMaskComposite: "xor", mask: "linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0)" };
  const gl = el(w, "abs", Object.assign({ inset: "-6px", borderRadius: H / 2 + 6 + "px", padding: "7px", filter: "blur(10px)" }, mask));
  el(w, "abs", { inset: 0, borderRadius: H / 2 + "px", background: "linear-gradient(180deg,#1E1E1E,#0F0F0F)", border: "1.5px solid rgba(255,255,255,.1)", boxShadow: "inset 0 1.5px 0 rgba(255,255,255,.08), 0 30px 70px rgba(0,0,0,.6)" });
  const bm = el(w, "abs", Object.assign({ inset: "-2px", borderRadius: H / 2 + 2 + "px", padding: "3.5px" }, mask));
  F((t) => {
    const a = (((t - 0.6) / 2.4) * 360).toFixed(1);
    const g = `conic-gradient(from ${a}deg at 50% 50%, rgba(255,90,31,0) 0deg, rgba(255,90,31,0) 245deg, rgba(253,148,87,.25) 290deg, #FD9457 330deg, #FF5A1F 350deg, #fff 357deg, rgba(255,90,31,0) 360deg)`;
    bm.style.background = g; gl.style.background = g;
    const o = prog(t, 0.6, 0.95).toFixed(3); bm.style.opacity = o; gl.style.opacity = o;
  });
  const ic = W(w, 28, 28, 120, 120);
  el(ic, "abs center m-ember", { inset: 0, borderRadius: "50%" }, icon("bolt", 62, "#fff", 2.3));
  const tx = el(w, "abs row caps", { left: "178px", top: "0", height: H + "px", gap: "20px", fontSize: "80px", fontWeight: 850, letterSpacing: "-.015em", whiteSpace: "nowrap" });
  const w1 = el(tx, "fx", { display: "inline-block" }, "Signal");
  const w2 = el(tx, "fx gtext", { display: "inline-block" }, "Engine");
  const tg = W(null, 960 - 170, Y + H + 36, 340, 60);
  el(tg, "abs row m-grey caps", { inset: 0, borderRadius: "30px", justifyContent: "center", gap: "12px", fontSize: "24px", fontWeight: 750, letterSpacing: ".08em", color: "#d6d6d6" }, icon("clock", 26, "#FD9457", 2.4) + "Runs daily · 7:00");
  neo(w, 0.3, { dist: 50, s0: 0.96 });
  pop(ic, 0.7, { s0: 0.3 }); A(ic, { rz: [[0.7, -150], [1.3, 0, "expo"]] });
  neo(w1, 0.85, { dist: 50 }); neo(w2, 0.95, { dist: 50 });
  neo(tg, 1.6, { dist: 30, blur: 8 });
});

D("P08", {
  name: "CAN / CANNOT verdict pair", cat: "pill", loop: 6,
  use: "<b>Yes/no, allowed/not, works/doesn't.</b> A header pill names the thing, two verdicts split out from under it, and the wrong one shakes.",
  ref: { id: "I98", label: "Visual Inspo #98 · Nate Herk's editor" },
  recipe: ["#ffffff", "#9E350F", "#FF5A1F", "#2A2A2A"],
  fusion: "Header pill + two pills; connectors are Polylines with Write-On. Split: Transform X from the centre on an expo spline. Shake: 5 X keys over 9 frames.",
}, (S) => {
  const { el, W, A, neo, pop, icon } = S;
  S.ground("aroll");
  const svg = S.svg();
  const hp = W(null, 960 - 175, 640, 350, 86);
  el(hp, "abs row m-dark caps", { inset: 0, borderRadius: "43px", justifyContent: "center", gap: "14px", fontSize: "34px", fontWeight: 800, letterSpacing: ".03em" }, icon("spark", 40, "#FF5A1F", 2.6) + "Claude");
  const c1 = S.path(svg, "M960 728 C 960 780, 700 766, 700 812", { color: "rgba(255,255,255,.75)", width: 3 });
  const c2 = S.path(svg, "M960 728 C 960 780, 1220 766, 1220 812", { color: "rgba(255,255,255,.75)", width: 3 });
  const L = W(null, 700 - 195, 812, 390, 128);
  const Lb = el(L, "abs row m-paper caps", { inset: 0, borderRadius: "64px", gap: "18px", justifyContent: "center", fontSize: "60px", fontWeight: 850, color: "#FF5A1F" });
  const Li = el(Lb, "center fx", { width: "78px", height: "78px", borderRadius: "50%", background: "#FF5A1F" }, icon("check", 46, "#fff", 3.4));
  el(Lb, "", {}, "Can");
  const R = W(null, 1220 - 235, 812, 470, 128);
  const Rb = el(R, "abs row m-deep caps", { inset: 0, borderRadius: "64px", gap: "18px", justifyContent: "center", fontSize: "60px", fontWeight: 850, color: "#FFD2B8" });
  const Ri = el(Rb, "center fx", { width: "78px", height: "78px", borderRadius: "50%", background: "rgba(255,210,184,.14)", border: "2.5px solid rgba(255,210,184,.55)" }, icon("x", 40, "#FFD2B8", 3.4));
  el(Rb, "", {}, "Cannot");
  neo(hp, 0.3, { ang: 90, dist: 50 });
  S.drawOn(c1, 0.75, 1.1, "out"); S.drawOn(c2, 0.75, 1.1, "out");
  A(L, { x: [[0.9, 260], [1.45, 0, "expo"]], s: [[0.9, 0.6], [1.45, 1, "expo"]], o: [[0.9, 0], [1.05, 1, "out"]], blur: [[0.9, 14], [1.3, 0, "out"]] });
  A(R, { x: [[0.95, -260], [1.5, 0, "expo"], [2.3, 0], [2.36, -13, "lin"], [2.44, 13, "lin"], [2.52, -9, "lin"], [2.6, 6, "lin"], [2.68, 0, "lin"]], s: [[0.95, 0.6], [1.5, 1, "expo"]], o: [[0.95, 0], [1.1, 1, "out"]], blur: [[0.95, 14], [1.35, 0, "out"]], br: [[2.3, 1], [2.9, 0.8]] });
  pop(Li, 1.35, { s0: 0.2, ease: "back2" }); pop(Ri, 1.45, { s0: 0.2, ease: "back2" });
});

D("P09", {
  name: "Stat pill with a segment bar", cat: "pill", loop: 6,
  use: "<b>One number that matters</b>, counted up live, with segments that light as it climbs. Sits low on the A-roll so he stays in frame.",
  ref: { id: "I81", label: "Visual Inspo #81 · best editor 44" },
  recipe: ["#2d2c2b", "#FD9457", "#FF5A1F", "#ffffff"],
  fusion: "Glass Rectangle (corner 0.35). Counter: Text+ with a number modifier. Segments: one small Rectangle duplicated 28× (Duplicate tool), colour keyed per copy with a time offset.",
}, (S) => {
  const { el, W, F, neo, pop, icon, count, prog, sweep } = S;
  S.ground("aroll");
  const X = 520, Y = 760, PW = 880, H = 206;
  const w = W(null, X, Y, PW, H);
  const card = el(w, "abs m-dark clip", { inset: 0, borderRadius: "48px" });
  const ic = W(card, 34, 32, 72, 72);
  el(ic, "abs center m-ember", { inset: 0, borderRadius: "50%" }, icon("users", 40, "#fff", 2.3));
  el(card, "abs caps", { left: "126px", top: "36px", fontSize: "25px", fontWeight: 700, letterSpacing: ".16em", color: "#bdbdbd", whiteSpace: "nowrap" }, "Accounts researched");
  const vt = el(card, "abs num", { left: "124px", top: "62px", fontSize: "76px", fontWeight: 850, color: "#FD9457", letterSpacing: "-.02em" }, "0");
  const live = W(card, PW - 190, 38, 154, 58);
  el(live, "abs row m-grey caps", { inset: 0, borderRadius: "29px", justifyContent: "center", gap: "12px", fontSize: "24px", fontWeight: 800, letterSpacing: ".1em" }, '<i style="width:14px;height:14px;border-radius:50%;background:#FF5A1F;box-shadow:0 0 12px #FF5A1F;display:block"></i>Live');
  const N = 28, gap = 8, tw = (PW - 68 - gap * (N - 1)) / N;
  const ticks = [];
  for (let i = 0; i < N; i++) ticks.push(el(card, "abs", { left: 34 + i * (tw + gap) + "px", top: "156px", width: tw + "px", height: "26px", borderRadius: "7px", background: "#3a3a3a" }));
  F((t) => {
    const lit = prog(t, 0.8, 2.4, "out") * N * 0.75;
    ticks.forEach((k, i) => {
      const on = i < lit;
      k.style.background = on ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#3a3a3a";
      k.style.boxShadow = on ? "0 0 12px rgba(255,90,31,.6)" : "none";
      k.style.transform = `scaleY(${on ? (1 + 0.35 * Math.max(0, 1 - (lit - i) * 0.6)).toFixed(3) : 1})`;
    });
  });
  count(vt, 0.8, 2.4, 0, 3655);
  neo(w, 0.3, { dist: 70, s0: 0.97 });
  pop(ic, 0.6, { s0: 0.3 });
  neo(live, 0.9, { ang: 0, dist: 30, blur: 8 });
  S.addSweep(card); sweep(card, 2.6, 1);
  F((t) => { live.firstChild.firstChild.style.opacity = (0.55 + 0.45 * Math.sin(t * 6)).toFixed(3); });
});

D("P10", {
  name: "Search pill that types", cat: "pill", loop: 6.4,
  use: "<b>“I searched for…” moments.</b> A white search bar on a light ground, the query types itself, the button presses and results drop down.",
  ref: { id: "I32", label: "Visual Inspo #32 · Andy Stauring's editor" },
  recipe: ["#ffffff", "#FFE9DC", "#FF5A1F", "#1B0903"],
  fusion: "White Rectangle (corner 1.0) + soft DropShadow on a cream Background. Text+ with a Write-On range for typing; caret = small Rectangle blinking. Results: Rectangle revealed by its own mask.",
}, (S) => {
  const { el, W, A, neo, icon, typeText, clip } = S;
  S.ground("cream", { grid: true });
  const X = 410, Y = 300, PW = 1100, H = 136;
  const w = W(null, X, Y, PW, H);
  el(w, "abs m-paper", { inset: 0, borderRadius: H / 2 + "px", boxShadow: "0 30px 70px rgba(120,50,20,.18), inset 0 -3px 0 rgba(27,9,3,.05), 0 0 0 1.5px rgba(90,30,8,.06)" });
  const row = el(w, "abs row", { inset: 0, padding: "0 18px 0 46px", gap: "24px" });
  row.innerHTML = icon("search", 52, "#9a8f89", 2.4);
  const tx = el(row, "", { fontSize: "46px", fontWeight: 550, color: "#1B0903", whiteSpace: "nowrap", letterSpacing: "-.01em" }, "");
  const caret = el(row, "", { width: "4px", height: "58px", background: "#FF5A1F", borderRadius: "2px", marginLeft: "-18px" });
  const btn = W(w, PW - 18 - 236, 20, 236, 96);
  el(btn, "abs center m-ember caps", { inset: 0, borderRadius: "48px", fontSize: "32px", fontWeight: 800, letterSpacing: ".02em" }, "Search");
  typeText(tx, 0.9, 2.5, "who is hiring SDRs this week", caret);
  neo(w, 0.3, { dist: 60, s0: 0.97 });
  A(btn, { s: [[2.7, 1], [2.8, 0.92, "out"], [3.0, 1, "back"]] });
  const res = W(null, X, Y + H + 22, PW, 372);
  const rc = el(res, "abs m-paper", { inset: 0, borderRadius: "36px", boxShadow: "0 30px 70px rgba(120,50,20,.16), 0 0 0 1.5px rgba(90,30,8,.06)" });
  const rows = [["building", "Northwind", "Hiring 3 SDRs"], ["user", "Brightpath", "New VP of Sales"], ["dollar", "Kestrel", "Raised a Series B"]];
  rows.forEach(([ic, n, m], i) => {
    const r = W(rc, 20, 20 + i * 112, PW - 40, 100);
    el(r, "abs row", { inset: 0, borderRadius: "24px", padding: "0 30px 0 22px", gap: "24px", background: i === 0 ? "#FFF0E6" : "transparent" },
      `<span class="center" style="width:64px;height:64px;border-radius:18px;background:${i === 0 ? "#FF5A1F" : "#F5ECE6"}">${icon(ic, 34, i === 0 ? "#fff" : "#FF5A1F", 2.3)}</span>` +
      `<span style="font-size:40px;font-weight:750;color:#1B0903">${n}</span><span style="margin-left:auto;font-size:32px;font-weight:600;color:${i === 0 ? "#FF5A1F" : "#8c7f78"}">${m}</span>`);
    neo(r, 3.15 + i * 0.12, { dist: 30, blur: 8 });
  });
  clip(rc, [0, 0, 372, 0], [0, 0, 0, 0], 2.95, 3.5, 36, "expo");
});

D("P11", {
  name: "Flow chips that break", cat: "pill", loop: 6,
  use: "<b>A process and the step where it fails.</b> Three chips, arrows draw between them, a light pulse runs the flow and stops dead at the warning; the goal dims.",
  ref: { id: "B35", label: "Best editor 35 · Nate Herk video" },
  recipe: ["#2d2c2b", "#FF5A1F", "#ffffff", "#FD9457"],
  fusion: "Three pills + Polyline arrows with Write-On. Pulse: small Ellipse + NeoGlow on a Path modifier along the arrow. Warning: Rectangle rotated 45° with a Text+ '!'.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, prog, lerp } = S;
  S.ground("aroll");
  const svg = S.svg();
  const Y = 850, H = 106;
  const chips = [[150, "building", "Find account", "m-dark"], [750, "mail", "Write email", "m-dark"], [1350, "calendar", "Book call", "m-ember"]];
  const nodes = chips.map(([x, ic, t, cls], i) => {
    const w = W(null, x, Y, 420, H);
    el(w, "abs row caps " + cls, { inset: 0, borderRadius: H / 2 + "px", gap: "20px", padding: "0 28px 0 20px", fontSize: "38px", fontWeight: 800, letterSpacing: "-.005em", whiteSpace: "nowrap" },
      `<span class="center" style="width:68px;height:68px;border-radius:50%;background:${cls === "m-ember" ? "rgba(255,255,255,.22)" : "rgba(255,255,255,.1)"}">${icon(ic, 36, cls === "m-ember" ? "#fff" : "#FD9457", 2.3)}</span>${t}`);
    neo(w, 0.3 + i * 0.6, { dist: 60 });
    return w;
  });
  const cy = Y + H / 2;
  const a1 = S.path(svg, `M584 ${cy} L734 ${cy}`, { color: "rgba(255,255,255,.8)", width: 4 });
  const h1 = S.path(svg, `M718 ${cy - 14} L736 ${cy} L718 ${cy + 14}`, { color: "rgba(255,255,255,.8)", width: 4 });
  const a2 = S.path(svg, `M1184 ${cy} L1334 ${cy}`, { color: "rgba(255,255,255,.8)", width: 4 });
  const h2 = S.path(svg, `M1318 ${cy - 14} L1336 ${cy} L1318 ${cy + 14}`, { color: "rgba(255,255,255,.8)", width: 4 });
  S.drawOn(a1, 0.7, 0.98, "out"); S.drawOn(h1, 0.95, 1.05, "out"); S.drawOn(a2, 1.3, 1.58, "out"); S.drawOn(h2, 1.55, 1.65, "out");
  const dot = el(null, "abs", { width: "22px", height: "22px", borderRadius: "50%", background: "#fff", boxShadow: "0 0 16px #fff, 0 0 30px #FF5A1F" });
  F((t) => {
    let x = -100, o = 0;
    if (t > 2.0 && t < 2.4) { x = lerp(584, 734, prog(t, 2.0, 2.4, "io")); o = 1; }
    else if (t >= 2.5 && t < 2.95) { x = lerp(1184, 1259, prog(t, 2.5, 2.75, "out")); o = 1 - prog(t, 2.75, 2.95); }
    Object.assign(dot.style, { left: x - 11 + "px", top: cy - 11 + "px", opacity: o.toFixed(3) });
  });
  const al = W(null, 1259 - 38, cy - 38, 76, 76);
  el(al, "abs center", { inset: "6px", borderRadius: "14px", transform: "rotate(45deg)", background: "linear-gradient(180deg,#FF8750,#FF5A1F)", boxShadow: "0 0 0 4px rgba(255,255,255,.95), 0 0 30px rgba(255,90,31,.8)" });
  el(al, "abs center", { inset: 0 }, icon("alert", 40, "#fff", 3.6));
  pop(al, 2.72, { s0: 0.1, ease: "back2", dur: 0.45 });
  A(al, { rz: [[2.72, 0], [2.95, 0], [3.0, -10, "lin"], [3.08, 10, "lin"], [3.16, -6, "lin"], [3.24, 0, "lin"]] });
  A(nodes[2], { br: [[2.85, 1], [3.3, 0.5]], sat: [[2.85, 1], [3.3, 0.25]] });
});

D("P12", {
  name: "Toggle switch", cat: "pill", loop: 6,
  use: "<b>Turning something on:</b> autopilot, a system, a new habit. Full orange ground for a hard pattern break; the knob slides, the track goes dark, sparks fly.",
  ref: { web: "Web · iOS toggle micro-interactions" },
  recipe: ["#FF5A1F", "#ffffff", "#1B0903", "#FD9457"],
  fusion: "Orange Background. Track: Rectangle (corner 1.0); knob: Ellipse + DropShadow; key knob X on a spring, squash on Size X mid-move. Track colour crossfades to dark. Sparks: pEmitter burst or 8 Ellipses.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, prog, lerp, E, burst, ripple } = S;
  S.ground("ember");
  const tt = W(null, 0, 236, 1920, 120);
  el(tt, "abs center caps", { inset: 0, fontSize: "112px", fontWeight: 900, letterSpacing: ".01em", color: "#fff", textShadow: "0 8px 36px rgba(120,30,0,.35)" }, "Autopilot");
  const X = 960 - 240, Y = 420, TW = 480, TH = 236;
  const tg = W(null, X, Y, TW, TH);
  el(tg, "abs", { inset: 0, borderRadius: TH / 2 + "px", background: "rgba(90,20,0,.26)", boxShadow: "inset 0 8px 20px rgba(80,15,0,.45), inset 0 -2px 0 rgba(255,255,255,.28)" });
  const on = el(tg, "abs", { inset: 0, borderRadius: TH / 2 + "px", background: "linear-gradient(180deg,#2A0E05,#140602)", boxShadow: "inset 0 5px 16px rgba(0,0,0,.7), 0 0 0 4px rgba(255,255,255,.22), 0 0 50px rgba(120,30,0,.4)" });
  const kn = el(tg, "abs center", { top: "22px", width: "192px", height: "192px", borderRadius: "96px", background: "linear-gradient(180deg,#FFFFFF,#F1EBE7)", boxShadow: "0 14px 30px rgba(80,15,0,.45), inset 0 -5px 0 rgba(0,0,0,.06)" });
  const off = el(kn, "abs center", { inset: 0 }, icon("bolt", 92, "#c9bdb6", 2.2));
  const lit = el(kn, "abs center", { inset: 0 }, icon("bolt", 92, "#FF5A1F", 2.4, "rgba(255,90,31,.18)"));
  F((t) => {
    const q = Math.min(1, Math.max(0, (t - 1.6) / 0.55));
    const x = lerp(22, TW - 22 - 192, E.spring(q));
    const squash = Math.sin(Math.PI * Math.min(1, q * 1.6)) * 0.28;
    Object.assign(kn.style, { left: x.toFixed(1) + "px", width: (192 * (1 + squash)).toFixed(1) + "px", marginLeft: (-96 * squash).toFixed(1) + "px" });
    on.style.opacity = prog(t, 1.62, 1.95).toFixed(3);
    lit.style.opacity = prog(t, 1.7, 1.9).toFixed(3); off.style.opacity = (1 - prog(t, 1.7, 1.9)).toFixed(3);
  });
  burst(null, X + TW - 22 - 96, Y + TH / 2, 1.95, 12, ["#fff", "#FFD2B8", "#1B0903"], 190);
  ripple(null, X + TW - 22 - 96, Y + TH / 2, 200, 1.95, "rgba(255,255,255,.9)", 0.8);
  const st = W(null, 0, 700, 1920, 80);
  const reel = el(st, "abs", { left: "0", top: "0", width: "1920px", height: "80px", overflow: "hidden" });
  const col = el(reel, "abs col caps", { left: "0", width: "1920px", top: "0", fontSize: "56px", fontWeight: 850, letterSpacing: ".12em", textAlign: "center", lineHeight: "80px" }, '<span style="color:#5a1a05">Off</span><span style="color:#fff">On</span>');
  F((t) => { col.style.transform = `translateY(${(-80 * prog(t, 1.75, 2.1, "back")).toFixed(1)}px)`; });
  neo(tt, 0.3, { dist: 60 });
  pop(tg, 0.65, { s0: 0.7 });
  neo(st, 0.95, { dist: 30, blur: 8 });
});

D("P13", {
  name: "Pill with a header tab", cat: "pill", loop: 6,
  use: "<b>Defining a term.</b> The orange tab names it (SIGNAL, MOAT, ICP); the white pill unrolls from under it with the meaning, and a marker swipes the key word.",
  ref: { id: "I72", label: "Visual Inspo #72 and #47 · Andy Stauring's editor" },
  recipe: ["#ffffff", "#FF5A1F", "#FD9457", "#1B0903"],
  fusion: "White Rectangle (corner 1.0) revealed by its mask Width from the centre; tab = orange Rectangle merged above it. Marker: light-orange Rectangle behind the word, Size X 0 → 1.",
}, (S) => {
  const { el, W, F, neo, pop, icon, clip, sweep, prog } = S;
  S.ground("aroll");
  const X = 320, Y = 830, PW = 1280, H = 136;
  const w = W(null, X, Y, PW, H);
  const m = el(w, "abs center m-paper clip caps", { inset: 0, borderRadius: H / 2 + "px", fontSize: "54px", fontWeight: 850, letterSpacing: "-.012em", whiteSpace: "nowrap" });
  const inner = el(m, "fx", { display: "inline-block" }, 'A reason to reach out <span style="position:relative;z-index:0;color:#FF5A1F">today<i class="hl" style="position:absolute;left:-8px;right:-8px;bottom:4px;height:20px;border-radius:6px;background:rgba(253,148,87,.5);z-index:-1;transform-origin:left;transform:scaleX(0)"></i></span>');
  const tab = W(null, 960 - 125, Y - 40, 250, 80);
  el(tab, "abs row m-ember caps", { inset: 0, borderRadius: "40px", justifyContent: "center", gap: "12px", fontSize: "36px", fontWeight: 850, letterSpacing: ".03em" }, icon("bolt", 34, "#fff", 2.4) + "Signal");
  pop(tab, 0.3, { s0: 0.3, ease: "back2" });
  clip(m, [0, PW / 2, 0, PW / 2], [0, 0, 0, 0], 0.62, 1.15, H / 2, "expo");
  neo(inner, 0.85, { dist: 34, blur: 10 });
  const hl = inner.querySelector(".hl");
  F((t) => { hl.style.transform = `scaleX(${prog(t, 1.6, 1.95, "out").toFixed(3)})`; });
  S.addSweep(m); sweep(m, 2.2, 1);
});
