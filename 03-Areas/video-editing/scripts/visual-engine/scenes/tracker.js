// The 4-tool tracker: four glossy cards in a 3D row, each holding its tool's real UI.
// Used at every tool intro (adapted each time) and for the final recap.
const TOOLS = [
  { name: "Clay", shot: "../_assets/tella/screen/tella_000022_scr.jpg", pos: "47% 52%", col: "#FF5A1F", glow: "rgba(255,90,31,", role: "Coordinates the data" },
  { name: "Railway", shot: "../_assets/tella/screen/tella_000327_scr.jpg", pos: "30% 45%", col: "#8B6CFF", glow: "rgba(139,108,255,", role: "Hosts the app" },
  { name: "Claude", shot: "../_assets/tella/screen/tella_000620_scr.jpg", pos: "50% 62%", col: "#D97757", glow: "rgba(217,119,87,", role: "Research · Build · Review" },
  { name: "Wispr Flow", shot: "../_assets/tella/screen/tella_001829_scr.jpg", pos: "20% 25%", col: "#F08CC0", glow: "rgba(240,140,192,", role: "Move faster" },
];

function ground(kind) {
  el(stage, "ground " + (kind || "warm"));
  el(stage, "grid");
  el(stage, "floor");
}

function buildTracker(opt) {
  const big = !!opt.big;
  const CW = big ? 400 : 360, CH = big ? 470 : 400, GAP = big ? 56 : 60;
  const total = 4 * CW + 3 * GAP;
  // camera: perspective container + a rig we can move
  const cam = W(stage, 0, 0, 1920, 1080, { perspective: "2000px", perspectiveOrigin: "50% 42%" });
  const rig = W(cam, 0, 0, 1920, 1080, { transformStyle: "preserve-3d" });
  A(rig, {}, "");
  const cards = TOOLS.map((tl, i) => {
    const x = (1920 - total) / 2 + i * (CW + GAP), y = (1080 - CH) / 2 - 10;
    const w = W(rig, x, y, CW, CH, { transformStyle: "preserve-3d" });
    const shadowWrap = el(w, "abs shadow", { inset: "0" });
    const c = el(shadowWrap, "card glass dark bevel reflect", { inset: "0", borderRadius: "34px" });
    // rim light (NeoGlow) layer in tool colour, faded in when active
    // inner glow in the tool colour, rising from the bottom (fades in with the rim)
    const inner = el(c, "abs", { inset: 0, background: `radial-gradient(ellipse 90% 60% at 50% 115%, ${tl.glow}.55), ${tl.glow}0) 70%)`, opacity: 0 });
    const rim = el(w, "abs", { inset: "-2px", borderRadius: "36px", border: `2.5px solid ${tl.col}`, boxShadow: `0 0 26px ${tl.glow}.7), 0 0 70px ${tl.glow}.35), inset 0 0 24px ${tl.glow}.25)`, opacity: 0 });
    // real UI thumbnail
    const th = el(c, "shot", { left: "22px", top: "22px", right: "22px", height: (CH * 0.56) + "px", borderRadius: "20px", backgroundImage: img(tl.shot), backgroundPosition: tl.pos, backgroundSize: "260%", boxShadow: "0 10px 24px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,255,255,.12)" });
    // top-edge highlight on the thumbnail
    el(th, "abs", { inset: "0", background: "linear-gradient(180deg, rgba(255,255,255,.18), rgba(255,255,255,0) 30%)", borderRadius: "20px" });
    const name = el(c, "abs", { left: "30px", right: "24px", top: (CH * 0.56 + 44) + "px", fontWeight: 850, fontSize: (big ? 54 : 50) + "px", letterSpacing: "-.01em", lineHeight: 1 }, tl.name);
    const role = el(c, "abs caps", { left: "30px", right: "24px", top: (CH * 0.56 + 108) + "px", fontSize: "22px", color: tl.col, opacity: 0, lineHeight: 1.2 }, tl.role);
    // number badge: white circle, accent numeral (house list style)
    const badge = W(w, -22, -22, 74, 74);
    el(badge, "abs", { inset: 0, borderRadius: "50%", background: "linear-gradient(170deg,#fff,#e9e6e2)", boxShadow: "0 8px 18px rgba(0,0,0,.45), inset 0 -3px 6px rgba(0,0,0,.12)", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 900, fontSize: "40px", color: tl.col }, String(i + 1));
    // done tick
    const tick = W(w, CW - 58, -20, 70, 70);
    el(tick, "abs glow-good", { inset: 0, borderRadius: "50%", background: "radial-gradient(circle at 35% 30%, #6be39f, #22a45a)", display: "flex", alignItems: "center", justifyContent: "center" }, `<svg width="38" height="38" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>`);
    A(tick, { o: 0 });
    const sw = addSweep(c);
    return { w, c, rim, inner, role, badge, tick, sw, x, i };
  });
  return { cam, rig, cards, CW, CH };
}

// states: 0 hidden (below), 1 waiting (blurred, dim, pushed back), 2 active (lit, forward), 3 done (clear, dim-ish, ticked)
function cardState(card, keys) {
  // keys: [[t, state], ...]
  const S = {
    0: { y: 160, z: -200, ry: 0, blur: 14, br: 0.4, o: 0, rim: 0 },
    1: { y: 0, z: -140, ry: 0, blur: 9, br: 0.42, o: 1, rim: 0 },
    2: { y: -24, z: 170, ry: 0, blur: 0, br: 1.08, o: 1, rim: 1 },
    3: { y: 0, z: -60, ry: 0, blur: 0, br: 0.72, o: 1, rim: 0 },
    4: { y: 0, z: 0, ry: 0, blur: 0, br: 1, o: 1, rim: 0.55 },  // recap: all lit
  };
  // each change animates over d seconds: expand keys
  const exp = [];
  keys.forEach(([t, s, d, e], j) => {
    if (j === 0) exp.push([t, s]);
    else { exp.push([t, keys[j - 1][1], 0]); exp.push([t + (d || 0.7), s, e || "expo"]); }
  });
  const track = (p) => exp.map(([t, s, e], j) => (j === 0 ? [t, S[s][p]] : [t, S[s][p], e || "io"]));
  A(card.w, { y: track("y"), z: track("z"), blur: track("blur"), br: track("br"), o: track("o") });
  A(card.rim, { o: track("rim") });
  A(card.inner, { o: track("rim") });
}
