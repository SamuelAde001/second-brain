// CARDS — C01..C08. Single-subject tiles: an option, a metric, a product, a person, a milestone.

D("C01", {
  name: "Glass pair with number badges", cat: "card", loop: 6.2,
  use: "<b>Two options, two parts of an idea.</b> Flat glass cards slide up with Neo Anim, the number badges pop, the icons draw themselves. No rotation.",
  ref: { id: "I6", label: "Visual Inspo #6 · Andy Stauring's editor" },
  recipe: ["rgba(255,255,255,.22)", "#FF5A1F", "#FD9457", "#ffffff"],
  fusion: "Each card: Rectangle (corner 0.3), glass = blurred background copy masked by the card + NeoBevel, orange underglow Background masked by the card. Neo Anim slide up. Icon: Polylines with Write-On.",
}, (S) => {
  const { el, W, A, F, pop, icon } = S;
  S.ground("bgo");
  const defs = S.svg(null, 1, 1);
  defs.innerHTML = `<defs><linearGradient id="c01g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD2B8"/><stop offset=".55" stop-color="#FD9457"/><stop offset="1" stop-color="#FF5A1F"/></linearGradient></defs>`;
  const persp = el(null, "abs", { inset: 0, perspective: "1800px", perspectiveOrigin: "50% 45%" });
  [[380, 16, -1.5, 1, "target", "FIND WHO'S", "BUYING"], [1020, -16, 1.5, 2, "clock", "SAY WHY", "NOW"]].forEach(([x, ry, rz, n, ic, a, b], i) => {
    const w = W(persp, x, 190, 520, 660, { transformStyle: "preserve-3d" });
    const c = el(w, "abs m-glass clip", { inset: 0, borderRadius: "46px" });
    el(c, "abs", { inset: 0, background: "linear-gradient(180deg, rgba(255,255,255,.05) 0%, rgba(255,90,31,0) 45%, rgba(255,90,31,.26) 100%)" });
    el(c, "abs", { left: "8%", right: "8%", top: 0, height: "3px", background: "linear-gradient(90deg, transparent, #fff, transparent)", boxShadow: "0 0 18px rgba(255,255,255,.7)" });
    const tile = el(c, "abs center", { left: "140px", top: "70px", width: "240px", height: "240px", borderRadius: "58px", background: "linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,.03))", border: "1.5px solid rgba(255,255,255,.18)", boxShadow: "inset 0 1.5px 0 rgba(255,255,255,.3)" }, icon(ic, 150, "url(#c01g)", 1.8));
    el(c, "abs caps", { left: "48px", right: "36px", bottom: "58px", fontSize: "56px", fontWeight: 850, lineHeight: 1.02, letterSpacing: "-.01em" }, `${a}<br><span style="color:#FD9457">${b}</span>`);
    const bd = W(w, -36, -36, 104, 104);
    el(bd, "abs center m-ember num", { inset: 0, borderRadius: "50%", fontSize: "50px", fontWeight: 900, boxShadow: "0 0 0 6px rgba(255,255,255,.95), 0 14px 30px rgba(0,0,0,.45)" }, String(n));
    const t0 = 0.3 + i * 0.3;
    S.neo(w, t0, { dist: 90, blur: 16 });
    S.float(w, 4, 1.2, i * 1.6);
    pop(bd, t0 + 0.55, { s0: 0.2, ease: "back2" });
    tile.querySelectorAll("path,circle,rect").forEach((p) => S.drawOn(p, t0 + 0.6, t0 + 1.4, "io"));
  });
});

