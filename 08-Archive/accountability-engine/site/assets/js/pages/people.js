/* Samuelsignals OS — People. */

(function () {
  const S = window.SS, OS = S.OS;
  const { h, naira, statCard, callout, table, pageHead, doc } = S;

  S.chrome('people');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  add(pageHead('People', 'The monthly visit fails in the week before it, not on the day.',
    'One new content creator visited in Abuja every month — someone he invites and meets in ' +
    'person, <strong>named in advance, met on a named date.</strong>'));

  add(h('div', { class: 'grid g4 tight' },
    statCard('Creators visited', '0', 'outreach rate effectively zero', 'red'),
    statCard('Girlfriend, September', naira(150000), '₦100k allowance + ₦50k school', 'pink'),
    statCard('Owed to his sister', naira(50000), 'after September · NO DATE', 'amber'),
    statCard('Community admin', naira(15000), 'per month · not a cost-cutting target')));

  add(h('div', { style: 'margin-top:14px' }, notesFor('people', 'n1')));

  add(h('h2', {}, 'Girlfriend'));
  add(notesFor('people', 'n2'));

  add(h('h2', {}, 'The network line, and what it cost'));
  add(notesFor('people', 'n3'));

  add(h('h2', {}, 'The live debt'));
  add(notesFor('people', 'n4'));

  add(h('h2', {}, 'Money that goes to people'));
  const cats = ['Girlfriend', 'Parents', 'Community admin', 'Creator visits', 'Giving', 'Other'];
  const rows = OS.budget.items.filter(i => i.active && cats.includes(i.category));
  add(h('div', { class: 'card pad-0' },
    table(['Item', 'Category', { label: 'Amount', num: true }, 'Payday', 'Note'],
      rows.sort((a, b) => b.amount - a.amount).map(i => [
        h('strong', {}, i.item), i.category, naira(i.amount),
        h('span', { class: 'pill ' + (i.payday === 'A' ? 'ok' : 'info') }, i.payday || '—'),
        h('span', { class: 't-sm t-dim' }, (i.note || '').slice(0, 160)),
      ]))));

  add(h('h2', {}, 'context/people.md'));
  add(doc('people'));
})();
