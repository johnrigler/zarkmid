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

echo
echo "Starting recorded development session."
echo "Transcript: $LOG"
echo

BOOTSTRAP='
echo
echo "========================================"
echo " ZARKMID SESSION CONTEXT"
echo "========================================"

echo
echo "[identity]"
whoami
hostname
pwd

echo
echo "[git]"
git remote -v
git status --short --branch
printf "HEAD: "
git rev-parse --short HEAD 2>/dev/null || true
printf "Last commit: "
git log -1 --pretty="%h %ad %s" --date=iso 2>/dev/null || true

echo
echo "[runtime]"
printf "Python: "
python3 --version 2>&1 || true
printf "dfrotz: "
command -v dfrotz || true
printf "curl: "
command -v curl || true

echo
echo "[project files]"
ls -la

echo
echo "[games]"
if [ -d games ]; then
    find games -maxdepth 2 -type f -printf "%p\n" | sort
else
    echo "games/ directory not found"
fi

echo
echo "[lantern]"
if [ -f lantern.py ]; then
    ls -l lantern.py
else
    echo "lantern.py not found"
fi

echo
echo "[port 7788]"
if command -v ss >/dev/null 2>&1; then
    ss -ltnp 2>/dev/null | grep ":7788" || echo "nothing listening on 7788"
else
    echo "ss command unavailable"
fi

echo
echo "[lantern probe]"
if command -v curl >/dev/null 2>&1; then
    curl --max-time 2 -i http://127.0.0.1:7788/ 2>&1 || echo "Lantern HTTP probe did not respond"
else
    echo "curl unavailable"
fi

echo
echo "========================================"
echo " Interactive shell ready."
echo " Run tests, inspect files, start Lantern, etc."
echo " Type exit when finished."
echo "========================================"
echo

exec bash -i
'

script --quiet --flush --return --command "bash -lc '$BOOTSTRAP'" "$LOG"
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
