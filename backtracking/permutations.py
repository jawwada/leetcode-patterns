"""
Permutations (LeetCode 46)  — Medium
Pattern: Backtracking with a used-set

Problem
-------
Given an array of distinct integers, return all possible orderings (permutations) of its
elements, in any order.
Example: [1,2,3] -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]].

Brute force
-----------
Generate every sequence of length n over the n values (the Cartesian product, n^n sequences)
and keep those with no repeated element. O(n^n * n) time, O(n) space beyond the output.
The waste: sequences like [1,1,...] and [1,2,1,...] are generated to completion and rejected,
even though the repeat was already visible at position 2; the vast majority of the n^n sequences
are discarded.

From brute force to optimal
---------------------------
The redundancy is building sequences that already contain a duplicate. Observation: if we track
which values are already in the partial sequence (a used-set, or a boolean per index), we can
refuse to place a repeated value at the moment of choosing it, so every branch explored is a
prefix of a valid permutation. Each level then has one fewer choice than the level above, and the
n^n tree collapses to exactly n! leaves with no dead branches. The shared path list plus
append/pop keeps the per-node cost O(1).

Intuition
---------
Fill n slots left to right; at each slot pick any value not yet used, recurse, then put it back.
Marking as used while descending and unmarking while ascending is the whole trick.

Geometric view
--------------
A tree with n children at the root, n-1 under each of those, down to 1: the leaves are the n!
permutations. The path list is the current root-to-node trail; the used-set is the shadow of
that trail. Dead branches (reusing a value) are never even drawn.

Steps
-----
1. result = [], path = [], used = [False] * n.
2. dfs(): if len(path) == n record a copy and return.
3. For each index i with used[i] False: mark used, append nums[i], recurse, pop, unmark.
4. Call dfs(), return result.

Complexity: O(n * n!) time (n! leaves, each copied in O(n)), O(n) recursion/path space beyond
the output.
Pitfalls: Forgetting to unmark used[i] on the way back; checking `nums[i] in path` (O(n) per
check; fine for small n but a used array is O(1)); appending path instead of a copy.
"""
from itertools import product
from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        path: List[int] = []
        used = [False] * len(nums)

        def dfs() -> None:
            if len(path) == len(nums):
                result.append(path[:])
                return
            for i, v in enumerate(nums):
                if used[i]:                    # already in the path: skip (prunes the branch)
                    continue
                used[i] = True
                path.append(v)
                dfs()
                path.pop()
                used[i] = False                # restore for sibling branches

        dfs()
        return result


def brute_force(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    out = []
    for seq in product(nums, repeat=n):                # n^n sequences, filtered after building
        if len(set(seq)) == n:
            out.append(list(seq))
    return out


if __name__ == "__main__":
    s = Solution()

    def canon(p):
        return sorted(tuple(x) for x in p)

    assert canon(s.permute([1, 2, 3])) == canon([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    assert canon(s.permute([0, 1])) == canon([[0, 1], [1, 0]])
    assert s.permute([1]) == [[1]]                                  # single element
    assert len(s.permute([1, 2, 3, 4, 5])) == 120
    for nums in ([1, 2, 3], [0, 1], [1], [5, -1, 7, 2]):
        assert canon(s.permute(nums)) == canon(brute_force(nums))
    print("ok")
