"""
Max Points on a Line (LeetCode 149)  — Hard
Pattern: Anchor point + slope as a reduced fraction

Problem
-------
Given n distinct points on the plane, return the maximum number of points that lie on one
straight line (n <= 300, coordinates up to 10^4 in absolute value).
Example: [[1,1],[2,2],[3,3]] -> 3.
Example: [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]] -> 4  (the line through (1,4),(2,3),(3,2),(4,1)).

Brute force
-----------
A line is fixed by two points, so for every pair (i, j) count the points k that are collinear
with it (cross product (xj-xi)(yk-yi) - (yj-yi)(xk-xi) == 0) and take the maximum. O(n^3) time,
O(1) space — 2.7*10^7 cross products at n = 300, borderline but exact. The waste: the same line
is rediscovered once per pair of points on it, so a line with c points is counted c(c-1)/2
times, each time with a full O(n) scan.

From brute force to optimal
---------------------------
The redundancy is re-identifying the same line through an anchor for every second point. Fix an
anchor i: every other point j defines a direction (dx, dy) from i, and all points sharing that
direction lie on one line through i. Two directions are the same iff they are equal as REDUCED
fractions, so normalise (dx, dy) by their gcd and a sign convention (dx > 0, or dx == 0 and
dy > 0) and use the pair as a hash key. One pass over j fills a counter; the best line through i
has max(counter) + 1 points. Repeating for every anchor costs O(n^2) and visits each line once
per anchor on it instead of once per pair, cutting a factor of n. Reduced fractions avoid the
precision problems of floating slopes (e.g. 1/3 vs 2/6) and handle vertical lines (dx = 0)
without a special case.

Intuition
---------
"Max points on a line" = "max points sharing a direction from some anchor". Directions are
exactly what a hash map can group, provided the key is canonical. gcd reduction plus a sign
rule is the canonical form for a rational slope.

Geometric view
--------------
Stand at the anchor and look outward: each other point sits on a ray, and collinear points sit
on the same ray or on the opposite ray (the sign normalisation folds both onto one key). The
counter is a histogram over directions; its tallest bar plus the anchor itself is the best line
through this anchor. Sweep the anchor over all points.

Steps
-----
1. For each anchor i: slopes = Counter().
2. For each j != i: dx, dy = xj - xi, yj - yi; g = gcd(dx, dy); dx //= g; dy //= g.
3. If dx < 0 or (dx == 0 and dy < 0): negate both (canonical sign).
4. slopes[(dx, dy)] += 1; best = max(best, max(slopes.values()) + 1).
5. Return best (1 when n == 1).

Complexity: O(n^2 log C) time (gcd per pair), O(n) space per anchor.
Pitfalls: floating-point slopes (0.1 + 0.2 problems and infinite slope); forgetting to
normalise the sign so (1,2) and (-1,-2) collide; off-by-one forgetting to add the anchor itself.
"""
import random
from collections import Counter
from math import gcd
from typing import List


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        best = 1
        for i in range(n):
            slopes = Counter()                       # canonical direction -> points on it
            xi, yi = points[i]
            for j in range(i + 1, n):                # j < i were counted with j as anchor
                dx, dy = points[j][0] - xi, points[j][1] - yi
                g = gcd(dx, dy)                      # > 0 since points are distinct
                dx, dy = dx // g, dy // g
                if dx < 0 or (dx == 0 and dy < 0):   # one sign per line direction
                    dx, dy = -dx, -dy
                slopes[(dx, dy)] += 1
            if slopes:
                best = max(best, max(slopes.values()) + 1)   # +1 for the anchor itself
        return best


def brute_force(points: List[List[int]]) -> int:
    n = len(points)
    best = min(n, 2)
    for i in range(n):
        for j in range(i + 1, n):                    # the line through i and j
            (xi, yi), (xj, yj) = points[i], points[j]
            on_line = sum(1 for xk, yk in points
                          if (xj - xi) * (yk - yi) - (yj - yi) * (xk - xi) == 0)
            best = max(best, on_line)                # same line recounted per pair on it
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.maxPoints([[1, 1], [2, 2], [3, 3]]) == 3
    assert s.maxPoints([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4
    assert s.maxPoints([[0, 0]]) == 1                                  # single point
    assert s.maxPoints([[0, 0], [1, 0], [2, 0], [0, 1]]) == 3           # horizontal line
    assert s.maxPoints([[0, 0], [0, 1], [0, -1], [1, 5]]) == 3          # vertical line
    assert s.maxPoints([[0, 0], [1, 3], [2, 6], [-1, -3], [5, 1]]) == 4 # both sides of anchor
    rng = random.Random(149)
    for _ in range(150):
        pts = list({(rng.randint(-4, 4), rng.randint(-4, 4)) for _ in range(rng.randint(1, 9))})
        pts = [list(p) for p in pts]
        assert s.maxPoints(pts) == brute_force(pts), pts
    print("ok")
