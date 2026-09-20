/* Samuelsignals OS — Money. */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, naira, num, pct, dateLabel, daysUntil, daysLabel, stat, statCard,
          callout, toggle, bar, table, pageHead, note, legend } = S;

  S.chrome('money');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const P = OS.pots, I = OS.income;
  const g1 = OS.goals.find(g => g.id === 'goal1');
  const g2 = OS.goals.find(g => g.id === 'goal2');
  const nextPay = OS.paydays.map(p => ({ ...p, d: daysUntil(p.date) })).filter(p => p.d >= 0)[0];

  add(pageHead('Money', 'The one lever is surplus, not income.',
    'Income doubled and halved across three months and the savings balance did not move. ' +
    '<strong>That proves income was never the lever.</strong> What matters is the surplus that ' +
    'is still there on the 30th.'));

  /* ------------------------------------------------------------ the numbers */

  add(h('div', { class: 'grid g4 tight' },
    statCard('In the bank', naira(P.bank), P.bank_sub || 'everything he can spend today',
      P.bank_free != null && P.bank_free < 50000 ? 'red' : ''),
    statCard('₦1M by 31 Dec', naira(g1.current, { short: true }),
      `${pct(g1.current / g1.target * 100)} · ${daysLabel(daysUntil(g1.deadline))} left`, 'red'),
    statCard('Next payday', nextPay ? daysLabel(nextPay.d) : '—',
      nextPay ? `${naira(nextPay.amount, { short: true })}${nextPay.confirmed ? '' : ' · UNCONFIRMED'}` : '',
      nextPay && !nextPay.confirmed ? 'amber' : 'green'),
    statCard('Ring-fenced', naira(P.cowrywise, { short: true }),
      'Cowrywise · locked to Jan 2027', 'violet')));

  add(h('div', { style: 'margin-top:14px' },
    notesFor('money', 'n1')));

  /* ---------------------------------------------------------------- the pots */

  add(h('h2', {}, 'Where the money actually is'));

  const potRows = [
    ['Bank (liquid)', P.bank, 'Everything he can spend today', 'red'],
    ['Goal 1 — house', P.goal1_house, 'Does not exist yet. Target ₦1,000,000 by 31 Dec.', ''],
    ['Emergency fund', P.emergency, 'Starts January 2027, after Goal 1 closes.', ''],
    ['Cowrywise investment', P.cowrywise, 'RING-FENCED. Locked to Jan 2027. Never counts toward the goals.', 'violet'],
    ['Buffer', P.buffer, 'New rule. ₦50,000/month to ₦200,000. Where urgencies come from — not savings.', ''],
  ];
  add(h('div', { class: 'card pad-0' },
    table(['Pot', { label: 'Amount', num: true }, 'What it is'],
      potRows.map(([n, v, note2, cls]) => [
        h('strong', {}, n),
        h('span', { class: 'v ' + cls, style: 'font-size:15px' }, naira(v)),
        h('span', { class: 't-sm t-dim' }, note2),
      ]))));

  /* ------------------------------------------------------------- the runway */

  add(h('h2', {}, 'Does the ₦1M close?'));

  const runwayHost = h('div');
  const cashHost = h('div');
  add(h('div', { class: 'grid g2' },
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'Runway to 31 December'),
        h('span', { class: 'sub' }, 'projected, August mix')),
      runwayHost,
      notesFor('money', 'n2')),
    h('div', { class: 'card' },
      h('div', { class: 'card-h' }, h('h3', {}, 'Cash actually landing'),
        h('span', { class: 'sub' }, 'per calendar month')),
      cashHost,
      notesFor('money', 'n3'))));

  // cumulative: opening balance + monthly surplus − ₦50,000/month to the buffer
  let acc = P.bank;
  const runway = I.projection.map(m => {
    acc += m.surplus - 50000;
    return { date: m.month + '-28', value: Math.round(acc), label: `${m.month} — ${naira(acc, { short: true })}` };
  });
  K.lineChart(runwayHost, [{ date: '2026-08-28', value: P.bank, label: `now — ${naira(P.bank)}` }, ...runway], {
    id: 'runway', colour: K.COLOURS.green, height: 235, yMax: 1200000,
    yFmt: v => '₦' + (v / 1000000).toFixed(1) + 'M',
    thresholds: [{ value: 1000000, colour: K.COLOURS.red, label: '₦1M target' }],
  });

  K.barChart(cashHost, [
    ...I.cash_landed.map(m => ({ label: m.month.slice(5) + '/' + m.month.slice(2, 4), value: m.amount, real: m.real || m.amount })),
    ...I.projection.map(m => ({ label: m.month.slice(5) + '/' + m.month.slice(2, 4), projected: m.surplus + I.obligations_floor })),
  ], {
    height: 235, yStep: 250000,
    yFmt: v => '₦' + (v / 1000000).toFixed(1) + 'M',
    series: [
      { key: 'value', name: 'Landed', colour: K.COLOURS.blue },
      { key: 'real', name: 'Real (ex-savings)', colour: K.COLOURS.teal },
      { key: 'projected', name: 'Projected', colour: '#2f3a4a' },
    ],
    thresholds: [{ value: I.committed_outflow, colour: K.COLOURS.amber, label: 'committed outflow' }],
  });

  /* ------------------------------------------------------------- scenarios */

  const scenHost = h('div');
  add(h('div', { class: 'card', style: 'margin-top:14px' },
    h('div', { class: 'card-h' }, h('h3', {}, 'Monthly surplus, by video mix'),
      h('span', { class: 'sub' }, 'after ' + naira(I.obligations_floor) +
        ' obligations + ' + naira(I.committed_outflow - I.obligations_floor) + ' Cowrywise')),
    scenHost,
    notesFor('money', 'n4')));

  K.hBars(scenHost, I.scenarios.map(s => ({
    label: s.name, value: s.surplus,
    valueColour: s.underwater ? K.COLOURS.red : K.COLOURS.green,
  })), {
    rowH: 38, max: 800000, fmt: v => naira(v),
    colour: d => d.value < 0 ? K.COLOURS.red : d.value > 500000 ? K.COLOURS.green : K.COLOURS.amber,
  });

  /* ------------------------------------------------------------ goal 2 */

  add(h('h2', {}, 'Goal 2 — and this is the real problem'));
  add(notesFor('money', 'n5'));

  /* ------------------------------------------------------------ the ledger */

  add(h('h2', {}, 'Every naira, as it was logged'));
  add(h('div', { class: 'card pad-0' },
    table(['Date', { label: 'Balance', num: true }, 'What went out', { label: 'To savings', num: true }, 'Note'],
      OS.money_ledger.slice().reverse().map(r => [
        h('span', { class: 'mono tight' }, r.label),
        h('strong', { class: 'v ' + (r.balance < 10000 ? 'red' : '') }, naira(r.balance)),
        h('span', { class: 't-sm' }, r.out_text || '—'),
        naira(r.savings_moved),
        h('span', { class: 't-sm t-dim' }, (r.note || '').slice(0, 220) + ((r.note || '').length > 220 ? '…' : '')),
      ]))));

  /* ------------------------------------------------------------- paydays */

  add(h('h2', {}, 'The payday calendar'));
  add(h('div', { class: 'card' }, h('div', { class: 'rows' },
    OS.paydays.map(p => {
      const d = daysUntil(p.date);
      return h('div', { class: 'row', style: d < 0 ? 'opacity:.42' : '' },
        h('div', { class: 'r mono', style: `min-width:66px;font-size:17px;font-weight:700;color:${d < 0 ? 'var(--dim)' : d <= 7 ? 'var(--amber)' : 'var(--text)'}` },
          d < 0 ? '—' : d),
        h('div', { class: 'grow' },
          h('div', { class: 't' }, p.label,
            p.slips ? h('span', { class: 'pill warn', style: 'margin-left:8px' }, 'slips') : null,
            !p.confirmed ? h('span', { class: 'pill bad', style: 'margin-left:8px' }, 'unconfirmed') : null),
          h('div', { class: 's' }, p.note || dateLabel(p.date))),
        h('div', { class: 'r mono', style: 'font-size:14px' }, naira(p.amount, { short: true })));
    }))));

  /* ---------------------------------------------------------------- rules */

  add(h('h2', {}, 'The rules'));
  const RULES = [
    ['1', 'Savings are untouchable.', 'Only three permitted withdrawals: medical emergency, building-project shortfall that would stop work, family emergency. A girlfriend\'s visit is not an emergency.'],
    ['2', 'Every withdrawal is logged the same day', 'with the reason in his own words. No silent withdrawals.'],
    ['3', 'Savings move ON A PAYDAY,', 'the day the money lands — never at month end. Money saved at the end of the month is money that was never saved. Cowrywise on Payday A; Goal 1 and the Buffer on Payday B. Any Payday A surplus over ₦50,000 moves the same day.'],
    ['4', 'Building project paid in full (₦500,000)', 'before any discretionary line. August was ₦200,000 — a ₦300,000 shortfall, on the record.'],
    ['5', 'No new work below $333/video', 'without logging the reason. The August batch lost ~₦432,000 to the $175 rate.'],
    ['6', 'A budget line that says money was saved when no money moved is a lie in a spreadsheet.', 'The ledger is the truth; the budget is a plan.'],
    ['7', 'The investment is ring-fenced.', '₦100,000/month to Cowrywise until year end. Never touched for the ₦1M, the ₦3M, the building, or anything else. It never pauses.'],
    ['8', 'THE BUFFER is where urgencies come from — not savings.', '₦50,000/month to ₦200,000. Lean-month cut order, decided in advance: personal/misc → creator visits → household to ₦20,000 → the buffer → and only then a conversation. If the buffer is empty, an urgency gets negotiated, not funded.'],
  ];
  add(h('div', { class: 'card' }, h('div', { class: 'rows' },
    RULES.map(([n, bold, rest]) => h('div', { class: 'row' },
      h('div', { class: 'r mono', style: 'min-width:26px;font-size:17px;font-weight:700;color:var(--red)' }, n),
      h('div', { class: 'grow' },
        h('div', { class: 't' }, bold),
        h('div', { class: 's' }, rest)))))));

  /* --------------------------------------------------------------- detail */

  add(h('h2', {}, 'The detail'));

  add(toggle('Income mechanics — one payer, two paydays', 'Route Rise Media LTD',
    h('p', {}, h('strong', {}, 'Route Rise Media LTD is an AGENCY, and it is his only payer. '),
      'It works with two end clients; he edits for both and sends one invoice covering both. ' +
      'There is no second client and there never was.'),
    h('p', {}, h('strong', { class: 'v red' }, '100% of income arrives through one invoice to one company. '),
      'If Route Rise goes, all of it goes — including the "$175 client", which is not a separate ' +
      'relationship he could keep.'),
    h('p', {}, 'Paid in USD, converted on Cleva at ≈ ₦', I.usd_ngn, '/$. ', I.split),
    table(['Batch', { label: 'Videos', num: true }, 'Note'],
      I.batches.map(b => [b.month, b.videos, b.note || ''])),
    h('p', {}, h('strong', {}, 'They do not pay at weekends. '),
      'A payday on a Saturday lands the following Monday night. Two slips are already on the ' +
      'calendar: Oct 70% Sat 31 Oct → Mon 2 Nov (the tightest point of the year — November\'s ' +
      'front half is funded on the 2nd, and Google bills on the 2nd, CapCut the 4th), and ' +
      'Nov 30% Sat 14 Nov → Mon 16 Nov.')));

  add(toggle('The concentration risk', 'one payer, one invoice',
    h('p', {}, h('strong', {}, '"Hit 4 videos a month" is not a SMART goal '),
      '— the A fails. Achievement is another company\'s decision, not his.'),
    h('p', {}, 'He has ruled out taking more clients. That is his call. But it means ',
      h('strong', {}, 'the course is the only income line whose existence he controls. '),
      'Every time course work is dropped for client work, that is diversification being traded ' +
      'away for concentration. The weekly review says so, out loud, every week.')));

  add(toggle('Said once about Rule 7, and not re-argued', 'the ring-fence trade',
    h('p', {}, 'He is putting ₦100,000/month into a locked pot he refuses to count toward his goals, ' +
      'while holding ₦2,503 liquid and a ₦1M target with ₦7,667 of margin.'),
    h('p', {}, h('strong', {}, 'That is a deliberate trade — long-term wealth bought with short-term ' +
      'fragility. It is his call.'), ' It is written down so that if December comes up short, the ' +
      'reason is on the record and not a mystery.')));
})();
