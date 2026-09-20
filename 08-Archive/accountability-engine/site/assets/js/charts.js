/* ============================================================================
   Samuelsignals OS — chart engine

   Hand-rolled SVG. No library, no CDN, no build step.

   Three reasons it is written rather than imported:
     1. It cannot break because someone else's CDN went down.
     2. Every chart matches the design system exactly instead of approximately.
     3. The charts that matter here are odd shapes — a bed-time-against-a-floor
        plot, a 37-lesson grid, a habit heatmap. A generic library fights you on
        all three.

   Every chart renders into a viewBox and scales to its container, so the same
   code works on a phone and a monitor.
   ========================================================================= */

const NS = 'http://www.w3.org/2000/svg';

const C = {
  green: '#35d870', amber: '#f5a623', red: '#ef4444', blue: '#4a90e2',
  violet: '#7b61ff', pink: '#ef4d8f', teal: '#02dbb2',
  grid: '#232c3a', axis: '#2f3a4a', dim: '#56616f', muted: '#7c8899',
  surface3: '#1e2632', text: '#e8eef7',
};

function el(tag, attrs = {}, parent = null) {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}

/* fixed = keep the drawing at its natural size and only shrink on narrow
   screens. Grid charts (heatmap, lesson grid, streak, arc) have a small
   intrinsic width, and letting the viewBox stretch them to the card width
   blows a 190px-tall heatmap up to 570px of mostly whitespace. */
function svg(host, w, h, fixed = false) {
  host.innerHTML = '';
  const attrs = {
    class: 'chart', viewBox: `0 0 ${w} ${h}`,
    preserveAspectRatio: 'xMidYMid meet', role: 'img',
  };
  if (fixed) {
    attrs.class = 'chart fixed';
    attrs.width = w;
    attrs.height = h;
  }
  return el('svg', attrs, host);
}

function niceMax(v, step) {
  if (!isFinite(v) || v <= 0) return step || 1;
  const s = step || Math.pow(10, Math.floor(Math.log10(v)));
  return Math.ceil(v / s) * s;
}

function shortDate(iso) {
  const d = new Date(iso + 'T00:00:00');
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
}

function tooltip(node, text) {
  if (!text) return node;
  const t = el('title', {}, node);
  t.textContent = text;
  return node;
}

/* -------------------------------------------------------- axes + plot frame */

function frame(s, { w, h, pad, yMax, yMin = 0, yTicks = 4, yFmt = v => v, xLabels = [], xEvery = 1 }) {
  const P = Object.assign({ t: 14, r: 14, b: 28, l: 40 }, pad || {});
  const pw = w - P.l - P.r;
  const ph = h - P.t - P.b;
  const yScale = v => P.t + ph - ((v - yMin) / (yMax - yMin)) * ph;
  const xScale = (i, n) => n <= 1 ? P.l + pw / 2 : P.l + (i / (n - 1)) * pw;
  const xBand = (i, n) => P.l + (pw / n) * (i + 0.5);

  for (let i = 0; i <= yTicks; i++) {
    const v = yMin + ((yMax - yMin) / yTicks) * i;
    const y = yScale(v);
    el('line', { class: 'grid-line', x1: P.l, y1: y, x2: w - P.r, y2: y }, s);
    const tx = el('text', { class: 'lbl-y', x: P.l - 8, y: y + 3.5 }, s);
    tx.textContent = yFmt(v);
  }
  el('line', { class: 'axis', x1: P.l, y1: P.t, x2: P.l, y2: P.t + ph }, s);

  xLabels.forEach((lab, i) => {
    if (i % xEvery !== 0 && i !== xLabels.length - 1) return;
    const x = xLabels.length <= 1 ? P.l + pw / 2 : xScale(i, xLabels.length);
    const tx = el('text', { class: 'lbl-x', x, y: h - 9 }, s);
    tx.textContent = lab;
  });

  return { P, pw, ph, yScale, xScale, xBand };
}

