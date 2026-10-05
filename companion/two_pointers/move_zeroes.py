"""
Move Zeroes (LeetCode 283) - Easy
Chapter: two_pointers
Pattern: Read/write pointers (stable compaction)

Move all 0s in nums to the end in place, keeping the relative order of the non-zero
elements; return nothing.
Example: nums = [0, 1, 0, 3, 12] -> [1, 3, 12, 0, 0].
"""


# --- brute force ---
def brute_force(nums):
    """Bubble zeros rightward one slot per pass until nothing moves. O(n^2) time."""
    moved = True
    while moved:
        moved = False
        for i in range(len(nums) - 1):
            if nums[i] == 0 and nums[i + 1] != 0:  # a zero sits in front of a non-zero
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                moved = True


# --- optimal ---
def move_zeroes(nums):
    """Write pointer for non-zeros, read pointer scans. O(n) time, O(1) space."""
    write = 0  # next slot for a non-zero; everything before it is done
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]  # the zero at write moves to read
            write += 1


# --- try the brute force ---
a = [0, 1, 0, 3, 12]
brute_force(a)
print(a)      # -> [1, 3, 12, 0, 0]
b = [0, 0, 1]
brute_force(b)
print(b)      # -> [1, 0, 0]
c = [4, 0, 5, 0, 0, 6]
brute_force(c)
print(c)      # -> [4, 5, 6, 0, 0, 0]


# --- try the optimal ---
a = [0, 1, 0, 3, 12]
move_zeroes(a)
print(a)      # -> [1, 3, 12, 0, 0]
b = [0, 0, 1]
move_zeroes(b)
print(b)      # -> [1, 0, 0]
c = [4, 0, 5, 0, 0, 6]
move_zeroes(c)
print(c)      # -> [4, 5, 6, 0, 0, 0]
