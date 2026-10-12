"""
Range Module - A Sorted List of Disjoint Intervals

Track half-open ranges [left, right), left < right: add_range marks a range,
remove_range unmarks it and query_range asks whether all of [left, right) is
tracked. add_range(10, 20), remove_range(14, 16), then query_range(10, 14),
query_range(13, 15), query_range(16, 17) -> True, False, True.
"""


# --- algorithm ---
class RangeModule:
    """Sorted, disjoint, non-touching [start, end) pairs. Updates O(n),
    queries O(log n)."""

    def __init__(self):
        self.intervals = []         # sorted [start, end), gaps between

    def add_range(self, left, right):
        """Copy the intervals before, absorb every one that overlaps or
        touches [left, right), copy the rest. O(n)."""
        merged = []
        i = 0
        n = len(self.intervals)
        while i < n and self.intervals[i][1] < left:    # ends before: keep
            merged.append(self.intervals[i])
            i += 1
        while i < n and self.intervals[i][0] <= right:  # overlaps or touches
            left = min(left, self.intervals[i][0])
            right = max(right, self.intervals[i][1])
            i += 1
        merged.append([left, right])
        while i < n:                                    # starts after: keep
            merged.append(self.intervals[i])
            i += 1
        self.intervals = merged

    def remove_range(self, left, right):
        """Keep what lies outside [left, right); a cut interval leaves one
        or two pieces. O(n)."""
        kept = []
        for start, end in self.intervals:
            if end <= left or start >= right:
                kept.append([start, end])       # no overlap: untouched
            else:
                if start < left:
                    kept.append([start, left])  # the piece on the left
                if end > right:
                    kept.append([right, end])   # the piece on the right
        self.intervals = kept

    def query_range(self, left, right):
        """Find the last interval starting at or before left; it must reach
        right. O(log n)."""
        lo = 0
        hi = len(self.intervals)
        while lo < hi:                  # first interval starting after left
            mid = (lo + hi) // 2
            if self.intervals[mid][0] <= left:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return False                # every interval starts after left
        return self.intervals[lo - 1][1] >= right


# --- try it ---
module = RangeModule()
module.add_range(10, 20)
module.remove_range(14, 16)
print(module.intervals)                             # -> [[10, 14], [16, 20]]
print(module.query_range(10, 14), module.query_range(13, 15))  # -> True False
print(module.query_range(16, 17))                   # -> True
module.add_range(14, 16)            # touches both pieces: one block again
print(module.intervals, module.query_range(10, 20))  # -> [[10, 20]] True
module.add_range(25, 30)
module.add_range(5, 8)
print(module.intervals)             # -> [[5, 8], [10, 20], [25, 30]]
print(module.query_range(8, 10), module.query_range(26, 29))  # -> False True
