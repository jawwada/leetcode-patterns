"""
K Closest Points to Origin (LeetCode 973) - Medium
Area: heap
Key operations: push (-dist, x, y), evict the root when the heap exceeds k, read the k survivors

Given points on a plane and an integer k, return the k points closest to the origin (Euclidean
distance). Any order is accepted; here the result is returned sorted for determinism.
Example: points = [[3, 3], [5, -1], [-2, 4]], k = 2 -> [[-2, 4], [3, 3]]  (distances 20 and 18 beat 26)
"""
import heapq
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
def dist(x: int, y: int) -> int:
    """Squared Euclidean distance to the origin; sqrt is monotonic, so it is never needed."""
    return x * x + y * y


# --- brute force ---
def brute_force(points: List[List[int]], k: int) -> List[List[int]]:
    """Sort all n points by squared distance and take the first k. O(n log n): it fully orders the
    n - k far points too, although their relative order is never needed."""
    ordered = sorted(points, key=lambda p: dist(p[0], p[1]))
    return sorted(ordered[:k])


# --- optimal ---
def solve(points: List[List[int]], k: int) -> List[List[int]]:
    """Max-heap (negated squared distance) of the k closest points seen so far. Its root is the
    farthest kept point, the doorman every new point has to beat. O(n log k) time, O(k) space."""
    kept = []  # entries (-d, x, y); kept[0] is the farthest of the kept points
    for x, y in points:
        d = dist(x, y)
        heapq.heappush(kept, (-d, x, y))
        log(f"point ({x}, {y}) d={d}: push -> heap {[(-nd, (px, py)) for nd, px, py in kept]}")
        if len(kept) > k:
            far = heapq.heappop(kept)
            log(f"    size {len(kept) + 1} > k={k}: evict root ({far[1]}, {far[2]}) d={-far[0]} -> heap {[(-nd, (px, py)) for nd, px, py in kept]}, radius now {-kept[0][0]}")
    return sorted([x, y] for _, x, y in kept)


# --- demo ---
def demo():
    points = [[3, 3], [5, -1], [-2, 4]]
    return solve(points, 2)


# --- tests ---
def tests():
    assert solve([[3, 3], [5, -1], [-2, 4]], 2) == [[-2, 4], [3, 3]]
    assert solve([[1, 3], [-2, 2]], 1) == [[-2, 2]]
    assert solve([[3, 0], [2, 2]], 1) == [[2, 2]]  # 8 < 9: Euclidean, not Manhattan
    assert solve([[0, 1], [1, 0]], 2) == [[0, 1], [1, 0]]  # k == n keeps everything
    assert solve([[7, 7]], 1) == [[7, 7]]
    assert solve([[1, 1], [1, 1], [2, 2]], 2) == [[1, 1], [1, 1]]  # duplicate points
    assert solve([[0, 0], [1, 1], [2, 2], [3, 3]], 1) == [[0, 0]]  # the origin itself
    import random
    for _ in range(200):
        n = random.randint(1, 10)
        pts = [[random.randint(-5, 5), random.randint(-5, 5)] for _ in range(n)]
        k = random.randint(1, n)
        got = solve(pts, k)
        assert len(got) == k, (pts, k)
        dists = lambda res: sorted(dist(x, y) for x, y in res)
        assert dists(got) == dists(brute_force(pts, k)), (pts, k)  # ties may pick either point


# --- bugs ---
BUGS = [
    {
        "replace": "        heapq.heappush(kept, (-d, x, y))",
        "with":    "        heapq.heappush(kept, (d, x, y))",
        "fix": "push -d so the root is the farthest kept point",
        "why": "Without the negation the root is the closest point, so the eviction throws away the best point each time: [[1, 3], [-2, 2]], k = 1 keeps [1, 3].",
        "decoys": [
            {"line": "        d = dist(x, y)", "change": "should take the square root of dist"},
            {"line": "        if len(kept) > k:", "change": "should be len(kept) == k"},
            {"line": "    return sorted([x, y] for _, x, y in kept)", "change": "should return kept[:k]"},
        ],
    },
    {
        "replace": "        if len(kept) > k:",
        "with":    "        if len(kept) >= k:",
        "fix": "evict only when the heap holds k + 1 points: strict >",
        "why": "With >= the heap is trimmed back to k - 1 after every push, so k = 1 returns an empty list.",
        "decoys": [
            {"line": "        heapq.heappush(kept, (-d, x, y))", "change": "should push (x, y, -d)"},
            {"line": "            far = heapq.heappop(kept)", "change": "should be heapq.heappop(kept, 0)"},
            {"line": "    kept = []  # entries (-d, x, y); kept[0] is the farthest of the kept points", "change": "should start as [None] * k"},
        ],
    },
    {
        "replace": "            far = heapq.heappop(kept)",
        "with":    "            far = kept.pop()",
        "fix": "use heapq.heappop: the farthest is the root, not the last slot",
        "why": "list.pop() removes whatever sits at the end of the heap array, usually a recently pushed close point: [[1, 3], [-2, 2]], k = 1 evicts (-2, 2) and keeps (1, 3).",
        "decoys": [
            {"line": "        heapq.heappush(kept, (-d, x, y))", "change": "should be kept.append((-d, x, y))"},
            {"line": "    for x, y in points:", "change": "should iterate over sorted(points)"},
            {"line": "        d = dist(x, y)", "change": "should be abs(x) + abs(y)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
