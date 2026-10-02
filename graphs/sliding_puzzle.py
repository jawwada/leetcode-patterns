"""
Sliding Puzzle (LeetCode 773)  — Hard
Pattern: BFS over board strings (implicit state graph, precomputed blank-neighbour table)

Problem
-------
A 2x3 board holds the tiles 1..5 and one blank 0. A move swaps the blank with a 4-directionally
adjacent tile. Return the minimum number of moves to reach [[1,2,3],[4,5,0]], or -1 if the board
is unsolvable.
Example: [[1,2,3],[4,0,5]] -> 1 (slide the 5 left).  [[1,2,3],[5,4,0]] -> -1.
[[4,1,2],[5,0,3]] -> 5.

Brute force
-----------
BFS over boards, but discover a board's neighbours the naive way: compare it against every one of
the 6! = 720 arrangements of "012345" and keep those that differ from it by one legal swap of the
blank. Each expansion costs O(720 * 6) and up to 360 boards are expanded, so O(S^2 * 6) with
S = 720 states, O(S) space. The waste: for every board, 719 candidate boards are scanned although
at most 3 of them are real neighbours, and the blank's position already tells you which 2 or 3
swaps are possible.

From brute force to optimal
---------------------------
The redundancy is the full scan to find neighbours that could be generated directly. Observation:
a move is determined by the blank's index and one of its at most 3 grid neighbours; flatten the
board into a 6-character string so a state is hashable, and precompute the adjacency of the six
cells once (index i touches i-1, i+1 within a row, and i +- 3 across rows). A neighbour of a board
is then "swap the blank with one adjacent index", O(1) each, so BFS over the implicit graph costs
O(S) with S <= 720 states, each visited once thanks to a set of seen strings. Unit moves mean BFS
depth is the move count, and an empty queue means the board is in the unreachable half of the
state space (parity), so return -1.

Intuition
---------
The puzzle is a shortest-path question on a graph whose nodes are board configurations, too many
to draw but tiny enough to search exhaustively (360 reachable). Everything hinges on a hashable
state (the string), a cheap neighbour function (swap with an adjacent index) and a visited set.

Geometric view
--------------
Nodes are 6-character strings; an edge is a swap of '0' with an adjacent position. BFS rings grow
from the start string; the ring number at which "123450" first appears is the answer.

    start "412503"   blank at 4 -> neighbours of 4: {1, 3, 5}
    ring1  "402513"  "412053"  "412530"
    ring2  ... each new string is pushed only if unseen
    ring5  "123450"  -> return 5

Steps
-----
1. nbr = [[1,3],[0,2,4],[1,5],[0,4],[1,3,5],[2,4]]; start = flattened board string.
2. queue = [(start, 0)], seen = {start}.
3. Pop (s, d); if s == "123450" return d.
4. i = s.index("0"); for j in nbr[i]: swap s[i] and s[j] into t; if unseen, mark and push (t, d+1).
5. Return -1 when the queue empties.

Complexity: O(S * 6) time, O(S) space with S = 720 boards — each state is expanded once with at
most 3 neighbours, each built in O(6).
Pitfalls: using a list of lists as the visited key (unhashable); hardcoding the adjacency with a
wrong wrap (index 2 and 3 are not adjacent); marking visited on pop (duplicates in the queue);
forgetting the -1 case.
"""
from collections import deque
from itertools import permutations
from typing import List


class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        nbr = [[1, 3], [0, 2, 4], [1, 5], [0, 4], [1, 3, 5], [2, 4]]   # grid adjacency of indices
        start = "".join(str(x) for row in board for x in row)
        queue = deque([(start, 0)])
        seen = {start}
        while queue:
            s, d = queue.popleft()
            if s == "123450":
                return d
            i = s.index("0")
            for j in nbr[i]:                                            # slide a neighbouring tile
                t = list(s)
                t[i], t[j] = t[j], t[i]
                t = "".join(t)
                if t not in seen:
                    seen.add(t)
                    queue.append((t, d + 1))
        return -1


def brute_force(board: List[List[int]]) -> int:
    # BFS, but neighbours are found by scanning all 720 arrangements for one-move differences.
    boards = ["".join(p) for p in permutations("012345")]
    nbr = [[1, 3], [0, 2, 4], [1, 5], [0, 4], [1, 3, 5], [2, 4]]

    def one_move(a: str, b: str) -> bool:
        diff = [i for i in range(6) if a[i] != b[i]]
        return len(diff) == 2 and "0" in (a[diff[0]], a[diff[1]]) and diff[1] in nbr[diff[0]]

    start = "".join(str(x) for row in board for x in row)
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        s, d = queue.popleft()
        if s == "123450":
            return d
        for t in boards:                                     # 719 failed comparisons per board
            if t not in seen and one_move(s, t):
                seen.add(t)
                queue.append((t, d + 1))
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = (
        ([[1, 2, 3], [4, 0, 5]], 1),
        ([[1, 2, 3], [5, 4, 0]], -1),
        ([[4, 1, 2], [5, 0, 3]], 5),
        ([[1, 2, 3], [4, 5, 0]], 0),                      # already solved
        ([[3, 2, 4], [1, 5, 0]], 14),
    )
    for board, want in cases:
        assert s.slidingPuzzle(board) == want, board
    for board, want in cases[:3]:
        assert brute_force(board) == want, board
    print("ok")