function threshold(s, f, w, value, colour, label) {
  const y = f.yScale(value);
  el('line', { class: 'thresh', x1: f.P.l, y1: y, x2: w - f.P.r, y2: y, stroke: colour, opacity: .75 }, s);
  if (label) {
    const t = el('text', { x: w - f.P.r, y: y - 5, 'text-anchor': 'end', fill: colour, 'font-size': 9.5 }, s);
    t.textContent = label;
  }
}

/* ------------------------------------------------------------- 1. line chart */

function lineChart(host, data, opts = {}) {
  if (!host) return;
  const pts = data.filter(d => d.value !== null && d.value !== undefined);
  if (!pts.length) { host.innerHTML = '<p class="tiny">No data yet.</p>'; return; }

  const w = opts.width || 760, h = opts.height || 240;
  const s = svg(host, w, h);
  const yMax = opts.yMax || niceMax(Math.max(...pts.map(d => d.value)), 25);
  const f = frame(s, {
    w, h, yMax, yTicks: opts.yTicks || 4,
    yFmt: opts.yFmt || (v => Math.round(v)),
    xLabels: data.map(d => shortDate(d.date)),
    xEvery: Math.max(1, Math.ceil(data.length / (opts.maxXLabels || 7))),
  });

  (opts.thresholds || []).forEach(t => threshold(s, f, w, t.value, t.colour, t.label));

  const grad = el('linearGradient', { id: 'lg-' + (opts.id || 'x'), x1: 0, y1: 0, x2: 0, y2: 1 },
    el('defs', {}, s));
  el('stop', { offset: '0%', 'stop-color': opts.colour || C.blue, 'stop-opacity': .28 }, grad);
  el('stop', { offset: '100%', 'stop-color': opts.colour || C.blue, 'stop-opacity': 0 }, grad);

  const xy = data.map((d, i) => ({ ...d, x: f.xScale(i, data.length), y: d.value == null ? null : f.yScale(d.value) }));
  const solid = xy.filter(p => p.y !== null);

  const dPath = solid.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
  if (solid.length > 1) {
    el('path', {
      d: `${dPath} L${solid[solid.length - 1].x.toFixed(1)},${f.P.t + f.ph} L${solid[0].x.toFixed(1)},${f.P.t + f.ph} Z`,
      fill: `url(#lg-${opts.id || 'x'})`, stroke: 'none',
    }, s);
  }
  el('path', {
    d: dPath, fill: 'none', stroke: opts.colour || C.blue,
    'stroke-width': 2.5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round',
  }, s);

  solid.forEach(p => {
    const col = opts.dotColour ? opts.dotColour(p) : (opts.colour || C.blue);
    el('circle', { cx: p.x, cy: p.y, r: 4.5, fill: '#0d1016', stroke: col, 'stroke-width': 2.5 }, s);
    tooltip(el('circle', { cx: p.x, cy: p.y, r: 13, fill: 'transparent' }, s),
      p.label || `${shortDate(p.date)} — ${p.value}`);
  });
  return s;
}

/* ---------------------------------------------- 2. grouped / threshold bars */

