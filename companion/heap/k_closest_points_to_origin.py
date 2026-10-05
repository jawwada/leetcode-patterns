"""
K Closest Points to Origin (LeetCode 973) - Medium
Chapter: heap
Pattern: Size-k heap (keep the k best)

Given points [[x, y], ...] on a plane and an integer k, return the k points closest to the
origin by Euclidean distance, in any order.
Example: points=[[1,3],[-2,2]], k=1 -> [[-2,2]] because 8 < 10.
Example: [[3,3],[5,-1],[-2,4]], k=2 -> [[3,3],[-2,4]].
"""
import heapq      # heappush / heappop keep the smallest item at index 0


# --- brute force ---
def brute_force(points, k):
    """Sort all n points by squared distance and take the first k. O(n log n) time."""
    with_distance = []
    for x, y in points:
        with_distance.append((x * x + y * y, x, y))
    with_distance.sort()                      # orders every point, not just the k nearest
    result = []
    for i in range(k):
        result.append([with_distance[i][1], with_distance[i][2]])
    return result


# --- optimal ---
def k_closest(points, k):
    """Max-heap (negated distance) of the k nearest so far; evict the farthest. O(n log k)."""
    heap = []                                 # (-distance, x, y): the root is the farthest kept
    for x, y in points:
        distance = x * x + y * y
        heapq.heappush(heap, (-distance, x, y))
        if len(heap) > k:
            heapq.heappop(heap)               # k + 1 points kept: drop the farthest one
    result = []
    for neg_distance, x, y in heap:
        result.append([x, y])
    return result


# --- try the brute force ---
# any order is accepted, so the demos print the points sorted
print(sorted(brute_force([[1, 3], [-2, 2]], 1)))              # -> [[-2, 2]]
print(sorted(brute_force([[3, 3], [5, -1], [-2, 4]], 2)))     # -> [[-2, 4], [3, 3]]
print(sorted(brute_force([[0, 1], [1, 0]], 2)))               # -> [[0, 1], [1, 0]]


# --- try the optimal ---
# any order is accepted, so the demos print the points sorted
print(sorted(k_closest([[1, 3], [-2, 2]], 1)))                # -> [[-2, 2]]
print(sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)))       # -> [[-2, 4], [3, 3]]
print(sorted(k_closest([[0, 1], [1, 0]], 2)))                 # -> [[0, 1], [1, 0]]
