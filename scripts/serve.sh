#!/usr/bin/env bash
# Serve the site on localhost and open it in the browser.
# Usage: ./scripts/serve.sh [port]   (default 8000)
set -e
cd "$(dirname "$0")/.."
PORT="${1:-8000}"
URL="http://localhost:$PORT/"
echo "Serving at $URL  (Ctrl+C to stop)"
( sleep 1; open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null ) &
exec python3 -m http.server "$PORT" --bind 127.0.0.1
