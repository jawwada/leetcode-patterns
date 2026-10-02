"""
Number of Islands II (LeetCode 305)  — Hard
Pattern: Union-Find (disjoint set union)

Problem
-------
An m x n grid starts as all water. positions[i] = (r, c) turns that cell into land, one
operation at a time. After each operation report the number of islands (4-directionally
connected land groups). The same cell may be added twice; the second add changes nothing.
Example: m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]] -> [1,1,2,3].

Brute force
-----------
Keep the grid; after each addition flood-fill (BFS/DFS) the whole grid from scratch to
count islands. Each recount is O(m*n), done k = len(positions) times -> O(k*m*n) time,
O(m*n) space. The waste: every recount rediscovers the same islands that existed one step
earlier -- only the neighbourhood of the newly added cell can have changed.

From brute force to optimal
---------------------------
The redundancy is recomputing global connectivity when only one cell changed. Observation:
adding a land cell creates ONE new island, then merges it with each distinct neighbouring
island -- islands only ever merge, never split, so the count after an add is
count + 1 - (number of distinct neighbouring islands). "Distinct island?" is exactly the
same-root question a disjoint-set union answers in near-constant amortised time, and the
merge is a union. Each operation touches at most 4 neighbours -> O(k * alpha(mn)) total.

Intuition
---------
Treat every land cell as a node in a union-find keyed by r*n + c. A new cell starts as its
own island (count += 1). Look at its 4 neighbours; for each one that is land and whose
root differs from the new cell's root, union them and decrement the count. A repeated
position is a no-op: report the current count unchanged.

Geometric view
--------------
Picture land tiles being dropped onto a blue board one at a time. Each dropped tile raises
a new flag; if it touches tiles flying other flags, those flags are lowered one by one and
the groups merge. The island count is simply the number of flags still standing, and it
changes by +1 minus the number of flags lowered on this drop.

Steps
-----
1. parent = {}, rank = {}, count = 0, out = [].
2. For (r, c): key = r*n + c. If key already in parent, append count and continue.
3. parent[key] = key, count += 1.
4. For each in-bounds neighbour that is land: if roots differ, union by rank, count -= 1.
5. Append count. Return out.

Complexity: O(k * alpha(m*n)) time, O(k) space — each add does <= 4 finds/unions; only land cells are stored.
Pitfalls: forgetting duplicate positions (they must NOT raise the count); counting the same
neighbouring island twice when two neighbours share a root (compare roots, not cells);
storing a full m*n parent array when m*n is huge but k is small.
"""
from typing import List


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        parent, rank = {}, {}
        count, out = 0, []

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for r, c in positions:
            key = r * n + c
            if key in parent:
                out.append(count)  # duplicate add: nothing changes
                continue
            parent[key], rank[key] = key, 0
            count += 1
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                nb = nr * n + nc
                if 0 <= nr < m and 0 <= nc < n and nb in parent:
                    ra, rb = find(key), find(nb)
                    if ra == rb:
                        continue  # same island already (two neighbours share a root)
                    if rank[ra] < rank[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    if rank[ra] == rank[rb]:
                        rank[ra] += 1
                    count -= 1
            out.append(count)
        return out


def brute_force(m: int, n: int, positions: List[List[int]]) -> List[int]:
    # After every add, flood-fill the entire grid from scratch and count islands.
    land = set()
    out = []
    for r, c in positions:
        land.add((r, c))
        seen, islands = set(), 0
        for cell in land:
            if cell in seen:
                continue
            islands += 1
            stack = [cell]
            seen.add(cell)
            while stack:
                cr, cc = stack.pop()
                for nb in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if nb in land and nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
        out.append(islands)
    return out


if __name__ == "__main__":
    s = Solution()
    cases = (
        (3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]], [1, 1, 2, 3]),
        (1, 1, [[0, 0]], [1]),
        (3, 3, [[0, 0], [0, 0], [1, 1], [0, 1]], [1, 1, 2, 1]),
        (2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]], [1, 2, 1, 1]),
    )
    for m, n, pos, want in cases:
        assert brute_force(m, n, pos) == want
        assert s.numIslands2(m, n, pos) == want
    print("ok")
