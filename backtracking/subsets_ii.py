"""
Subsets II (LeetCode 90)  — Medium
Pattern: Backtracking with sort + skip-duplicates-at-same-depth

Problem
-------
Given an array that may contain duplicates, return all possible subsets with no duplicate
subsets, in any order.
Example: [1,2,2] -> [[],[1],[2],[1,2],[2,2],[1,2,2]].

Brute force
-----------
Enumerate all 2^n bitmasks, decode each into a sorted tuple, and insert into a set to drop the
duplicates. O(n * 2^n) time, O(n * 2^n) space for the set. The waste: with d copies of a value,
every subset containing j of them is generated C(d, j) times and then thrown away by the set;
for [2,2,2] the subset [2] is produced three times, [2,2] three times.

From brute force to optimal
---------------------------
The redundancy is generating the same multiset via different index choices. Observation: if the
array is sorted, duplicate values are adjacent, and choosing the SECOND copy of a value at the
same tree level when the first copy was skipped produces exactly the same subtree as choosing the
first copy did. So at each level, skip nums[i] when i > start and nums[i] == nums[i-1]. This rule
cuts the duplicate subtrees before they are explored, so every emitted subset is unique with no
set needed. Choosing the second copy right AFTER the first (deeper level, i == start) is still
allowed, which is how [2,2] gets produced exactly once.

Intuition
---------
Sort, then at any level treat equal values as one choice: "how many copies of this value do I
take" is decided by going deeper, never by trying siblings with the same value.

Geometric view
--------------
The same include/exclude tree as Subsets, but siblings carrying an equal value are drawn and
then crossed out (pruned) except the first one. Sorting is what lines the equal values up next to
each other so the crossing out is a single comparison with the previous index.

Steps
-----
1. Sort nums. result = [], path = [].
2. dfs(start): record a copy of path.
3. For i in range(start, n): if i > start and nums[i] == nums[i-1] continue (duplicate sibling).
4. Append nums[i], recurse dfs(i + 1), pop.
5. Call dfs(0), return result.

Complexity: O(n * 2^n) time worst case, O(n) recursion/path space beyond the output.
Pitfalls: Forgetting to sort (the skip rule only works on adjacent duplicates); writing the skip
condition as i > 0 instead of i > start (would wrongly forbid [2,2]); dedup with a set instead
of pruning (works, but defeats the purpose and costs memory).
"""
from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()                                     # line duplicates up side by side
        result: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int) -> None:
            result.append(path[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue                            # same value as a sibling: prune
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return result


def brute_force(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    seen = set()
    for mask in range(1 << n):
        sub = tuple(sorted(nums[i] for i in range(n) if mask >> i & 1))
        seen.add(sub)                                   # duplicates generated, then discarded
    return [list(t) for t in seen]


if __name__ == "__main__":
    s = Solution()

    def canon(subs):
        return sorted(tuple(sorted(x)) for x in subs)

    assert canon(s.subsetsWithDup([1, 2, 2])) == canon([[], [1], [2], [1, 2], [2, 2], [1, 2, 2]])
    assert canon(s.subsetsWithDup([0])) == canon([[], [0]])
    assert canon(s.subsetsWithDup([2, 2, 2])) == canon([[], [2], [2, 2], [2, 2, 2]])   # all equal
    assert len(s.subsetsWithDup([4, 4, 4, 1, 4])) == 10
    for nums in ([1, 2, 2], [0], [2, 2, 2], [4, 4, 4, 1, 4], [1, 1, 2, 2, 3]):
        assert canon(s.subsetsWithDup(nums[:])) == canon(brute_force(nums))
    print("ok")
