// Motion gallery engine. A multi-stage port of the visual-engine kit (scripts/visual-engine/scenes/kit.js).
// Same names (el, W, A, F, neo, pop, fade, sweep, count, typeText) so an approved design ports into a
// render scene by dropping the "S." prefix. Deterministic: every stage is drawn from its time t.
(function () {
  const FPS = 24000 / 1001;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
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
    spring: (x) => (x >= 1 ? 1 : 1 - Math.exp(-7 * x) * Math.cos(10 * x)),
  };
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
  const prog = (t, t0, t1, e) => (E[e || "io"])(clamp((t - t0) / (t1 - t0), 0, 1));
  const lerp = (a, b, p) => a + (b - a) * p;
  // deterministic noise for grain and hand-drawn boil
  const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

  // ---------- icons: 24x24 stroke glyphs ----------
  function gearPath(n, ro, ri) {
    const st = (2 * Math.PI) / n, P = (r, a) => `${(12 + r * Math.cos(a)).toFixed(2)} ${(12 + r * Math.sin(a)).toFixed(2)}`;
    let d = "";
    for (let i = 0; i < n; i++) { const a = i * st - Math.PI / 2; d += (i ? " L" : "M") + P(ri, a) + " L" + P(ro, a + st * 0.14) + " L" + P(ro, a + st * 0.4) + " L" + P(ri, a + st * 0.54); }
    return d + " Z";
  }
  const IC = {
    user: '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5c0-4 3.4-6.5 7.5-6.5s7.5 2.5 7.5 6.5"/>',
    users: '<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M15.5 5.2a3.5 3.5 0 0 1 0 6.6"/><path d="M18 14.4c2.1.8 3.5 2.8 3.5 5.6"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
    alert: '<path d="M12 6v7.5"/><path d="M12 17.8v.2"/>',
    question: '<path d="M9.1 9.2a3 3 0 1 1 4.6 2.5c-1 .6-1.7 1.3-1.7 2.4v.3"/><path d="M12 17.8v.2"/>',
    dollar: '<path d="M12 2.8v18.4"/><path d="M16.6 7.2c-.9-1.4-2.5-2.1-4.6-2.1-2.7 0-4.4 1.3-4.4 3.2 0 4.5 9.2 2.5 9.2 7.1 0 2-2 3.4-4.8 3.4-2.4 0-4.2-.9-5-2.5"/>',
    trend: '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    bars: '<path d="M5 20v-9"/><path d="M12 20V5"/><path d="M19 20v-6"/>',
    box: '<path d="M21 7.5l-9-4.5-9 4.5 9 4.5 9-4.5z"/><path d="M3 7.5v9l9 4.5 9-4.5v-9"/><path d="M12 12v9"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    phone: '<path d="M6.5 3.5h3l1.8 4.6-2.3 1.5a11 11 0 0 0 5.4 5.4l1.5-2.3 4.6 1.8v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4.5 5.7a2 2 0 0 1 2-2.2z"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M20.5 20.5l-4.6-4.6"/>',
    bolt: '<path d="M13.5 2.5L4.5 14h7l-1 7.5 9-11.5h-7l1-7.5z"/>',
    target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
    calendar: '<rect x="3" y="4.5" width="18" height="16.5" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
    shield: '<path d="M12 2.8l8 3v6.1c0 4.9-3.4 8.2-8 9.3-4.6-1.1-8-4.4-8-9.3V5.8l8-3z"/><path d="M8.6 12.1l2.4 2.4 4.6-4.6"/>',
    gear: '<path d="' + gearPath(8, 10.4, 7.9) + '"/><circle cx="12" cy="12" r="3.2"/>',
    wrench: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8z"/>',
    link: '<path d="M10 14a4.2 4.2 0 0 0 5.9 0l3-3a4.2 4.2 0 0 0-5.9-5.9l-1.2 1.2"/><path d="M14 10a4.2 4.2 0 0 0-5.9 0l-3 3a4.2 4.2 0 0 0 5.9 5.9l1.2-1.2"/>',
    star: '<path d="M12 3.2l2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3.2z"/>',
    heart: '<path d="M12 20.3S3.2 15 3.2 9.1C3.2 6.3 5.3 4.2 8 4.2c1.7 0 3.1.9 4 2.3.9-1.4 2.3-2.3 4-2.3 2.7 0 4.8 2.1 4.8 4.9 0 5.9-8.8 11.2-8.8 11.2z"/>',
    bookmark: '<path d="M6.5 3.5h11v17.5L12 17l-5.5 4V3.5z"/>',
    send: '<path d="M21.5 2.5L10.8 13.2"/><path d="M21.5 2.5l-6.8 19-3.9-8.3-8.3-3.9 19-6.8z"/>',
    file: '<path d="M14 2.8H6.6a2 2 0 0 0-2 2v14.4a2 2 0 0 0 2 2h10.8a2 2 0 0 0 2-2V8.2L14 2.8z"/><path d="M14 2.8v5.4h5.4"/><path d="M8.5 13h7M8.5 16.5h5"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.8 3.2 2.8 14.8 0 18M12 3c-2.8 3.2-2.8 14.8 0 18"/>',
    lock: '<rect x="4.5" y="10.5" width="15" height="10.5" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    flag: '<path d="M5 21.5V3.5"/><path d="M5 4h12.5l-2.5 4.5 2.5 4.5H5"/>',
    crown: '<path d="M3 8.5l4.6 3.8L12 5l4.4 7.3L21 8.5l-2 10.5H5L3 8.5z"/>',
    building: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7.5h.01M15 7.5h.01M9 11.5h.01M15 11.5h.01M9 15.5h.01M15 15.5h.01"/><path d="M10.5 21v-3h3v3"/>',
    message: '<path d="M4 4.5h16a1.5 1.5 0 0 1 1.5 1.5v10a1.5 1.5 0 0 1-1.5 1.5H9.5L4.5 21v-3.5H4A1.5 1.5 0 0 1 2.5 16V6A1.5 1.5 0 0 1 4 4.5z"/>',
    pen: '<path d="M4 20l1-4.5L16 4.5a2.1 2.1 0 0 1 3 3L8 18.5 4 20z"/><path d="M14 6.5l3 3"/>',
    eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    arrow: '<path d="M4 12h15.5"/><path d="M13.5 6l6 6-6 6"/>',
    sync: '<path d="M20 11.5A8 8 0 0 0 5.4 7"/><path d="M4 12.5A8 8 0 0 0 18.6 17"/><path d="M4.5 3.5V7.5h4"/><path d="M19.5 20.5v-4h-4"/>',
    layers: '<path d="M12 3l9.5 5L12 13 2.5 8 12 3z"/><path d="M2.5 12.5L12 17.5l9.5-5"/><path d="M2.5 16.5L12 21.5l9.5-5"/>',
    tag: '<path d="M3 12.2V4.5A1.5 1.5 0 0 1 4.5 3h7.7l8.8 8.8a1.5 1.5 0 0 1 0 2.1l-7.1 7.1a1.5 1.5 0 0 1-2.1 0L3 12.2z"/><circle cx="7.8" cy="7.8" r="1.4"/>',
    megaphone: '<path d="M3.5 10v4h3l8 5V5l-8 5h-3z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
    spark: '<path d="M12 3v6M12 15v6M3 12h6M15 12h6M5.6 5.6l4.2 4.2M14.2 14.2l4.2 4.2M5.6 18.4l4.2-4.2M14.2 9.8l4.2-4.2"/>',
    play: '<path d="M7 4.5v15l12-7.5-12-7.5z"/>',
    wand: '<path d="M4 20L15 9"/><path d="M17.5 3v3M16 4.5h3M20.5 8v2M19.5 9h2M12.5 3.5v1.6M11.7 4.3h1.6"/>',
    receipt: '<path d="M5 3h14v18l-2.3-1.5L14.3 21 12 19.5 9.7 21l-2.4-1.5L5 21V3z"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4"/>',
  };
  function icon(name, size, color, sw, fill) {
    return `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24" fill="${fill || "none"}" stroke="${color || "currentColor"}" stroke-width="${sw || 2}" stroke-linecap="round" stroke-linejoin="round">${IC[name] || ""}</svg>`;
  }
  // *word* -> accent-coloured word
  const tt = (s, col) => s.replace(/\*([^*]+)\*/g, `<span style="color:${col || "#FF5A1F"}">$1</span>`);

  // hand-drawn loop: an ellipse drawn twice with wobble; seed changes the wobble (boil)
  function rough(cx, cy, rx, ry, seed, turns, jit) {
    turns = turns || 1.15; jit = jit == null ? 0.06 : jit;
    const n = Math.round(64 * turns), pts = [];
    const a0 = -2.2 + hash(seed) * 0.4;
    for (let i = 0; i <= n; i++) {
      const a = a0 + (i / 64) * Math.PI * 2;
      const w = 1 + (hash(seed * 7 + Math.floor(i / 6)) - 0.5) * jit * 2 + Math.sin(a * 3 + seed) * jit * 0.6;
      const grow = 1 + (i / n) * 0.07;
      pts.push([cx + Math.cos(a) * rx * w * grow, cy + Math.sin(a) * ry * w * (2 - grow)]);
    }
    let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
    for (let i = 1; i < pts.length - 1; i++) {
      const mx = (pts[i][0] + pts[i + 1][0]) / 2, my = (pts[i][1] + pts[i + 1][1]) / 2;
      d += ` Q${pts[i][0].toFixed(1)} ${pts[i][1].toFixed(1)} ${mx.toFixed(1)} ${my.toFixed(1)}`;
    }
    return d;
  }

  // ---------- one stage ----------
  function Scene(host, meta) {
    const tracks = [], fns = [];
    const stage = document.createElement("div");
    stage.className = "stage";
    host.appendChild(stage);
    const bg = mk(stage, "layer bg");
    const root = mk(stage, "layer root");
    const over = mk(stage, "layer over");
    function mk(parent, cls, style, html) {
      const d = document.createElement("div");
      if (cls) d.className = cls;
      if (style) Object.assign(d.style, style);
      if (html != null) d.innerHTML = html;
      parent.appendChild(d);
      return d;
    }
    const loop = meta.loop || 6;
    const S = { stage, root, bg, over, FPS, E, clamp, val, prog, lerp, hash, icon, tt, rough, loop };
    S.el = (parent, cls, style, html) => mk(parent || root, cls, style, html);
    S.W = (parent, x, y, w, h, extra) => S.el(parent, "abs fx", Object.assign({ left: x + "px", top: y + "px", width: w != null ? w + "px" : "auto", height: h != null ? h + "px" : "auto" }, extra || {}));
    S.A = (node, props, base) => {
      let tr = tracks.find((q) => q.node === node);
      if (!tr) { tr = { node, props: {}, base: base != null ? base : "" }; tracks.push(tr); }
      for (const k in props) { const v = props[k]; tr.props[k] = typeof v === "number" ? [[0, v]] : v; }
      if (base != null) tr.base = base;
      return node;
    };
    S.F = (cb) => { fns.push(cb); };
    S.neo = (node, t0, o) => {
      o = o || {};
      const d = o.dur || 22 / FPS, dist = o.dist == null ? 70 : o.dist, ang = o.ang == null ? -90 : o.ang;
      const dx = Math.cos((ang * Math.PI) / 180) * dist;
      const dy = -Math.sin((ang * Math.PI) / 180) * dist;
      const p = {
        x: [[t0, dx], [t0 + d, 0, "expo"]],
        y: [[t0, dy], [t0 + d, 0, "expo"]],
        o: [[t0, 0], [t0 + d * 0.45, 1, "out"]],
        blur: [[t0, o.blur == null ? 16 : o.blur], [t0 + d * 0.8, 0, "out"]],
      };
      if (o.s0 != null) p.s = [[t0, o.s0], [t0 + d, 1, "expo"]];
      return S.A(node, p);
    };
    S.pop = (node, t0, o) => {
      o = o || {};
      const d = o.dur || 0.5;
      return S.A(node, { s: [[t0, o.s0 == null ? 0.5 : o.s0], [t0 + d, 1, o.ease || "back"]], o: [[t0, 0], [t0 + d * 0.35, 1, "out"]], blur: [[t0, o.blur == null ? 8 : o.blur], [t0 + d * 0.6, 0, "out"]] });
    };
    S.fade = (node, t0, d, from, to) => S.A(node, { o: [[t0, from == null ? 0 : from], [t0 + (d || 0.4), to == null ? 1 : to, "out"]] });
    S.addSweep = (node, cls) => S.el(node, "sweep" + (cls ? " " + cls : ""));
    S.sweep = (node, t0, d) => {
      const s = node.querySelector(":scope > .sweep") || S.addSweep(node);
      d = d || 1.1;
      S.F((t) => { const p = clamp((t - t0) / d, 0, 1); s.style.transform = `translateX(${-160 + 480 * E.sine(p)}%) skewX(-18deg)`; });
    };
    S.count = (node, t0, t1, a, b, fmt, ease) => {
      S.F((t) => { const v = a + (b - a) * prog(t, t0, t1, ease || "out"); node.textContent = fmt ? fmt(v) : Math.round(v).toLocaleString("en-US"); });
    };
    S.typeText = (node, t0, t1, text, caretNode) => {
      S.F((t) => {
        const n = Math.round(text.length * clamp((t - t0) / (t1 - t0), 0, 1));
        node.textContent = text.slice(0, n);
        if (caretNode) caretNode.style.opacity = t < t0 - 0.3 ? 0 : (n < text.length || Math.floor(t * 2.2) % 2 === 0 ? 1 : 0);
      });
    };
    // clip-path inset reveal: from/to are [top,right,bottom,left] in px
    S.clip = (node, keysFrom, keysTo, t0, t1, r, ease) => {
      S.F((t) => {
        const p = prog(t, t0, t1, ease || "expo");
        const v = keysFrom.map((a, i) => lerp(a, keysTo[i], p).toFixed(1) + "px");
        node.style.clipPath = `inset(${v.join(" ")} round ${r || 0}px)`;
      });
    };
    S.float = (node, amp, speed, phase) => { S.F((t) => { node.style.translate = `0 ${(Math.sin(t * (speed || 1.6) + (phase || 0)) * (amp || 4)).toFixed(2)}px`; }); };
    S.svg = (parent, w, h) => {
      const ns = "http://www.w3.org/2000/svg";
      const s = document.createElementNS(ns, "svg");
      s.setAttribute("width", w || 1920); s.setAttribute("height", h || 1080);
      s.setAttribute("viewBox", `0 0 ${w || 1920} ${h || 1080}`);
      s.style.position = "absolute"; s.style.left = "0"; s.style.top = "0"; s.style.overflow = "visible";
      (parent || root).appendChild(s);
      return s;
    };
    S.node = (svg, tag, attrs) => {
      const n = document.createElementNS("http://www.w3.org/2000/svg", tag);
      for (const k in attrs) n.setAttribute(k, attrs[k]);
      svg.appendChild(n);
      return n;
    };
    S.path = (svg, d, o) => {
      o = o || {};
      return S.node(svg, "path", Object.assign({ d, fill: o.fill || "none", stroke: o.color || "#fff", "stroke-width": o.width || 3, "stroke-linecap": "round", "stroke-linejoin": "round" }, o.dash ? { "stroke-dasharray": o.dash } : {}, o.attrs || {}));
    };
    S.rr = (x, y, w, h, r) => `M${x + r} ${y} H${x + w - r} A${r} ${r} 0 0 1 ${x + w} ${y + r} V${y + h - r} A${r} ${r} 0 0 1 ${x + w - r} ${y + h} H${x + r} A${r} ${r} 0 0 1 ${x} ${y + h - r} V${y + r} A${r} ${r} 0 0 1 ${x + r} ${y} Z`;
    // ring-only mask (border glow and beams): apply to an element with padding = ring width
    S.ringMask = { WebkitMask: "linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)", WebkitMaskComposite: "xor", mask: "linear-gradient(#000 0 0) content-box exclude, linear-gradient(#000 0 0)" };
    S.drawOn = (p, t0, t1, ease, from) => {
      let L = null;
      S.F((t) => {
        if (L == null) { L = p.getTotalLength(); p.style.strokeDasharray = L + " " + (L + 2); }
        const q = prog(t, t0, t1, ease || "io");
        p.style.strokeDashoffset = (L * (1 - lerp(from || 0, 1, q))).toFixed(2);
        p.style.opacity = t < t0 ? 0 : 1;
      });
    };
    S.ripple = (parent, x, y, size, t0, color, dur) => {
      const r = S.el(parent, "abs ripple", { left: x - size / 2 + "px", top: y - size / 2 + "px", width: size + "px", height: size + "px", borderColor: color || "rgba(255,255,255,.8)" });
      S.A(r, { s: [[t0, 0.6], [t0 + (dur || 0.7), 2.3, "out"]], o: [[t0 - 0.01, 0], [t0, 0.9], [t0 + (dur || 0.7), 0, "out"]] });
      return r;
    };
    S.burst = (parent, x, y, t0, n, colors, dist) => {
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2 + hash(i + 3) * 0.5, D = (dist || 120) * (0.7 + hash(i * 3.1) * 0.6), sz = 10 + hash(i * 5.3) * 12;
        const d = S.el(parent, "abs", { left: x - sz / 2 + "px", top: y - sz / 2 + "px", width: sz + "px", height: sz + "px", borderRadius: "50%", background: (colors || ["#FF5A1F", "#FD9457", "#fff"])[i % (colors || [1, 2, 3]).length] });
        S.A(d, { x: [[t0, 0], [t0 + 0.6, Math.cos(a) * D, "out"]], y: [[t0, 0], [t0 + 0.6, Math.sin(a) * D, "out"]], s: [[t0, 0.2], [t0 + 0.15, 1, "out"], [t0 + 0.6, 0.3, "in"]], o: [[t0 - 0.01, 0], [t0, 1], [t0 + 0.45, 1], [t0 + 0.6, 0, "in"]] });
      }
    };
    // grounds and overlays
    S.ground = (kind, opt) => {
      opt = opt || {};
      const g = mk(bg, "gr " + kind);
      if (kind === "aroll") {
        g.style.backgroundImage = `url(${(window.ASSETS && window.ASSETS[opt.src || "aroll"]) || ""})`;
        if (opt.push !== false) S.F((t) => { g.style.transform = `scale(${(1.02 + 0.035 * (t / loop)).toFixed(4)})`; });
        if (opt.shade !== false) mk(bg, "shade");
      }
      if (opt.grid) mk(bg, opt.grid === "dots" ? "dots" : "grid" + (kind === "cream" || kind === "peach" ? " dark" : ""));
      if (opt.vig !== false) mk(over, "vig" + (kind === "cream" || kind === "peach" || kind === "ember" ? " light" : kind === "aroll" ? " soft" : ""));
      if (opt.grain !== false) {
        const gr = mk(over, "grain" + (kind === "cream" || kind === "peach" ? " soft" : ""));
        S.F((t) => { const f = Math.floor(t * 24); gr.style.transform = `translate(${Math.round((hash(f) - 0.5) * 120)}px,${Math.round((hash(f + 9) - 0.5) * 120)}px)`; });
      }
      return g;
    };
    S.R = (t) => {
      for (const tr of tracks) {
        const p = tr.props;
        const g = (k, d) => (p[k] ? val(p[k], t) : d);
        const x = g("x", 0), y = g("y", 0), z = g("z", 0), rx = g("rx", 0), ry = g("ry", 0), rz = g("rz", 0), s = g("s", 1), sx = g("sx", 1), sy = g("sy", 1);
        tr.node.style.transform = `${tr.base} translate3d(${x.toFixed(2)}px,${y.toFixed(2)}px,${z.toFixed(2)}px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) rotateZ(${rz.toFixed(2)}deg) scale(${(s * sx).toFixed(4)},${(s * sy).toFixed(4)})`;
        if (p.o) tr.node.style.opacity = g("o", 1).toFixed(3);
        const blur = g("blur", 0), br = g("br", 1), sat = g("sat", 1);
        const f = [];
        if (blur > 0.05) f.push(`blur(${blur.toFixed(2)}px)`);
        if (Math.abs(br - 1) > 0.001) f.push(`brightness(${br.toFixed(3)})`);
        if (Math.abs(sat - 1) > 0.001) f.push(`saturate(${sat.toFixed(3)})`);
        tr.node.style.filter = f.join(" ");
      }
      for (const cb of fns) cb(t);
      root.style.opacity = (1 - prog(t, loop - 0.45, loop - 0.08, "in")).toFixed(3);
    };
    return S;
  }

  // ---------- registry ----------
  window.DESIGNS = [];
  window.D = (code, meta, build) => { window.DESIGNS.push(Object.assign({ code, build }, meta)); };
  window.MG = { Scene, E, val, prog, icon, tt, FPS };
})();
