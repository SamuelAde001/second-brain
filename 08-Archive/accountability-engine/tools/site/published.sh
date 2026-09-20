#!/usr/bin/env bash
# Is the LIVE site actually showing the record we built here?
#
# Why this exists: on 2026-08-28 six consecutive Pages deploys failed and
# nothing said a word. Every session truthfully reported "rebuilt and pushed"
# and was wrong about the only thing that mattered — what Samuel could see.
# A push is not a publish. This checks the deploy.
#
# It compares content_hash: a sha256 of the record with the build clock
# stripped out. Wall-clock stamps are useless here because this machine
# writes WAT and the CI runner writes UTC, so identical records would look
# different forever. Same hash = the live site is showing this record.

set -u
URL="${1:-https://samuelade001.github.io/engine}"
LOCAL="site/data/os.json"

fail() { echo "NOT PUBLISHED: $1"; exit 1; }
hash_of() { python -c "import json,sys;print(json.load(sys.stdin)['content_hash'])" 2>/dev/null; }

[ -f "$LOCAL" ] || fail "no local build at $LOCAL — run tools/site/build.py"
local_hash=$(hash_of < "$LOCAL")
[ -n "$local_hash" ] || fail "local build has no content_hash — rebuild with tools/site/build.py"

code=$(curl -s -o /dev/null -w '%{http_code}' -L "$URL/" || echo 000)
[ "$code" = "200" ] || fail "$URL/ returned HTTP $code — the site is not being served"

live_hash=$(curl -s -L "$URL/data/os.json" | hash_of)
[ -n "$live_hash" ] || fail "served a page but could not read content_hash from data/os.json"

echo "local : $local_hash"
echo "live  : $live_hash"
if [ "$local_hash" = "$live_hash" ]; then
  echo "PUBLISHED: $URL/ is showing this exact record."
else
  echo "STALE: the live site is showing a different record. The deploy has not caught up."
  exit 1
fi
