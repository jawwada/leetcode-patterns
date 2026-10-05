"""
01 Matrix (LeetCode 542) - Basics
Area: searches
Key operations: enqueue every source first (distance 0), layer-by-layer BFS, mark a cell when enqueued, first arrival = nearest source

For every cell of a 0/1 matrix return the distance to the nearest 0 (moving up/down/left/right).
Put ALL zeros in the queue at the start: one BFS then grows from every source at once, and the layer in
which a cell is first reached is its distance to the closest zero.
Example: [[0, 0, 0], [0, 1, 0], [1, 1, 1]] -> [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
"""
from collections import deque
from typing import List


def picture(dist):
    """Trace only: the grid, '.' where the distance is not known yet."""
    return "\n".join("    " + " ".join("." if d < 0 else str(d) for d in row) for row in dist)


# --- brute force ---
def brute_force(mat: List[List[int]]) -> List[List[int]]:
    """For every cell scan every zero and keep the smallest Manhattan distance (there are no walls, so that is the BFS distance). O((m*n)^2)."""
    m, n = len(mat), len(mat[0])
    zeros = [(r, c) for r in range(m) for c in range(n) if mat[r][c] == 0]
    return [[min(abs(r - zr) + abs(c - zc) for zr, zc in zeros) for c in range(n)] for r in range(m)]


# --- optimal ---
def solve(mat):
    """Multi-source BFS: all zeros start in the queue with distance 0; every other cell is reached once, in its layer. O(m*n)."""
    m, n = len(mat), len(mat[0])
    dist = [[0 if v == 0 else -1 for v in row] for row in mat]
    q = deque((r, c) for r in range(m) for c in range(n) if mat[r][c] == 0)
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
    return dist


# --- demo ---
def demo():
    return solve([[0, 0, 0], [0, 1, 0], [1, 1, 1]])


# --- bugs ---
BUGS = [
    {
        "replace": "    q = deque((r, c) for r in range(m) for c in range(n) if mat[r][c] == 0)",
        "with":    "    q = deque((r, c) for r in range(m) for c in range(n) if mat[r][c] == 1)",
        "fix": "the BFS starts from the ZEROS (the sources, distance 0), not from the cells we want distances for",
        "why": "The ones start with distance -1, so their unreached neighbours get -1 + 1 = 0: [[0, 1, 1, 1]] returns [[0, 1, 0, 1]].",
        "decoys": [
            {"line": "                    dist[nr][nc] = dist[r][c] + 1", "change": "should be dist[r][c]"},
            {"line": "    dist = [[0 if v == 0 else -1 for v in row] for row in mat]", "change": "should use None instead of -1"},
            {"line": "            r, c = q.popleft()", "change": "should be q.pop()"},
        ],
    },
    {
        "replace": "                    dist[nr][nc] = dist[r][c] + 1",
        "with":    "                    dist[nr][nc] = 1",
        "fix": "a neighbour is one step further than the cell it was reached from: dist[r][c] + 1",
        "why": "Every reached cell gets distance 1 regardless of its layer: [[0, 1, 1, 1]] returns [[0, 1, 1, 1]] instead of [[0, 1, 2, 3]].",
        "decoys": [
            {"line": "                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:", "change": "should be dist[nr][nc] != 0"},
            {"line": "        for _ in range(len(q)):", "change": "should be while q"},
            {"line": "    return dist", "change": "should return mat"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
