"""
Rotting Oranges (LeetCode 994) - Medium
Chapter: graphs
Pattern: Multi-source BFS (level = distance)

In an m x n grid, 0 is empty, 1 is a fresh orange and 2 is a rotten orange. Every minute each
rotten orange rots its 4-neighbouring fresh oranges. Return the minimum number of minutes until
no fresh orange remains, or -1 if that never happens.
Example: [[2,1,1],[1,1,0],[0,1,1]] -> 4; [[2,1,1],[0,1,1],[1,0,1]] -> -1 (bottom-left is cut off).
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(grid):
    """Simulate minute by minute, rescanning the whole grid every round. O((mn)^2) time."""
    rows = len(grid)
    cols = len(grid[0])
    minutes = 0
    while True:
        next_grid = []
        for row in grid:
            next_grid.append(row[:])     # rot into a copy so the whole minute happens at once
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != 2:
                    continue
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        next_grid[nr][nc] = 2
                        changed = True
        if not changed:
            break
        grid = next_grid
        minutes += 1
    for row in grid:                 # a fresh orange still left can never rot
        if 1 in row:
            return -1
    return minutes


# --- optimal ---
def rotting_oranges(grid):
    """Multi-source BFS: every rotten orange is a start; one BFS layer is one minute. O(mn)."""
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):      # exactly the oranges that rotted last minute
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    if fresh > 0:
        return -1
    return minutes


# --- try the brute force ---
print(brute_force([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # -> 4
print(brute_force([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # -> -1
print(brute_force([[0, 2]]))                            # -> 0
print(brute_force([[2, 1, 1, 1, 1]]))                   # -> 4


# --- try the optimal ---
print(rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))   # -> 4
print(rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # -> -1
print(rotting_oranges([[0, 2]]))                            # -> 0
print(rotting_oranges([[2, 1, 1, 1, 1]]))                   # -> 4
