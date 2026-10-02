"""
Find the Duplicate Number (LeetCode 287)  — Medium
Pattern: Floyd's tortoise and hare (fast/slow pointers)

Problem
-------
nums has n + 1 integers, each in [1, n], and exactly one value repeats (possibly many
times). Return it without modifying nums and using O(1) extra space.
Example: nums = [1,3,4,2,2] -> 2; nums = [3,1,3,4,2] -> 3.

Brute force
-----------
Compare every pair (i, j) and return nums[i] when nums[i] == nums[j]. O(n^2) time, O(1)
space (a hash set gives O(n) time but breaks the O(1)-space rule; sorting breaks the
no-modify rule). The waste: every value is compared against every other value although
the input's shape (n + 1 values in [1, n]) already guarantees structure we never use.

From brute force to optimal
---------------------------
Step 1 (the original solution): binary search on the VALUE. For a guess mid, count how
many nums are <= mid; without a duplicate in [1, mid] that count is at most mid, so
count > mid means the duplicate is <= mid. This uses the pigeonhole structure and gives
O(n log n) time, O(1) space — but it still re-reads the whole array log n times.
Step 2: read the array as a linked list, i -> nums[i]. Every value is a valid index in
[1, n] and index 0 is never a target, so starting at 0 we walk a rho-shaped path. Two
indices pointing to the same value means two arrows enter one node: that node is exactly
where the cycle begins. Floyd's algorithm finds a cycle entrance in O(n) time, O(1) space,
without writing to nums.

Intuition
---------
The duplicate value is a node with in-degree 2 in the functional graph i -> nums[i]. A walk
from 0 must eventually loop (finite nodes), and the first repeated node on that walk is the
node with two incoming arrows — the duplicate. Floyd finds that first repeated node.

Geometric view
--------------
Draw indices as dots and nums[i] as arrows. Starting at 0 the arrows trace a tail into a
loop. Phase 1: slow (1 hop) and fast (2 hops) race until they meet inside the loop.
Phase 2: one pointer restarts at 0; both move 1 hop; they meet at the junction of the rho.

Steps
-----
1. slow = fast = 0; repeat slow = nums[slow], fast = nums[nums[fast]] until slow == fast.
2. slow = 0; while slow != fast: slow = nums[slow], fast = nums[fast].
3. Return slow (the cycle entrance = the duplicate value).

Complexity: O(n) time, O(1) space — two pointer phases, each O(n) hops.
Pitfalls: Starting phase 1 with a while-check before the first move (slow == fast at
start); returning the phase-1 meeting point instead of the entrance; treating the problem
as "single duplicate occurrence" when the value may repeat several times.
"""
from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = 0
        while True:                      # phase 1: meet somewhere inside the cycle
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = 0                         # phase 2: head and meeting point converge on entrance
        while slow != fast:
            slow, fast = nums[slow], nums[fast]
        return slow                      # the index with two incoming arrows


def brute_force(nums: List[int]) -> int:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):   # compares every pair of positions
            if nums[i] == nums[j]:
                return nums[i]
    return -1


if __name__ == "__main__":
    s = Solution()
    cases = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3), ([3, 3, 3, 3, 3], 3),
             ([1, 1], 1), ([2, 5, 9, 6, 9, 3, 8, 9, 7, 1], 9)]
    for nums, want in cases:
        assert s.findDuplicate(nums) == want
        assert brute_force(nums) == want
    print("ok")
