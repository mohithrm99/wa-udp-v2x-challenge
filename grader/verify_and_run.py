#!/usr/bin/env python3
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CAND = os.path.join(ROOT, "candidate", "neighbor_node.py")
REQ_TOPIC = "/v2x/neighbor_summary"

def is_number(x): return isinstance(x, (int, float)) and not isinstance(x, bool)

def verify_json_line(line: str) -> None:
    obj = json.loads(line)  # let this raise if invalid
    for k in ("topic","count","nearest","ts"):
        if k not in obj: raise AssertionError(f"Missing key: {k}")
    if obj["topic"] != REQ_TOPIC: raise AssertionError("wrong topic")
    if not isinstance(obj["count"], int) or obj["count"] < 0: raise AssertionError("bad count")
    if not isinstance(obj["ts"], int): raise AssertionError("ts must be int")

    # --- Optional expectations via env ---
    exp_min_count = os.getenv("EXPECT_MIN_COUNT")
    exp_nearest_present = os.getenv("EXPECT_NEAREST_PRESENT")  # "1" means must be present
    exp_nearest_id = os.getenv("EXPECT_NEAREST_ID")
    exp_nearest_dist = os.getenv("EXPECT_NEAREST_DIST")
    exp_nearest_tol = float(os.getenv("EXPECT_NEAREST_TOL", "0.05"))

    nearest = obj["nearest"]

    if exp_nearest_present == "1":
        if nearest is None:
            raise AssertionError("Expected nearest to be present")
        if not isinstance(nearest, dict): raise AssertionError("nearest must be object")
        if "id" not in nearest or "dist" not in nearest: raise AssertionError("nearest missing id/dist")
        if exp_nearest_id is not None and nearest["id"] != exp_nearest_id:
            raise AssertionError(f"nearest.id={nearest['id']!r} != {exp_nearest_id!r}")
        if exp_nearest_dist is not None:
            try:
                target = float(exp_nearest_dist)
            except ValueError:
                raise AssertionError("EXPECT_NEAREST_DIST not a float")
            if not is_number(nearest["dist"]) or abs(nearest["dist"] - target) > exp_nearest_tol:
                raise AssertionError(f"nearest.dist {nearest['dist']} not within {exp_nearest_tol} of {target}")
    else:
        # if not required present, still validate shape if present
        if nearest is not None:
            if not isinstance(nearest, dict): raise AssertionError("nearest must be object or null")
            if "id" not in nearest or "dist" not in nearest: raise AssertionError("nearest missing id/dist")

    if exp_min_count is not None:
        try:
            mc = int(exp_min_count)
        except ValueError:
            raise AssertionError("EXPECT_MIN_COUNT not an int")
        if obj["count"] < mc:
            raise AssertionError(f"count {obj['count']} < EXPECT_MIN_COUNT {mc}")

def main() -> int:
    try:
        proc = subprocess.Popen(["python", CAND], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        print(f"ERROR: candidate not found at {CAND}", file=sys.stderr)
        return 2
    try:
        out, err = proc.communicate(timeout=8.0)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        print("ERROR: candidate timed out.", file=sys.stderr)
        print("STDOUT:", out, file=sys.stderr)
        print("STDERR:", err, file=sys.stderr)
        return 1

    if err.strip():
        print(f"[candidate stderr]\n{err}", file=sys.stderr)

    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if len(lines) != 1:
        print(f"ERROR: expected exactly 1 JSON line, got {len(lines)}", file=sys.stderr)
        print("STDOUT:", out, file=sys.stderr)
        return 1

    try:
        verify_json_line(lines[0])
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())