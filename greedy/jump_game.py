"""
Jump Game (LeetCode 55)  — Medium
Pattern: Greedy reach (furthest reachable index)

Problem
-------
You start at index 0 of `nums`; nums[i] is the maximum jump length from i. Return True if you can
reach the last index.
Example: nums = [2,3,1,1,4] -> True; nums = [3,2,1,0,4] -> False (always stuck at index 3).

Brute force
-----------
DFS/BFS over indices: from i try every jump 1..nums[i] and recurse; True if any path reaches the
end. Exponential time without memo, O(n) stack. The wasted work: many different paths land on the
same index, and we re-explore it each time — yet whether the end is reachable from index i does
not depend on how we got there.

From brute force to optimal
---------------------------
The redundancy is exploring individual paths. Observation: the set of indices reachable from 0 is
always a prefix [0, reach] — if you can reach i you can reach every index before it (shorter
jumps). So the whole state collapses to one number, `reach`. Scan left to right: if i > reach we
are stuck; otherwise reach = max(reach, i + nums[i]). The end is reachable iff reach >= n-1 at
some point. No recursion, no memo.

Intuition
---------
Track how far you could possibly get so far. Each index you can stand on pushes the frontier
forward by its jump length. If you ever arrive at an index beyond the frontier, you never
actually got there. Reaching the frontier past the last index wins.

Geometric view
--------------
A number line with a shaded prefix [0..reach] that only grows. The scan pointer i moves right
inside the shade; each stop extends the shade to max(reach, i + nums[i]). Fail = i steps out of
the shade; success = the shade covers n-1.

    nums:  [ 3, 2, 1, 0, 4 ]
    i=0 reach=3   ###---      shade covers 0..3
    i=3 reach=3   ####-       nums[3]=0, no extension
    i=4 > reach   stuck -> False

Steps
-----
1. reach = 0.
2. For i in range(n): if i > reach: return False; reach = max(reach, i + nums[i]).
3. Return True (loop finished, so n-1 was within reach).

Complexity: O(n) time, O(1) space — one scan with a single integer of state.
Pitfalls: checking `i > reach` AFTER updating reach (lets you "jump from" an unreachable index);
early-exiting on `reach >= n-1` is fine but not required.
"""
from typing import List


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        reach = 0                            # furthest index reachable so far
        for i, jump in enumerate(nums):
            if i > reach:                    # standing beyond the frontier: never got here
                return False
            reach = max(reach, i + jump)
        return True


def brute_force(nums: List[int]) -> bool:
    n = len(nums)

    def dfs(i: int) -> bool:
        if i >= n - 1:
            return True
        return any(dfs(i + step) for step in range(1, nums[i] + 1))

    return dfs(0)


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([2, 3, 1, 1, 4], True),
        ([3, 2, 1, 0, 4], False),
        ([0], True),
        ([1, 0, 1], False),
        ([2, 0, 0], True),
    ]
    for nums, want in cases:
        assert s.canJump(nums) == want
        assert brute_force(nums) == want
    print("ok")
