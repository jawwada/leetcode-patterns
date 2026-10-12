"""
Single Number - XOR Cancels Pairs

Every element of a non-empty array appears twice except one, which appears
once; find it in O(n) time and O(1) extra space: [4, 1, 2, 1, 2] -> 4.
"""


# --- algorithm ---
def single_number(nums):
    """XOR everything: each pair cancels to 0, the single survives. O(n)."""
    result = 0
    for value in nums:
        result ^= value                 # x ^ x = 0 and x ^ 0 = x
    return result


def missing_number(nums):
    """nums holds 0..n with one value missing; XOR indices and values. O(n)."""
    result = len(nums)                  # index n has no slot of its own
    for i in range(len(nums)):
        result ^= i                     # value v cancels against index v
        result ^= nums[i]
    return result


# --- try it ---
print(single_number([4, 1, 2, 1, 2]))     # -> 4
print(single_number([-3, 7, 7]))          # -> -3
print(missing_number([3, 0, 1]))          # -> 2
print(missing_number([0, 1]))             # -> 2
