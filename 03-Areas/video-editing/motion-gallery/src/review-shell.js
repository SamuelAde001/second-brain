// Visual review page: every sentence of the cut in order; each visual plays in sync with a live caption of the words.
// Data from the build: window.JOB {title, version, date, fps, sentences[{id,start,end,vo}], cues[[start,end,text]], sections[{name,start,color}]}
// Visuals registered by the job's scenes file: RV(code, meta, build?) with meta {beats:"B11-B12", kind, title, desc, from, fusion, still, prompt}
(function () {
  const JB = window.JOB, A = window.ASSETS || {};
  const FPS = JB.fps || 24000 / 1001;
  const P = new URLSearchParams(location.search);
  const ONLY = P.get("only"), FREEZE = P.has("t") ? P.get("t") : null;
  const tFor = (sc) => (FREEZE === "end" ? Math.max(0, sc.loop - 1.1) : FREEZE === "mid" ? sc.loop * 0.45 : +FREEZE);
  if (ONLY) document.body.classList.add("solo");
  const SENT = JB.sentences, byId = {};
  SENT.forEach((s, i) => { s.i = i; byId[s.id] = s; });
  const tc = (f) => { const s = f / FPS; return `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`; };
  const KIND = { mg: "Motion graphic · BGORANGE", overlay: "Motion graphic · on the A-roll", text: "Text · Down fade", quote: "Quote · on his footage", idea: "Intro idea (yours to edit)", ui: "Real screen (as planned)", reuse: "Reuse from #3", flow: "AI video · Flow", aroll: "A-roll" };
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

  // word timeline from the cues: each word gets a frame, spread across its cue by character position
  const WORDS = [];
  JB.cues.forEach(([s, e, text], ci) => {
    const parts = text.split(/\s+/).filter(Boolean);
    let pos = 0;
    const len = Math.max(1, text.length);
    parts.forEach((w) => {
      const at = text.indexOf(w, pos);
      WORDS.push({ f: s + (e - s) * (at / len), raw: w, n: w.toLowerCase().replace(/[^a-z0-9%$']/g, ""), ci });
      pos = at + w.length;
    });
  });

  // visuals, beat -> visual
  const VIS = window.RVS || [];
  const owner = {};
  VIS.forEach((v) => {
    const [a, b] = (v.beats.includes("-") ? v.beats.split("-") : [v.beats, v.beats]);
    v.first = byId[a]; v.last = byId[b];
    for (let i = v.first.i; i <= v.last.i; i++) owner[SENT[i].id] = v;
    v.F0 = v.first.start; v.F1 = v.last.end;
  });

  const KEY = "review-" + JB.slug + "-" + JB.version;
  let state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };

  const main = document.getElementById("main");
  const scenes = [];
  let secIdx = -1, plain = null;
  const secAt = (f) => { let k = 0; JB.sections.forEach((s, i) => { if (f >= s.start) k = i; }); return k; };
  const flushPlain = () => {
    if (!plain) return;
    const row = document.createElement("div");
    row.className = "arow"; row.dataset.kind = "aroll";
    const th = A.thumbs && A.thumbs[plain[0].id];
    row.innerHTML = `${th ? `<img src="${th}" alt="">` : "<span></span>"}<div><span class="kind k-aroll"><i></i>A-roll · let it breathe</span><br>${plain.map((s) => `<em>${tc(s.start)}</em>${esc(s.vo)}`).join("<br>")}</div>`;
    main.appendChild(row);
    plain = null;
  };
  SENT.forEach((s) => {
    const k = secAt(s.start);
    if (k !== secIdx && !ONLY) {
      flushPlain();
      secIdx = k;
      const sec = JB.sections[k];
      const h = document.createElement("div");
      h.className = "sec-h"; h.dataset.sec = k;
      h.innerHTML = `<i class="bar" style="background:${sec.color}"></i><h3>${k + 1}. ${esc(sec.name)}</h3><small>${tc(sec.start)}</small>`;
      main.appendChild(h);
    }
    const v = owner[s.id];
    if (!v) { if (!ONLY) (plain = plain || []).push(s); return; }
    if (v.first !== s) return;
    flushPlain();
    if (ONLY && v.code !== ONLY) return;
    buildRow(v);
  });
  flushPlain();

  function buildRow(v) {
    const row = document.createElement("article");
    row.className = "vrow"; row.id = v.code; row.dataset.kind = v.kind;
    const sents = SENT.slice(v.first.i, v.last.i + 1);
    row.innerHTML = `
      <div><div class="stage-wrap"><div class="stage-host"></div><span class="code">${v.code}</span>
        <div class="ctl"><button class="rp" title="Replay">↻</button><button class="fs" title="Full screen">⤢</button></div></div>
        <div class="cap"></div></div>
      <div class="vinfo">
        <div class="top"><span class="code2">${v.code}</span><span class="kind k-${v.kind}"><i></i>${KIND[v.kind] || v.kind}</span><span class="tc">${tc(v.F0)}–${tc(v.F1)} · ${((v.F1 - v.F0) / FPS).toFixed(1)} s · ${v.beats}</span></div>
        <h4>${esc(v.title)}</h4>
        <p class="desc">${v.desc || ""}</p>
        <div class="vo">${sents.map((s) => `<span><em>${tc(s.start)}</em>${esc(s.vo)}</span>`).join("")}</div>
        ${v.from ? `<div class="from">Built from the gallery: <b>${v.from}</b></div>` : ""}
        ${v.fusion ? `<p class="fusion"><b>Fusion:</b> ${v.fusion}</p>` : ""}
        <div class="warn"></div>
        <div class="review"><button data-v="approve">Approve</button><button data-v="change">Change</button><button data-v="drop">Drop</button><input placeholder="Comment on ${v.code}…"></div>
      </div>`;
    main.appendChild(row);
    const host = row.querySelector(".stage-host"), cap = row.querySelector(".cap");
    const dur = (v.F1 - v.F0) / FPS;
    let S = null;
    if (v.build) {
      S = MG.Scene(host, { loop: dur + (v.tail == null ? 1.8 : v.tail) });
      const warns = [];
      const w0 = WORDS.findIndex((w) => w.f >= v.F0 - 6), w1 = WORDS.findIndex((w) => w.f > v.F1 + 6);
      const ws = WORDS.slice(w0, w1 < 0 ? WORDS.length : w1);
      S.when = (phrase, nth) => {
        const q = phrase.toLowerCase().split(/\s+/).map((w) => w.replace(/[^a-z0-9%$']/g, "")).filter(Boolean);
        let hit = 0;
        for (let i = 0; i + q.length <= ws.length; i++) {
          if (q.every((w, j) => ws[i + j].n === w)) { hit++; if (hit === (nth || 1)) return Math.max(0, (ws[i].f - v.F0) / FPS); }
        }
        warns.push(phrase);
        return 0.6;
      };
      S.beat = (id) => (byId[id].start - v.F0) / FPS;
      S.dur = dur;
      try { v.build(S, window.PARTS); } catch (e) {
        console.error(v.code, e);
        host.insertAdjacentHTML("beforeend", `<div style="position:absolute;inset:0;display:grid;place-items:center;color:#ff7a7a;font:600 14px Geist,sans-serif;z-index:9">${v.code}: ${esc(e.message)}</div>`);
      }
      if (warns.length) row.querySelector(".warn").textContent = "Timing not found for: " + warns.join(" · ");
    } else if (v.kind === "flow") {
      host.innerHTML = `<div class="flowbox"><div><b>AI video · Flow</b>${esc(v.prompt || "")}</div></div>`;
    } else {
      const src = A.stills && A.stills[v.still || v.code];
      host.innerHTML = src ? `<img class="still" src="${src}" alt="">` : "";
    }
    // caption: the sentence being spoken in the corrected script text, the current word lit (timed from the raw cue words)
    const capS = sents.map((s) => ({ s, raw: WORDS.filter((x) => x.f >= s.start - 2 && x.f < s.end), words: s.vo.split(/\s+/) }));
    let lastKey = "";
    const caption = (t) => {
      const f = v.F0 + t * FPS;
      let si = 0;
      capS.forEach((c, i) => { if (f >= c.s.start - 2) si = i; });
      const c = capS[si];
      let k = 0;
      c.raw.forEach((x, i) => { if (x.f <= f) k = i; });
      const idx = c.raw.length ? Math.min(c.words.length - 1, Math.floor((k * c.words.length) / c.raw.length)) : 0;
      const key = si + ":" + idx;
      if (key === lastKey) return;
      lastKey = key;
      cap.innerHTML = c.words.map((x, i) => (i === idx ? `<b>${esc(x)}</b>` : esc(x))).join(" ");
    };
    caption(0);
    const sc = { S, host, cap: caption, loop: S ? S.loop : dur, t0: performance.now(), code: v.code, still: !S };
    scenes.push(sc); host.__sc = sc;
    const fit = () => { if (S) S.stage.style.transform = `scale(${(host.clientWidth || 1920) / 1920})`; };
    if (window.ResizeObserver) new ResizeObserver(fit).observe(host);
    fit();
    const toggleFull = () => { row.classList.toggle("full"); row.querySelector(".stage-wrap").classList.toggle("fullw"); requestAnimationFrame(fit); };
    row.querySelector(".rp").onclick = (e) => { e.stopPropagation(); sc.t0 = performance.now(); };
    row.querySelector(".fs").onclick = (e) => { e.stopPropagation(); toggleFull(); };
    host.onclick = toggleFull;
    const st = state[v.code] || {};
    const btns = row.querySelectorAll(".review button"), inp = row.querySelector(".review input");
    const paint = () => { btns.forEach((b) => b.classList.toggle("on", b.dataset.v === st.v)); row.classList.remove("v-approve", "v-change", "v-drop"); if (st.v) row.classList.add("v-" + st.v); tally(); };
    btns.forEach((b) => (b.onclick = () => { st.v = st.v === b.dataset.v ? undefined : b.dataset.v; state[v.code] = st; save(); paint(); }));
    inp.value = st.note || "";
    inp.oninput = () => { st.note = inp.value; state[v.code] = st; save(); tally(); };
    setTimeout(paint);
  }

  // play only what's on screen
  const onScreen = new Set();
  const io = new IntersectionObserver((es) => es.forEach((e) => { const sc = e.target.__sc; if (e.isIntersecting) { if (!onScreen.has(sc)) sc.t0 = performance.now(); onScreen.add(sc); } else onScreen.delete(sc); }), { rootMargin: "80px" });
  scenes.forEach((sc) => io.observe(sc.host));
  const draw = (sc, t) => { try { if (sc.S) sc.S.R(t); sc.cap(t); } catch (e) { if (!sc.err) { sc.err = 1; console.error(sc.code, e); } } };
  const tick = (now) => { for (const sc of onScreen) draw(sc, FREEZE != null ? tFor(sc) : ((now - sc.t0) / 1000) % sc.loop); requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  if (FREEZE != null) scenes.forEach((sc) => draw(sc, tFor(sc)));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") document.querySelectorAll(".vrow.full").forEach((c) => { c.classList.remove("full"); c.querySelector(".stage-wrap").classList.remove("fullw"); }); });

  // filters
  const GROUPS = { all: null, mg: ["mg", "overlay", "text", "quote"], idea: ["idea"], screen: ["ui", "reuse", "flow"] };
  let filter = "all";
  function applyFilter() {
    document.querySelectorAll(".vrow").forEach((r) => {
      const v = (state[r.id] || {}).v;
      const g = GROUPS[filter];
      r.style.display = filter === "flag" ? (v === "change" || v === "drop" ? "" : "none") : filter === "todo" ? (v ? "none" : "") : !g || g.includes(r.dataset.kind) ? "" : "none";
    });
    document.querySelectorAll(".arow").forEach((r) => { r.style.display = filter === "all" ? "" : "none"; });
    document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("on", x.dataset.f === filter));
  }
  document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => { filter = b.dataset.f; applyFilter(); }));
  function tally() {
    let ok = 0, ch = 0, dr = 0;
    VIS.forEach((v) => { const s = (state[v.code] || {}).v; if (s === "approve") ok++; else if (s === "change") ch++; else if (s === "drop") dr++; });
    const el = document.getElementById("tally");
    if (el) el.innerHTML = `<span><b>${ok}</b> approved</span><span><b>${ch}</b> change</span><span><b>${dr}</b> drop</span><span><b>${VIS.length - ok - ch - dr}</b> to review</span>`;
  }
  tally();
  function reviewText() {
    const L = [`${JB.title} · visual review ${JB.version}`], todo = [];
    const tag = { approve: "APPROVE", change: "CHANGE", drop: "DROP" };
    VIS.forEach((v) => { const s = state[v.code] || {}; if (!s.v && !s.note) { todo.push(v.code); return; } L.push(`${v.code} ${v.title}: ${s.v ? tag[s.v] : "NOTE"}${s.note ? " — " + s.note : ""}`); });
    if (todo.length) L.push("Not reviewed: " + todo.join(", "));
    return L.join("\n");
  }
  const modal = document.getElementById("modal"), ta = modal.querySelector("textarea");
  document.getElementById("copy").onclick = async () => {
    const txt = reviewText(); ta.value = txt; let ok = false;
    try { await navigator.clipboard.writeText(txt); ok = true; } catch (e) {}
    modal.querySelector(".msg").textContent = ok ? "Copied. Paste it into the chat." : "Select all and copy, then paste it into the chat.";
    modal.classList.add("on"); ta.focus(); ta.select();
  };
  modal.querySelector(".close").onclick = () => modal.classList.remove("on");
  document.getElementById("clear").onclick = () => { if (!confirm("Clear your marks and comments on this page?")) return; state = {}; save(); location.reload(); };
  if (location.hash) { const t = document.querySelector(location.hash); if (t) setTimeout(() => t.scrollIntoView({ block: "center" }), 300); }
})();
