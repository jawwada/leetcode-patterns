"""
Interval Scheduling - Sort by End, Keep What Fits

Keep as many intervals [start, end] as possible with no two overlapping (ends
that only touch, like [1, 3] and [3, 5], are fine); the fewest removals is the
rest: [[1, 3], [2, 4], [3, 5], [1, 8], [6, 7]] -> keep 3, remove 2.
"""
import math                         # math.inf


# --- algorithm ---
def max_non_overlapping(intervals):
    """Sort by end, keep whatever fits after the last kept end. O(n log n)."""
    by_end = []
    for start, end in intervals:
        by_end.append((end, start))     # end first: the sort orders by end
    by_end.sort()
    kept = 0
    last_end = -math.inf            # end of the last kept interval
    for end, start in by_end:
        if start >= last_end:       # fits after the last kept one
            kept += 1
            last_end = end
    return kept


def min_removals(intervals):
    """Remove everything the greedy did not keep (LC 435). O(n log n)."""
    return len(intervals) - max_non_overlapping(intervals)


# --- try it ---
intervals = [[1, 3], [2, 4], [3, 5], [1, 8], [6, 7]]
print(max_non_overlapping(intervals))           # -> 3
print(min_removals(intervals))                  # -> 2
print(min_removals([[1, 2], [1, 2], [1, 2]]))   # -> 2
print(max_non_overlapping([]))                  # -> 0
