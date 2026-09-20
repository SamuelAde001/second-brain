/* Samuelsignals OS — Spirit. The one he named first. */

(function () {
  const S = window.SS, K = window.SSCharts, OS = S.OS;
  const { h, statCard, callout, table, pageHead, note, legend, doc } = S;

  S.chrome('spirit');
  const SP = OS.spirit || {};
  const DAY = (OS.rules || {}).day || {};
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  const log = OS.habit_log || {};
  const dates = Object.keys(log).sort();
  const SPIRIT = ['Prayed', 'Bible study (morning)', 'No social media (detox)', 'No masturbating'];
  const count = n => dates.filter(d => log[d][n] === true).length;

  add(pageHead('Spirit', 'Time with God every single day, without a miss.',
    '<strong>This is the one he named first when asked about his life. It is not third on a list.</strong> ' +
    'Weekly minimum is 7/7 — this one has no acceptable miss rate.'));

  add(h('div', { class: 'grid g4 tight' },
    statCard('Prayed', `${count('Prayed')}/${dates.length}`, 'days on the record', 'green'),
    statCard('Bible study', `${count('Bible study (morning)')}/${dates.length}`, `the ${DAY.prayer || '—'} block`, 'green'),
    statCard('The block', `${DAY.prayer_minutes || '—'} min`, `${DAY.prayer || '—'}, prayer and Bible combined`),
    statCard('Next church', SP.church_next ? daysLabel(daysUntil(SP.church_next)) : '—',
      SP.church_status === 'ON' ? SP.church_note : 'OFF — ' + (SP.last_missed||{}).reason,
      SP.church_status === 'ON' ? 'green' : 'red')));

  add(h('div', { style: 'margin-top:14px' }, notesFor('spirit', 'n1')));

  add(h('h2', {}, 'The habits that carry it'));
  const heatHost = h('div', { style: 'overflow-x:auto' });
  add(h('div', { class: 'card' },
    h('div', { class: 'card-h' }, h('h3', {}, 'Every day of the 7-day block'),
      h('span', { class: 'sub' }, '25–31 Aug')),
    heatHost,
    legend([[K.COLOURS.green, 'Hit'], [K.COLOURS.red, 'Broken'], ['#1e2632', 'Not tracked']]),
    notesFor('spirit', 'n2')));
  K.heatmap(heatHost, SPIRIT, dates, (n, d) => (log[d] && log[d][n] !== undefined) ? log[d][n] : null,
    { cell: 30, labelW: 160 });

  add(h('h2', {}, 'Sunday is not a free day'));
  add(h('div', { class: 'card pad-0' },
    table(['', ''], [
      ['Service', '9:00am'],
      ['Commute', h('strong', {}, 'up to 1h30 each way')],
      ['Leaves', '~7:30am'],
      ['Service ends', '12:30pm'],
      ['Home', '~3:00pm'],
      [h('strong', {}, 'Total'), h('strong', { class: 'v amber' }, '~7.5 hours')],
    ])));

  add(h('div', { style: 'margin-top:12px' }, notesFor('spirit', 'n3')));

  add(h('div', { style: 'margin-top:12px' }, notesFor('spirit', 'n4')));

  add(h('h2', {}, 'context/spirit.md'));
  add(doc('spirit'));
})();