function barChart(host, data, opts = {}) {
  if (!host) return;
  if (!data.length) { host.innerHTML = '<p class="tiny">No data yet.</p>'; return; }

  const w = opts.width || 760, h = opts.height || 240;
  const s = svg(host, w, h);
  const series = opts.series || [{ key: 'value', colour: C.blue, name: '' }];
  const maxV = Math.max(
    ...data.flatMap(d => series.map(se => d[se.key] || 0)),
    ...(opts.thresholds || []).map(t => t.value)
  );
  const yMax = opts.yMax || niceMax(maxV, opts.yStep || 4);
  const f = frame(s, {
    w, h, yMax, yTicks: opts.yTicks || 4,
    yFmt: opts.yFmt || (v => v % 1 ? v.toFixed(1) : v),
    xLabels: data.map(d => d.label || shortDate(d.date)),
    xEvery: Math.max(1, Math.ceil(data.length / (opts.maxXLabels || 7))),
  });

  const bandW = f.pw / data.length;
  const inner = Math.min(bandW * 0.62, 46);
  const barW = inner / series.length;

  data.forEach((d, i) => {
    const cx = f.P.l + bandW * (i + 0.5);
    series.forEach((se, j) => {
      const v = d[se.key];
      if (v === null || v === undefined) return;
      const y = f.yScale(Math.max(v, 0));
      const bh = Math.max(f.P.t + f.ph - y, v > 0 ? 2 : 0);
      const x = cx - inner / 2 + j * barW;
      const colour = typeof se.colour === 'function' ? se.colour(d) : se.colour;
      const r = el('rect', {
        x: x + 1, y, width: Math.max(barW - 2, 2), height: bh,
        rx: 3, fill: colour, opacity: se.opacity ?? 1,
      }, s);
      tooltip(r, `${d.label || shortDate(d.date)} — ${se.name || se.key}: ${v}`);
    });
  });

  (opts.thresholds || []).forEach(t => threshold(s, f, w, t.value, t.colour, t.label));
  return s;
}

/* ------------------------------------------ 3. bed time against the 10:30 floor */

/* The most important chart on the site. Plots what time he actually went to bed
   against the 22:30 floor, so a run of 1:30am nights is a shape, not a sentence. */
function bedChart(host, data, opts = {}) {
  if (!host) return;
  const pts = data.filter(d => d.bed);
  if (!pts.length) { host.innerHTML = '<p class="tiny">No bed times recorded yet.</p>'; return; }

  const w = opts.width || 760, h = opts.height || 250;
  const s = svg(host, w, h);

  // Minutes from 18:00. Anything after midnight wraps forward, so later is lower.
  const toMin = bed => {
    const [H, M] = bed.split(':').map(Number);
    let m = H * 60 + M;
    if (m < 12 * 60) m += 24 * 60;   // 01:30 -> 25:30
    return m - 18 * 60;               // 0 = 6pm
  };
  const floorMin = toMin('22:30');
  const maxMin = Math.max(...pts.map(p => toMin(p.bed)), floorMin + 60) + 45;

  const P = { t: 14, r: 14, b: 28, l: 52 };
  const pw = w - P.l - P.r, ph = h - P.t - P.b;
  const y = m => P.t + (m / maxMin) * ph;
  const x = i => data.length <= 1 ? P.l + pw / 2 : P.l + (i / (data.length - 1)) * pw;

  for (let m = 0; m <= maxMin; m += 120) {
    const yy = y(m);
    el('line', { class: 'grid-line', x1: P.l, y1: yy, x2: w - P.r, y2: yy }, s);
    const hh = Math.floor((m + 18 * 60) / 60) % 24;
    const t = el('text', { class: 'lbl-y', x: P.l - 8, y: yy + 3.5 }, s);
    t.textContent = `${((hh + 11) % 12) + 1}${hh < 12 || hh === 24 ? 'am' : 'pm'}`;
  }

  // the floor
  const fy = y(floorMin);
  el('rect', { x: P.l, y: P.t, width: pw, height: fy - P.t, fill: C.green, opacity: .06 }, s);
  el('line', { class: 'thresh', x1: P.l, y1: fy, x2: w - P.r, y2: fy, stroke: C.green, 'stroke-width': 1.5 }, s);
  const fl = el('text', { x: w - P.r, y: fy - 6, 'text-anchor': 'end', fill: C.green, 'font-size': 9.5 }, s);
  fl.textContent = '10:30pm floor — 7h';

  const xy = data.map((d, i) => d.bed ? { ...d, cx: x(i), cy: y(toMin(d.bed)) } : { ...d, cx: x(i), cy: null });
  const solid = xy.filter(p => p.cy !== null);

  if (solid.length > 1) {
    el('path', {
      d: solid.map((p, i) => `${i ? 'L' : 'M'}${p.cx.toFixed(1)},${p.cy.toFixed(1)}`).join(' '),
      fill: 'none', stroke: C.violet, 'stroke-width': 2, opacity: .5,
      'stroke-dasharray': '5 4',
    }, s);
  }

  solid.forEach(p => {
    const late = toMin(p.bed) > floorMin;
    el('line', { x1: p.cx, y1: fy, x2: p.cx, y2: p.cy, stroke: late ? C.red : C.green, 'stroke-width': 2, opacity: .45 }, s);
    el('circle', { cx: p.cx, cy: p.cy, r: 5.5, fill: '#0d1016', stroke: late ? C.red : C.green, 'stroke-width': 2.5 }, s);
    tooltip(el('circle', { cx: p.cx, cy: p.cy, r: 14, fill: 'transparent' }, s),
      `${shortDate(p.date)} — bed ${p.bedLabel || p.bed}${p.slept ? ` (${p.slept}h)` : ''}`);
  });

  data.forEach((d, i) => {
    const t = el('text', { class: 'lbl-x', x: x(i), y: h - 9 }, s);
    t.textContent = shortDate(d.date);
  });
  return s;
}

