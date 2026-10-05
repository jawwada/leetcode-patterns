"""
Rotting Oranges (LeetCode 994) - Medium
Area: graphs
Key operations: enqueue every rotten source, process one layer per minute, rot fresh neighbours, count fresh left

In an m x n grid, 0 is empty, 1 is a fresh orange and 2 is a rotten orange. Every minute each
rotten orange rots the fresh oranges 4-directionally adjacent to it. Return the minimum number
of minutes until no fresh orange remains, or -1 if some fresh orange can never rot.
Example: [[2,1,1],[1,1,0],[0,1,1]] -> 4
"""
import sys
from collections import deque
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- helpers ---
def draw(grid: List[List[int]]) -> str:
    """Grid as text: . empty, o fresh, X rotten."""
    return "\n".join("    " + " ".join(".oX"[v] for v in row) for row in grid)


# --- brute force ---
def brute_force(grid: List[List[int]]) -> int:
    """Simulate minute by minute: each round rescan the WHOLE grid and rot every fresh neighbour of a
    rotten cell (into a copy, so the round is simultaneous); stop when a round changes nothing.
    Up to mn rounds of O(mn) work: O((mn)^2). The waste is rescanning cells that cannot change."""
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])
    minutes = 0
    while True:
        nxt = [row[:] for row in grid]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            nxt[nr][nc] = 2
        if nxt == grid:
            break
        grid, minutes = nxt, minutes + 1
    return -1 if any(1 in row for row in grid) else minutes


# --- optimal ---
def solve(grid: List[List[int]]) -> int:
    """Multi-source BFS: every rotten orange is a source, one BFS layer is one minute. Each cell
    enters the queue at most once: O(mn) time and space."""
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])
    queue, fresh = deque(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    log(f"minute 0 | fresh {fresh} | queue {list(queue)}")
    log(draw(grid))
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
                    log(f"    ({r},{c}) rots ({nr},{nc}); fresh left {fresh}")
        minutes += 1
        log(f"minute {minutes} | fresh {fresh} | queue (next layer) {list(queue)}")
        log(draw(grid))
    return minutes if fresh == 0 else -1


# --- demo ---
def demo():
    return solve([[2, 1, 1], [1, 1, 0], [0, 1, 1]])


# --- tests ---
def tests():
    assert solve([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert solve([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1  # (2,0) is cut off
    assert solve([[0, 2]]) == 0  # nothing fresh: zero minutes
    assert solve([[0]]) == 0
    assert solve([[1]]) == -1  # fresh with no rotten source
    assert solve([[2, 1]]) == 1
    assert solve([[1], [2]]) == 1  # rot must travel into row 0
    assert solve([[2, 1, 1, 1, 1]]) == 4
    assert solve([[2, 1, 1], [1, 1, 1], [1, 1, 2]]) == 2  # two sources meet in the middle
    import random
    random.seed(1)
    for _ in range(200):
        rows, cols = random.randint(1, 4), random.randint(1, 4)
        g = [[random.choice([0, 1, 1, 1, 1, 2, 2]) for _ in range(cols)] for _ in range(rows)]
        assert solve(g) == brute_force(g), g


# --- bugs ---
BUGS = [
    {
        "replace": "    while queue and fresh:",
        "with":    "    while queue:",
        "fix": "stop as soon as no fresh orange is left: while queue and fresh",
        "why": "The oranges rotted in the last minute still sit in the queue, so one more empty layer runs and minutes is one too big: [[2, 1]] returns 2 instead of 1.",
        "decoys": [
            {"line": "        for _ in range(len(queue)):", "change": "should be range(len(queue) - 1)"},
            {"line": "                    fresh -= 1", "change": "should happen only when the queue becomes empty"},
            {"line": "    return minutes if fresh == 0 else -1", "change": "should return minutes - 1 when fresh == 0"},
        ],
    },
    {
        "replace": "                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:",
        "with":    "                if 0 < nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:",
        "fix": "row 0 is a valid row: the bound check is 0 <= nr < rows",
        "why": "Rot can never travel into row 0, so [[1], [2]] returns -1 instead of 1 and any fresh orange in the top row is reported unreachable.",
        "decoys": [
            {"line": "                queue.append((r, c))", "change": "should append (c, r)"},
            {"line": "        minutes += 1", "change": "should be inside the inner for loop"},
            {"line": "    while queue and fresh:", "change": "should be while queue or fresh"},
        ],
    },
    {
        "replace": "    return minutes if fresh == 0 else -1",
        "with":    "    return minutes",
        "fix": "return -1 when fresh oranges remain: minutes if fresh == 0 else -1",
        "why": "A fresh orange walled off by empty cells is never reached, yet the elapsed minutes are returned: [[2,1,1],[0,1,1],[1,0,1]] returns 2 instead of -1.",
        "decoys": [
            {"line": "            elif grid[r][c] == 1:", "change": "should be elif grid[r][c] != 2"},
            {"line": "                    grid[nr][nc] = 2", "change": "should be done after the inner for loop"},
            {"line": "    queue, fresh = deque(), 0", "change": "fresh should start at rows * cols"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
