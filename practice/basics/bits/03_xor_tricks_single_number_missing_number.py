"""
XOR Tricks: Single Number and Missing Number (LeetCode 136) - Basics
Area: bits
Key operations: acc ^= x cancels pairs, xor with the indices 0..n finds the missing one, lowest set bit of a ^ b splits two singles

x ^ x == 0 and x ^ 0 == x, and XOR is commutative, so XOR-ing a whole list cancels every pair.
LeetCode 136: every element appears twice except one -> XOR all. LeetCode 268: nums holds 0..n with
one missing -> XOR all values and all indices 0..n. LeetCode 260: two singles a, b -> XOR all gives
a ^ b; any set bit of it (take the lowest) is set in exactly one of them; XOR each group separately.
Example: single_number([4, 1, 2, 1, 2]) -> 4; missing_number([3, 0, 1]) -> 2; single_number_iii([1, 2, 1, 3, 2, 5]) -> [3, 5]
"""
from collections import Counter
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Count every value and keep the ones seen once. O(n) time but O(n) extra memory for the counts."""
    return sorted(x for x, c in Counter(nums).items() if c == 1)


def brute_missing(nums: List[int]) -> int:
    """Set difference between 0..n and the list. O(n) time and memory."""
    return (set(range(len(nums) + 1)) - set(nums)).pop()


# --- optimal ---
def single_number(nums: List[int]) -> int:
    """XOR everything: pairs cancel, the single survives. O(n) time, O(1) space."""
    acc = 0
    for x in nums:
        acc ^= x
    return acc


def missing_number(nums: List[int]) -> int:
    """XOR 0..n with every element: each present value cancels its index copy, the missing one survives. O(n)."""
    acc = len(nums)
    for i, x in enumerate(nums):
        acc ^= i ^ x
    return acc


def single_number_iii(nums: List[int]) -> List[int]:
    """XOR of all is a ^ b; its lowest set bit tells a from b; XOR the group that has that bit. O(n)."""
    both = 0
    for x in nums:
        both ^= x
    diff = both & -both
    a = 0
    for x in nums:
        if x & diff:
            a ^= x
    return sorted([a, both ^ a])


# --- demo ---
def demo():
    return single_number([4, 1, 2, 1, 2]), missing_number([3, 0, 1]), single_number_iii([1, 2, 1, 3, 2, 5])


# --- bugs ---
BUGS = [
    {
        "replace": "    diff = both & -both",
        "with":    "    diff = both & (both - 1)",
        "fix": "isolate the lowest set bit with both & -both; both & (both - 1) DROPS it instead",
        "why": "When a ^ b has a single set bit the mask becomes 0, nothing joins the group, and [2, 3, 7, 7] answers [0, 1] instead of [2, 3].",
        "decoys": [
            {"line": "        if x & diff:", "change": "should be if x ^ diff"},
            {"line": "    return sorted([a, both ^ a])", "change": "should be [a, both & a]"},
            {"line": "        both ^= x", "change": "should be both |= x"},
        ],
    },
    {
        "replace": "    acc = len(nums)",
        "with":    "    acc = 0",
        "fix": "start the accumulator at n: the indices 0..n-1 come from enumerate, n itself must be added by hand",
        "why": "The value n is never XOR-ed in, so when n is the missing number the answer is 0: missing_number([0]) returns 0 instead of 1.",
        "decoys": [
            {"line": "        acc ^= i ^ x", "change": "should be acc ^= i + x"},
            {"line": "    both = 0", "change": "should start at len(nums)"},
            {"line": "    for i, x in enumerate(nums):", "change": "should enumerate from 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
