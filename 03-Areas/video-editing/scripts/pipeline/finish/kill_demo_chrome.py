# Stop the headless Chrome that record_demo.py leaves running on a DevTools port (or list which ports are still running).
# usage: python kill_demo_chrome.py <port> | --list      (--list, or no argument: prints "port: process count", stops nothing)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# Only touches processes whose command line holds "demo_rec_chrome_<port>" (record_demo.py's throwaway profile).
import argparse, subprocess, sys, re, collections

ap = argparse.ArgumentParser(description="Stop the headless Chrome that record_demo.py leaves on a DevTools port.")
ap.add_argument("port", nargs="?", help="DevTools port whose Chrome to stop")
ap.add_argument("--list", action="store_true", help="print port: process count for every leftover Chrome; stop nothing")
args = ap.parse_args()

PS = ("Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'demo_rec_chrome_' } | "
      "ForEach-Object { '' + $_.ProcessId + ' ' + $_.CommandLine }")
rows = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True).stdout.splitlines()
procs = []
for r in rows:
    m = re.match(r"(\d+) .*demo_rec_chrome_(\d+)", r)
    if m:
        procs.append((int(m.group(1)), m.group(2)))
if args.list or not args.port:
    for port, n in sorted(collections.Counter(p for _, p in procs).items()):
        print("%s: %d" % (port, n))
    sys.exit(0)
port = args.port
pids = [pid for pid, p in procs if p == port]
for pid in pids:
    subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
print("port %s: stopped %d processes" % (port, len(pids)))
