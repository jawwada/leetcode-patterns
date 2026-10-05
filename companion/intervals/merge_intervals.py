"""
Merge Intervals (LeetCode 56) - Medium
Chapter: intervals
Pattern: Sort by start, sweep and merge

Given a list of intervals [start, end], merge all overlapping intervals and return the
non-overlapping intervals that cover the same points. Intervals that merely touch, like [1,4]
and [4,5], count as overlapping.
Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]].
"""


# --- brute force ---
def brute_force(intervals):
    """Keep scanning every pair; fuse the first overlapping pair found and start over. O(n^3)."""
    result = []
    for interval in intervals:
        result.append(interval[:])   # work on copies so the input is left alone
    changed = True
    while changed:
        changed = False
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                a = result[i]
                b = result[j]
                if a[0] <= b[1] and b[0] <= a[1]:    # they overlap or touch
                    result[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    result.pop(j)
                    changed = True
                    break
            if changed:
                break                # the list changed under us: restart the pair scan
    result.sort()
    return result


# --- optimal ---
def merge_intervals(intervals):
    """Sort by start, then sweep once keeping a single running interval. O(n log n) time."""
    intervals.sort()                 # by start (ties broken by end)
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        last = merged[-1]            # the running interval
        if start <= last[1]:         # starts inside the running interval: fuse into it
            last[1] = max(last[1], end)    # max, not end: a nested interval must not shrink it
        else:
            merged.append([start, end])    # a gap: close the running interval, start a new one
    return merged


# --- try the brute force ---
print(brute_force([[1, 3], [2, 6], [8, 10], [15, 18]]))   # -> [[1, 6], [8, 10], [15, 18]]
print(brute_force([[1, 4], [4, 5]]))                      # -> [[1, 5]]
print(brute_force([[1, 4], [2, 3]]))                      # -> [[1, 4]]
print(brute_force([[4, 7], [1, 4], [8, 9], [2, 5]]))      # -> [[1, 7], [8, 9]]


# --- try the optimal ---
print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))   # -> [[1, 6], [8, 10], [15, 18]]
print(merge_intervals([[1, 4], [4, 5]]))                      # -> [[1, 5]]
print(merge_intervals([[1, 4], [2, 3]]))                      # -> [[1, 4]]
print(merge_intervals([[4, 7], [1, 4], [8, 9], [2, 5]]))      # -> [[1, 7], [8, 9]]
