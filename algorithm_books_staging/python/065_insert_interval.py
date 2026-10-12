"""
Insert Interval - Before, Overlapping, After

Given closed intervals sorted by start and pairwise disjoint, insert one more,
merging it with every interval it overlaps or touches, so the list stays
sorted and disjoint: [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]] with [4, 8]
-> [[1, 2], [3, 10], [12, 16]].
"""


# --- algorithm ---
def insert_interval(intervals, new_interval):
    """Copy what ends before it, absorb what overlaps it, copy the rest.
    One pass and no sort: O(n) time, O(n) space for the output."""
    result = []
    new_start = new_interval[0]
    new_end = new_interval[1]
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < new_start:     # ends before it starts
        result.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new_end:      # overlaps or touches it
        new_start = min(new_start, intervals[i][0])  # the new interval grows
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append([new_start, new_end])              # added exactly once
    while i < n:                                     # starts after it ends
        result.append(intervals[i])
        i += 1
    return result


# --- try it ---
intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
print(insert_interval(intervals, [4, 8]))      # -> [[1, 2], [3, 10], [12, 16]]
print(insert_interval([[1, 3], [6, 9]], [2, 5]))       # -> [[1, 5], [6, 9]]
print(insert_interval([[1, 4]], [4, 6]))               # -> [[1, 6]]
print(insert_interval([[1, 2], [5, 6]], [3, 4]))  # -> [[1, 2], [3, 4], [5, 6]]
print(insert_interval([], [5, 7]))                     # -> [[5, 7]]
