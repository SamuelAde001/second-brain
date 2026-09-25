// Shared builders for Route Rise #3 scenes.
const AROLL_STILL = "../_assets/aroll_ref_0330.jpg";
const SHOT = (n) => `../_assets/tella/screen/tella_${n}_scr.jpg`;

function grounds(kind, opt) {
  opt = opt || {};
  el(stage, "ground " + kind);
  if (opt.grid !== false) el(stage, kind === "cream" || kind === "light" ? "grid dark" : "grid");
  if (opt.floor) el(stage, "floor");
}
function vignette(soft) { return el(stage, "vignette" + (soft ? " soft" : "")); }

// blurred photo/screenshot ground (depth of field)
function photoGround(src, opt) {
  opt = opt || {};
  const w = W(stage, -60, -60, 2040, 1200);
  el(w, "shot", { inset: 0, backgroundImage: img(src), backgroundPosition: opt.pos || "center", filter: `blur(${opt.blur == null ? 18 : opt.blur}px) brightness(${opt.br == null ? 0.45 : opt.br}) saturate(${opt.sat == null ? 1 : opt.sat})` });
  if (opt.tint) el(w, "abs", { inset: 0, background: opt.tint });
  return w;
}

// two-tone title, each word slides up (NeoAnim) with a stagger
function title2(parent, x, y, words, accent, t0, opt) {
  opt = opt || {};
  const box = W(parent, x, y, opt.w || null, null, { whiteSpace: "nowrap" });
  const size = opt.size || 92;
  const ws = [];
  words.forEach((w, i) => {
    const s = el(box, "", { display: "inline-block", marginRight: (size * 0.24) + "px", fontWeight: 850, fontSize: size + "px", lineHeight: 1, textTransform: "uppercase", letterSpacing: "-.01em", color: accent.includes(i) ? "var(--acc)" : (opt.ink || "#fff") }, w);
    if (accent.includes(i) && opt.glow !== false) s.classList.add("tglow");
    const tt = Array.isArray(t0) ? t0[i] : t0 + i * (opt.stagger || 0.09);
    neo(s, tt, { dist: size * 0.7, blur: 18 });
    ws.push(s);
  });
  if (opt.center) box.style.transform = "translateX(-50%)", A(box, {}, "translateX(-50%)");
  return { box, ws };
}

// chip with icon: returns wrapper
function chip(parent, x, y, text, o) {
  o = o || {};
  const w = W(parent, x, y);
  const c = el(w, "chip " + (o.cls || "glass dark bevel"), Object.assign({ position: "relative", color: o.color || "#fff", fontSize: (o.size || 26) + "px" }, o.style || {}));
  if (o.icon) el(c, "ibox", { width: (o.size || 26) * 1.7 + "px", height: (o.size || 26) * 1.7 + "px", background: o.ibg || "rgba(255,90,31,.16)", borderRadius: "12px" }, icon(o.icon, (o.size || 26) * 1.05, o.icol || "var(--acc)"));
  if (o.dot) el(c, "dot", { background: o.dot, boxShadow: `0 0 10px ${o.dot}` });
  el(c, "", {}, text);
  if (o.sweep) addSweep(c);
  if (o.shadow !== false) w.classList.add("shadow");
  return w;
}

// macOS window with title bar; returns {w, body}
function macWin(parent, x, y, wd, ht, url, o) {
  o = o || {};
  const w = W(parent, x, y, wd, ht);
  const sh = el(w, "abs shadow", { inset: 0 });
  const win = el(sh, "win", { inset: 0, background: o.bg || "#fff", color: o.fg || "#1d1d1f" });
  const bar = el(win, "bar", o.barBg ? { background: o.barBg, borderBottom: "1px solid rgba(255,255,255,.06)" } : {}, `<i></i><i></i><i></i>` + (url != null ? `<div class="url" style="${o.urlStyle || ""}">${url}</div>` : ""));
  const body = el(win, "abs", { left: 0, right: 0, top: "44px", bottom: 0, overflow: "hidden" });
  return { w, win, body };
}

