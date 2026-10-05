"""
Trapping Rain Water II (LeetCode 407) - Hard
Chapter: heap
Pattern: Min-heap frontier expanding inward from the boundary (lowest wall first)

Given an m x n elevation map, return the volume of water trapped after raining. Water can only
escape over the border, flowing through 4-directionally adjacent cells.
Example: [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]] -> 4 (the middle row's 2, 1, 2 fill to 3).
"""
import heapq                       # heappush / heappop keep the smallest item at index 0
import math                        # math.inf: "no level found yet"


# --- helpers ---
def is_border(row, col, rows, cols):
    """True for a cell on the outer edge of the grid."""
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1


# --- brute force ---
def brute_force(height_map):
    """Relax level = max(height, lowest neighbour level) over the grid until stable. O((mn)^2)."""
    rows = len(height_map)
    cols = len(height_map[0])
    level = []                                 # final water surface over each cell
    for row in range(rows):
        level.append([math.inf] * cols)
        for col in range(cols):
            if is_border(row, col, rows, cols):
                level[row][col] = height_map[row][col]   # water on the border just runs off
    changed = True
    while changed:
        changed = False
        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                lowest_neighbour = min(level[row - 1][col], level[row + 1][col],
                                       level[row][col - 1], level[row][col + 1])
                new_level = max(height_map[row][col], lowest_neighbour)
                if new_level < level[row][col]:    # water can drain a bit more this sweep
                    level[row][col] = new_level
                    changed = True
    water = 0
    for row in range(rows):
        for col in range(cols):
            water += level[row][col] - height_map[row][col]
    return water


# --- optimal ---
def trap_rain_water(height_map):
    """Dijkstra from the border: pop the lowest wall, flood neighbours to its level. O(mn log n)."""
    rows = len(height_map)
    cols = len(height_map[0])
    seen = []
    frontier = []                              # (water level, row, col): root = lowest wall
    for row in range(rows):
        seen.append([False] * cols)
        for col in range(cols):
            if is_border(row, col, rows, cols):
                seen[row][col] = True
                heapq.heappush(frontier, (height_map[row][col], row, col))
    water = 0
    while len(frontier) > 0:
        level, row, col = heapq.heappop(frontier)      # lowest point of the current dam
        for next_row, next_col in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if next_row < 0 or next_row >= rows or next_col < 0 or next_col >= cols:
                continue
            if seen[next_row][next_col]:
                continue
            seen[next_row][next_col] = True
            height = height_map[next_row][next_col]
            water += max(0, level - height)            # fills up to the dam's level
            heapq.heappush(frontier, (max(level, height), next_row, next_col))
    return water


# --- try the brute force ---
print(brute_force([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]))   # -> 4
print(brute_force([[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3], [3, 2, 2, 2, 3],
                   [3, 3, 3, 3, 3]]))   # -> 10
print(brute_force([[5, 5, 5], [5, 1, 5], [5, 5, 5]]))   # -> 4
print(brute_force([[5, 5, 5], [5, 1, 5], [5, 0, 5]]))   # -> 0


# --- try the optimal ---
print(trap_rain_water([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]]))   # -> 4
print(trap_rain_water([[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3], [3, 2, 2, 2, 3],
                       [3, 3, 3, 3, 3]]))   # -> 10
print(trap_rain_water([[5, 5, 5], [5, 1, 5], [5, 5, 5]]))   # -> 4
print(trap_rain_water([[5, 5, 5], [5, 1, 5], [5, 0, 5]]))   # -> 0
