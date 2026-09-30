// CIRCLES — O01..O10. Hubs, orbits, rings, badges and marks.

D("O01", {
  name: "Hub ring with labels around it", cat: "circle", loop: 6.4,
  use: "<b>One thing and what it does.</b> A thick glowing ring draws itself, the idea sits in the middle, and each effect branches off on the right as he names it. The ring's light keeps turning.",
  ref: { id: "I87", label: "Visual Inspo #86, #87 · Andy Stauring's editor" },
  recipe: ["#FF5A1F", "#FD9457", "#1c1c1c", "#ffffff"],
  fusion: "Ring: Ellipse with Border Width + gradient, Write-On via the mask's Length, NeoGlow; spin the gradient angle. Branches: Polylines + Ellipse icon holders + Text+, one Follower delay each.",
}, (S) => {
  const { el, W, A, F, neo, pop, icon } = S;
  S.ground("graphite", { grid: "dots" });
  const cx = 620, cy = 540, R = 250;
  el(null, "abs", { left: cx - 420 + "px", top: cy - 420 + "px", width: "840px", height: "840px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,90,31,.2), transparent)" });
  const svg = S.svg();
  svg.innerHTML = `<defs><linearGradient id="o01g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD2B8"/><stop offset=".35" stop-color="#FF5A1F"/><stop offset=".7" stop-color="#7A2A0E"/><stop offset="1" stop-color="#FD9457"/></linearGradient></defs>`;
  svg.style.filter = "drop-shadow(0 0 22px rgba(255,90,31,.75))";
  const g = S.node(svg, "g", {});
  const ring = S.node(g, "circle", { cx, cy, r: R, fill: "none", stroke: "url(#o01g)", "stroke-width": 42, "stroke-linecap": "round" });
  g.style.transformOrigin = `${cx}px ${cy}px`;
  F((t) => { g.style.transform = `rotate(${(t * 24 - 90).toFixed(2)}deg)`; });
  S.drawOn(ring, 0.3, 1.2, "io");
  const disc = W(null, cx - 200, cy - 200, 400, 400);
  el(disc, "abs center col", { inset: 0, borderRadius: "50%", background: "radial-gradient(circle at 50% 35%, #2a2a2a, #111 70%)", boxShadow: "inset 0 10px 30px rgba(0,0,0,.6), inset 0 -2px 0 rgba(255,255,255,.06)", gap: "12px" }, icon("spark", 110, "#FF5A1F", 2.6) + '<span style="font-size:36px;font-weight:900;letter-spacing:.08em">THE SKILL</span>');
  pop(disc, 0.55, { s0: 0.6 });
  const items = [[-58, "building", "Finds accounts"], [-20, "eye", "Reads the signals"], [20, "user", "Picks the person"], [58, "pen", "Writes the angle"]];
  items.forEach(([deg, ic, tx], i) => {
    const a = (deg * Math.PI) / 180, c = Math.cos(a), s = Math.sin(a);
    const t0 = 1.25 + i * 0.45;
    const ln = S.path(svg, `M${cx + 292 * c} ${cy + 292 * s} L${cx + 418 * c} ${cy + 418 * s}`, { color: "rgba(255,255,255,.55)", width: 3 });
    S.drawOn(ln, t0, t0 + 0.25, "out");
    const dt = W(null, cx + 292 * c - 9, cy + 292 * s - 9, 18, 18);
    el(dt, "abs", { inset: 0, borderRadius: "50%", background: "#fff", boxShadow: "0 0 12px #FD9457" });
    pop(dt, t0 - 0.05, { s0: 0, dur: 0.3 });
    const nx = cx + 470 * c, ny = cy + 470 * s;
    const nd = W(null, nx - 52, ny - 52, 104, 104);
    el(nd, "abs center m-dark", { inset: 0, borderRadius: "50%", boxShadow: "0 0 0 3px rgba(255,90,31,.8), 0 14px 30px rgba(0,0,0,.5)" }, icon(ic, 50, "#FD9457", 2.2));
    pop(nd, t0 + 0.2, { s0: 0.3 });
    const lb = W(null, nx + 76, ny - 30, 520, 60);
    el(lb, "abs", { left: 0, top: 0, fontSize: "46px", fontWeight: 750, letterSpacing: "-.01em", whiteSpace: "nowrap" }, tx);
    neo(lb, t0 + 0.3, { ang: 180, dist: 40, blur: 10 });
  });
});

