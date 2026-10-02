"""
The Skyline Problem (LeetCode 218)  — Hard
Pattern: Sweep line over events + max-heap with lazy removal

Problem
-------
Buildings are given as [left, right, height] rectangles on a shared ground line. Return the
skyline as a list of key points [x, y] where the outline's height changes, sorted by x and
ending with a point of height 0; consecutive points must not share a height.
Example: [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]] ->
[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]].

Brute force
-----------
The outline can only change at a building edge. Collect all distinct left/right x values,
sort them, and at each x compute the tallest building with left <= x < right by scanning all
n buildings; emit [x, height] whenever that height differs from the previous one. O(n^2) time,
O(n) space. The waste: at each of the 2n edges the full set of buildings is rescanned to find
the max, although between consecutive edges only one building was added or removed.

From brute force to optimal
---------------------------
The redundancy is recomputing "the tallest building covering x" from scratch when the covering
set changes by exactly one building per edge. Maintain that set in a max-heap of (height,
right) as the sweep line moves across sorted edges: a left edge pushes its building; a right
edge should remove one -- but heaps cannot delete arbitrary entries. Lazy removal solves it:
leave dead buildings in the heap and, before reading the top, pop while the top's right <= x
(it has ended). Since we only ever read the top, stale entries deeper down are harmless until
they surface. Each building is pushed once and popped once: O(n log n). Sorting edges as
(x, -height, right) with right edges as (x, 0, 0) makes starts at the same x come before ends
and taller starts first, so equal-x ties produce no spurious points.

Intuition
---------
Walk left to right; the skyline height at the sweep line is the tallest building currently
"alive". Births are easy to record; deaths are deferred until the dead building would
otherwise be reported as the maximum. A sentinel (height 0, infinite right) means the heap is
never empty and the ground level is reported automatically when the last building ends.
Append a key point only when the max changes -- that is the whole definition of a key point.

Geometric view
--------------
Rectangles standing on a line. A vertical sweep line slides right and stops at every left and
right edge. Beside it a max-heap triangle holds the live rectangles, tallest at the apex; the
apex height IS the skyline height at the sweep line. Some entries in the triangle are ghosts
(already ended) and are blown away only when they reach the apex. Whenever the apex height
differs from the last recorded height, a new corner of the outline is drawn.

Steps
-----
1. events = [(l, -h, r) for each building] + [(r, 0, 0) for each building]; sort.
2. live = [(0, inf)] (max-heap via negated heights, sentinel never expires); out = [[0, 0]].
3. For (x, negh, r): while live[0].right <= x: pop (lazy removal of ended buildings).
4. If negh < 0: push (negh, r).
5. If -live[0][0] != out[-1][1]: append [x, -live[0][0]].
6. Return out[1:].

Complexity: O(n log n) time, O(n) space — 2n events sorted; each building pushed once, popped once.
Pitfalls: Popping expired buildings with < instead of <= (a building ending at x does not cover
x); processing a right edge before a left edge at the same x (phantom dip to 0); forgetting to
drop the leading dummy point; emitting a point when the height did not change.
"""
import heapq
from typing import List


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # starts sort before ends at the same x (negative height < 0); taller starts first
        events = sorted([(l, -h, r) for l, r, h in buildings] + [(r, 0, 0) for _, r, _ in buildings])
        live = [(0, float("inf"))]                   # max-heap of (-height, right); sentinel ground
        out = [[0, 0]]                               # dummy so out[-1][1] always exists
        for x, neg_h, right in events:
            while live[0][1] <= x:                   # lazy removal: top has already ended
                heapq.heappop(live)
            if neg_h:
                heapq.heappush(live, (neg_h, right))
            if -live[0][0] != out[-1][1]:            # max changed: a corner of the outline
                out.append([x, -live[0][0]])
        return out[1:]


def brute_force(buildings: List[List[int]]) -> List[List[int]]:
    # At every edge x, rescan all buildings for the tallest covering x (left <= x < right).
    xs = sorted({x for l, r, _ in buildings for x in (l, r)})
    out, prev = [], 0
    for x in xs:
        h = max((hh for l, r, hh in buildings if l <= x < r), default=0)
        if h != prev:
            out.append([x, h])
            prev = h
    return out


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],
         [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
        ([[0, 2, 3], [2, 5, 3]], [[0, 3], [5, 0]]),             # touching, same height: merge
        ([[1, 4, 2]], [[1, 2], [4, 0]]),
        ([[1, 5, 3], [2, 4, 3]], [[1, 3], [5, 0]]),             # nested, same height
        ([[1, 3, 4], [3, 6, 2]], [[1, 4], [3, 2], [6, 0]]),     # drop at the shared edge
    )
    for b, want in cases:
        assert s.getSkyline([x[:] for x in b]) == want, (b, want)
        assert brute_force(b) == want, (b, want)
    import random
    random.seed(218)
    for _ in range(200):
        bs = []
        for _ in range(random.randint(1, 7)):
            l = random.randint(0, 20)
            bs.append([l, l + random.randint(1, 8), random.randint(1, 9)])
        assert s.getSkyline([x[:] for x in bs]) == brute_force(bs), bs
    print("ok")
