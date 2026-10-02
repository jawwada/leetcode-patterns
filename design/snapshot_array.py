"""
Snapshot Array (LeetCode 1146)  — Medium
Pattern: Sorted version list + binary search

Problem
-------
Implement SnapshotArray(length) of zeros with set(index, val), snap() -> snap_id (the number of
snaps taken before this one), and get(index, snap_id) -> the value at index as of that snapshot.
Example: SnapshotArray(3); set(0,5); snap()->0; set(0,6); get(0,0)->5.

Brute force
-----------
snap() copies the whole current array into a list of snapshots; get(index, snap_id) indexes the
stored copy. O(1) set and get, but O(length) per snap and O(snaps * length) space. The wasted
work is copying every cell on every snapshot even though typically only a handful of cells
changed since the previous snapshot; identical values are duplicated across all copies.

From brute force to optimal
---------------------------
Store changes, not copies: for each index keep a list of (snap_id, value) pairs recording only
the snapshots in which that cell was written. snap_ids only increase, so each per-index list is
sorted by construction, and get(index, snap_id) becomes "the last pair with snap_id <= query",
a bisect_right on that list. Multiple sets within the same snapshot overwrite the last pair
instead of appending, so the list length is bounded by the number of distinct snapshots in
which the cell changed. The tracker remembers only cells that actually changed and when; it
forgets nothing it needs but never stores a value twice.

Intuition
---------
A snapshot is just a monotonically increasing counter; the data lives in per-cell histories.
Asking "what was cell i at snapshot k" is "find the most recent write to cell i that happened
at or before k", the same right-bisect used in a time-based key-value store.

Geometric view
--------------
index 0: [(0,5), (2,6)]        get(0, 1): bisect_right((1,inf)) -> 1, step back -> (0,5) -> 5
index 1: [(0,0)]               get(1, 7): only the seed pair -> 0
index 2: [(0,0), (1,9)]        get(2, 1) -> 9
Each row is a sparse timeline; the columns (snapshots) are never materialised.

Steps
-----
1. hist = [[(0, 0)] for each index]; snap_id = 0.
2. set(i, v): if hist[i][-1][0] == snap_id overwrite that pair; else append (snap_id, v).
3. snap(): snap_id += 1; return snap_id - 1.
4. get(i, k): j = bisect_right(hist[i], (k, inf)); return hist[i][j-1][1].

Complexity: O(1) set and snap, O(log m) get where m is the number of versions of that cell,
            O(length + total sets) space — sorted-by-construction lists plus binary search.
Pitfalls: appending a new pair for repeated sets in the same snapshot (unbounded growth);
          bisecting on (k, 0) instead of (k, inf) (misses a write at exactly k);
          returning snap_id instead of snap_id - 1.
"""
import random
from bisect import bisect_right


class SnapshotArray:
    def __init__(self, length: int):
        self.hist = [[(0, 0)] for _ in range(length)]   # per index: (snap_id, value), ascending
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        h = self.hist[index]
        if h[-1][0] == self.snap_id:
            h[-1] = (self.snap_id, val)       # overwrite: same snapshot, keep one pair
        else:
            h.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        h = self.hist[index]
        i = bisect_right(h, (snap_id, float("inf")))   # first pair written after snap_id
        return h[i - 1][1]


class BruteForce:
    """snap() copies the whole array; O(length) per snap, O(snaps * length) space."""

    def __init__(self, length: int):
        self.cur = [0] * length
        self.snaps = []

    def set(self, index: int, val: int) -> None:
        self.cur[index] = val

    def snap(self) -> int:
        self.snaps.append(self.cur[:])
        return len(self.snaps) - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.snaps[snap_id][index]


if __name__ == "__main__":
    a = SnapshotArray(3)
    a.set(0, 5)
    assert a.snap() == 0
    a.set(0, 6)
    assert a.get(0, 0) == 5
    assert a.snap() == 1
    assert a.get(0, 1) == 6
    assert a.get(2, 1) == 0                    # never-set cell

    e = SnapshotArray(1)                       # edge: several sets inside one snapshot
    e.set(0, 1)
    e.set(0, 2)
    e.set(0, 3)
    assert e.snap() == 0 and e.get(0, 0) == 3 and len(e.hist[0]) == 1

    random.seed(9)
    n = 6
    fast, slow = SnapshotArray(n), BruteForce(n)
    snaps = 0
    for _ in range(2000):
        r = random.random()
        if r < 0.5:
            i, v = random.randrange(n), random.randint(0, 50)
            fast.set(i, v)
            slow.set(i, v)
        elif r < 0.7:
            assert fast.snap() == slow.snap()
            snaps += 1
        elif snaps:
            i, k = random.randrange(n), random.randrange(snaps)
            assert fast.get(i, k) == slow.get(i, k)
    print("ok")
