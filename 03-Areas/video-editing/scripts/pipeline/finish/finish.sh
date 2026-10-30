#!/bin/bash
# One finish chain for a round of changed beats: stop the render queue -> install changed beats onto a copy of Samuel's timeline -> snapshot check -> A1 voice keep -> chunked render -> master -> phone parts.
# usage: bash finish.sh --job <job folder> --project "<project name start>" --base "<Samuel's timeline>" --new "<new timeline>" --beats A,B,C --res 1080|4k --snapshot <base tl_snapshot.json> --cut "<cut timeline>" [--ver v3] [--kits <kits dir>] [--out <dir>] [--parts "0-3055,3055-6060,..."] [--replace] [--from-render] [--dry-run]
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# Needs Resolve running. Steps: 0 stop queue, 1 install changed beats (install_changed.py), 2 snapshot + compare with --base (tl_snapshot.py, tl_diff.py, audio identical, video changes only at the beats),
# 3 A1 Voice Isolation = --cut's (a1_voice.py --keep), 4 chunked render (kit build_v1.sh), 5 master (master.py), 6 phone parts. --from-render skips 1-3 (render again from the timeline as it is).
# --replace: the new timeline exists (rebuild mine; the old one is renamed zz ... old). RERENDER="4040 8080" in the environment is passed to build_v1.sh. Log: <out>/finish_<ver>.log
# Not in this chain (video 4's one-offs): sfx_fix_v3.py, the v3c patch render + splice. Default render step: render_chunks.sh beside this script; master: ..\audio\master.py. --build / --master override them.
HERE="$(cd "$(dirname "$0")" && pwd)"
PIPE="$HERE/.."
w() { cygpath -w "$1"; }
usage() { sed -n '2,3p' "$0" | cut -c3-; exit 2; }
JOB=""; KITS=""; PROJECT=""; BASE=""; NEW=""; BEATS=""; RES=""; VER=""; SNAP=""; CUT=""; OUT=""; PARTS=""; LEN=""; BUILD=""; MASTER=""; REPLACE=""; FROM=""; DRY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --replace) REPLACE="--replace"; shift; continue;;
    --from-render) FROM="--from-render"; shift; continue;;
    --dry-run) DRY=1; shift; continue;;
    -h|--help) usage;;
  esac
  [ $# -ge 2 ] || { echo "$1 needs a value" >&2; usage; }
  case "$1" in
    --job) JOB="$2";; --kits) KITS="$2";; --project) PROJECT="$2";; --base) BASE="$2";; --new) NEW="$2";;
    --beats) BEATS="$2";; --res) RES="$2";; --ver) VER="$2";; --snapshot) SNAP="$2";; --cut) CUT="$2";;
    --out) OUT="$2";; --parts) PARTS="$2";; --len) LEN="$2";; --build) BUILD="$2";; --master) MASTER="$2";;
    *) echo "unknown argument: $1" >&2; usage;;
  esac
  shift 2
done
for v in JOB BASE NEW BEATS RES; do [ -n "${!v}" ] || { echo "missing --$(echo $v | tr 'A-Z' 'a-z')" >&2; usage; }; done
case "$RES" in 1080|4k) ;; *) echo "--res must be 1080 or 4k" >&2; usage;; esac
if [ "$FROM" != "--from-render" ]; then
  [ -n "$SNAP" ] || { echo "missing --snapshot (or use --from-render)" >&2; usage; }
  [ -n "$CUT" ] || { echo "missing --cut (or use --from-render)" >&2; usage; }
