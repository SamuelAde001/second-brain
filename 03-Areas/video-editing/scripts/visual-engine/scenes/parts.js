// Larger reusable pieces (UI rebuilds) for Route Rise #3.

// ---- the messy prospecting desktop (B02, B03) ----
function deskWallpaper() {
  const w = W(stage, -40, -40, 2000, 1160);
  el(w, "abs", { inset: 0, background: "radial-gradient(ellipse 60% 70% at 25% 30%, #d9c4ee 0%, rgba(217,196,238,0) 60%), radial-gradient(ellipse 60% 70% at 80% 75%, #f0c9d9 0%, rgba(240,201,217,0) 60%), linear-gradient(135deg,#b9a6de,#e7bfd3)" });
  el(w, "abs", { inset: 0, background: "rgba(20,10,20,.28)" });
  return w;
}
function linkedinWin(parent, x, y) {
  const m = macWin(parent, x, y, 620, 430, "linkedin.com/in/sarah-lee");
  const b = m.body;
  el(b, "abs", { left: 0, right: 0, top: 0, height: "52px", background: "#fff", borderBottom: "1px solid #e6e6e6" }, `<div style="position:absolute;left:18px;top:11px;width:30px;height:30px;border-radius:6px;background:#0A66C2;color:#fff;font-weight:900;font-size:19px;display:flex;align-items:center;justify-content:center">in</div>`);
  el(b, "abs", { left: "16px", right: "16px", top: "66px", height: "110px", borderRadius: "10px", background: "linear-gradient(120deg,#a8c6e8,#d8e6f5)" });
  avatar(b, 40, 120, 104, "#8aa4c2", { bg: "linear-gradient(160deg,#9bb3cf,#56708f)", ring: "#fff" });
  el(b, "abs", { left: "40px", top: "240px", fontWeight: 750, fontSize: "26px", color: "#191919" }, "Sarah Lee");
  el(b, "abs", { left: "40px", top: "276px", fontSize: "17px", color: "#555" }, "Head of Sales at Northwind");
  el(b, "abs", { left: "40px", top: "318px", width: "150px", height: "40px", borderRadius: "20px", background: "#0A66C2", color: "#fff", fontWeight: 700, fontSize: "16px", display: "flex", alignItems: "center", justifyContent: "center" }, "Connect");
  el(b, "abs line", { left: "220px", top: "334px", width: "260px" });
  return m;
}
function websiteWin(parent, x, y) {
  const m = macWin(parent, x, y, 640, 420, "northwind.io");
  const b = m.body;
  b.style.background = "linear-gradient(160deg,#10233f,#1b3c66)";
  b.style.color = "#fff";
  el(b, "abs", { left: "28px", top: "20px", fontWeight: 800, fontSize: "20px" }, "◆ Northwind");
  el(b, "abs", { right: "28px", top: "22px", fontSize: "14px", opacity: .7 }, "Product&nbsp;&nbsp;Pricing&nbsp;&nbsp;Careers");
  el(b, "abs", { left: "28px", top: "92px", fontWeight: 800, fontSize: "40px", lineHeight: 1.05, width: "420px" }, "Analytics for modern retail teams");
  el(b, "abs", { left: "28px", top: "208px", width: "360px" }, `<div class="dline" style="width:100%;margin-bottom:10px"></div><div class="dline" style="width:78%"></div>`);
  el(b, "abs", { left: "28px", top: "262px", width: "170px", height: "46px", borderRadius: "10px", background: "#4f9dff", fontWeight: 700, fontSize: "16px", display: "flex", alignItems: "center", justifyContent: "center" }, "Book a demo");
  el(b, "abs", { right: "30px", top: "96px", width: "190px", height: "220px", borderRadius: "14px", background: "rgba(255,255,255,.1)", border: "1px solid rgba(255,255,255,.15)" });
  return m;
}
function databaseWin(parent, x, y) {
  const m = macWin(parent, x, y, 600, 380, "db.internal / companies", { bg: "#16181d", fg: "#dfe3ea", barBg: "linear-gradient(#26292f,#1e2025)", urlStyle: "background:#2c2f36;color:#9aa3b1" });
  const b = m.body;
  const cols = ["id", "company", "domain", "employees"];
  let h = `<div style="display:grid;grid-template-columns:60px 1.3fr 1.2fr 1fr;font-family:Consolas,monospace;font-size:15px">`;
  cols.forEach((c) => (h += `<div style="padding:12px 14px;color:#7f8a9b;border-bottom:1px solid #2b2f37">${c}</div>`));
  const rows = [["1041", "Northwind", "northwind.io", "120"], ["1042", "Acme Corp", "acme.co", "85"], ["1043", "Globex", "globex.com", "—"], ["1044", "Initech", "initech.io", "240"], ["1045", "Umbrella", "umbrella.ai", "—"], ["1046", "Hooli", "hooli.xyz", "1,200"]];
  rows.forEach((r) => r.forEach((c) => (h += `<div style="padding:11px 14px;border-bottom:1px solid #22252c">${c}</div>`)));
  el(b, "abs", { inset: 0 }, h + "</div>");
  return m;
}
function sheetWin(parent, x, y, title) {
  const m = macWin(parent, x, y, 660, 420, title || "Prospect list.xlsx");
  const b = m.body;
  el(b, "abs", { left: 0, right: 0, top: 0, height: "40px", background: "#107C41", color: "#fff", fontWeight: 700, fontSize: "15px", display: "flex", alignItems: "center", paddingLeft: "16px" }, "Prospect list");
  let h = `<div style="display:grid;grid-template-columns:40px repeat(4,1fr);font-size:14px;color:#333">`;
  ["", "A  Name", "B  Company", "C  Email", "D  Title"].forEach((c) => (h += `<div style="padding:8px;background:#f3f3f3;border:1px solid #e1e1e1;font-weight:600">${c}</div>`));
  for (let r = 1; r <= 8; r++) {
    h += `<div style="padding:8px;background:#f3f3f3;border:1px solid #e1e1e1;color:#888">${r}</div>`;
    for (let c = 0; c < 4; c++) h += `<div class="cell" style="padding:8px;border:1px solid #e6e6e6;height:37px"></div>`;
  }
  el(b, "abs", { left: 0, right: 0, top: "40px" }, h + "</div>");
  return m;
}
function outreachWin(parent, x, y) {
  const m = macWin(parent, x, y, 560, 400, "app.sequencer.io / campaign");
  const b = m.body;
  b.style.background = "#f7f7fb";
  el(b, "abs", { left: "24px", top: "18px", fontWeight: 800, fontSize: "20px", color: "#222" }, "Q4 outbound");
  const steps = [["Email 1", "#6c5ce7"], ["Wait 2 days", "#aaa"], ["Email 2", "#6c5ce7"], ["LinkedIn touch", "#0A66C2"]];
  steps.forEach((s, i) => el(b, "abs", { left: "24px", right: "24px", top: 64 + i * 66 + "px", height: "54px", borderRadius: "12px", background: "#fff", border: "1px solid #e4e4ee", display: "flex", alignItems: "center", gap: "12px", padding: "0 16px", fontWeight: 650, fontSize: "17px", color: "#333" }, `<span style="width:12px;height:12px;border-radius:50%;background:${s[1]}"></span>${s[0]}`));
  el(b, "abs", { right: "24px", bottom: "18px", width: "130px", height: "42px", borderRadius: "10px", background: "#6c5ce7", color: "#fff", fontWeight: 700, fontSize: "16px", display: "flex", alignItems: "center", justifyContent: "center" }, "Launch");
  return m;
}
// the full desktop with the five windows; returns handles
function messyDesk() {
  deskWallpaper();
  const cam = W(stage, 0, 0, 1920, 1080);
  const sheet = sheetWin(cam, 640, 330);
  const li = linkedinWin(cam, 120, 120);
  const web = websiteWin(cam, 1150, 90);
  const db = databaseWin(cam, 230, 560);
  const out = outreachWin(cam, 1240, 560);
  return { cam, sheet, li, web, db, out };
}

