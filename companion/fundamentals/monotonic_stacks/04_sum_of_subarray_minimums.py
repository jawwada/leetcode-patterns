"""
Sum of Subarray Minimums (LeetCode 907) - Fundamentals
Chapter: fundamentals/monotonic_stacks
Key operations: pop while top >= current (or at the sentinel), count the popped index's subarrays

Return the sum of min(b) over every contiguous subarray b, modulo 10^9 + 7. An element at i is the
minimum of (i - left) * (right - i) subarrays, where left is its previous strictly-smaller index
and right its next smaller-or-equal index; one increasing stack finds both when it pops i.
Example: [3, 1, 2, 4] -> 17  (3 + 1 + 2 + 4 + 1 + 1 + 2 + 1 + 1 + 1)
"""


# --- algorithm ---
def sum_of_subarray_minimums(nums):
    """Increasing stack of indices; a popped index is the minimum of a known count of subarrays."""
    n = len(nums)
    stack = []                              # indices; nums[...] strictly increasing bottom -> top
    total = 0
    for right in range(n + 1):              # right == n is a sentinel that pops everything left
        while len(stack) > 0 and (right == n or nums[stack[-1]] >= nums[right]):
            middle = stack.pop()
            if len(stack) > 0:
                left = stack[-1]            # previous strictly smaller index
            else:
                left = -1
            # nums[middle] is the minimum of every subarray starting in (left, middle] and ending
            # in [middle, right): (middle - left) starts times (right - middle) ends
            total += nums[middle] * (middle - left) * (right - middle)
        if right < n:
            stack.append(right)
    return total % (10**9 + 7)


# --- try it ---
print(sum_of_subarray_minimums([3, 1, 2, 4]))         # -> 17
print(sum_of_subarray_minimums([11, 81, 94, 43, 3]))  # -> 444
print(sum_of_subarray_minimums([2, 2]))               # -> 6
print(sum_of_subarray_minimums([5]))                  # -> 5
