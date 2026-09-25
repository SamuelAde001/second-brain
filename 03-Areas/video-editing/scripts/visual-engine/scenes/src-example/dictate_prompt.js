// B41 9733-9971 "So for example, I can say: review the list summary for B2B outbound campaign, tell me which records still need verification, what information is missing, and what we should check before using the contacts on LinkedIn."
// His words land in Claude's prompt box on his timing (subtitle cues, words spread evenly inside each cue).
grounds("cream");
vignette(true);
const m = macWin(stage, 200, 90, 1520, 760, "claude.ai / new chat");
const b = m.body;
b.style.background = "#faf9f5";
el(b, "abs serif", { left: 0, right: 0, top: "70px", textAlign: "center", fontSize: "56px", color: "#3d3929" }, `<span style="color:#D97757">✳</span> Welcome, Alex Vacca`);
const box = el(b, "abs", { left: "140px", right: "140px", top: "190px", minHeight: "300px", borderRadius: "28px", background: "#fff", border: "2px solid #e5e2d9", padding: "34px 38px 90px", fontSize: "36px", lineHeight: 1.45, color: "#3d3929", boxShadow: "0 10px 30px rgba(60,40,20,.08)" });
const txtEl = el(box, "", {});
const send = el(box, "abs", { right: "26px", bottom: "22px", width: "62px", height: "62px", borderRadius: "16px", background: "#D97757", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 900, fontSize: "32px" }, "↑");
neo(m.w, 0.05, { dist: 50 });
// cues (timeline frames) -> words
const cues = [
  [9760, 9783, "Review the list"],
  [9784, 9825, "summary for our B2B outbound campaign."],
  [9830, 9861, "Tell me which records still need"],
  [9861, 9884, "verification, what"],
  [9884, 9911, "information is missing,"],
  [9913, 9949, "and what we should check before using the"],
  [9950, 9971, "contacts on LinkedIn."],
];
const W8 = [];
cues.forEach(([a, z, s]) => { const ws = s.split(" "); ws.forEach((w, i) => W8.push([T(a) + ((T(z) - T(a)) * i) / ws.length, w + " "])); });
F((t) => { txtEl.textContent = W8.filter((w) => w[0] <= t).map((w) => w[1]).join(""); });
// the pill listens while he speaks
const pill = wisprPill(stage, 810, 900, { w: 300, h: 86, on: (t) => (t > T(9755) && t < T(9969) ? 1 : 0.15) });
neo(pill, 0.3, { dist: 60 });
const lab = el(stage, "abs caps", { left: "1130px", top: "926px", fontSize: "24px", color: "#8a7f76", letterSpacing: ".1em" }, "Wispr Flow");
fade(lab, 0.4, 0.3);
// send on the last word
A(send, { s: [[T(9966), 1], [T(9968), 0.85], [T(9971), 1]] }, "");