D("C02", {
  name: "Fanned deck of cards", cat: "card", loop: 6.2,
  use: "<b>Lists where the current item is on top.</b> A small stack slides in beside him and fans like a hand of cards; the front card is the one he's talking about.",
  ref: { id: "I85", label: "Visual Inspo #73, #85 · Andy Stauring's editor" },
  recipe: ["#3a3a3a", "#FFE5D4", "#FF5A1F", "#8C8C8C"],
  fusion: "Three card Rectangles in one Merge chain; pivot below the cards; key Angle −18 / −7 / +7 on a spring. Front card: cream fill, ghost number Text+ at 22% opacity. NeoLightSweep on the front card.",
}, (S) => {
  const { el, W, A, F, icon, sweep, float } = S;
  S.ground("aroll");
  const specs = [
    { cls: "m-grey", n: "01", t: "SIGNALS", rz: -18, dx: -48, dy: 14, col: "rgba(255,255,255,.07)", tc: "#bdbdbd" },
    { cls: "m-grey", n: "02", t: "CONTACTS", rz: -7, dx: -15, dy: 4, col: "rgba(255,255,255,.08)", tc: "#d9d9d9" },
    { cls: "m-cream", n: "03", t: "THE <span style='color:#FF5A1F'>ANGLE</span>", rz: 7, dx: 30, dy: -15, col: "rgba(255,90,31,.22)", tc: "#1B0903", front: true },
  ];
  specs.forEach((s, i) => {
    const w = W(null, 250, 360, 290, 372, { transformOrigin: "50% 125%" });
    const c = el(w, "abs clip " + s.cls, { inset: 0, borderRadius: "28px" });
    el(c, "abs num", { right: "16px", bottom: "-24px", fontSize: "172px", fontWeight: 900, letterSpacing: "-.06em", color: s.col, lineHeight: 1 }, s.n);
    el(c, "abs caps", { left: "28px", top: "30px", right: "28px", fontSize: s.front ? "44px" : "32px", fontWeight: 900, lineHeight: 1, letterSpacing: "-.01em", color: s.tc }, s.front ? "THE<br><span style='color:#FF5A1F'>ANGLE</span>" : s.t);
    if (s.front) el(c, "abs center", { right: "24px", top: "26px", width: "54px", height: "54px", borderRadius: "16px", background: "#FF5A1F" }, icon("message", 30, "#fff", 2.2));
    A(w, {
      x: [[0.3, -420], [0.85, 0, "expo"], [1.0, 0], [1.55, s.dx, "spring"]],
      y: [[1.0, 0], [1.55, s.dy, "spring"]],
      rz: [[0.3, -6], [0.85, 0, "expo"], [1.0, 0], [1.55, s.rz, "spring"]],
      s: s.front ? [[1.0, 1], [1.55, 1.05, "spring"]] : [[0, 1]],
      o: [[0.3, 0], [0.45, 1, "out"]], blur: [[0.3, 16], [0.7, 0, "out"]],
    });
    if (s.front) { S.addSweep(c); sweep(c, 1.9, 1); }
    float(w, 4, 1.2, i * 0.8);
  });
});

D("C03", {
  name: "Counter card + hand-drawn arrow", cat: "card", loop: 6.2,
  use: "<b>A metric he's proud of or shocked by.</b> The number counts with its bar, then a hand-drawn arrow and a scribbled note point at it. The arrow wobbles like real drawn animation.",
  ref: { id: "B27", label: "Best editor 26, 27 · web 2026 hand-drawn trend" },
  recipe: ["#1c1c1c", "#FD9457", "#FF5A1F", "#ffffff"],
  fusion: "Glass Rectangle + Text+ counter + bar Rectangle Size X. Arrow: Polyline Write-On with a Displace (noise, stepped every 4 frames) for the boil. Note: Text+ rotated −5°.",
}, (S) => {
  const { el, W, A, F, neo, count, prog, hash } = S;
  S.ground("bgo");
  const X = 300, Y = 360, CW = 860, CH = 400;
  const card = W(null, X, Y, CW, CH);
  el(card, "abs", { left: "12%", right: "12%", bottom: "-50px", height: "100px", background: "radial-gradient(closest-side, rgba(255,90,31,.55), transparent)", filter: "blur(10px)" });
  el(card, "abs m-dark", { inset: 0, borderRadius: "42px" });
  el(card, "abs caps", { left: "58px", top: "54px", fontSize: "30px", fontWeight: 750, letterSpacing: ".16em", color: "#bdbdbd" }, "Accounts researched");
  const v = el(card, "abs num", { left: "50px", top: "96px", fontSize: "170px", fontWeight: 850, color: "#FD9457", letterSpacing: "-.04em", lineHeight: 1 }, "0");
  el(card, "abs", { left: "58px", right: "58px", top: "304px", height: "24px", borderRadius: "12px", background: "#333" });
  const fill = el(card, "abs", { left: "58px", top: "304px", height: "24px", borderRadius: "12px", background: "linear-gradient(90deg,#FD9457,#FF5A1F)", boxShadow: "0 0 18px rgba(255,90,31,.7)" });
  count(v, 0.6, 2.0, 0, 3655);
  F((t) => { fill.style.width = ((CW - 116) * prog(t, 0.6, 2.0, "out")).toFixed(1) + "px"; });
  const svg = S.svg();
  const arrow = S.path(svg, "", { color: "#fff", width: 8 });
  const head = S.path(svg, "", { color: "#fff", width: 8 });
  F((t) => {
    const f = Math.floor(t * 6), j = (k) => ((hash(f * 13 + k) - 0.5) * 7).toFixed(1);
    arrow.setAttribute("d", `M${1590 + +j(1)} ${260 + +j(2)} C ${1520 + +j(3)} ${360 + +j(4)}, ${1400 + +j(5)} ${450 + +j(6)}, ${1196 + +j(7)} ${462 + +j(8)}`);
    head.setAttribute("d", `M${1236 + +j(9)} ${424 + +j(10)} L${1194 + +j(11)} ${462 + +j(12)} L${1240 + +j(13)} ${492 + +j(14)}`);
  });
  S.drawOn(arrow, 2.1, 2.6, "io"); S.drawOn(head, 2.55, 2.7, "out");
  const note = W(null, 1330, 140, 520, 90);
  const nt = el(note, "abs", { left: 0, top: 0, fontSize: "64px", fontWeight: 700, color: "#fff", whiteSpace: "nowrap", transform: "rotate(-5deg)", letterSpacing: "-.01em" }, "");
  S.typeText(nt, 2.65, 3.2, "the whole list");
  neo(card, 0.3, { dist: 60, s0: 0.97 });
});

