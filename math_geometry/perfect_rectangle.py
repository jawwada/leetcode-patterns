"""
Perfect Rectangle (LeetCode 391)  — Hard
Pattern: Corner parity + area invariant

Problem
-------
Given n axis-aligned rectangles [x1, y1, x2, y2], return True iff together they form an exact
cover of some rectangle: no gaps and no overlaps.
Example: [[1,1,3,3],[3,1,4,2],[3,2,4,4],[1,3,2,4],[2,3,3,4]] -> True (they tile the 3x3 square
[1,1,4,4]). [[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]] -> False (a gap in the middle).

Brute force
-----------
Compare every pair of rectangles for a positive-area overlap, and check that the areas sum to the
area of the bounding box. No overlap + areas add up exactly => every point of the box is covered
exactly once. O(n^2) time, O(1) space. The wasted work is the pairwise overlap test: most pairs
are nowhere near each other, yet every pair is examined.

From brute force to optimal
---------------------------
The O(n^2) term exists only to rule out overlaps; the area sum already rules out "gap without a
compensating overlap". Observation about corners: in a perfect tiling every corner point is
shared by exactly 2 or 4 rectangles EXCEPT the four corners of the bounding box, which belong to
exactly one rectangle each. So if we toggle each rectangle's four corners in a set (add if absent,
remove if present), only points touched an odd number of times survive, and a valid tiling leaves
exactly the four bounding-box corners. That is a single O(n) pass with a hash set. Neither test
alone is sufficient: two copies of [0,0,1,1] plus [0,0,2,2] pass the corner test (the duplicate
corners cancel) but have area 6 != 4; and a gap balanced by an overlap elsewhere passes the area
test but leaves stray corners. Together they are a complete characterisation.

Intuition
---------
Think of each rectangle corner as a light switch. Interior meeting points are flipped an even
number of times (two rectangles meet along an edge, four at a cross) and end up off. Only the
four outer corners are flipped once. Any gap or overlap creates a corner that is not matched
and leaves an extra light on. The area check closes the one loophole where cancellation hides
an overlap.

Geometric view
--------------
Lay the rectangles on graph paper. Where two tiles meet edge to edge, their shared corners sit on
top of each other in pairs; where four tiles meet, in a group of four. Pair them off and they all
disappear, leaving just the four corners of the outline. A missing tile or a doubled tile breaks
the pairing somewhere and that point sticks out.

Steps
-----
1. Track min_x, min_y, max_x, max_y and the total area while scanning.
2. For each rectangle toggle its four corners in a set (symmetric difference).
3. After the scan the set must be exactly the four corners of the bounding box.
4. The summed area must equal (max_x - min_x) * (max_y - min_y).
5. Both conditions hold -> True.

Complexity: O(n) time, O(n) space — one pass, at most 4n corner toggles in a hash set.
Pitfalls: checking only corner parity (duplicate rectangles can cancel out) or only area (gap
          plus overlap can balance); comparing len(corners) == 4 without checking they are the
          bounding-box corners; using closed-interval overlap tests that flag touching edges.
"""
from typing import List


class Solution:
    def isRectangleCover(self, rectangles: List[List[int]]) -> bool:
        corners = set()
        area = 0
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")
        for x1, y1, x2, y2 in rectangles:
            area += (x2 - x1) * (y2 - y1)
            min_x, min_y = min(min_x, x1), min(min_y, y1)
            max_x, max_y = max(max_x, x2), max(max_y, y2)
            for p in ((x1, y1), (x1, y2), (x2, y1), (x2, y2)):
                corners ^= {p}                       # toggle: interior corners cancel in pairs
        outline = {(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)}
        return corners == outline and area == (max_x - min_x) * (max_y - min_y)


def brute_force(rectangles: List[List[int]]) -> bool:
    """Pairwise overlap test + total-area check. O(n^2)."""
    for i, (ax1, ay1, ax2, ay2) in enumerate(rectangles):
        for bx1, by1, bx2, by2 in rectangles[i + 1:]:
            if ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2:   # positive-area overlap
                return False
    min_x = min(r[0] for r in rectangles)
    min_y = min(r[1] for r in rectangles)
    max_x = max(r[2] for r in rectangles)
    max_y = max(r[3] for r in rectangles)
    area = sum((x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in rectangles)
    return area == (max_x - min_x) * (max_y - min_y)


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        ([[1, 1, 3, 3], [3, 1, 4, 2], [3, 2, 4, 4], [1, 3, 2, 4], [2, 3, 3, 4]], True),
        ([[1, 1, 2, 3], [1, 3, 2, 4], [3, 1, 4, 2], [3, 2, 4, 4]], False),      # gap
        ([[1, 1, 3, 3], [3, 1, 4, 2], [1, 3, 2, 4], [2, 2, 4, 4]], False),      # overlap
        ([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2]], False),   # corners cancel, area wrong
        ([[0, 0, 4, 1]], True),                                # edge: a single rectangle
    ]
    for rects, want in cases:
        assert s.isRectangleCover(rects) is want, rects
        assert brute_force(rects) is want, rects

    random.seed(391)
    for _ in range(400):
        # random tiling of a grid by rows of random column cuts, then maybe perturb it
        w, h = random.randint(1, 4), random.randint(1, 4)
        rects = []
        for y in range(h):
            x = 0
            while x < w:
                nx = random.randint(x + 1, w)
                rects.append([x, y, nx, y + 1])
                x = nx
        if random.random() < 0.5:
            r = random.choice(rects)
            if random.random() < 0.5:
                rects.remove(r)                       # gap
            else:
                rects.append(r[:])                    # overlap
        if rects:
            random.shuffle(rects)
            assert s.isRectangleCover(rects) == brute_force(rects), rects
    print("ok")