D("O02", {
  name: "Sonar hub with pills on the rings", cat: "circle", loop: 6.4,
  use: "<b>Someone at the centre and what surrounds them</b>: signals around a buyer, forces around a business. Light-orange ground, white rings, the pulse keeps going.",
  ref: { id: "I57", label: "Visual Inspo #56, #57 · best editor 12" },
  recipe: ["#FD9457", "#ffffff", "#1B0903", "#FF5A1F"],
  fusion: "Light-orange Background; rings = Ellipse outlines. Pulse: one Ellipse outline with Size and Blend keyed on a loop. Pills: Rectangles (corner 1.0) placed on the rings, back-ease pops.",
}, (S) => {
  const { el, W, A, F, pop, icon } = S;
  S.ground("peach", { grid: true });
  const cx = 960, cy = 520;
  [340, 560, 780, 1020].forEach((d, i) => {
    const r = el(null, "abs", { left: cx - d / 2 + "px", top: cy - d / 2 + "px", width: d + "px", height: d + "px", borderRadius: "50%", border: "2.5px solid rgba(255,255,255,.6)", background: "radial-gradient(closest-side, rgba(255,255,255,0) 70%, rgba(255,255,255,.14))" });
    A(r, { s: [[0.35 + i * 0.1, 0.6], [0.95 + i * 0.1, 1, "expo"]], o: [[0.35 + i * 0.1, 0], [0.6 + i * 0.1, 1, "out"]] });
  });
  const pulses = [0, 1].map(() => el(null, "abs", { borderRadius: "50%", border: "3px solid rgba(255,255,255,.9)" }));
  F((t) => {
    pulses.forEach((p, k) => {
      const q = t < 0.9 ? 0 : (((t - 0.9) / 2.0 + k * 0.5) % 1), d = 280 + q * 1100;
      Object.assign(p.style, { width: d + "px", height: d + "px", left: cx - d / 2 + "px", top: cy - d / 2 + "px", opacity: t < 0.9 ? 0 : ((1 - q) * 0.7).toFixed(3) });
    });
  });
  const hub = W(null, cx - 135, cy - 135, 270, 270);
  el(hub, "abs center", { inset: 0, borderRadius: "50%", background: "linear-gradient(180deg,#3A1508,#1B0903)", boxShadow: "0 0 0 9px #fff, 0 24px 50px rgba(120,40,0,.4)" }, icon("user", 124, "#FF5A1F", 2));
  const yo = W(null, cx - 80, cy + 118, 160, 66);
  el(yo, "abs center m-ember caps", { inset: 0, borderRadius: "33px", fontSize: "32px", fontWeight: 900, letterSpacing: ".1em", boxShadow: "0 0 0 4px #fff" }, "Buyer");
  pop(hub, 0.3, { s0: 0.4 }); pop(yo, 0.75, { s0: 0.4 });
  const pills = [[-155, 390, "Hiring", "users", "m-paper"], [-25, 390, "Funding", "dollar", "m-paper"], [150, 510, "New VP", "user", "dark"], [30, 510, "Tech change", "gear", "ember"]];
  pills.forEach(([deg, r, tx, ic, kind], i) => {
    const a = (deg * Math.PI) / 180, x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
    const w = W(null, x, y, null, 88);
    const bg = kind === "dark" ? "background:linear-gradient(180deg,#3A1508,#1B0903);color:#fff" : kind === "ember" ? "" : "";
    const p = el(w, "row caps " + (kind === "m-paper" ? "m-paper" : kind === "ember" ? "m-ember" : ""), { height: "88px", borderRadius: "44px", padding: "0 30px 0 12px", gap: "16px", fontSize: "34px", fontWeight: 850, letterSpacing: ".02em", whiteSpace: "nowrap", boxShadow: "0 16px 36px rgba(120,40,0,.28)" },
      `<span class="center" style="width:62px;height:62px;border-radius:50%;background:${kind === "m-paper" ? "#FF5A1F" : "rgba(255,255,255,.2)"}">${icon(ic, 34, "#fff", 2.3)}</span>${tx}`);
    if (kind === "dark") p.setAttribute("style", p.getAttribute("style") + ";" + bg);
    S.A(w, { s: [[1.2 + i * 0.3, 0.3], [1.65 + i * 0.3, 1, "back2"]], o: [[1.2 + i * 0.3, 0], [1.35 + i * 0.3, 1, "out"]] }, "translate(-50%,-50%)");
  });
});

