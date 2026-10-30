# Records a real website as a frame-exact live-demo screen recording, off-screen, in headless Chrome (take mp4 + contact sheet + log).
# Usage: python record_demo.py shot.json [--out DIR] [--width CSS_PX] [--still SECONDS] [--compare 1280,1536,1920 --at SECONDS] [--keep-frames]
# Promoted from video 4 on 2026-10-30.
"""record_demo.py - record a real website as a live-demo screen recording, fully off-screen.

Headless Chrome (its own throwaway profile, never Samuel's browser, nothing on his screen) is driven
over the DevTools protocol. The page renders normally, but its clock is ours: from the first frame
of the take, the page's timers, requestAnimationFrame, performance.now/Date, CSS + WAAPI animations,
SVG animations and <video> all advance exactly 1/fps per captured frame. So the site's own animations,
counters, marquees and hover transitions play at true speed however long each capture takes, and the
take is frame-exact. Scroll is eased; a macOS-style cursor glides to what is being talked about and
real mouse events make the page's hover states fire. The page is rendered at device scale
out_w / viewport_width (1536 CSS px -> 1920 px is DPR 1.25), so text is sharp, never upscaled.

  python record_demo.py shot.json                     take -> <out>/<name>.mp4 + _sheet.jpg + .log.json
  python record_demo.py shot.json --still 6.5         one PNG of the moment at 6.5 s
  python record_demo.py shot.json --compare 1280,1536,1920 --at 6.5
                                                      the same moment at three zoom levels, side by side
  options: --out DIR   --width CSS_PX   --keep-frames

Shot JSON: see README.md next to this file. Stdlib + ffmpeg; Pillow for the sheet and --compare.
Safety: never logs in, never types, never submits a form, never accepts cookies (rejects or hides the
banner), real clicks only on tabs / accordions / toggles that do not navigate.
"""
import os, sys, json, time, math, base64, socket, struct, subprocess, shutil, glob, argparse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9361
PROFILE = os.path.join(os.environ.get("TEMP", HERE), "demo_rec_chrome")
FFMPEG = shutil.which("ffmpeg") or (glob.glob(os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe")) or ["ffmpeg"])[0]


# ---------------------------------------------------------------- DevTools client (stdlib websocket)
class CDP:
    def __init__(self, url):
        hostport, path = url[5:].split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)), timeout=90)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(("GET /%s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        "Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n" % (path, hostport, key)).encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.id = 0
        self.events = []
        self.done = {}
        self.partial = b""

    def _frame(self):
        """One whole websocket frame from the buffer, or None; nothing is consumed until it is whole,
        so a socket timeout never leaves the stream half-read."""
        b = self.buf
        if len(b) < 2:
            return None
        n, off = b[1] & 0x7F, 2
        if n == 126:
            if len(b) < 4: return None
            n, off = struct.unpack(">H", b[2:4])[0], 4
        elif n == 127:
            if len(b) < 10: return None
            n, off = struct.unpack(">Q", b[2:10])[0], 10
        if len(b) < off + n:
            return None
        fin, op, payload = b[0] & 0x80, b[0] & 0x0F, b[off:off + n]
        self.buf = b[off + n:]
        return fin, op, payload

    def _recv(self, timeout):
        end = time.time() + timeout
        while True:
            f = self._frame()
            if f:
                fin, op, payload = f
                if op == 8:
                    raise IOError("devtools socket closed")
                if op in (9, 10):
                    continue
                self.partial += payload
                if fin:
                    msg, self.partial = self.partial, b""
                    return json.loads(msg.decode("utf-8", "ignore"))
                continue
            left = end - time.time()
            if left <= 0:
                return None
            self.s.settimeout(left)
            try:
                chunk = self.s.recv(1 << 20)
            except socket.timeout:
                return None
            if not chunk:
                raise IOError("devtools socket closed")
            self.buf += chunk

    def _send(self, text):
        data = text.encode()
        hdr = bytearray([0x81])
        n = len(data)
        if n < 126: hdr.append(0x80 | n)
        elif n < 65536: hdr.append(0x80 | 126); hdr += struct.pack(">H", n)
        else: hdr.append(0x80 | 127); hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        self.s.sendall(bytes(hdr) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def send(self, method, params=None):
        self.id += 1
        self._send(json.dumps({"id": self.id, "method": method, "params": params or {}}))
        return self.id

    def _stash(self, m):
        if "id" in m:
            if len(self.done) > 500:
                self.done.clear()
            self.done[m["id"]] = m
        elif "method" in m and len(self.events) < 2000:
            self.events.append(m)

    def wait(self, mid, timeout):
        """Result of command mid, or None on timeout (the command stays pending)."""
        m = self.done.pop(mid, None)
        end = time.time() + timeout
        while m is None:
            r = self._recv(max(0.0, end - time.time()))
            if r is None:
                return None
            if r.get("id") == mid:
                m = r
            else:
                self._stash(r)
        if "error" in m:
            raise RuntimeError("devtools error: %s" % m["error"])
        return m.get("result", {})

    def call(self, method, params=None, timeout=90):
        r = self.wait(self.send(method, params), timeout)
        if r is None:
            raise TimeoutError(method)
        return r

    def wait_event(self, name, timeout=30):
        for i, e in enumerate(self.events):
            if e["method"] == name:
                return self.events.pop(i)
        end = time.time() + timeout
        while time.time() < end:
            m = self._recv(max(0.0, end - time.time()))
            if m is None:
                break
            if m.get("method") == name:
                return m
            self._stash(m)
        raise TimeoutError(name)

    def js(self, expr, await_promise=False, timeout=90):
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True,
                                           "awaitPromise": await_promise}, timeout)
        if r.get("exceptionDetails"):
            raise RuntimeError("page JS failed: " + json.dumps(r["exceptionDetails"])[:600])
        return r.get("result", {}).get("value")


def chrome_up():
    try:
        return json.loads(urllib.request.urlopen("http://127.0.0.1:%d/json/version" % PORT, timeout=1).read())
    except Exception:
        return None


def start_chrome():
    v = chrome_up()
    if v:
        return v
    # headless=new: no window ever appears on Samuel's screen; its own profile, never his.
    subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT, "--user-data-dir=%s_%d" % (PROFILE, PORT),
                      "--window-size=1920,1080", "--hide-scrollbars", "--force-color-profile=srgb",
                      "--remote-allow-origins=*", "--mute-audio", "--no-first-run", "--no-default-browser-check",
                      "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
                      "--disable-backgrounding-occluded-windows", "--autoplay-policy=no-user-gesture-required",
                      "--lang=en-US", "about:blank"],
                     creationflags=0x8 | 0x200, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(80):
        time.sleep(0.25)
        v = chrome_up()
        if v:
            return v
    raise RuntimeError("headless Chrome did not start")


