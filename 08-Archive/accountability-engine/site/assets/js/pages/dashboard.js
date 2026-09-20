/* Samuelsignals OS — dashboard.
   The one screen that answers "how am I doing across everything". */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, mount, naira, num, pct, hours, time12, dateLabel, dayName,
          daysUntil, daysLabel, verdictPill, stat, statCard, callout, toggle,
          bar, table, scoreClass, chartCard, legend, note } = S;

  S.chrome('index');
  if (!S.guard()) return;

  const M = document.getElementById('main');
  const ledger = OS.ledger;
  const closed = ledger.filter(r => r.score !== null);
  const today = ledger[ledger.length - 1];
  const last = closed[closed.length - 1];
  const sum = OS.summary;

  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  /* ------------------------------------------------- 0. is this record current? */
  /* TWO different problems, deliberately shown differently. Conflating them made
     this banner shout "OUT OF SYNC" about days Samuel simply had not logged yet —
     which is not a site failure, and a banner that cries wolf stops being read.

     WARNINGS = the site does not match context/. A build problem. Fix it in code.
     GAPS     = context/ is behind real life. Closed by logging, not by building. */

  if ((OS.warnings || []).length) {
    add(callout('bad', '\u{26A0}\u{FE0F}',
      '<strong>THIS SITE IS OUT OF SYNC WITH THE RECORD.</strong> The build found ' +
      OS.warnings.length + ' thing' + (OS.warnings.length === 1 ? '' : 's') +
      ' the site is showing wrongly. This is a build problem, not a logging one:',
      ...OS.warnings.map(w => '• ' + w)));
  }

  if ((OS.gaps || []).length) {
    add(callout('warn', '\u{1F4DD}',
      '<strong>THE RECORD HAS ' + OS.gaps.length + ' GAP' +
      (OS.gaps.length === 1 ? '' : 'S') + ', AND THE SITE IS SHOWING THEM HONESTLY.</strong> ' +
      'Everything below matches <code>context/</code> exactly. These are days and ' +
      'numbers not yet written down — they close at the reckoning, not in the code:',
      ...OS.gaps.map(g => '• ' + g)));
  }

  /* ------------------------------------------------------------ 1. today */

  add(h('div', { class: 'page-head' },
    h('div', { class: 'eyebrow' }, `${dayName(today.date)} ${dateLabel(today.date)} · ${OS.profile.location}`),
    h('h1', {}, 'Everything, in one glance.'),
    h('p', { class: 'lede' },
      'The whole record, derived from ', h('code', {}, 'context/'),
      '. Nothing here is typed by hand — if a number is wrong, the file is wrong.')));

  const scoreHost = h('div', { style: 'display:grid;place-items:center' });
  add(h('div', { class: 'grid g-2-1' },
    h('div', { class: 'card' },
      h('div', { class: 'card-h' },
        h('h3', {}, 'Today'),
        verdictPill(today.verdict)),
      h('p', { style: 'color:var(--text-2);font-size:14.5px' }, today.committed || '—'),
      today.shipped
        ? h('p', { style: 'margin-top:10px;font-size:14px' },
            h('span', { class: 'tiny', style: 'display:block;margin-bottom:3px' }, 'SHIPPED'),
            today.shipped)
        : h('p', { class: 'tiny', style: 'margin-top:12px' },
            ((OS.rules || {}).touches || {}).closes_at || ''),
      h('div', { class: 'grid g3 tight', style: 'margin-top:16px' },
        stat('Focus', today.focus_logged != null ? hours(today.focus_logged) : '—',
          today.focus_committed ? `of ${hours(today.focus_committed)}` : 'not logged yet'),
        stat('Habits', today.habits_set ? `${today.habits_hit}/${today.habits_set}` : '—', 'confirmed at reckoning'),
        stat('Bed', time12(today.bed) , today.bed ? '' : (((OS.rules || {}).touches || {}).bed_ask || '')))),
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'Behaviour score'),
        h('span', { class: 'sub' }, dateLabel(last.date))),
      scoreHost,
      h('p', { class: 'chart-note', style: 'text-align:center' },
        `week average ${sum.avg_score} · ${sum.days_closed} days closed`))));

  K.arc(scoreHost, last.score, {
    size: 168, stroke: 13,
    colour: last.score >= 85 ? K.COLOURS.green : last.score >= 60 ? K.COLOURS.amber : K.COLOURS.red,
    centre: String(last.score), sub: 'out of 100', big: 40,
  });

  /* ------------------------------------------------------- 2. the numbers */

  const g1 = OS.goals.find(g => g.id === 'goal1');
  const nextPay = OS.paydays.map(p => ({ ...p, d: daysUntil(p.date) })).filter(p => p.d >= 0)[0];
  const launch = OS.countdowns.find(c => c.date === OS.course.launch);

  add(h('div', { class: 'grid g4 tight', style: 'margin-top:14px' },
    statCard('In the bank', naira(OS.pots.bank), 'everything he can spend today',
      OS.pots.bank < 10000 ? 'red' : ''),
    statCard('₦1M by 31 Dec', pct(g1.current / g1.target * 100),
      `${naira(g1.current, { short: true })} of ₦1M · ${daysLabel(daysUntil(g1.deadline))} left`, 'red'),
    statCard('Next payday', nextPay ? daysLabel(nextPay.d) : '—',
      nextPay ? `${naira(nextPay.amount, { short: true })}${nextPay.confirmed ? '' : ' · UNCONFIRMED'}` : '',
      nextPay && !nextPay.confirmed ? 'amber' : 'green'),
    statCard('Course launch', daysLabel(daysUntil(OS.course.launch)),
      `${OS.course.recorded} of ${OS.course.total_lessons} lessons recorded`, 'violet')));

  /* ------------------------------------------------- 3. the score, in shape */

  add(h('h2', {}, 'The score, and what it is made of'));

  const scoreLine = h('div');
  const scoreStack = h('div');
  add(h('div', { class: 'grid g2' },
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'Behaviour score'),
        h('span', { class: 'sub' }, '0–100')),
      scoreLine,
      notesFor('dashboard', 'n1')),
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'What made up each score'),
        h('span', { class: 'sub' }, 'components')),
      scoreStack,
      legend([[K.COLOURS.blue, 'Verdict'], [K.COLOURS.teal, 'Focus'],
              [K.COLOURS.violet, 'Habits'], [K.COLOURS.green, 'Sleep']]),
      notesFor('dashboard', 'n2'))));

  K.lineChart(scoreLine, closed.map(r => ({ date: r.date, value: r.score })), {
    id: 'score', yMax: 100, colour: K.COLOURS.blue, height: 230,
    dotColour: p => p.value >= 85 ? K.COLOURS.green : p.value >= 60 ? K.COLOURS.amber : K.COLOURS.red,
    thresholds: [{ value: 85, colour: K.COLOURS.green, label: 'a good day' }],
  });

  K.stackedBar(scoreStack, closed.map(r => {
    const c = r.score_components || {};
    const avail = ['verdict', 'focus', 'habits', 'sleep']
      .reduce((a, k) => a + (c[k] ? c[k].of : 0), 0) || 1;
    const scale = 100 / avail;   // rescale to the same 0–100 the score uses
    return {
      date: r.date,
      verdict: (c.verdict?.points || 0) * scale,
      focus:   (c.focus?.points   || 0) * scale,
      habits:  (c.habits?.points  || 0) * scale,
      sleep:   (c.sleep?.points   || 0) * scale,
    };
  }), {
    height: 230, yMax: 100,
    keys: [
      { key: 'verdict', name: 'Verdict', colour: K.COLOURS.blue },
      { key: 'focus',   name: 'Focus',   colour: K.COLOURS.teal },
      { key: 'habits',  name: 'Habits',  colour: K.COLOURS.violet },
      { key: 'sleep',   name: 'Sleep',   colour: K.COLOURS.green },
    ],
  });

  /* ------------------------------------------------------ 4. focus + sleep */

  add(h('h2', {}, 'The two things underneath it'));

  const focusHost = h('div');
  const bedHost = h('div');
  add(h('div', { class: 'grid g2' },
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'Focus logged vs committed'),
        h('span', { class: 'sub' }, 'hours')),
      focusHost,
      legend([[K.COLOURS.teal, 'Logged'], [K.COLOURS.surface3 || '#1e2632', 'Committed'],
              [K.COLOURS.red, '12h — the invoice line']]),
      notesFor('dashboard', 'n3')),
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'What time he actually went to bed'),
        h('span', { class: 'sub' }, `${sum.nights_floor_hit}/${sum.nights_recorded} nights hit the floor`)),
      bedHost,
      notesFor('dashboard', 'n4'))));

  K.barChart(focusHost, ledger.filter(r => r.focus_logged != null), {
    height: 230, yStep: 4,
    series: [
      { key: 'focus_committed', name: 'Committed', colour: '#1e2632' },
      { key: 'focus_logged', name: 'Logged',
        colour: d => d.focus_logged > 12 ? K.COLOURS.red : K.COLOURS.teal },
    ],
    thresholds: [{ value: 12, colour: K.COLOURS.red, label: '12h — an invoice' }],
  });

  K.bedChart(bedHost, ledger, { height: 250 });

  /* ---------------------------------------------------------- 5. habits */

  const hlog = OS.habit_log || {};
  const hdates = Object.keys(hlog).sort();
  const hnames = OS.habits.habits.map(x => x.name)
    .filter(n => hdates.some(d => hlog[d][n] !== undefined));

  if (hdates.length) {
    const heatHost = h('div', { style: 'overflow-x:auto' });
    add(h('h2', {}, 'Habits'),
      h('div', { class: 'card' },
        h('div', { class: 'card-h' },
          h('h3', {}, 'Every habit, every day'),
          h('span', { class: 'sub' }, '7-day block · 25–31 Aug')),
        heatHost,
        legend([[K.COLOURS.green, 'Hit'], [K.COLOURS.red, 'Broken'], ['#1e2632', 'Not tracked']]),
        notesFor('dashboard', 'n5')));
    K.heatmap(heatHost, hnames, hdates, (name, d) => {
      const v = hlog[d]?.[name];
      return v === undefined ? null : v;
    }, { cell: 30, labelW: 150 });
  }

  /* ------------------------------------------------------- 6. the week */

  add(h('h2', {}, 'Day by day'));
  add(h('div', { class: 'card pad-0' },
    table(
      ['Date', 'Verdict', { label: 'Score', num: true }, { label: 'Focus', num: true },
       { label: 'Habits', num: true }, { label: 'Bed', num: true }, 'What shipped'],
      ledger.slice().reverse().map(r => [
        h('span', { class: 'mono tight' }, r.date),
        verdictPill(r.verdict),
        r.score == null ? '—' : h('strong', { class: 'v ' + scoreClass(r.score) }, r.score),
        r.focus_logged == null ? '—' :
          h('span', { title: `${hours(r.focus_logged)} of ${hours(r.focus_committed)}` },
            r.focus_pct != null ? r.focus_pct + '%' : hours(r.focus_logged)),
        r.habits_set ? `${r.habits_hit}/${r.habits_set}` : '—',
        r.bed ? h('span', { class: r.bed < '12:00' ? 'v red' : '' }, time12(r.bed)) : '—',
        h('span', { class: 't-sm' }, r.shipped || h('span', { class: 't-dim' }, 'open')),
      ]))));

  /* --------------------------------------------------------- 7. goals */

  add(h('h2', {}, 'Goals'));
  add(h('div', { class: 'card pad-0' },
    table(
      ['Goal', { label: 'Now', num: true }, { label: 'Target', num: true },
       'Progress', { label: 'Days left', num: true }, 'Status'],
      OS.goals.map(g => {
        const p = g.target ? (g.current / g.target) * 100 : 0;
        const d = daysUntil(g.deadline);
        const money = g.unit === 'naira';
        return [
          h('div', {}, h('div', { class: 't', style: 'font-size:13.5px' }, g.short),
            h('div', { class: 's' }, g.name)),
          money ? naira(g.current, { short: true }) : g.current,
          money ? naira(g.target, { short: true }) : `${g.target} ${g.unit}`,
          h('div', { style: 'min-width:110px' },
            bar(g.current, g.target, g.status === 'behind' ? 'red' : g.status === 'at risk' ? 'amber' : 'blue'),
            h('div', { class: 'tiny', style: 'margin-top:4px' }, pct(p))),
          h('span', { class: d < 60 ? 'v red' : '' }, d),
          h('span', { class: 'pill ' + (g.status === 'on track' ? 'ok' : g.status === 'behind' ? 'bad' : g.status === 'at risk' ? 'warn' : 'neutral') }, g.status),
        ];
      }))));

  add(notesFor('dashboard', 'n6'));

  /* ------------------------------------------------------- 8. patterns */

  add(h('h2', {}, 'Active failure patterns'));
  add(h('div', { class: 'grid g3' },
    OS.patterns.map(p => h('div', { class: 'card' },
      h('div', { class: 'card-h' },
        h('h3', {}, h('span', { class: 'mono', style: 'color:var(--dim);margin-right:7px' }, p.id), p.name),
        h('span', { class: 'pill ' + (p.status === 'active' ? 'bad' : 'warn') }, p.status)),
      h('p', { style: 'color:var(--text-2);font-size:13.5px' }, p.mechanism),
      p.evidence ? h('p', { class: 'tiny', style: 'margin-top:9px' },
        h('strong', {}, 'Evidence: '), p.evidence) : null))));

  /* ------------------------------------------------------ 9. what's coming */

  add(h('h2', {}, 'What is coming'));
  const up = OS.countdowns
    .map(c => ({ ...c, d: daysUntil(c.date) }))
    .filter(c => c.d >= 0 && !/superseded/i.test(c.note || ''))
    .sort((a, b) => a.d - b.d);

  add(h('div', { class: 'card' }, h('div', { class: 'rows' },
    up.map(c => h('div', { class: 'row' },
      h('div', { class: 'r mono', style: `min-width:74px;font-size:20px;font-weight:700;color:${c.d <= 3 ? 'var(--red)' : c.d <= 14 ? 'var(--amber)' : 'var(--text)'}` },
        c.d === 0 ? 'today' : c.d),
      h('div', { class: 'grow' },
        h('div', { class: 't' }, c.label),
        h('div', { class: 's' }, c.note || dateLabel(c.date))),
      h('div', { class: 'r' }, h('span', { class: 'pill neutral' }, c.kind)))))));

  /* ------------------------------------------------------- 10. the detail */

  add(h('h2', {}, 'The detail'));

  add(toggle('How the behaviour score works', 'and why a SHIPPED day can score 70',
    h('p', {}, 'Out of 100. Four components that apply every day, two penalties that only apply on the day the obligation exists.'),
    table(['Component', { label: 'Weight', num: true }, 'Scoring'], [
      ['Verdict', 40, 'SHIPPED 40 · PARTIAL 20 · MISSED 0'],
      ['Focus coverage', 20, h('span', {}, 'min(logged ÷ committed, 1.0) × 20 — ', h('strong', {}, 'capped at 10 if logged > 12h'))],
      ['Habits', 20, 'hit ÷ set × 20'],
      ['Sleep', 20, 'bed ≤10:30pm → 20 · ≤11:30pm → 10 · later → 0'],
      [h('span', { class: 'v red' }, 'Penalty'), -15, 'Video not live by Wednesday 7:00pm'],
      [h('span', { class: 'v red' }, 'Penalty'), -15, 'Planned savings transfer did not move'],
    ]),
    h('p', {}, h('strong', {}, 'Why the focus cap is the important part. '),
      'Uncapped, 25 August scores 180% on focus — the system would hand its highest mark to the 19-hour day. Capping at 1.0 and halving anything over 12h means a march can still ship and still not score well.'),
    h('p', {}, h('strong', {}, 'Missing data rescales. '),
      'No sleep figure recorded → drop the component and rescale the rest to 100. A day nobody asked about is not a day he failed.'),
    h('p', {}, h('strong', {}, 'He has never had a 100. '),
      'That needs shipped, full focus coverage under 12h, all habits, and bed by 10:30.')));

  add(toggle('The hard rules', 'unchanged, and not negotiable',
    h('ul', {},
      ((OS.rules || {}).hard || []).map(t => h('li', {}, t)))));

  add(toggle('Where this data comes from', `${sum.days_recorded} days · generated`,
    h('p', {}, 'Everything on this site is derived from the markdown record in ',
      h('code', {}, 'context/'), ' by ', h('code', {}, 'tools/site/build.py'), '.'),
    h('ul', {},
      [['ledger.md', 'the daily rows, focus, habits counts, bed times, verdicts'],
       ['ledger-notes/', 'the narrative behind each day'],
       ['money-ledger.md', 'every naira in and out'],
       ['habits.md', 'the habit names and cadences'],
       ['patterns.md', 'the documented failure modes'],
       ['tools/sheets/plan.json', 'every budget line item'],
       ['site.json', 'the goals, pots and targets that live in prose'],
      ].map(([f, w]) => h('li', {}, h('code', {}, f), ' — ', w))),
    h('p', {}, h('strong', {}, 'The site is a view, never the record. '),
      'That is deliberate: it means the record keeps git\'s append-only guarantee, ' +
      'and a 40% day cannot be softened by editing a dashboard.')));
})();
