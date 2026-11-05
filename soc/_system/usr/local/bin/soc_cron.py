#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from urllib.request import urlopen

BASE = Path("/home/ubuntu/cron-lab")
STATE = BASE / "state.json"
ALERT = BASE / "alerts.log"
RESPONSE = BASE / "response.log"
URL = "http://172.29.113.10:8080/state"

def get_state():
    with urlopen(URL, timeout=8) as r:
        return json.load(r)

def collect():
    data = get_state()
    STATE.write_text(json.dumps(data, indent=2))
    print("SOC_COLLECT_OK")
    print("CRONTAB:\n" + data["crontab"])

def detect():
    if not STATE.exists():
        sys.exit("RUN_COLLECT_FIRST")
    data = json.loads(STATE.read_text())
    checks = (
        "LAB4_PERSIST" in data["crontab"],
        "PERSISTENCE_CREATED" in data["actions.log"],
        "PERSISTENCE_CRON_EXECUTED" in data["executions.log"]
    )
    if all(checks):
        with ALERT.open("a") as f:
            f.write("CRON_PERSISTENCE_DETECTED\n")
        print("CRON_PERSISTENCE_DETECTED")
    else:
        print("DETECTION_PENDING:", checks)

def verify():
    data = get_state()
    checks = (
        "LAB4_NORMAL" in data["crontab"],
        "LAB4_PERSIST" not in data["crontab"],
        "PERSISTENCE_REMOVED_BASELINE_PRESERVED"
            in data["actions.log"],
        ALERT.exists() and
            "CRON_PERSISTENCE_DETECTED" in ALERT.read_text()
    )
    if all(checks):
        with RESPONSE.open("a") as f:
            f.write("PERSISTENCE_REMOVED_VERIFIED\n")
        print("PERSISTENCE_REMOVED_VERIFIED")
    else:
        sys.exit(f"RESPONSE_NOT_VERIFIED: {checks}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: soc_cron.py collect|detect|verify")
    commands = {
        "collect": collect,
        "detect": detect,
        "verify": verify
    }
    command = commands.get(sys.argv[1])
    if command is None:
        sys.exit("UNKNOWN_MODE")
    command()
