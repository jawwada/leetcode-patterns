"""
Jump Game II (LeetCode 45) - Medium
Chapter: greedy
Pattern: Greedy reach (furthest reachable index)

Same setup as Jump Game (nums[i] is the maximum jump length from i), and the last index is
guaranteed reachable. Return the minimum number of jumps needed to reach it.
Example: [2, 3, 1, 1, 4] -> 2 (jump 0 -> 1 -> 4).
"""
from collections import deque      # popleft is O(1)


# --- brute force ---
def brute_force(nums):
    """BFS over indices, one jump per level, enqueue each landing spot. O(n^2) time, O(n) space."""
    n = len(nums)
    jumps_to = [-1] * n                      # fewest jumps to reach each index, -1 = not yet seen
    jumps_to[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        if i == n - 1:
            return jumps_to[i]
        furthest = min(n - 1, i + nums[i])
        for j in range(i + 1, furthest + 1):
            if jumps_to[j] == -1:            # first time we land on j: that is the shortest way
                jumps_to[j] = jumps_to[i] + 1
                queue.append(j)
    return jumps_to[n - 1]


# --- optimal ---
def jump_game_ii(nums):
    """Each BFS level is a window of indices; track only its right edge. O(n) time, O(1) space."""
    jumps = 0
    current_end = 0                          # right edge of the indices reachable in `jumps` jumps
    farthest = 0                             # right edge of the next window
    for i in range(len(nums) - 1):           # arriving at the last index needs no further jump
        if i + nums[i] > farthest:
            farthest = i + nums[i]
        if i == current_end:                 # stepping off the current window: one more jump
            jumps = jumps + 1
            current_end = farthest
    return jumps


# --- try the brute force ---
print(brute_force([2, 3, 1, 1, 4]))      # -> 2
print(brute_force([2, 3, 0, 1, 4]))      # -> 2
print(brute_force([0]))                  # -> 0
print(brute_force([1, 1, 1, 1]))         # -> 3


# --- try the optimal ---
print(jump_game_ii([2, 3, 1, 1, 4]))     # -> 2
print(jump_game_ii([2, 3, 0, 1, 4]))     # -> 2
print(jump_game_ii([0]))                 # -> 0
print(jump_game_ii([1, 1, 1, 1]))        # -> 3