D("O03", {
  name: "Orbit system", cat: "circle", loop: 6.4,
  use: "<b>An ecosystem around one thing</b>: channels around a pipeline, clients around an agency, tools around a workflow. Satellites really orbit, passing behind and in front.",
  ref: { id: "B19", label: "Best editor 19 · Visual Inspo #41 · web orbit animations" },
  recipe: ["#FF5A1F", "#FD9457", "#1c1c1c", "#ffffff"],
  fusion: "Planet: Ellipse with a radial gradient + NeoGlow. Orbits: Ellipse outlines squashed and rotated. Satellites: a Transform on a Path modifier per orbit, or Shape3D in Renderer3D for real depth.",
}, (S) => {
  const { el, W, A, F, pop, icon } = S;
  S.ground("warm", { grid: true });
  const cx = 960, cy = 540, tilt = (-9 * Math.PI) / 180;
  const orbits = [[440, 150], [660, 228]];
  const svg = S.svg();
  orbits.forEach(([a, b], i) => {
    const e = S.node(svg, "ellipse", { cx, cy, rx: a, ry: b, fill: "none", stroke: i ? "rgba(255,255,255,.22)" : "rgba(253,148,87,.45)", "stroke-width": 2.5, transform: `rotate(-9 ${cx} ${cy})` });
    S.drawOn(e, 0.5 + i * 0.2, 1.3 + i * 0.2, "io");
  });
  const pl = W(null, cx - 160, cy - 160, 320, 320);
  pl.style.zIndex = 3;
  el(pl, "abs center col caps", { inset: 0, borderRadius: "50%", background: "radial-gradient(circle at 34% 28%, #FFC9A8 0%, #FF7A40 28%, #FF5A1F 52%, #A9360D 100%)", boxShadow: "0 0 90px rgba(255,90,31,.6), inset -18px -24px 50px rgba(90,20,0,.45)", fontSize: "40px", fontWeight: 900, lineHeight: 1.02, letterSpacing: ".02em", textAlign: "center" }, "Your<br>pipeline");
  pop(pl, 0.3, { s0: 0.4 });
  const sats = [[0, 0.2, "mail", "#FF5A1F"], [0, 3.3, "phone", "#FD9457"], [1, 1.1, "calendar", "#fff"], [1, 3.2, "users", "#FD9457"], [1, 5.2, "message", "#FF5A1F"]];
  sats.forEach(([oi, th0, ic, col], i) => {
    const [a, b] = orbits[oi], w = oi ? 0.42 : 0.62;
    const s = el(null, "abs", { width: "110px", height: "110px" });
    const inner = el(s, "abs center m-dark", { inset: 0, borderRadius: "50%", boxShadow: "0 0 0 2.5px rgba(255,255,255,.25), 0 14px 30px rgba(0,0,0,.5)" }, icon(ic, 52, col, 2.2));
    F((t) => {
      const th = th0 + w * t, ex = a * Math.cos(th), ey = b * Math.sin(th);
      const x = cx + ex * Math.cos(tilt) - ey * Math.sin(tilt), y = cy + ex * Math.sin(tilt) + ey * Math.cos(tilt);
      const front = Math.sin(th), k = 0.78 + 0.22 * (front + 1) / 2, o = S.prog(t, 1.0 + i * 0.12, 1.4 + i * 0.12);
      Object.assign(s.style, { left: (x - 55).toFixed(1) + "px", top: (y - 55).toFixed(1) + "px", transform: `scale(${(k * (0.4 + 0.6 * o)).toFixed(3)})`, opacity: o.toFixed(3), zIndex: front > 0 ? 5 : 1, filter: `brightness(${(0.6 + 0.4 * (front + 1) / 2).toFixed(3)})` });
    });
  });
});