D("C04", {
  name: "Glossy 3D tiles with reflection", cat: "card", loop: 6.2,
  use: "<b>Products, offers, tools, “this vs that”.</b> App-icon tiles rise onto a reflective floor and turn to face us; the chosen one gets the ✓. White vs orange, so it isn't one colour again.",
  ref: { id: "I104", label: "Visual Inspo #103, #104 · Nate Herk's editor" },
  recipe: ["#ffffff", "#FF5A1F", "#8C8C8C", "#FD9457"],
  fusion: "Squircle Rectangle (corner 0.5) + NeoBevel + a gloss Rectangle on top; NeoReflection for the floor. 3D turn: ImagePlane3D + Renderer3D, or a DVE Y rotation.",
}, (S) => {
  const { el, W, A, F, pop, icon, ripple } = S;
  S.ground("bgo");
  const persp = el(null, "abs", { inset: 0, perspective: "1600px", perspectiveOrigin: "50% 40%" });
  [[520, "white", "wrench", "#FF5A1F", "Service"], [1100, "ember", "box", "#fff", "Product"]].forEach(([x, kind, ic, col, label], i) => {
    const w = W(persp, x, 360, 300, 300);
    const tile = el(w, "abs center", { inset: 0, borderRadius: "78px", background: kind === "white" ? "linear-gradient(160deg,#FFFFFF 0%,#F0EAE6 58%,#DCD2CB 100%)" : "linear-gradient(160deg,#FFA06A 0%,#FF5A1F 55%,#D5400D 100%)", boxShadow: "inset 0 3px 0 rgba(255,255,255,.9), inset 0 -12px 22px rgba(0,0,0,.14), 0 34px 60px rgba(0,0,0,.5)", WebkitBoxReflect: "below 22px linear-gradient(transparent 58%, rgba(0,0,0,.3))" }, icon(ic, 160, col, 2));
    el(tile, "abs", { left: "9%", right: "9%", top: "5%", height: "40%", borderRadius: "64px 64px 36px 36px", background: "linear-gradient(180deg, rgba(255,255,255,.5), rgba(255,255,255,0))" });
    const pl = W(null, x + 20, 720, 260, 72);
    el(pl, "abs center m-grey caps", { inset: 0, borderRadius: "36px", fontSize: "30px", fontWeight: 850, letterSpacing: ".1em" }, label);
    const t0 = 0.3 + i * 0.28;
    A(w, { y: [[t0, 240], [t0 + 0.85, 0, "expo"]], ry: [[t0, 40], [t0 + 1.0, 0, "expo"], [3.6, -7, "sine"], [6.2, 5, "sine"]], o: [[t0, 0], [t0 + 0.3, 1, "out"]], blur: [[t0, 12], [t0 + 0.5, 0, "out"]] });
    S.neo(pl, t0 + 0.6, { dist: 30, blur: 8 });
    tile.querySelectorAll("path,circle,rect").forEach((p) => S.drawOn(p, t0 + 0.55, t0 + 1.3, "io"));
    if (kind === "ember") {
      const bd = W(w, 300 - 60, -32, 92, 92);
      el(bd, "abs center", { inset: 0, borderRadius: "50%", background: "#fff", boxShadow: "0 0 0 5px #FF5A1F, 0 12px 26px rgba(0,0,0,.45)" }, icon("check", 52, "#FF5A1F", 3.4));
      pop(bd, 1.7, { s0: 0.1, ease: "back2" });
      ripple(w, 300 - 14, 14, 92, 1.78, "#FD9457");
    }
  });
});

