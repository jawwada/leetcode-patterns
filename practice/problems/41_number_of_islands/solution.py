"""
Number of Islands (LeetCode 200) - Medium
Area: graphs
Key operations: scan for unvisited land, flood fill with a stack, mark visited on push, count the floods

Given an m x n grid of '1' (land) and '0' (water), count the islands: maximal groups of '1's
connected up / down / left / right. The grid must not be modified.
Example: [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]] -> 3
"""
from typing import List


# --- helpers ---
def draw(grid: List[List[str]], seen: List[List[bool]]) -> str:
    """Rows joined by ' / ': '#' visited land, '1' land not yet visited, '0' water."""
    return " / ".join("".join("#" if seen[r][c] else ch for c, ch in enumerate(row)) for r, row in enumerate(grid))


# --- brute force ---
def brute_force(grid: List[List[str]]) -> int:
    """Union-find over the land cells: union every land cell with its right and down land neighbours,
    then count the distinct roots. O(mn * alpha(mn)) with a parent table and two finds per edge; the
    flood fill needs no parent structure at all and touches each cell exactly once."""
    rows, cols = len(grid), len(grid[0])
    parent = {(r, c): (r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "1"}

    def find(p):
        while parent[p] != p:
            p = parent[p]
        return p

    for r, c in list(parent):
        for nb in ((r + 1, c), (r, c + 1)):
            if nb in parent:
                parent[find(nb)] = find((r, c))
    return len({find(p) for p in parent})


# --- optimal ---
def solve(grid: List[List[str]]) -> int:
    """Scan every cell; an unvisited '1' is a new island, flooded with a stack. Cells are marked visited
    the moment they are pushed, so each is pushed at most once. O(mn) time, O(mn) space."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True
                stack = [(r, c)]
                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "1" and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))
    return count


# --- demo ---
def demo():
    grid = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
    return solve(grid)


# --- bugs ---
BUGS = [
    {
        "replace": "            if grid[r][c] == \"1\" and not seen[r][c]:",
        "with":    "            if grid[r][c] == \"1\":",
        "fix": "start a flood only from land that is not visited yet; a flooded island is already counted",
        "why": "Every land cell starts its own flood and bumps count, so the example returns 7 (one per land cell) instead of 3.",
        "decoys": [
            {"line": "                    x, y = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    seen = [[False] * cols for _ in range(rows)]", "change": "should be [[False] * rows for _ in range(cols)]"},
            {"line": "    return count", "change": "should return count - 1"},
        ],
    },
    {
        "replace": "                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == \"1\" and not seen[nx][ny]:",
        "with":    "                        if 0 <= nx < cols and 0 <= ny < rows and grid[nx][ny] == \"1\" and not seen[nx][ny]:",
        "fix": "rows bounds the row index nx and cols bounds the column index ny",
        "why": "On a non-square grid the swapped bounds index past the last row (IndexError) or refuse valid rows, splitting one island into several.",
        "decoys": [
            {"line": "                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):", "change": "should include the four diagonal neighbours"},
            {"line": "                            seen[nx][ny] = True", "change": "should be set when the cell is popped instead"},
            {"line": "                count += 1", "change": "should move after the while loop"},
        ],
    },
    {
        "replace": "                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):",
        "with":    "                    for nx, ny in ((x + 1, y), (x, y + 1)):",
        "fix": "look in all four directions: an island can bend back up or to the left of the scan",
        "why": "Only down and right are explored, so [['1','1','1'],['0','0','1'],['1','1','1']] is counted as 2 islands: the bottom-left arm is never reached from the top.",
        "decoys": [
            {"line": "                seen[r][c] = True", "change": "should be set after the while loop"},
            {"line": "                stack = [(r, c)]", "change": "should start empty"},
            {"line": "    rows, cols = len(grid), len(grid[0])", "change": "should be len(grid[0]), len(grid)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
