#!/usr/bin/env bash
# Print one or more named sections of a markdown file instead of the whole file.
# Loading a 19KB file to read one rule is how sessions get expensive.
#
#   bash tools/section.sh context/money.md "Rules"
#   bash tools/section.sh context/body.md "Sleep" "Daily anchors"
#
# Matching is case-insensitive and prefix-based on the heading text, so
# "Sleep" finds "## Sleep — the load-bearing wall". A section runs to the next
# heading at the same or shallower level. With no section names, lists what's there.
set -euo pipefail
file="${1:?usage: section.sh FILE [SECTION...]}"; shift
[ -f "$file" ] || { echo "no such file: $file" >&2; exit 1; }

if [ $# -eq 0 ]; then
  echo "sections in $file:"
  grep -n '^#\{1,6\} ' "$file" | sed 's/^\([0-9]*\):/  [\1] /'
  exit 0
fi

for want in "$@"; do
  awk -v want="$want" '
    function level(l){ match(l,/^#+/); return RLENGTH }
    /^#+ / {
      if (inside && level($0) <= depth) { inside=0 }
      if (!inside) {
        h=$0; sub(/^#+[ \t]*/,"",h)
        if (tolower(substr(h,1,length(want))) == tolower(want)) { inside=1; depth=level($0) }
      }
    }
    inside { print }
  ' "$file"
  echo
done
