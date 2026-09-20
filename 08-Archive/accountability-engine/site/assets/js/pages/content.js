/* Samuelsignals OS — Content & Audience. */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, pct, num, dateLabel, daysUntil, daysLabel, statCard, callout,
          toggle, table, pageHead, note, legend, bar, doc } = S;

  S.chrome('content');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const C = OS.content;
  const goal = OS.goals.find(g => g.id === 'wednesdays');

  add(pageHead('Content & Audience', 'Depth over volume. The cadence is the point.',
    'His own reading of his own posted content: <em>"it is when I focus and put in time in one ' +
    'video does it get views and reach... if I focus on quality, I get feedbacks and follows."</em>'));

  add(h('div', { class: 'grid g4 tight' },
    statCard('Wednesdays shipped', `${goal.current} / ${goal.target}`, 'consecutive, no miss', 'red'),
    statCard('Instagram', num(C.instagram), 'followers', 'pink'),
    statCard('TikTok', num(C.tiktok), 'followers', 'pink'),
    statCard('Weeks banked', '0 / 18', 'cadence has not run once', 'amber')));

  add(h('div', { style: 'margin-top:14px' }, notesFor('content', 'n1')));

  add(h('h2', {}, 'The 18 Wednesdays'));
  const streakHost = h('div');
  add(h('div', { class: 'card' },
    h('div', { class: 'card-h' }, h('h3', {}, 'Every Wednesday to 31 December'),
      h('span', { class: 'sub' }, `${goal.current} of ${goal.target}`)),
    streakHost,
    legend([[K.COLOURS.green, 'Shipped'], [K.COLOURS.red, 'Missed'], ['#1e2632', 'Still to come']]),
    notesFor('content', 'n2')));

  const cells = [];
  const d = new Date(C.cadence_start + 'T00:00:00');
  for (let i = 0; i < 18; i++) {
    const iso = d.toISOString().slice(0, 10);
    const past = daysUntil(iso) < 0;
    cells.push({
      state: past ? 'miss' : 'future',
      tick: i % 3 === 0 ? String(d.getDate()) : '',
      label: `Week ${i + 1} — ${iso}`,
    });
    d.setDate(d.getDate() + 7);
  }
  K.streak(streakHost, cells, { cell: 26 });

  add(notesFor('content', 'n3'));

  add(h('h2', {}, 'The weekly pipeline'));
  add(h('div', { class: 'card pad-0' },
    table(['Day', 'Phase', { label: 'Hours', num: true }, 'Block'],
      C.pipeline.map(p => [
        h('strong', { class: p.day === 'Wednesday' ? 'v pink' : '' }, p.day),
        p.phase, p.hours || '—', p.block,
      ]))));

  add(h('div', { style: 'margin-top:12px' }, notesFor('content', 'n4')));

  add(h('h2', {}, 'Community and mentorship'));
  add(h('div', { class: 'grid g3' },
    statCard('HighSignals community', num(C.community_members), 'members, currently free'),
    statCard('Mentees', num(C.mentees), 'unpaid, ad hoc, ~1h/week'),
    statCard('Community admin', '₦15,000', 'per month — not a cost-cutting target')));

  add(h('div', { style: 'margin-top:12px' }, notesFor('content', 'n5')));

  add(h('h2', {}, 'context/audience.md'));
  add(doc('audience'));
})();
