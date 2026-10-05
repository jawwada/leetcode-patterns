"""
Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368) - Hard
Chapter: graphs
Pattern: 0-1 BFS (deque shortest path)

Each cell of an m x n grid holds an arrow: 1 right, 2 left, 3 down, 4 up. Following the arrow
out of a cell is free; changing a cell's arrow costs 1, at most once per cell. Return the
minimum cost so that a path from (0,0) following the arrows reaches (m-1,n-1).
Example: [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]] -> 3
"""
from collections import deque      # popleft and appendleft are O(1)
import math                        # math.inf


# --- helpers ---
MOVES = ((0, 1), (0, -1), (1, 0), (-1, 0))   # arrow values 1, 2, 3, 4 point this way


def step_cost(grid, row, col, k):
    """0 if the arrow in (row, col) already points in direction k, else 1 to change it."""
    if grid[row][col] == k + 1:
        return 0
    return 1


# --- brute force ---
def brute_force(grid):
    """Bellman-Ford: sweep every cell relaxing its 4 moves until nothing improves. O((m*n)^2)."""
    m = len(grid)
    n = len(grid[0])
    cost = []
    for row in range(m):
        cost.append([math.inf] * n)
    cost[0][0] = 0
    changed = True
    while changed:                     # one more full sweep as long as any cell improved
        changed = False
        for row in range(m):
            for col in range(n):
                for k in range(4):
                    nr = row + MOVES[k][0]
                    nc = col + MOVES[k][1]
                    if nr < 0 or nr >= m or nc < 0 or nc >= n:
                        continue
                    step = step_cost(grid, row, col, k)
                    if cost[row][col] + step < cost[nr][nc]:
                        cost[nr][nc] = cost[row][col] + step
                        changed = True
    return cost[m - 1][n - 1]


# --- optimal ---
def minimum_cost_to_make_at_least_one_valid_path_in_a_grid(grid):
    """0-1 BFS: free moves go to the front of the deque, paid moves to the back. O(m*n)."""
    m = len(grid)
    n = len(grid[0])
    cost = []
    for row in range(m):
        cost.append([math.inf] * n)
    cost[0][0] = 0
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()     # the front always holds a cheapest cell, like Dijkstra
        for k in range(4):
            nr = row + MOVES[k][0]
            nc = col + MOVES[k][1]
            if nr < 0 or nr >= m or nc < 0 or nc >= n:
                continue
            step = step_cost(grid, row, col, k)
            if cost[row][col] + step < cost[nr][nc]:
                cost[nr][nc] = cost[row][col] + step
                if step == 0:
                    queue.appendleft((nr, nc))   # same cost layer: handle before any paid move
                else:
                    queue.append((nr, nc))       # one layer deeper: goes to the back
    return cost[m - 1][n - 1]


# --- try the brute force ---
print(brute_force([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]))   # -> 3
print(brute_force([[1, 1, 3], [3, 2, 2], [1, 1, 4]]))                          # -> 0
print(brute_force([[1, 2], [4, 3]]))                                           # -> 1
print(brute_force([[2, 2, 2], [2, 2, 2]]))                                     # -> 3


# --- try the optimal ---
grid_a = [[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]
print(minimum_cost_to_make_at_least_one_valid_path_in_a_grid(grid_a))                   # -> 3
grid_b = [[1, 1, 3], [3, 2, 2], [1, 1, 4]]
print(minimum_cost_to_make_at_least_one_valid_path_in_a_grid(grid_b))                   # -> 0
print(minimum_cost_to_make_at_least_one_valid_path_in_a_grid([[1, 2], [4, 3]]))         # -> 1
print(minimum_cost_to_make_at_least_one_valid_path_in_a_grid([[2, 2, 2], [2, 2, 2]]))   # -> 3
