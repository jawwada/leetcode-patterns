"""
XOR Tricks: Single Number and Missing Number - Fundamentals
Chapter: fundamentals/bits
Key operations: xor cancels pairs, xor indices 0..n finds the missing, lowest bit of a^b splits two

x ^ x == 0 and x ^ 0 == x, and XOR is commutative, so XOR-ing a whole list cancels every pair.
LeetCode 136: every element appears twice except one -> XOR all. LeetCode 268: nums holds 0..n
with one missing -> XOR all values and all indices 0..n. LeetCode 260: two singles a, b -> XOR all
gives a ^ b; any set bit of it (take the lowest) is set in exactly one of them; XOR each group.
Example: [4, 1, 2, 1, 2] -> 4; [3, 0, 1] misses 2; two singles of [1, 2, 1, 3, 2, 5] -> [3, 5]
"""


# --- algorithm ---
def single_number(nums):
    """XOR everything: pairs cancel, the single survives. O(n) time, O(1) space."""
    acc = 0
    for x in nums:
        acc ^= x
    return acc


def missing_number(nums):
    """XOR the indices 0..n with every element: present values cancel their index copy. O(n)."""
    acc = len(nums)   # index n has no element to pair with, so it starts the accumulator
    for i in range(len(nums)):
        acc ^= i
        acc ^= nums[i]
    return acc


def two_single_numbers(nums):
    """XOR of all is a ^ b; its lowest set bit tells a from b; XOR the group having it. O(n)."""
    both = 0
    for x in nums:
        both ^= x           # pairs cancel: both == a ^ b
    diff = both & -both     # lowest set bit of a ^ b: set in exactly one of a, b
    first = 0
    for x in nums:
        if x & diff:        # only the group with this bit; pairs still cancel inside it
            first ^= x
    second = both ^ first
    return sorted([first, second])


# --- try it ---
print(single_number([4, 1, 2, 1, 2]))             # -> 4
print(single_number([7]))                         # -> 7
print(missing_number([3, 0, 1]))                  # -> 2
print(missing_number([0, 1]))                     # -> 2
print(two_single_numbers([1, 2, 1, 3, 2, 5]))     # -> [3, 5]
print(two_single_numbers([0, 9]))                 # -> [0, 9]
