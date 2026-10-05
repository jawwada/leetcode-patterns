"""
3Sum (LeetCode 15) - Medium-Hard
Area: two pointers
Key operations: sort, fix the anchor i, converge lo/hi on the suffix, skip equal neighbours

Given an integer array, return every unique triplet [a, b, c] with a + b + c == 0. The order of the
triplets and of the numbers inside them does not matter; no triplet may appear twice.
Example: nums = [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]]
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[List[int]]:
    """Three nested loops over i < j < k, keep the sorted triplets in a set. O(n^3): for a fixed
    pair the third value is already known (-(a + b)) yet a whole loop searches for it, and every
    duplicate triplet is generated just to be thrown away by the set."""
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in found]


# --- optimal ---
def solve(nums: List[int]) -> List[List[int]]:
    """Sort; fix the smallest element i, then converge two pointers on the rest (sum too small:
    lo right, too big: hi left). Equal values are adjacent, so skipping equal neighbours yields
    each triplet once. O(n^2) after an O(n log n) sort, O(1) extra space."""
    nums = sorted(nums)
    n = len(nums)
    result = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo, hi = lo + 1, hi - 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
    return result


# --- demo ---
def demo():
    return solve([-1, 0, 1, 2, -1, -4])


# --- bugs ---
BUGS = [
    {
        "replace": "        if i > 0 and nums[i] == nums[i - 1]:",
        "with":    "        if i > 0 and nums[i] == nums[i + 1]:",
        "fix": "compare with the previous anchor nums[i - 1]",
        "why": "Comparing with the next element skips the first copy of a repeated value, so the triplet that needs two copies is lost: the example returns only [-1, 0, 1].",
        "decoys": [
            {"line": "        lo, hi = i + 1, n - 1", "change": "should be lo, hi = i, n - 1"},
            {"line": "    for i in range(n - 2):", "change": "should loop over range(n)"},
            {"line": "                while lo < hi and nums[hi] == nums[hi + 1]:", "change": "should compare with nums[hi - 1]"},
        ],
    },
    {
        "replace": "                while lo < hi and nums[lo] == nums[lo - 1]:",
        "with":    "                while lo < hi and nums[lo] == nums[lo + 1]:",
        "fix": "compare with the value just used, nums[lo - 1]",
        "why": "Comparing with the next element does not step past the value just recorded, so the same triplet is recorded again: [-2, 0, 0, 2, 2] returns [-2, 0, 2] twice.",
        "decoys": [
            {"line": "                lo, hi = lo + 1, hi - 1", "change": "should move only lo"},
            {"line": "            if total < 0:", "change": "should be total <= 0"},
            {"line": "    nums = sorted(nums)", "change": "should be sorted(nums, reverse=True)"},
        ],
    },
    {
        "replace": "        while lo < hi:",
        "with":    "        while lo <= hi:",
        "fix": "stop when the pointers meet: lo < hi",
        "why": "With <= the pointers can coincide and the same element is counted twice: [-2, 1, 3] returns [[-2, 1, 1]] instead of [].",
        "decoys": [
            {"line": "            total = nums[i] + nums[lo] + nums[hi]", "change": "should be nums[lo] + nums[hi]"},
            {"line": "            elif total > 0:", "change": "should be total >= 0"},
            {"line": "                result.append([nums[i], nums[lo], nums[hi]])", "change": "should append [i, lo, hi]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
