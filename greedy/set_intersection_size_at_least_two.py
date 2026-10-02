"""
Set Intersection Size At Least Two (LeetCode 757)  — Hard
Pattern: Greedy by earliest end (interval scheduling)

Problem
-------
Given closed integer intervals [start, end], find the smallest set of integers S such that every
interval contains at least TWO elements of S. Return |S|.
Example: [[1,3],[3,7],[8,9]] -> 5 (S = {2,3,4,8,9}).
[[1,3],[1,4],[2,5],[3,5]] -> 3 (S = {2,3,5}).

Brute force
-----------
Let P be all integer points from the smallest start to the largest end. Try every subset of P in
increasing size and check that each interval contains at least two chosen points. Exponential in
the coordinate range, O(n) space per check. The wasted work: the subsets never use the fact that
when an interval forces a choice, the best points to pick are the ones furthest to the right, so
that they also serve as many later intervals as possible.

From brute force to optimal
---------------------------
Interval scheduling logic, doubled. Sort intervals by end ascending; ties by start DESCENDING so
that among intervals sharing an end the widest ones come later and are already satisfied by the
points chosen for the narrower ones (otherwise the narrow one could be left with one point). Walk
the sorted list keeping only the two largest chosen points a < b. For interval [s, e]: if s > b
neither chosen point is inside, so it needs two new points, and the best are e-1 and e (rightmost
possible, so they overlap the most future intervals, which all end at >= e). If a < s <= b only b
is inside, so add one point, e. Otherwise both are inside and nothing is needed. The invariant
"a and b are the two largest chosen points, and every processed interval has two chosen points"
is all the state needed: O(n log n) for the sort, O(1) extra space.

Intuition
---------
Process intervals by deadline (end). When an interval is short of points, add them as far right
as possible: a point at e helps every later interval that starts at or before e, and a point
further left helps a subset of those. Only the two most recent points can matter for later
intervals because later intervals end further right.

Geometric view
--------------
Intervals stacked and sorted by their right edge. Two markers a and b sit on the number line at
the two rightmost chosen points. For each interval in order, look at whether its left edge is
right of both markers (need 2), between them (need 1), or left of both (need 0). New markers
always land on the interval's right edge, pushing a and b to the right.

Steps
-----
1. Sort by (end ascending, start descending).
2. a = b = -1 (no points yet), count = 0.
3. For each [s, e]: if s > b: choose e-1 and e; a, b = e-1, e; count += 2.
4.   elif s > a: choose e; a, b = b, e; count += 1.
5. Return count.

Complexity: O(n log n) time, O(1) extra space — one sort, one pass with two integers.
Pitfalls: breaking end-ties by start ASCENDING: with chosen points {0,1} and then [1,5],[3,5],
          the wide one grabs 5 and the narrow one grabs 5 again (a duplicate), so
          [[0,1],[1,5],[3,5],[5,6]] returns 4 instead of 5; choosing e and e+1 or s and s+1
          instead of e-1 and e; using >= instead of > (endpoints are inclusive).
"""
from itertools import combinations
from typing import List


class Solution:
    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda iv: (iv[1], -iv[0]))   # end asc, start desc
        a = b = -1                   # two largest chosen points so far, a < b
        count = 0
        for s, e in intervals:
            if s > b:                # neither chosen point inside -> take e-1, e
                a, b = e - 1, e
                count += 2
            elif s > a:              # only b inside -> add e
                a, b = b, e
                count += 1
        return count


def brute_force(intervals: List[List[int]]) -> int:
    """Try every subset of candidate points by increasing size (exponential)."""
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    points = range(lo, hi + 1)
    for size in range(2, len(points) + 1):
        for chosen in combinations(points, size):
            if all(sum(s <= p <= e for p in chosen) >= 2 for s, e in intervals):
                return size
    return -1   # unreachable: every interval has length >= 1 so all points always work


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([[1, 3], [3, 7], [8, 9]], 5),
        ([[1, 3], [1, 4], [2, 5], [3, 5]], 3),
        ([[1, 2], [2, 3], [2, 4], [4, 5]], 5),
        ([[4, 9]], 2),                                  # edge: single interval
        ([[1, 2], [1, 3]], 2),                          # edge: tie on start, nested ends
        ([[0, 1], [1, 5], [3, 5], [5, 6]], 5),          # edge: end tie must go start-desc
    ]
    for ivs, want in cases:
        assert s.intersectionSizeTwo([iv[:] for iv in ivs]) == want, ivs
        assert brute_force([iv[:] for iv in ivs]) == want, ivs

    random.seed(757)
    for _ in range(200):
        ivs = []
        for _ in range(random.randint(1, 6)):
            a = random.randint(0, 7)
            ivs.append([a, random.randint(a + 1, 9)])
        assert s.intersectionSizeTwo([iv[:] for iv in ivs]) == brute_force(ivs), ivs
    print("ok")
