"""
Min Cost to Connect All Points (LeetCode 1584)
Connect all points with minimum total Manhattan distance (a minimum spanning tree).
  points = [[0,0],[2,2],[3,10],[5,2],[7,0]]  ->  20

Idea: Prim. Grow one tree from point 0; always add the outside point that is cheapest to attach.
      A min-heap of (cost, point) gives that cheapest point.

Pseudocode:
  heap = [(0, point 0)]
  while not all points joined:
      cost, i = pop smallest
      if i in tree: skip
      add i to tree, total += cost
      for every point j not in tree: push (dist(i, j), j)
  return total

Time O(n^2 log n), space O(n^2).
"""
import heapq


def min_cost_connect_points(points):
    n = len(points)
    in_tree = [False] * n
    heap = [(0, 0)]                              # (cost to join, point index)
    total = joined = 0
    while joined < n:
        cost, i = heapq.heappop(heap)
        if in_tree[i]:                           # already joined via a cheaper edge
            continue
        in_tree[i] = True
        total += cost
        joined += 1
        xi, yi = points[i]
        for j, (xj, yj) in enumerate(points):    # offer edges to outside points
            if not in_tree[j]:
                heapq.heappush(heap, (abs(xi - xj) + abs(yi - yj), j))
    return total


if __name__ == "__main__":
    print(min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))  # 20
    print(min_cost_connect_points([[3, 12], [-2, 5], [-4, 1]]))                # 18
