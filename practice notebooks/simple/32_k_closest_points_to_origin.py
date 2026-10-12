"""
K Closest Points to Origin (LeetCode 973)
Return the k points closest to the origin (0, 0).
  points = [[3, 3], [5, -1], [-2, 4]], k = 2  ->  [[-2, 4], [3, 3]]   (18 and 20 beat 26)

Idea: keep only the k best points in a max-heap keyed by distance.
      The root is the farthest kept point: any new point that is closer kicks it out.
      Compare squared distances (x*x + y*y); sqrt never changes the order.

Pseudocode:
  heap = []                       # max-heap via (-dist, x, y)
  for x, y in points:
      push (-(x*x + y*y), x, y)
      if len(heap) > k: pop       # drops the farthest
  return the points left in heap

Time O(n log k), space O(k).
"""
import heapq


def k_closest(points, k):
    heap = []                                  # (-dist, x, y): root = farthest kept
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))
        if len(heap) > k:                      # too many: drop the farthest
            heapq.heappop(heap)
    return sorted([x, y] for _, x, y in heap)  # sorted only for a stable printout


if __name__ == "__main__":
    print(k_closest([[3, 3], [5, -1], [-2, 4]], 2))  # [[-2, 4], [3, 3]]
    print(k_closest([[1, 3], [-2, 2]], 1))           # [[-2, 2]]
