"""
Walls and Gates (LeetCode 286)  — Medium
Pattern: Multi-source BFS (level = distance)

Problem
-------
Given an m x n grid where -1 is a wall, 0 is a gate and INF (2**31 - 1) is an empty room,
fill each empty room with the distance to its nearest gate. Rooms unreachable from any
gate stay INF. Modify in place.
Example: [[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]
-> [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]].

Brute force
-----------
For every empty room, run its own BFS until the first gate is found and write that depth.
Each BFS is O(mn), there are up to mn rooms -> O((mn)^2) time, O(mn) space. The wasted
work: two adjacent rooms explore almost identical regions, and the same gate is
"discovered" once per room instead of once in total.

From brute force to optimal
---------------------------
The redundancy is computing shortest paths room-by-room when all queries share the same
targets. Observation: the distance from a room to its nearest gate equals the distance
from the SET of gates to that room, and a BFS seeded with every gate at depth 0 computes
exactly that for all rooms at once (the first time a wave reaches a room, it came from
the closest gate). One traversal, each cell relaxed once -> O(mn). The INF value itself
acts as the visited marker: only cells still INF are enqueued.

Intuition
---------
Flip the direction: instead of rooms searching for gates, gates flood toward rooms. Put
all gates in the queue; expand layer by layer, writing depth into each INF cell when it is
first reached. Because BFS visits cells in increasing distance, the first write is final.

Geometric view
--------------
Picture every gate as a source of light switching on simultaneously. Light spreads one
cell per tick through empty rooms and is blocked by walls. The queue is the glowing ring
of cells reached at the current tick; each room records the tick at which it first lit
up. Rooms in sealed chambers never light up and keep INF.

Steps
-----
1. Enqueue every gate (value 0).
2. Pop (r, c); for each in-bounds neighbour whose value is INF, set it to
   rooms[r][c] + 1 and enqueue it.
3. Stop when the queue is empty.

Complexity: O(m*n) time, O(m*n) space — every cell is enqueued at most once.
Pitfalls: starting one BFS per room (quadratic); checking `!= -1` instead of `== INF` and
overwriting gates or already-set rooms; forgetting level separation is NOT needed here
because we propagate rooms[r][c] + 1 rather than a layer counter.
"""
from collections import deque
from typing import List

INF = 2**31 - 1


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        rows, cols = len(rooms), len(rooms[0])
        queue = deque((r, c) for r in range(rows) for c in range(cols) if rooms[r][c] == 0)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1  # first arrival is the nearest gate
                    queue.append((nr, nc))


def brute_force(rooms: List[List[int]]) -> None:
    # One BFS per empty room, stopping at the first gate it reaches.
    rows, cols = len(rooms), len(rooms[0])
    result = [row[:] for row in rooms]
    for r0 in range(rows):
        for c0 in range(cols):
            if rooms[r0][c0] != INF:
                continue
            seen, queue = {(r0, c0)}, deque([(r0, c0, 0)])
            while queue:
                r, c, d = queue.popleft()
                if rooms[r][c] == 0:
                    result[r0][c0] = d
                    break
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] != -1 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        queue.append((nr, nc, d + 1))
    for r in range(rows):
        rooms[r][:] = result[r]


if __name__ == "__main__":
    import copy

    s = Solution()
    g1 = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
    w1 = [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
    g2 = [[-1]]
    g3 = [[INF, -1, 0]]  # left room is sealed off
    w3 = [[INF, -1, 0]]
    g4 = [[0, INF, INF, 0]]
    w4 = [[0, 1, 1, 0]]
    for g, want in ((g1, w1), (g2, [[-1]]), (g3, w3), (g4, w4)):
        a, b = copy.deepcopy(g), copy.deepcopy(g)
        s.wallsAndGates(a)
        brute_force(b)
        assert a == want and b == want
    print("ok")
