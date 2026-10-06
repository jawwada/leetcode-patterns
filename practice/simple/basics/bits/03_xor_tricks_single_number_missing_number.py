"""
XOR Tricks: Single Number and Missing Number (basics: bits)
Find the value without a pair, the value missing from 0..n, and the two values without a pair.
  [4, 1, 2, 1, 2]  ->  4   (1 ^ 1 and 2 ^ 2 cancel, 4 is left)

Idea: x ^ x == 0 and x ^ 0 == x in any order, so XOR-ing a list cancels every pair.
      Missing number: XOR the values and also 0..n; each present value cancels its twin.
      Two singles a, b: a set bit of a ^ b is set in only one of them, so it splits the list.

Pseudocode:
  single_number(nums):   acc = 0; for x in nums: acc ^= x; return acc
  missing_number(nums):  acc = n; for i, x in nums: acc ^= i ^ x; return acc
  two_single_numbers(nums):
      both = XOR of all nums                 # = a ^ b
      bit = both & -both                     # lowest bit where a and b differ
      a = XOR of the nums that have that bit; return [a, both ^ a]

Time O(n), space O(1).
"""


def single_number(nums):
    acc = 0
    for x in nums:
        acc ^= x                         # pairs cancel, the single survives
    return acc


def missing_number(nums):
    acc = len(nums)                      # n itself: enumerate gives only 0..n-1
    for i, x in enumerate(nums):
        acc ^= i ^ x                     # a present value cancels its equal index
    return acc


def two_single_numbers(nums):
    both = 0
    for x in nums:
        both ^= x                        # pairs cancel: both = a ^ b
    bit = both & -both                   # lowest bit where a and b differ
    a = 0
    for x in nums:
        if x & bit:                      # XOR only the group that has that bit
            a ^= x
    return [a, both ^ a]                 # the other single is (a ^ b) ^ a


if __name__ == "__main__":
    print(single_number([4, 1, 2, 1, 2]))          # 4
    print(missing_number([3, 0, 1]))               # 2
    print(two_single_numbers([1, 2, 1, 3, 2, 5]))  # [3, 5]
