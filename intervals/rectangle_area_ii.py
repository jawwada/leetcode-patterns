"""
Rectangle Area II (LeetCode 850)  — Hard
Pattern: Sweep line over sorted events

Problem
-------
Given n axis-aligned rectangles [x1, y1, x2, y2] with coordinates up to 1e9, return the total
area covered by their union, modulo 1e9+7. Overlapping regions count once.
Example: [[0,0,2,2],[1,0,2,3],[1,0,3,1]] -> 6 (the 2x2 square, plus the 1x1 cell above it, plus
the 1x1 cell to its right).

Brute force
-----------
Painting unit cells is hopeless at 1e9 coordinates, so compress first: the distinct x's and y's
cut the plane into at most (2n-1)^2 cells, and every rectangle covers a whole block of them.
Paint each rectangle's cells into a boolean grid, then sum the true areas of painted cells.
O(n^3) time (n rectangles x O(n^2) cells each), O(n^2) space. The wasted work: a rectangle is
painted cell by cell even though within one vertical strip it covers a single contiguous
y-interval that we could handle as one object.

From brute force to optimal
---------------------------
First reduction: coverage only changes at rectangle edges, so sweep a vertical line left to
right through the 2n sorted x-events (x1 = rectangle enters, x2 = rectangle leaves). Between two
consecutive events the set of active rectangles is fixed, so the covered area of that strip is
(width) x (length of the union of the active y-intervals). Second reduction: that union length is
the classic merge-sorted-intervals routine, O(k log k) for k active rectangles, instead of
O(n^2) painting per strip. Total O(n^2 log n) with O(n) extra space, and no grid at all. The
remaining per-strip re-sort is the only slack left; a segment tree over compressed y's with
cover counts brings it to O(n log n), which interviewers accept as the follow-up.

Intuition
---------
Area is an integral: slide a vertical line across the plane and add up (how much of the line is
covered) x (how far the line moved). The covered length is piecewise constant, changing only at
rectangle edges, so you only need to evaluate it 2n times, once per event.

Geometric view
--------------
A vertical line sweeps rightwards. Each rectangle switches on when the line reaches x1 and off at
x2. Between consecutive switch points the line carries a fixed set of y-intervals; project them
onto the y-axis, merge overlaps, and that merged length times the horizontal distance to the next
switch point is one slab of the union's area.

Steps
-----
1. For each rectangle emit (x1, +1, y1, y2) and (x2, -1, y1, y2); sort events by x.
2. active = list of y-intervals currently cut by the sweep line; area = 0; prev_x = first x.
3. For each event at x: area += (x - prev_x) * covered(active); prev_x = x.
4. Add or remove the event's y-interval from active.
5. covered(active): sort by start, merge, sum lengths (clip each start to the running end).
6. Return area mod 1e9+7.

Complexity: O(n^2 log n) time, O(n) space — 2n events, each re-merging up to n active
            y-intervals in O(n log n).
Pitfalls: computing the strip area AFTER applying the event instead of before (the strip to the
          left of x uses the old active set); using an inclusive compressed-cell count instead of
          actual coordinate differences; forgetting the modulo on the final sum only (intermediate
          Python ints are fine, but in other languages overflow appears at 1e18).
"""
from itertools import pairwise
from typing import List


class Solution:
    def rectangleArea(self, rectangles: List[List[int]]) -> int:
        MOD = 10**9 + 7
        events = []
        for x1, y1, x2, y2 in rectangles:
            events.append((x1, 1, y1, y2))          # rectangle enters the sweep line
            events.append((x2, -1, y1, y2))         # rectangle leaves it
        events.sort()

        active: List[tuple] = []                    # y-intervals cut by the line right now
        area, prev_x = 0, events[0][0]
        for x, kind, y1, y2 in events:
            area += (x - prev_x) * self._covered(active)   # slab left of x uses the OLD set
            prev_x = x
            if kind == 1:
                active.append((y1, y2))
            else:
                active.remove((y1, y2))
        return area % MOD

    @staticmethod
    def _covered(intervals: List[tuple]) -> int:
        """Length of the union of y-intervals: sort by start, merge, sum."""
        total, reach = 0, float("-inf")
        for s, e in sorted(intervals):
            s = max(s, reach)                       # clip away the part already counted
            if e > s:
                total += e - s
                reach = e
        return total


def brute_force(rectangles: List[List[int]]) -> int:
    """Compress coordinates, paint every cell of every rectangle, sum painted cells. O(n^3)."""
    xs = sorted({x for x1, _, x2, _ in rectangles for x in (x1, x2)})
    ys = sorted({y for _, y1, _, y2 in rectangles for y in (y1, y2)})
    xi = {x: i for i, x in enumerate(xs)}
    yi = {y: i for i, y in enumerate(ys)}
    painted = [[False] * (len(ys) - 1) for _ in range(len(xs) - 1)]
    for x1, y1, x2, y2 in rectangles:
        for i in range(xi[x1], xi[x2]):
            for j in range(yi[y1], yi[y2]):
                painted[i][j] = True
    area = 0
    for i, (xa, xb) in enumerate(pairwise(xs)):
        for j, (ya, yb) in enumerate(pairwise(ys)):
            if painted[i][j]:
                area += (xb - xa) * (yb - ya)
    return area % (10**9 + 7)


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]], 6),
        ([[0, 0, 1000000000, 1000000000]], 49),               # 1e18 mod 1e9+7
        ([[0, 0, 3, 3], [1, 1, 2, 2]], 9),                    # fully nested
        ([[0, 0, 1, 1], [0, 0, 1, 1]], 1),                    # identical duplicates
        ([[0, 0, 1, 1], [2, 2, 3, 3]], 2),                    # disjoint
    ]
    for rects, want in cases:
        assert s.rectangleArea([r[:] for r in rects]) == want, rects
        assert brute_force([r[:] for r in rects]) == want, rects

    random.seed(850)
    for _ in range(300):
        rects = []
        for _ in range(random.randint(1, 8)):
            x1, x2 = sorted(random.sample(range(0, 12), 2))
            y1, y2 = sorted(random.sample(range(0, 12), 2))
            rects.append([x1, y1, x2, y2])
        assert s.rectangleArea(rects) == brute_force(rects), rects
    print("ok")
