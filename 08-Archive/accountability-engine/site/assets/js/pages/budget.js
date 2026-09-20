/* Samuelsignals OS — Budget. The spreadsheet, mirrored. */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, naira, pct, stat, statCard, callout, toggle, table, pageHead, note, legend } = S;

  S.chrome('budget');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const B = OS.budget;
  // Which month this page is showing. Defaults to the month we are actually
  // IN, not to plan_start — a dashboard pinned to September is a dashboard
  // that starts lying on 1 October. ?m=YYYY-MM overrides it, and every figure
  // on the page follows, so the whole thing is one month's view of the record.
  const MONTHS_AVAIL = Object.keys(B.months || {}).sort();
  const qsMonth = new URLSearchParams(location.search).get('m');
  const nowMonth = (B.today || '').slice(0, 7);
  const MONTH = (MONTHS_AVAIL.indexOf(qsMonth) >= 0 && qsMonth)
    || (MONTHS_AVAIL.indexOf(nowMonth) >= 0 ? nowMonth : B.plan_start);
  const monthLabel = (m) => new Date(m + '-02')
    .toLocaleString('en-GB', { month: 'short', year: '2-digit' });
  const items = B.items.filter(i => i.active);
  const forMonth = items.filter(i => !i.month || i.month === MONTH);

  /* The month, entirely derived in build.py from plan.json + spend.jsonl +
     OS.paydays. Nothing on this page is typed: log a spend row, change a plan
     line or correct a payday amount and every number below moves with it. */
  const MO = (B.months || {})[MONTH] || {};
  const CATS = MO.categories || [];
  const actualByCat = {};
  CATS.forEach(c => { actualByCat[c.category] = c.paid; });

  const TODAY = B.today || '';
  const dayOfMonth = TODAY.startsWith(MONTH) ? parseInt(TODAY.slice(8), 10) : 0;
  const inFirstHalf = dayOfMonth > 0 && dayOfMonth < 15;
  const monthStarted = TODAY >= MONTH + '-01';

  // Free right now = what is in the bank, less what the CURRENT payday period
  // still has to pay. Payday B's bills are not yet funded, so counting them
  // here would show a man with money in the bank as broke.
  const stillThisHalf = monthStarted
    ? (inFirstHalf ? (MO.left_a || 0) : (MO.left_b || 0))
    : (MO.left_a || 0);
  const bank = (OS.pots || {}).bank || 0;
  const freeNow = bank - stillThisHalf;

  const cats = [...new Set(forMonth.map(i => i.category))];
  const planByCat = {};
  cats.forEach(c => {
    planByCat[c] = forMonth.filter(i => i.category === c).reduce((a, i) => a + (i.amount || 0), 0);
  });
  const totalPlan = Object.values(planByCat).reduce((a, b) => a + b, 0);
  const paydayA = forMonth.filter(i => i.payday === 'A').reduce((a, i) => a + i.amount, 0);
  const paydayB = forMonth.filter(i => i.payday === 'B').reduce((a, i) => a + i.amount, 0);

  // What the two paydays actually bring in. Read from OS.paydays, never typed:
  // the amounts are NET of the flat per-payment charge and use the measured rate,
  // so they move whenever the record does. Prefer this month's; fall back to the
  // next one on the calendar so the table is never blank.
  const payIn = (letter) => {
    const of = OS.paydays.filter(x => (x.label || '').startsWith('Payday ' + letter));
    const here = of.filter(x => (x.date || '').startsWith(MONTH));
    return (here[0] || of.find(x => x.date >= MONTH) || of[of.length - 1] || {}).amount || 0;
  };
  const inA = payIn('A'), inB = payIn('B');

  // Pots are committed money. Cowrywise moves on A; Goal 1 and the Buffer on B.
  // A "free" figure that ignores them is the kind of number that gets spent.
  const potsOn = (letter) => B.savings
    .filter(v => v.payday === letter)
    .reduce((a, v) => a + (v.schedule[MONTH] || 0), 0);
  const potsA = potsOn('A'), potsB = potsOn('B');

  add(pageHead('Budget', `The plan for ${monthLabel(MONTH)}`,
    'Every line item, what it is made of, and which payday funds it. ' +
    '<strong>Nothing here is a mystery number</strong> — a category total is always the sum of ' +
    'named items underneath it.'));

  if (MONTHS_AVAIL.length > 1) {
    add(h('div', { class: 'monthpick' },
      h('span', { class: 't-sm t-dim' }, 'Month:'),
      MONTHS_AVAIL.map(m => h('a', {
        class: 'mp' + (m === MONTH ? ' on' : '') + (m === nowMonth ? ' now' : ''),
        href: '?m=' + m,
        title: m === nowMonth ? 'the month you are in' : m,
      }, monthLabel(m)))));
  }

  add(callout('info', 'ℹ',
    `<strong>August was never planned, deliberately.</strong> The baseline was set on 26 August ` +
    `<em>for</em> September, so <code>plan_start</code> is <strong>${B.plan_start}</strong> and ` +
    `nothing before it is judged against a plan. Comparing August to a plan it never had would ` +
    `invent an overspend that never happened.`,
    `<code>tracking_start</code> is <strong>${B.tracking_start}</strong> — the date the opening ` +
    `bank balance was taken. Everything earned or spent before it is already inside that balance, ` +
    `so it must never also appear as a row. That would double-count and break the bank figure.`));

  /* ------------------------------------------------------------- headline */

  const monthName = new Date(MONTH + '-02').toLocaleString('en-GB', { month: 'long' });

  add(h('h2', {}, monthName + ' at a glance'),
    h('p', { class: 'lede', style: 'margin-bottom:12px' },
      monthStarted
        ? h('span', {}, 'As at ', h('strong', {}, TODAY), ' — day ', h('strong', {}, String(dayOfMonth)),
            ', in the ', h('strong', {}, inFirstHalf ? 'FIRST half (Payday A funds it)'
                                                     : 'SECOND half (Payday B funds it)'), '.')
        : h('span', {}, monthName + ' has not started yet. Everything below is the plan.')));

  add(h('div', { class: 'grid g4 tight' },
    statCard('Expected in this month', naira(MO.income_expected || 0, { short: true }),
      naira(MO.income_received || 0, { short: true }) + ' received · ' +
      naira(MO.income_to_come || 0, { short: true }) + ' still to come', 'green'),
    statCard('Budgeted out', naira(MO.budget_total || 0, { short: true }),
      CATS.length + ' categories, bills and pots together', 'amber'),
    statCard('Paid so far', naira(MO.paid_total || 0, { short: true }),
      MO.paid_total ? 'logged rows only — nothing is assumed paid' : 'nothing logged yet'),
    statCard('Left to pay', naira(MO.left_total || 0, { short: true }),
      naira(MO.left_a || 0, { short: true }) + ' on A · ' +
      naira(MO.left_b || 0, { short: true }) + ' on B', 'blue')));

  const isThisMonth = MONTH === nowMonth;

  add(h('div', { class: 'grid g4 tight', style: 'margin-top:10px' },
    isThisMonth
      ? statCard('In the bank', naira(bank, { short: true }),
          'as at ' + ((OS.pots || {}).as_of || '—'))
      : statCard('In the bank', h('span', { class: 't-dim' }, '—'),
          'a fact about today, not about ' + monthLabel(MONTH)),
    isThisMonth
      ? statCard('Free right now', naira(freeNow, { short: true }),
          'after the ' + (inFirstHalf ? 'Payday A' : 'Payday B') + ' money still to go out',
          freeNow < 0 ? 'red' : freeNow < 50000 ? 'amber' : 'green')
      : statCard('Cushion if it goes to plan', naira((MO.income_expected || 0) - (MO.budget_total || 0), { short: true }),
          'everything in, everything out',
          (MO.income_expected || 0) - (MO.budget_total || 0) < 0 ? 'red' : 'green'),
    statCard('Payday A', naira(inA, { short: true }),
      naira(MO.budget_a || 0, { short: true }) + ' budgeted · ' +
      naira(MO.paid_a || 0, { short: true }) + ' paid', 'green'),
    statCard('Payday B', naira(inB, { short: true }),
      naira(MO.budget_b || 0, { short: true }) + ' budgeted · ' +
      naira(MO.paid_b || 0, { short: true }) + ' paid', 'blue')));

  /* ------------------------------------------------ the two paydays, in full */

  const cushA = (MO.cushion_a == null ? inA - (MO.budget_a || 0) : MO.cushion_a);
  const cushB = (MO.cushion_b == null ? inB - (MO.budget_b || 0) : MO.cushion_b);
  const vcol = (n) => h('strong', { class: 'v ' + (n < 0 ? 'red' : 'green') }, naira(n));

  add(h('div', { class: 'card pad-0', style: 'margin-top:14px' },
    table(['', { label: 'Payday A · 1st–14th', num: true },
               { label: 'Payday B · 15th–end', num: true },
               { label: 'The month', num: true }], [
      ['Money in', naira(inA), naira(inB), h('strong', {}, naira(inA + inB))],
      ['Budgeted out', naira(MO.budget_a || 0), naira(MO.budget_b || 0),
        h('strong', {}, naira(MO.budget_total || 0))],
      ['Paid so far', naira(MO.paid_a || 0), naira(MO.paid_b || 0),
        h('strong', {}, naira(MO.paid_total || 0))],
      ['Still to pay', naira(MO.left_a || 0), naira(MO.left_b || 0),
        h('strong', {}, naira(MO.left_total || 0))],
      [h('strong', {}, 'Cushion'), vcol(cushA), vcol(cushB), vcol(cushA + cushB)],
    ])));

  const shortHalf = cushA < 0 || cushB < 0;
  const monthShort = (cushA + cushB) < 0;
  if (shortHalf || monthShort) {
    const paras = [];
    if (shortHalf) {
      const bad = cushA < 0 ? 'A' : 'B', good = cushA < 0 ? 'B' : 'A';
      const gap = -(cushA < 0 ? cushA : cushB), spare = Math.max(cushA, cushB);
      paras.push(
        '<strong>Payday ' + bad + ' cannot fund itself \u2014 short ' + naira(gap) + '.</strong> ' +
        (spare > 0
          ? 'Payday ' + good + ' has ' + naira(spare) + ' spare, so ' +
            (spare >= gap
              ? 'this is a TIMING problem, not a money one. Rule 3 already covers it: any Payday A ' +
                'excess over \u20a650,000 moves the same day it lands.'
              : 'moving that across still leaves ' + naira(gap - spare) + ' to find.')
          : 'and the other half has nothing spare to move.'));
    }
    if (monthShort) {
      paras.push('<strong>And the month itself is short ' + naira(-(cushA + cushB)) + '.</strong> ' +
        'That is real money missing, not a scheduling problem, and no amount of moving cash between ' +
        'paydays closes it. It comes out of the Buffer or it comes out of a plan line.');
    } else if (shortHalf) {
      paras.push('The month as a whole still balances, with ' + naira(cushA + cushB) + ' over.');
    }
    add(callout('warn', '⚠', ...paras));
  }

  /* --------------------------------------------------- plan vs actual chart */

  add(h('h2', {}, `Plan vs actual — ${MONTH}`));

  // Every row carries its own numbers. A bar with no figure beside it says
  // "something is happening here" and nothing more, which is how a page ends
  // up being looked at rather than read.
  const rowsByPlan = CATS.slice().sort((a, b) => b.planned - a.planned);
  const maxPlan = Math.max(1, ...rowsByPlan.map(c => Math.max(c.planned, c.paid)));

  add(h('div', { class: 'card pad-0' },
    table([
      'Category',
      { label: 'Planned', num: true },
      { label: 'Paid', num: true },
      { label: 'Left', num: true },
      { label: 'Payday A', num: true },
      { label: 'Payday B', num: true },
      'Progress',
    ], rowsByPlan.map(c => {
      const donePct = c.planned ? Math.min(100, Math.round(c.paid / c.planned * 100)) : (c.paid ? 100 : 0);
      const w = (n) => Math.max(n > 0 ? 1 : 0, Math.round(n / maxPlan * 100));
      return [
        h('span', {}, c.is_pot ? h('span', { class: 'pill ok', style: 'margin-right:6px' }, 'pot') : null,
          c.category.replace(/^Savings — /, '')),
        naira(c.planned),
        c.paid ? h('span', { class: 'v ' + (c.paid > c.planned ? 'red' : 'teal') }, naira(c.paid))
               : h('span', { class: 't-dim' }, '—'),
        h('span', { class: 'v ' + (c.left < 0 ? 'red' : '') }, naira(c.left)),
        c.planned_a ? naira(c.planned_a) : h('span', { class: 't-dim' }, '—'),
        c.planned_b ? naira(c.planned_b) : h('span', { class: 't-dim' }, '—'),
        h('div', { class: 'minibar', title: donePct + '% paid' },
          h('div', { class: 'minibar-plan', style: 'width:' + w(c.planned) + '%' },
            h('div', { class: 'minibar-paid', style: 'width:' + donePct + '%' }))),
      ];
    }))));

  add(h('p', { class: 't-sm t-dim', style: 'margin-top:8px' },
    'Grey is the plan, teal is what has actually been paid. ',
    h('strong', {}, 'Paid comes only from logged spend rows'),
    ' — a category cannot claim money moved when no row exists. ',
    MO.unplanned
      ? h('strong', { class: 'v red' }, naira(MO.unplanned) + ' was spent outside any plan line.')
      : 'Nothing has been spent outside a plan line this month.'));

  add(notesFor('budget', 'n1'));

  /* -------------------------------------------------- the details, by cat */

  add(h('h2', {}, 'What each category is actually made of'));
  add(h('p', { class: 'lede', style: 'margin-bottom:14px' },
    'This is the Details tab. It is the only place a plan number is typed, and it is why ',
    h('strong', {}, '₦66,700 of subscriptions is not a budget line — it is Claude + Google + ' +
      'CapCut + YouTube + Spotify, each with its own amount and renewal date.')));

  cats.sort((a, b) => planByCat[b] - planByCat[a]).forEach(c => {
    const rows = forMonth.filter(i => i.category === c)
      .sort((a, b) => b.amount - a.amount);
    add(h('details', { class: 'tg', open: rows.length <= 2 ? '' : null },
      h('summary', {},
        c,
        h('span', { class: 'sub' },
          `${naira(planByCat[c])} · ${rows.length} item${rows.length > 1 ? 's' : ''}`)),
      h('div', { class: 'tg-body' },
        table(['Item', { label: 'Amount', num: true }, 'Tier', 'Payday', 'Due', 'Note'],
          rows.map(i => [
            h('strong', {}, i.item),
            naira(i.amount),
            h('span', { class: 'pill ' + (i.tier === 'Fixed' ? 'bad' : i.tier === 'Committed' ? 'warn' : 'neutral') }, i.tier),
            h('span', { class: 'pill ' + (i.payday === 'A' ? 'ok' : 'info') }, i.payday || '—'),
            i.due || (i.month ? h('span', { class: 'pill neutral' }, 'one-off') : '—'),
            h('span', { class: 't-sm t-dim' }, i.note || ''),
          ])))));
  });

  /* ----------------------------------------------------------- cancelled */

  const dead = B.items.filter(i => !i.active);
  if (dead.length) {
    add(h('h2', {}, 'Cancelled — kept, never deleted'));
    add(notesFor('budget', 'n2'));
    add(h('div', { class: 'card pad-0', style: 'margin-top:10px' },
      table(['Item', 'Category', { label: 'Was', num: true }, 'Note'],
        dead.map(i => [
          h('span', { class: 'strike' }, i.item), i.category, naira(i.amount),
          h('span', { class: 't-sm t-dim' }, i.note || ''),
        ]))));
  }

  /* --------------------------------------------- the month must balance */

  const BAL = B.balance || [];
  const y26 = BAL.filter(r => r.month < '2027-01');
  const y27 = BAL.filter(r => r.month >= '2027-01');
  const mLabel = m => new Date(m + '-01T00:00:00')
    .toLocaleString('en', { month: 'short', year: '2-digit' });

  add(h('h2', {}, 'The month must balance'));
  add(notesFor('budget', 'n3'));

  const balRow = (label, pick, opts = {}) => [
    opts.strong ? h('strong', {}, label) : label,
    ...y26.map(r => {
      const v = pick(r);
      const txt = (opts.neg ? '\u2212 ' : '') + naira(Math.abs(v));
      if (opts.total) {
        return h('strong', { class: 'v ' + (v === 0 ? 'green' : 'red') },
          v === 0 ? naira(0) : naira(v));
      }
      return v === 0 && opts.neg ? h('span', { class: 't-dim' }, '\u2014') : txt;
    }),
  ];

  add(h('div', { class: 'card pad-0', style: 'margin-top:10px' },
    table(['', ...y26.map(r => ({ label: mLabel(r.month), num: true }))], [
      balRow('Expected income', r => r.income, { strong: true }),
      balRow('Bills', r => r.bills, { neg: true }),
      balRow('One-offs', r => r.one_offs, { neg: true }),
      balRow('Into the pots', r => r.pots, { neg: true }),
      balRow('LEFT OVER', r => r.left, { strong: true, total: true }),
    ])));
  add(notesFor('budget', 'n4'));

  if (y27.length) {
    const short = y27.filter(r => r.left < 0);
    add(callout('bad', '!',
      '<strong>From January it stops balancing.</strong> Cowrywise ends in December, freeing ' +
      naira(100000) + '/month \u2014 but Goal 2 needs ' + naira(428571) + ' and the emergency ' +
      'fund ' + naira(50000) + '. At the August mix that is <strong>' + naira(-short[0].left) +
      ' short, every month from January to June</strong>.',
      'That gap is the course\u2019s job. It is also far smaller than the ₦152,000\u2013₦186,000 ' +
      'money.md carried \u2014 that figure was a Sep\u2013Dec surplus wrongly applied to a period ' +
      'in which Cowrywise has already stopped.'));
  }

  /* ------------------------------------------------------- savings plan */

  add(h('h2', {}, 'The savings plan'));
  add(h('p', { class: 'lede', style: 'margin-bottom:14px' },
    'Per month, not a flat average \u2014 and ',
    h('strong', {}, 'every pot needs an account it physically goes into'),
    '. A pot with no home cannot be funded on payday.'));

  const months26 = ['2026-09', '2026-10', '2026-11', '2026-12'];
  add(h('div', { class: 'card pad-0' },
    table(['Pot', 'Where it lives', 'Payday', { label: 'Target', num: true },
      ...months26.map(m => ({ label: mLabel(m), num: true }))],
      B.savings.map(v => [
        h('strong', {}, v.pot),
        v.account === 'NOT SET'
          ? h('span', { class: 'pill bad' }, 'NOT SET')
          : h('span', { class: 't-sm' }, v.account),
        h('span', { class: 'pill ' + (v.payday === 'A' ? 'ok' : 'info') }, v.payday),
        naira(v.target),
        ...months26.map(m => v.schedule[m]
          ? naira(v.schedule[m])
          : h('span', { class: 't-dim' }, '\u2014')),
      ]))));

  const homeless = B.savings.filter(v => !v.account || /^NOT SET/i.test(v.account));
  const clashes = (() => {
    const byAcct = {};
    B.savings.forEach(v => {
      // Normalise to the INSTITUTION. "Cowrywise (locked)" and
      // "Cowrywise — created 2026-09-02" are the same place, and the whole
      // point of this callout is to say so.
      const raw = (v.account || '').trim();
      if (!raw || /^NOT SET/i.test(raw)) return;
      const a = raw.split(/\s+[—(]/)[0].replace(/[^A-Za-z0-9 ]/g, '').trim().toLowerCase();
      if (!a) return;
      (byAcct[a] = byAcct[a] || { label: raw.split(/\s+—/)[0].trim(), pots: [] }).pots.push(v.pot);
    });
    return Object.values(byAcct).filter(g => g.pots.length > 1);
  })();

  add(callout('warn', '\u26a0',
    ...clashes.map(g =>
      '<strong>' + g.pots.length + ' pots, one place \u2014 ' + g.label + '.</strong> ' +
      g.pots.join(' and ') + ' share it. Two pots that mean different things behind one ' +
      'balance, and a balance that means two things means neither.'),
    ...(homeless.length
      ? homeless.map(v => '<strong>' + v.pot + ' has no account.</strong> A pot with no home ' +
          'cannot be funded on payday.')
      : ['<strong>Every pot has a home.</strong> Nothing is waiting on an account to exist.'])));

  add(h('div', { class: 'card pad-0', style: 'margin-top:10px' },
    table(['Pot', 'What it is'],
      B.savings.map(v => [
        h('strong', {}, v.pot),
        h('span', { class: 't-sm t-dim' }, v.note),
      ]))));

  /* ------------------------------------------------------- lean ladder */

  add(h('h2', {}, 'The lean-month ladder'));
  add(notesFor('budget', 'n5'));
  add(h('div', { class: 'card', style: 'margin-top:10px' },
    h('div', { class: 'rows' },
      B.lean_ladder.filter(l => /^\d\./.test(l.trim())).map((l, i) =>
        h('div', { class: 'row' },
          h('div', { class: 'r mono', style: 'min-width:26px;font-size:17px;font-weight:700;color:var(--amber)' }, i + 1),
          h('div', { class: 'grow' }, h('div', { class: 't' }, l.replace(/^\d\.\s*/, ''))))),
      h('div', { class: 'row' },
        h('div', { class: 'r mono', style: 'min-width:26px;font-size:17px;font-weight:700;color:var(--red)' }, '!'),
        h('div', { class: 'grow' },
          h('div', { class: 't' }, 'Savings are never the valve (Rule 1). Cowrywise never pauses (Rule 7).'),
          h('div', { class: 's' }, 'If the buffer is empty, an urgency gets negotiated, not funded.'))))));

  /* ------------------------------------------------------------ how it works */

  add(h('h2', {}, 'How this stays honest'));
  add(toggle('The rule that makes a budget line unable to lie', 'carried over from the sheet',
    h('p', {}, h('strong', {}, 'Nothing is typed where it should be derived. '),
      'A category total is the SUM of its named line items. An actual is the SUM of logged rows. ' +
      'Neither can be typed over.'),
    h('p', {}, 'That design came straight out of the June–August failure: the old sheets booked ' +
      '₦900,250 to savings that never moved, because a budget line could simply say a number. ' +
      h('strong', {}, 'A budget line that says money was saved when no money moved is a lie in a ' +
        'spreadsheet.')),
    h('p', {}, h('strong', {}, 'The finding worth keeping: '),
      'his estimate and his truth differed by ₦5,940. Feeding\'s ₦150,000 did not become savings — ' +
      'it moved house, into transport, data, household, the gym and a misc line that did not exist ' +
      'before. Nothing got cheaper. Worth remembering the next time a category looks like it has ' +
      'slack in it.')));

  /* ------------------------------------------------------------ shopping */
  const SH = OS.shopping || {};
  if ((SH.buying || []).length) {
    const priced  = SH.buying.filter(i => i.amount && !i.held);
    const held    = SH.buying.filter(i => i.held);
    const noPrice = SH.buying.filter(i => !i.amount && !i.held);
    const byLine  = {};
    priced.forEach(i => { byLine[i.line] = (byLine[i.line] || 0) + i.amount; });

    add(h('h2', {}, 'Things to buy'));
    add(h('p', { class: 't-dim' }, SH.note || ''));

    add(h('div', { class: 'grid' },
      statCard('Buying this month', naira(priced.reduce((a, i) => a + i.amount, 0), { short: true }),
        priced.length + ' items, all inside a budget line', 'green'),
      statCard('Held back', held.length ? naira(held.reduce((a, i) => a + i.amount, 0), { short: true }) : '—',
        held.length ? held.map(i => i.item).join(', ') + ' — kept in the cushion' : 'nothing held', 'blue'),
      statCard('No price yet', String(noPrice.length + (SH.wishlist || []).filter(w => !w.amount).length),
        'unpriced items cannot be planned against a surplus', noPrice.length ? 'amber' : '')));

    add(h('div', { class: 'card pad-0', style: 'margin-top:10px' },
      table(['Item', { label: '₦', num: true }, 'Comes out of', 'Payday'],
        SH.buying.map(i => [
          h('span', {}, i.item,
            i.new ? h('span', { class: 'pill ok', style: 'margin-left:6px' }, 'new') : null,
            i.held ? h('span', { class: 'pill info', style: 'margin-left:6px' }, 'held') : null,
            i.note ? h('span', { class: 'sub' }, i.note) : null),
          i.amount ? naira(i.amount) : h('span', { class: 't-dim' }, '?'),
          i.line,
          h('span', { class: 'pill ' + (i.payday === 'A' ? 'ok' : 'info') }, i.payday || '—'),
        ]))));

    add(h('div', { class: 'card pad-0', style: 'margin-top:10px' },
      table(['Budget line', { label: 'This list takes', num: true }, { label: 'The line holds', num: true }],
        Object.keys(byLine).sort((a, b) => byLine[b] - byLine[a]).map(k => {
          const hold = planByCat[k] || 0;
          return [k, naira(byLine[k]),
            hold ? h('span', { class: 'v ' + (byLine[k] > hold ? 'red' : 'green') }, naira(hold))
                 : h('span', { class: 't-dim' }, '—')];
        }))));

    if (SH.buying_note) add(callout('ok', '✓', SH.buying_note));

    add(toggle('The wish list', 'only from spare cash, and only after every pot is funded',
      h('p', {}, SH.wishlist_note || ''),
      table(['Item', { label: '₦', num: true }, 'Note'],
        (SH.wishlist || []).map(w => [
          w.item,
          w.amount ? naira(w.amount) : h('span', { class: 't-dim' }, '?'),
          w.note || '',
        ]))));
  }

  add(toggle('The two paydays', 'the spine of the budget',
    h('p', {}, 'One batch, two dates. Payday A is the 70% landing at the end of the previous month ' +
      'and funds the 1st–14th. Payday B is the 30% landing around the 14th and funds the 15th to ' +
      'month end. ', h('strong', {}, 'The 30% is always the previous month\'s remaining batch, never a new one.')),
    table(['', 'Payday A — 70%', 'Payday B — 30%'], [
      ['Expected in', naira(inA), naira(inB)],
      ['Bills and one-offs', naira(paydayA), naira(paydayB)],
      ['Into the pots', naira(potsA), naira(potsB)],
      [h('strong', {}, 'Cushion'),
        h('strong', { class: 'v ' + (inA - paydayA - potsA < 0 ? 'red' : 'green') },
          naira(inA - paydayA - potsA)),
        h('strong', { class: 'v ' + (inB - paydayB - potsB < 0 ? 'red' : 'green') },
          naira(inB - paydayB - potsB))],
    ]),
    h('p', {}, h('strong', {}, 'The pots are committed money, so they are subtracted here. '),
      'Cowrywise moves on A; Goal 1 and the Buffer move on B. A cushion figure that ignores ' +
      'them is a number that gets spent twice.'),
    h('p', {}, h('strong', {}, 'Girlfriend moved to A '), '— she needs it at the start of the month ' +
      'for household essentials. ', h('strong', {}, 'Community admin moved to B '),
      '— he is paid mid-month.'),
    h('p', {}, h('strong', {}, 'And the front half got funded. '),
      'Feeding, transport, household and personal/misc used to sit entirely on Payday B, which left ' +
      'the 1st–14th with almost nothing to run on — and that already cost something real: he missed ' +
      'church on 30 August for want of ₦5,000. Each of those lines is now split, its front-half share ' +
      'on A and the remainder on B. ',
      h('strong', {}, 'Same monthly totals. The failure was the timing, not the size.')),
    OS.income.charge_note ? h('p', {}, h('strong', { class: 'v red' }, 'These figures are NET. '),
      OS.income.charge_note) : null));
})();