/* ---------------------------------------------------- 4. stacked components */

function stackedBar(host, data, opts = {}) {
  if (!host) return;
  const w = opts.width || 760, h = opts.height || 210;
  const s = svg(host, w, h);
  const keys = opts.keys;
  const yMax = opts.yMax || 100;
  const f = frame(s, {
    w, h, yMax, yTicks: 4, yFmt: v => Math.round(v),
    xLabels: data.map(d => shortDate(d.date)),
    xEvery: Math.max(1, Math.ceil(data.length / (opts.maxXLabels || 7))),
  });
  const bandW = f.pw / data.length;
  const barW = Math.min(bandW * 0.55, 52);

  data.forEach((d, i) => {
    const cx = f.P.l + bandW * (i + 0.5);
    let acc = 0;
    keys.forEach(k => {
      const v = d[k.key] || 0;
      if (!v) return;
      const yTop = f.yScale(acc + v), yBot = f.yScale(acc);
      const r = el('rect', {
        x: cx - barW / 2, y: yTop, width: barW, height: Math.max(yBot - yTop, 1),
        fill: k.colour, rx: 2,
      }, s);
      tooltip(r, `${shortDate(d.date)} — ${k.name}: ${v.toFixed(1)}`);
      acc += v;
    });
    if (d.penalty) {
      const yTop = f.yScale(acc);
      el('rect', { x: cx - barW / 2, y: yTop - 3, width: barW, height: 3, fill: C.red }, s);
    }
  });
  return s;
}

/* --------------------------------------------------------- 5. horizontal bars */

function hBars(host, data, opts = {}) {
  if (!host) return;
  if (!data.length) { host.innerHTML = '<p class="tiny">Nothing to show.</p>'; return; }

  const rowH = opts.rowH || 30;
  const w = opts.width || 700;
  const labelW = opts.labelW || 150;
  const valueW = opts.valueW || 108;
  const h = data.length * rowH + 8;
  const s = svg(host, w, h);
  const barMax = w - labelW - valueW - 14;
  const max = opts.max || Math.max(...data.flatMap(d => [d.value || 0, d.compare || 0]), 1);

  data.forEach((d, i) => {
    const y = i * rowH + 4;
    const lab = el('text', { x: 0, y: y + rowH / 2 + 1, fill: C.text, 'font-size': 12.5,
      'font-family': "'Inter',sans-serif" }, s);
    lab.textContent = d.label.length > 22 ? d.label.slice(0, 21) + '…' : d.label;
    if (d.label.length > 22) tooltip(lab, d.label);

    const bh = 9;
    const by = y + rowH / 2 - bh / 2;

    // the plan, behind
    if (d.compare != null) {
      el('rect', { x: labelW, y: by, width: Math.max((d.compare / max) * barMax, 1), height: bh,
        rx: 4.5, fill: C.surface3 }, s);
    }
    const colour = typeof opts.colour === 'function' ? opts.colour(d) : (opts.colour || C.blue);
    const bw = Math.max((Math.abs(d.value || 0) / max) * barMax, d.value ? 2 : 0);
    tooltip(el('rect', { x: labelW, y: by, width: bw, height: bh, rx: 4.5, fill: colour }, s),
      `${d.label} — ${opts.fmt ? opts.fmt(d.value) : d.value}${d.compare != null ? ` of ${opts.fmt ? opts.fmt(d.compare) : d.compare}` : ''}`);

    const val = el('text', { x: w, y: y + rowH / 2 + 1, 'text-anchor': 'end',
      fill: d.valueColour || C.muted, 'font-size': 11.5 }, s);
    val.textContent = opts.fmt ? opts.fmt(d.value) : String(d.value);
  });
  return s;
}

