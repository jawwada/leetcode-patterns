"""
Shortest Path in a 0/1 Grid - Fundamentals
Chapter: fundamentals/searches
Key operations: queue of cells, mark visited when enqueued, four directions with a bounds check

Grid of 0 (free) and 1 (wall). Return the number of cells on a shortest path from the top-left to
the bottom-right moving up, down, left or right, or -1 if there is none. BFS explores in layers
(one layer = one step), so the first time the target leaves the queue its distance is final.
Example: [[0, 0, 1], [1, 0, 0], [1, 1, 0]] -> 5, the path (0,0) (0,1) (1,1) (1,2) (2,2)
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def shortest_path(grid):
    """BFS layer by layer; a cell gets its distance when ENQUEUED, so it is queued once. O(m*n)."""
    rows = len(grid)
    cols = len(grid[0])
    if grid[0][0] == 1:
        return -1
    dist = {(0, 0): 1}                 # cell -> number of cells on the path so far
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == rows - 1 and c == cols - 1:
            return dist[(r, c)]        # first pop of the target: its distance is the shortest
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] == 1 or (nr, nc) in dist:
                continue
            dist[(nr, nc)] = dist[(r, c)] + 1   # mark now, not when popped, or cells queue twice
            queue.append((nr, nc))
    return -1


# --- try it ---
print(shortest_path([[0, 0, 1], [1, 0, 0], [1, 1, 0]]))   # -> 5
print(shortest_path([[0, 1], [1, 0]]))                    # -> -1
print(shortest_path([[0]]))                               # -> 1
print(shortest_path([[0, 0], [0, 0]]))                    # -> 3
