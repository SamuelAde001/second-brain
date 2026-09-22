#!/usr/bin/env node
// Smoke test for edit-clock.html. Stubs just enough DOM to run the inline
// script, then checks the behaviour that has broken before.
// Usage: node test_clock.js path/to/edit-clock.html
const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
if (!file) { console.error('Usage: node test_clock.js <edit-clock.html>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) { console.error('FAIL  no inline <script> block found'); process.exit(1); }
const js = match[1];
const KEY = (js.match(/\bKEY\s*=\s*'([^']+)'/) || [])[1];

const HOUR = 3600000;
let failures = 0;
function check(name, ok, detail) {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + name + (detail !== undefined ? '  [' + detail + ']' : ''));
  if (!ok) failures++;
}

// Run the page script against a fake DOM and the given storage object.
function boot(store) {
  const els = {};
  function el() {
    const on = {};
    return {
      textContent: '', value: '', style: {},
      classList: { toggle() {}, add() {}, remove() {} },
      addEventListener(type, fn) { on[type] = fn; },
      focus() {},
      click() { if (on.click) on.click(); },
    };
  }
  const document = {
    getElementById: id => els[id] || (els[id] = el()),
    addEventListener() {},
    visibilityState: 'visible',
  };
  const ctx = {
    document,
    navigator: {},
    setInterval() {},
    localStorage: {
      getItem: k => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: k => { delete store[k]; },
    },
  };
  vm.createContext(ctx);
  vm.runInContext(js, ctx);
  return id => document.getElementById(id);
}

// WAT clock time offsetMs from now, as HH:MM (minutes rounded down).
function watHHMM(offsetMs) {
  const d = new Date(Date.now() + HOUR + offsetMs);
  return String(d.getUTCHours()).padStart(2, '0') + ':' + String(d.getUTCMinutes()).padStart(2, '0');
}
const saved = store => (store[KEY] ? JSON.parse(store[KEY]) : null);

// 0. script runs at all
try { boot({}); check('script runs without errors', true); }
catch (e) { check('script runs without errors', false, e.message); process.exit(1); }
check('storage key found', !!KEY, KEY);

// 1. a plan from days ago is cleared, so a new video opens at setup
{
  const now = Date.now();
  const store = { [KEY]: JSON.stringify({ endPos: 2026, anchorPos: 653, anchorEpoch: now - 72 * HOUR, endEpoch: now - 68 * HOUR, dh: 19, dm: 0, last: null }) };
  boot(store);
  check('stale plan is cleared on load', !(KEY in store));
}

// 2. an active plan survives a refresh and shows the right target
{
  const now = Date.now();
  const store = { [KEY]: JSON.stringify({ endPos: 1800, anchorPos: 600, anchorEpoch: now - HOUR, endEpoch: now + HOUR, dh: 0, dm: 0, last: null }) };
  const $ = boot(store);
  check('active plan survives reload', KEY in store);
  check('target is halfway along the line', /^(19:5\d|20:0\d)$/.test($('target').textContent), $('target').textContent);
}

// 3. setup, check-ins and re-anchor
{
  const store = {};
  const $ = boot(store);
  $('f-len').value = '30:00'; $('f-pos').value = '10:00'; $('f-end').value = watHHMM(2 * HOUR);
  $('go').click();
  const S = saved(store);
  const hrs = S ? (S.endEpoch - Date.now()) / HOUR : -1;
  check('setup saves a plan', !!S);
  check('deadline locked about 2h ahead', hrs > 1.95 && hrs <= 2.0, hrs.toFixed(3));
  check('target starts at current position', $('target').textContent === '10:00', $('target').textContent);
  check('rate is about 10:00 per hour', /^10:0\d$/.test($('rate').textContent), $('rate').textContent);

  $('actual').value = '08:00'; $('check-btn').click();
  check('check-in behind the line says behind', /behind/.test($('verdict').textContent), $('verdict').textContent);
  $('actual').value = '12:00'; $('check-btn').click();
  check('check-in ahead of the line says ahead', /ahead/.test($('verdict').textContent), $('verdict').textContent);

  $('actual').value = '12:00'; $('reanchor').click();
  const S2 = saved(store);
  check('re-anchor moves the start to the real position', S2 && S2.anchorPos === 720 && S2.last === null);
  check('re-anchor keeps the deadline', S2 && S && S2.endEpoch === S.endEpoch);
}

// 4. bad input is rejected with a message
{
  const store = {};
  const $ = boot(store);
  $('f-len').value = 'abc'; $('f-pos').value = '10:00'; $('f-end').value = '19:00';
  $('go').click();
  check('bad length is rejected with a message', !(KEY in store) && $('setup-err').textContent.length > 0, $('setup-err').textContent);
}

// 5. a finish-by time earlier than now rolls to tomorrow
{
  const store = {};
  const $ = boot(store);
  $('f-len').value = '30:00'; $('f-pos').value = '10:00'; $('f-end').value = watHHMM(-2 * HOUR);
  $('go').click();
  const S = saved(store);
  const hrs = S ? (S.endEpoch - Date.now()) / HOUR : -1;
  check('earlier clock time rolls to tomorrow', hrs > 21.95 && hrs <= 22.0, hrs.toFixed(3));
}

console.log(failures ? `\n${failures} check(s) failed` : '\nAll checks passed');
process.exit(failures ? 1 : 0);
