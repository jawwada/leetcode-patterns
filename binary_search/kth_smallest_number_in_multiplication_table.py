"""
Kth Smallest Number in Multiplication Table (LeetCode 668)  — Hard
Pattern: Binary search on the answer + row counting

Problem
-------
An m x n multiplication table has table[i][j] = i * j (1-indexed). Return the k-th smallest
value in the table (1 <= k <= m*n).
Example: m = 3, n = 3, k = 5 -> 3  (table 1 2 3 / 2 4 6 / 3 6 9; sorted 1,2,2,3,3,4,6,6,9).
Example: m = 2, n = 3, k = 6 -> 6.

Brute force
-----------
Generate all m*n products, sort them, return index k-1. O(mn log(mn)) time, O(mn) space — with
m, n up to 3*10^4 that is 9*10^8 numbers, far too many. The waste: we materialise and sort the
whole table although it has so much structure (every row is sorted and is a multiple of the
first row) that "how many entries are <= v" can be computed without touching the entries.

From brute force to optimal
---------------------------
The redundancy is enumerating entries to rank them. Row i is i, 2i, 3i, ..., ni, so the number
of entries in row i that are <= v is min(n, v // i) — one division. Summing over the m rows
gives count(v) = #entries <= v in O(m). count(v) is monotone in v, and the k-th smallest value is
the smallest v with count(v) >= k, so binary search v over [1, m*n]. That v is guaranteed to
actually appear in the table: at the first v where count reaches k the count strictly increased
from v-1, and count only increases at values that occur. O(m log(mn)) total.

Intuition
---------
You never need the table — only the ability to count below a threshold. Each row is an
arithmetic progression, so counting below v in a row is a single floor division. Binary search
turns "find the k-th" into log(mn) such counts.

Geometric view
--------------
Draw the table as a grid; shade every cell <= v. The shaded region is a staircase hugging the
top-left corner: row i is shaded for exactly min(n, v // i) cells, shorter as i grows (it is the
region under the hyperbola i*j = v). count(v) is the staircase's area; over v the predicate
count(v) >= k is F...FT...T and lo/hi squeeze onto the first T.

Steps
-----
1. lo = 1, hi = m * n.
2. count(v) = sum(min(n, v // i) for i in 1..m).
3. While lo < hi: mid = (lo+hi)//2; if count(mid) >= k: hi = mid else lo = mid + 1.
4. Return lo.

Complexity: O(m log(mn)) time, O(1) space — log(mn) probes, each summing over m rows.
Pitfalls: forgetting min(n, ...) (a row has only n entries); looping over the larger dimension
(swap so the loop runs over min(m, n)); a heap merge of m rows is O(k log m) and k can be mn.
"""
import random


class Solution:
    def findKthNumber(self, m: int, n: int, k: int) -> int:
        if m > n:
            m, n = n, m                              # loop over the shorter dimension

        def count(v: int) -> int:                    # entries <= v, one division per row
            return sum(min(n, v // i) for i in range(1, m + 1))

        lo, hi = 1, m * n
        while lo < hi:                               # first v with count(v) >= k
            mid = (lo + hi) // 2
            if count(mid) >= k:
                hi = mid                             # enough entries at or below mid
            else:
                lo = mid + 1
        return lo                                    # lo is guaranteed to be in the table


def brute_force(m: int, n: int, k: int) -> int:
    table = sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))
    return table[k - 1]


if __name__ == "__main__":
    s = Solution()
    assert s.findKthNumber(3, 3, 5) == 3
    assert s.findKthNumber(2, 3, 6) == 6
    assert s.findKthNumber(1, 1, 1) == 1
    assert s.findKthNumber(9, 9, 81) == 81                   # largest entry
    assert s.findKthNumber(1, 10, 7) == 7                    # single row
    rng = random.Random(668)
    for _ in range(300):
        m, n = rng.randint(1, 12), rng.randint(1, 12)
        k = rng.randint(1, m * n)
        assert s.findKthNumber(m, n, k) == brute_force(m, n, k), (m, n, k)
    print("ok")
