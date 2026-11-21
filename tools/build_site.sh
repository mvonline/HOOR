#!/usr/bin/env bash
# Rebuild the private story site end to end.
#   tools/build_site.sh              sync -> check -> snapshot -> encrypt (asks passphrase) -> build
#   tools/build_site.sh --no-encrypt skip the encrypt step (keeps the existing public/content.hoor)
# Run from anywhere. The passphrase is typed by you on the TTY; this script never stores it.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="$ROOT/sites/hoor-github-pages-20261121"
ENCRYPT=1
[ "${1:-}" = "--no-encrypt" ] && ENCRYPT=0

cd "$ROOT"
echo "== 1/5 sync dialogues from the v10 screenplay"
python3 -I tools/sync_dialogues.py
echo "== 2/5 continuity check (read-only report)"
python3 -I tools/check_continuity.py | tail -15
cd "$SITE"
[ -d node_modules ] || { echo "== npm ci"; npm ci; }
echo "== 3/5 snapshot (plain text, git-ignored)"
npm run --silent snapshot
if [ "$ENCRYPT" = 1 ]; then
  echo "== 4/5 encrypt (type the passphrase when asked)"
  npm run --silent encrypt
else
  echo "== 4/5 encrypt skipped (--no-encrypt): public/content.hoor is unchanged"
fi
echo "== 5/5 type check + vite build"
npx tsc --noEmit
npm run --silent build
echo "Done: $SITE/dist"
[ "$ENCRYPT" = 0 ] && echo "Note: dist/ still carries the OLD content.hoor; run again without --no-encrypt to ship the new story."
