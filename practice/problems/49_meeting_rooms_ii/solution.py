"""
Meeting Rooms II (LeetCode 253) - Medium
Area: intervals / heap
Key operations: sort by start, pop every end time <= start, push the new end, track the max heap size

Given meeting intervals [start, end), return the minimum number of conference rooms needed so
that no two meetings in the same room overlap. A meeting may start exactly when another ends.
Example: [[0,30],[5,10],[15,20]] -> 2
"""
import sys
import heapq
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(intervals: List[List[int]]) -> int:
    """Sweep every time unit and count the meetings in progress (start <= t < end); the answer is
    the peak. O(n * C) for coordinate range C; the waste is recounting from scratch at every
    instant when the count only changes at starts and ends."""
    best = 0
    for t in range(max((e for _, e in intervals), default=0)):
        best = max(best, sum(1 for s, e in intervals if s <= t < e))
    return best


# --- optimal ---
def solve(intervals: List[List[int]]) -> int:
    """Sort by start; a min-heap holds the end time of every occupied room. For each meeting free
    the rooms that have ended, take a room, record the peak occupancy. O(n log n)."""
    intervals = sorted(intervals, key=lambda iv: iv[0])
    log(f"sorted by start: {intervals}")
    ends = []  # min-heap of end times, one per occupied room
    rooms = 0
    for start, end in intervals:
        while ends and ends[0] <= start:
            freed = heapq.heappop(ends)
            log(f"    room ending {freed} <= {start} is free again; ends {ends}")
        heapq.heappush(ends, end)
        rooms = max(rooms, len(ends))
        log(f"[{start},{end}] takes a room | ends heap {ends} | in use {len(ends)}, peak {rooms}")
    return rooms


# --- demo ---
def demo():
    return solve([[0, 30], [5, 10], [15, 20]])


# --- tests ---
def tests():
    assert solve([[0, 30], [5, 10], [15, 20]]) == 2
    assert solve([[7, 10], [2, 4]]) == 1
    assert solve([[1, 5], [5, 10]]) == 1  # back to back share a room
    assert solve([]) == 0
    assert solve([[3, 4]]) == 1
    assert solve([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]]) == 4
    assert solve([[9, 10], [4, 9], [4, 17]]) == 2
    assert solve([[0, 1], [0, 1], [5, 6]]) == 2  # peak is early, not at the end
    assert solve([[1, 2], [1, 3], [0, 10], [4, 5]]) == 3  # a long early meeting
    import random
    random.seed(1)
    for _ in range(200):
        ivs = []
        for _ in range(random.randint(0, 8)):
            s = random.randint(0, 12)
            ivs.append([s, s + random.randint(1, 6)])
        assert solve(ivs) == brute_force(ivs), ivs


# --- bugs ---
BUGS = [
    {
        "replace": "        while ends and ends[0] <= start:",
        "with":    "        while ends and ends[0] < start:",
        "fix": "a room whose meeting ends exactly at start is free: compare with <=",
        "why": "Back-to-back meetings are counted as overlapping, so [[1,5],[5,10]] returns 2 instead of 1.",
        "decoys": [
            {"line": "        heapq.heappush(ends, end)", "change": "should push start"},
            {"line": "    ends = []  # min-heap of end times, one per occupied room", "change": "should start as [0]"},
            {"line": "    return rooms", "change": "should return len(ends)"},
        ],
    },
    {
        "replace": "        rooms = max(rooms, len(ends))",
        "with":    "        rooms = len(ends)",
        "fix": "the answer is the PEAK occupancy: rooms = max(rooms, len(ends))",
        "why": "Only the occupancy after the last meeting survives, so [[0,1],[0,1],[5,6]] returns 1 instead of 2.",
        "decoys": [
            {"line": "            freed = heapq.heappop(ends)", "change": "should pop ends[-1]"},
            {"line": "    for start, end in intervals:", "change": "should iterate intervals[1:]"},
            {"line": "    rooms = 0", "change": "should start at 1"},
        ],
    },
    {
        "replace": "    intervals = sorted(intervals, key=lambda iv: iv[0])",
        "with":    "    intervals = sorted(intervals, key=lambda iv: iv[1])",
        "fix": "sort by START so meetings arrive in chronological order",
        "why": "Sorted by end, a long early meeting arrives last and finds rooms already freed by meetings it actually overlaps: [[1,2],[1,3],[0,10],[4,5]] returns 2 instead of 3.",
        "decoys": [
            {"line": "        while ends and ends[0] <= start:", "change": "should be if instead of while"},
            {"line": "        rooms = max(rooms, len(ends))", "change": "should be max(rooms, len(ends) + 1)"},
            {"line": "        heapq.heappush(ends, end)", "change": "should happen before the while loop"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