def new_tab():
    info = json.loads(urllib.request.urlopen(urllib.request.Request(
        "http://127.0.0.1:%d/json/new?about:blank" % PORT, method="PUT"), timeout=10).read())
    return info, CDP(info["webSocketDebuggerUrl"])


def close_tab(info):
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/json/close/%s" % (PORT, info["id"]), timeout=5)
    except Exception:
        pass


# ---------------------------------------------------------------- the page clock (runs before any page script)
# Until freeze() everything is the real clock. freeze() moves every pending timer / rAF onto our clock;
# advance(ms) then runs due timers in order, the rAF callbacks, and steps CSS/WAAPI/SVG animations.
CLOCK_JS = r"""
(() => {
if (window.__vt) return;
const N = {now: performance.now.bind(performance), dnow: Date.now, raf: window.requestAnimationFrame.bind(window),
  caf: window.cancelAnimationFrame.bind(window), st: window.setTimeout.bind(window), ct: window.clearTimeout.bind(window),
  si: window.setInterval.bind(window), ci: window.clearInterval.bind(window), Date: window.Date};
const V = window.__vt = {N, f: {raf: true, timers: true, time: true}, on: false, t: 0, p0: 0, d0: 0, id: 5e6, timers: new Map(), rafs: new Map(), anims: new Map(), svgs: null};
const run = (fn, args) => { try { typeof fn === 'function' ? fn(...args) : 0; } catch (e) { N.st(() => { throw e; }); } };
performance.now = () => V.on && V.f.time ? V.t : N.now();
Date.now = () => V.on && V.f.time ? Math.round(V.d0 + V.t - V.p0) : N.dnow();
const D = N.Date;
function VDate(...a) { if (!new.target) return new D(Date.now()).toString(); return a.length ? new D(...a) : new D(Date.now()); }
VDate.prototype = D.prototype; VDate.now = Date.now; VDate.parse = D.parse; VDate.UTC = D.UTC;
window.Date = VDate;
window.setTimeout = function (fn, ms, ...args) { const on = V.on && V.f.timers, id = ++V.id, e = {fn, args, every: 0, at: (on ? V.t : N.now()) + Math.max(0, +ms || 0)};
  if (!on) e.nid = N.st(() => { V.timers.delete(id); run(fn, args); }, ms);
  V.timers.set(id, e); return id; };
window.setInterval = function (fn, ms, ...args) { const on = V.on && V.f.timers, id = ++V.id, iv = Math.max(4, +ms || 0), e = {fn, args, every: iv, at: (on ? V.t : N.now()) + iv};
  if (!on) e.nid = N.si(() => { e.at = N.now() + iv; run(fn, args); }, iv);
  V.timers.set(id, e); return id; };
window.clearTimeout = window.clearInterval = id => { const e = V.timers.get(id);
  if (e) { if (e.nid != null) { N.ct(e.nid); N.ci(e.nid); } V.timers.delete(id); } else { N.ct(id); N.ci(id); } };
window.requestAnimationFrame = cb => { const id = ++V.id, e = {cb};
  if (!(V.on && V.f.raf)) e.nid = N.raf(ts => { if (V.rafs.get(id) !== e) return; V.rafs.delete(id); run(cb, [ts]); });
  V.rafs.set(id, e); return id; };
window.cancelAnimationFrame = id => { const e = V.rafs.get(id); if (e) { if (e.nid != null) N.caf(e.nid); V.rafs.delete(id); } else N.caf(id); };
V.freeze = () => { if (V.on) return; V.p0 = V.t = N.now(); V.d0 = N.dnow();
  if (V.f.timers) for (const e of V.timers.values()) if (e.nid != null) { N.ct(e.nid); N.ci(e.nid); e.nid = null; }
  if (V.f.raf) for (const e of V.rafs.values()) if (e.nid != null) { N.caf(e.nid); e.nid = null; }
  V.on = true;
  // Headless Chrome only answers a screenshot quickly while a large area of the page keeps redrawing
  // (otherwise it waits ~1.4 s for a fresh frame). A full-viewport overlay at 0.1-0.2 % grey, animated by
  // the compositor and never stepped by us, keeps that going: no visible pixel changes (< 0.3 of a level).
  const st = document.createElement('style');
  st.textContent = '@keyframes __vt_keep{from{opacity:.001}to{opacity:.002}}';
  document.documentElement.appendChild(st);
  const px = V.px = document.createElement('div');
  px.style.cssText = 'margin:0 !important;padding:0 !important;border:0 !important;position:fixed !important;left:0 !important;top:0 !important;width:100vw !important;height:100vh !important;z-index:2147483646 !important;pointer-events:none !important;display:block !important;background:#808080 !important;animation:__vt_keep .5s linear infinite alternate !important;';
  document.documentElement.appendChild(px);
  V.step(); };
V.step = () => {   // CSS animations, transitions, WAAPI: paused, then seeked to our clock
  let n = 0;
  for (const a of document.getAnimations()) { if (V.px && a.effect && a.effect.target === V.px) continue; let o = V.anims.get(a);
    if (!o) { o = {c: a.currentTime || 0, t0: V.t}; V.anims.set(a, o); try { a.pause(); } catch (e) {} }
    try { a.currentTime = o.c + (V.t - o.t0) * (a.playbackRate || 1); n++; } catch (e) {} }
  if (!V.svgs) { V.svgs = [...document.querySelectorAll('svg')].filter(s => s.querySelector('animate,animateTransform,animateMotion,set'))
    .map(s => { try { s.pauseAnimations(); } catch (e) {} return {s, c: s.getCurrentTime ? s.getCurrentTime() : 0, t0: V.t}; }); }
  for (const o of V.svgs) try { o.s.setCurrentTime(o.c + (V.t - o.t0) / 1000); } catch (e) {}
  return n; };
V.advance = ms => { if (!V.on) V.freeze(); const end = V.t + ms;
  for (let g = 0; g < 5000; g++) { let nid = null, nat = Infinity;
    for (const [id, e] of V.timers) if (e.at <= end && e.at < nat) { nat = e.at; nid = id; }
    if (nid === null) break;
    const e = V.timers.get(nid); V.t = Math.max(V.t, e.at);
    if (e.every) e.at += e.every; else V.timers.delete(nid);
    run(e.fn, e.args); }
  V.t = end;
  const cbs = [...V.rafs.values()]; V.rafs.clear();
  for (const e of cbs) run(e.cb, [V.t]);
  return V.step(); };
})();
"""

