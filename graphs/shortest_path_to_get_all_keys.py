"""
Shortest Path to Get All Keys (LeetCode 864)  — Hard
Pattern: BFS over augmented states (position + bitmask/budget)

Problem
-------
A grid has '.' empty cells, '#' walls, '@' the start, lowercase letters as keys and the matching
uppercase letters as locks. You may walk 4-directionally over empty cells and keys (picking a key
up automatically) and through a lock only if you hold its key. Return the fewest moves to collect
every key, or -1. There are at most 6 keys (a..f, with exactly one of each lock/key pair).
Example: ["@.a..","###.#","b.A.B"] -> 8 (walk around to a, then back through A to b).
["@..aA",".#B#.","....b"] -> 6.  ["@Aa"] -> -1.

Brute force
-----------
Choose the order in which the k keys will be collected (k! permutations). For each order run a
BFS from the current position to the next key, where the locks you may pass are those whose keys
have already been collected; sum the segment lengths and take the best order.
O(k! * k * R * C) time, O(R * C) space; exponential in k. The waste: the segment "from key a to
key b holding {a}" is recomputed inside every one of the (k-2)! orders that start with a, b, and
more generally BFS runs from the same (position, key set) over and over.

From brute force to optimal
---------------------------
The redundancy is re-running searches from identical situations. Observation: the situation is
fully described by (row, col, set of keys held); nothing else about the history matters. With k <= 6
the key set is a 6-bit mask, so there are at most R * C * 2^k states, and every step is a unit edge
between states (moving into a key cell ORs its bit into the mask; a lock cell is passable iff its
bit is set). One BFS over this state graph, seeded at (start, 0), finds the first state whose mask
is full at the minimum number of moves. The visited set is on states, so walking back over a cell
with more keys than before is allowed - that is exactly what "fetch b, then come back through A"
needs.

Intuition
---------
Standard grid BFS fails because passability changes as you pick up keys. Make the keys part of
the position: the same cell with a different key ring is a different place. The state space is
small (grid times 64), BFS on it is ordinary, and the target is "any cell, full key ring".

Geometric view
--------------
2^k stacked copies of the grid, one per key ring. Walking moves you inside a copy; stepping on an
uncollected key teleports you to the copy with that bit added (same cell); locks are walls in the
copies that lack the key and floor in those that have it. BFS ripples outward across copies; the
answer is the depth of the first cell reached in the all-keys copy.

Steps
-----
1. Scan the grid: find '@' and OR every key's bit into full (full == 0 -> answer 0).
2. queue = [(r0, c0, 0)], seen = {(r0, c0, 0)}, steps = 0; BFS layer by layer.
3. Pop (r, c, mask); if mask == full return steps. For each neighbour: skip walls and out of
   bounds; if lowercase, nm = mask | bit(ch); if uppercase and the bit is missing, skip.
4. Push (nr, nc, nm) if unseen; after each layer, steps += 1.
5. Return -1 when the queue empties.

Complexity: O(R * C * 2^k) time and space — each state is dequeued once with 4 neighbours.
Pitfalls: marking visited by cell instead of (cell, mask); treating a key cell as "must pick up
later" (pick-up is automatic); using ord(ch) - ord('A') for keys and ord('a') for locks swapped;
counting the key-cell step twice.
"""
from collections import deque
from itertools import permutations
from typing import List, Optional, Tuple


class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        R, C = len(grid), len(grid[0])
        full = 0                                      # bitmask of every key on the grid
        for r in range(R):
            for c in range(C):
                if grid[r][c] == "@":
                    sr, sc = r, c
                elif grid[r][c].islower():
                    full |= 1 << (ord(grid[r][c]) - 97)
        queue = deque([(sr, sc, 0)])                  # (row, col, keys-held bitmask)
        seen = {(sr, sc, 0)}
        steps = 0
        while queue:
            for _ in range(len(queue)):               # one BFS layer = one move
                r, c, mask = queue.popleft()
                if mask == full:
                    return steps
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if not (0 <= nr < R and 0 <= nc < C) or grid[nr][nc] == "#":
                        continue
                    ch, nm = grid[nr][nc], mask
                    if ch.islower():
                        nm |= 1 << (ord(ch) - 97)     # pick the key up
                    elif ch.isupper() and not mask >> (ord(ch) - 65) & 1:
                        continue                      # locked and no key
                    if (nr, nc, nm) not in seen:
                        seen.add((nr, nc, nm))
                        queue.append((nr, nc, nm))
            steps += 1
        return -1


def brute_force(grid: List[str]) -> int:
    # Try every pickup order; BFS each leg with only the keys collected so far. k! * BFS.
    R, C = len(grid), len(grid[0])
    pos = {ch: (r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "@" or ch.islower()}
    keys = sorted(k for k in pos if k != "@")

    def bfs(src: Tuple[int, int], dst: Tuple[int, int], held: set) -> Optional[int]:
        dist, queue = {src: 0}, deque([src])
        while queue:
            r, c = queue.popleft()
            if (r, c) == dst:
                return dist[(r, c)]
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and (nr, nc) not in dist \
                        and not (grid[nr][nc].isupper() and grid[nr][nc].lower() not in held):
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))
        return None

    best = -1
    for order in permutations(keys):                  # same (position, key set) re-searched
        total, cur, held = 0, pos["@"], set()
        for k in order:
            leg = bfs(cur, pos[k], held)
            if leg is None:
                break
            total, cur = total + leg, pos[k]
            held.add(k)
        else:
            best = total if best < 0 else min(best, total)
    return best


if __name__ == "__main__":
    s = Solution()
    cases = (
        (["@.a..", "###.#", "b.A.B"], 8),
        (["@..aA", ".#B#.", "....b"], 6),               # must fetch a first
        (["@Aa"], -1),
        (["@", ".", "a"], 2),                          # one key straight down
        (["@...a", ".###.", "b.B.A", "..C..", "c...."], 12),
        (["@."], 0),                                   # no keys at all
    )
    for g, want in cases:
        assert s.shortestPathAllKeys(g) == want, g
        if want != 0:
            assert brute_force(g) == want, g
    print("ok")
