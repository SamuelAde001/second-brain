// B07 1480-1664 "...find an email address and one provider can't find the email you need, you can have Clay check another provider based on the workflow you have configured."
photoGround(SHOT("000022"), { blur: 16, br: 0.3, pos: "50% 45%" });
const svg = svgLayer();
// email field
const fw = W(stage, 530, 110, 860, 116);
const fs = el(fw, "abs shadow", { inset: 0 });
const fc = el(fs, "card glass dark bevel", { inset: 0, borderRadius: "28px", display: "flex", alignItems: "center", gap: "22px", padding: "0 30px" });
el(fc, "ibox", { width: "68px", height: "68px", background: "rgba(255,90,31,.16)", color: "#FF5A1F" }, icon("email", 38));
const ft = el(fc, "mono", { fontSize: "40px", color: "rgba(255,255,255,.4)" }, "__________@northwind.io");
const fglow = el(fw, "abs", { inset: "-3px", borderRadius: "30px", border: "3px solid #3ED07E", boxShadow: "0 0 30px rgba(62,208,126,.7)" });
A(fglow, { o: 0 });
neo(fw, 0.05, { dist: 70 });
const fb = badge(fw, 776, 26, 64, "good");
A(fb, { o: 0 });
// providers in the workflow order
const P = [[330, 330], [700, 510], [1070, 690]].map((p, i) => {
  const w = W(stage, p[0], p[1], 520, 124);
  const s = el(w, "abs shadow", { inset: 0 });
  el(s, "card glass dark bevel", { inset: 0, borderRadius: "28px", display: "flex", alignItems: "center", gap: "22px", padding: "0 28px" },
    `<div style="width:62px;height:62px;border-radius:50%;background:linear-gradient(170deg,#fff,#e9e6e2);color:#FF5A1F;font-weight:900;font-size:34px;display:flex;align-items:center;justify-content:center">${i + 1}</div><div style="font-weight:800;font-size:30px;letter-spacing:.02em">PROVIDER ${i + 1}</div>`);
  const ring = el(w, "abs", { inset: "-3px", borderRadius: "30px", border: "3px solid transparent" });
  A(ring, { o: 0 });
  neo(w, 0.25 + i * 0.1, { dist: 60 });
  if (i < 2) path(svg, `M${p[0] + 440} ${p[1] + 124} C ${p[0] + 440} ${p[1] + 170}, ${p[0] + 420} ${p[1] + 180}, ${p[0] + 480} ${p[1] + 180}`, { color: "rgba(255,255,255,.35)", width: 3, dash: "6 10", glow: false });
  return { w, ring };
});
// provider 1: searches, misses
const sp1 = spinner(P[0].w, 430, 34, 56, "#FF5A1F");
A(sp1, { o: [[T(1531), 0], [T(1535), 1], [T(1562), 1], [T(1565), 0]] });
const x1 = badge(P[0].w, 426, 30, 64, "bad");
pop(x1, T(1564));
P[0].ring.style.borderColor = "#F0453A"; P[0].ring.style.boxShadow = "0 0 26px rgba(240,69,58,.6)";
A(P[0].ring, { o: [[T(1564), 0], [T(1568), 1]] });
A(P[0].w, { br: [[T(1575), 1], [T(1590), 0.6]] });
// the drop of light moves on to provider 2
const dp = W(stage, 0, 0, 30, 30);
el(dp, "abs glow-acc", { inset: 0, borderRadius: "50%", background: "radial-gradient(circle at 35% 30%, #ffd2b8, #FF5A1F)" });
A(dp, { x: [[T(1572), 770], [T(1586), 790, "io"]], y: [[T(1572), 454], [T(1586), 560, "io"]], o: [[T(1570), 0], [T(1573), 1], [T(1586), 1], [T(1590), 0]] });
// provider 2: searches, finds it
const sp2 = spinner(P[1].w, 430, 34, 56, "#FF5A1F");
A(sp2, { o: [[T(1586), 0], [T(1589), 1], [T(1612), 1], [T(1615), 0]] });
const ok2 = badge(P[1].w, 426, 30, 64, "good");
pop(ok2, T(1614));
P[1].ring.style.borderColor = "#3ED07E"; P[1].ring.style.boxShadow = "0 0 30px rgba(62,208,126,.7)";
A(P[1].ring, { o: [[T(1614), 0], [T(1618), 1]] });
// the found email flies up into the field
const em = chip(stage, 760, 560, "sarah.lee@northwind.io", { cls: "greenfill bevel", size: 26, style: { fontFamily: "Consolas,monospace", textTransform: "none" } });
A(em, { o: [[T(1616), 0], [T(1620), 1], [T(1640), 1], [T(1644), 0]], x: [[T(1620), 0], [T(1640), 20, "io"]], y: [[T(1620), 0], [T(1640), -410, "io"]], s: [[T(1616), 0.6], [T(1622), 1, "back"]] });
F((t) => { if (t > T(1640)) { ft.style.color = "#fff"; ft.textContent = "sarah.lee@northwind.io"; } else { ft.style.color = "rgba(255,255,255,.4)"; ft.textContent = "__________@northwind.io"; } });
A(fglow, { o: [[T(1640), 0], [T(1646), 1, "out"]] });
pop(fb, T(1642));
// provider 3 wasn't needed
A(P[2].w, { br: [[T(1630), 1], [T(1645), 0.45]] });
vignette();