D("O04", {
  name: "Big-numeral circle with pills", cat: "circle", loop: 6.2,
  use: "<b>“There are 3 things.”</b> A huge circle half off the frame holds the number; each item branches out as a pill with a slanted orange number.",
  ref: { id: "B1", label: "Best editor 1 · Nate Herk video" },
  recipe: ["#FF5A1F", "#FD9457", "#1c1c1c", "#ffffff"],
  fusion: "Ellipse outline with a gradient Border + NeoGlow, Write-On via mask length; big Text+ numeral. Pills: Rectangles with a sheared Text+ number (Transform Shear X −0.18). Lines: Polylines Write-On.",
}, (S) => {
  const { el, W, A, neo, pop } = S;
  S.ground("warm", { grid: true });
  const cx = 330, cy = 540, R = 420;
  el(null, "abs", { left: cx - R + "px", top: cy - R + "px", width: 2 * R + "px", height: 2 * R + "px", borderRadius: "50%", background: "radial-gradient(closest-side, rgba(255,90,31,.16), rgba(255,90,31,.03) 80%, transparent)" });
  const svg = S.svg();
  svg.innerHTML = `<defs><linearGradient id="o04g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FD9457"/><stop offset=".5" stop-color="#FF5A1F"/><stop offset="1" stop-color="#FF5A1F" stop-opacity=".15"/></linearGradient></defs>`;
  svg.style.filter = "drop-shadow(0 0 14px rgba(255,90,31,.7))";
  const c1 = S.node(svg, "circle", { cx, cy, r: R, fill: "none", stroke: "url(#o04g)", "stroke-width": 8, transform: `rotate(-90 ${cx} ${cy})` });
  const c2 = S.node(svg, "circle", { cx, cy, r: R - 44, fill: "none", stroke: "rgba(255,255,255,.1)", "stroke-width": 2 });
  S.drawOn(c1, 0.3, 1.2, "io"); S.drawOn(c2, 0.45, 1.35, "io");
  const nm = W(null, 250, 250, 300, 380);
  el(nm, "abs center", { inset: 0, fontSize: "380px", fontWeight: 900, letterSpacing: "-.06em", lineHeight: 1, textShadow: "0 10px 40px rgba(0,0,0,.4)" }, "3");
  A(nm, { s: [[0.6, 1.5], [1.1, 1, "expo"]], o: [[0.6, 0], [0.75, 1, "out"]], blur: [[0.6, 20], [1.0, 0, "out"]] });
  const lb = W(null, 170, 640, 460, 90);
  el(lb, "abs center caps gtext", { inset: 0, fontSize: "80px", fontWeight: 900, letterSpacing: ".02em" }, "Signals");
  neo(lb, 0.9, { dist: 40 });
  [[342, "1", "Hiring now"], [542, "2", "Fresh funding"], [742, "3", "New leader"]].forEach(([y, n, tx], i) => {
    const a = Math.asin((y - cy) / R), x0 = cx + R * Math.cos(a);
    const t0 = 1.25 + i * 0.35;
    const ln = S.path(svg, `M${x0.toFixed(1)} ${y} L 860 ${y}`, { color: "rgba(255,255,255,.5)", width: 3 });
    S.drawOn(ln, t0, t0 + 0.25, "out");
    const dt = W(null, x0 - 11, y - 11, 22, 22);
    el(dt, "abs", { inset: 0, borderRadius: "50%", background: "#fff", boxShadow: "0 0 14px #FF5A1F" });
    pop(dt, t0 - 0.05, { s0: 0, dur: 0.3 });
    const p = W(null, 860, y - 64, 780, 128);
    el(p, "abs row m-dark", { inset: 0, borderRadius: "64px", padding: "0 40px 0 36px", gap: "30px" }, `<span class="gtext" style="font-size:96px;font-weight:900;letter-spacing:-.04em;display:inline-block;transform:skewX(-10deg);line-height:1">${n}</span><span style="font-size:52px;font-weight:750;letter-spacing:-.01em;white-space:nowrap">${tx}</span>`);
    neo(p, t0 + 0.15, { ang: 180, dist: 70 });
  });
});

D("O05", {
  name: "Progress ring", cat: "circle", loop: 6.2,
  use: "<b>Percentages and shares:</b> reply rate, completion, signal vs noise. A clean ring on a light ground, a glowing head on the arc, the number counting with it.",
  ref: { web: "Web · Dribbble progress rings · the 80% signal pie in Taking a Step Back (approved)" },
  recipe: ["#FFE9DC", "#FF5A1F", "#FD9457", "#1B0903"],
  fusion: "Two Ellipses with Border Width: a light track and a gradient arc whose mask Length is keyed (round caps via a small Ellipse at each end). Head: Ellipse + NeoGlow on the arc end. Counter: Text+.",
}, (S) => {
  const { el, W, F, neo, count, prog } = S;
  S.ground("cream", { grid: true });
  const cx = 960, cy = 450, R = 250, SW = 50, C = 2 * Math.PI * R, P = 0.8;
  const svg = S.svg();
  svg.innerHTML = `<defs><linearGradient id="o05g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FD9457"/><stop offset="1" stop-color="#FF5A1F"/></linearGradient></defs>`;
  const tr = S.node(svg, "circle", { cx, cy, r: R, fill: "none", stroke: "#F0DDD0", "stroke-width": SW });
  const arc = S.node(svg, "circle", { cx, cy, r: R, fill: "none", stroke: "url(#o05g)", "stroke-width": SW, "stroke-linecap": "round", transform: `rotate(-90 ${cx} ${cy})`, "stroke-dasharray": `${C} ${C}` });
  const head = el(null, "abs", { width: "34px", height: "34px", borderRadius: "50%", background: "#fff", boxShadow: "0 0 0 6px rgba(255,255,255,.5), 0 0 26px #FF5A1F" });
  F((t) => {
    const p = P * prog(t, 0.5, 2.1, "out");
    arc.style.strokeDashoffset = (C * (1 - p)).toFixed(1);
    arc.style.opacity = t < 0.5 ? 0 : 1;
    tr.style.opacity = prog(t, 0.2, 0.5).toFixed(3);
    const a = -Math.PI / 2 + p * 2 * Math.PI;
    Object.assign(head.style, { left: (cx + R * Math.cos(a) - 17).toFixed(1) + "px", top: (cy + R * Math.sin(a) - 17).toFixed(1) + "px", opacity: t < 0.55 ? 0 : 1, transform: `scale(${(1 + 0.12 * Math.sin(t * 6)).toFixed(3)})` });
  });
  const mid = el(null, "abs center", { left: cx - 250 + "px", top: cy - 110 + "px", width: "500px", height: "220px", color: "#1B0903" });
  const v = el(mid, "num", { fontSize: "190px", fontWeight: 900, letterSpacing: "-.05em", lineHeight: 1 }, "0");
  el(mid, "", { fontSize: "96px", fontWeight: 900, color: "#FF5A1F", marginLeft: "6px", alignSelf: "flex-start", marginTop: "30px" }, "%");
  count(v, 0.5, 2.1, 0, 80);
  const lb = W(null, 0, 760, 1920, 80);
  el(lb, "abs center caps", { inset: 0, gap: "22px", fontSize: "64px", fontWeight: 900, letterSpacing: ".02em", color: "#FF5A1F" }, 'Signal <span style="font-size:36px;font-weight:600;color:#8c7f78;text-transform:none;letter-spacing:0">the rest is noise</span>');
  neo(lb, 1.9, { dist: 40 });
  [["#FF5A1F", "Signal 80%", 700], ["#c9b6aa", "Noise 20%", 980]].forEach(([c, tx, x], i) => {
    const p = W(null, x, 870, 240, 70);
    el(p, "abs row m-paper", { inset: 0, borderRadius: "35px", justifyContent: "center", gap: "12px", fontSize: "30px", fontWeight: 750, color: "#1B0903", boxShadow: "0 12px 28px rgba(120,50,20,.14)" }, `<i style="width:18px;height:18px;border-radius:50%;background:${c};display:block"></i>${tx}`);
    neo(p, 2.3 + i * 0.15, { dist: 30, blur: 8 });
  });
});