// ---- light data table (Clay-like) ----
function dataTable(parent, x, y, w, cols, rows, o) {
  o = o || {};
  const wr = W(parent, x, y, w, null);
  const sh = el(wr, "abs shadow" + (o.lightShadow ? " light" : ""), { left: 0, top: 0, width: w + "px" });
  const card = el(sh, "card lightcard bevel soft", { position: "relative", borderRadius: "22px", padding: "10px 0 6px" });
  const grid = el(card, "", { display: "grid", gridTemplateColumns: o.tpl || `repeat(${cols.length},1fr)`, fontSize: (o.fs || 19) + "px", color: "#2a2420" });
  const cells = [];
  cols.forEach((c) => el(grid, "", { padding: "14px 20px", fontWeight: 700, fontSize: (o.fs || 19) - 3 + "px", letterSpacing: ".05em", textTransform: "uppercase", color: "#8a8178", borderBottom: "1px solid #ece8e3" }, c));
  rows.forEach((r, ri) => {
    const rc = [];
    r.forEach((c) => rc.push(el(grid, "", { padding: (o.pad || 15) + "px 24px", borderBottom: ri < rows.length - 1 ? "1px solid #f0ece7" : "none", whiteSpace: "nowrap", position: "relative" }, c)));
    cells.push(rc);
  });
  return { wr, card, grid, cells };
}
function statusPill(text, kind) {
  const c = { good: ["#e3f8ec", "#1e9e55"], warn: ["#fff3dc", "#c27b06"], bad: ["#fde6e4", "#d63a2f"], grey: ["#efedea", "#8a8178"] }[kind];
  return `<span style="display:inline-flex;align-items:center;gap:10px;padding:8px 18px;border-radius:999px;background:${c[0]};color:${c[1]};font-weight:800;font-size:22px;letter-spacing:.06em"><i style="width:9px;height:9px;border-radius:50%;background:${c[1]};display:inline-block"></i>${text}</span>`;
}

