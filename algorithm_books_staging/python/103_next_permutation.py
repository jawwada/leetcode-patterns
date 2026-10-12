"""
Next Permutation - Find the Pivot, Swap, Reverse the Suffix

Rearrange an array in place into the next permutation in lexicographic order,
or into the first (sorted) one if it is already the last; values may repeat:
[1, 3, 5, 4, 2] -> [1, 4, 2, 3, 5], and [3, 2, 1] -> [1, 2, 3].
"""


# --- algorithm ---
def next_permutation(nums):
    """Find the pivot, swap it with the rightmost larger value, reverse the
    suffix. O(n) time, O(1) space, in place."""
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:    # walk past the falling suffix
        i -= 1
    if i >= 0:                                  # nums[i] is the pivot
        j = len(nums) - 1
        while nums[j] <= nums[i]:               # rightmost larger value
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    reverse(nums, i + 1, len(nums) - 1)         # falling suffix -> rising


def reverse(nums, left, right):
    """Reverse nums[left..right] in place, swapping the ends inward. O(n)."""
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


# --- try it ---
nums = [1, 3, 5, 4, 2]
next_permutation(nums)
print(nums)                         # -> [1, 4, 2, 3, 5]
nums = [3, 2, 1]
next_permutation(nums)
print(nums)                         # -> [1, 2, 3]
nums = [1, 5, 1]
next_permutation(nums)
print(nums)                         # -> [5, 1, 1]
nums = [7]
next_permutation(nums)
print(nums)                         # -> [7]
