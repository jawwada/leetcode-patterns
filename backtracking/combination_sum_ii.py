"""
Combination Sum II (LeetCode 40)  — Medium
Pattern: Backtracking with sort + skip-duplicates-at-same-depth

Problem
-------
Given candidates (which may repeat) and a target, return all unique combinations summing to
target where each candidate index is used at most once.
Example: candidates=[10,1,2,7,6,1,5], target=8 -> [[1,1,6],[1,2,5],[1,7],[2,6]].

Brute force
-----------
Enumerate all 2^n index subsets via bitmasks, keep those whose sum equals target, and dedupe
by inserting the sorted tuple into a set. O(n * 2^n) time, O(2^n) space for the set.
The waste is twofold: subsets whose running sum already exceeds target are still fully decoded
and summed, and combinations that differ only in WHICH copy of a repeated value they use (the two
1's in the example) are generated separately and then collapsed by the set.

From brute force to optimal
---------------------------
Two redundancies, two fixes. (1) Overflowing partial sums: candidates are positive, so sort and
`break` out of the loop the moment candidates[i] > remaining; everything to the right is bigger.
(2) Equal values at the same level: after sorting, duplicates are adjacent; if we skipped the
first copy at this level (i > start) and the current value equals the previous, its subtree is
identical to one already explored, so `continue`. Recursing with i + 1 enforces "each index at
most once". The DFS then visits only prefixes of distinct, feasible combinations.

Intuition
---------
Subsets II's dedupe rule plus Combination Sum's sum pruning, with i + 1 instead of i because
reuse is forbidden. Sorting enables both rules at once.

Geometric view
--------------
A tree whose nodes hold the remaining target. At each node the children are the candidates from
start onward, sorted ascending. Two kinds of cuts: a child bigger than the remaining target
truncates the rest of the row (break), and a child equal to its left sibling is crossed out
(continue).

Steps
-----
1. Sort candidates. result = [], path = [].
2. dfs(start, remaining): if remaining == 0 record a copy of path and return.
3. For i from start: if candidates[i] > remaining break.
4. If i > start and candidates[i] == candidates[i-1] continue.
5. Append, recurse dfs(i + 1, remaining - candidates[i]), pop.
6. Call dfs(0, target), return result.

Complexity: O(2^n) time worst case (each index in or out), O(n) recursion/path space beyond the
output.
Pitfalls: Recursing with i instead of i + 1 (allows reuse); using i > 0 instead of i > start in
the skip rule (loses [1,1,6]); forgetting to sort before applying either rule.
"""
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        result: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break                               # sorted: later values are even bigger
                if i > start and candidates[i] == candidates[i - 1]:
                    continue                            # duplicate sibling: same subtree
                path.append(candidates[i])
                dfs(i + 1, remaining - candidates[i])   # i+1: each index used at most once
                path.pop()

        dfs(0, target)
        return result


def brute_force(candidates: List[int], target: int) -> List[List[int]]:
    n = len(candidates)
    seen = set()
    for mask in range(1 << n):
        chosen = [candidates[i] for i in range(n) if mask >> i & 1]
        if sum(chosen) == target:                       # summed only after full decoding
            seen.add(tuple(sorted(chosen)))             # duplicates collapsed late
    return [list(t) for t in seen]


if __name__ == "__main__":
    s = Solution()

    def canon(c):
        return sorted(tuple(sorted(x)) for x in c)

    assert canon(s.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)) == canon([[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]])
    assert canon(s.combinationSum2([2, 5, 2, 1, 2], 5)) == canon([[1, 2, 2], [5]])
    assert s.combinationSum2([2, 2], 5) == []                        # impossible
    assert s.combinationSum2([1, 1, 1, 1], 4) == [[1, 1, 1, 1]]      # all copies needed, once
    for cands, t in ([10, 1, 2, 7, 6, 1, 5], 8), ([2, 5, 2, 1, 2], 5), ([2, 2], 5), ([1, 1, 1, 1], 4):
        assert canon(s.combinationSum2(cands[:], t)) == canon(brute_force(cands, t)), (cands, t)
    print("ok")