// ---- Railway service card (rebuilt from the real canvas) ----
const GH = `<svg width="30" height="30" viewBox="0 0 24 24"><path fill="#e8e6f3" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.56-.29-5.25-1.28-5.25-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.39-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5z"/></svg>`;
const PG = `<svg width="30" height="30" viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="8" ry="3" fill="none" stroke="#9fb4ff" stroke-width="2"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" fill="none" stroke="#9fb4ff" stroke-width="2"/></svg>`;
function railCard(parent, x, y, name, sub, o) {
  o = o || {};
  const w = W(parent, x, y, o.w || 400, o.h || 170);
  const s = el(w, "abs shadow", { inset: 0 });
  const c = el(s, "card navycard bevel", { inset: 0, borderRadius: "22px", padding: "26px 28px" });
  el(c, "", { display: "flex", alignItems: "center", gap: "16px", fontWeight: 750, fontSize: "27px", color: "#f1effa" }, (o.pg ? PG : GH) + `<span>${name}</span>`);
  if (sub) el(c, "", { marginTop: "6px", marginLeft: "46px", fontSize: "18px", color: "rgba(230,226,250,.5)" }, sub);
  const on = el(c, "", { position: "absolute", left: "74px", bottom: "26px", display: "flex", alignItems: "center", gap: "10px", fontWeight: 650, fontSize: "20px", color: "#3ED07E" }, `<i style="width:11px;height:11px;border-radius:50%;background:#3ED07E;box-shadow:0 0 12px #3ED07E;display:inline-block"></i>Online`);
  addSweep(c);
  return { w, c, on };
}
function navyGround() { grounds("violet", { floor: true }); }

// ---- Wispr Flow dictation pill (black pill with live bars, as in the real app) ----
function wisprPill(parent, x, y, o) {
  o = o || {};
  const w = W(parent, x, y, o.w || 300, o.h || 84);
  const s = el(w, "abs shadow", { inset: 0 });
  const c = el(s, "card", { inset: 0, borderRadius: "999px", background: "linear-gradient(180deg,#1a1a1a,#050505)", border: "1.5px solid rgba(255,255,255,.18)", display: "flex", alignItems: "center", justifyContent: "center", gap: "7px", boxShadow: "inset 0 1.5px 0 rgba(255,255,255,.25)" });
  const bars = [];
  const n = o.n || 13;
  for (let i = 0; i < n; i++) bars.push(el(c, "", { width: "7px", height: "10px", borderRadius: "4px", background: "#fff" }));
  const on = o.on || (() => 1);
  F((t) => { const a = on(t); bars.forEach((b, i) => { const v = a * (0.25 + 0.75 * Math.abs(Math.sin(t * (7 + (i % 5)) + i * 1.7) * Math.cos(t * 3.1 + i))); b.style.height = 8 + v * ((o.h || 84) * 0.55) + "px"; }); });
  return w;
}

