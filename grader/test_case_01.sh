#DO NOT CHANGE THIS FILE

#!/usr/bin/env bash

# Test Case 01: Single well-formed beacon
# - Beacon sent: {"id": "veh_123", "pos": [10.0, 5.0], "speed": 4.0, "ts": <ms>}
# - Expectation:
#     count = 1
#     nearest = {"id": "veh_123", "dist": sqrt(10^2 + 5^2) ≈ 11.18}
# - Checks candidate can parse a single message and compute distance.


set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HARNESS="$ROOT/harness"
GRADER="$ROOT/grader"

# Expect one neighbor: veh_123 at [10,5] -> dist ~ 11.18034
export BEACON_DISABLE="0"
unset BEACON_MESSAGES  # use default in publisher
export BEACON_SLEEP_BEFORE_MS="1000"
export BEACON_INTERVAL_MS="50"

export EXPECT_MIN_COUNT="1"
export EXPECT_NEAREST_PRESENT="1"
export EXPECT_NEAREST_ID="veh_123"
export EXPECT_NEAREST_DIST="11.18034"
export EXPECT_NEAREST_TOL="0.05"

bash "$HARNESS/launch.sh" &
HPID=$!
sleep 0.15

if python "$GRADER/verify_and_run.py"; then
  echo "[PASS] test_case_01"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 0
else
  echo "[FAIL] test_case_01"
  kill "$HPID" 2>/dev/null || true; wait "$HPID" 2>/dev/null || true
  exit 1
fi