D("O06", {
  name: "Avatar row, YOU in the middle", cat: "circle", loop: 6.2,
  use: "<b>“You vs everyone else”, “one of them is you”.</b> A row of grey people; the middle one grows, turns white with an orange ring, gets the label, and pulses.",
  ref: { id: "I45", label: "Visual Inspo #45 · Andy Stauring's editor" },
  recipe: ["#2d2c2b", "#ffffff", "#FF5A1F", "#8C8C8C"],
  fusion: "Five Ellipses (glass) with a person icon; the middle one gets a white fill Merge + orange Border + NeoGlow, Size 1 → 1.35 on a spring; the rest Brightness down. Ripple: Ellipse outline loop.",
}, (S) => {
  const { el, W, A, F, pop, icon, prog } = S;
  S.ground("aroll");
  const xs = [560, 760, 960, 1160, 1360], y = 840, D0 = 150;
  const order = [2, 1, 3, 0, 4];
  xs.forEach((x, i) => {
    const w = W(null, x - D0 / 2, y - D0 / 2, D0, D0);
    el(w, "abs center m-dark", { inset: 0, borderRadius: "50%" }, icon("user", 76, "rgba(255,255,255,.9)", 2));
    const t0 = 0.3 + order.indexOf(i) * 0.1;
    if (i === 2) {
      const on = el(w, "abs center m-paper", { inset: 0, borderRadius: "50%", boxShadow: "0 0 0 7px #FF5A1F, 0 0 40px rgba(255,90,31,.7), 0 18px 40px rgba(0,0,0,.4)" }, icon("user", 80, "#FF5A1F", 2.2));
      F((t) => { on.style.opacity = prog(t, 1.4, 1.7).toFixed(3); });
      A(w, { s: [[t0, 0.3], [t0 + 0.5, 1, "back2"], [1.4, 1], [1.95, 1.38, "spring"]], o: [[t0, 0], [t0 + 0.15, 1, "out"]] });
      const rp = el(null, "abs", { borderRadius: "50%", border: "3px solid rgba(255,90,31,.9)" });
      F((t) => { const q = t < 2.0 ? 0 : ((t - 2.0) % 1.2) / 1.2, d = 210 + q * 180; Object.assign(rp.style, { width: d + "px", height: d + "px", left: x - d / 2 + "px", top: y - d / 2 + "px", opacity: t < 2.0 ? 0 : ((1 - q) * 0.9).toFixed(3) }); });
    } else {
      A(w, { s: [[t0, 0.3], [t0 + 0.5, 1, "back2"], [1.4, 1], [1.9, 0.86, "out"]], o: [[t0, 0], [t0 + 0.15, 1, "out"]], br: [[1.4, 1], [1.9, 0.5]] });
    }
  });
  const yo = W(null, 960 - 90, y + 88, 180, 70);
  el(yo, "abs center m-ember caps", { inset: 0, borderRadius: "35px", fontSize: "38px", fontWeight: 900, letterSpacing: ".14em", boxShadow: "0 0 0 4px rgba(255,255,255,.95), 0 12px 30px rgba(0,0,0,.4)" }, "You");
  pop(yo, 1.85, { s0: 0.3, ease: "back2" });
});

