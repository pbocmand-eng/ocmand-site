#!/usr/bin/env bash
# Rebuild the site and run the automated check. Usage:  bash _source/check.sh
# Passes when it prints "ISSUES (0)". Needs python3, node and Playwright (already present in Claude cloud sessions).
set -e
cd "$(dirname "$0")/.."
python3 _source/build.py
python3 _source/serve.py . 8812 & SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT
sleep 1
node _source/qa.js
