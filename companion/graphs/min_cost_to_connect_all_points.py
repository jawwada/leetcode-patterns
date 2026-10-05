"""
Min Cost to Connect All Points (LeetCode 1584) - Medium
Chapter: graphs
Pattern: Minimum spanning tree (Prim's with heap)

Given n points on a plane, connecting two points costs their Manhattan distance |x1-x2| + |y1-y2|.
Return the minimum total cost to connect all points so that there is a path between every pair,
i.e. the weight of a minimum spanning tree of the complete graph.
Example: [[0,0],[2,2],[3,10],[5,2],[7,0]] -> 20.
"""
import heapq                       # heappush / heappop keep the smallest at index 0


# --- helpers ---
def manhattan(p, q):
    """Distance between two points when you may only move along the grid lines."""
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


# --- brute force ---
def brute_force(points):
    """Kruskal without union-find: sort edges, take one if a DFS finds the ends apart. O(n^3)"""
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((manhattan(points[i], points[j]), i, j))
    edges.sort()                     # cheapest edge first
    neighbours = []
    for _ in range(n):
        neighbours.append([])
    total = 0
    for w, u, v in edges:
        seen = {u}
        stack = [u]
        while stack:                 # DFS over the accepted edges: can u already reach v?
            cur = stack.pop()
            for nb in neighbours[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if v not in seen:            # different trees: the edge is safe to take
            neighbours[u].append(v)
            neighbours[v].append(u)
            total += w
    return total


# --- optimal ---
def min_cost_to_connect_all_points(points):
    """Prim's: grow one tree, always adding the outside point closest to the tree. O(n^2 log n)."""
    n = len(points)
    in_tree = [False] * n
    heap = [(0, 0)]                  # (cost to join the tree, point index); point 0 joins for free
    total = 0
    added = 0
    while added < n:
        cost, i = heapq.heappop(heap)
        if in_tree[i]:
            continue                 # stale: i joined earlier through a cheaper edge
        in_tree[i] = True
        total += cost
        added += 1
        for j in range(n):
            if not in_tree[j]:       # offer every outside point a connection to the new member
                heapq.heappush(heap, (manhattan(points[i], points[j]), j))
    return total


# --- try the brute force ---
print(brute_force([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # -> 20
print(brute_force([[3, 12], [-2, 5], [-4, 1]]))                 # -> 18
print(brute_force([[0, 0]]))                                    # -> 0
print(brute_force([[0, 0], [1, 1], [1, 0], [-1, 1]]))           # -> 4


# --- try the optimal ---
print(min_cost_to_connect_all_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # -> 20
print(min_cost_to_connect_all_points([[3, 12], [-2, 5], [-4, 1]]))                 # -> 18
print(min_cost_to_connect_all_points([[0, 0]]))                                    # -> 0
print(min_cost_to_connect_all_points([[0, 0], [1, 1], [1, 0], [-1, 1]]))           # -> 4
