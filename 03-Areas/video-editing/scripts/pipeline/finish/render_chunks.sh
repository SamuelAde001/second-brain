#!/bin/bash
# Chunked final render of a timeline: 2020-f chunks with a Resolve restart before each (one long pass dies on memory), video-only join,
# then seam_audio.py splices clean audio over the joins. 4K renders with the kit's render_4k.py, RES=1080 with render_review.py. Resumable: a chunk already on disk is skipped.
#   JOB=<job folder> LEN=<timeline frames> TL="Visuals v3 (Editor)" VER=v3 [RES=1080] [RERENDER="4040 8080"] bash render_chunks.sh
# Promoted from video 4's kit build_v1.sh on 2026-10-30 (General Manager). The render queue must be stopped first (it restarts Resolve too).
# Needs the job kit's final\render_4k.py + seam_audio.py (in the master kit since 2026-10-30) and kits\open_job.py, kits\render_queue.py.
HERE="$(cd "$(dirname "$0")" && pwd)"
BRAIN="$(cd "$HERE/../../../../.." && pwd)"
[ -n "$JOB" ] || { echo "JOB=<job folder> is required"; exit 64; }
[ -n "$LEN" ] || { echo "LEN=<timeline length in frames> is required"; exit 64; }
KIT="${KIT:-$JOB/Graphics/Frontal kit (Editor)}"
VER="${VER:-v1}"
TL="${TL:-Visuals v1 (Editor)}"
CH="${CH:-2020}"
if [ "$RES" = "1080" ]; then
  OUT="$JOB/Renders/$VER 1080p (Editor)"; NAME="${VER}_1080"; RDIR="$HERE"; RSCRIPT="render_review.py"; RARGS=(--kits "$(cygpath -w "$KIT/kits")")
else
  OUT="$JOB/Renders/$VER 4K (Editor)"; NAME="${VER}_4k"; RDIR="$KIT/final"; RSCRIPT="render_4k.py"; RARGS=()
fi
mkdir -p "$OUT"
LOG="${LOG:-$OUT/build_$VER.log}"
w() { cygpath -w "$1"; }
say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
fail() { say "FAILED: $*"; exit 1; }
restart() {
  python - <<'EOF' >> "$LOG" 2>&1
import sys
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
r = dvr.scriptapp("Resolve")
print("save before restart:", r.GetProjectManager().SaveProject() if r else "no Resolve")
EOF
  python "$BRAIN/03-Areas/video-editing/scripts/restart_resolve.py" --force >> "$LOG" 2>&1 || fail "restart"
  (cd "$KIT" && timeout 400 python kits/open_job.py --wait 380 >> "$LOG" 2>&1) || fail "open_job"
  python - <<'EOF2' >> "$LOG" 2>&1
import sys
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr
r = dvr.scriptapp("Resolve"); p = r.GetProjectManager().GetCurrentProject()
n = len(p.GetRenderJobList()); p.DeleteAllRenderJobs(); r.GetProjectManager().SaveProject()
print("render queue cleared:", n, "jobs; rendering", p.IsRenderingInProgress(), "project", p.GetName())
EOF2
}
python "$HERE/../resolve_guard.py" preflight --kits "$(w "$KIT/kits")" --for render >> "$LOG" 2>&1 || fail "resolve_guard preflight blocked (see $LOG)"
for s in $RERENDER; do
  e=$((s + CH)); [ $e -gt $LEN ] && e=$LEN
  f="$OUT/$(printf '%s_%05d_%05d.mp4' "$NAME" "$s" "$e")"
  [ -s "$f" ] && { mv "$f" "$f.old_$(date +%H%M%S)"; say "render: moved aside $s-$e for a re-render"; }
  rm -f "$OUT/$(printf '%s_%05d_%05d_v.mp4' "$NAME" "$s" "$e")"
done
for s in $(seq 0 $CH $((LEN - 1))); do
  e=$((s + CH)); [ $e -gt $LEN ] && e=$LEN
  f="$OUT/$(printf '%s_%05d_%05d.mp4' "$NAME" "$s" "$e")"
  [ -s "$f" ] && { say "render: have $s-$e"; continue; }
  say "render: restart Resolve for $s-$e"; restart
  (cd "$RDIR" && python -u "$RSCRIPT" "$TL" "$(w "$OUT")" "${RARGS[@]}" --name "$NAME" --from "$s" --to "$e" >> "$LOG" 2>&1) || fail "render $s-$e"
done
say "render: video-only join"
(cd "$RDIR" && python -u "$RSCRIPT" "$TL" "$(w "$OUT")" "${RARGS[@]}" --name "$NAME" --chunk $CH >> "$LOG" 2>&1) || fail "render join"
say "render: seam audio"; restart
(cd "$KIT/final" && python -u seam_audio.py "$TL" "$(w "$OUT")" "$NAME" >> "$LOG" 2>&1) || fail "seam_audio"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,width,height,codec_name -of csv=p=0 "$(w "$OUT/$NAME.mp4")" | sed 's/^/video: /' | tee -a "$LOG"
say "ALL DONE: $OUT/$NAME.mp4"