fi
JOB="$(cygpath -u "$JOB")"; JOB="${JOB%/}"
[ -n "$KITS" ] && KITS="$(cygpath -u "$KITS")" || KITS="$JOB/Graphics/Frontal kit (Editor)/kits"
KIT="$(dirname "$KITS")"
[ -n "$OUT" ] && OUT="$(cygpath -u "$OUT")" || OUT="$JOB/Docs/finish"
[ -n "$SNAP" ] && SNAP="$(cygpath -u "$SNAP")"
[ -n "$VER" ] || VER="$(echo "$NEW" | grep -oiE 'v[0-9]+[a-z0-9]*' | head -1)"
[ -n "$VER" ] || { echo "cannot read a version tag from --new; pass --ver" >&2; usage; }
[ -n "$BUILD" ] || BUILD="$HERE/render_chunks.sh"
[ -n "$MASTER" ] || MASTER="$HERE/../audio/master.py"
LABEL="$(basename "$JOB" | sed -nE 's/^([0-9]+)\..*/v\1/p')"; [ -n "$LABEL" ] || LABEL="video"
SLUG="$(python -c "import re,sys; print(re.sub(r'[^\w]+', '_', sys.argv[1]).strip('_'))" "$NEW")"
INSTNEW="$KIT/renders/v2/INST/$SLUG"
SPANS="$OUT/${VER}_seed_spans.json"
NEWSNAP="$OUT/tl_${VER}_$(date +%F).json"
LOG="$OUT/finish_$VER.log"
if [ "$RES" = "1080" ]; then R="$JOB/Renders/$VER 1080p (Editor)"; NAME="${VER}_1080"; else R="$JOB/Renders/$VER 4K (Editor)"; NAME="${VER}_4k"; fi
if [ -z "$PARTS" ]; then   # default: four equal parts of the timeline
  [ -z "$LEN" ] && [ -n "$SNAP" ] && LEN="$(python -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); print(d['end']-d['start'])" "$(w "$SNAP")")"
  [ -n "$LEN" ] && PARTS="$(python -c "n=int(__import__('sys').argv[1]); print(','.join('%d-%d' % (i*n//4, (i+1)*n//4) for i in range(4)))" "$LEN")"
fi
if [ -n "$DRY" ]; then
  echo "job=$JOB"; echo "kits=$KITS"; echo "out=$OUT"; echo "project=$PROJECT"; echo "base=$BASE"; echo "new=$NEW ($SLUG)"; echo "beats=$BEATS"
  echo "res=$RES ver=$VER from=${FROM:-no} replace=${REPLACE:-no}"; echo "render=$R/$NAME.mp4"; echo "build=$BUILD"; echo "master=$MASTER"
  echo "parts=${PARTS:-none (give --parts or --len)} label=$LABEL"; echo "log=$LOG"; exit 0
fi
mkdir -p "$OUT"
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
cd "$OUT" || exit 1
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*render_queue.py run*' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force; 'queue stopped ' + \$_.ProcessId }" >> "$LOG" 2>&1
for i in $(seq 1 24); do   # queue.alive goes stale within 60 s of the kill (render_queue.py ALIVE_S)
  python "$(w "$PIPE/render_queue.py")" status --kits "$(w "$KITS")" | grep -q '"alive": false' && break
  [ "$i" = 24 ] && fail "the render queue is still alive"
  sleep 5
done
if [ "$FROM" != "--from-render" ]; then
  say "1 install onto a copy of Samuel's timeline -> $NEW: $BEATS"
  if [ ! -s "$SPANS" ]; then   # first run: seed the records from his timeline's snapshot, remember where the changed beats sat
    python -X utf8 "$(w "$HERE/install_changed.py")" seed --beats "$BEATS" --kits "$(w "$KITS")" --out "$(w "$OUT")" --ver "$VER" \
      --timeline "$NEW" --src-timeline "$BASE" --snapshot "$(w "$SNAP")" >> "$LOG" 2>&1 || fail "seed"
    python -X utf8 -c "import json,glob,os,sys; d=sys.argv[1]; json.dump([(v['start'],v['end']) for f in glob.glob(os.path.join(d,'installed_*.json')) for v in json.load(open(f,encoding='utf-8'))['items'].values() if 'start' in v], open(sys.argv[2],'w'))" \
      "$(w "$INSTNEW")" "$(w "$SPANS")" || fail "seed spans"
  fi
  python -X utf8 "$(w "$HERE/install_changed.py")" build --beats "$BEATS" --kits "$(w "$KITS")" --out "$(w "$OUT")" --ver "$VER" \
    --timeline "$NEW" --src-timeline "$BASE" --tries 3 ${REPLACE:+--replace} ${PROJECT:+--project "$PROJECT"} >> "$LOG" 2>&1 || fail "install $VER"
  grep "verify" "$OUT/install_$VER.log" | tail -1 | cut -c1-400 >> "$LOG"
  say "2 snapshot $NEW and compare with Samuel's timeline (audio and his edits must come through unchanged)"
  python -X utf8 "$(w "$HERE/tl_snapshot.py")" "$(w "$NEWSNAP")" --timeline "$NEW" --kits "$(w "$KITS")" >> "$LOG" 2>&1 || fail "snapshot $VER"
  python -X utf8 "$(w "$HERE/tl_diff.py")" "$(w "$SNAP")" "$(w "$NEWSNAP")" >> "$LOG" 2>&1
  python -X utf8 - "$(w "$SNAP")" "$(w "$NEWSNAP")" "$(w "$INSTNEW")" "$(w "$SPANS")" >> "$LOG" 2>&1 <<'EOF' || fail "$NEW differs from Samuel's timeline outside the changed beats"
import json, sys, glob, os
a = json.load(open(sys.argv[1], encoding="utf-8")); b = json.load(open(sys.argv[2], encoding="utf-8"))
bad = [t for t in a["tracks"] if t.startswith("A") and a["tracks"][t] != b["tracks"].get(t)]
assert not bad, ("audio tracks changed", bad)
assert len(b["markers"]) in (0, len(a["markers"])), "markers"
INST = sys.argv[3]
spans = []
for f in glob.glob(os.path.join(INST, "installed_*.json")):
    its = [v for v in json.load(open(f, encoding="utf-8")).get("items", {}).values() if "start" in v]
    spans += [(v["start"], v["end"]) for v in its]
spans += [tuple(x) for x in json.load(open(sys.argv[4]))]   # where the changed beats sat on Samuel's timeline
for t in a["tracks"]:
    if not t.startswith("V"):
        continue
    A = {(i["s"], i["e"], i["name"]) for i in a["tracks"][t]}; B = {(i["s"], i["e"], i["name"]) for i in b["tracks"].get(t, [])}
    for s, e, n in sorted(A ^ B):
        assert any(s < e2 + 60 and e > s2 - 60 for s2, e2 in spans), ("outside the changed beats", t, s, e, n)
print("%s vs Samuel's timeline: audio identical, video changes only at the changed beats" % b["timeline"])
EOF
  say "3 A1 Voice Isolation on $NEW = $CUT's"
  python -X utf8 "$(w "$HERE/a1_voice.py")" --keep --timeline "$NEW" --src-timeline "$CUT" --kits "$(w "$KITS")" >> "$LOG" 2>&1 || fail "A1 voice isolation"
fi
say "4 chunked $RES render of $NEW + seam audio"
[ -z "$LEN" ] && [ -s "$NEWSNAP" ] && LEN="$(python -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); print(d['end']-d['start'])" "$(w "$NEWSNAP")")"
[ -n "$LEN" ] || fail "timeline length unknown: pass --len"
(cd "$KIT" && JOB="$JOB" KIT="$KIT" LEN="$LEN" TL="$NEW" RES="$RES" VER="$VER" bash "$BUILD") || fail "render $VER"
say "5 master"
python -X utf8 "$(w "$MASTER")" "$(w "$R/$NAME.mp4")" "$(w "$R/${NAME}_master.mp4")" >> "$LOG" 2>&1 || fail "master"
tail -3 "$LOG"
say "6 phone parts"
[ -n "$PARTS" ] || fail "no --parts and no --len/--snapshot to split the timeline"
mkdir -p "$R/phone parts (Editor)"; i=1; N=$(echo "$PARTS" | tr ',' '\n' | wc -l)
for r in $(echo "$PARTS" | tr ',' ' '); do
  a="${r%-*}"; b="${r#*-}"
  ss=$(python -c "print('%.6f' % ($a*1001/24000))"); du=$(python -c "print('%.6f' % (($b-$a)*1001/24000))")
  ffmpeg -y -v error -hwaccel cuda -ss $ss -i "$(w "$R/${NAME}_master.mp4")" -t $du -vf scale=1280:720:flags=lanczos -c:v h264_nvenc -preset p7 -multipass fullres -rc vbr -b:v 1550k -maxrate 2200k -bufsize 4400k -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$(w "$R/phone parts (Editor)/$LABEL $VER part $i of $N.mp4")" || fail "phone part $i"
  i=$((i+1))
done
say "FINISH $VER OK"
