"""
Flood Fill (LeetCode 733)  — Easy
Pattern: Grid flood fill (DFS/BFS)

Problem
-------
Given an image (grid of colours), a start pixel (sr, sc) and a new colour, recolour the
start pixel and every pixel 4-connected to it that has the start pixel's ORIGINAL colour.
Example: image=[[1,1,1],[1,1,0],[1,0,1]], sr=1, sc=1, color=2 -> [[2,2,2],[2,2,0],[2,0,1]]
(the bottom-right 1 is not connected, so it stays 1).

Brute force
-----------
Repeated relaxation: keep sweeping the whole grid, and paint any pixel of the old colour
that touches an already-painted pixel (tracked in a boolean mask); stop when a sweep
paints nothing. A snake-shaped region can need O(m*n) sweeps of O(m*n) each:
O((m*n)^2) time, O(m*n) space. The waste: every sweep revisits pixels that cannot change
instead of looking only at the neighbours of pixels just painted.

From brute force to optimal
---------------------------
The redundancy is rescanning the whole grid when only the frontier (pixels painted last
round) can spread colour. Keep that frontier explicitly: a stack (DFS) or queue (BFS).
Painting a pixel the moment it is pushed doubles as the visited mark, because a painted
pixel no longer matches the old colour. Each pixel is pushed at most once -> O(m*n). One
edge case: if old colour == new colour, painting does not change anything, so the
"visited" mark fails and the fill would loop forever; return immediately.

Intuition
---------
The region to recolour is one connected component of same-coloured pixels. Any graph
traversal from the start pixel enumerates exactly that component; recolouring in place
is the visited set for free.

Geometric view
--------------
Paint-bucket tool: tip paint on one pixel; it spreads to every touching pixel of the same
colour and stops at colour borders. The stack holds the wet edge of the spreading paint.

Steps
-----
1. old = image[sr][sc]; if old == color return image.
2. Paint (sr, sc), push it.
3. Pop a pixel; for each in-bounds neighbour still equal to old, paint and push it.
4. Return image when the stack is empty.

Complexity: O(m*n) time, O(m*n) space — each pixel painted once; stack may hold a region.
Pitfalls: infinite loop when old == color; recursive DFS hitting the recursion limit on
large images (the user's original recursive version is fine for LeetCode's 50x50 limit;
here an explicit stack is used).
"""
from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        old = image[sr][sc]
        if old == color:  # painting would not mark anything as visited
            return image
        rows, cols = len(image), len(image[0])
        image[sr][sc] = color
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == old:
                    image[nr][nc] = color
                    stack.append((nr, nc))
        return image


def brute_force(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
    # Sweep the whole grid until no new pixel joins the painted mask: O((m*n)^2).
    rows, cols, old = len(image), len(image[0]), image[sr][sc]
    mask = [[False] * cols for _ in range(rows)]
    mask[sr][sc] = changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if not mask[r][c] and image[r][c] == old and any(
                        0 <= nr < rows and 0 <= nc < cols and mask[nr][nc]
                        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))):
                    mask[r][c] = changed = True
    return [[color if mask[r][c] else image[r][c] for c in range(cols)] for r in range(rows)]


if __name__ == "__main__":
    import copy

    s = Solution()
    cases = [([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2, [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
             ([[0, 0, 0], [0, 0, 0]], 0, 0, 0, [[0, 0, 0], [0, 0, 0]]),   # same colour
             ([[5]], 0, 0, 7, [[7]]),
             ([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 2, 3, [[3, 0, 3], [3, 0, 3], [3, 3, 3]])]
    for img, r, c, col, want in cases:
        assert brute_force(copy.deepcopy(img), r, c, col) == want
        assert s.floodFill(copy.deepcopy(img), r, c, col) == want
    print("ok")
