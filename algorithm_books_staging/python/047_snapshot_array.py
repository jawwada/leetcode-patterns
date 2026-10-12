"""
Snapshot Array - Per-Index History + Binary Search

An array of zeros with set(index, val), snap() that takes a snapshot and
returns its id (0, 1, 2, ...), and get(index, snap_id), the value at index in
that snapshot: set(0, 5), snap() -> 0, then set(0, 6); get(0, 0) -> 5.
"""


# --- algorithm ---
class SnapshotArray:
    """Each index keeps its own history of (snap_id, value) pairs."""

    def __init__(self, length):
        self.history = []                   # index -> list of (snap_id, value)
        for i in range(length):
            self.history.append([])
        self.snap_id = 0                    # the id the next snap() returns

    def set(self, index, val):
        """Record val under the open snap id, rewriting a pair written since
        the last snap. O(1)."""
        pairs = self.history[index]
        last = len(pairs) - 1               # the newest pair, if any
        if last >= 0 and pairs[last][0] == self.snap_id:
            pairs[last] = (self.snap_id, val)   # same snapshot: rewrite it
        else:
            pairs.append((self.snap_id, val))

    def snap(self):
        """Close the open snapshot and return its id. O(1)."""
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        """The last pair at or before snap_id, by binary search. O(log w)."""
        pairs = self.history[index]
        left = 0
        right = len(pairs)
        while left < right:                 # find the first pair after snap_id
            mid = (left + right) // 2
            if pairs[mid][0] <= snap_id:
                left = mid + 1              # mid was written by then
            else:
                right = mid                 # mid is later: maybe the first
        if left == 0:
            return 0                        # not written by that snapshot
        return pairs[left - 1][1]


# --- try it ---
array = SnapshotArray(3)
array.set(0, 5)
print(array.snap())                         # -> 0
array.set(0, 6)
array.set(1, 4)
array.set(0, 8)                             # rewrites the 6: same snapshot
print(array.get(0, 0), array.history[0])    # -> 5 [(0, 5), (1, 8)]
print(array.snap(), array.snap())           # -> 1 2
array.set(1, 9)
print(array.snap(), array.history[1])       # -> 3 [(1, 4), (3, 9)]
print(array.get(0, 2), array.get(1, 2), array.get(1, 0))    # -> 8 4 0
print(array.get(1, 3), array.get(2, 3))     # -> 9 0
