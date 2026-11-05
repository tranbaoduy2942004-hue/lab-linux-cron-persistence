#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime, timezone

BASE = Path("/home/ubuntu/cron-lab")
LOG = BASE / "executions.log"

if len(sys.argv) != 2 or sys.argv[1] not in ("normal", "persist"):
    sys.exit("Usage: cron_task.py normal|persist")

mode = sys.argv[1]

event = (
    "NORMAL_CRON_EXECUTED"
    if mode == "normal"
    else "PERSISTENCE_CRON_EXECUTED"
)

BASE.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now(timezone.utc).isoformat()

with LOG.open("a") as f:
    f.write(f"{timestamp} {event}\n")
