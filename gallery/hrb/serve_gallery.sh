#!/bin/bash
# Serve the H_RB gallery on loopback only. Stop with: pkill -f "http.server $PORT"
PORT=${1:-8790}; DIR="$(cd "$(dirname "$0")" && pwd)"
curl -s -o /dev/null "http://127.0.0.1:$PORT/index.html" || { nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR" >/dev/null 2>&1 & sleep 1; }
xdg-open "http://127.0.0.1:$PORT/index.html" >/dev/null 2>&1
