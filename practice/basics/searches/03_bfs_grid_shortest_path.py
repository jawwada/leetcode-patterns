"""
Shortest Path in a 0/1 Grid - Basics
Area: searches
Key operations: queue of cells, mark visited when enqueued, four directions with a bounds check, one layer = one step

Grid of 0 (free) and 1 (wall). Return the number of cells on a shortest path from the top-left to the
bottom-right moving up, down, left or right, or -1 if there is none. BFS explores in layers, so the first
time the target leaves the queue its distance is final.
Example: [[0, 0, 1], [1, 0, 0], [1, 1, 0]] -> 5, the path (0,0) (0,1) (1,1) (1,2) (2,2)
"""
from collections import deque
from typing import List


def picture(grid, dist):
    """Trace only: # for a wall, . for an unreached cell, otherwise the BFS distance."""
    rows = []
    for r, row in enumerate(grid):
        rows.append("    " + " ".join("#" if v else str(dist.get((r, c), ".")) for c, v in enumerate(row)))
    return "\n".join(rows)


# --- brute force ---
def brute_force(grid: List[List[int]]) -> int:
    """DFS over every simple path and keep the shortest. Exponential in the grid size; fine for 4x4."""
    m, n = len(grid), len(grid[0])
    best = [-1]

    def dfs(r, c, seen):
        if not (0 <= r < m and 0 <= c < n) or grid[r][c] or (r, c) in seen:
            return
        if (r, c) == (m - 1, n - 1):
            best[0] = len(seen) + 1 if best[0] == -1 else min(best[0], len(seen) + 1)
            return
        seen.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc, seen)
        seen.remove((r, c))
    dfs(0, 0, set())
    return best[0]


# --- optimal ---
def solve(grid):
    """BFS layer by layer; a cell is marked (given a distance) when it is ENQUEUED, so it enters the queue once. O(m*n)."""
    m, n = len(grid), len(grid[0])
    if grid[0][0] == 1:
        return -1
    dist = {(0, 0): 1}
    q = deque([(0, 0)])
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if (r, c) == (m - 1, n - 1):
                return dist[r, c]
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in dist:
                    dist[nr, nc] = dist[r, c] + 1
                    q.append((nr, nc))
    return -1


# --- demo ---
def demo():
    return solve([[0, 0, 1], [1, 0, 0], [1, 1, 0]])


# --- bugs ---
BUGS = [
    {
        "replace": "    dist = {(0, 0): 1}",
        "with":    "    dist = {(0, 0): 0}",
        "fix": "the start cell is already one cell on the path, so its distance is 1",
        "why": "Counting steps instead of cells: every answer is one too small, [[0]] returns 0 instead of 1.",
        "decoys": [
            {"line": "                    dist[nr, nc] = dist[r, c] + 1", "change": "should be dist[r, c]"},
            {"line": "    q = deque([(0, 0)])", "change": "should start empty"},
            {"line": "    if grid[0][0] == 1:", "change": "should also check the target cell"},
        ],
    },
    {
        "replace": "                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in dist:",
        "with":    "                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0:",
        "fix": "only enqueue a cell that has no distance yet; without the visited check cells bounce back and forth forever",
        "why": "Neighbours re-enqueue each other with ever larger distances; when there is no path the queue never empties: [[0, 1], [1, 0]] hangs.",
        "decoys": [
            {"line": "            if (r, c) == (m - 1, n - 1):", "change": "should be checked when enqueuing instead"},
            {"line": "            r, c = q.popleft()", "change": "should be q.pop()"},
            {"line": "        for _ in range(len(q)):", "change": "should be while q"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
