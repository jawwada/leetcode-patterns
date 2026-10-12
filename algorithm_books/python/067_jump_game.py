"""
Jump Game - Track the Farthest Reach

In a non-empty array, nums[i] is the longest jump allowed from index i (any
shorter jump is allowed too). Starting at index 0, can you reach the last index?
[2, 3, 1, 1, 4] -> True, [3, 2, 1, 0, 4] -> False.
"""


# --- algorithm ---
def can_jump(nums):
    """Grow the block [0, farthest] while i is in it. O(n) time, O(1) space."""
    farthest = 0                        # indices 0..farthest are reachable
    i = 0
    while i <= farthest:                # i is a spot we can really stand on
        farthest = max(farthest, i + nums[i])
        if farthest >= len(nums) - 1:   # the reach covers the last index
            return True
        i += 1
    return False                        # walked past the reach: a wall


# --- try it ---
print(can_jump([2, 3, 1, 1, 4]))    # -> True
print(can_jump([3, 2, 1, 0, 4]))    # -> False
print(can_jump([0]))                # -> True
print(can_jump([2, 0, 0]))          # -> True
print(can_jump([1, 0, 1]))          # -> False