D("O07", {
  name: "Venn, the overlap is the answer", cat: "circle", loop: 6.2,
  use: "<b>Where two things meet</b>: who's buying × who you can help = your list. Full orange ground, white outlines, and the overlap fills dark with the answer in it.",
  ref: { web: "Web · classic explainer Venn, rebuilt in our colours" },
  recipe: ["#FF5A1F", "#ffffff", "#1B0903", "#FD9457"],
  fusion: "Orange Background; two Ellipse outlines (white) with a faint white fill. Overlap: Ellipse A masked by Ellipse B (mask Paint mode Multiply), dark fill, Size from 0.3 on a back spline.",
}, (S) => {
  const { el, W, A, neo, pop } = S;
  S.ground("ember");
  const svg = S.svg();
  svg.innerHTML = `<defs><clipPath id="o07c"><circle cx="1160" cy="540" r="300"/></clipPath></defs>`;
  const fa = S.node(svg, "circle", { cx: 760, cy: 540, r: 300, fill: "rgba(255,255,255,.12)", stroke: "none" });
  const fb = S.node(svg, "circle", { cx: 1160, cy: 540, r: 300, fill: "rgba(255,255,255,.12)", stroke: "none" });
  const lens = S.node(svg, "circle", { cx: 760, cy: 540, r: 300, fill: "#1B0903", "clip-path": "url(#o07c)" });
  const sa = S.node(svg, "circle", { cx: 760, cy: 540, r: 300, fill: "none", stroke: "#fff", "stroke-width": 7, transform: "rotate(-150 760 540)" });
  const sb = S.node(svg, "circle", { cx: 1160, cy: 540, r: 300, fill: "none", stroke: "#fff", "stroke-width": 7, transform: "rotate(-30 1160 540)" });
  S.drawOn(sa, 0.3, 1.05, "io"); S.drawOn(sb, 0.7, 1.45, "io");
  S.fade(fa, 0.8, 0.5); S.fade(fb, 1.2, 0.5);
  lens.style.transformOrigin = "960px 540px";
  A(lens, { s: [[1.9, 0.3], [2.35, 1, "back"]], o: [[1.9, 0], [2.05, 1, "out"]] });
  const la = W(null, 470, 470, 330, 140);
  el(la, "abs center caps", { inset: 0, fontSize: "50px", fontWeight: 900, lineHeight: 1.02, textAlign: "center", letterSpacing: "-.005em" }, "Who's<br>buying");
  const lb = W(null, 1120, 470, 330, 140);
  el(lb, "abs center caps", { inset: 0, fontSize: "50px", fontWeight: 900, lineHeight: 1.02, textAlign: "center", letterSpacing: "-.005em" }, "Who you<br>can help");
  neo(la, 1.0, { dist: 40 }); neo(lb, 1.4, { dist: 40 });
  const lc = W(null, 880, 480, 160, 120);
  el(lc, "abs center caps", { inset: 0, fontSize: "40px", fontWeight: 900, lineHeight: 1.02, textAlign: "center", color: "#FD9457" }, "Your<br>list");
  pop(lc, 2.2, { s0: 0.3, ease: "back2" });
});

