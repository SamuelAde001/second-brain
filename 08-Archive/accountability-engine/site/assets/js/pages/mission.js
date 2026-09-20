/* Samuelsignals OS — Mission & Stakes. His files, verbatim. */

(function () {
  const S = window.SS, OS = S.OS;
  const { h, pageHead, callout, doc } = S;

  S.chrome('mission');
  if (!S.guard()) return;
  const M = document.getElementById('main');
  const add = (...n) => n.flat().forEach(x => x && M.appendChild(x));

  add(pageHead('Mission & Stakes', 'What he is building, and what he loses if he doesn\'t.',
    'These two files are his. Everything else on this site is generated and can be rebuilt; ' +
    '<strong>these are never rewritten without his word.</strong>'));

  add(notesFor('mission', 'n1'));

  add(h('h2', {}, 'Mission'));
  add(doc('mission'));

  add(h('h2', {}, 'Stakes'));
  add(doc('stakes'));

  add(notesFor('mission', 'n2'));
})();
