// Gallery page: builds a card per design, loops the visible stages, and keeps Samuel's verdicts.
(function () {
  const P = new URLSearchParams(location.search);
  const ONLY = P.get("only");
  const FREEZE = P.has("t") ? +P.get("t") : null;
  const A = window.ASSETS || {};
  const CATS = [
    ["pill", "Pills", "Labels, lists, verdicts, stats. Most beats on the A-roll are a pill, so this is the biggest set."],
    ["box", "Boxes", "Containers: a list, a comparison, a conversation, a set of results."],
    ["card", "Cards", "One subject per card: an option, a metric, a product, a person, a milestone."],
    ["circle", "Circles", "Hubs, orbits, rings, badges and hand-drawn marks."],
  ];
  const KEY = "motion-gallery-v1";
  let state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };
  if (ONLY) document.body.classList.add("solo");

  const main = document.getElementById("main");
  const base = document.getElementById("baseline-strip");
  if (base && A.base) base.innerHTML = A.base.map((b) => `<figure><img src="${b.src}" alt=""><figcaption>${b.cap}</figcaption></figure>`).join("");

  const scenes = [];
  CATS.forEach(([cat, title, lede]) => {
    const list = DESIGNS.filter((d) => d.cat === cat && (!ONLY || d.code === ONLY));
    if (!list.length) return;
    const sec = document.createElement("section");
    sec.className = "cat"; sec.dataset.cat = cat; sec.id = "cat-" + cat;
    sec.innerHTML = `<h3>${title} <em>${list.length}</em></h3><p class="lede">${lede}</p><div class="grid2"></div>`;
    main.appendChild(sec);
    const grid = sec.querySelector(".grid2");
    list.forEach((d) => {
      const card = document.createElement("article");
      card.className = "card"; card.id = d.code; card.dataset.cat = cat;
      const refImg = d.ref && d.ref.id && A.refs ? A.refs[d.ref.id] : null;
      card.innerHTML = `
        <div class="stage-wrap"><div class="stage-host"></div><span class="code">${d.code}</span>
          <div class="ctl"><button class="rp" title="Replay">↻</button><button class="fs" title="Full screen">⤢</button></div></div>
        <div class="info">
          <div class="r1"><h4>${d.name}</h4><div class="dots">${(d.recipe || []).map((c) => `<i style="background:${c}"></i>`).join("")}</div></div>
          <p class="use">${d.use}</p>
          <div class="ref">${refImg ? `<img src="${refImg}" alt="">` : `<span class="noimg">WEB</span>`}<div><b>Inspired by</b><br>${d.ref ? d.ref.label || d.ref.web : ""}</div></div>
          <p class="fusion"><b>Fusion:</b> ${d.fusion}</p>
          <div class="review"><button data-v="approve">Approve</button><button data-v="change">Change</button><button data-v="drop">Drop</button><input placeholder="Note for this design…"></div>
        </div>`;
      grid.appendChild(card);
      const host = card.querySelector(".stage-host");
      const S = MG.Scene(host, d);
      try { d.build(S); } catch (e) {
        console.error(d.code, e);
        host.insertAdjacentHTML("beforeend", `<div style="position:absolute;inset:0;display:grid;place-items:center;color:#ff7a7a;font:600 14px Geist,sans-serif;z-index:9">${d.code}: ${e.message}</div>`);
      }
      const sc = { S, host, loop: d.loop || 6, t0: performance.now(), card, code: d.code };
      scenes.push(sc); host.__sc = sc;
      const fit = () => { const w = host.clientWidth || 1920; S.stage.style.transform = `scale(${w / 1920})`; };
      if (window.ResizeObserver) new ResizeObserver(fit).observe(host);
      fit();
      const toggleFull = () => { card.classList.toggle("full"); requestAnimationFrame(fit); };
      card.querySelector(".rp").onclick = (e) => { e.stopPropagation(); sc.t0 = performance.now(); };
      card.querySelector(".fs").onclick = (e) => { e.stopPropagation(); toggleFull(); };
      host.onclick = toggleFull;
      const st = state[d.code] || {};
      const btns = card.querySelectorAll(".review button"), inp = card.querySelector(".review input");
      const paint = () => {
        btns.forEach((b) => b.classList.toggle("on", b.dataset.v === st.v));
        card.classList.remove("v-approve", "v-change", "v-drop");
        if (st.v) card.classList.add("v-" + st.v);
        tally();
      };
      btns.forEach((b) => (b.onclick = () => { st.v = st.v === b.dataset.v ? undefined : b.dataset.v; state[d.code] = st; save(); paint(); applyFilter(); }));
      inp.value = st.note || "";
      inp.oninput = () => { st.note = inp.value; state[d.code] = st; save(); tally(); };
      card.__paint = paint;
    });
  });

  // loop only the stages on screen
  const live = new Set();
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    const sc = e.target.__sc;
    if (e.isIntersecting) { if (!live.has(sc)) sc.t0 = performance.now(); live.add(sc); } else live.delete(sc);
  }), { rootMargin: "100px" });
  scenes.forEach((sc) => io.observe(sc.host));
  const draw = (sc, t) => { try { sc.S.R(t); } catch (e) { if (!sc.err) { sc.err = 1; console.error(sc.code, e); } } };
  const tick = (now) => {
    for (const sc of live) draw(sc, FREEZE != null ? FREEZE : ((now - sc.t0) / 1000) % sc.loop);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  window.RENDER_AT = (t) => scenes.forEach((sc) => draw(sc, t));
  if (FREEZE != null) scenes.forEach((sc) => draw(sc, FREEZE));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") document.querySelectorAll(".card.full").forEach((c) => c.classList.remove("full")); });

  // filters
  let filter = "all";
  function applyFilter() {
    document.querySelectorAll(".card").forEach((c) => {
      const v = (state[c.id] || {}).v;
      const show = filter === "all" || filter === c.dataset.cat || (filter === "approve" && v === "approve") || (filter === "change" && v === "change") || (filter === "todo" && !v);
      c.style.display = show ? "" : "none";
    });
    document.querySelectorAll("section.cat").forEach((s) => { s.style.display = [...s.querySelectorAll(".card")].some((c) => c.style.display !== "none") ? "" : "none"; });
    document.getElementById("baseline").style.display = filter === "all" ? "" : "none";
  }
  document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => {
    filter = b.dataset.f;
    document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("on", x === b));
    applyFilter();
  }));

  function tally() {
    const n = { approve: 0, change: 0, drop: 0 };
    DESIGNS.forEach((d) => { const v = (state[d.code] || {}).v; if (v) n[v]++; });
    const el = document.getElementById("tally");
    if (el) el.innerHTML = `<span><b>${n.approve}</b> approved</span><span><b>${n.change}</b> change</span><span><b>${n.drop}</b> drop</span><span><b>${DESIGNS.length - n.approve - n.change - n.drop}</b> to review</span>`;
  }
  tally();

  // review text to paste back into chat
  function reviewText() {
    const lines = ["Motion gallery v1 review"];
    const tag = { approve: "APPROVE", change: "CHANGE", drop: "DROP" };
    const todo = [];
    DESIGNS.forEach((d) => {
      const s = state[d.code] || {};
      if (!s.v && !s.note) { todo.push(d.code); return; }
      lines.push(`${d.code} ${d.name}: ${s.v ? tag[s.v] : "NOTE"}${s.note ? " — " + s.note : ""}`);
    });
    if (todo.length) lines.push("Not reviewed: " + todo.join(", "));
    return lines.join("\n");
  }
  const modal = document.getElementById("modal"), ta = modal.querySelector("textarea");
  document.getElementById("copy").onclick = async () => {
    const txt = reviewText();
    ta.value = txt;
    let ok = false;
    try { await navigator.clipboard.writeText(txt); ok = true; } catch (e) {}
    modal.querySelector(".msg").textContent = ok ? "Copied. Paste it into the chat." : "Select all and copy, then paste it into the chat.";
    modal.classList.add("on");
    ta.focus(); ta.select();
  };
  modal.querySelector(".close").onclick = () => modal.classList.remove("on");
  document.getElementById("clear").onclick = () => {
    if (!confirm("Clear every verdict and note on this page?")) return;
    state = {}; save(); location.reload();
  };
  if (location.hash) { const t = document.querySelector(location.hash); if (t) setTimeout(() => t.scrollIntoView({ block: "center" }), 300); }
})();
