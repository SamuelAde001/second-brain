// Route Rise #3 scene engine. Deterministic: the renderer calls R(t) for every frame.
// Scenes use timeline frames through T(frame) so words land on the exact frame.
(function () {
  const P = new URLSearchParams(location.search);
  const FPS = 24000 / 1001;
  window.FPS = FPS;
  window.START = +(P.get("start") || 0);          // beat start (timeline frame)
  window.DUR = +(P.get("dur") || 5);              // seconds
  window.T = (frame) => (frame - START) / FPS;     // timeline frame -> scene seconds
  const stage = document.getElementById("stage");
  window.stage = stage;

  // ---------- easing ----------
  const E = {
    lin: (x) => x,
    in: (x) => x * x * x,
    out: (x) => 1 - Math.pow(1 - x, 3),
    out5: (x) => 1 - Math.pow(1 - x, 5),
    expo: (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
    io: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
    back: (x) => { const c1 = 1.55, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    back2: (x) => { const c1 = 2.2, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  };
  window.EASE = E;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  window.clamp = clamp;
  // value of a keyed track at time t. keys: [[t, v, ease?], ...] (ease applies on the way INTO that key)
  function val(keys, t) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1, e] = keys[i];
      if (t <= t1) {
        const [t0, v0] = keys[i - 1];
        const p = t1 === t0 ? 1 : (t - t0) / (t1 - t0);
        return v0 + (v1 - v0) * (E[e || "io"])(clamp(p, 0, 1));
      }
    }
    return keys[keys.length - 1][1];
  }
  window.val = val;
  window.prog = (t, t0, t1, e) => (E[e || "io"])(clamp((t - t0) / (t1 - t0), 0, 1));

  // ---------- DOM ----------
  window.el = function (parent, cls, style, html) {
    const d = document.createElement("div");
    if (cls) d.className = cls;
    if (style) Object.assign(d.style, style);
    if (html != null) d.innerHTML = html;
    (parent || stage).appendChild(d);
    return d;
  };
  // wrapper that receives animation (transform/opacity/blur); content goes inside it
  window.W = function (parent, x, y, w, h, extra) {
    const d = el(parent, "abs fx", Object.assign({ left: x + "px", top: y + "px", width: w != null ? w + "px" : "auto", height: h != null ? h + "px" : "auto" }, extra || {}));
    return d;
  };
  window.icon = function (name, size, color) {
    return `<span class="ico" style="width:${size}px;height:${size}px;color:${color || "currentColor"};-webkit-mask-image:url('../_assets/icons/${name}.png')"></span>`;
  };
  window.img = (src) => `url('${src}')`;

  // ---------- animation registry ----------
  const tracks = [];
  const fns = [];
  const DEF = { x: 0, y: 0, z: 0, rx: 0, ry: 0, rz: 0, s: 1, sx: 1, sy: 1, o: 1, blur: 0, br: 1, sat: 1 };
  window.A = function (node, props, base) {
    let tr = tracks.find((q) => q.node === node);
    if (!tr) { tr = { node, props: {}, base: base != null ? base : node.dataset.base || "" }; tracks.push(tr); }
    for (const k in props) {
      const v = props[k];
      tr.props[k] = typeof v === "number" ? [[0, v]] : v;
    }
    if (base != null) tr.base = base;
    return node;
  };
  window.F = function (cb) { fns.push(cb); };

  // NeoAnim: slide in from an angle with start blur (measured house values: 20–25 f, blur 5.5–25)
  window.neo = function (node, t0, o) {
    o = o || {};
    const d = o.dur || 22 / FPS, dist = o.dist == null ? 70 : o.dist, ang = o.ang == null ? -90 : o.ang;
    const dx = -Math.cos((ang * Math.PI) / 180) * dist * (o.flip ? -1 : 1);
    const dy = -Math.sin((ang * Math.PI) / 180) * dist;
    const p = {
      x: [[t0, (o.x0 || 0) + dx * -1], [t0 + d, o.x0 || 0, "expo"]],
      y: [[t0, (o.y0 || 0) + dy * -1], [t0 + d, o.y0 || 0, "expo"]],
      o: [[t0, 0], [t0 + d * 0.45, 1, "out"]],
      blur: [[t0, o.blur == null ? 16 : o.blur], [t0 + d * 0.8, 0, "out"]],
    };
    if (o.s0 != null) p.s = [[t0, o.s0], [t0 + d, 1, "expo"]];
    if (o.out) { // animate out at o.out
      const t2 = o.out, d2 = o.outDur || 0.35;
      p.o.push([t2, 1], [t2 + d2, 0, "in"]);
      p.y.push([t2, o.y0 || 0], [t2 + d2, (o.y0 || 0) - 40, "in"]);
      p.blur.push([t2, 0], [t2 + d2, 10, "in"]);
    }
    return A(node, p);
  };
  window.pop = function (node, t0, o) {
    o = o || {};
    const d = o.dur || 0.5;
    return A(node, { s: [[t0, o.s0 == null ? 0.5 : o.s0], [t0 + d, 1, o.ease || "back"]], o: [[t0, 0], [t0 + d * 0.35, 1, "out"]], blur: [[t0, o.blur == null ? 8 : o.blur], [t0 + d * 0.6, 0, "out"]] });
  };
  window.fade = function (node, t0, d, from, to) { return A(node, { o: [[t0, from == null ? 0 : from], [t0 + (d || 0.4), to == null ? 1 : to, "out"]] }); };
  // NeoLightSweep: one pass of the band across .sweep inside node
  window.sweep = function (node, t0, d) {
    const s = node.querySelector(".sweep") || el(node, "sweep");
    d = d || 1.1;
    F((t) => { const p = clamp((t - t0) / d, 0, 1); s.style.transform = `translateX(${-120 + 240 * E.sine(p)}%)`; });
  };
  window.addSweep = (node) => el(node, "sweep");
  // counters and typing
  window.count = function (node, t0, t1, a, b, fmt, ease) {
    F((t) => { const v = a + (b - a) * prog(t, t0, t1, ease || "out"); node.textContent = fmt ? fmt(v) : Math.round(v).toLocaleString("en-US"); });
  };
  window.typeText = function (node, t0, t1, text, caret) {
    F((t) => {
      const n = Math.round(text.length * clamp((t - t0) / (t1 - t0), 0, 1));
      node.textContent = text.slice(0, n);
      if (caret) node.classList.toggle("caret-on", t > t0 - 0.2 && n < text.length);
    });
  };
  // words timed across [t0,t1] (used for word-synced prompts)
  window.words = function (node, items) { // items: [[t, "word "], ...]
    F((t) => { node.textContent = items.filter((w) => w[0] <= t).map((w) => w[1]).join(""); });
  };

  // ---------- frame ----------
  function apply(t) {
    for (const tr of tracks) {
      const v = {};
      for (const k in DEF) v[k] = tr.props[k] ? val(tr.props[k], t) : DEF[k];
      const tf = `${tr.base} translate3d(${v.x}px,${v.y}px,${v.z}px) rotateX(${v.rx}deg) rotateY(${v.ry}deg) rotateZ(${v.rz}deg) scale(${v.s * v.sx},${v.s * v.sy})`;
      tr.node.style.transform = tf;
      tr.node.style.opacity = v.o;
      const f = [];
      if (v.blur > 0.05) f.push(`blur(${v.blur}px)`);
      if (v.br !== 1) f.push(`brightness(${v.br})`);
      if (v.sat !== 1) f.push(`saturate(${v.sat})`);
      tr.node.style.filter = f.join(" ");
    }
    for (const cb of fns) cb(t);
  }
  window.AWAIT = [];
  window.R = async function (t) { apply(t); const w = AWAIT.splice(0); if (w.length) await Promise.all(w); return true; };
  // an <img> that shows the lip-synced A-roll frame for the current scene time
  window.arollImg = function (parent, style) {
    const im = document.createElement("img");
    Object.assign(im.style, { position: "absolute", objectFit: "cover" }, style || {});
    parent.appendChild(im);
    const id = P.get("id");
    let last = -1;
    F((t) => {
      const i = Math.min(Math.round(t * FPS), Math.round(DUR * FPS) - 1);
      if (i === last) return; last = i;
      im.src = `../_assets/aroll/${id}/f${String(i).padStart(5, "0")}.jpg`;
      AWAIT.push(im.decode().catch(() => {}));
    });
    return im;
  };
  window.READY = () => (async () => {
    await document.fonts.ready;
    const imgs = [...document.images].filter((i) => !i.complete);
    await Promise.all(imgs.map((i) => new Promise((r) => { i.onload = i.onerror = r; })));
    // background-image urls
    const urls = new Set();
    document.querySelectorAll("*").forEach((n) => { const b = getComputedStyle(n).backgroundImage; (b.match(/url\("?([^")]+)"?\)/g) || []).forEach((u) => urls.add(u.replace(/^url\("?|"?\)$/g, ""))); });
    await Promise.all([...urls].map((u) => new Promise((r) => { const i = new Image(); i.onload = i.onerror = r; i.src = u; })));
    apply(0);
    return true;
  })();
})();
