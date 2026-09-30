// Parts: the approved gallery vocabulary as building blocks for real job visuals (remix them, don't copy the gallery).
// Every part takes the scene API S from gallery-engine.js. Coordinates are px on the 1920x1080 stage, or inside `parent`.
(function () {
  const P = { _n: 0 };
  const FILL = { paper: "m-paper", ember: "m-ember", deep: "m-deep", dark: "m-dark", glass: "m-glass", cream: "m-cream", peach: "m-peach", grey: "m-grey", light: "m-light", black: "m-black" };
  P.fill = (f) => FILL[f] || f || "";
  const uid = (p) => (p || "p") + ++P._n;

  // logos: ASSETS.logos[key] (png favicon or svg). Drawn on a white tile unless o.bare.
  P.logo = (key, size, o) => {
    o = o || {};
    const src = window.ASSETS && window.ASSETS.logos && window.ASSETS.logos[key];
    const r = o.round ? "50%" : Math.round(size * 0.24) + "px";
    if (!src) return `<span class="center" style="width:${size}px;height:${size}px;border-radius:${r};background:#fff;color:#1B0903;font-weight:900;font-size:${Math.round(size * 0.46)}px;flex:none">${(o.alt || key || "?").slice(0, 1).toUpperCase()}</span>`;
    const pad = o.bare ? 0 : Math.round(size * (o.pad == null ? 0.16 : o.pad));
    return `<span class="center" style="width:${size}px;height:${size}px;border-radius:${r};background:${o.bare ? "transparent" : o.bg || "#fff"};flex:none;box-shadow:${o.bare ? "none" : "0 6px 16px rgba(0,0,0,.28)"}"><img src="${src}" style="width:${size - 2 * pad}px;height:${size - 2 * pad}px;object-fit:contain;display:block"></span>`;
  };

  // entrance: 'neo' (NeoAnim slide, ang = side it comes from), 'pop', 'fade', 'wipe' (clip from the left), 'none'
  P.enter = (S, node, t0, how, o) => {
    o = o || {};
    if (t0 == null || how === "none") return node;
    if (how === "pop") return S.pop(node, t0, { s0: o.s0 == null ? 0.4 : o.s0, dur: o.dur || 0.5, ease: o.ease || "back" });
    if (how === "fade") return S.fade(node, t0, o.dur || 0.4);
    return S.neo(node, t0, { ang: o.ang == null ? -90 : o.ang, dist: o.dist == null ? 60 : o.dist, blur: o.blur, s0: o.s0 });
  };
  const anchorBase = (a) => (a === "center" ? "translate(-50%,-50%)" : a === "right" ? "translate(-100%,0)" : a === "mid" ? "translate(0,-50%)" : a === "top" ? "translate(-50%,0)" : "");

  // pill: {x,y,h,html,fill,font,weight,caps,icon,iconColor,iconBg,iconFill,logo,anchor,t0,enter,ang,dist,sweep,glow,w,radius,pad}
  P.pill = (S, parent, o) => {
    const h = o.h || 96, font = o.font || Math.round(h * 0.4), ic = Math.round(h * 0.68);
    const w = S.W(parent, o.x, o.y, o.w || null, h);
    if (o.anchor) S.A(w, {}, anchorBase(o.anchor));
    let lead = "";
    if (o.logo) lead = P.logo(o.logo, ic, { round: true, pad: 0.2 });
    else if (o.icon) lead = `<span class="center" style="width:${ic}px;height:${ic}px;border-radius:50%;background:${o.iconBg || "rgba(255,255,255,.16)"};flex:none">${S.icon(o.icon, Math.round(ic * 0.56), o.iconColor || "#fff", 2.3, o.iconFill)}</span>`;
    const st = { position: "relative", height: h + "px", borderRadius: (o.radius == null ? h / 2 : o.radius) + "px", padding: o.pad || (lead ? `0 ${Math.round(h * 0.4)}px 0 ${Math.round((h - ic) / 2)}px` : `0 ${Math.round(h * 0.44)}px`), gap: Math.round(h * 0.2) + "px", fontSize: font + "px", fontWeight: o.weight || 800, letterSpacing: o.caps === false ? "-.01em" : ".01em", whiteSpace: "nowrap", justifyContent: o.center || (o.w && !lead) ? "center" : "flex-start" };
    if (o.w) st.width = "100%";
    if (o.glow) st.boxShadow = "0 0 40px rgba(255,90,31,.55), inset 0 2px 0 rgba(255,222,204,.6)";
    const b = S.el(w, "row clip " + P.fill(o.fill || "dark") + (o.caps === false ? "" : " caps"), st, lead + `<span>${o.html}</span>`);
    P.enter(S, w, o.t0, o.enter || "neo", o);
    if (o.sweep != null) { S.addSweep(b); S.sweep(b, o.sweep, 0.9); }
    return { w, b };
  };

  // round badge with an icon: kind check | alert | question | x
  P.badge = (S, parent, x, y, kind, size, t0, o) => {
    o = o || {};
    const C = { check: ["#fff", "#FF5A1F", "#FF5A1F"], alert: ["#FF5A1F", "#fff", "rgba(255,255,255,.95)"], question: ["#2A2A2A", "#fff", "rgba(255,255,255,.95)"], x: ["#2A2A2A", "#d6d6d6", "#4a4a4a"] }[kind];
    const w = S.W(parent, x - size / 2, y - size / 2, size, size);
    S.el(w, "abs center", { inset: 0, borderRadius: "50%", background: C[0], boxShadow: `0 0 0 ${Math.max(3, Math.round(size * 0.06))}px ${C[2]}, 0 10px 24px rgba(0,0,0,.4)` }, S.icon(kind, Math.round(size * 0.56), C[1], 3.2));
    S.pop(w, t0, { s0: 0, ease: "back2", blur: 0, dur: 0.45 });
    if (o.ripple !== false) S.ripple(parent, x, y, size, t0 + 0.08, kind === "check" ? "#FF5A1F" : "rgba(255,255,255,.8)");
    return w;
  };

  // small status tag that drops in (hangs off a pill or a card): {fill, kind, t0}
  P.tag = (S, parent, x, y, html, o) => {
    o = o || {};
    const K = { check: ["#fff", "#FF5A1F"], alert: ["#FF5A1F", "#fff"], question: ["#fff", "#1B0903"], x: ["#474747", "#e0e0e0"], clock: ["#fff", "#FF5A1F"], bolt: ["#fff", "#FF5A1F"] }[o.kind || "check"];
    const w = S.W(parent, x, y, null, 62);
    if (o.anchor) S.A(w, {}, anchorBase(o.anchor));
    S.el(w, "row caps " + P.fill(o.fill || "grey"), { height: "62px", borderRadius: "31px", padding: "0 24px 0 9px", gap: "12px", fontSize: (o.font || 24) + "px", fontWeight: 800, letterSpacing: ".06em", whiteSpace: "nowrap" },
      `<span class="center" style="width:44px;height:44px;border-radius:50%;background:${K[0]};flex:none">${S.icon(o.kind || "check", 28, K[1], 3)}</span>${html}`);
    if (o.t0 != null) S.A(w, { y: [[o.t0, -30], [o.t0 + 0.45, 0, "back2"]], o: [[o.t0, 0], [o.t0 + 0.15, 1, "out"]] });
    return w;
  };

  // card: {x,y,w,h,fill,radius,t0,enter,ang,dist,rim} -> {w, c}
  P.card = (S, parent, o) => {
    const w = S.W(parent, o.x, o.y, o.w, o.h);
    if (o.anchor) S.A(w, {}, anchorBase(o.anchor));
    const c = S.el(w, "abs clip " + P.fill(o.fill || "dark"), { inset: 0, borderRadius: (o.radius == null ? 40 : o.radius) + "px" });
    if (o.rim) S.el(c, "abs", { left: "8%", right: "8%", top: 0, height: "2px", background: "linear-gradient(90deg, transparent, rgba(253,148,87,.95), transparent)" });
    P.enter(S, w, o.t0, o.enter || "neo", o);
    return { w, c };
  };

  // list row: {x,y,w,h,html,icon,iconColor,iconBg,num,fill,font,t0,enter,ang}
  P.row = (S, parent, o) => {
    const h = o.h || 110, ic = Math.round(h * 0.62);
    const w = S.W(parent, o.x, o.y, o.w, h);
    const r = S.el(w, "abs row " + P.fill(o.fill || "glass"), { inset: 0, borderRadius: (o.radius == null ? 28 : o.radius) + "px", padding: `0 ${o.num != null ? Math.round(h + 10) : 34}px 0 ${o.icon ? Math.round((h - ic) / 2) : 34}px`, gap: "20px", fontSize: (o.font || 40) + "px", fontWeight: o.weight || 700, whiteSpace: "nowrap" },
      (o.icon ? `<span class="center" style="width:${ic}px;height:${ic}px;border-radius:50%;background:${o.iconBg || "rgba(255,90,31,.18)"};flex:none">${S.icon(o.icon, Math.round(ic * 0.55), o.iconColor || "#FD9457", 2.3)}</span>` : "") + `<span>${o.html}</span>`);
    let nb = null;
    if (o.num != null) nb = S.el(w, "abs center num", { right: Math.round(h * 0.18) + "px", top: Math.round(h * 0.2) + "px", width: Math.round(h * 0.6) + "px", height: Math.round(h * 0.6) + "px", borderRadius: "50%", fontSize: Math.round(h * 0.28) + "px", fontWeight: 850, background: "#fff", color: "#1B0903" }, String(o.num));
    P.enter(S, w, o.t0, o.enter || "neo", o);
    return { w, r, nb };
  };

  // the GTM OS core (recurring motif): gradient ring that draws on and keeps turning, dark disc with a logo/label
  P.hub = (S, parent, o) => {
    const r = o.r || 200, id = uid("hub"), svg = S.svg(parent);
    svg.innerHTML = `<defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFD2B8"/><stop offset=".35" stop-color="#FF5A1F"/><stop offset=".7" stop-color="#7A2A0E"/><stop offset="1" stop-color="#FD9457"/></linearGradient></defs>`;
    svg.style.filter = "drop-shadow(0 0 22px rgba(255,90,31,.7))";
    const g = S.node(svg, "g", {});
    g.style.transformOrigin = `${o.cx}px ${o.cy}px`;
    const ring = S.node(g, "circle", { cx: o.cx, cy: o.cy, r, fill: "none", stroke: `url(#${id})`, "stroke-width": Math.round(r * 0.17), "stroke-linecap": "round" });
    S.F((t) => { g.style.transform = `rotate(${(t * (o.spin || 24) - 90).toFixed(2)}deg)`; });
    S.drawOn(ring, o.t0, o.t0 + (o.dur || 0.9), "io");
    const d = Math.round(r * 1.64);
    const disc = S.W(parent, o.cx - d / 2, o.cy - d / 2, d, d);
    let inner = "";
    if (o.logo) inner += P.logo(o.logo, Math.round(r * 0.44), { pad: 0.18 });
    else if (o.icon) inner += S.icon(o.icon, Math.round(r * 0.5), "#FF5A1F", 2.4);
    if (o.label) inner += `<span style="font-size:${Math.round(r * (o.labelSize || 0.17))}px;font-weight:900;letter-spacing:.05em;text-transform:uppercase;text-align:center;line-height:1.02">${o.label}</span>`;
    if (o.sub) inner += `<span style="font-size:${Math.round(r * 0.095)}px;font-weight:750;letter-spacing:.16em;color:#FD9457;text-transform:uppercase">${o.sub}</span>`;
    const face = S.el(disc, "abs center col", { inset: 0, borderRadius: "50%", background: "radial-gradient(circle at 50% 32%, #2c2b2b, #111 72%)", boxShadow: "inset 0 10px 30px rgba(0,0,0,.6), inset 0 -2px 0 rgba(255,255,255,.06)", gap: Math.round(r * 0.07) + "px" }, inner);
    S.pop(disc, o.t0 + 0.25, { s0: 0.6 });
    return { svg, ring, disc, face, r };
  };

  // his "Moving dashed line": revealed along its length, then the dashes keep flowing
  P.dash = (S, svg, d, o) => {
    o = o || {};
    const id = uid("m"), defs = S.node(svg, "defs", {});
    const mk = S.node(defs, "mask", { id, maskUnits: "userSpaceOnUse", x: -2000, y: -2000, width: 6000, height: 6000 });
    const mp = S.node(mk, "path", { d, fill: "none", stroke: "#fff", "stroke-width": (o.width || 3) + 10, "stroke-linecap": "round" });
    const p = S.path(svg, d, { color: o.color || "rgba(255,255,255,.8)", width: o.width || 3, dash: o.dash || "12 14", attrs: { mask: `url(#${id})` } });
    S.drawOn(mp, o.t0, o.t0 + (o.dur || 0.6), o.ease || "out");
    S.F((t) => { p.style.strokeDashoffset = (-t * (o.speed || 46)).toFixed(1); });
    return p;
  };

  // his "Arrowline": a curve that draws on, then its head appears along the end tangent
  P.arrow = (S, svg, d, o) => {
    o = o || {};
    const col = o.color || "#fff", wd = o.width || 4, dur = o.dur || 0.5;
    const p = S.path(svg, d, { color: col, width: wd });
    S.drawOn(p, o.t0, o.t0 + dur, o.ease || "io");
    const head = S.path(svg, "M0 0", { color: col, width: wd });
    let done = false;
    S.F((t) => {
      if (!done) {
        const L = p.getTotalLength(), a = p.getPointAtLength(L), b = p.getPointAtLength(Math.max(0, L - 8));
        const ang = Math.atan2(a.y - b.y, a.x - b.x), s = o.head || 18;
        const pt = (k) => `${(a.x - s * Math.cos(ang + k)).toFixed(1)} ${(a.y - s * Math.sin(ang + k)).toFixed(1)}`;
        head.setAttribute("d", `M${pt(0.55)} L${a.x.toFixed(1)} ${a.y.toFixed(1)} L${pt(-0.55)}`);
        done = true;
      }
      head.style.opacity = S.prog(t, o.t0 + dur * 0.85, o.t0 + dur + 0.05).toFixed(3);
    });
    return { p, head };
  };

  // two-tone title, *word* = orange with glow, each word NeoAnims in: {x,y,text,size,t0,stagger,anchor,color,accent,weight,caps}
  P.title = (S, parent, o) => {
    const box = S.W(parent, o.x, o.y, o.w || null, null, { whiteSpace: "nowrap" });
    if (o.anchor) S.A(box, {}, anchorBase(o.anchor));
    const size = o.size || 90;
    o.text.split(" ").forEach((wd, i) => {
      const acc = wd.includes("*");
      const s = S.el(box, "fx" + (acc && o.glow !== false ? " tglow" : ""), { display: "inline-block", marginRight: Math.round(size * 0.24) + "px", fontWeight: o.weight || 850, fontSize: size + "px", lineHeight: 1, textTransform: o.caps === false ? "none" : "uppercase", letterSpacing: "-.01em", color: acc ? o.accent || "#FF5A1F" : o.color || "#fff" }, wd.replace(/\*/g, ""));
      const tt = Array.isArray(o.t0) ? o.t0[i] : o.t0 + i * (o.stagger || 0.08);
      S.neo(s, tt, { dist: size * 0.7, blur: 18 });
    });
    return box;
  };

  // his "Down fade": dark gradient at the bottom for text-only beats on the A-roll
  P.downFade = (S, t0, h) => {
    const d = S.el(null, "abs", { left: 0, right: 0, bottom: 0, height: (h || 560) + "px", background: "linear-gradient(180deg, rgba(17,6,2,0) 0%, rgba(17,6,2,.72) 55%, rgba(17,6,2,.92) 100%)" });
    S.fade(d, t0 || 0, 0.5);
    return d;
  };

  // the build board (recurring motif): tabbed box, steps done get a tick, the indicator slides from `from` to `active`
  P.board = (S, o) => {
    const steps = o.steps || ["Define", "Connect", "Check", "Outreach"];
    const X = o.x == null ? 330 : o.x, Y = o.y == null ? 250 : o.y, BW = o.w || 1260, BH = o.h || 640, TW = o.tw || 280, GAP = o.tgap || 300;
    const t0 = o.t0 || 0;
    const tabs = steps.map((n, i) => {
      const w = S.W(null, X + 30 + i * GAP, Y - 92, TW, 104);
      const on = i === o.active, done = i < o.active;
      const b = S.el(w, "abs row caps", { inset: 0, borderRadius: "30px 30px 0 0", padding: "0 0 12px 24px", gap: "16px", fontSize: "30px", fontWeight: 800, letterSpacing: ".04em", background: on ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#2B2B2B", color: on ? "#fff" : done ? "#e8dcd5" : "#9a9a9a" });
      S.el(b, "center num", { width: "52px", height: "52px", borderRadius: "50%", fontSize: "26px", fontWeight: 850, background: on ? "#fff" : done ? "rgba(255,90,31,.2)" : "#3d3d3d", color: on ? "#FF5A1F" : "#bdbdbd", flex: "none" }, done ? S.icon("check", 28, "#FD9457", 3.2) : String(i + 1));
      S.el(b, "", {}, n);
      if (!o.static) S.neo(w, t0 + i * 0.06, { dist: 40, blur: 10 });
      return w;
    });
    const box = S.W(null, X, Y, BW, BH);
    S.el(box, "abs m-dark", { inset: 0, borderRadius: "36px", borderTopLeftRadius: "12px" });
    const ind = S.el(box, "abs", { top: 0, height: "5px", width: TW + "px", borderRadius: "3px", background: "linear-gradient(90deg,#FD9457,#FF5A1F)", boxShadow: "0 0 16px rgba(255,90,31,.8)" });
    const from = o.from == null ? o.active : o.from;
    S.F((t) => { ind.style.left = (30 + S.lerp(from, o.active, S.prog(t, t0 + 0.3, t0 + 0.8, "expo")) * GAP).toFixed(1) + "px"; });
    if (!o.static) S.A(box, { y: [[t0, 60], [t0 + 0.55, 0, "expo"]], o: [[t0, 0], [t0 + 0.25, 1, "out"]] });
    return { box, tabs, X, Y, BW, BH };
  };

  // chat bubble: {side:'l'|'r', x (left side) / right (right side), y, html, t0, maxw, font, fill}
  P.bubble = (S, parent, o) => {
    const b = S.el(parent, "abs fx", Object.assign({ top: o.y + "px", maxWidth: (o.maxw || 580) + "px", transformOrigin: o.side === "r" ? "100% 100%" : "0% 100%" }, o.side === "r" ? { right: (o.right || 36) + "px" } : { left: (o.x || 36) + "px" }));
    const me = o.side === "r";
    S.el(b, "", { padding: "22px 30px", borderRadius: me ? "34px 34px 10px 34px" : "34px 34px 34px 10px", background: o.bg || (me ? "linear-gradient(180deg,#FF8750,#FF5A1F)" : "#F1EAE5"), color: o.color || (me ? "#fff" : "#1B0903"), fontSize: (o.font || 34) + "px", fontWeight: 550, lineHeight: 1.26, boxShadow: me ? "0 10px 24px rgba(255,90,31,.25)" : "none" }, o.html);
    S.A(b, { s: [[o.t0, 0.5], [o.t0 + 0.4, 1, "back"]], o: [[o.t0, 0], [o.t0 + 0.12, 1, "out"]] });
    return b;
  };

  // hand-drawn marker loop that boils (redrawn with a new wobble ~8 times a second)
  P.marker = (S, svg, o) => {
    const loop = S.path(svg, S.rough(o.cx, o.cy, o.rx, o.ry, 1), { color: o.color || "#FF5A1F", width: o.width || 12 });
    S.F((t) => { loop.setAttribute("d", S.rough(o.cx, o.cy, o.rx, o.ry, 1 + (Math.floor(t * 8) % 4))); });
    S.drawOn(loop, o.t0, o.t0 + (o.dur || 0.6), "io");
    return loop;
  };
  // hand-drawn strike-through across a word or pill
  P.strike = (S, svg, o) => {
    const p = S.path(svg, "M0 0", { color: o.color || "#FF5A1F", width: o.width || 12 });
    S.F((t) => {
      const f = Math.floor(t * 8), j = (k) => ((S.hash(f * 13 + k) - 0.5) * 6).toFixed(1);
      p.setAttribute("d", `M${o.x1} ${o.y1 + +j(1)} C ${o.x1 + (o.x2 - o.x1) * 0.3} ${o.y1 - 10 + +j(2)}, ${o.x1 + (o.x2 - o.x1) * 0.7} ${o.y2 + 10 + +j(3)}, ${o.x2} ${o.y2 + +j(4)}`);
    });
    S.drawOn(p, o.t0, o.t0 + (o.dur || 0.35), "out");
    return p;
  };

  // a label over a big counting number: {x,y,label,from,to,fmt,t0,t1,size,color,labelColor,anchor}
  P.stat = (S, parent, o) => {
    const w = S.W(parent, o.x, o.y, null, null);
    if (o.anchor) S.A(w, {}, anchorBase(o.anchor));
    S.el(w, "caps", { fontSize: Math.round((o.size || 120) * 0.22) + "px", fontWeight: 800, letterSpacing: ".16em", color: o.labelColor || "#bdbdbd", whiteSpace: "nowrap" }, o.label);
    const n = S.el(w, "num" + (o.grad ? " gtext" : ""), { fontSize: (o.size || 120) + "px", fontWeight: 900, letterSpacing: "-.04em", lineHeight: 1.02, color: o.color || "#fff", whiteSpace: "nowrap" }, "0");
    S.count(n, o.t0, o.t1 || o.t0 + 1.2, o.from || 0, o.to, o.fmt);
    P.enter(S, w, o.t0 - 0.2, o.enter || "neo", o);
    return w;
  };

  window.PARTS = P;
  // job visuals register here: RV(code, meta, build)
  window.RVS = window.RVS || [];
  window.RV = (code, meta, build) => { window.RVS.push(Object.assign({ code, build }, meta)); };
})();
