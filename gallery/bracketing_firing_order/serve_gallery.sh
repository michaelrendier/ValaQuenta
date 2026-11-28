#!/bin/bash
# Serve the Bracketing and firing order gallery on loopback only (the repo root is served so the code flow chart link works). Stop with: pkill -f "http.server $PORT"
PORT=${1:-8795}; ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
curl -s -o /dev/null "http://127.0.0.1:$PORT/gallery/bracketing_firing_order/index.html" || { nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$ROOT" >/dev/null 2>&1 & sleep 1; }
xdg-open "http://127.0.0.1:$PORT/gallery/bracketing_firing_order/index.html" >/dev/null 2>&1
