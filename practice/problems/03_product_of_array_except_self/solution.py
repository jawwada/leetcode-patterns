"""
Product of Array Except Self (LeetCode 238) - Medium
Area: arrays & hashing
Key operations: left sweep stamping prefix products, right sweep multiplying in a running suffix product

Given an integer array nums, return answer where answer[i] is the product of every element except
nums[i]. No division, O(n) time; the output array does not count as extra space.
Example: nums = [1, 2, 3, 4] -> [24, 12, 8, 6]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """For each i multiply every other element. O(n^2): answer[i] and answer[i + 1] share n - 2
    factors, yet that shared product is rebuilt from scratch for every position."""
    n = len(nums)
    answer = []
    for i in range(n):
        prod = 1
        for j in range(n):
            if j != i:
                prod *= nums[j]
        answer.append(prod)
    return answer


# --- optimal ---
def solve(nums: List[int]) -> List[int]:
    """answer[i] = (product of everything left of i) * (product of everything right of i). Stamp the
    left products into answer in one sweep, then multiply a running right product in on the way
    back. O(n) time, O(1) extra space."""
    n = len(nums)
    answer = [1] * n
    prefix = 1  # product of nums[0..i-1]
    log(f"nums {nums}")
    log("left sweep: answer[i] = product of nums[0..i-1]")
    for i in range(n):
        answer[i] = prefix
        log(f"  i={i}: answer[{i}] = prefix = {prefix:3d}")
        prefix *= nums[i]
        log(f"        prefix *= nums[{i}] = {nums[i]} -> {prefix:3d} | answer {answer}")
    suffix = 1  # product of nums[i+1..n-1]
    log("right sweep: answer[i] *= product of nums[i+1..n-1]")
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        log(f"  i={i}: answer[{i}] *= suffix {suffix} -> {answer[i]:3d}")
        suffix *= nums[i]
        log(f"        suffix *= nums[{i}] = {nums[i]} -> {suffix:3d} | answer {answer}")
    return answer


# --- demo ---
def demo():
    return solve([1, 2, 3, 4])


# --- tests ---
def tests():
    assert solve([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert solve([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert solve([0, 0, 2]) == [0, 0, 0]
    assert solve([5, 2]) == [2, 5]
    assert solve([7]) == [1]
    assert solve([]) == []
    import random
    for _ in range(200):
        a = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "        answer[i] = prefix",
        "with":    "        answer[i] = prefix * nums[i]",
        "fix": "stamp prefix before multiplying nums[i] in",
        "why": "answer[i] then contains nums[i] itself, so [1, 2, 3, 4] gives [24, 24, 24, 24] instead of [24, 12, 8, 6].",
        "decoys": [
            {"line": "        prefix *= nums[i]", "change": "should be prefix *= answer[i]"},
            {"line": "    answer = [1] * n", "change": "should start as [0] * n"},
            {"line": "        suffix *= nums[i]", "change": "should run before answer[i] *= suffix"},
        ],
    },
    {
        "replace": "    for i in range(n - 1, -1, -1):",
        "with":    "    for i in range(n - 1, 0, -1):",
        "fix": "stop at -1 so index 0 is swept too",
        "why": "Index 0 never receives its suffix product, so [1, 2, 3, 4] gives [1, 12, 8, 6] instead of [24, 12, 8, 6].",
        "decoys": [
            {"line": "    for i in range(n):", "change": "should be range(1, n)"},
            {"line": "    suffix = 1  # product of nums[i+1..n-1]", "change": "should start as nums[-1]"},
            {"line": "        answer[i] *= suffix", "change": "should be answer[i] *= suffix * nums[i]"},
        ],
    },
    {
        "replace": "        answer[i] *= suffix",
        "with":    "        answer[i] = suffix",
        "fix": "multiply with *=, keep the stamped prefix",
        "why": "The left products are overwritten, so answer[i] is only the product of the right side: [1, 2, 3, 4] gives [24, 12, 4, 1].",
        "decoys": [
            {"line": "        answer[i] = prefix", "change": "should be answer[i] *= prefix"},
            {"line": "    prefix = 1  # product of nums[0..i-1]", "change": "should start as nums[0]"},
            {"line": "    return answer", "change": "should return answer[::-1]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