D("C05", {
  name: "Milestone flags on an orange horizon", cat: "card", loop: 6.4,
  use: "<b>Stages, pillars, milestones.</b> A glowing planet edge rises, poles grow out of it and the flags unfurl one by one. The current stage flies orange; its flag keeps waving.",
  ref: { id: "I75", label: "Visual Inspo #74, #75 · Andy Stauring's editor" },
  recipe: ["#FFE5D4", "#FF5A1F", "#1c1c1c", "#FD9457"],
  fusion: "Planet: big Ellipse + NeoGlow on its edge. Poles: Rectangles with Size Y keyed from the base. Flags: Polygon cut-corner mask, Transform Size X from the pole; the wave is a Grid Warp or Bender.",
}, (S) => {
  const { el, W, A, F } = S;
  S.ground("bgo");
  const R = 1700, top = 800;
  const pl = el(null, "abs", { left: 960 - R + "px", top: top + "px", width: 2 * R + "px", height: 2 * R + "px", borderRadius: "50%", background: "radial-gradient(closest-side, #140703 0%, #1d0a04 90%, #3a1407 100%)", boxShadow: "0 -6px 24px rgba(255,120,60,.95), 0 -40px 140px rgba(255,90,31,.5), inset 0 22px 50px rgba(255,90,31,.45)", border: "3px solid #FF7A40" });
  A(pl, { y: [[0.2, 280], [1.0, 0, "expo"]], o: [[0.2, 0], [0.5, 1, "out"]] });
  const flags = [[560, "Define", "01", false], [960, "Research", "02", false], [1360, "Build", "03", true]];
  flags.forEach(([x, name, num, active], i) => {
    const dx = x - 960, base = top + (R - Math.sqrt(R * R - dx * dx)), ftop = 300;
    const pole = el(null, "abs", { left: x - 3 + "px", top: ftop + "px", width: "6px", height: base - ftop + 4 + "px", borderRadius: "3px", background: "linear-gradient(180deg,#fff,rgba(255,255,255,.35))", transformOrigin: "50% 100%" });
    const tip = el(null, "abs", { left: x - 10 + "px", top: ftop - 10 + "px", width: "20px", height: "20px", borderRadius: "50%", background: "#fff", boxShadow: "0 0 18px #FD9457, 0 0 36px #FF5A1F" });
    const p0 = 0.8 + i * 0.2;
    A(pole, { sy: [[p0, 0], [p0 + 0.5, 1, "expo"]] });
    A(tip, { y: [[p0, base - ftop], [p0 + 0.5, 0, "expo"]], o: [[p0, 0], [p0 + 0.1, 1]] });
    const fw = W(null, x + 3, ftop, 340, 220, { transformOrigin: "0% 50%" });
    const flag = el(fw, "abs clip " + (active ? "m-ember" : "m-cream"), { inset: 0, borderRadius: "0 0 26px 0", clipPath: "polygon(0 0, calc(100% - 48px) 0, 100% 48px, 100% 100%, 0 100%)" });
    el(flag, "abs caps", { left: "30px", top: "30px", fontSize: "46px", fontWeight: 900, letterSpacing: "-.01em", color: active ? "#fff" : "#1B0903" }, name);
    el(flag, "abs num", { right: "22px", bottom: "-18px", fontSize: "140px", fontWeight: 900, letterSpacing: "-.05em", color: active ? "rgba(255,255,255,.3)" : "rgba(255,90,31,.26)", lineHeight: 1 }, num);
    const f0 = 1.1 + i * 0.22;
    A(fw, { sx: [[f0, 0], [f0 + 0.6, 1, "back"]], o: [[f0, 0], [f0 + 0.1, 1]] });
    if (active) F((t) => { flag.style.transform = `skewY(${(Math.sin(t * 3.2) * 2.2 * S.prog(t, 1.8, 2.3)).toFixed(2)}deg)`; });
  });
});

