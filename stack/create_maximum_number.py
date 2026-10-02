"""
Create Maximum Number (LeetCode 321)  — Hard
Pattern: Monotonic stack (pick max subsequence) + greedy merge

Problem
-------
Given two digit arrays nums1 (length m) and nums2 (length n) and k <= m + n, build the largest
possible number of k digits by taking digits from both arrays while keeping each array's
relative order. Return it as a digit list.
Example: nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5 -> [9,8,6,5,3];
nums1 = [6,7], nums2 = [6,0,4], k = 5 -> [6,7,6,0,4].

Brute force
-----------
Enumerate every subsequence of nums1 of size i and every subsequence of nums2 of size k - i,
and for each pair every interleaving that preserves both orders; keep the lexicographically
largest. Exponential: O(2^m * 2^n * C(k, i)) candidates. Correct for toy sizes only. The wasted
work is total: almost every candidate shares a long prefix with a candidate already known to be
smaller, and the "best i digits from one array" sub-problem is re-solved for every partner.

From brute force to optimal
---------------------------
Two independent decisions are tangled together: WHICH digits to keep from each array, and HOW to
interleave them. Observation 1: for a fixed split (i from nums1, k-i from nums2) the best choice
from one array does not depend on the other, and "largest subsequence of length t" is a classic
monotonic-stack problem: walk the array, pop the stack top while it is smaller than the current
digit and we still have deletions left (len - t), then push; O(len). Observation 2: merging two
chosen sequences to maximise the result is a greedy merge, but ties must be broken by comparing
the REMAINING suffixes, not just the heads ([6,7] vs [6,0,4]: take the 6 from [6,7] first).
Python compares lists lexicographically, so `a[i:] > b[j:]` does exactly that. Trying all k+1
splits and keeping the max is O(k) rounds of O(m + n + k^2) work.

Intuition
---------
Split the problem by "how many digits come from nums1". For each split the best subsequence of
each array is fixed and found greedily (keep the stack decreasing while you can still afford to
drop digits). Then zip the two picks together, always taking from whichever remainder is
lexicographically larger: an equal head is resolved by looking further right, because the
digit after the tie decides which stream should be spent first.

Geometric view
--------------
   nums1 = 3 4 6 5   pick 2 ->  stack: [3] -> [4] -> [6] -> [6,5]   (drops = 2 used up)
   nums2 = 9 1 2 5 8 3  pick 3 -> [9] [9,1] [9,2] [9,5] [9,8] [9,8,3]
   merge [6,5] with [9,8,3]: 9 8 6 5 3   (compare remaining tails at each step)
Picture two conveyor belts of digits; a monotonic stack skims the best t off each belt, then a
zipper closes the two skimmed strips, always pulling the heavier remaining strip first.

Steps
-----
1. pick(nums, t): drop = len(nums) - t; for x in nums: while drop and stack and stack[-1] < x:
   pop, drop -= 1; push x. Return stack[:t].
2. merge(a, b): while either remains, append the head of whichever remaining list compares
   greater (lexicographic comparison of the tails).
3. For i in max(0, k-n) .. min(k, m): candidate = merge(pick(nums1, i), pick(nums2, k-i)).
4. Return the lexicographically largest candidate.

Complexity: O(k * (m + n + k^2)) time, O(m + n) space — k+1 splits, each with two O(len) stack
passes and a merge whose tie-breaking comparison can cost O(k) per step.
Pitfalls: merging by comparing heads only (fails on equal digits); forgetting to truncate the
stack to t when fewer than `drop` pops happened (increasing input); split range must respect
both lengths (i <= m and k - i <= n).
"""
from itertools import combinations
from typing import List


class Solution:
    def maxNumber(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        def pick(nums: List[int], t: int) -> List[int]:     # largest subsequence of length t
            drop = len(nums) - t
            stack = []
            for x in nums:
                while drop and stack and stack[-1] < x:     # a bigger digit wants this slot
                    stack.pop()
                    drop -= 1
                stack.append(x)
            return stack[:t]                                # trim if input was increasing

        def merge(a: List[int], b: List[int]) -> List[int]:
            i = j = 0
            out = []
            while i < len(a) or j < len(b):
                if a[i:] > b[j:]:                           # compare remaining tails, not heads
                    out.append(a[i])
                    i += 1
                else:
                    out.append(b[j])
                    j += 1
            return out

        best = []
        for i in range(max(0, k - len(nums2)), min(k, len(nums1)) + 1):
            best = max(best, merge(pick(nums1, i), pick(nums2, k - i)))
        return best


def brute_force(nums1: List[int], nums2: List[int], k: int) -> List[int]:
    def interleave(a, b):                                   # every order-preserving merge
        if not a or not b:
            yield a + b
            return
        for rest in interleave(a[1:], b):
            yield [a[0]] + rest
        for rest in interleave(a, b[1:]):
            yield [b[0]] + rest

    best = []
    for i in range(max(0, k - len(nums2)), min(k, len(nums1)) + 1):
        for ca in combinations(nums1, i):                   # exponential: 2^m * 2^n * C(k, i)
            for cb in combinations(nums2, k - i):
                for merged in interleave(list(ca), list(cb)):
                    best = max(best, merged)
    return best


if __name__ == "__main__":
    s = Solution()
    assert s.maxNumber([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5) == [9, 8, 6, 5, 3]
    assert s.maxNumber([6, 7], [6, 0, 4], 5) == [6, 7, 6, 0, 4]
    assert s.maxNumber([3, 9], [8, 9], 3) == [9, 8, 9]
    assert s.maxNumber([2, 5, 6, 4, 4, 0], [7, 3, 8, 0, 6, 5, 7, 6, 2], 15) == \
        [7, 3, 8, 2, 5, 6, 4, 4, 0, 6, 5, 7, 6, 2, 0]
    import random
    random.seed(5)
    for _ in range(150):
        a = [random.randint(0, 9) for _ in range(random.randint(0, 5))]
        b = [random.randint(0, 9) for _ in range(random.randint(0, 5))]
        if not a and not b:
            continue
        k = random.randint(1, len(a) + len(b))
        assert s.maxNumber(a, b, k) == brute_force(a, b, k), (a, b, k)
    print("ok")
