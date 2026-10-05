"""
Unique Paths III (LeetCode 980) - Hard
Chapter: backtracking
Pattern: Grid DFS backtracking with in-place visited marking

A grid holds one start (1), one end (2), empty cells (0) and obstacles (-1). Count the
4-directional walks from start to end that visit every empty cell exactly once and never
touch an obstacle or repeat a cell.
Example: [[1,0,0],[0,0,0],[2,0,0]] -> 2; [[0,1],[2,0]] -> 0.
"""
from itertools import permutations   # every ordering of a list


# --- brute force ---
def brute_force(grid):
    """Try every ordering of the empty cells, keep those that form an adjacent chain. O(k! * k)."""
    empties = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                start = (row, col)
            elif grid[row][col] == 2:
                end = (row, col)
            elif grid[row][col] == 0:
                empties.append((row, col))
    count = 0
    for order in permutations(empties):           # k! orderings, each checked only when complete
        chain = [start] + list(order) + [end]
        if is_adjacent_chain(chain):
            count += 1
    return count


def is_adjacent_chain(chain):
    """True when every consecutive pair of cells shares an edge."""
    for i in range(len(chain) - 1):
        row_gap = abs(chain[i][0] - chain[i + 1][0])
        col_gap = abs(chain[i][1] - chain[i + 1][1])
        if row_gap + col_gap != 1:
            return False
    return True


# --- optimal ---
def unique_paths_iii(grid):
    """DFS from the start, marking cells in place and counting cells still owed. O(4^(RC))."""
    todo = 1                                      # the end cell itself must be stepped on too
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 1:
                start_row, start_col = row, col
            elif grid[row][col] == 0:
                todo += 1
    return count_walks(grid, start_row, start_col, todo)


def count_walks(grid, row, col, todo):
    if grid[row][col] == 2:
        if todo == 0:                             # end reached with every empty cell used
            return 1
        return 0                                  # end reached too early: dead end
    saved = grid[row][col]
    grid[row][col] = -1                           # mark: this cell is on the path right now
    count = 0
    for next_row, next_col in ((row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)):
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            if grid[next_row][next_col] in (0, 2):
                count += count_walks(grid, next_row, next_col, todo - 1)
    grid[row][col] = saved                        # unmark on the way back
    return count


# --- try the brute force ---
print(brute_force([[1, 0, 0], [0, 0, 0], [2, 0, 0]]))       # -> 2
print(brute_force([[1, 0, 0], [0, -1, 0], [0, 0, 2]]))      # -> 0
print(brute_force([[0, 1], [2, 0]]))                        # -> 0
print(brute_force([[1, 2]]))                                # -> 1


# --- try the optimal ---
print(unique_paths_iii([[1, 0, 0], [0, 0, 0], [2, 0, 0]]))       # -> 2
print(unique_paths_iii([[1, 0, 0], [0, -1, 0], [0, 0, 2]]))      # -> 0
print(unique_paths_iii([[0, 1], [2, 0]]))                        # -> 0
print(unique_paths_iii([[1, 2]]))                                # -> 1
