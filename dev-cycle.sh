#!/usr/bin/env bash
set -u

REPO="$HOME/zarkmid"
LOGDIR="$REPO/typescripts"

cd "$REPO" || exit 1
mkdir -p "$LOGDIR"

STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$LOGDIR/$STAMP.typescript"

echo "Updating repository..."
git pull --ff-only || echo "WARNING: git pull failed; continuing."

echo "Recording session to: $LOG"
echo "Type exit when finished."

script --quiet --flush --return --command "bash -i" "$LOG"
STATUS=$?

chmod 644 "$LOG"

echo
echo "Session recorded:"
echo "  $LOG"
echo
echo "Review it, then publish with:"
echo "  git add typescripts/"
echo "  git commit -m \"Add development session $STAMP\""
echo "  git push"

exit "$STATUS"