D("O08", {
  name: "Rotating seal stamp", cat: "circle", loop: 6.2,
  use: "<b>A stamp of proof</b>: tested, verified, guaranteed, new. It slams onto a paper ground, the frame shakes, and the text ring keeps rotating.",
  ref: { web: "Web · rotating text-badge trend" },
  recipe: ["#BE4117", "#FFD2B8", "#ffffff", "#FFE9DC"],
  fusion: "Star Polygon (40 points) with a deep-orange gradient; Text+ on a circular path (Follower / Text+ Layout: Circle) rotating; white Ellipse + check. Slam: Size 2.3 → 1 in 5 frames + Shake modifier.",
}, (S) => {
  const { el, W, A, F, neo, hash, prog, ripple, burst } = S;
  S.ground("cream", { grid: true });
  const sz = 480, c = sz / 2;
  const seal = W(null, 960 - c, 440 - c, sz, sz);
  const pts = Array.from({ length: 80 }, (_, i) => { const a = (i / 80) * Math.PI * 2, r = i % 2 ? 220 : 238; return `${(c + r * Math.cos(a)).toFixed(1)},${(c + r * Math.sin(a)).toFixed(1)}`; }).join(" ");
  seal.innerHTML = `<svg width="${sz}" height="${sz}" viewBox="0 0 ${sz} ${sz}" style="overflow:visible;filter:drop-shadow(0 22px 34px rgba(120,40,0,.35))">
    <defs><linearGradient id="o08g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4561F"/><stop offset=".55" stop-color="#BE4117"/><stop offset="1" stop-color="#7A2A0E"/></linearGradient>
    <path id="o08p" d="M${c},${c} m-176,0 a176,176 0 1,1 352,0 a176,176 0 1,1 -352,0"/></defs>
    <polygon points="${pts}" fill="url(#o08g)"/>
    <circle cx="${c}" cy="${c}" r="206" fill="none" stroke="rgba(255,210,184,.55)" stroke-width="2.5"/>
    <circle cx="${c}" cy="${c}" r="146" fill="none" stroke="rgba(255,210,184,.55)" stroke-width="2.5"/>
    <g class="txt" style="transform-origin:${c}px ${c}px"><text font-family="Geist, sans-serif" font-size="34" font-weight="800" fill="#FFE3D2" letter-spacing="4"><textPath href="#o08p" textLength="1090" lengthAdjust="spacing">TESTED • PROVEN • TESTED • PROVEN •</textPath></text></g>
    <circle cx="${c}" cy="${c}" r="120" fill="#fff"/>
    <path d="M${c - 52} ${c + 4} l36 36 l72 -80" fill="none" stroke="#FF5A1F" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const tg = seal.querySelector(".txt");
  F((t) => { tg.style.transform = `rotate(${(t * 28).toFixed(2)}deg)`; });
  A(seal, { s: [[0.5, 2.3], [0.72, 1, "in"], [0.8, 1.04, "out"], [0.9, 1, "out"]], rz: [[0.5, 28], [0.72, -4, "in"], [0.9, 0, "out"]], o: [[0.5, 0], [0.56, 1, "out"]], blur: [[0.5, 10], [0.7, 0, "out"]] });
  ripple(null, 960, 440, 470, 0.72, "rgba(190,65,23,.55)", 0.8);
  burst(null, 960, 440, 0.72, 14, ["#BE4117", "#FD9457", "#1B0903"], 300);
  F((t) => { const k = t > 0.72 && t < 0.98 ? (1 - (t - 0.72) / 0.26) * 14 : 0; S.root.style.translate = k ? `${((hash(Math.floor(t * 70)) - 0.5) * k).toFixed(1)}px ${((hash(Math.floor(t * 70) + 5) - 0.5) * k).toFixed(1)}px` : ""; });
  const lb = W(null, 960 - 210, 740, 420, 84);
  el(lb, "abs center caps", { inset: 0, borderRadius: "42px", background: "linear-gradient(180deg,#3A1508,#1B0903)", color: "#fff", fontSize: "34px", fontWeight: 850, letterSpacing: ".1em", boxShadow: "0 16px 36px rgba(120,40,0,.3)" }, "Signal checked");
  neo(lb, 1.2, { dist: 40 });
});

D("O09", {
  name: "Hand-drawn marker circle", cat: "circle", loop: 6.2,
  use: "<b>Emphasis on one word or number</b> on the A-roll. An orange marker loop circles it, an arrow scribbles off to a note. The strokes “boil” like frame-by-frame drawing, the 2026 hand-made look.",
  ref: { id: "B27", label: "Web · 2026 hand-drawn trend · best editor 27 arrow" },
  recipe: ["#FF5A1F", "#ffffff", "#FD9457"],
  fusion: "Polyline loop with Write-On + a Displace driven by a stepped noise (hold every 3 frames) for the boil; NeoGlow soft. Arrow: second Polyline. Note: Text+ rotated −4°.",
}, (S) => {
  const { el, W, F, neo, rough, hash } = S;
  S.ground("aroll");
  const tx = W(null, 1150, 186, 660, 140);
  const line = el(tx, "abs row caps tshadow", { left: 0, top: 0, gap: "30px", fontSize: "108px", fontWeight: 900, letterSpacing: "-.02em", whiteSpace: "nowrap" });
  ["This", "week"].forEach((w, i) => { const s = el(line, "fx", { display: "inline-block" }, w); neo(s, 0.3 + i * 0.12, { dist: 60 }); });
  const svg = S.svg();
  svg.style.filter = "drop-shadow(0 0 10px rgba(255,90,31,.55)) drop-shadow(0 4px 10px rgba(0,0,0,.35))";
  const loop = S.path(svg, rough(1478, 252, 372, 112, 1), { color: "#FF5A1F", width: 13 });
  const arrow = S.path(svg, "", { color: "#FF5A1F", width: 11 });
  const head = S.path(svg, "", { color: "#FF5A1F", width: 11 });
  F((t) => {
    const f = Math.floor(t * 8);
    loop.setAttribute("d", rough(1478, 252, 372, 112, 1 + (f % 4)));
    const j = (k) => ((hash(f * 17 + k) - 0.5) * 6).toFixed(1);
    arrow.setAttribute("d", `M${1500 + +j(1)} ${378 + +j(2)} C ${1504 + +j(3)} ${430 + +j(4)}, ${1486 + +j(5)} ${470 + +j(6)}, ${1452 + +j(7)} ${506 + +j(8)}`);
    head.setAttribute("d", `M${1462 + +j(9)} ${474 + +j(10)} L${1450 + +j(11)} ${509 + +j(12)} L${1486 + +j(13)} ${506 + +j(14)}`);
  });
  S.drawOn(loop, 0.95, 1.6, "io"); S.drawOn(arrow, 1.7, 2.05, "io"); S.drawOn(head, 2.0, 2.15, "out");
  const nt = W(null, 1290, 520, 620, 80);
  const n = el(nt, "abs tshadow", { left: 0, top: 0, fontSize: "56px", fontWeight: 750, whiteSpace: "nowrap", transform: "rotate(-4deg)", letterSpacing: "-.01em" }, "");
  S.typeText(n, 2.2, 2.8, "timing is the signal");
});

D("O10", {
  name: "Social buttons: like, save, send", cat: "circle", loop: 6.2,
  use: "<b>Engagement and share moments</b>, or “people love this”. Round glass buttons pop in; the heart gets tapped, fills orange and bursts; save fills; send flies off and comes back.",
  ref: { id: "I20", label: "Visual Inspo #20 · Andy Stauring's editor" },
  recipe: ["#2d2c2b", "#FF5A1F", "#ffffff", "#FD9457"],
  fusion: "Three glass Ellipses with icons. Heart: second, filled icon scaled 0 → 1.3 → 1 + pEmitter burst. +1: Text+ moving up and fading. Send: Transform to the top-right, then back.",
}, (S) => {
  const { el, W, A, F, pop, icon, prog, burst, ripple } = S;
  S.ground("aroll");
  const y = 850, xs = [700, 960, 1220], D0 = 156;
  const btn = (x, i) => { const w = W(null, x - D0 / 2, y - D0 / 2, D0, D0); el(w, "abs m-dark", { inset: 0, borderRadius: "50%" }); pop(w, 0.3 + i * 0.15, { s0: 0.3, ease: "back2" }); return w; };
  const hb = btn(xs[0], 0), bb = btn(xs[1], 1), sb = btn(xs[2], 2);
  el(hb, "abs center", { inset: 0 }, icon("heart", 76, "#fff", 2.2));
  const hf = W(hb, 0, 0, D0, D0); el(hf, "abs center", { inset: 0 }, icon("heart", 76, "#FF5A1F", 2.2, "#FF5A1F"));
  A(hf, { s: [[1.35, 0], [1.55, 1.35, "out"], [1.8, 1, "back"]], o: [[1.34, 0], [1.35, 1]] });
  F((t) => { hb.firstChild.style.boxShadow = t > 1.4 ? `0 0 0 4px rgba(255,90,31,${(0.9 * prog(t, 1.4, 1.6)).toFixed(3)}), 0 0 36px rgba(255,90,31,${(0.5 * prog(t, 1.4, 1.6)).toFixed(3)})` : ""; });
  ripple(null, xs[0], y, 150, 1.3, "rgba(255,255,255,.9)", 0.5);
  burst(null, xs[0], y, 1.42, 12, ["#FF5A1F", "#FD9457", "#fff"], 150);
  const pl = W(null, xs[0] - 50, y - 150, 100, 60);
  el(pl, "abs center", { inset: 0, fontSize: "46px", fontWeight: 900, color: "#FD9457", textShadow: "0 4px 12px rgba(0,0,0,.4)" }, "+1");
  A(pl, { y: [[1.45, 30], [2.3, -90, "out"]], o: [[1.45, 0], [1.6, 1], [2.1, 1], [2.3, 0]] });
  el(bb, "abs center", { inset: 0 }, icon("bookmark", 70, "#fff", 2.2));
  const bf = W(bb, 0, 0, D0, D0); el(bf, "abs center", { inset: 0 }, icon("bookmark", 70, "#fff", 2.2, "#fff"));
  A(bf, { s: [[2.2, 0], [2.4, 1.25, "out"], [2.6, 1, "back"]], o: [[2.19, 0], [2.2, 1]] });
  const sw = W(sb, 0, 0, D0, D0); el(sw, "abs center", { inset: 0 }, icon("send", 68, "#fff", 2.2));
  A(sw, { x: [[2.8, 0], [3.15, 240, "in"], [3.16, -60], [3.55, 0, "back"]], y: [[2.8, 0], [3.15, -240, "in"], [3.16, 60], [3.55, 0, "back"]], o: [[2.8, 1], [3.1, 0], [3.16, 0], [3.35, 1]], s: [[2.8, 1], [3.15, 0.6], [3.16, 0.6], [3.55, 1, "back"]] });
});
