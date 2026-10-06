"""
Rotting Oranges (LeetCode 994)
Each minute rot spreads to adjacent fresh oranges; return minutes until none are fresh, or -1.
  grid = [[2,1,1],[1,1,0],[0,1,1]]  ->  4

Idea: all rotten oranges start spreading at once, so start a BFS from all of them together.
      One BFS layer = one minute.

Pseudocode:
  queue = all rotten cells; fresh = count of fresh cells
  while queue and fresh:
      for each cell in the current layer:
          rot each fresh neighbour, fresh -= 1, push it
      minutes += 1
  return minutes if fresh == 0 else -1

Time O(rows * cols), space O(rows * cols).
"""
from collections import deque


def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue, fresh = deque(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))             # every rotten orange is a source
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):              # one layer = one minute
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2             # rot it
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1


if __name__ == "__main__":
    print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]))  # 4
    print(oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))  # -1
    print(oranges_rotting([[0, 2]]))                           # 0
