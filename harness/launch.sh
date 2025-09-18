#!/usr/bin/env bash
# Launch both publishers and wait for them to finish (works from any cwd)

set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "$DIR/publisher_beacons.py" &
P1=$!

python "$DIR/publisher_ticks.py" &
P2=$!

wait "$P1" "$P2"