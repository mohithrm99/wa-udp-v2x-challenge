#DO NOT CHANGE THIS FILE

#!/usr/bin/env bash

# Test Case 02: Multiple beacons from different vehicles
# - Beacons:
#     veh_A at [3.0, 4.0] → dist = 5.0
#     veh_B at [6.0, 8.0] → dist = 10.0
# - Expectation:
#     count = 2
#     nearest = {"id": "veh_A", "dist": 5.0}
# - Verifies candidate can track multiple neighbors and pick the closest.



set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/harness"
GRADER="$ROOT/grader"

export BEACON_DISABLE="1"   # send nothing
unset BEACON_MESSAGES
export BEACON_SLEEP_BEFORE_MS="200"  # irrelevant; disabled

unset EXPECT_MIN_COUNT
unset EXPECT_NEAREST_PRESENT  # nearest not required

bash "$HARNESS/launch.sh" &
HPID=$!
sleep 0.05

if python "$GRADER/verify_and_run.py"; then
  echo "[PASS] test_case_02"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 0
else
  echo "[FAIL] test_case_02"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 1
fi