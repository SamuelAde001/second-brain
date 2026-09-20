/* Samuelsignals OS — Work & Clients. */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, naira, hours, dateLabel, daysUntil, daysLabel, statCard, callout,
          toggle, table, pageHead, note, legend, verdictPill } = S;

  S.chrome('work');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const I = OS.income;
  const led = OS.ledger;
  const W = OS.work || {};
  const JOB = W.current_job || null;

  add(pageHead('Work & Clients', 'Five days from start. Route Rise sets it, not him.',
    'The one lever he owns, in his words: <em>"I just want to meet all my deadlines."</em>'));

  add(h('div', { class: 'grid g4 tight' },
    statCard(JOB ? JOB.name + ' due' : 'No job open',
      JOB ? daysLabel(daysUntil(JOB.due)) : '—',
      JOB ? 'send ' + JOB.send_target : 'nothing in flight', 'red'),
    statCard('The cap', (W.cap_days || 5) + ' days', 'from start — their term, not his', 'amber'),
    statCard('Payers', '1', '100% of income, one invoice', 'red'),
    statCard('Focus this week', hours(OS.summary.total_focus), OS.summary.days_closed + ' days closed')));

  add(h('div', { style: 'margin-top:14px' }, callout('bad', '\u{26A0}',
    '<strong>ONE PAYER. Not one client — one payer.</strong> Route Rise Media LTD is an agency. ' +
    'It works with two end clients; he edits for both and sends one invoice covering both. ' +
    'Both rates are Route Rise’s. The volume is Route Rise’s decision.',
    '<strong>And the deadline is theirs too.</strong> ' + (W.cap_note || ''),
    '<strong>"Hit 4 videos a month" is not a SMART goal</strong> — the A fails. Achievement is ' +
    'another company’s decision, not his. Which leaves exactly one lever he owns: the course.')));

  /* ------------------------------------------------- the job in flight */

  if (JOB) {
    add(h('h2', {}, JOB.name + ' — ' + JOB.scope));
    add(h('div', { class: 'card' }, h('div', { class: 'rows' },
      JOB.days.map(d => {
        const past = daysUntil(d.date) < 0;
        const state = d.state === 'done' ? 'done' : (past ? 'missed' : 'open');
        return h('div', { class: 'row' },
          h('div', { class: 'r mono', style: 'min-width:74px;font-weight:700' }, dateLabel(d.date)),
          h('div', { class: 'grow' },
            h('div', { class: 't' }, d.label),
            h('div', { class: 'sub' }, 'must close: ' + d.must)),
          h('div', { class: 'r' }, h('span', {
            class: 'pill ' + (state === 'done' ? 'ok' : state === 'missed' ? 'bad' : 'neutral'),
          }, state === 'done' ? 'done' : state === 'missed' ? 'not closed' : 'open')));
      }))));
  }

  /* --------------------------------------------- what the cap has cost */

  if ((W.history || []).length) {
    add(h('h2', {}, 'Every delivery so far'));
    add(h('div', { class: 'card pad-0' },
      table(['Job', 'Due', 'Delivered', 'Verdict', 'What happened'],
        W.history.map(j => [
          h('strong', {}, j.name),
          j.due ? dateLabel(j.due) : '—',
          j.delivered ? dateLabel(j.delivered) : '—',
          h('span', { class: 'pill bad' }, j.verdict),
          j.note,
        ]))));
    add(h('div', { style: 'margin-top:12px' }, notesFor('work', 'n1')));
  }

  /* --------------------------------------------------------- the record */

  add(h('h2', {}, 'The delivery record'));
  add(h('div', { class: 'card pad-0' },
    table(['Date', 'Committed', 'Verdict', { label: 'Focus', num: true }, 'What happened'],
      led.slice().reverse().map(r => [
        h('span', { class: 'mono tight' }, r.date),
        h('span', { class: 't-sm' }, (r.committed || '').slice(0, 90) + ((r.committed || '').length > 90 ? '…' : '')),
        verdictPill(r.verdict),
        r.focus_pct != null ? r.focus_pct + '%' : '—',
        h('span', { class: 't-sm t-dim' }, r.shipped || 'open'),
      ]))));

  /* ------------------------------------------------------ income shape */

  add(h('h2', {}, 'Where the money comes from'));
  const batchHost = h('div');
  add(h('div', { class: 'card' },
    h('div', { class: 'card-h' }, h('h3', {}, 'Videos invoiced per batch'),
      h('span', { class: 'sub' }, 'volume is not his decision')),
    batchHost,
    notesFor('work', 'n2')));

  K.barChart(batchHost, I.batches.map(b => ({ label: b.month.slice(5) + '/' + b.month.slice(2, 4), videos: b.videos })), {
    height: 210, yStep: 1, yMax: 6,
    series: [{ key: 'videos', name: 'Videos', colour: d => d.videos <= 2 ? K.COLOURS.red : K.COLOURS.blue }],
    thresholds: [{ value: 4, colour: K.COLOURS.green, label: '4 — the mix that closes December' }],
  });

  /* ---------------------------------------------------------- the rules */

  add(h('h2', {}, 'The rules that came out of the misses'));
  const RULES = (OS.rules || {}).work || [];
  add(h('div', { class: 'card' }, h('div', { class: 'rows' },
    RULES.map(([t, s]) => h('div', { class: 'row' },
      h('div', { class: 'grow' }, h('div', { class: 't' }, t), h('div', { class: 's' }, s)))))));

  /* --------------------------------------------------------- the detail */

  add(h('h2', {}, 'The detail'));
  add(toggle('The concentration risk, in full', 'one payer, one invoice',
    h('p', {}, h('strong', { class: 'v red' }, '100% of income arrives through one invoice to one company. '),
      'If Route Rise goes, all of it goes — including the "$175 client", which is not a separate ' +
      'relationship he could keep.'),
    h('p', {}, 'Rates: $333.33/video on the original end client — he has tried to raise it, they ' +
      'will not move, and he is content with it. $175/video on the second end client, new August ' +
      '2026, two videos agreed, may or may not recur. ',
      h('strong', {}, 'The rate mix cost ~₦432,000 on the August batch alone.')),
    h('p', {}, h('strong', {}, 'He does not want more clients. '), 'His reason: one client’s ' +
      'workload is already high. His call, and not to be re-litigated at every check-in — but it ' +
      'means the course is the only income line whose existence he controls.'),
    h('p', {}, h('strong', {}, 'They do not pay at weekends. '), 'Oct 70% slips Sat 31 Oct → Mon 2 Nov ' +
      '(the tightest point of the year), and Nov 30% slips Sat 14 Nov → Mon 16 Nov.')));
})();
