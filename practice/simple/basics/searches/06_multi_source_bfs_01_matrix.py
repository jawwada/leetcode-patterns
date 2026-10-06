"""
01 Matrix (basics: searches)
For every cell of a 0/1 matrix return its distance (up/down/left/right steps) to the nearest 0.
  [[0, 0, 0], [0, 1, 0], [1, 1, 1]]  ->  [[0, 0, 0], [0, 1, 0], [1, 2, 1]]

Idea: multi-source BFS. Start with ALL zeros in the queue (distance 0). The queue then hands
      out cells in order of distance, so the first time a cell is reached it comes from its
      nearest zero: set its distance once and never change it.

Pseudocode:
  dist = -1 everywhere; every zero gets dist 0 and goes in the queue
  while queue:
      r, c = pop front
      for each in-bounds neighbour with dist -1:
          dist[neighbour] = dist[r][c] + 1; enqueue it
  return dist

Time O(m * n), space O(m * n).
"""
from collections import deque


def distance_to_nearest_zero(mat):
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]  # -1 = not reached yet
    queue = deque()
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 0:
                dist[r][c] = 0           # every zero is a source
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1   # first arrival = nearest zero
                queue.append((nr, nc))
    return dist


if __name__ == "__main__":
    mat = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    print(distance_to_nearest_zero(mat))             # [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
    print(distance_to_nearest_zero([[0, 1, 1, 1]]))  # [[0, 1, 2, 3]]
