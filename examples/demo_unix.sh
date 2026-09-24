#!/usr/bin/env bash
set -e
python examples/demo_upstream.py &
UP=$!
sleep 1
mockrelay serve --mode record &
MR=$!
sleep 2
curl -s http://localhost:8080/local/v1/users
echo
echo "fixtures:"
find fixtures/local -name '*.json' 2>/dev/null || true
kill $MR $UP 2>/dev/null || true
echo
echo "now run: mockrelay serve --mode replay --latency 150"
