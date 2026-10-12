"""
Interval List Intersections - Two Pointers over Two Sorted Lists

Given two lists of closed intervals, each sorted and pairwise disjoint, return
the intersection of the two lists: [[0, 2], [5, 10], [13, 23], [24, 25]] and
[[1, 5], [8, 12], [15, 24], [25, 26]] ->
[[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]].
"""


# --- algorithm ---
def interval_intersection(first, second):
    """Overlap of the two current intervals is [later start, earlier end];
    then drop whichever ends first. O(m + n) time, O(1) extra space."""
    result = []
    i = 0
    j = 0
    while i < len(first) and j < len(second):
        first_start, first_end = first[i]
        second_start, second_end = second[j]
        overlap_start = max(first_start, second_start)  # the later start
        overlap_end = min(first_end, second_end)        # the earlier end
        if overlap_start <= overlap_end:
            result.append([overlap_start, overlap_end])     # a point counts too
        if first_end < second_end:
            i += 1                  # first[i] can meet nothing further on
        else:
            j += 1                  # second[j] can meet nothing further on
    return result


# --- try it ---
first = [[0, 2], [5, 10], [13, 23], [24, 25]]
second = [[1, 5], [8, 12], [15, 24], [25, 26]]
result = interval_intersection(first, second)
print(result[0:3])                  # -> [[1, 2], [5, 5], [8, 10]]
print(result[3:6])                  # -> [[15, 23], [24, 24], [25, 25]]
print(interval_intersection([[0, 10]], [[1, 2], [3, 4]]))  # -> [[1, 2], [3, 4]]
print(interval_intersection([[1, 3], [5, 9]], []))         # -> []
print(interval_intersection([[1, 7]], [[3, 10]]))          # -> [[3, 7]]