/* ------------------------------------------------------------ 6. progress arc */

function arc(host, pct, opts = {}) {
  if (!host) return;
  const size = opts.size || 148, sw = opts.stroke || 12;
  const s = svg(host, size, size, true);
  const r = (size - sw) / 2, cx = size / 2, cy = size / 2;
  const circ = 2 * Math.PI * r;
  const p = Math.max(0, Math.min(pct, 100));

  el('circle', { cx, cy, r, fill: 'none', stroke: C.surface3, 'stroke-width': sw }, s);
  el('circle', {
    cx, cy, r, fill: 'none', stroke: opts.colour || C.green, 'stroke-width': sw,
    'stroke-linecap': 'round', 'stroke-dasharray': `${(p / 100) * circ} ${circ}`,
    transform: `rotate(-90 ${cx} ${cy})`,
  }, s);

  const t1 = el('text', {
    x: cx, y: cy + 3, 'text-anchor': 'middle', fill: C.text,
    'font-size': opts.big || 27, 'font-weight': 700, 'font-family': "'JetBrains Mono',monospace",
  }, s);
  t1.textContent = opts.centre != null ? opts.centre : `${Math.round(p)}%`;
  if (opts.sub) {
    const t2 = el('text', { x: cx, y: cy + 21, 'text-anchor': 'middle', fill: C.dim, 'font-size': 10.5 }, s);
    t2.textContent = opts.sub;
  }
  return s;
}

/* -------------------------------------------------------------- 7. sparkline */