D("C06", {
  name: "Wrong vs right cards", cat: "card", loop: 6.2,
  use: "<b>The old way vs the new way.</b> Grey card first, then the orange card pops bigger; the grey one shrinks back and gets the ✗, the orange one gets the ✓ and a shine.",
  ref: { id: "B13", label: "Best editor 13 · Visual Inspo #125" },
  recipe: ["#3a3a3a", "#FF5A1F", "#ffffff", "#8C8C8C"],
  fusion: "Two Rectangles (corner 0.3): grey and orange. Badges: Ellipses. Grey card: Transform Size 0.94 + Brightness down. Orange card: NeoGlow + NeoLightSweep.",
}, (S) => {
  const { el, W, A, F, pop, icon, ripple, sweep, prog } = S;
  S.ground("bgo");
  const card = (x, cls, ic, icb, t1, t2, sub) => {
    const w = W(null, x, 220, 540, 640);
    const c = el(w, "abs clip " + cls, { inset: 0, borderRadius: "46px" });
    el(c, "abs center", { left: "52px", top: "52px", width: "108px", height: "108px", borderRadius: "32px", background: icb }, icon(ic, 60, "#fff", 2.2));
    el(c, "abs caps", { left: "54px", right: "40px", bottom: "150px", fontSize: "76px", fontWeight: 900, lineHeight: 0.98, letterSpacing: "-.02em" }, `${t1}<br>${t2}`);
    el(c, "abs", { left: "56px", right: "40px", bottom: "64px", fontSize: "32px", fontWeight: 550, opacity: 0.8 }, sub);
    return { w, c };
  };
  const glow = el(null, "abs", { left: "960px", top: "180px", width: "660px", height: "720px", borderRadius: "80px", background: "radial-gradient(closest-side, rgba(255,90,31,.55), transparent)", filter: "blur(30px)" });
  const L = card(360, "m-grey", "megaphone", "#4a4a4a", "Spray", "and pray", "Same email to everyone");
  const Rr = card(1020, "m-ember", "target", "rgba(255,255,255,.22)", "Signal", "first", "The right email, right person");
  el(null, "abs center caps", { left: "900px", top: "500px", width: "120px", height: "80px", fontSize: "40px", fontWeight: 900, color: "rgba(255,255,255,.35)" }, "vs");
  A(L.w, { s: [[0.3, 0.9], [0.8, 1, "back"], [1.6, 1], [2.1, 0.94, "out"]], o: [[0.3, 0], [0.45, 1, "out"]], blur: [[0.3, 10], [0.6, 0, "out"]], x: [[1.6, 0], [2.1, -22, "out"]], br: [[1.6, 1], [2.1, 0.62]], sat: [[1.6, 1], [2.1, 0.2]] });
  A(Rr.w, { s: [[0.9, 0.9], [1.4, 1, "back"], [1.6, 1], [2.1, 1.05, "back"]], o: [[0.9, 0], [1.05, 1, "out"]], blur: [[0.9, 10], [1.2, 0, "out"]] });
  F((t) => { glow.style.opacity = (prog(t, 1.6, 2.2) * (0.75 + 0.25 * Math.sin(t * 2.4))).toFixed(3); });
  const xb = W(null, 360 + 540 - 64, 190, 96, 96);
  el(xb, "abs center", { inset: 0, borderRadius: "50%", background: "#262626", boxShadow: "0 0 0 5px #4a4a4a, 0 12px 26px rgba(0,0,0,.45)" }, icon("x", 50, "#d0d0d0", 3.4));
  const cb = W(null, 1020 + 540 - 50, 176, 104, 104);
  el(cb, "abs center", { inset: 0, borderRadius: "50%", background: "#fff", boxShadow: "0 0 0 6px #FF5A1F, 0 12px 26px rgba(0,0,0,.45)" }, icon("check", 58, "#FF5A1F", 3.4));
  pop(xb, 1.85, { s0: 0.1, ease: "back2" });
  pop(cb, 2.05, { s0: 0.1, ease: "back2" }); ripple(null, 1020 + 540 + 2, 228, 104, 2.12, "#FD9457");
  S.addSweep(Rr.c); sweep(Rr.c, 2.35, 1);
});

