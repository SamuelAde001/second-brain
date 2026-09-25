"""Render Route Rise #3 visual scenes (HTML) to frame-exact video.

python render.py B01 B02 ...   render those beats
python render.py all           render every visual beat
python render.py B01 --still   one mid still only (fast check)

Overlays -> ProRes 4444 .mov with alpha. Full frame -> H.264 .mp4 (review quality).
Stdlib only + ffmpeg. Chrome headless over the DevTools protocol.
"""
import os, sys, json, time, base64, socket, struct, subprocess, urllib.request, shutil, glob, threading
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as BT

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FFMPEG = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe"))[0]
PORT = 9341
FPS = BT.FPS
OUT = os.path.join(HERE, "renders")
STILLS = os.path.join(HERE, "stills")
TMP = os.path.join(os.environ["TEMP"], "rr3_frames")


class WS:
    def __init__(self, url):
        hostport, path = url[5:].split("/", 1)
        host, port = hostport.split(":")
        self.s = socket.create_connection((host, int(port)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(("GET /%s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        "Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n" % (path, hostport, key)).encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.id = 0

    def _recvn(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(max(1 << 20, n - len(self.buf)))
            if not chunk:
                raise IOError("closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, text):
        data = text.encode()
        hdr = bytearray([0x81])
        n = len(data)
        if n < 126: hdr.append(0x80 | n)
        elif n < 65536: hdr.append(0x80 | 126); hdr += struct.pack(">H", n)
        else: hdr.append(0x80 | 127); hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        self.s.sendall(bytes(hdr) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        msg = b""
        while True:
            b1, b2 = self._recvn(2)
            op = b1 & 0x0F
            n = b2 & 0x7F
            if n == 126: n = struct.unpack(">H", self._recvn(2))[0]
            elif n == 127: n = struct.unpack(">Q", self._recvn(8))[0]
            payload = self._recvn(n)
            if op == 9:
                continue
            msg += payload
            if b1 & 0x80:
                return msg.decode("utf-8", "ignore")

    def call(self, method, params=None, timeout=120):
        self.id += 1
        mid = self.id
        self.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        t0 = time.time()
        while time.time() - t0 < timeout:
            m = json.loads(self.recv())
            if m.get("id") == mid:
                if "error" in m:
                    raise RuntimeError("%s: %s" % (method, m["error"]))
                return m.get("result", {})
        raise TimeoutError(method)


def ensure_chrome():
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/json/version" % PORT, timeout=1).read()
        return
    except Exception:
        pass
    ud = os.path.join(os.environ["TEMP"], "rr3_chrome_%d" % PORT)
    subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT, "--user-data-dir=" + ud,
                      "--window-size=1920,1080", "--hide-scrollbars", "--force-color-profile=srgb",
                      "--allow-file-access-from-files", "--remote-allow-origins=*", "--mute-audio",
                      "--disable-background-timer-throttling", "--disable-renderer-backgrounding", "about:blank"],
                     creationflags=0x8 | 0x200, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        time.sleep(0.25)
        try:
            urllib.request.urlopen("http://127.0.0.1:%d/json/version" % PORT, timeout=1).read()
            return
        except Exception:
            pass
    raise RuntimeError("chrome did not start")


def open_tab():
    info = json.loads(urllib.request.urlopen(urllib.request.Request(
        "http://127.0.0.1:%d/json/new?about:blank" % PORT, method="PUT"), timeout=10).read())
    return info, WS(info["webSocketDebuggerUrl"])


def close_tab(info):
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/json/close/%s" % (PORT, info["id"]), timeout=5)
    except Exception:
        pass


def scene_url(b):
    path = os.path.join(HERE, "scenes", b["scene"] + ".html").replace("\\", "/")
    dur = (b["end"] - b["start"]) / FPS
    return "file:///%s?start=%d&dur=%.4f&id=%s" % (path, b["start"], dur, b["id"])


def render_beat(b, still_only=False):
    alpha = b.get("layer") == "overlay"
    n = b["end"] - b["start"]
    info, ws = open_tab()
    try:
        ws.call("Page.enable")
        ws.call("Emulation.setDeviceMetricsOverride", {"width": 1920, "height": 1080, "deviceScaleFactor": 1, "mobile": False})
        if alpha:
            ws.call("Emulation.setDefaultBackgroundColorOverride", {"color": {"r": 0, "g": 0, "b": 0, "a": 0}})
        ws.call("Page.navigate", {"url": scene_url(b)})
        for _ in range(100):
            time.sleep(0.1)
            r = ws.call("Runtime.evaluate", {"expression": "typeof READY==='function'", "returnByValue": True})
            if r.get("result", {}).get("value"):
                break
        r = ws.call("Runtime.evaluate", {"expression": "READY()", "awaitPromise": True, "returnByValue": True})
        if r.get("exceptionDetails"):
            raise RuntimeError("READY failed: " + json.dumps(r["exceptionDetails"])[:400])
        err = ws.call("Runtime.evaluate", {"expression": "window.__err||''", "returnByValue": True}).get("result", {}).get("value")
        if err:
            raise RuntimeError("scene error: " + err)
        fmt = "png" if alpha else "jpeg"
        frames = [int(n * 0.8)] if still_only else range(n)
        fdir = os.path.join(TMP, b["id"])
        if not still_only:
            shutil.rmtree(fdir, ignore_errors=True)
            os.makedirs(fdir)
        for i in frames:
            rr = ws.call("Runtime.evaluate", {"expression": "R(%.6f)" % (i / FPS), "awaitPromise": True})
            if rr.get("exceptionDetails"):
                raise RuntimeError("R() failed: " + json.dumps(rr["exceptionDetails"])[:400])
            p = {"format": fmt, "captureBeyondViewport": False}
            if fmt == "jpeg":
                p["quality"] = 94
            data = base64.b64decode(ws.call("Page.captureScreenshot", p)["data"])
            if still_only:
                os.makedirs(STILLS, exist_ok=True)
                sp = os.path.join(STILLS, "%s_%s.%s" % (b["id"], b["scene"], "png" if alpha else "jpg"))
                open(sp, "wb").write(data)
                return sp
            open(os.path.join(fdir, "f%05d.%s" % (i, "png" if alpha else "jpg")), "wb").write(data)
    finally:
        close_tab(info)
    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, b["id"] + "_*")):
        os.remove(old)
    name = "%s_%s" % (b["id"], b["scene"])
    src = os.path.join(fdir, "f%05d." + ("png" if alpha else "jpg"))
    if alpha:
        dst = os.path.join(OUT, name + ".mov")
        cmd = [FFMPEG, "-v", "error", "-y", "-framerate", "24000/1001", "-i", src,
               "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0", dst]
    else:
        dst = os.path.join(OUT, name + ".mp4")
        cmd = [FFMPEG, "-v", "error", "-y", "-framerate", "24000/1001", "-i", src,
               "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst]
    subprocess.run(cmd, check=True)
    # mid still for the sheet
    mid = os.path.join(fdir, "f%05d.%s" % (n // 2, "png" if alpha else "jpg"))
    os.makedirs(STILLS, exist_ok=True)
    shutil.copy(mid, os.path.join(STILLS, "%s_%s.%s" % (b["id"], b["scene"], "png" if alpha else "jpg")))
    shutil.rmtree(fdir, ignore_errors=True)
    return dst


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    still = "--still" in sys.argv
    todo = [b for b in BT.B if b["kind"] == "visual" and b.get("scene")]
    if args and args != ["all"]:
        todo = [b for b in todo if b["id"] in args or b["scene"] in args]
    ready = [b for b in todo if os.path.exists(os.path.join(HERE, "scenes", b["scene"] + ".html"))]
    missing = [b["id"] for b in todo if b not in ready]
    if missing:
        print("no scene yet:", " ".join(missing))
    ensure_chrome()
    t0 = time.time()
    lock = threading.Lock()

    def job(b):
        s = time.time()
        try:
            out = render_beat(b, still)
            with lock:
                print("%s ok %.1fs %s" % (b["id"], time.time() - s, os.path.basename(out)), flush=True)
        except Exception as e:
            with lock:
                print("%s FAILED %s" % (b["id"], e), flush=True)

    with ThreadPoolExecutor(max_workers=1 if still else 3) as ex:
        list(ex.map(job, ready))
    print("done %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
