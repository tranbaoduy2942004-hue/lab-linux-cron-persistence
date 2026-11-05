#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = Path("/home/ubuntu/cron-lab")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.client_address[0] != "172.29.113.20":
            self.send_error(403)
            return
        if self.path != "/state":
            self.send_error(404)
            return

        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True
        )
        data = {"crontab": result.stdout}
        for name in ("actions.log", "executions.log"):
            path = BASE / name
            data[name] = path.read_text() if path.exists() else ""

        raw = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
