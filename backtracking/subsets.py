"""
Subsets (LeetCode 78)  — Medium
Pattern: Backtracking include/exclude decision tree

Problem
-------
Given an array of distinct integers, return all possible subsets (the power set), in any order,
without duplicates.
Example: [1,2,3] -> [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]].

Brute force
-----------
Enumerate every bitmask from 0 to 2^n - 1; for each mask, loop over the n bits and collect the
elements whose bit is set. O(n * 2^n) time, O(n * 2^n) output space. The waste: two masks that
share a prefix (e.g. 0b110xx and 0b110yy) rebuild the same first elements [1,2] from scratch;
every subset is decoded independently with no shared work.

From brute force to optimal
---------------------------
The output is itself of size O(n * 2^n), so no algorithm beats the brute force asymptotically;
the goal is to stop rebuilding shared prefixes and to arrive at a template that generalises to
pruning. Observation: subsets form a binary decision tree, at depth i decide "include nums[i]"
or "skip it". A depth-first walk with ONE shared path list adds an element on the way down and
removes it on the way up, so each subset costs O(1) incremental work plus the O(n) copy when it
is emitted. The same walk, plus a "skip duplicates" or "stop when sum exceeds target" rule,
solves Subsets II and Combination Sum: the structure is the point.

Intuition
---------
Every subset is a sequence of n yes/no answers. Walk the yes/no tree depth first with one path
list that you mutate and restore (push before recursing, pop after). The equivalent "for-loop"
form, at each level choose the next index to include from start onward, emits every node of the
tree as a subset and never produces duplicates because indices only increase.

Geometric view
--------------
A binary tree of depth n: each level is an element, the left branch means "take", the right
branch means "skip". The 2^n leaves are the subsets. The path list is the single pencil line
from the root to the current node; backtracking erases the last segment and draws a new one.

Steps
-----
1. result = [], path = []. Define dfs(start).
2. Record a copy of path (every node is a valid subset).
3. For i in range(start, n): append nums[i], recurse dfs(i + 1), pop.
4. Call dfs(0), return result.

Complexity: O(n * 2^n) time, O(n) recursion/path space beyond the output — 2^n subsets, each
copied in O(n).
Pitfalls: Appending the path object itself instead of a copy (all entries alias one list);
forgetting to pop (path keeps growing); starting the loop at 0 instead of start (duplicates).
"""
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int) -> None:
            result.append(path[:])             # every node of the tree is a subset
            for i in range(start, len(nums)):
                path.append(nums[i])           # choose
                dfs(i + 1)                     # explore (indices only increase: no dups)
                path.pop()                     # un-choose

        dfs(0)
        return result


def brute_force(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    out = []
    for mask in range(1 << n):                              # 2^n masks
        out.append([nums[i] for i in range(n) if mask >> i & 1])   # decode each from scratch
    return out


if __name__ == "__main__":
    s = Solution()

    def canon(subs):
        return sorted(tuple(sorted(x)) for x in subs)

    assert canon(s.subsets([1, 2, 3])) == canon([[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]])
    assert s.subsets([0]) == [[], [0]]
    assert s.subsets([]) == [[]]                                    # empty input -> only the empty set
    assert len(s.subsets([1, 2, 3, 4, 5])) == 32
    for nums in ([1, 2, 3], [0], [], [4, 7, 9, 10]):
        assert canon(s.subsets(nums)) == canon(brute_force(nums))
    print("ok")