# ---------------------------------------------------------------- page-side helpers (after load)
PAGE_JS = r"""
(() => {
if (window.__demo) return 'ok';
const D = window.__demo = {refs: {}, vids: null};
const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
const vis = b => b && b.width > 0 && b.height > 0;
const shown = el => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const s = getComputedStyle(e);
  if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; } return true; };
D.sc = (() => { const se = document.scrollingElement || document.documentElement;
  if (se.scrollHeight > innerHeight + 5) return null;
  let best = null, bh = 0;
  for (const e of document.querySelectorAll('body *')) { const s = getComputedStyle(e);
    if ((s.overflowY === 'auto' || s.overflowY === 'scroll') && e.scrollHeight > e.clientHeight + 50 && e.clientHeight > innerHeight * 0.5 && e.scrollHeight > bh) { bh = e.scrollHeight; best = e; } }
  return best; })();
D.sy = () => D.sc ? D.sc.scrollTop : window.scrollY;
D.maxY = () => D.sc ? D.sc.scrollHeight - D.sc.clientHeight : (document.scrollingElement || document.documentElement).scrollHeight - innerHeight;
D.scroll = y => { y = Math.max(0, Math.min(y, D.maxY()));
  if (D.sc) D.sc.scrollTo({top: y, left: 0, behavior: 'instant'}); else window.scrollTo({top: y, left: 0, behavior: 'instant'});
  if (window.lenis && typeof window.lenis.scrollTo === 'function') { try { window.lenis.scrollTo(y, {immediate: true, force: true}); } catch (e) {} }
  return D.sy(); };
D.fixedOf = el => { for (let e = el; e && e !== document.documentElement; e = e.parentElement) { const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') return true; } return false; };
// a target is a CSS selector, or "text:<words>" (words exactly as on the page; case and spacing ignored)
D.findAll = spec => { const out = [];
  if (spec.startsWith('text:')) { const want = norm(spec.slice(5));
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
    while ((n = tw.nextNode())) { const raw = n.nodeValue; if (!raw || raw.length < want.length) continue;
      let nn = '', map = [];
      for (let i = 0; i < raw.length; i++) { const ch = raw[i];
        if (/\s/.test(ch)) { if (nn.length && nn[nn.length - 1] !== ' ') { nn += ' '; map.push(i); } }
        else { nn += ch.toLowerCase(); map.push(i); } }
      const k = nn.indexOf(want);
      if (k < 0) continue;
      const r = document.createRange(); r.setStart(n, map[k]); r.setEnd(n, map[k + want.length - 1] + 1);
      if (vis(r.getBoundingClientRect()) && shown(n.parentElement)) out.push({range: r, el: n.parentElement}); }
    if (!out.length) { const els = [...document.body.querySelectorAll('*')].filter(e => e.offsetParent !== null && norm(e.innerText).includes(want));
      for (const e of els) if (![...e.children].some(ch => norm(ch.innerText).includes(want)) && vis(e.getBoundingClientRect()) && shown(e)) out.push({el: e}); }
  } else { for (const e of document.querySelectorAll(spec)) if (vis(e.getBoundingClientRect()) && shown(e)) out.push({el: e}); }
  return out; };
D.reg = (id, spec, nth) => { const all = D.findAll(spec); if (!all.length) return null;
  D.refs[id] = all[Math.min(nth || 0, all.length - 1)]; const r = D.rect(id); r.count = all.length; return r; };
D.rect = id => { const m = D.refs[id]; if (!m) return null; const b = (m.range || m.el).getBoundingClientRect();
  return {x: b.left, y: b.top, w: b.width, h: b.height, fixed: D.fixedOf(m.el), sy: D.sy()}; };
// cookie / consent: click a reject / necessary-only button inside a consent box, else hide the banner. Never accept.
D.consent = mode => { const log = [];
  const rx = /^(reject|decline|deny|refuse|disagree|continue without|only (strictly )?(necessary|essential|required)|(use |allow |accept )?(only )?(strictly )?(necessary|essential|required)( cookies)?( only)?$)/i;
  const tag = e => (e.id || '') + ' ' + (typeof e.className === 'string' ? e.className : '') + ' ' + (e.getAttribute('aria-label') || '');
  const inBox = el => { for (let e = el, i = 0; e && i < 10; e = e.parentElement, i++)
    if (/cookie|consent|privacy|tracking|gdpr|cmp/i.test(tag(e)) || (i > 1 && /cookie|consent/i.test((e.innerText || '').slice(0, 2000)))) return true; return false; };
  if (mode !== 'hide') for (const b of document.querySelectorAll('button,a,[role=button],input[type=button]')) {
    const t = (b.innerText || b.value || b.getAttribute('aria-label') || '').trim();
    if (t.length < 60 && rx.test(t) && vis(b.getBoundingClientRect()) && inBox(b)) { b.click(); log.push('clicked "' + t + '"'); break; } }
  const known = '#onetrust-consent-sdk,#onetrust-banner-sdk,#CybotCookiebotDialog,#CookiebotWidget,#CybotCookiebotDialogBodyUnderlay,.cc-window,.cc-banner,#hs-eu-cookie-confirmation,.osano-cm-window,.osano-cm-dialog,#truste-consent-track,#usercentrics-root,#cmpbox,#cmpbox2,.cky-consent-container,.cky-overlay,#cookie-law-info-bar,.termly-styles-root,#axeptio_overlay,#didomi-host,#qc-cmp2-container,.fc-consent-root,#iubenda-cs-banner,#cookiescript_injected,#cookie-notice,.cookie-notice,#cookieConsent,.cookie-consent,[class*="cookie-banner" i],[id*="cookie-banner" i],[class*="cookieBanner"],[id*="cookieBanner"],[class*="consent-banner" i],[aria-label*="cookie" i][role=dialog],[aria-label*="consent" i][role=dialog]';
  for (const e of document.querySelectorAll(known)) { if (e.style.display !== 'none' && vis(e.getBoundingClientRect())) { e.style.setProperty('display', 'none', 'important'); log.push('hid ' + e.tagName + (e.id ? '#' + e.id : '')); } }
  for (const e of document.querySelectorAll('body *')) { const s = getComputedStyle(e);
    const txt = (s.position === 'fixed' || s.position === 'sticky') && e.offsetHeight > 30 ? (e.innerText || '') : '';
    if (txt && txt.length < 1200 && /cookie|consent/i.test(txt) && /accept|reject|agree|allow|decline|preferences|settings|got it/i.test(txt) && !e.matches('header,nav') && !e.querySelector('nav')) {
      e.style.setProperty('display', 'none', 'important'); log.push('hid fixed ' + e.tagName + (e.id ? '#' + e.id : '')); } }
  if (log.some(l => l.startsWith('hid'))) { for (const e of [document.documentElement, document.body]) if (getComputedStyle(e).overflow === 'hidden') e.style.setProperty('overflow', 'auto', 'important'); }
  return log; };
D.hide = sels => { let n = 0; for (const s of sels) { let l; try { l = document.querySelectorAll(s); } catch (e) { continue; }
  for (const e of l) { e.style.setProperty('display', 'none', 'important'); n++; } } return n; };
D.css = txt => { const st = document.createElement('style'); st.textContent = txt; document.documentElement.appendChild(st); };
// cursor: macOS-style arrow, pointing hand on clickables, I-beam on text fields (whatever the page itself asks for)
D.cursorInit = scale => { let c = document.getElementById('__demo_cursor');
  if (!c) { c = document.createElement('div'); c.id = '__demo_cursor'; document.documentElement.appendChild(c); c.attachShadow({mode: 'open'}); }
  c.style.cssText = 'all:initial !important;position:fixed !important;left:0 !important;top:0 !important;width:1px !important;height:1px !important;z-index:2147483647 !important;pointer-events:none !important;display:none !important;margin:0 !important;padding:0 !important;';
  const root = c.shadowRoot;
  const s = scale;
  root.innerHTML = '<style>:host{all:initial}svg{position:absolute;max-width:none;max-height:none;overflow:visible;filter:drop-shadow(0 1px 1.4px rgba(0,0,0,.38))}</style>' +
   '<svg data-k="arrow" width="' + 17 * s + '" height="' + 24 * s + '" viewBox="0 0 17 24" style="position:absolute;left:' + (-1.2 * s) + 'px;top:' + (-1.2 * s) + 'px">' +
   '<path d="M1.2 1.2 L1.2 19 L5.5 14.9 L8.4 21.7 L11.5 20.4 L8.7 13.7 L14.7 13.7 Z" fill="#000" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>' +
   '<svg data-k="hand" width="' + 20 * s + '" height="' + 24 * s + '" viewBox="0 0 20 24" style="position:absolute;left:' + (-6.6 * s) + 'px;top:' + (-1 * s) + 'px;display:none">' +
   '<path d="M6.6 1 C5.6 1 5 1.7 5 2.6 L5 12.2 L4.1 11.2 C3.3 10.4 2.1 10.4 1.5 11.1 C0.9 11.8 1 12.8 1.6 13.5 L5.4 18.6 C6.6 20.4 8.2 22.6 11.2 22.6 L13.4 22.6 C16.2 22.6 18.1 20.4 18.1 17.6 L18.1 11.8 C18.1 10.9 17.4 10.3 16.6 10.3 C15.8 10.3 15.1 10.9 15.1 11.6 L15.1 11 C15.1 10.1 14.4 9.5 13.6 9.5 C12.8 9.5 12.1 10.1 12.1 11 L12.1 10.4 C12.1 9.5 11.4 8.9 10.6 8.9 C9.8 8.9 9.1 9.5 9.1 10.4 L8.2 10.4 L8.2 2.6 C8.2 1.7 7.6 1 6.6 1 Z" fill="#fff" stroke="#000" stroke-width="1.15" stroke-linejoin="round"/>' +
   '<path d="M9.1 10.6 L9.1 15 M12.1 11 L12.1 15 M15.1 11.6 L15.1 15" stroke="#000" stroke-width="1" stroke-linecap="round"/></svg>' +
   '<svg data-k="ibeam" width="' + 9 * s + '" height="' + 18 * s + '" viewBox="0 0 9 18" style="position:absolute;left:' + (-4.5 * s) + 'px;top:' + (-9 * s) + 'px;display:none">' +
   '<path d="M1.3 1.3 C3.3 1.3 4.5 1.9 4.5 3.3 L4.5 14.7 C4.5 16.1 3.3 16.7 1.3 16.7 M7.7 1.3 C5.7 1.3 4.5 1.9 4.5 3.3 M4.5 14.7 C4.5 16.1 5.7 16.7 7.7 16.7 M2.6 9 L6.4 9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' +
   '<path d="M1.3 1.3 C3.3 1.3 4.5 1.9 4.5 3.3 L4.5 14.7 C4.5 16.1 3.3 16.7 1.3 16.7 M7.7 1.3 C5.7 1.3 4.5 1.9 4.5 3.3 M4.5 14.7 C4.5 16.1 5.7 16.7 7.7 16.7 M2.6 9 L6.4 9" fill="none" stroke="#000" stroke-width="1.3" stroke-linecap="round"/></svg>';
  D.cur = c; D.svgs = [...root.querySelectorAll('svg')]; D.scale = scale; return 'ok'; };
D.kindAt = (x, y) => { const el = document.elementFromPoint(x, y); if (!el) return 'arrow';
  const cur = getComputedStyle(el).cursor;
  if (cur === 'pointer') return 'hand';
  if (cur === 'text' || el.isContentEditable || el.matches('textarea,input:not([type=button]):not([type=submit]):not([type=checkbox]):not([type=radio]):not([type=range])')) return 'ibeam';
  return 'arrow'; };
D.cursor = (x, y, press, show) => { if (!document.getElementById('__demo_cursor')) D.cursorInit(D.scale || 1.2);
  const k = D.kindAt(x, y);
  for (const s of D.svgs) s.style.display = s.dataset.k === k ? 'block' : 'none';
  D.cur.style.setProperty('display', show ? 'block' : 'none', 'important');
  D.cur.style.setProperty('transform', 'translate(' + x + 'px,' + y + 'px) scale(' + (1 - 0.14 * press) + ')', 'important');
  D.cur.style.setProperty('transform-origin', '0 0', 'important');
  return k; };
// real click guard: only tabs / accordions / toggles; never a link that navigates, never anything in a form
D.clickOk = (x, y) => { const el = document.elementFromPoint(x, y); if (!el) return 'nothing there';
  if (el.closest('form')) return 'inside a form';
  const a = el.closest('a[href]'); if (a && !a.getAttribute('href').startsWith('#')) return 'link navigates: ' + a.href;
  if (el.closest('[type=submit]')) return 'submit button';
  return ''; };
// <video> plays on the real clock: pause it and step it on ours
D.videoStep = t => { if (!D.vids) { D.vids = [...document.querySelectorAll('video')].map(v => { const base = v.currentTime; try { v.pause(); } catch (e) {} return {v, base}; }); }
  const ps = [];
  for (const o of D.vids) { const v = o.v; if (!v.duration || !isFinite(v.duration)) continue;
    let tt = o.base + t; tt = v.loop ? tt % v.duration : Math.min(tt, v.duration - 0.05);
    if (Math.abs(v.currentTime - tt) < 0.001) continue;
    ps.push(new Promise(res => { const done = () => { v.removeEventListener('seeked', done); res(); }; v.addEventListener('seeked', done); setTimeout(done, 400); v.currentTime = tt; })); }
  return Promise.all(ps).then(() => ps.length); };
return 'ok';
})()
"""

