"""
Shortest Path in a 0/1 Grid (basics: searches)
Count the cells on a shortest top-left to bottom-right path (0 = free, 1 = wall), or -1.
  grid = [[0, 0, 1], [1, 0, 0], [1, 1, 0]]  ->  5   (0,0) (0,1) (1,1) (1,2) (2,2)

Idea: BFS spreads out in layers: layer k holds exactly the cells k steps from the start.
      So the first time the target leaves the queue, its layer gives the shortest path.
      Mark a cell seen when it is enqueued, so no cell enters the queue twice.

Pseudocode:
  if start is a wall: return -1
  queue = [start]; seen = {start}; cells = 1
  while queue:
      for each cell in the current layer:
          if cell is the target: return cells
          for each of the 4 neighbours that is in bounds, free and unseen:
              mark it seen, enqueue it
      cells += 1                         # next layer is one cell further
  return -1

Time O(m * n), space O(m * n).
"""
from collections import deque


def shortest_path(grid):
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1:
        return -1                        # start is a wall
    queue = deque([(0, 0)])
    seen = {(0, 0)}
    cells = 1                            # path length (in cells) of the current layer
    while queue:
        for _ in range(len(queue)):      # one layer = one more cell on the path
            r, c = queue.popleft()
            if (r, c) == (m - 1, n - 1):
                return cells             # first arrival is the shortest
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in seen:
                    seen.add((nr, nc))   # mark when enqueued
                    queue.append((nr, nc))
        cells += 1
    return -1


if __name__ == "__main__":
    print(shortest_path([[0, 0, 1], [1, 0, 0], [1, 1, 0]]))  # 5
    print(shortest_path([[0, 1], [1, 0]]))                   # -1
    print(shortest_path([[0]]))                              # 1
