#!/bin/bash
set -euo pipefail

BASE=/home/ubuntu/cron-lab
LOG="$BASE/actions.log"
NORMAL='* * * * * /usr/bin/python3 /usr/local/bin/cron_task.py normal # LAB4_NORMAL'
PERSIST='* * * * * /usr/bin/python3 /usr/local/bin/cron_task.py persist # LAB4_PERSIST'
mkdir -p "$BASE"

CURRENT=$(crontab -l 2>/dev/null || true)
MODE="${1:-}"

case "$MODE" in
  normal)
    if ! printf '%s\n' "$CURRENT" | grep -Fxq "$NORMAL"; then
      printf '%s\n%s\n' "$CURRENT" "$NORMAL" | sed '/^$/d' | crontab -
    fi
    echo "NORMAL_CRON_CONFIGURED" | tee -a "$LOG"
    ;;
  attack)
    if ! printf '%s\n' "$CURRENT" | grep -Fxq "$NORMAL"; then
      echo "ERROR: RUN_NORMAL_FIRST"; exit 1
    fi
    if ! printf '%s\n' "$CURRENT" | grep -Fxq "$PERSIST"; then
      printf '%s\n%s\n' "$CURRENT" "$PERSIST" | sed '/^$/d' | crontab -
    fi
    echo "PERSISTENCE_CREATED" | tee -a "$LOG"
    ;;
  cleanup)
    printf '%s\n' "$CURRENT" | grep -Fxv "$PERSIST" | crontab -
    crontab -l | grep -Fxq "$NORMAL" || exit 1
    if crontab -l | grep -Fxq "$PERSIST"; then exit 1; fi
    echo "PERSISTENCE_REMOVED_BASELINE_PRESERVED" | tee -a "$LOG"
    ;;
  status)
    crontab -l 2>/dev/null || true
    ;;
  *)
    echo "Usage: manage_cron.sh normal|attack|status|cleanup"
    exit 2
    ;;
esac
