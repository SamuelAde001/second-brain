"""Restart DaVinci Resolve when it is hung or has crashed. Touches Resolve.exe only.

Samuel, 2026-10-13: "Yes, you have full permission to always start resolve".
Default: start Resolve if it isn't running; kill and relaunch it only if Windows
reports it Not Responding. --force kills and relaunches even when it responds
(memory leak between render batches). Unsaved changes in a killed Resolve are lost,
so save the project by script first whenever Resolve still answers.

    python 03-Areas/video-editing/scripts/restart_resolve.py [--force] [--status]
"""
import subprocess, sys, time

EXE = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"


def tasks(extra=()):
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe", *extra, "/FO", "CSV", "/NH"],
                         capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l.startswith('"Resolve.exe"')]


def state():
    if not tasks():
        return "not running"
    if tasks(("/FI", "STATUS eq NOT RESPONDING")):
        return "not responding"
    return "running"


def main():
    force = "--force" in sys.argv
    s = state()
    if "--status" in sys.argv:
        print(f"Resolve: {s}")
        return
    if s == "running" and not force:
        print("Resolve: running and responding, left alone (use --force to restart anyway)")
        return
    if s != "not running":
        subprocess.run(["taskkill", "/IM", "Resolve.exe", "/F"], capture_output=True)
        for _ in range(60):
            if not tasks():
                break
            time.sleep(1)
        else:
            print("Resolve: still running 60 s after taskkill, not relaunched")
            sys.exit(1)
        time.sleep(3)
    subprocess.Popen([EXE], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                     close_fds=True)
    for _ in range(120):
        if tasks():
            print(f"Resolve: was {s}, relaunched. Wait for the project manager, then GotoRootFolder before LoadProject.")
            return
        time.sleep(1)
    print("Resolve: launched but no process after 120 s")
    sys.exit(1)


if __name__ == "__main__":
    main()
