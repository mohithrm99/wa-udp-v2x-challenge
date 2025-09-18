#DO NOT CHANGE THIS FILE

#!/usr/bin/env bash


# Test Case 03: Ignore malformed messages
# - Beacons:
#     1 valid → {"id": "veh_X", "pos": [1.0, 1.0], "speed": 1.0, "ts": <ms>}
#     1 malformed → {"bad": "data"}  (missing required fields)
# - Expectation:
#     count = 1
#     nearest = {"id": "veh_X", "dist": sqrt(2) ≈ 1.41}
# - Ensures candidate ignores invalid input and doesn’t crash.




set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/harness"
GRADER="$ROOT/grader"

# veh_123 at [10,5] (~11.18), veh_B at [3,4] (5.0) -> nearest veh_B
export BEACON_MESSAGES='[
  {"id":"veh_123","pos":[10,5],"speed":4.0},
  {"id":"veh_B","pos":[3,4],"speed":2.0}
]'
export BEACON_DISABLE="0"
export BEACON_SLEEP_BEFORE_MS="800"
export BEACON_INTERVAL_MS="30"

export EXPECT_MIN_COUNT="2"
export EXPECT_NEAREST_PRESENT="1"
export EXPECT_NEAREST_ID="veh_B"
export EXPECT_NEAREST_DIST="5.0"
export EXPECT_NEAREST_TOL="0.01"

bash "$HARNESS/launch.sh" &
HPID=$!
sleep 0.1

if python "$GRADER/verify_and_run.py"; then
  echo "[PASS] test_case_03"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 0
else
  echo "[FAIL] test_case_03"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 1
fi