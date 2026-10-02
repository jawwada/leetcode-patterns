"""
Maximum XOR With an Element From Array (LeetCode 1707)  — Hard
Pattern: Offline queries + binary trie (greedy bit by bit)

Problem
-------
Given `nums` and queries [x_i, m_i], answer each query with the maximum of x_i XOR nums[j] over
all j with nums[j] <= m_i, or -1 if no element is <= m_i. Values are < 10^9 (30 bits);
nums and queries each have up to 10^5 entries.
Example: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]] -> [3,3,7]
         (3^0=3; 1^2=3; 5^2=7).

Brute force
-----------
For each query scan nums, skip values > m, keep the maximum XOR. O(q * n) time, O(1) space —
10^10 operations. The waste is twofold: every query re-filters nums against its own m (the
filters are nested sets, so sorting once would make them prefixes), and the XOR maximum is
recomputed from scratch by brute enumeration although a bit-by-bit greedy can find it in 30
steps.

From brute force to optimal
---------------------------
Step 1 (max XOR without the bound): insert nums into a binary trie keyed on the 30 bits from
most significant to least. To maximise x XOR y, walk down from the root and at each level take
the child whose bit is the OPPOSITE of x's bit when it exists (that sets a 1 in the result at
the highest possible position); the greedy is correct because a 1 at bit b outweighs all lower
bits combined. O(30) per query instead of O(n).
Step 2 (the bound m): answering queries in the given order would require a trie restricted to
nums <= m per query. Go offline: sort nums and sort the queries by m, then sweep — before
answering a query, insert every num <= its m. The trie at that moment contains exactly the
allowed elements. Each num is inserted once; the restriction costs nothing extra.

Intuition
---------
XOR maximisation is lexicographic: decide the top bit first, never regret it. A trie over bit
strings is exactly the structure that lets you ask "does any inserted number have bit b = 1
with these top bits?" in O(1). Sorting the queries converts the per-query filter into a
monotone sweep where the data structure only ever grows.

Geometric view
--------------
Write the numbers in binary as columns from bit 29 down to bit 0 and overlay them into a binary
tree: left edge = 0, right edge = 1, depth = bit position. A query x traces one root-to-leaf
path that at each depth prefers the edge opposite to x's bit, falling back to the only edge
when it must. The sweep over sorted m draws ever more paths into the tree.

Steps
-----
1. Sort nums; sort query indices by m.
2. child[node] = [left, right]; insert(x): walk bits 29..0 creating nodes as needed.
3. best_xor(x): at each bit b want = 1 - bit(x, b); if child exists go there and set bit b
   in the answer, else take the other child.
4. Sweep queries in m order: insert nums[i] while nums[i] <= m; answer -1 if the trie is
   still empty, else best_xor(x).
5. Place each answer at its original query index.

Complexity: O((n + q) * 30 + n log n + q log q) time, O(n * 30) space for trie nodes.
Pitfalls: forgetting the -1 case (empty trie); returning answers in sorted-by-m order instead of
the original order; building the trie with 31/32 bits and shifting negatives (values are
non-negative here, 30 bits suffice).
"""
import random
from typing import List


class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        BITS = 30                                     # values < 10^9 < 2^30
        nums.sort()
        child = [[0, 0]]                              # child[node][bit] -> node index, 0 = none

        def insert(x: int) -> None:
            node = 0
            for b in range(BITS - 1, -1, -1):
                bit = (x >> b) & 1
                if not child[node][bit]:
                    child[node][bit] = len(child)
                    child.append([0, 0])
                node = child[node][bit]

        def best_xor(x: int) -> int:
            node, out = 0, 0
            for b in range(BITS - 1, -1, -1):
                want = 1 - ((x >> b) & 1)             # opposite bit -> result bit b becomes 1
                if child[node][want]:
                    out |= 1 << b
                    node = child[node][want]
                else:
                    node = child[node][1 - want]      # forced: only one branch exists
            return out

        ans = [-1] * len(queries)
        i = 0                                         # next num to insert
        for qi in sorted(range(len(queries)), key=lambda q: queries[q][1]):
            x, m = queries[qi]
            while i < len(nums) and nums[i] <= m:     # trie now holds exactly nums <= m
                insert(nums[i])
                i += 1
            if i:
                ans[qi] = best_xor(x)
        return ans


def brute_force(nums: List[int], queries: List[List[int]]) -> List[int]:
    ans = []
    for x, m in queries:
        best = -1
        for v in nums:                                # re-filter and re-scan per query
            if v <= m:
                best = max(best, x ^ v)
        ans.append(best)
    return ans


if __name__ == "__main__":
    s = Solution()
    assert s.maximizeXor([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]]) == [3, 3, 7]
    assert s.maximizeXor([5, 2, 4, 6, 6, 3], [[12, 4], [8, 1], [6, 3]]) == [15, -1, 5]
    assert s.maximizeXor([7], [[0, 7], [0, 6]]) == [7, -1]             # bound exactly equal
    rng = random.Random(1707)
    for _ in range(200):
        nums = [rng.randint(0, 63) for _ in range(rng.randint(1, 8))]
        queries = [[rng.randint(0, 63), rng.randint(0, 63)] for _ in range(rng.randint(1, 6))]
        assert s.maximizeXor(list(nums), queries) == brute_force(nums, queries), (nums, queries)
    print("ok")
