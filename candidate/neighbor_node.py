#Author: Mohith Muchukota
#Date: 9/16/2025
#This should be the only file you edit. You are free to look at other files for reference, but do not change them.
#Below are are two methods which you must implement: euclidean_dist_to_origin and nearest_neighbor as well as the main function beacon handling. 
#Helper Functions are allowed, but not required. You must not change the imports, the main function signature, or the return value of the main function.


"""
Neighbor Table

Listen on UDP 127.0.0.1:5005 for beacon messages:
  {"id":"veh_XXX","pos":[x,y],"speed":mps,"ts":epoch_ms}

Collect beacons for ~1 second starting from the *first* message.
Then print exactly ONE JSON line and exit:

{
  "topic": "/v2x/neighbor_summary",
  "count": <int>,
  "nearest": {"id": "...", "dist": <float>} OR null,
  "ts": <now_ms>
}

Constraints:
- Python 3 stdlib only.
- Ignore malformed messages; don’t crash.
- Do NOT listen to ticks (5006).
"""

import socket, json, time, math, sys
from multiprocessing.util import MAXFD
from typing import Dict, Any, Optional, Tuple

HOST = "127.0.0.1"
PORT_BEACON = 5005
COLLECT_WINDOW_MS = 1000  # ~1 second


def now_ms() -> int:
    return int(time.time() * 1000)


def euclidean_dist_to_origin(pos) -> float:
    if pos is not None and pos is [float, float]:  # validating that pos isn't None and is [x, y] of numbers
        return math.sqrt(pos[0] ** 2 + pos[1] ** 2)  # using the pythagorean theorem to calculate euclidian distance
    return 0.0


def nearest_neighbor(neighbors: Dict[str, Dict[str, Any]]) -> Optional[Tuple[str, float]]:
    # neighbors[id] -> {"pos":[x,y], "speed": float, "last_ts": int}
    id = ""
    dist = sys.float_info.max
    for neighbor in neighbors:
        if euclidean_dist_to_origin(neighbors[neighbor].get("pos")) < dist: # if the distance of this neighbor is
            # shorter, we replace id and dist with the id and dist of this neighbor
            id = neighbors[neighbor].get("id")
            dist = euclidean_dist_to_origin(neighbors[neighbor].get("pos"))

    nearest = (id, dist)
    return nearest


def main() -> int:
    neighbors: Dict[str, Dict[str, Any]] = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT_BEACON))
    sock.settimeout(1.5)

    first_ts: Optional[int] = None
    try:
        while True:
            try:
                data, _ = sock.recvfrom(4096)
            except socket.timeout:
                break

            try:
                msg = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                continue

                # Expect: {"id": "...", "pos":[x,y], "speed": float, "ts": int}
            # TODO: validate required keys/types defensively
            if msg["id"] is None: return -1
            if msg["pos"] is None or msg["pos"] != [float, float]: return -2
            if msg["speed"] is None or msg["speed"] != float: return -3
            if msg["ts"] is None or msg["ts"] != int: return -4

            nearest = nearest_neighbor(msg)
            neighbor = {
                "topic": "/v2x/neighbor_summary",
                "count": msg["count"],
                "nearest": nearest,
                "ts": msg["ts"]
            }

            print(json.dumps(neighbor))
            #   neighbors[msg["id"]] = {"pos": msg["pos"], "speed": msg["speed"], "last_ts": msg["ts"]}
            #hint: beacon handling, check each message and store in neighbors, try to cover edge cases
            # try to avoid changing anything in the main function outside this TODO block

            #END of TODO block
            now = now_ms()
            if first_ts is None:
                first_ts = now
            # stop after ~1 second from first message
            if first_ts is not None and (now - first_ts) >= COLLECT_WINDOW_MS:
                break

    finally:
        sock.close()

    # Build summary
    nn = nearest_neighbor(neighbors)
    summary = {
        "topic": "/v2x/neighbor_summary",
        "count": len(neighbors),
        "nearest": None if nn is None else {"id": nn[0], "dist": nn[1]},
        "ts": now_ms(),
    }
    print(json.dumps(summary), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
