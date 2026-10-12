"""
Jump Game II - Greedy BFS over Reach Levels

nums[i] is the longest jump allowed from index i, and the last index is known
to be reachable. Return the fewest jumps from index 0 to the last index:
[2, 3, 1, 1, 4] -> 2 (index 0 -> 1 -> 4).
"""


# --- algorithm ---
def min_jumps(nums):
    """BFS whose levels are intervals; count levels. O(n) time, O(1) space."""
    jumps = 0
    current_end = 0                 # right edge of the current level
    farthest = 0                    # right edge of the next level
    for i in range(len(nums) - 1):  # never jump from the last index
        farthest = max(farthest, i + nums[i])
        if i == current_end:        # this level is used up: jump again
            jumps += 1
            current_end = farthest  # the next level ends here
    return jumps


# --- try it ---
print(min_jumps([2, 3, 1, 1, 4]))   # -> 2
print(min_jumps([2, 3, 0, 1, 4]))   # -> 2
print(min_jumps([1, 1, 1, 1]))      # -> 3
print(min_jumps([0]))               # -> 0