function spark(host, values, opts = {}) {
  if (!host || !values.length) return;
  const w = opts.width || 120, h = opts.height || 30;
  const s = svg(host, w, h);
  const vals = values.filter(v => v != null);
  if (!vals.length) return;
  const max = Math.max(...vals), min = Math.min(...vals);
  const range = max - min || 1;
  const pts = values.map((v, i) => v == null ? null : {
    x: (i / Math.max(values.length - 1, 1)) * (w - 4) + 2,
    y: h - 3 - ((v - min) / range) * (h - 6),
  }).filter(Boolean);
  el('path', {
    d: pts.map((p, i) => `${i ? 'L' : 'M'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' '),
    fill: 'none', stroke: opts.colour || C.blue, 'stroke-width': 2,
    'stroke-linecap': 'round', 'stroke-linejoin': 'round',
  }, s);
  const last = pts[pts.length - 1];
  el('circle', { cx: last.x, cy: last.y, r: 2.5, fill: opts.colour || C.blue }, s);
  return s;
}

/* --------------------------------------------------------- 8. habit heatmap */

function heatmap(host, habits, dates, lookup, opts = {}) {
  if (!host) return;
  const cell = opts.cell || 19, gap = 4, labelW = opts.labelW || 132;
  const w = labelW + dates.length * (cell + gap);
  const h = habits.length * (cell + gap) + 22;
  const s = svg(host, Math.max(w, 320), h, true);

  dates.forEach((d, i) => {
    const t = el('text', {
      x: labelW + i * (cell + gap) + cell / 2, y: 10,
      'text-anchor': 'middle', fill: C.dim, 'font-size': 9,
    }, s);
    t.textContent = new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: 'numeric' });
  });

  habits.forEach((hb, r) => {
    const y = 22 + r * (cell + gap);
    const t = el('text', { x: 0, y: y + cell / 2 + 4, fill: C.muted, 'font-size': 11.5,
      'font-family': "'Inter',sans-serif" }, s);
    t.textContent = hb.length > 19 ? hb.slice(0, 18) + '…' : hb;
    if (hb.length > 19) tooltip(t, hb);

    dates.forEach((d, i) => {
      const state = lookup(hb, d);       // true | false | null
      const fill = state === true ? C.green : state === false ? C.red : C.surface3;
      const rect = el('rect', {
        x: labelW + i * (cell + gap), y, width: cell, height: cell, rx: 4,
        fill, opacity: state === null ? .5 : 1,
        stroke: state === null ? C.grid : 'none',
      }, s);
      tooltip(rect, `${hb} — ${shortDate(d)}: ${state === true ? 'hit' : state === false ? 'BROKEN' : 'not tracked'}`);
    });
  });
  return s;
}

/* ----------------------------------------------------------- 9. lesson grid */

function lessonGrid(host, lessons, opts = {}) {
  if (!host) return;
  const cols = opts.cols || 13, cell = 26, gap = 5;
  const rows = Math.ceil(lessons.length / cols);
  const w = cols * (cell + gap), h = rows * (cell + gap);
  const s = svg(host, w, h, true);
  const colours = {
    recorded: C.green, edited: C.violet, published: C.teal,
    planned: C.amber, 'not started': C.surface3,
  };
  lessons.forEach((l, i) => {
    const cx = (i % cols) * (cell + gap), cy = Math.floor(i / cols) * (cell + gap);
    const fill = colours[l.status] || C.surface3;
    const g = el('g', {}, s);
    el('rect', {
      x: cx, y: cy, width: cell, height: cell, rx: 6, fill,
      stroke: l.gate ? C.amber : (l.status === 'not started' ? C.grid : 'none'),
      'stroke-width': l.gate ? 2 : 1,
    }, g);
    const t = el('text', {
      x: cx + cell / 2, y: cy + cell / 2 + 3.5, 'text-anchor': 'middle',
      fill: l.status === 'not started' ? C.dim : '#06120b',
      'font-size': 10, 'font-weight': 700,
    }, g);
    t.textContent = l.n;
    tooltip(g, `${l.n}. ${l.name} — ${l.status}${l.due ? ` (due ${shortDate(l.due)})` : ''}${l.gate ? ' — GATES THE LAUNCH' : ''}`);
  });
  return s;
}

/* -------------------------------------------------------- 10. streak strip */

function streak(host, cells, opts = {}) {
  if (!host) return;
  const cell = opts.cell || 22, gap = 4;
  const w = cells.length * (cell + gap), h = cell + 18;
  const s = svg(host, Math.max(w, 200), h, true);
  cells.forEach((c, i) => {
    const fill = c.state === 'hit' ? C.green : c.state === 'miss' ? C.red :
                 c.state === 'due' ? C.surface3 : C.surface3;
    const g = el('g', {}, s);
    el('rect', {
      x: i * (cell + gap), y: 0, width: cell, height: cell, rx: 5, fill,
      stroke: c.state === 'due' ? C.amber : (c.state === 'future' ? C.grid : 'none'),
      'stroke-width': c.state === 'due' ? 2 : 1,
      'stroke-dasharray': c.state === 'future' ? '3 2' : null,
    }, g);
    tooltip(g, c.label || '');
    if (c.tick) {
      const t = el('text', { x: i * (cell + gap) + cell / 2, y: h - 5,
        'text-anchor': 'middle', fill: C.dim, 'font-size': 9 }, s);
      t.textContent = c.tick;
    }
  });
  return s;
}

window.SSCharts = { lineChart, barChart, bedChart, stackedBar, hBars, arc, spark, heatmap, lessonGrid, streak, COLOURS: C, shortDate };
