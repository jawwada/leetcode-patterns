"""
01 Matrix (LeetCode 542) - Fundamentals
Chapter: fundamentals/searches
Key operations: enqueue every source first (distance 0), layer-by-layer BFS, mark when enqueued

For every cell of a 0/1 matrix return the distance to the nearest 0 (moving up/down/left/right).
Put ALL zeros in the queue at the start: one BFS then grows from every source at once, and the
layer in which a cell is first reached is its distance to the closest zero.
Example: [[0, 0, 0], [0, 1, 0], [1, 1, 1]] -> [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
"""
from collections import deque      # popleft is O(1)


# --- algorithm ---
def nearest_zero_distances(mat):
    """Multi-source BFS: every zero starts in the queue at distance 0; cells are reached once."""
    rows = len(mat)
    cols = len(mat[0])
    dist = []
    queue = deque()
    for r in range(rows):
        row = []
        for c in range(cols):
            if mat[r][c] == 0:
                row.append(0)
                queue.append((r, c))   # all sources go in before the BFS starts
            else:
                row.append(-1)         # -1 means "not reached yet"
        dist.append(row)
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if dist[nr][nc] != -1:
                continue               # already reached from a nearer (or equally near) zero
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
    return dist


# --- try it ---
print(nearest_zero_distances([[0, 0, 0], [0, 1, 0], [1, 1, 1]]))
# -> [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
print(nearest_zero_distances([[0, 1, 1, 1]]))                      # -> [[0, 1, 2, 3]]
print(nearest_zero_distances([[1, 1], [1, 0]]))                    # -> [[2, 1], [1, 0]]