D("C07", {
  name: "Profile card with buying signals", cat: "card", loop: 6.4,
  use: "<b>Introducing a person:</b> a prospect, a client, a founder. White card on a light ground, banner wipes, avatar pops, then the signals stack in and the status pill lands.",
  ref: { id: "M7-67", label: "Top Engagement List, $7M Founder 1:07 (approved) · pushed further" },
  recipe: ["#ffffff", "#FF5A1F", "#FFE9DC", "#1B0903"],
  fusion: "White Rectangle card + DropShadow on cream. Banner: orange gradient Rectangle revealed left → right. Avatar: Ellipse mask on the photo + white ring. Signal rows: Rectangles with Follower-style delays.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon, clip, ripple } = S;
  S.ground("bgo");
  const X = 610, Y = 120, CW = 700, CH = 840;
  const card = W(null, X, Y, CW, CH);
  const c = el(card, "abs m-paper clip", { inset: 0, borderRadius: "46px", boxShadow: "0 40px 90px rgba(120,50,20,.22), 0 0 0 1.5px rgba(90,30,8,.05)" });
  const ban = el(c, "abs", { left: 0, right: 0, top: 0, height: "210px", background: "linear-gradient(120deg,#FF5A1F,#FD9457)" });
  el(ban, "abs", { inset: 0, backgroundImage: "radial-gradient(rgba(255,255,255,.28) 2px, transparent 2.5px)", backgroundSize: "26px 26px", opacity: 0.6 });
  clip(ban, [0, CW, 0, 0], [0, 0, 0, 0], 0.4, 0.95, 0, "expo");
  const av = W(c, CW / 2 - 100, 110, 200, 200);
  el(av, "abs center", { inset: 0, borderRadius: "50%", background: "linear-gradient(180deg,#3A1508,#1B0903)", color: "#fff", fontSize: "76px", fontWeight: 850, boxShadow: "0 0 0 9px #fff, 0 0 0 13px rgba(255,90,31,.35), 0 16px 36px rgba(120,40,0,.3)" }, "SL");
  pop(av, 0.75, { s0: 0.3 }); ripple(c, CW / 2, 210, 220, 0.9, "rgba(255,90,31,.6)");
  const nm = el(c, "abs center", { left: 0, right: 0, top: "334px", fontSize: "62px", fontWeight: 850, letterSpacing: "-.02em", color: "#1B0903" }, "Sarah Lee");
  const rl = el(c, "abs center", { left: 0, right: 0, top: "412px", fontSize: "32px", fontWeight: 550, color: "#8c7f78" }, "VP Sales · Northwind");
  neo(nm, 0.95, { dist: 30, blur: 8 }); neo(rl, 1.05, { dist: 30, blur: 8 });
  const hd = el(c, "abs caps", { left: "56px", top: "490px", fontSize: "24px", fontWeight: 800, letterSpacing: ".24em", color: "#FF5A1F" }, "Buying signals");
  neo(hd, 1.25, { ang: 180, dist: 30, blur: 6 });
  [["users", "Hiring 3 SDRs"], ["dollar", "Raised a Series B"], ["user", "New VP of Sales"]].forEach(([ic, tx], i) => {
    const r = W(c, 46, 534 + i * 88, CW - 92, 74);
    el(r, "abs row", { inset: 0, borderRadius: "24px", background: "#FFF6F0", padding: "0 20px 0 10px", gap: "18px", fontSize: "34px", fontWeight: 650, color: "#1B0903" }, `<span class="center" style="width:56px;height:56px;border-radius:18px;background:#FF5A1F">${icon(ic, 32, "#fff", 2.3)}</span>${tx}`);
    neo(r, 1.4 + i * 0.16, { ang: 180, dist: 60, blur: 10 });
  });
  const st = W(c, CW - 290, 30, 262, 64);
  el(st, "abs row m-paper caps", { inset: 0, borderRadius: "32px", justifyContent: "center", gap: "12px", fontSize: "23px", fontWeight: 850, letterSpacing: ".08em", color: "#1B0903", boxShadow: "0 10px 24px rgba(120,40,0,.25)" }, '<i class="pd" style="width:16px;height:16px;border-radius:50%;background:#FF5A1F;display:block"></i>Ready to buy');
  pop(st, 2.25, { s0: 0.3, ease: "back2" });
  const pd = st.querySelector(".pd");
  F((t) => { const k = Math.max(0, Math.sin(t * 5)); pd.style.boxShadow = `0 0 0 ${(k * 7).toFixed(1)}px rgba(255,90,31,${(0.35 * (1 - k)).toFixed(3)})`; });
  A(card, { y: [[0.2, 80], [0.8, 0, "expo"]], o: [[0.2, 0], [0.45, 1, "out"]], blur: [[0.2, 10], [0.6, 0, "out"]] });
});

