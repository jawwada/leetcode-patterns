"""
Non-overlapping Intervals (LeetCode 435) - Medium
Chapter: intervals
Pattern: Greedy by earliest end (interval scheduling)

Given intervals [start, end], return the minimum number of intervals to remove so that the
remaining ones are pairwise non-overlapping. Touching intervals such as [1,2] and [2,3] do not
overlap.
Example: [[1,2],[2,3],[3,4],[1,3]] -> 1 (remove [1,3]); [[1,2],[1,2],[1,2]] -> 2.
"""
import math                        # math.inf


# --- brute force ---
def brute_force(intervals):
    """Try every subset, keep the biggest with no overlaps; the rest are removed. O(2^n n^2)."""
    n = len(intervals)
    best = 0
    for mask in range(1 << n):       # bit i of mask says whether interval i is kept
        chosen = []
        for i in range(n):
            if (mask >> i) & 1 == 1:
                chosen.append(intervals[i])
        ok = True
        for i in range(len(chosen)):
            for j in range(i + 1, len(chosen)):
                a = chosen[i]
                b = chosen[j]
                if a[0] < b[1] and b[0] < a[1]:      # strict: touching intervals do not overlap
                    ok = False
        if ok:
            best = max(best, len(chosen))
    return n - best


# --- optimal ---
def non_overlapping_intervals(intervals):
    """Sort by end; keep every interval that starts at or after the last kept end. O(n log n)."""
    by_end = []
    for start, end in intervals:
        by_end.append((end, start))  # end first, so a plain sort orders by end
    by_end.sort()
    removed = 0
    last_end = -math.inf
    for end, start in by_end:
        if start >= last_end:        # keep it: it begins after the last kept one finishes
            last_end = end
        else:
            removed += 1             # overlaps a kept interval that ends no later: drop this one
    return removed


# --- try the brute force ---
print(brute_force([[1, 2], [2, 3], [3, 4], [1, 3]]))           # -> 1
print(brute_force([[1, 2], [1, 2], [1, 2]]))                   # -> 2
print(brute_force([[1, 2], [2, 3]]))                           # -> 0
print(brute_force([[1, 100], [11, 22], [1, 11], [2, 12]]))     # -> 2


# --- try the optimal ---
print(non_overlapping_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))           # -> 1
print(non_overlapping_intervals([[1, 2], [1, 2], [1, 2]]))                   # -> 2
print(non_overlapping_intervals([[1, 2], [2, 3]]))                           # -> 0
print(non_overlapping_intervals([[1, 100], [11, 22], [1, 11], [2, 12]]))     # -> 2
