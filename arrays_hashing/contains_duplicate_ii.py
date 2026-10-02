"""
Contains Duplicate II (LeetCode 219)  — Easy
Pattern: Hash map of last-seen index

Problem
-------
Given an integer array nums and an integer k, return True if there are two distinct
indices i and j with nums[i] == nums[j] and |i - j| <= k.
Example: nums = [1, 2, 3, 1], k = 3 -> True (indices 0 and 3).
         nums = [1, 2, 3, 1, 2, 3], k = 2 -> False.

Brute force
-----------
For each index i, compare nums[i] against the next k elements nums[i+1..i+k]. O(n * k)
time, O(1) space. The wasted work: for a fixed value we only care about where it was
LAST seen (the nearest earlier copy is the one most likely to be within k), yet we
re-scan a window of k elements for every single index.

From brute force to optimal
---------------------------
The brute force's window scan asks "did this value appear in the previous k
positions?" Instead of searching backwards, remember forward: keep a dict from value
-> index of its most recent occurrence. When we see v at index i, check whether
i - last[v] <= k. The most recent occurrence is the only one worth checking, since
any older copy is even farther away. Then overwrite last[v] = i. One dict lookup
replaces the k-element scan. (Equivalently, maintain a set of the last k values as a
sliding window — same complexity, O(min(n, k)) space.)

Intuition
---------
A duplicate within distance k always involves the nearest previous copy of the same
value. Track exactly one piece of information per value — where it was last seen —
and compare distances in O(1).

Geometric view
--------------
Picture a cursor sweeping right over the array, dragging behind it a "shadow" of
length k. Each value has a flag planted at its most recent position. When the cursor
lands on a value, it looks back at that value's flag: if the flag is inside the
shadow, the answer is True; either way the flag is moved to the cursor.

Steps
-----
1. last = {} mapping value -> most recent index.
2. For each index i with value v:
3.   if v in last and i - last[v] <= k, return True.
4.   last[v] = i.
5. Return False.

Complexity: O(n) time, O(n) space — one pass, one dict with at most n keys.
Pitfalls: checking only the first occurrence instead of the most recent; off-by-one on
<= k vs < k; k == 0 must return False (distinct indices required).
"""
from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        last = {}  # value -> most recent index; only the nearest copy can be within k
        for i, v in enumerate(nums):
            if v in last and i - last[v] <= k:
                return True
            last[v] = i
        return False


def brute_force(nums: List[int], k: int) -> bool:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, min(n, i + k + 1)):
            if nums[i] == nums[j]:
                return True
    return False


if __name__ == "__main__":
    s = Solution()
    assert s.containsNearbyDuplicate([1, 2, 3, 1], 3) is True
    assert s.containsNearbyDuplicate([1, 0, 1, 1], 1) is True
    assert s.containsNearbyDuplicate([1, 2, 3, 1, 2, 3], 2) is False
    assert s.containsNearbyDuplicate([1, 1], 0) is False
    assert s.containsNearbyDuplicate([], 5) is False
    for nums, k in [([1, 2, 3, 1], 3), ([1, 0, 1, 1], 1), ([1, 2, 3, 1, 2, 3], 2), ([1, 1], 0), ([], 5)]:
        assert s.containsNearbyDuplicate(nums, k) == brute_force(nums, k)
    print("ok")
