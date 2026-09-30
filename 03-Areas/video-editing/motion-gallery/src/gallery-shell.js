// Gallery page: a card per design, loops the stages on screen, shows round-1 verdicts, keeps Samuel's new marks.
(function () {
  const P = new URLSearchParams(location.search);
  const ONLY = P.get("only");
  const FREEZE = P.has("t") ? +P.get("t") : null;
  const A = window.ASSETS || {};
  const VD = window.VERDICTS || { items: {} };
  const V = (code) => (VD.items[code] || ["todo"]);
  const CATS = [
    ["pill", "Pills", "Labels, lists, verdicts, stats. Most beats on the A-roll are a pill, so this is the biggest set."],
    ["box", "Boxes", "Containers: a list, a comparison, a conversation, a result."],
    ["card", "Cards", "One subject per card: an option, a metric, a product, a person, a milestone."],
    ["circle", "Circles", "Hubs, orbits, rings and hand-drawn marks."],
  ];
  const KEY = "motion-gallery-v" + (VD.round || 1);
  let state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };
  if (ONLY) document.body.classList.add("solo");
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

  const main = document.getElementById("main");
  const base = document.getElementById("baseline-strip");
  if (base && A.base) base.innerHTML = A.base.map((b) => `<figure><img src="${b.src}" alt=""><figcaption>${b.cap}</figcaption></figure>`).join("");

  const live = DESIGNS.filter((d) => (ONLY ? d.code === ONLY : V(d.code)[0] !== "drop"));
  const scenes = [];
  CATS.forEach(([cat, title, lede]) => {
    const list = live.filter((d) => d.cat === cat);
    if (!list.length) return;
    const sec = document.createElement("section");
    sec.className = "cat"; sec.dataset.cat = cat; sec.id = "cat-" + cat;
    sec.innerHTML = `<h3>${title} <em>${list.length}</em></h3><p class="lede">${lede}</p><div class="grid2"></div>`;
    main.appendChild(sec);
    const grid = sec.querySelector(".grid2");
    list.forEach((d) => {
      const [verdict, note, done] = V(d.code);
      const card = document.createElement("article");
      card.className = "card"; card.id = d.code; card.dataset.cat = cat; card.dataset.r1 = verdict;
      const refImg = d.ref && d.ref.id && A.refs ? A.refs[d.ref.id] : null;
      const chip = verdict === "approve" ? '<span class="st ok">Approved</span>' : verdict === "change" ? '<span class="st new">Changed for you</span>' : '<span class="st todo">Not reviewed</span>';
      const vnote = note || done ? `<div class="vnote">${note ? `<b>You:</b> <em>“${esc(note)}”</em>${done ? "<br>" : ""}` : ""}${done ? `<b>${verdict === "change" ? "Changed" : "Updated"}:</b> ${esc(done)}` : ""}</div>` : "";
      card.innerHTML = `
        <div class="stage-wrap"><div class="stage-host"></div><span class="code">${d.code}</span>
          <div class="ctl"><button class="rp" title="Replay">↻</button><button class="fs" title="Full screen">⤢</button></div></div>
        <div class="info">
          <div class="r1"><h4>${d.name}</h4>${chip}<div class="dots">${(d.recipe || []).map((c) => `<i style="background:${c}"></i>`).join("")}</div></div>
          ${vnote}
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
        else if (verdict === "approve") card.classList.add("v-approve");
        tally();
      };
      btns.forEach((b) => (b.onclick = () => { st.v = st.v === b.dataset.v ? undefined : b.dataset.v; state[d.code] = st; save(); paint(); applyFilter(); }));
      inp.value = st.note || "";
      inp.oninput = () => { st.note = inp.value; state[d.code] = st; save(); tally(); };
      paint();
    });
  });

  // loop only the stages on screen
  const onScreen = new Set();
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    const sc = e.target.__sc;
    if (e.isIntersecting) { if (!onScreen.has(sc)) sc.t0 = performance.now(); onScreen.add(sc); } else onScreen.delete(sc);
  }), { rootMargin: "100px" });
  scenes.forEach((sc) => io.observe(sc.host));
  const draw = (sc, t) => { try { sc.S.R(t); } catch (e) { if (!sc.err) { sc.err = 1; console.error(sc.code, e); } } };
  const tick = (now) => {
    for (const sc of onScreen) draw(sc, FREEZE != null ? FREEZE : ((now - sc.t0) / 1000) % sc.loop);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  window.RENDER_AT = (t) => scenes.forEach((sc) => draw(sc, t));
  if (FREEZE != null) scenes.forEach((sc) => draw(sc, FREEZE));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") document.querySelectorAll(".card.full").forEach((c) => c.classList.remove("full")); });

  // filters: "review" = what still needs Samuel (changed for him, or never reviewed)
  let filter = ONLY ? "all" : "review";
  function applyFilter() {
    document.querySelectorAll(".card").forEach((c) => {
      const r1 = c.dataset.r1, v = (state[c.id] || {}).v;
      const show = filter === "all" || filter === c.dataset.cat ||
        (filter === "review" && (r1 === "change" || r1 === "todo")) ||
        (filter === "approve" && (v === "approve" || (r1 === "approve" && !v))) ||
        (filter === "change" && v === "change");
      c.style.display = show ? "" : "none";
    });
    document.querySelectorAll("section.cat").forEach((s) => { s.style.display = [...s.querySelectorAll(".card")].some((c) => c.style.display !== "none") ? "" : "none"; });
    document.getElementById("baseline").style.display = filter === "all" ? "" : "none";
    document.querySelectorAll(".tabs button").forEach((x) => x.classList.toggle("on", x.dataset.f === filter));
  }
  document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => { filter = b.dataset.f; applyFilter(); }));
  applyFilter();

  function tally() {
    let ok = 0, ch = 0, todo = 0, dropped = 0;
    DESIGNS.forEach((d) => {
      const r1 = V(d.code)[0], v = (state[d.code] || {}).v;
      if (r1 === "drop") { dropped++; return; }
      if (v === "approve" || (!v && r1 === "approve")) ok++;
      else if (v === "change" || v === "drop") ch++;
      else todo++;
    });
    const el = document.getElementById("tally");
    if (el) el.innerHTML = `<span><b>${ok}</b> approved</span><span><b>${todo}</b> to review</span><span><b>${ch}</b> flagged</span><span><b>${dropped}</b> dropped</span>`;
  }
  tally();

  // review text to paste back into chat
  function reviewText() {
    const lines = [`Motion gallery v${VD.round || 1} review`];
    const tag = { approve: "APPROVE", change: "CHANGE", drop: "DROP" };
    const todo = [];
    live.forEach((d) => {
      const s = state[d.code] || {}, r1 = V(d.code)[0];
      if (!s.v && !s.note) { if (r1 !== "approve") todo.push(d.code); return; }
      lines.push(`${d.code} ${d.name}: ${s.v ? tag[s.v] : "NOTE"}${s.note ? " — " + s.note : ""}`);
    });
    if (todo.length) lines.push("Not reviewed yet: " + todo.join(", "));
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
    if (!confirm("Clear your marks and notes for this round?")) return;
    state = {}; save(); location.reload();
  };
  if (location.hash) { const t = document.querySelector(location.hash); if (t) { filter = "all"; applyFilter(); setTimeout(() => t.scrollIntoView({ block: "center" }), 300); } }
})();