CHAT_HIDE = ["#intercom-container", ".intercom-lightweight-app", ".intercom-launcher", "#hubspot-messages-iframe-container",
             "#drift-widget", "#drift-frame-controller", "#drift-frame-chat", ".crisp-client", "#crisp-chatbox",
             "#fc_frame", ".zsiq_floatmain", "#chatlio-widget", "#qualified-messenger", "iframe[src*='qualified.com']",
             "iframe[title*='chat' i]", "#tidio-chat", "#gorgias-chat-container", "[id^='chat-widget']", ".chat-widget",
             "iframe[src*='web-chat']", "iframe[src*='/chat' i]"]


# ---------------------------------------------------------------- motion
def _min_jerk(s):
    return s * s * s * (10 - 15 * s + 6 * s * s)


EASES = {
    "linear": lambda s: s,
    "inOutSine": lambda s: 0.5 - 0.5 * math.cos(math.pi * s),
    "inOutCubic": lambda s: 4 * s ** 3 if s < 0.5 else 1 - (-2 * s + 2) ** 3 / 2,
    "inOutQuart": lambda s: 8 * s ** 4 if s < 0.5 else 1 - (-2 * s + 2) ** 4 / 2,
    "inOutQuint": lambda s: 16 * s ** 5 if s < 0.5 else 1 - (-2 * s + 2) ** 5 / 2,
    "outCubic": lambda s: 1 - (1 - s) ** 3,
    "outQuart": lambda s: 1 - (1 - s) ** 4,
    "smooth": _min_jerk,          # minimum-jerk: how a hand actually moves a mouse
}


