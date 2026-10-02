"""
Search a 2D Matrix (LeetCode 74)  — Medium
Pattern: Binary search on a sorted array

Problem
-------
An m x n matrix has each row sorted ascending, and the first integer of each row is greater than
the last integer of the previous row. Return True if `target` is in the matrix.
Example: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3 -> True.

Brute force
-----------
Scan every cell and compare with target. O(m*n) time, O(1) space. The wasted work: the matrix is
globally sorted (row-major order is a sorted sequence), yet each comparison eliminates only one
cell instead of a whole prefix or suffix.

From brute force to optimal
---------------------------
The redundancy is ignoring the ordering. Observation: because row i's first element exceeds row
i-1's last element, reading the matrix row by row yields one sorted list of length m*n. So the
2D structure is a disguise: index k in that list maps to cell (k // n, k % n). Treat it as a
flat sorted array and run ordinary binary search over indices 0..m*n-1 with the divmod mapping.
That gives O(log(mn)) with no extra memory.

Intuition
---------
Unroll the matrix into a single sorted line without copying anything — the `divmod` conversion is
the "virtual flatten". Then binary search works exactly as on a 1D array.

Geometric view
--------------
Picture the rows laid end to end into one strip of m*n cells. lo and hi are positions on that
strip; the strip halves each probe. To read a value at strip position k you fold it back into
the grid: row = k // n, col = k % n.

Steps
-----
1. m, n = dimensions; lo = 0, hi = m*n - 1.
2. While lo <= hi: mid = (lo+hi)//2; r, c = divmod(mid, n); v = matrix[r][c].
3. If v == target return True.
4. If v < target: lo = mid + 1 else hi = mid - 1.
5. Return False.

Complexity: O(log(m*n)) time, O(1) space — one binary search over m*n virtual positions.
Pitfalls: using divmod(mid, m) instead of divmod(mid, n); empty matrix / empty row; the two-pass
"binary search rows then columns" variant works but is twice the code for the same bound.
"""
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        m, n = len(matrix), len(matrix[0])
        lo, hi = 0, m * n - 1                # virtual flat index range
        while lo <= hi:
            mid = (lo + hi) // 2
            r, c = divmod(mid, n)            # fold flat index back into grid
            v = matrix[r][c]
            if v == target:
                return True
            if v < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return False


def brute_force(matrix: List[List[int]], target: int) -> bool:
    for row in matrix:
        for v in row:
            if v == target:
                return True
    return False


if __name__ == "__main__":
    s = Solution()
    M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    cases = [
        (M, 3, True),
        (M, 13, False),
        ([[1]], 1, True),
        ([[1]], 2, False),
        ([[1, 3]], 3, True),
    ]
    for mat, t, want in cases:
        assert s.searchMatrix(mat, t) == want
        assert brute_force(mat, t) == want
    print("ok")
