"""
Multi-Source BFS - Rotting Oranges

In a grid, 0 is empty, 1 is a fresh orange and 2 a rotten one. Every minute,
each fresh orange next to a rotten one (up, down, left, right) rots. Return
the minutes until no fresh orange is left, or -1 if one never rots:
[[2, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 2]] -> 2.
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def oranges_rotting(grid):
    """BFS from every rotten orange at once; one layer per minute. O(R * C)."""
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    fresh = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 2:
                queue.append((row, col))    # every source starts at minute 0
            elif grid[row][col] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):         # exactly the oranges of this layer
            row, col = queue.popleft()
            for d_row, d_col in DIRECTIONS:
                next_row = row + d_row
                next_col = col + d_col
                inside = 0 <= next_row < rows and 0 <= next_col < cols
                if inside and grid[next_row][next_col] == 1:
                    grid[next_row][next_col] = 2    # rot it now: enqueued once
                    fresh -= 1
                    queue.append((next_row, next_col))
        minutes += 1
    if fresh > 0:
        return -1                           # walled off from every rotten one
    return minutes


# --- try it ---
print(oranges_rotting([[2, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 2]]))  # -> 2
print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))           # -> 4
print(oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))           # -> -1
print(oranges_rotting([[0, 2]]))                                    # -> 0
