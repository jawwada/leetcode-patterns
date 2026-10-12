"""
Merge Intervals - Sort by Start, Sweep and Extend

Given closed intervals [start, end] in any order, merge every group that
overlaps or touches and return the result sorted by start:
[[1, 3], [8, 12], [2, 6], [9, 10], [12, 14]] -> [[1, 6], [8, 14]].
"""


# --- algorithm ---
def merge_intervals(intervals):
    """Sort by start; stretch the last merged interval or open a new one.
    O(n log n) time for the sort, O(n) space for the output."""
    merged = []
    for start, end in sorted(intervals):    # pairs sort by start first
        if len(merged) > 0 and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # overlap: stretch it
        else:
            merged.append([start, end])     # a gap: a new interval begins
    return merged


# --- try it ---
intervals = [[1, 3], [8, 12], [2, 6], [9, 10], [12, 14]]
print(merge_intervals(intervals))           # -> [[1, 6], [8, 14]]
print(merge_intervals([[1, 4], [4, 5]]))    # -> [[1, 5]]
print(merge_intervals([[1, 4], [5, 6]]))    # -> [[1, 4], [5, 6]]
print(merge_intervals([]))                  # -> []