// ---- the 4-step workflow rail (progress bar across the "together" section) ----
const STEPS = [["Define", "target"], ["Research", "search"], ["Angle", "online-writing"], ["Build", "network"]];
function stepRail(active, t0) {
  const w = W(stage, 260, 40, 1400, 96);
  const svgw = el(w, "abs", { left: "0", right: "0", top: "46px", height: "4px", background: "rgba(255,255,255,.12)", borderRadius: "2px" });
  const fill = el(svgw, "abs", { left: 0, top: 0, bottom: 0, width: ((active - 1) / 3) * 100 + "%", background: "linear-gradient(90deg,#FF5A1F,#FD9457)", boxShadow: "0 0 12px #FF5A1F" });
  STEPS.forEach(([lab, ic], i) => {
    const n = i + 1, x = (i / 3) * 1400 - 120;
    const p = W(w, x, 10, 240, 76);
    const on = n === active, done = n < active;
    el(p, "chip " + (on ? "orangefill bevel" : "glass dark bevel"), { position: "absolute", left: 0, top: 0, width: "240px", justifyContent: "center", fontSize: "24px", color: done ? "rgba(255,255,255,.75)" : "#fff" }, `<b style="font-size:28px;opacity:.7">${n}</b>&nbsp;${lab.toUpperCase()}${done ? "&nbsp;<span style='color:#3ED07E'>✓</span>" : ""}`);
    if (!on && !done) A(p, { blur: 5, o: 0.55 });
    else if (on) A(p, { s: [[t0 || 0.1, 0.8], [(t0 || 0.1) + 0.5, 1.08, "back"]] });
  });
  neo(w, 0.02, { dist: 40, ang: 90 });
  return w;
}
function stepHeader(n, lab, x, y, t0) {
  const w = W(stage, x, y, 620, 118);
  const s = el(w, "abs shadow", { inset: 0 });
  const p = el(s, "pill orangefill bevel", { position: "absolute", inset: 0, height: "118px", borderRadius: "28px" });
  el(p, "num", { fontSize: "150px" }, String(n));
  el(p, "txt", { fontSize: "52px" }, lab);
  addSweep(p);
  neo(w, t0, { dist: 70 });
  sweep(p, t0 + 0.5, 0.9);
  return w;
}
function toolTile(parent, x, y, size, idx, o) {
  o = o || {};
  const tl = TOOLS[idx];
  const w = W(parent, x, y, size, size * 1.1);
  const s = el(w, "abs shadow", { inset: 0 });
  const c = el(s, "card glass dark bevel", { inset: 0, borderRadius: size * 0.16 + "px", border: `2px solid ${tl.col}`, boxShadow: `0 0 22px ${tl.glow}.5), inset 0 2px 0 rgba(255,255,255,.3)` });
  el(c, "abs", { inset: 0, background: `radial-gradient(ellipse 90% 60% at 50% 115%, ${tl.glow}.5), ${tl.glow}0) 70%)` });
  el(c, "shot", { left: size * 0.07 + "px", top: size * 0.07 + "px", right: size * 0.07 + "px", height: size * 0.62 + "px", borderRadius: size * 0.08 + "px", backgroundImage: img(tl.shot), backgroundPosition: tl.pos, backgroundSize: "260%" });
  el(c, "abs", { left: 0, right: 0, bottom: size * 0.1 + "px", textAlign: "center", fontWeight: 850, fontSize: size * 0.15 + "px" }, tl.name);
  addSweep(c);
  return { w, c };
}

// ---- the full workflow board (B52, B53) ----
function fullBoard(svg) {
  const cols = [[120, "Define", 3], [560, "Research", 0], [1000, "Angle", 2], [1440, "Build", 1]];
  const cards = cols.map(([x, lab, ti], i) => {
    const w = W(stage, x, 300, 380, 470);
    const s = el(w, "abs shadow", { inset: 0 });
    const c = el(s, "card glass dark bevel", { inset: 0, borderRadius: "34px" });
    el(c, "abs", { left: "26px", top: "20px", fontWeight: 900, fontSize: "90px", lineHeight: 1, color: "rgba(255,255,255,.1)" }, String(i + 1));
    el(c, "abs caps", { left: "30px", bottom: "34px", fontSize: "40px" }, lab);
    const t = toolTile(w, 75, 90, 230, ti);
    addSweep(c);
    return { w, c, t };
  });
  const links = [];
  for (let i = 0; i < 3; i++) links.push(path(svg, `M${cols[i][0] + 380} 535 L${cols[i + 1][0]} 535`, { width: 5 }));
  return { cards, links, cols };
}