def fps_ratio(fps):
    fps = float(fps)
    if abs(fps - 23.976) < 0.01: return 24000, 1001
    if abs(fps - 29.97) < 0.01: return 30000, 1001
    if abs(fps - 59.94) < 0.01: return 60000, 1001
    return int(round(fps)), 1


class Shot:
    """Turns the JSON keyframes into scroll(t) and cursor(t) once targets are measured on the live page."""

    def __init__(self, cfg, vw, vh):
        self.cfg, self.vw, self.vh = cfg, vw, vh
        self.scroll_k = []      # (t_from, t_to, y_to, ease, y_from)
        self.cursor_k = []
        self.warn = []
        self.start = None

    def build_scroll(self, c, max_y):
        y_prev, t_prev = 0.0, 0.0
        for i, k in enumerate(self.cfg.get("scroll", [])):
            t = float(k["t"])
            if "target" in k:
                r = c.js("__demo.reg(%s,%s,%d)" % (json.dumps("s%d" % i), json.dumps(k["target"]), k.get("nth", 0)))
                if not r:
                    self.warn.append("scroll target not found: %s" % k["target"])
                    y = y_prev
                else:
                    if r["count"] > 1 and "nth" not in k:
                        self.warn.append("scroll target %r matched %d times, used the first" % (k["target"], r["count"]))
                    align = float(k.get("align", 0.42))   # where the target's centre lands: 0 top .. 1 bottom
                    y = r["y"] + r["sy"] + r["h"] / 2 - align * self.vh + float(k.get("dy", 0))
            elif "dy" in k:
                y = y_prev + float(k["dy"])
            elif k.get("y") == "bottom":
                y = max_y
            else:
                y = float(k.get("y", 0))
            y = max(0.0, min(y, max_y))
            t_from = float(k.get("from", t_prev))
            self.scroll_k.append((t_from, t, y, k.get("ease", "inOutCubic"), y_prev))
            y_prev, t_prev = y, t

    def scroll_at(self, t):
        y = 0.0
        for t0, t1, y1, ease, y0 in self.scroll_k:
            if t >= t1:
                y = y1
                continue
            if t > t0:
                s = (t - t0) / max(1e-6, t1 - t0)
                return y0 + (y1 - y0) * EASES.get(ease, EASES["inOutCubic"])(s)
            return y0
        return y

    def peak_speed(self):
        """Fastest scroll in CSS px per second, for the readability warning."""
        best = 0.0
        for t0, t1, y1, ease, y0 in self.scroll_k:
            if t1 > t0:
                for j in range(1, 41):
                    a, b = t0 + (t1 - t0) * (j - 1) / 40, t0 + (t1 - t0) * j / 40
                    best = max(best, abs(self.scroll_at(b) - self.scroll_at(a)) / (b - a))
        return best

    def build_cursor(self, c):
        for i, k in enumerate(self.cfg.get("cursor", [])):
            d = {"t": float(k["t"]), "move": k.get("move"), "arc": float(k.get("arc", 0.07)), "ease": k.get("ease", "smooth")}
            if "target" in k:
                cid = "c%d" % i
                r = c.js("__demo.reg(%s,%s,%d)" % (json.dumps(cid), json.dumps(k["target"]), k.get("nth", 0)))
                if not r:
                    self.warn.append("cursor target not found: %s" % k["target"])
                    continue
                if r["count"] > 1 and "nth" not in k:
                    self.warn.append("cursor target %r matched %d times, used the first" % (k["target"], r["count"]))
                at = k.get("at", [0.5, 0.55])
                d.update(kind="target", id=cid, at=at, dx=float(k.get("dx", 0)), dy=float(k.get("dy", 0)), fixed=r["fixed"],
                         x=r["x"] + at[0] * r["w"] + float(k.get("dx", 0)),
                         docy=r["y"] + (0 if r["fixed"] else r["sy"]) + at[1] * r["h"] + float(k.get("dy", 0)))
            else:
                d.update(kind="pt", x=float(k["x"]) if "x" in k else float(k.get("fx", 0.5)) * self.vw,
                         y=float(k["y"]) if "y" in k else float(k.get("fy", 0.5)) * self.vh)
            self.cursor_k.append(d)
        prev = 0.0
        for d in self.cursor_k:
            d["prev_arrive"] = prev
            prev = d["t"]
        st = self.cfg.get("cursor_start")
        if st:
            self.start = (float(st["x"]) if "x" in st else float(st.get("fx", 0.5)) * self.vw,
                          float(st["y"]) if "y" in st else float(st.get("fy", 0.5)) * self.vh)

    def static_xy(self, d):
        if d["kind"] == "pt":
            return d["x"], d["y"]
        if d["fixed"]:
            return d["x"], d["docy"]
        return d["x"], d["docy"] - self.scroll_at(d["t"])


