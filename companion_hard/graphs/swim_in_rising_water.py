"""
Swim in Rising Water (LeetCode 778) - Hard
Chapter: graphs
Pattern: Minimax path via min-heap (bottleneck Dijkstra)

An n x n grid holds the distinct elevations 0..n*n-1. At time t the water level is t and you can
move between 4-adjacent cells whose elevations are both <= t. Starting at (0,0), return the
least t at which you can reach (n-1,n-1).
Example: [[0,2],[1,3]] -> 3;  [[7,5,3],[8,6,1],[0,2,4]] -> 7
"""
import heapq                       # heappush / heappop keep the smallest at index 0


# --- brute force ---
def reachable(grid, level):
    """Can (0,0) reach (n-1,n-1) stepping only on cells with elevation <= level?"""
    n = len(grid)
    if grid[0][0] > level:
        return False
    seen = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        row, col = stack.pop()
        for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
            if nr < 0 or nr >= n or nc < 0 or nc >= n:
                continue
            if (nr, nc) not in seen and grid[nr][nc] <= level:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return (n - 1, n - 1) in seen


def brute_force(grid):
    """Try every water level from 0 upward; the first that connects the corners wins. O(n^4)."""
    n = len(grid)
    for level in range(n * n):         # each level re-walks the region the last one explored
        if reachable(grid, level):
            return level
    return -1


# --- optimal ---
def swim_in_rising_water(grid):
    """Bottleneck Dijkstra: always expand the lowest cell on the shoreline. O(n^2 log n)."""
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]        # (highest elevation on the path so far, row, col)
    seen = {(0, 0)}
    while heap:
        level, row, col = heapq.heappop(heap)
        if row == n - 1 and col == n - 1:
            return level               # the first time the goal pops, its level is the smallest
        for nr, nc in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
            if nr < 0 or nr >= n or nc < 0 or nc >= n or (nr, nc) in seen:
                continue
            seen.add((nr, nc))         # later pops are at least this high: they cannot do better
            heapq.heappush(heap, (max(level, grid[nr][nc]), nr, nc))
    return -1


# --- try the brute force ---
print(brute_force([[0, 2], [1, 3]]))                        # -> 3
print(brute_force([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
                   [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]))   # -> 16
print(brute_force([[3, 2], [0, 1]]))                        # -> 3
print(brute_force([[7, 5, 3], [8, 6, 1], [0, 2, 4]]))       # -> 7


# --- try the optimal ---
print(swim_in_rising_water([[0, 2], [1, 3]]))                        # -> 3
print(swim_in_rising_water([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
                            [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]))   # -> 16
print(swim_in_rising_water([[3, 2], [0, 1]]))                        # -> 3
print(swim_in_rising_water([[7, 5, 3], [8, 6, 1], [0, 2, 4]]))       # -> 7
