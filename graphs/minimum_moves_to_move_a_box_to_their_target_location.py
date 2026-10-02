"""
Minimum Moves to Move a Box to Their Target Location (LeetCode 1263)  — Hard
Pattern: 0-1 BFS over (box, player) states (player steps cost 0, pushes cost 1)

Problem
-------
A grid holds walls '#', floor '.', the player 'S', a box 'B' and the target 'T'. The player walks
4-directionally on floor; standing next to the box and walking into it pushes the box one cell in
that direction if that cell is floor. Return the minimum number of PUSHES to bring the box onto
the target, or -1. Player walking is free.
Example (3 pushes): the player walks up to the right of the box at (2,3) and pushes it left twice
to (2,1), then walks round below it and pushes it up once onto T at (1,1):
    # # # # # #
    # T # # # #
    # . . B . #
    # . # # . #
    # . . . S #
    # # # # # #

Brute force
-----------
The state is (box, player); a move either walks the player (weight 0) or pushes the box
(weight 1), so the obvious correct approach is Dijkstra with a binary heap over all
(R*C)^2 states: pop the cheapest state, relax the four moves. O(S log S) time and O(S) space with
S = (R*C)^2 states (up to 160 000 for a 20x20 grid). The waste: the heap sorts keys that only
ever take two values at any moment (d and d + 1), paying O(log S) per push/pop to maintain an
order that a deque could keep for free.

From brute force to optimal
---------------------------
The redundancy is the heap. Observation: with edge weights restricted to {0, 1}, a deque can play
the role of the priority queue - relax a 0-cost edge by pushing to the FRONT and a 1-cost edge by
pushing to the BACK, and the deque stays sorted by distance (all d's before all d+1's). That is
0-1 BFS: Dijkstra's correctness with BFS's O(1) per edge, so the search is O(S) over the
(box, player) state space. The invariant is "dist[state] is final when popped from the front";
we keep a dist map and skip relaxations that do not improve. The first time a state with the box
on the target is popped, its distance is the push count. (An equivalent view: BFS on box
positions where each layer recomputes the player's reachable region; 0-1 BFS fuses that inner
reachability walk into the main search so no region is recomputed.)

Intuition
---------
Two agents, one objective: minimise pushes, not steps. Walking is free, so the player's
wandering is a zero-cost move in a weighted graph whose only paid action is a push. Pushing
requires the player to be on the opposite side of the box - that is encoded automatically because
the player can only push by stepping INTO the box, carrying both forward.

Geometric view
--------------
Each box position is a "room"; inside a room the player roams freely on cells not blocked by walls
or the box (cost 0 edges, drawn as thin lines). A thick arrow leaves the room when the player
stands behind the box and walks into it: the box advances one cell and the player takes the box's
old cell (cost 1). 0-1 BFS floods a room completely (front-pushes) before taking any thick arrow
(back-pushes), so the number of thick arrows on the first route into the target room is minimal.

Steps
-----
1. Locate S, B, T. State = (br, bc, pr, pc); dist = {start: 0}; deque = [start].
2. Pop from the left; if the box is on T return its distance.
3. For each direction: the player's next cell must be in bounds and not a wall.
4. If that cell is the box: the cell beyond must be free; new state (box+d, box) with cost 1
   (append right). Else new state (box, player+d) with cost 0 (append left).
5. Relax only if the new distance is smaller; return -1 if the deque empties.

Complexity: O((R*C)^2) time and space — at most R*C box positions times R*C player positions,
each relaxed with 4 moves in O(1).
Pitfalls: counting player steps instead of pushes; a visited set on box positions alone (the
side the player is on matters); letting the player walk through the box; not checking the cell
beyond the box before a push; forgetting that dist must be re-checked when the same state is
pushed twice (front and back).
"""
import heapq
from collections import deque
from typing import List


class Solution:
    def minPushBox(self, grid: List[List[str]]) -> int:
        R, C = len(grid), len(grid[0])
        for r in range(R):
            for c in range(C):
                if grid[r][c] == "S":
                    pr, pc = r, c
                elif grid[r][c] == "B":
                    br, bc = r, c
                elif grid[r][c] == "T":
                    tr, tc = r, c

        def free(r: int, c: int) -> bool:
            return 0 <= r < R and 0 <= c < C and grid[r][c] != "#"

        start = (br, bc, pr, pc)
        dist = {start: 0}
        dq = deque([start])
        while dq:
            state = dq.popleft()
            br, bc, pr, pc = state
            d = dist[state]
            if (br, bc) == (tr, tc):
                return d
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = pr + dr, pc + dc                     # where the player steps
                if not free(nr, nc):
                    continue
                if (nr, nc) == (br, bc):                      # stepping into the box = push
                    if not free(br + dr, bc + dc):
                        continue
                    nxt, cost = (br + dr, bc + dc, nr, nc), 1
                else:
                    nxt, cost = (br, bc, nr, nc), 0
                if d + cost < dist.get(nxt, float("inf")):
                    dist[nxt] = d + cost
                    (dq.append if cost else dq.appendleft)(nxt)   # 0-1 BFS: deque stays sorted
        return -1


def brute_force(grid: List[List[str]]) -> int:
    # Dijkstra with a heap over the same (box, player) states; weights are only 0 and 1.
    R, C = len(grid), len(grid[0])
    find = lambda ch: next((r, c) for r in range(R) for c in range(C) if grid[r][c] == ch)
    (pr, pc), (br, bc), target = find("S"), find("B"), find("T")
    free = lambda r, c: 0 <= r < R and 0 <= c < C and grid[r][c] != "#"
    heap, best = [(0, br, bc, pr, pc)], {(br, bc, pr, pc): 0}
    while heap:
        d, br, bc, pr, pc = heapq.heappop(heap)             # O(log S) per operation
        if (br, bc) == target:
            return d
        if d > best[(br, bc, pr, pc)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = pr + dr, pc + dc
            if not free(nr, nc) or ((nr, nc) == (br, bc) and not free(br + dr, bc + dc)):
                continue
            nxt = (br + dr, bc + dc, nr, nc) if (nr, nc) == (br, bc) else (br, bc, nr, nc)
            nd = d + ((nr, nc) == (br, bc))
            if nd < best.get(nxt, float("inf")):
                best[nxt] = nd
                heapq.heappush(heap, (nd, *nxt))
    return -1


if __name__ == "__main__":
    s = Solution()
    g = lambda rows: [list(r) for r in rows]
    cases = (
        (g(["######", "#T####", "#..B.#", "#.##.#", "#...S#", "######"]), 3),
        (g(["######", "#T####", "#..B.#", "####.#", "#...S#", "######"]), -1),   # cannot get behind
        (g(["######", "#T..##", "#.#B.#", "#....#", "#...S#", "######"]), 5),
        (g(["######", "#.T..#", "#....#", "#..B.#", "#S...#", "######"]), 3),
        (g(["#####", "#.T.#", "#...#", "#.#.#", "#S.B#", "#####"]), -1),        # box wedged in a corner
        (g(["TB.S"]), 1),
        (g(["T.BS."]), 2),
    )
    for grid, want in cases:
        assert s.minPushBox([row[:] for row in grid]) == want, grid
        assert brute_force(grid) == want, grid
    print("ok")