def press_at(t, clicks):
    p = 0.0
    for ck in clicks:
        dt = t - float(ck["t"])
        if -0.09 <= dt <= 0:
            p = max(p, 1 + dt / 0.09)
        elif 0 < dt <= 0.16:
            p = max(p, 1 - dt / 0.16)
    return p


def frame_state(sh, t, live_rect, landed):
    """Cursor position at t (viewport CSS px). landed[i] = where keyframe i actually ended."""
    ks = sh.cursor_k
    if not ks:
        return sh.start
    pos = sh.start or sh.static_xy(ks[0])
    for i, d in enumerate(ks):
        if d["move"] is not None and i not in landed and t <= max(d["t"] - d["move"], d["prev_arrive"]):
            return pos
        tgt = landed.get(i)
        if tgt is None:
            tgt = live_rect(d) if d["kind"] == "target" else (d["x"], d["y"])
        if d["move"] is None:
            dist = math.hypot(tgt[0] - pos[0], tgt[1] - pos[1])
            d["move"] = max(0.35, min(1.05, 0.3 + dist / 1500.0))
        t_dep = max(d["t"] - d["move"], d["prev_arrive"])
        if t >= d["t"]:
            if i not in landed:
                landed[i] = tgt
            pos = landed[i]
            continue
        if t <= t_dep:
            return pos
        s = (t - t_dep) / max(1e-6, d["t"] - t_dep)
        u = EASES.get(d["ease"], _min_jerk)(s)
        dx, dy = tgt[0] - pos[0], tgt[1] - pos[1]
        dist = math.hypot(dx, dy) or 1.0
        bow = d["arc"] * dist * math.sin(math.pi * u)      # a hand's path bows slightly, always to the same side
        nx, ny = -dy / dist, dx / dist
        if ny < 0:
            nx, ny = -nx, -ny
        return pos[0] + dx * u + nx * bow, pos[1] + dy * u + ny * bow
    return pos


# ---------------------------------------------------------------- page setup
def ua_for(version_json):
    ua = version_json["User-Agent"].replace("HeadlessChrome", "Chrome")
    full = version_json.get("Browser", "Chrome/155.0.0.0").split("/")[-1]
    major = full.split(".")[0]
    meta = {"brands": [{"brand": "Google Chrome", "version": major}, {"brand": "Chromium", "version": major},
                       {"brand": "Not=A?Brand", "version": "24"}],
            "fullVersion": full, "platform": "Windows", "platformVersion": "19.0.0", "architecture": "x86",
            "model": "", "mobile": False, "bitness": "64", "wow64": False}
    return ua, meta


def load(c, url, settle, log):
    c.events.clear()
    t0 = time.time()
    c.call("Page.navigate", {"url": url})
    try:
        c.wait_event("Page.loadEventFired", 45)
    except TimeoutError:
        log.append("load event timed out after 45 s, carried on")
    try:
        c.js("document.fonts.ready.then(()=>1)", await_promise=True, timeout=15)
    except Exception:
        pass
    time.sleep(settle)
    log.append("loaded %s in %.1f s (+%.1f s settle)" % (url, time.time() - t0 - settle, settle))


def prepare(c, cfg, log):
    c.js(PAGE_JS)
    # real clicks that close things a visitor would close first (a docked chat panel's X, a promo modal).
    # Coordinates in viewport CSS px; never a link, never anything inside a form.
    for pc in cfg.get("pre_click", []):
        why = c.js("__demo.clickOk(%.1f,%.1f)" % (pc["x"], pc["y"]))
        if why:
            log.append("pre_click at %s refused: %s" % ((pc["x"], pc["y"]), why))
            continue
        for typ in ("mouseMoved", "mousePressed", "mouseReleased"):
            c.call("Input.dispatchMouseEvent", {"type": typ, "x": pc["x"], "y": pc["y"], "button": "left", "clickCount": 1})
        log.append("pre_click at (%.0f, %.0f)%s" % (pc["x"], pc["y"], " - " + pc["why"] if pc.get("why") else ""))
        time.sleep(float(pc.get("wait", 1.5)))
    if cfg.get("consent", "reject") != "none":
        r = c.js("__demo.consent(%s)" % json.dumps(cfg.get("consent", "reject")))
        if r:
            log.append("consent: " + "; ".join(r))
            time.sleep(0.8)
            r2 = c.js("__demo.consent('hide')")
            if r2:
                log.append("consent: " + "; ".join(r2))
    hide = list(cfg.get("hide", []))
    if cfg.get("hide_chat", True):
        hide += CHAT_HIDE
    n = c.js("__demo.hide(%s)" % json.dumps(hide))
    if n:
        log.append("hid %d chat/extra elements" % n)
    if cfg.get("css"):
        c.js("__demo.css(%s)" % json.dumps(cfg["css"]))
    # native lazy images / iframes load now on the real clock, not mid-take
    n = c.js("(()=>{let n=0;for(const e of document.querySelectorAll('[loading=lazy]')){e.loading='eager';n++}return n})()")
    if n:
        log.append("made %d lazy images/iframes load now" % n)


