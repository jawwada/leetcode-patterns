"""
Number of Islands (LeetCode 200) - Medium
Chapter: graphs
Pattern: Grid flood fill (DFS/BFS)

Given an m x n grid of '1' (land) and '0' (water), count the islands, where an island is a
maximal group of '1' cells connected horizontally or vertically.
Example: [["1","1","0"],["0","1","0"],["0","0","1"]] -> 2 (the L-shape top-left and the lone
cell bottom-right).
"""


# --- brute force ---
def brute_force(grid):
    """From each land cell walk its whole island; count it only at its smallest cell. O((mn)^2)"""
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            seen = {(r, c)}          # a private visited set: nothing is shared between starts
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                        if (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
            if min(seen) == (r, c):  # count the island once, from its first cell in scan order
                count += 1
    return count


# --- optimal ---
def sink(grid, r, c):
    """Turn the whole island containing (r, c) into water, using a stack. O(island size)."""
    rows = len(grid)
    cols = len(grid[0])
    grid[r][c] = "0"
    stack = [(r, c)]
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1":
                grid[nx][ny] = "0"       # mark on push, not on pop, so no cell is pushed twice
                stack.append((nx, ny))


def number_of_islands(grid):
    """Scan the grid; a land cell still standing is a new island: count it, then sink it. O(mn)."""
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "1":
                count += 1
                sink(grid, r, c)     # afterwards no cell of this island can start another count
    return count


# --- try the brute force ---
print(brute_force([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]))                # -> 2
print(brute_force([["1", "1", "0", "1"], ["1", "0", "0", "0"], ["0", "0", "1", "1"]]))  # -> 3
print(brute_force([["0"]]))                                                            # -> 0
print(brute_force([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]))                # -> 5


# --- try the optimal ---
print(number_of_islands([["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]))          # -> 2
print(number_of_islands([["1", "1", "0", "1"], ["1", "0", "0", "0"], ["0", "0", "1", "1"]])) # -> 3
print(number_of_islands([["0"]]))                                                      # -> 0
print(number_of_islands([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]))          # -> 5
