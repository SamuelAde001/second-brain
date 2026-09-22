#!/usr/bin/env python3
"""Pace numbers for finishing a video edit by a deadline, in WAT (UTC+1).

Usage:
  python3 pace.py --length 33:46 --pos 10:53 --end 19:00 [--now 14:48]

--length and --pos are timeline times: MM:SS or H:MM:SS.
--end and --now are 24-hour WAT clock times: HH:MM.
--now defaults to the current WAT time. A deadline earlier than now
is treated as tomorrow (past-midnight finishes).
"""
import argparse
import sys
from datetime import datetime, timedelta, timezone

WAT = timezone(timedelta(hours=1))


def parse_dur(s):
    parts = s.strip().split(":")
    if not 2 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"'{s}' should look like 33:46 or 1:12:00")
    nums = [int(p) for p in parts]
    if any(n > 59 for n in nums[1:]):
        raise ValueError(f"'{s}' has minutes or seconds above 59")
    if len(nums) == 2:
        return nums[0] * 60 + nums[1]
    return nums[0] * 3600 + nums[1] * 60 + nums[2]


def parse_clock(s):
    parts = s.strip().split(":")
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise ValueError(f"'{s}' should look like 19:00")
    h, m = int(parts[0]), int(parts[1])
    if h > 23 or m > 59:
        raise ValueError(f"'{s}' is not a valid 24-hour time")
    return h, m


def fmt(sec):
    sec = max(0, round(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def fmt_span(sec):
    sec = max(0, round(sec))
    h, rem = divmod(sec, 3600)
    return f"{h}h {rem // 60:02d}m"


def main():
    ap = argparse.ArgumentParser(description="Edit pace in WAT")
    ap.add_argument("--length", required=True, help="full video length, e.g. 33:46")
    ap.add_argument("--pos", required=True, help="current playhead, e.g. 10:53")
    ap.add_argument("--end", required=True, help="finish-by WAT time, e.g. 19:00")
    ap.add_argument("--now", help="current WAT time if stated, e.g. 14:48")
    a = ap.parse_args()

    try:
        length = parse_dur(a.length)
        pos = parse_dur(a.pos)
        eh, em = parse_clock(a.end)
        real_now = datetime.now(WAT).replace(microsecond=0)
        if a.now:
            nh, nm = parse_clock(a.now)
            now = real_now.replace(hour=nh, minute=nm, second=0)
        else:
            now = real_now
    except ValueError as e:
        sys.exit(f"Error: {e}")

    if pos >= length:
        sys.exit("Error: the playhead is already at or past the end of the video.")

    end = now.replace(hour=eh, minute=em, second=0)
    if end <= now:
        end += timedelta(days=1)
    left = (end - now).total_seconds()
    if left < 60:
        sys.exit("Error: the deadline is less than a minute away.")

    remaining = length - pos
    rate = remaining / (left / 3600)

    tomorrow = " (tomorrow)" if end.date() != now.date() else ""
    print(f"Now {now:%H:%M} WAT, finish by {end:%H:%M} WAT{tomorrow}")
    print(f"Timeline left: {fmt(remaining)} (from {fmt(pos)} to {fmt(length)})")
    print(f"Time left: {fmt_span(left)}")
    print(f"Pace: {fmt(rate)} of timeline per hour")
    print()

    # On-the-hour checkpoints when there's room, 15-minute ones when it's tight.
    step = 60 if left >= 2 * 3600 else 15
    midnight = now.replace(hour=0, minute=0, second=0)
    minutes_now = now.hour * 60 + now.minute
    cp = midnight + timedelta(minutes=(minutes_now // step + 1) * step)

    print("Checkpoints (WAT time, playhead should be at):")
    while cp < end:
        at = pos + remaining * ((cp - now).total_seconds() / left)
        day = " +1d" if cp.date() != now.date() else ""
        print(f"  {cp:%H:%M}{day}  {fmt(at)}")
        cp += timedelta(minutes=step)
    day = " +1d" if end.date() != now.date() else ""
    print(f"  {end:%H:%M}{day}  {fmt(length)}  done")


if __name__ == "__main__":
    main()
