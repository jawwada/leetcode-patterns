"""
Insert Interval (LeetCode 57) - Medium
Chapter: intervals
Pattern: Sort by start, sweep and merge

intervals is sorted by start and pairwise non-overlapping. Insert newInterval, merging where
necessary, and return the list still sorted and non-overlapping.
Example: [[1,3],[6,9]] with new [2,5] -> [[1,5],[6,9]];
[[1,2],[3,5],[6,7],[8,10],[12,16]] with new [4,8] -> [[1,2],[3,10],[12,16]].
"""


# --- brute force ---
def brute_force(intervals, new_interval):
    """Ignore the sorted input: add the new one, sort, merge as in Merge Intervals. O(n log n)"""
    all_intervals = []
    for interval in intervals:
        all_intervals.append(interval[:])
    all_intervals.append(new_interval[:])
    all_intervals.sort()             # the wasted step: the input was already sorted
    merged = [all_intervals[0]]
    for start, end in all_intervals[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged


# --- optimal ---
def insert_interval(intervals, new_interval):
    """Three phases in one pass: copy the left part, absorb the overlaps, copy the rest. O(n)"""
    start = new_interval[0]
    end = new_interval[1]
    result = []
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < start:     # phase 1: ends before the new one begins
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:      # phase 2: overlaps, swallow it into [start, end]
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])                  # the grown new interval goes in exactly once
    while i < n:                                 # phase 3: starts after the new one ends
        result.append(intervals[i])
        i += 1
    return result


# --- try the brute force ---
print(brute_force([[1, 3], [6, 9]], [2, 5]))                # -> [[1, 5], [6, 9]]
print(brute_force([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))
# -> [[1, 2], [3, 10], [12, 16]]
print(brute_force([], [5, 7]))                              # -> [[5, 7]]
print(brute_force([[3, 5], [12, 15]], [6, 6]))              # -> [[3,5],[6,6],[12,15]]


# --- try the optimal ---
print(insert_interval([[1, 3], [6, 9]], [2, 5]))            # -> [[1, 5], [6, 9]]
print(insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))
# -> [[1, 2], [3, 10], [12, 16]]
print(insert_interval([], [5, 7]))                          # -> [[5, 7]]
print(insert_interval([[3, 5], [12, 15]], [6, 6]))          # -> [[3,5],[6,6],[12,15]]
