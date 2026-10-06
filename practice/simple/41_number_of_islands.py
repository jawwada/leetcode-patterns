"""
Number of Islands (LeetCode 200)
Count groups of '1' cells connected up/down/left/right in a grid of '1' (land) and '0' (water).
  grid = ["11000", "11000", "00100", "00011"]  ->  3

Idea: scan every cell. An unvisited '1' starts a new island: count it, then flood fill
      the whole island with a stack so none of its cells is counted again.
      Mark a cell visited the moment it is pushed, so each cell is pushed once.

Pseudocode:
  for each cell (r, c):
      if land and not seen:
          count += 1; mark seen; stack = [(r, c)]
          while stack:
              pop (x, y)
              for each land neighbour not seen: mark seen, push it
  return count

Time O(m * n), space O(m * n).
"""


def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:       # new island
                count += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:                               # flood fill it
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1" and not seen[nx][ny]:
                            seen[nx][ny] = True            # mark on push
                            stack.append((nx, ny))
    return count


if __name__ == "__main__":
    print(num_islands(["11000", "11000", "00100", "00011"]))  # 3
    print(num_islands(["11110", "11010", "11000", "00000"]))  # 1
