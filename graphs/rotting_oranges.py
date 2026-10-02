"""
Rotting Oranges (LeetCode 994)  — Medium
Pattern: Multi-source BFS (level = distance)

Problem
-------
In an m x n grid, 0 = empty, 1 = fresh orange, 2 = rotten orange. Every minute, each
rotten orange rots its 4-neighbouring fresh oranges. Return the minimum minutes until no
fresh orange remains, or -1 if impossible.
Example: [[2,1,1],[1,1,0],[0,1,1]] -> 4.  [[2,1,1],[0,1,1],[1,0,1]] -> -1.

Brute force
-----------
Simulate minute by minute: each round, scan the ENTIRE grid, and for every rotten orange
rot its fresh neighbours (into a copy so the round is simultaneous). Stop when a round
changes nothing. Each round is O(mn) and there can be O(mn) rounds (a snake-shaped
path), so O((mn)^2) time, O(mn) space. The waste: every round rescans all cells even
though only the oranges rotted in the PREVIOUS round can rot anything new.

From brute force to optimal
---------------------------
The redundancy is rescanning cells that cannot possibly change. Observation: the only
oranges that spread rot at minute t are those that became rotten at minute t-1, i.e.
the "frontier". Keep that frontier in a queue: this is exactly multi-source BFS where
every initially-rotten orange is a source and BFS depth equals the minute. Each cell is
enqueued once -> O(mn). Counting fresh oranges up front lets us detect the -1 case
without a second scan.

Intuition
---------
All rotten oranges spread simultaneously, so treat them as one BFS wave with many
sources. Each BFS layer is one minute. The answer is the number of layers it takes to
reach the last fresh orange; if the BFS finishes with fresh oranges unreached, return -1.

Geometric view
--------------
Picture ripples spreading from several stones dropped into a pond at the same instant.
Each ripple ring is one minute; where rings meet they just merge. The queue holds the
current ring. The time is the radius of the farthest ring needed to cover every fresh
orange; any fresh orange on an "island" cut off by empty cells is never reached.

Steps
-----
1. Scan once: enqueue every rotten cell, count fresh cells.
2. While queue non-empty and fresh > 0: process the whole current layer; for each fresh
   neighbour mark it rotten, decrement fresh, enqueue; after the layer, minutes += 1.
3. Return minutes if fresh == 0 else -1.

Complexity: O(m*n) time, O(m*n) space — each cell enters the queue at most once.
Pitfalls: incrementing minutes for the final empty layer (loop only while fresh > 0 or
subtract 1); returning 0 vs -1 confusion when there are no fresh oranges; mutating the
grid during the layer without level separation (would rot two steps in one minute).
"""
from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue, fresh = deque(), 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        minutes = 0
        while queue and fresh:
            for _ in range(len(queue)):  # one BFS layer == one minute
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))
            minutes += 1
        return minutes if fresh == 0 else -1


def brute_force(grid: List[List[int]]) -> int:
    # Full-grid simulation: each minute rescan every cell and rot fresh neighbours of
    # rotten ones (written to a copy so the step is simultaneous).
    rows, cols = len(grid), len(grid[0])
    minutes = 0
    while True:
        nxt = [row[:] for row in grid]
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            nxt[nr][nc] = 2
                            changed = True
        if not changed:
            break
        grid, minutes = nxt, minutes + 1
    return -1 if any(1 in row for row in grid) else minutes


if __name__ == "__main__":
    import copy

    s = Solution()
    cases = (
        ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
        ([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1),
        ([[0, 2]], 0),
        ([[1]], -1),
        ([[2, 1, 1, 1, 1]], 4),
    )
    for g, want in cases:
        assert brute_force(copy.deepcopy(g)) == want
        assert s.orangesRotting(copy.deepcopy(g)) == want
    print("ok")
