"""
Jump Game II (LeetCode 45)  — Medium
Pattern: Greedy reach (furthest reachable index)

Problem
-------
Same setup as Jump Game, but the last index is guaranteed reachable; return the MINIMUM number of
jumps to get there.
Example: nums = [2,3,1,1,4] -> 2 (0 -> 1 -> 4).

Brute force
-----------
BFS over indices one jump per level, or recursive "min over all jumps from i". BFS is O(n^2)
because from each index we enqueue every landing spot individually; naive recursion is
exponential. The wasted work: enqueuing indices one by one when every index reachable in j jumps
forms a contiguous interval — we only ever need the interval's right end.

From brute force to optimal
---------------------------
The redundancy is tracking individual positions per BFS level. Observation: the positions
reachable with exactly j jumps form a window [lo, hi] (a contiguous range), and the window for
j+1 is [hi+1, max(i + nums[i] for i in [lo, hi])]. So BFS collapses to: keep `cur_end` (end of
the current level) and `farthest` (max reach seen while scanning the level). Each time the scan
index i reaches cur_end, we must take another jump: jumps += 1, cur_end = farthest. Stop scanning
at n-2 because arriving at the last index needs no further jump.

Intuition
---------
This is BFS where each level is an interval. Walk through the current interval collecting the
furthest reach; when you step off its right edge, you have used one more jump and the next
interval is everything up to that furthest reach.

Geometric view
--------------
    nums:    [ 2, 3, 1, 1, 4 ]
    level 0:   [0]            farthest = 2
    level 1:      [1 2]       farthest = max(1+3, 2+1) = 4   -> covers index 4
    level 2:            [3 4] reached n-1 after 2 jumps

Steps
-----
1. jumps = cur_end = farthest = 0.
2. For i in range(n-1): farthest = max(farthest, i + nums[i]).
3. If i == cur_end: jumps += 1; cur_end = farthest.
4. Return jumps.

Complexity: O(n) time, O(1) space — one scan, three integers.
Pitfalls: iterating to n-1 inclusive (counts a spurious extra jump when you land exactly on the
end); updating cur_end before farthest; forgetting that n == 1 needs 0 jumps.
"""
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = cur_end = farthest = 0
        for i in range(len(nums) - 1):       # no need to jump from the last index
            farthest = max(farthest, i + nums[i])
            if i == cur_end:                 # end of this BFS level: must jump again
                jumps += 1
                cur_end = farthest
        return jumps


def brute_force(nums: List[int]) -> int:
    n = len(nums)
    dist = [-1] * n                          # BFS, enqueue every landing spot individually
    dist[0] = 0
    queue = [0]
    for i in queue:
        if i == n - 1:
            return dist[i]
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
    return dist[n - 1]


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([2, 3, 1, 1, 4], 2),
        ([2, 3, 0, 1, 4], 2),
        ([0], 0),
        ([1, 1, 1, 1], 3),
        ([5, 1, 1, 1, 1, 1], 1),
    ]
    for nums, want in cases:
        assert s.jump(nums) == want
        assert brute_force(nums) == want
    print("ok")
