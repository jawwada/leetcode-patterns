"""
Shortest Path in a Grid with Obstacles Elimination (LeetCode 1293) - Hard
Chapter: graphs
Pattern: BFS over augmented states (position + bitmask/budget)

In a 0/1 grid you walk 4-directionally from (0,0) to (m-1,n-1) and may step onto at most k
obstacle cells (1s), eliminating them. Return the minimum number of steps, or -1.
Example: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1 -> 6 (along the top, then down
the right edge through the obstacle at (3,2)).
"""
from collections import deque            # popleft is O(1)
from itertools import combinations       # every subset of a given size, as tuples


# --- helpers ---
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]     # down, up, right, left


# --- brute force ---
def steps_avoiding_obstacles(grid, cleared):
    """Plain BFS from (0,0) to the far corner over 0 cells and the cleared cells; -1 if cut off."""
    rows, cols = len(grid), len(grid[0])
    steps_to = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        row, col = queue.popleft()
        if (row, col) == (rows - 1, cols - 1):
            return steps_to[(row, col)]
        for d_row, d_col in DIRECTIONS:
            new_row, new_col = row + d_row, col + d_col
            if not (0 <= new_row < rows and 0 <= new_col < cols):
                continue
            if grid[new_row][new_col] == 1 and (new_row, new_col) not in cleared:
                continue
            if (new_row, new_col) not in steps_to:
                steps_to[(new_row, new_col)] = steps_to[(row, col)] + 1
                queue.append((new_row, new_col))
    return -1


def brute_force(grid, k):
    """Try every subset of at most k obstacles to clear and BFS each one. Exponential in k."""
    obstacles = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                obstacles.append((row, col))
    best = -1
    for size in range(min(k, len(obstacles)) + 1):
        for subset in combinations(obstacles, size):       # a full BFS for every subset
            steps = steps_avoiding_obstacles(grid, set(subset))
            if steps != -1 and (best == -1 or steps < best):
                best = steps
    return best


# --- optimal ---
def shortest_path(grid, k):
    """BFS over states (row, col, eliminations left) in layers. O(m * n * k) time and space."""
    rows, cols = len(grid), len(grid[0])
    if k >= rows + cols - 2:
        return rows + cols - 2                 # the straight Manhattan walk is affordable
    start = (0, 0, k)
    queue = deque([start])
    seen = {start}
    steps = 0
    while queue:
        for _ in range(len(queue)):            # one layer = one step
            row, col, left = queue.popleft()
            if (row, col) == (rows - 1, cols - 1):
                return steps
            for d_row, d_col in DIRECTIONS:
                new_row, new_col = row + d_row, col + d_col
                if not (0 <= new_row < rows and 0 <= new_col < cols):
                    continue
                new_left = left - grid[new_row][new_col]     # stepping on a 1 spends one
                state = (new_row, new_col, new_left)
                if new_left >= 0 and state not in seen:      # same cell, more budget: new state
                    seen.add(state)
                    queue.append(state)
        steps += 1
    return -1


# --- try the brute force ---
print(brute_force([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1))        # -> 6
print(brute_force([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1))                              # -> -1
print(brute_force([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 2))                              # -> 4
print(brute_force([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0))            # -> 10
print(brute_force([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 1))            # -> 6


# --- try the optimal ---
print(shortest_path([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1))        # -> 6
print(shortest_path([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1))                              # -> -1
print(shortest_path([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 2))                              # -> 4
print(shortest_path([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 0))            # -> 10
print(shortest_path([[0, 1, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 1, 0]], 1))            # -> 6
