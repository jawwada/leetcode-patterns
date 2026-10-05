"""
Jump Game (LeetCode 55) - Medium
Chapter: greedy
Pattern: Greedy reach (furthest reachable index)

You start at index 0 and nums[i] is the maximum jump length from index i.
Return True if you can reach the last index.
Example: [2, 3, 1, 1, 4] -> True; [3, 2, 1, 0, 4] -> False (every path gets stuck at index 3).
"""


# --- brute force ---
def can_reach_end(nums, i):
    """Recursive helper: can we get from index i to the last index?"""
    if i >= len(nums) - 1:
        return True
    for step in range(1, nums[i] + 1):       # try every jump length from here
        if can_reach_end(nums, i + step):
            return True
    return False


def brute_force(nums):
    """Explore every path of jumps by recursion. Exponential time, O(n) stack."""
    return can_reach_end(nums, 0)


# --- optimal ---
def jump_game(nums):
    """Track the furthest index reachable so far in one scan. O(n) time, O(1) space."""
    reach = 0                                # furthest index we can stand on so far
    for i in range(len(nums)):
        if i > reach:                        # beyond the frontier: we never actually got here
            return False
        if i + nums[i] > reach:
            reach = i + nums[i]
    return True


# --- try the brute force ---
print(brute_force([2, 3, 1, 1, 4]))   # -> True
print(brute_force([3, 2, 1, 0, 4]))   # -> False
print(brute_force([0]))               # -> True
print(brute_force([1, 0, 1]))         # -> False


# --- try the optimal ---
print(jump_game([2, 3, 1, 1, 4]))   # -> True
print(jump_game([3, 2, 1, 0, 4]))   # -> False
print(jump_game([0]))               # -> True
print(jump_game([1, 0, 1]))         # -> False
