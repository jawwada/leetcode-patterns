"""
K Closest Points to Origin (LeetCode 973)  — Medium
Pattern: Size-k heap (keep the k best)

Problem
-------
Given points [[x, y], ...] on a plane and an integer k, return the k points closest to the origin
(Euclidean distance). Any order is accepted.
Example: points=[[1,3],[-2,2]], k=1 -> [[-2,2]] because 8 < 10.

Brute force
-----------
Compute every point's squared distance, sort all n points by it, return the first k.
O(n log n) time, O(n) space. The waste: sorting fully orders ALL n points, but we only need to
separate the k smallest from the rest; the relative order of the n-k far points is irrelevant.

From brute force to optimal
---------------------------
The redundancy is ordering points we will discard. Observation: a point that is farther than k
points we have already seen can never be in the answer, so it can be rejected immediately.
To test that in O(log k) we need fast access to the *worst* point currently kept: a max-heap of
size k keyed on distance. Each new point is compared to the heap root (the farthest kept point);
if closer, it replaces it. Only k items are ever stored, so n points cost O(n log k).
(For the fully optimal O(n) average, quickselect on distance partitions the array in place.)

Intuition
---------
Hold a "k closest so far" club whose doorman is the farthest member. Every arriving point only
has to beat the doorman. Python has a min-heap, so negate the distance to make it a max-heap.

Geometric view
--------------
Draw the kept points as a disc around the origin whose radius is the heap root's distance.
Each new point either lands outside the disc (ignored) or inside it (admitted), and then the
disc shrinks to the new farthest member. The disc radius is monotonically non-increasing.

Steps
-----
1. For each point compute d = x*x + y*y (no sqrt needed; monotone).
2. Push (-d, x, y) onto the heap.
3. If the heap grows past k, pop (removes the farthest kept point).
4. Return the points left in the heap.

Complexity: O(n log k) time, O(k) space — each push/pop costs log k on a heap of at most k items.
Pitfalls: Using math.sqrt (slower and floating point, unnecessary); forgetting to negate for a
max-heap; pushing the raw list into the tuple (fine here, but ties then compare coordinates).
"""
import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap: List[tuple] = []                       # max-heap on distance via negation
        for x, y in points:
            heapq.heappush(heap, (-(x * x + y * y), x, y))
            if len(heap) > k:                        # root = farthest kept point, evict it
                heapq.heappop(heap)
        return [[x, y] for _, x, y in heap]


def brute_force(points: List[List[int]], k: int) -> List[List[int]]:
    ordered = sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])  # orders ALL n points
    return ordered[:k]


if __name__ == "__main__":
    s = Solution()

    def same(a, b):
        return sorted(map(tuple, a)) == sorted(map(tuple, b))

    assert same(s.kClosest([[1, 3], [-2, 2]], 1), [[-2, 2]])
    assert same(s.kClosest([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]])
    assert same(s.kClosest([[0, 1], [1, 0]], 2), [[0, 1], [1, 0]])          # k == n
    assert same(s.kClosest([[1, 3], [-2, 2]], 1), brute_force([[1, 3], [-2, 2]], 1))
    assert same(s.kClosest([[3, 3], [5, -1], [-2, 4]], 2), brute_force([[3, 3], [5, -1], [-2, 4]], 2))
    print("ok")