// generic avatar circle with a person silhouette
function avatar(parent, x, y, size, color, o) {
  o = o || {};
  const w = W(parent, x, y, size, size);
  el(w, "abs", { inset: 0, borderRadius: "50%", background: o.bg || `linear-gradient(160deg, ${color || "#FF7A3D"}, ${o.bg2 || "#b8330a"})`, border: o.ring ? `3px solid ${o.ring}` : "none", display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden", boxShadow: "inset 0 2px 0 rgba(255,255,255,.35)" },
    `<svg width="${size * 0.72}" height="${size * 0.72}" viewBox="0 0 24 24" style="margin-top:${size * 0.18}px"><circle cx="12" cy="8" r="4.6" fill="rgba(255,255,255,.92)"/><path d="M2.5 23c0-5.6 4.3-9.2 9.5-9.2s9.5 3.6 9.5 9.2z" fill="rgba(255,255,255,.92)"/></svg>`);
  return w;
}

// SVG layer for lines/streams
function svgLayer(parent) {
  const d = el(parent || stage, "abs", { left: 0, top: 0, width: "1920px", height: "1080px" });
  d.innerHTML = `<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;inset:0;overflow:visible"><defs>
    <filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs></svg>`;
  return d.querySelector("svg");
}
function path(svg, d, o) {
  o = o || {};
  const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
  p.setAttribute("d", d);
  p.setAttribute("fill", "none");
  p.setAttribute("stroke", o.color || "#FF5A1F");
  p.setAttribute("stroke-width", o.width || 3);
  p.setAttribute("stroke-linecap", "round");
  if (o.glow !== false) p.setAttribute("filter", "url(#gl)");
  if (o.dash) p.setAttribute("stroke-dasharray", o.dash);
  svg.appendChild(p);
  return p;
}
// draw a path on over [t0, t1]
function drawOn(p, t0, t1, ease) {
  const L = p.getTotalLength();
  const dash = p.getAttribute("stroke-dasharray");
  if (!dash) { p.style.strokeDasharray = L; }
  F((t) => {
    const k = prog(t, t0, t1, ease || "out");
    if (!dash) p.style.strokeDashoffset = L * (1 - k);
    else p.style.opacity = k;
  });
}
// flowing dashes along a path (data stream)
function flow(p, t0, speed) {
  p.setAttribute("stroke-dasharray", "10 26");
  F((t) => { p.style.strokeDashoffset = -(Math.max(0, t - t0)) * (speed || 220); });
}

// mark icons for ✓ ✕ ! as inline svg
const SVG_TICK = (c, s) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="${c || "#fff"}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const SVG_X = (c, s) => `<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="${c || "#fff"}" stroke-width="3.2" stroke-linecap="round"/></svg>`;
function badge(parent, x, y, size, kind) {
  const w = W(parent, x, y, size, size);
  const col = kind === "good" ? ["#6be39f", "#22a45a"] : kind === "bad" ? ["#ff7a70", "#c9281f"] : ["#ffc56b", "#d98a12"];
  el(w, "abs " + (kind === "good" ? "glow-good" : kind === "bad" ? "glow-bad" : ""), { inset: 0, borderRadius: "50%", background: `radial-gradient(circle at 35% 30%, ${col[0]}, ${col[1]})`, display: "flex", alignItems: "center", justifyContent: "center" }, kind === "good" ? SVG_TICK("#fff", size * 0.55) : kind === "bad" ? SVG_X("#fff", size * 0.5) : `<b style="font-size:${size * 0.6}px;color:#fff;font-weight:900">!</b>`);
  return w;
}
// spinner
function spinner(parent, x, y, size, color) {
  const w = W(parent, x, y, size, size);
  const s = el(w, "abs", { inset: 0, borderRadius: "50%", border: `${size * 0.12}px solid rgba(255,255,255,.15)`, borderTopColor: color || "var(--acc)" });
  F((t) => { s.style.transform = `rotate(${t * 540}deg)`; });
  return w;
}
