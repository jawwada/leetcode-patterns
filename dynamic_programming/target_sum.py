"""
Target Sum (LeetCode 494)  — Medium
Pattern: Count ways per reachable sum

Problem
-------
Put a '+' or '-' in front of every number in nums and evaluate the expression. Return
how many sign assignments evaluate to target. Example: nums=[1,1,1,1,1], target=3 -> 5
(the single '-' can go on any of the five 1s).  nums=[1], target=1 -> 1.

Brute force
-----------
Recursion: ways(i, s) = ways(i+1, s + nums[i]) + ways(i+1, s - nums[i]), and at the end
count 1 if s == target. That enumerates all 2^n sign patterns: O(2^n) time, O(n) stack.
The waste: many different prefixes reach the same running sum s at the same index i
(e.g. +1-1 and -1+1 both give 0), and each re-explores the identical suffix.

From brute force to optimal
---------------------------
Overlapping subproblems: the number of ways to finish depends only on (i, running sum),
and the running sum lies in [-total, total], so there are at most n * (2*total + 1)
states (the user's original memo dict keyed on exactly (i, ct)).
State: after processing i numbers, counts[s] = number of sign patterns of nums[:i] whose
sum is s.
Recurrence: counts_{i+1}[s + x] += counts_i[s] and counts_{i+1}[s - x] += counts_i[s].
Order: one layer per number, left to right; only the previous layer is needed, so keep a
single dict of reachable sums. Answer: counts[target]. O(n * total) time, O(total) space.
Paths that merge on the same sum are collapsed into one count instead of 2^n paths.

Intuition
---------
You don't need to remember the signs, only where the running sum currently is and how
many ways got there. Every number splits each reachable sum into two (s+x and s-x), and
equal sums merge by adding their counts.

Geometric view
--------------
Picture a token on a number line starting at 0 and a layered lattice below it: each row
is one number, each token moves left or right by x. Many paths land on the same point;
instead of tracking paths, write the path COUNT on each point (Pascal's triangle when all
x = 1). Read the count at target in the last row.

Steps
-----
1. counts = {0: 1}.
2. For x in nums: nxt = defaultdict(int); for s, c in counts: nxt[s + x] += c,
   nxt[s - x] += c; counts = nxt.
3. Return counts.get(target, 0).

Complexity: O(n * total) time, O(total) space — at most 2*total+1 sums per layer.
Pitfalls: zeros double the count (+0 and -0 are different assignments); |target| > total
is simply 0; the subset-sum rewrite (P = (total + target) / 2) needs parity and sign
checks.
"""
from collections import defaultdict
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        counts = {0: 1}  # running sum -> number of sign patterns reaching it
        for x in nums:
            nxt = defaultdict(int)
            for s, c in counts.items():
                nxt[s + x] += c
                nxt[s - x] += c
            counts = nxt
        return counts.get(target, 0)


def brute_force(nums: List[int], target: int) -> int:
    # Try '+' and '-' on every number: O(2^n).
    def ways(i: int, s: int) -> int:
        if i == len(nums):
            return 1 if s == target else 0
        return ways(i + 1, s + nums[i]) + ways(i + 1, s - nums[i])

    return ways(0, 0)


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 1, 1, 1, 1], 3, 5), ([1], 1, 1), ([0, 0, 1], 1, 4),
             ([1, 2, 3], 7, 0), ([2, 3, 5, 1], -1, 2)]
    for nums, t, want in cases:
        assert s.findTargetSumWays(nums, t) == want
        assert brute_force(nums, t) == want
    print("ok")
