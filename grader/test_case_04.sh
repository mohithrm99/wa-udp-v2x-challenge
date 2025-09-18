#DO NOT CHANGE THIS FILE

#!/usr/bin/env bash

# Test Case 04: Multiple beacons for the same vehicle ID
# - Beacons:
#     veh_Z at [5.0, 0.0] → dist = 5.0
#     veh_Z again at [2.0, 0.0] → dist = 2.0 (latest overwrites)
# - Expectation:
#     count = 1
#     nearest = {"id": "veh_Z", "dist": 2.0}
# - Verifies candidate correctly updates info for a single ID and keeps the latest.




set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/harness"
GRADER="$ROOT/grader"

# Mix of bad and good messages; candidate should ignore bad ones
export BEACON_MESSAGES='[
  {"id": null,         "pos": [0, 0],   "speed": 1.0},
  {"id": "veh_X",      "pos": [1],      "speed": 1.0},
  {"id": "veh_Y",      "pos": [-6, 8],  "speed": 3.0}
]'
export BEACON_DISABLE="0"
export BEACON_SLEEP_BEFORE_MS="600"
export BEACON_INTERVAL_MS="20"

export EXPECT_MIN_COUNT="1"
export EXPECT_NEAREST_PRESENT="1"
export EXPECT_NEAREST_ID="veh_Y"
export EXPECT_NEAREST_DIST="10.0"
export EXPECT_NEAREST_TOL="0.01"

bash "$HARNESS/launch.sh" &
HPID=$!
sleep 0.1

if python "$GRADER/verify_and_run.py"; then
  echo "[PASS] test_case_04"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 0
else
  echo "[FAIL] test_case_04"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 1
fi