def open_page(cfg, vw, vh, dpr, log):
    ver = start_chrome()
    info, c = new_tab()
    ua, meta = ua_for(ver)
    c.call("Page.enable")
    c.call("Page.addScriptToEvaluateOnNewDocument", {"source": CLOCK_JS})
    c.call("Emulation.setUserAgentOverride", {"userAgent": ua, "acceptLanguage": "en-US,en;q=0.9",
                                              "platform": "Win32", "userAgentMetadata": meta})
    c.call("Emulation.setDeviceMetricsOverride", {"width": vw, "height": vh, "deviceScaleFactor": dpr,
                                                  "mobile": False, "screenWidth": vw, "screenHeight": vh})
    c.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
    settle = float(cfg.get("settle", 4))
    load(c, cfg["url"], settle, log)
    prepare(c, cfg, log)
    if cfg.get("prewarm", True):
        # scroll the whole page once so lazy images / fonts / videos are cached, then reload clean,
        # so scroll-triggered reveals still play live in the take
        h = c.js("__demo.maxY()") or 0
        y = 0
        while y <= min(h, float(cfg.get("prewarm_max", 26000))):
            c.js("__demo.scroll(%d)" % y)
            time.sleep(0.2)
            y += int(vh * 0.7)
        c.js("__demo.scroll(0)")
        time.sleep(0.4)
        load(c, cfg["url"], settle, log)
        prepare(c, cfg, log)
    return info, c


