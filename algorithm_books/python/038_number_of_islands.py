"""
Number of Islands - Grid Flood Fill

Given a grid of "1" (land) and "0" (water), count the islands: groups of land
cells joined up, down, left or right, never diagonally:
["11000", "11000", "00100", "00011"] -> 3.
"""


# --- helpers ---
def make_grid(rows):
    """Turn a list of strings into a grid of one-character cells."""
    grid = []
    for row in rows:
        grid.append(list(row))
    return grid


# --- algorithm ---
def num_islands(grid):
    """Each '1' the scan meets starts a fill that sinks its island. O(R * C)."""
    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "1":
                count += 1                  # a new island starts here
                sink(grid, row, col)        # so it is never counted again
    return count


def sink(grid, start_row, start_col):
    """Explicit-stack DFS: turn every land cell of one island into water."""
    stack = []
    stack.append((start_row, start_col))
    while stack:
        row, col = stack.pop()
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            continue                        # stepped off the map
        if grid[row][col] != "1":
            continue                        # water, or land already sunk
        grid[row][col] = "0"                # sinking is the visited mark
        stack.append((row + 1, col))        # down, up, right, left
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))


# --- try it ---
grid = make_grid(["11000", "11000", "00100", "00011"])
print(num_islands(grid))                    # -> 3
grid = make_grid(["11110", "11010", "11000", "00000"])
print(num_islands(grid))                    # -> 1
print(num_islands(make_grid(["101", "010", "101"])))    # -> 5
print(num_islands(make_grid(["0"])))        # -> 0
