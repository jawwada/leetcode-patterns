"""
Combination Sum (LeetCode 39)  — Medium
Pattern: Backtracking with start index and sum pruning

Problem
-------
Given distinct positive candidates and a target, return all unique combinations (each candidate
may be reused any number of times) that sum to target. Order inside a combination does not
matter.
Example: candidates=[2,3,6,7], target=7 -> [[2,2,3],[7]].

Brute force
-----------
For every length r from 1 to target // min(candidates), generate every multiset of size r
(combinations_with_replacement) and keep the ones summing to target.
O(sum over r of C(n+r-1, r) * r) time, i.e. exponential with a huge constant. The waste: a
multiset is fully built before its sum is checked, so [2,2,2,2,2,...] is generated for every
length even though [2,2,2,2] already exceeds 7, and nothing learned from one failing multiset
prunes its extensions.

From brute force to optimal
---------------------------
The redundancy is extending partial combinations whose sum already exceeds the target.
Observation 1: candidates are positive, so a partial sum only grows; once it passes target,
every extension is dead and the whole subtree can be cut. Observation 2: to avoid emitting
[2,3,2] and [2,2,3] as different answers, only allow picking candidates at index >= the last
picked index (the "start" parameter); reuse is allowed by recursing with i, not i + 1.
Observation 3: sorting the candidates lets us `break` instead of `continue` on overflow, since
every later candidate is even bigger. The result is a DFS whose live branches are exactly the
partial sums that could still hit the target.

Intuition
---------
Build combinations as non-decreasing sequences of candidate indices. At each node either commit
another copy of the current candidate or move on to a bigger one; stop the moment the remaining
budget goes negative.

Geometric view
--------------
A tree where each node holds "remaining target"; children subtract a candidate >= the parent's
last choice. Leaves with remaining 0 are answers; any node whose remaining would go below 0 is
pruned, and because candidates are sorted its right-hand siblings are pruned with it (break).

Steps
-----
1. Sort candidates. result = [], path = [].
2. dfs(start, remaining): if remaining == 0 record a copy of path and return.
3. For i from start: if candidates[i] > remaining break (sorted: all later ones also too big).
4. Append candidates[i], recurse dfs(i, remaining - candidates[i]) (i, not i+1: reuse allowed),
   then pop.
5. Call dfs(0, target), return result.

Complexity: O(n^(target/min_candidate)) worst-case time (branching n, depth up to target/min),
O(target/min_candidate) recursion space beyond the output.
Pitfalls: Recursing with i + 1 (forbids reuse); looping from 0 (emits permutations of the same
combination); using `continue` where `break` is valid after sorting (correct but slower).
"""
from itertools import combinations_with_replacement
from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        result: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:       # sorted: every later candidate also too big
                    break
                path.append(candidates[i])
                dfs(i, remaining - candidates[i])   # i (not i+1): the same value may be reused
                path.pop()

        dfs(0, target)
        return result


def brute_force(candidates: List[int], target: int) -> List[List[int]]:
    out = []
    for r in range(1, target // min(candidates) + 1):
        for combo in combinations_with_replacement(candidates, r):   # built fully, checked late
            if sum(combo) == target:
                out.append(list(combo))
    return out


if __name__ == "__main__":
    s = Solution()

    def canon(c):
        return sorted(tuple(sorted(x)) for x in c)

    assert canon(s.combinationSum([2, 3, 6, 7], 7)) == canon([[2, 2, 3], [7]])
    assert canon(s.combinationSum([2, 3, 5], 8)) == canon([[2, 2, 2, 2], [2, 3, 3], [3, 5]])
    assert s.combinationSum([2], 1) == []                              # impossible
    assert s.combinationSum([1], 2) == [[1, 1]]
    for cands, t in ([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([2], 1), ([1], 2), ([7, 3, 2], 18):
        assert canon(s.combinationSum(cands, t)) == canon(brute_force(cands, t)), (cands, t)
    print("ok")