# ---------------------------------------------------------------- record
def record(cfg, out_dir, width=None, still=None, keep=False, tag=None):
    os.makedirs(out_dir, exist_ok=True)
    out_w, out_h = cfg.get("out", [1920, 1080])
    vw = int(width or cfg.get("viewport_width", 1536))
    vh = int(round(vw * out_h / out_w))
    dpr = out_w / vw
    num, den = fps_ratio(cfg.get("fps", 23.976))
    fps = num / den
    n = int(round(float(cfg["duration"]) * fps))
    name = tag or cfg["name"]
    log = ["viewport %dx%d CSS px at DPR %.4f -> %dx%d, %d frames at %d/%d" % (vw, vh, dpr, out_w, out_h, n, num, den)]
    t_start = time.time()
    info, c = open_page(cfg, vw, vh, dpr, log)
    try:
        max_y = c.js("__demo.maxY()") or 0
        sh = Shot(cfg, vw, vh)
        c.js("__demo.scroll(0)")
        time.sleep(0.3)
        sh.build_scroll(c, max_y)
        sh.build_cursor(c)
        pk = sh.peak_speed()
        log.append("page height %d px; peak scroll %.0f CSS px/s" % (max_y + vh, pk))
        if pk > 1600:
            sh.warn.append("peak scroll %.0f px/s is fast to read; give that scroll more time" % pk)
        show_cursor = cfg.get("cursor_visible", True) and bool(sh.cursor_k or sh.start)
        c.js("__demo.cursorInit(%s)" % float(cfg.get("cursor_scale", 1.2)))
        clicks = cfg.get("clicks", [])
        landed = {}

        def live_rect(d):
            r = c.js("__demo.rect(%s)" % json.dumps(d["id"]))
            if not r:
                return sh.static_xy(d)
            x = r["x"] + d["at"][0] * r["w"] + d["dx"]
            y = r["y"] + d["at"][1] * r["h"] + d["dy"]
            if not r["fixed"]:
                y += r["sy"] - sh.scroll_at(d["t"])   # where it will be when the cursor arrives
            return x, y

        def apply(t):
            c.js("__demo.scroll(%.2f)" % sh.scroll_at(t))
            xy = frame_state(sh, t, live_rect, landed) if show_cursor else None
            if xy:
                c.call("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": xy[0], "y": xy[1]})
                c.js("__demo.cursor(%.2f,%.2f,%.3f,true)" % (xy[0], xy[1], press_at(t, clicks)))
            for ck in clicks:
                if ck.get("real") and xy and abs(t - float(ck["t"])) < 0.5 / fps:
                    why = c.js("__demo.clickOk(%.1f,%.1f)" % xy)
                    if why:
                        sh.warn.append("real click at %.2f s refused: %s (shown as a press only)" % (t, why))
                    else:
                        for typ in ("mousePressed", "mouseReleased"):
                            c.call("Input.dispatchMouseEvent", {"type": typ, "x": xy[0], "y": xy[1], "button": "left", "clickCount": 1})

        def grab(fmt="jpeg"):
            p = {"format": fmt}
            if fmt == "jpeg":
                p["quality"] = 96
            for attempt in range(3):
                r = c.wait(c.send("Page.captureScreenshot", p), 20)
                if r is not None:
                    return base64.b64decode(r["data"])
            raise TimeoutError("screenshot never came back")

        if still is not None:
            t = float(still)
            # walk the cursor history up to t so it lands where the take would have it
            for j in range(0, int(t * fps) + 1, max(1, int(fps / 8))):
                c.js("__demo.scroll(%.2f)" % sh.scroll_at(j / fps))
                if show_cursor:
                    frame_state(sh, j / fps, live_rect, landed)
            apply(t)
            time.sleep(1.2)
            apply(t)
            time.sleep(0.4)
            p = os.path.join(out_dir, name + ".png")
            open(p, "wb").write(grab("png"))
            print("\n".join(log + ["WARN " + w for w in sh.warn] + ["-> " + p]))
            return p

        # starting state on the real clock, so hovers and reveals at frame 0 are settled; then freeze
        apply(0)
        time.sleep(0.9)
        fdir = os.path.join(os.environ.get("TEMP", out_dir), "demo_frames_" + name)
        shutil.rmtree(fdir, ignore_errors=True)
        os.makedirs(fdir)
        step = 1000.0 * den / num
        c.js("__vt.freeze()")
        t_cap = time.time()
        stepped = 0
        prof = {"apply": 0.0, "clock": 0.0, "video": 0.0, "shot": 0.0}
        for i in range(n):
            t = i / fps
            a0 = time.time()
            apply(t)
            a1 = time.time()
            stepped = max(stepped, c.js("__vt.advance(%.6f)" % (step if i else 0)) or 0)
            a2 = time.time()
            if cfg.get("video_sync", True):
                c.js("__demo.videoStep(%.4f)" % t, await_promise=True)
            a3 = time.time()
            open(os.path.join(fdir, "f%05d.jpg" % i), "wb").write(grab())
            a4 = time.time()
            for k_, v_ in zip(prof, (a1 - a0, a2 - a1, a3 - a2, a4 - a3)):
                prof[k_] += v_
            if i and i % 72 == 0:
                print("  %s: %d/%d frames (%.0f s)" % (name, i, n, time.time() - t_cap), flush=True)
        log.append("captured %d frames in %.1f s; %d page animations stepped on the take clock" % (n, time.time() - t_cap, stepped))
        log.append("per frame: " + ", ".join("%s %.0f ms" % (k_, 1000 * v_ / max(1, n)) for k_, v_ in prof.items()))
        sched = {"scroll": [{"from": a, "to": b, "y": round(y, 1)} for a, b, y, e, y0 in sh.scroll_k],
                 "cursor": [{"t": d["t"], "move": round(d["move"] or 0, 2),
                             "landed": [round(v, 1) for v in landed.get(i, sh.static_xy(d))]} for i, d in enumerate(sh.cursor_k)]}
    finally:
        close_tab(info)
    mp4 = os.path.join(out_dir, name + ".mp4")
    cmd = [FFMPEG, "-v", "error", "-y", "-framerate", "%d/%d" % (num, den), "-i", os.path.join(fdir, "f%05d.jpg"),
           "-vf", "scale=in_color_matrix=bt601:in_range=full:out_color_matrix=bt709:out_range=tv:flags=lanczos,format=yuv420p",
           "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", mp4]
    subprocess.run(cmd, check=True)
    sheet = contact_sheet(fdir, n, fps, os.path.join(out_dir, name + "_sheet.jpg"))
    if not keep:
        shutil.rmtree(fdir, ignore_errors=True)
    log.append("total %.1f s" % (time.time() - t_start))
    meta = {"shot": cfg, "viewport": [vw, vh], "dpr": dpr, "out": [out_w, out_h], "fps": "%d/%d" % (num, den),
            "frames": n, "schedule": sched, "warnings": sh.warn, "log": log, "mp4": mp4, "sheet": sheet,
            "recorded": time.strftime("%Y-%m-%d %H:%M")}
    with open(os.path.join(out_dir, name + ".log.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    print("\n".join(log + ["WARN " + w for w in sh.warn] + ["-> " + mp4]))
    return mp4


def contact_sheet(fdir, n, fps, path, cols=4, rows=2):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    k = cols * rows
    idx = [int(round(i * (n - 1) / (k - 1))) for i in range(k)]
    tw, th = 480, 270
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 8, rows * (th + 26) + 8), (24, 24, 24))
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(sheet)
    for j, i in enumerate(idx):
        im = Image.open(os.path.join(fdir, "f%05d.jpg" % i)).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = 8 + (j % cols) * (tw + 8), 8 + (j // cols) * (th + 26)
        sheet.paste(im, (x, y))
        d.text((x, y + th + 3), "f%d  %.2f s" % (i, i / fps), fill=(220, 220, 220), font=font)
    sheet.save(path, quality=90)
    return path


def compare(cfg, out_dir, widths, at):
    from PIL import Image, ImageDraw, ImageFont
    stills = [(w, record(cfg, out_dir, width=w, still=at, tag="%s_zoom_%d" % (cfg["name"], w))) for w in widths]
    out_w, out_h = cfg.get("out", [1920, 1080])
    tw, th = 960, int(960 * out_h / out_w)
    pad, lab = 16, 46
    img = Image.new("RGB", (len(stills) * tw + (len(stills) + 1) * pad, th + lab + 2 * pad), (20, 20, 20))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
    except Exception:
        font = ImageFont.load_default()
    for j, (w, p) in enumerate(stills):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        x = pad + j * (tw + pad)
        img.paste(im, (x, pad + lab))
        d.text((x, pad + 6), "%d CSS px wide  (page zoom %d%%)" % (w, round(100 * out_w / w)), fill=(240, 240, 240), font=font)
    path = os.path.join(out_dir, "%s_zoom_compare.jpg" % cfg["name"])
    img.save(path, quality=92)
    print("-> " + path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shot")
    ap.add_argument("--out", default=None, help="output folder (default: next to the shot file)")
    ap.add_argument("--width", type=int, default=None, help="override viewport_width (CSS px)")
    ap.add_argument("--still", type=float, default=None, help="one PNG of the moment at this time (s)")
    ap.add_argument("--compare", default=None, help="comma list of viewport widths for a zoom comparison")
    ap.add_argument("--at", type=float, default=None, help="time (s) of the --compare moment")
    ap.add_argument("--keep-frames", action="store_true")
    ap.add_argument("--port", type=int, default=PORT, help="DevTools port; give each parallel job its own (9361, 9362, ...)")
    a = ap.parse_args()
    globals()["PORT"] = a.port
    with open(a.shot, encoding="utf-8") as f:
        cfg = json.load(f)
    out = a.out or os.path.dirname(os.path.abspath(a.shot))
    if a.compare:
        compare(cfg, out, [int(x) for x in a.compare.split(",")], a.at if a.at is not None else float(cfg["duration"]) / 2)
    else:
        record(cfg, out, width=a.width, still=a.still, keep=a.keep_frames)


if __name__ == "__main__":
    main()
