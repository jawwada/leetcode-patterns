"""
Erect the Fence (LeetCode 587)  — Hard
Pattern: Convex hull (Andrew's monotone chain, keeping collinear boundary points)

Problem
-------
Given the coordinates of trees in a garden, fence the whole garden with the minimum length of
rope, i.e. return every tree that lies ON the convex hull boundary (including trees that sit on
a hull edge between two corners). Any order is accepted.
Example: [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]] -> [[1,1],[2,0],[4,2],[3,3],[2,4]]
         ((2,2) is strictly inside).  [[1,2],[2,2],[4,2]] -> all three (collinear).

Brute force
-----------
A segment (i, j) is on the hull iff every other point lies on one side of its line (or on it).
For each pair compute the cross product sign of every third point; if no two signs disagree, the
line is a supporting line and every point with cross == 0 is a boundary tree. O(n^3) time, O(n)
space — n = 3000 gives 2.7*10^10. The waste: each of the n^2 candidate lines is tested against
all n points although only O(n) of them are hull edges, and the hull's defining property (a
left turn at every vertex) can be enforced incrementally.

From brute force to optimal
---------------------------
The redundancy is testing every pair as a potential edge. Observation: once the points are
sorted by (x, y), the lower hull is traversed left to right and the upper hull right to left,
and along either walk every consecutive triple makes a counter-clockwise (or straight) turn.
Build the lower chain with a stack: before pushing p, pop the top while the turn
(stack[-2] -> stack[-1] -> p) is clockwise (cross < 0); popped points are strictly inside. Do
the same over the reversed order for the upper chain. Keeping cross == 0 points (rather than
popping them as the classic hull does) is what retains trees on the edges. Sorting dominates:
O(n log n), and each point is pushed and popped at most once per chain.

Intuition
---------
Walk around the garden keeping it on your left; whenever you would have to turn right, the
previous post was not a corner — remove it. A sorted order makes this walk a single sweep, and
the stack is the fence under construction. Collinear points are neither left nor right turns,
so they stay.

Geometric view
--------------
Picture the points sorted left to right. The lower chain hangs like a rope stretched under the
points; pushing a new point and popping clockwise turns is the rope snapping taut. The upper
chain is the same rope stretched over the top, built from right to left. Their union is the
fence; the leftmost and rightmost trees appear in both chains, hence the set.

Steps
-----
1. Sort trees by (x, y).
2. cross(o, a, b) = (a-o) x (b-o): > 0 counter-clockwise, < 0 clockwise, 0 collinear.
3. lower: for p in trees: while len >= 2 and cross(lower[-2], lower[-1], p) < 0: pop; push p.
4. upper: same loop over reversed(trees).
5. Return the set union of both chains as lists.

Complexity: O(n log n) time (sort), O(n) space — amortised O(1) stack work per point.
Pitfalls: popping on cross <= 0 (drops collinear edge trees); returning duplicates of the two
end points; floating-point slopes instead of integer cross products; forgetting n < 3 edge cases
(everything is on the hull).
"""
import random
from typing import List


class Solution:
    def outerTrees(self, trees: List[List[int]]) -> List[List[int]]:
        def cross(o, a, b) -> int:                   # (a - o) x (b - o)
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        pts = sorted(map(tuple, trees))
        lower = []
        for p in pts:                                # left -> right along the bottom
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
                lower.pop()                          # clockwise turn: middle point is inside
            lower.append(p)
        upper = []
        for p in reversed(pts):                      # right -> left along the top
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:
                upper.pop()
            upper.append(p)
        return [list(p) for p in set(lower + upper)]  # ends appear in both chains


def brute_force(trees: List[List[int]]) -> List[List[int]]:
    n = len(trees)
    if n < 3:
        return [list(p) for p in trees]
    on_hull = set()
    for i in range(n):
        for j in range(i + 1, n):                    # is line (i, j) a supporting line?
            (xi, yi), (xj, yj) = trees[i], trees[j]
            crosses = [(xj - xi) * (y - yi) - (yj - yi) * (x - xi) for x, y in trees]
            if all(c >= 0 for c in crosses) or all(c <= 0 for c in crosses):
                on_hull.update(tuple(trees[k]) for k, c in enumerate(crosses) if c == 0)
    return [list(p) for p in on_hull]


if __name__ == "__main__":
    s = Solution()
    as_set = lambda pts: {tuple(p) for p in pts}
    assert as_set(s.outerTrees([[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]])) == \
        {(1, 1), (2, 0), (4, 2), (3, 3), (2, 4)}
    assert as_set(s.outerTrees([[1, 2], [2, 2], [4, 2]])) == {(1, 2), (2, 2), (4, 2)}
    assert as_set(s.outerTrees([[0, 0]])) == {(0, 0)}                           # one tree
    assert as_set(s.outerTrees([[0, 0], [0, 1], [0, 2], [1, 1]])) == \
        {(0, 0), (0, 1), (0, 2), (1, 1)}                                        # vertical edge
    rng = random.Random(587)
    for _ in range(150):
        pts = list({(rng.randint(0, 5), rng.randint(0, 5)) for _ in range(rng.randint(1, 10))})
        pts = [list(p) for p in pts]
        assert as_set(s.outerTrees(pts)) == as_set(brute_force(pts)), pts
    print("ok")
