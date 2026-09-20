/* Samuelsignals OS — Systems. How the engine runs, and how this site is built. */

(function () {
  const S = window.SS, OS = S.OS;
  const { h, time12, statCard, callout, toggle, table, pageHead, doc } = S;

  S.chrome('systems');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const B = OS.body;
  const gen = OS.generated ? new Date(OS.generated) : null;

  const T = (OS.rules || {}).touches || {};

  add(pageHead('Systems', 'How the engine runs, and how this site gets built.',
    (T.lede || '') +
    '<strong>Nothing here is a database — that is deliberate.</strong>'));

  add(h('div', { class: 'grid g4 tight' },
    statCard(T.stat_label || '—', T.stat_value || '—', T.stat_sub || ''),
    statCard('Skills', '9', 'each declares exactly what it reads'),
    statCard('Engine cost', `${B.pa_weekly_hours}h`, 'per week, of his actual time', 'amber'),
    statCard('Days on record', String(OS.summary.days_recorded), gen ? `built ${gen.toLocaleDateString('en-GB')}` : '')));

  /* -------------------------------------------------------- the routines */

  add(h('h2', {}, T.heading || 'Check-ins'));
  add(h('div', { class: 'card pad-0' },
    table(['Session', 'When (WAT)', 'Does', 'Model'],
      (T.rows || []).map(([a, b, c, d]) => [a, b, h('code', {}, c), d]))));
  add(h('p', { class: 'tiny', style: 'margin-top:9px' }, T.footnote || ''));

  /* ------------------------------------------------------ architecture */

  add(h('h2', {}, 'How this site is built'));
  add(notesFor('systems', 'n1'));

  add(h('div', { class: 'card', style: 'margin-top:12px' },
    h('pre', { style: 'margin:0;background:var(--bg);border:1px solid var(--border);border-radius:9px;padding:14px 16px;overflow-x:auto' },
      h('code', { style: 'font-family:var(--mono);font-size:12.5px;line-height:1.7;color:var(--text-2)' },
`context/*.md            the record — written by the check-ins
context/site.json       the numbers that only live in prose
tools/sheets/plan.json  every budget line item
        │
        ▼
tools/site/build.py     parses the tables, computes the scores
        │
        ▼
site/data/os.json       the whole state, one file
site/data/os.js         the same, as a script (so file:// works)
        │
        ▼
site/                   static HTML + hand-rolled SVG charts`))));

  add(h('div', { class: 'card', style: 'margin-top:12px' },
    h('div', { class: 'card-h' }, h('h3', {}, 'Rebuild it')),
    h('pre', { style: 'margin:0;background:var(--bg);border:1px solid var(--border);border-radius:9px;padding:14px 16px' },
      h('code', { style: 'font-family:var(--mono);font-size:12.5px;color:var(--teal)' },
        'python tools/site/build.py')),
    h('p', { class: 'chart-note' },
      'Run it after any check-in that writes to ', h('code', {}, 'context/'),
      '. The reckoning does it automatically.')));

  /* ------------------------------------------------------ cost discipline */

  add(h('h2', {}, 'Cost discipline'));
  add(notesFor('systems', 'n2'));
  const COST = (OS.rules || {}).cost || [];
  add(h('div', { class: 'card', style: 'margin-top:10px' }, h('div', { class: 'rows' },
    COST.map(([t, s]) => h('div', { class: 'row' },
      h('div', { class: 'grow' }, h('div', { class: 't' }, t), h('div', { class: 's' }, s)))))));

  /* -------------------------------------------------------- the sessions */

  add(h('h2', {}, 'What the engine costs him'));
  add(h('div', { class: 'card' },
    h('div', { class: 'rows' }, B.pa_sessions.map(p => h('div', { class: 'row' },
      h('div', { class: 'r mono', style: 'min-width:62px;font-weight:700' }, time12(p.time)),
      h('div', { class: 'grow' }, h('div', { class: 't' }, p.label)),
      h('div', { class: 'r mono t-dim' }, p.minutes + ' min')))),
    h('p', { class: 'chart-note' },
      `That is 1h30m every weekday, ${B.pa_weekly_hours}h a week, plus the Sunday review — ` +
      `more than a full working day spent running the engine. Not an argument for cutting the ` +
      `check-ins; they are what caught the 18-minute timer misread and the sleep chain. ` +
      `It IS an argument for holding each to its stated length.`)));

  /* ---------------------------------------------------------- the rules */

  add(h('h2', {}, 'The hard rules'));
  add(h('div', { class: 'card' }, h('ul', { style: 'margin:0 0 0 18px;color:var(--text-2);font-size:14.5px' },
    ((OS.rules || {}).hard || []).map(t => h('li', { style: 'margin-bottom:6px' }, t)))));

  /* ------------------------------------------------------------ patterns */

  add(h('h2', {}, 'context/patterns.md'));
  add(doc('patterns'));
})();
