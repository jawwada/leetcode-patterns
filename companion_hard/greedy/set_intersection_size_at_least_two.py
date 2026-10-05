"""
Set Intersection Size At Least Two (LeetCode 757) - Hard
Chapter: greedy
Pattern: Greedy by earliest end (interval scheduling)

Given closed integer intervals [start, end], find the smallest set of integers S such that every
interval contains at least two elements of S; return the size of S.
Example: [[1,3],[3,7],[8,9]] -> 5 (S = {2,3,4,8,9}); [[1,3],[1,4],[2,5],[3,5]] -> 3 (S = {2,3,5}).
"""
from itertools import combinations   # every subset of a given size


# --- brute force ---
def brute_force(intervals):
    """Try every subset of the integer points by increasing size until each interval holds two."""
    lowest = intervals[0][0]
    highest = intervals[0][1]
    for start, end in intervals:
        lowest = min(lowest, start)
        highest = max(highest, end)
    points = list(range(lowest, highest + 1))
    for size in range(2, len(points) + 1):
        for chosen in combinations(points, size):
            if every_interval_has_two(intervals, chosen):
                return size
    return -1                                     # never reached: all the points always work


def every_interval_has_two(intervals, chosen):
    for start, end in intervals:
        inside = 0
        for p in chosen:
            if start <= p <= end:
                inside += 1
        if inside < 2:
            return False
    return True


# --- optimal ---
def set_intersection_size_at_least_two(intervals):
    """Sort by end (ties: wider first); keep the two largest picks, add rightmost. O(n log n)"""
    order = []
    for start, end in intervals:
        order.append((end, -start))
    order.sort()                                  # end ascending, then start descending
    a = -1                                        # the two largest chosen points so far, a < b
    b = -1
    count = 0
    for end, neg_start in order:
        start = -neg_start
        if start > b:                             # neither chosen point inside: take end - 1, end
            a = end - 1
            b = end
            count += 2
        elif start > a:                           # only b is inside: add end
            a = b
            b = end
            count += 1
    return count


# --- try the brute force ---
print(brute_force([[1, 3], [3, 7], [8, 9]]))              # -> 5
print(brute_force([[1, 3], [1, 4], [2, 5], [3, 5]]))      # -> 3
print(brute_force([[1, 2], [2, 3], [2, 4], [4, 5]]))      # -> 5
print(brute_force([[0, 1], [1, 5], [3, 5], [5, 6]]))      # -> 5


# --- try the optimal ---
print(set_intersection_size_at_least_two([[1, 3], [3, 7], [8, 9]]))              # -> 5
print(set_intersection_size_at_least_two([[1, 3], [1, 4], [2, 5], [3, 5]]))      # -> 3
print(set_intersection_size_at_least_two([[1, 2], [2, 3], [2, 4], [4, 5]]))      # -> 5
print(set_intersection_size_at_least_two([[0, 1], [1, 5], [3, 5], [5, 6]]))      # -> 5
