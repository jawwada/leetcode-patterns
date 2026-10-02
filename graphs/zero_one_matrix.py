"""
01 Matrix (LeetCode 542)  — Medium
Pattern: Multi-source BFS (level = distance)

Problem
-------
Given an m x n binary matrix, return a matrix where each cell holds the distance to the
nearest 0, moving one step up/down/left/right. At least one 0 exists.
Example: [[0,0,0],[0,1,0],[1,1,1]] -> [[0,0,0],[0,1,0],[1,2,1]].

Brute force
-----------
For every 1-cell, run its own BFS outward until it hits the first 0. A single BFS can
touch the whole grid, so the total is O((m*n)^2) time, O(m*n) space. The waste: the
BFS from neighbouring cells re-explores almost the same region over and over, and no
cell reuses the distance its neighbour already found.

From brute force to optimal
---------------------------
The redundancy is running one BFS per 1-cell when every search is looking for the same
target set: "any 0". Reverse the direction: start ONE BFS from ALL zeros at once (every 0
is at distance 0, enqueued together). BFS settles cells in nondecreasing distance order,
so the first time the wave reaches a 1-cell, that is its distance to the nearest 0, and
dist[cell] = dist[parent] + 1. Each cell is enqueued once -> O(m*n). The user's original
version (init 1-cells to m*n, relax when a shorter distance is found) is this same BFS.

Intuition
---------
"Nearest 0 to each cell" equals "distance from the set of all zeros". Treat the zeros as
a single super-source; one BFS from it answers every cell in one sweep.

Geometric view
--------------
Every 0 drops a stone in the pond at the same instant. Ripples expand one ring per step;
the ring number at which a cell first gets wet is its answer. The queue holds the current
ring; rings from different zeros merge where they meet.

Steps
-----
1. dist = 0 for zeros (enqueue them), m*n (unknown) for ones.
2. Pop (r, c); for each in-bounds neighbour with dist > dist[r][c] + 1, set it and enqueue.
3. When the queue empties, return dist.

Complexity: O(m*n) time, O(m*n) space — each cell is improved and enqueued at most once.
Pitfalls: BFS-ing from each 1 (quadratic); using DFS (does not give shortest distance);
forgetting to seed ALL zeros before starting.
"""
from collections import deque
from typing import List


class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        dist = [[0 if mat[r][c] == 0 else m * n for c in range(n)] for r in range(m)]
        queue = deque((r, c) for r in range(m) for c in range(n) if mat[r][c] == 0)
        while queue:
            r, c = queue.popleft()
            nd = dist[r][c] + 1
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] > nd:
                    dist[nr][nc] = nd  # first (shortest) arrival of the wave
                    queue.append((nr, nc))
        return dist


def brute_force(mat: List[List[int]]) -> List[List[int]]:
    # Independent BFS from every cell until it finds a 0: O((m*n)^2).
    m, n = len(mat), len(mat[0])
    out = [[0] * n for _ in range(m)]
    for sr in range(m):
        for sc in range(n):
            seen, queue = {(sr, sc)}, deque([(sr, sc, 0)])
            while queue:
                r, c, d = queue.popleft()
                if mat[r][c] == 0:
                    out[sr][sc] = d
                    break
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        queue.append((nr, nc, d + 1))
    return out


if __name__ == "__main__":
    s = Solution()
    cases = [([[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
             ([[0, 0, 0], [0, 1, 0], [1, 1, 1]], [[0, 0, 0], [0, 1, 0], [1, 2, 1]]),
             ([[0]], [[0]]),
             ([[1, 1, 1, 1, 0]], [[4, 3, 2, 1, 0]])]
    for mat, want in cases:
        assert s.updateMatrix(mat) == want
        assert brute_force(mat) == want
    print("ok")
