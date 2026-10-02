"""
Shortest Subarray with Sum at Least K (LeetCode 862)  — Hard
Pattern: Monotonic deque

Problem
-------
Given an integer array nums (values may be negative) and an integer k, return the length
of the shortest non-empty contiguous subarray whose sum is >= k, or -1 if none exists.
Example: nums = [2,-1,2], k = 3 -> 3 (the whole array; no shorter window reaches 3).

Brute force
-----------
For every start i, extend the end j and keep a running sum; record j - i + 1 whenever the
sum reaches k. O(n^2) time, O(1) space. With negatives you cannot stop early: a later
element may push the sum back over k, so every (i, j) pair is examined. The repeated work
is that the same prefix sums are re-added for every start, and that we keep considering
starts that can never beat an already-known shorter answer.

From brute force to optimal
---------------------------
Rewrite with prefix sums P (P[0] = 0, P[j] = sum of first j elements): we want the shortest
j - i with P[j] - P[i] >= k, i < j. Two observations prune candidate starts i. (1) If
i1 < i2 and P[i1] >= P[i2], then i1 is useless: any j that works with i1 also works with
i2 (P[j] - P[i2] >= P[j] - P[i1] >= k) and i2 is closer, so i1 can never be the best start.
Hence the useful starts have strictly increasing prefix sums — keep them in a deque that is
monotonic increasing by P. (2) Once the smallest-P start at the front satisfies
P[j] - P[front] >= k for the current j, record j - front and pop it: any later j' > j would
give a longer subarray with the same start. Each index enters and leaves the deque at most
once, so the sweep is O(n) with no sorting or heap.

Intuition
---------
Negative numbers break the plain sliding window because shrinking from the left can
increase the sum. Prefix sums restore order: we are looking for a pair (i, j) with a large
difference and a small gap. A start i is only worth remembering if its prefix sum is lower
than every later remembered start — otherwise the later start dominates it in both
distance and sum. That dominance rule is exactly what a monotonic deque maintains.

Geometric view
--------------
Plot the prefix sums as points (index, P). The deque holds the "lower-left staircase" of
candidate starts: points that are to the left and strictly below everything after them.
For each new point j, pop from the front while j is at least k above it (each pop is an
answer candidate), then pop from the back while the new point is at or below the back
(those starts are dominated), then push j.

Steps
-----
1. Build prefix sums P of length n + 1 with P[0] = 0.
2. For j from 0 to n, with deque dq of indices:
3.   while dq and P[j] - P[dq[0]] >= k: best = min(best, j - dq.popleft()).
4.   while dq and P[j] <= P[dq[-1]]: dq.pop()  (the back is dominated by j).
5.   append j.
6. Return best, or -1 if never updated.

Complexity: O(n) time, O(n) space — each index is pushed and popped at most once.
Pitfalls: popping from the front with a while (not if) — several fronts may qualify; using
< instead of <= on the back pop, which keeps useless equal-sum starts; trying a plain
two-pointer window, which fails on negatives; forgetting P[0] = 0 as a start.
"""
from collections import deque
from itertools import accumulate
from typing import List


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        prefix = [0] + list(accumulate(nums))
        best = float("inf")
        dq = deque()                     # indices whose prefix sums strictly increase
        for j, pj in enumerate(prefix):
            # front is the smallest prefix; if it already reaches k, no later j
            # can beat this start, so settle and drop it
            while dq and pj - prefix[dq[0]] >= k:
                best = min(best, j - dq.popleft())
            # a start with a prefix >= pj is farther away AND no better: dominated
            while dq and pj <= prefix[dq[-1]]:
                dq.pop()
            dq.append(j)
        return best if best != float("inf") else -1


def brute_force(nums: List[int], k: int) -> int:
    best = float("inf")
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= k:
                best = min(best, j - i + 1)
    return best if best != float("inf") else -1


if __name__ == "__main__":
    s = Solution()
    assert s.shortestSubarray([1], 1) == 1
    assert s.shortestSubarray([1, 2], 4) == -1
    assert s.shortestSubarray([2, -1, 2], 3) == 3
    assert s.shortestSubarray([84, -37, 32, 40, 95], 167) == 3
    assert s.shortestSubarray([-5, 3, 7, -2, 9], 10) == 2
    import random
    random.seed(862)
    cases = [([1], 1), ([1, 2], 4), ([2, -1, 2], 3), ([84, -37, 32, 40, 95], 167)]
    for _ in range(200):
        n = random.randint(1, 12)
        nums = [random.randint(-10, 10) for _ in range(n)]
        cases.append((nums, random.randint(1, 25)))
    for nums, k in cases:
        assert s.shortestSubarray(nums, k) == brute_force(nums, k)
    print("ok")
