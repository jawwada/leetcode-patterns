"""
Pacific Atlantic Water Flow (LeetCode 417)  — Medium
Pattern: Multi-source reverse BFS/DFS from the boundary

Problem
-------
An m x n height grid is bordered by the Pacific on the top and left edges and the Atlantic
on the bottom and right edges. Water flows from a cell to a 4-neighbour whose height is
<= its own. Return every cell from which water can reach BOTH oceans.
Example: heights=[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
-> [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]].

Brute force
-----------
For each of the mn cells, run a downhill DFS/BFS and check whether it touches a top/left
border cell and a bottom/right border cell. Each search is O(mn), so the whole thing is
O((mn)^2) time, O(mn) space. The wasted step: two neighbouring cells of similar height
re-explore nearly the same downhill region, and most cells' searches end up re-walking
the same low basins over and over.

From brute force to optimal
---------------------------
The redundancy is asking "can cell X reach the ocean?" separately for every X when the
reachability structure is shared. Observation: reverse the question. Instead of flowing
down from each cell, climb UP from each ocean: a cell can drain to the Pacific iff it is
reachable from some Pacific-border cell by moving to neighbours of height >= current.
That is a single multi-source traversal per ocean, visiting each cell at most once,
giving two boolean grids; the answer is their intersection. O(mn) total.

Intuition
---------
Water flows down, so start at the oceans and walk uphill. Seed a BFS with every Pacific
border cell and mark everything it can climb to; do the same from the Atlantic border.
Any cell marked by both can drain to both.

Geometric view
--------------
Picture two tides rising from opposite corners of the map. The Pacific tide creeps up
from the top/left edges onto any neighbouring cell at least as high; the Atlantic tide
does the same from the bottom/right. The frontier of each tide is a BFS queue. Cells
submerged by both tides are the answer.

Steps
-----
1. Create two boolean grids pac, atl.
2. Seed pac queue with all cells in row 0 and column 0; seed atl queue with the last row
   and last column.
3. BFS each: from (r, c) move to in-bounds neighbour (nr, nc) not yet marked with
   heights[nr][nc] >= heights[r][c]; mark and enqueue.
4. Return all (r, c) with pac[r][c] and atl[r][c].

Complexity: O(m*n) time, O(m*n) space — each ocean's BFS visits every cell at most once.
Pitfalls: using > instead of >= when climbing (equal heights still flow); seeding only the
corners instead of whole edges; forgetting a 1xN grid where every cell touches both oceans.
"""
from collections import deque
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])

        def climb(sources: List[tuple]) -> List[List[bool]]:
            seen = [[False] * cols for _ in range(rows)]
            queue = deque(sources)
            for r, c in sources:
                seen[r][c] = True
            while queue:
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] \
                            and heights[nr][nc] >= heights[r][c]:  # reverse flow: go uphill
                        seen[nr][nc] = True
                        queue.append((nr, nc))
            return seen

        pacific = [(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)]
        atlantic = [(r, cols - 1) for r in range(rows)] + [(rows - 1, c) for c in range(cols)]
        pac, atl = climb(pacific), climb(atlantic)
        return [[r, c] for r in range(rows) for c in range(cols) if pac[r][c] and atl[r][c]]


def brute_force(heights: List[List[int]]) -> List[List[int]]:
    # From every cell, flow downhill with its own visited set and test whether both
    # ocean borders were touched.
    rows, cols = len(heights), len(heights[0])

    def reaches_both(r0: int, c0: int) -> bool:
        seen, stack, pac, atl = {(r0, c0)}, [(r0, c0)], False, False
        while stack:
            r, c = stack.pop()
            pac |= r == 0 or c == 0
            atl |= r == rows - 1 or c == cols - 1
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen \
                        and heights[nr][nc] <= heights[r][c]:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
        return pac and atl

    return [[r, c] for r in range(rows) for c in range(cols) if reaches_both(r, c)]


if __name__ == "__main__":
    s = Solution()
    h1 = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
    h2 = [[1]]
    h3 = [[1, 2], [4, 3]]
    h4 = [[3, 3, 3], [3, 1, 3], [3, 3, 3]]
    assert s.pacificAtlantic(h1) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert s.pacificAtlantic(h2) == [[0, 0]]
    assert s.pacificAtlantic(h3) == [[0, 1], [1, 0], [1, 1]]  # (0,0) is a pit: cannot reach the Atlantic
    assert s.pacificAtlantic(h4) == [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    for h in (h1, h2, h3, h4):
        assert brute_force(h) == s.pacificAtlantic(h)
    print("ok")