D("C08", {
  name: "Notification stack", cat: "card", loop: 6.4,
  use: "<b>Proof that it worked:</b> replies, bookings, deals. Phone-style notifications drop in at the top right and stack behind each other, newest on top.",
  ref: { id: "I23", label: "Web · iOS notification stacks · Visual Inspo #23" },
  recipe: ["rgba(255,255,255,.85)", "#FF5A1F", "#1B0903", "#FD9457"],
  fusion: "Light glass Rectangles (blurred A-roll behind, white 85%). Each new card: Transform Y on a spring; older ones step down 26 px, Size −5 %, Brightness down.",
}, (S) => {
  const { el, W, F, icon, prog, lerp, E } = S;
  S.ground("aroll");
  const notes = [["mail", "#FF5A1F", "Gmail", "Sarah Lee", "Honestly, too long."], ["calendar", "#1B0903", "Calendar", "Meeting booked", "Thu · 10:00 with Northwind"], ["trend", "#FD9457", "CRM", "Deal created", "Northwind · stage 1"]];
  const arr = [0.4, 1.35, 2.3];
  const els = notes.map(([ic, bg, app, title, body], i) => {
    const w = el(null, "abs", { left: "1200px", top: "0px", width: "660px", height: "136px", transformOrigin: "50% 0%" });
    el(w, "abs row m-light", { inset: 0, borderRadius: "38px", padding: "0 30px 0 24px", gap: "22px" },
      `<span class="center" style="width:84px;height:84px;border-radius:24px;background:${bg};flex:none">${icon(ic, 46, "#fff", 2.2)}</span>` +
      `<span class="col" style="gap:4px;flex:1;min-width:0"><span class="row" style="justify-content:space-between;font-size:22px;font-weight:700;letter-spacing:.08em;color:#8c7f78;text-transform:uppercase"><span>${app}</span><span style="letter-spacing:0;text-transform:none;font-weight:550">now</span></span>` +
      `<b style="font-size:34px;font-weight:800;color:#1B0903;white-space:nowrap">${title}</b><span style="font-size:29px;font-weight:500;color:#5b4f49;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${body}</span></span>`);
    return w;
  });
  F((t) => {
    els.forEach((w, i) => {
      const a = arr[i];
      let depth = 0;
      for (let k = i + 1; k < arr.length; k++) depth += prog(t, arr[k], arr[k] + 0.45, "out");
      const inq = Math.min(1, Math.max(0, (t - a) / 0.6));
      const yIn = lerp(-190, 70, E.spring(inq));
      const y = yIn + depth * 30;
      const s = 1 - depth * 0.055;
      const o = t < a ? 0 : Math.min(1, (t - a) / 0.15) * (1 - Math.max(0, depth - 1.6));
      Object.assign(w.style, { transform: `translateY(${y.toFixed(1)}px) scale(${s.toFixed(4)})`, opacity: o.toFixed(3), zIndex: String(10 - Math.round(depth * 2)), filter: depth > 0.05 ? `brightness(${(1 - depth * 0.12).toFixed(3)})` : "" });
    });
  });
});
