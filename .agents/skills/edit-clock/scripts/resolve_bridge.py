"""Live mode for the edit clock: reads the playhead from DaVinci Resolve.

Serves the clock at http://127.0.0.1:8765/ and the current timeline state at /status.
Read-only: it only asks Resolve for the current timeline, its length and the playhead.

    python 00-System/skills/edit-clock/scripts/resolve_bridge.py [--port 8765]

Needs Resolve open with Preferences > System > General > External scripting = Local.
Stop it with Ctrl+C or by closing its window.
"""
import argparse
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CLOCK = os.path.join(HERE, "..", "assets", "edit-clock.html")

_resolve = None


def tc_to_frames(tc, base):
    h, m, s, f = (int(x) for x in tc.replace(";", ":").split(":"))
    return ((h * 60 + m) * 60 + s) * base + f


def status():
    global _resolve
    if _resolve is None:
        _resolve = dvr.scriptapp("Resolve")
    if _resolve is None:
        return {"ok": False, "error": "Resolve not reachable (is it open, with external scripting on Local?)"}
    try:
        project = _resolve.GetProjectManager().GetCurrentProject()
        tl = project.GetCurrentTimeline() if project else None
    except Exception:
        _resolve = None
        return {"ok": False, "error": "Lost Resolve, retrying"}
    if not tl:
        return {"ok": False, "error": "No timeline open"}
    fps = float(tl.GetSetting("timelineFrameRate"))
    base = round(fps)
    start = tl.GetStartFrame()
    head = tc_to_frames(tl.GetCurrentTimecode(), base) - tc_to_frames(tl.GetStartTimecode(), base)
    return {
        "ok": True,
        "project": project.GetName(),
        "timeline": tl.GetName(),
        "fps": fps,
        "length": (tl.GetEndFrame() - start) / fps,
        "playhead": max(0, head) / fps,
        "page": _resolve.GetCurrentPage(),
        "ts": time.time(),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/status"):
            try:
                data = status()
            except Exception as e:  # never kill the server over one bad read
                data = {"ok": False, "error": str(e)}
            self._send(200, json.dumps(data).encode(), "application/json")
        elif self.path in ("/", "/index.html", "/edit-clock.html"):
            with open(CLOCK, "rb") as fh:
                self._send(200, fh.read(), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")

    def log_message(self, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    print(json.dumps(status()))
    print(f"Edit clock live at http://127.0.0.1:{a.port}/")
    HTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
