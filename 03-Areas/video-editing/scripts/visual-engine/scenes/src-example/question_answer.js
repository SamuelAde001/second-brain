// B24 4926-5039 "Start with a question that your buyers actually care about, then build something that helps them answer it."
// House list style: A-roll shrinks into a bordered card at the top, numbered orange pills build below.
grounds("warm", { floor: true });
const svg = svgLayer();
// A-roll card (lip-synced frames)
const ar = W(stage, 560, 60, 800, 450);
const as = el(ar, "abs shadow", { inset: 0 });
const ac = el(as, "card", { inset: 0, borderRadius: "30px", border: "3px solid #FF5A1F", boxShadow: "0 0 34px rgba(255,90,31,.55)" });
arollImg(ac, { inset: 0, width: "100%", height: "100%", borderRadius: "27px" });
A(ar, { s: [[0, 2.4], [0.7, 1, "expo"]], y: [[0, 260], [0.7, 0, "expo"]] });
// dashed connector
const cn = path(svg, "M960 515 L960 900", { color: "rgba(255,255,255,.55)", width: 3, dash: "7 11", glow: false });
cn.style.opacity = 0; F((t) => { cn.style.opacity = prog(t, 0.6, 0.9); });
// pills
function pill(y, n, text, ic, t0, blurUntil) {
  const w = W(stage, 530, y, 860, 118);
  const s = el(w, "abs shadow", { inset: 0 });
  const p = el(s, "pill orangefill bevel", { position: "absolute", inset: 0, height: "118px", borderRadius: "28px" });
  el(p, "num", { fontSize: "150px" }, n);
  el(p, "ibox", { width: "74px", height: "74px", background: "rgba(255,255,255,.2)", color: "#fff" }, icon(ic, 44, "#fff"));
  el(p, "txt", { fontSize: "44px" }, text);
  addSweep(p);
  neo(w, t0, { dist: 80 });
  if (blurUntil) A(w, { blur: [[t0, 16], [t0 + 0.4, 8], [blurUntil, 8], [blurUntil + 0.35, 0, "out"]], br: [[t0, 0.6], [blurUntil, 0.6], [blurUntil + 0.35, 1, "out"]] });
  sweep(p, (blurUntil || t0) + 0.4, 0.9);
  return w;
}
pill(560, "1", "Their question", "question", T(4940));
pill(720, "2", "Your answer", "verify", T(4960), T(4995));
vignette();
