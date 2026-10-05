"""
Search in Rotated Sorted Array (LeetCode 33) - Medium
Area: binary search
Key operations: compute mid, decide which half is sorted, test target against the sorted half, move lo or hi

A sorted array of distinct integers was rotated at an unknown pivot. Return the index of target,
or -1 if it is absent, in O(log n).
Example: nums = [4, 5, 6, 7, 0, 1, 2], target = 0 -> 4
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int], target: int) -> int:
    """Linear scan. O(n): every probe discards one element although the array is almost sorted
    and could discard half."""
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


# --- optimal ---
def solve(nums: List[int], target: int) -> int:
    """Binary search where at every mid one half, [lo..mid] or [mid..hi], is plain sorted. Test
    the target against that half's endpoints: inside -> search it, else -> the other half.
    O(log n) time, O(1) space."""
    lo, hi = 0, len(nums) - 1
    log("".join(f"{x:4d}" for x in nums))
    while lo <= hi:
        mid = (lo + hi) // 2
        log("".join(f"{'^' if j in (lo, mid, hi) else '':>4}" for j in range(len(nums))) + f"   lo={lo} mid={mid} hi={hi}")
        if nums[mid] == target:
            log(f"    nums[{mid}] == {target}: found")
            return mid
        if nums[lo] <= nums[mid]:  # left half [lo..mid] is sorted
            log(f"    nums[lo]={nums[lo]} <= nums[mid]={nums[mid]}: left half [{nums[lo]}..{nums[mid]}] is sorted")
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
                log(f"    {target} is inside it: hi = {hi}")
            else:
                lo = mid + 1
                log(f"    {target} is not inside it: lo = {lo}")
        else:  # right half [mid..hi] is sorted
            log(f"    nums[lo]={nums[lo]} > nums[mid]={nums[mid]}: right half [{nums[mid]}..{nums[hi]}] is sorted")
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
                log(f"    {target} is inside it: lo = {lo}")
            else:
                hi = mid - 1
                log(f"    {target} is not inside it: hi = {hi}")
    log("    lo > hi: not found")
    return -1


# --- demo ---
def demo():
    return solve([4, 5, 6, 7, 0, 1, 2], 0)


# --- tests ---
def tests():
    assert solve([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert solve([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert solve([4, 5, 6, 7, 0, 1, 2], 4) == 0  # target equal to nums[lo]
    assert solve([4, 5, 6, 7, 0, 1, 2], 2) == 6  # target equal to nums[hi]
    assert solve([1], 0) == -1
    assert solve([1], 1) == 0
    assert solve([3, 1], 1) == 1  # two elements: lo == mid
    assert solve([5, 1, 3], 5) == 0
    assert solve([5, 1, 3], 3) == 2
    assert solve([1, 2, 3, 4, 5], 5) == 4  # no rotation at all
    import random
    rng = random.Random(33)
    for _ in range(200):
        n = rng.randint(1, 10)
        vals = sorted(rng.sample(range(-20, 21), n))
        k = rng.randrange(n)
        nums = vals[k:] + vals[:k]
        target = rng.choice(nums) if rng.random() < 0.6 else rng.randint(-25, 25)
        assert solve(nums, target) == brute_force(nums, target), (nums, target)


# --- bugs ---
BUGS = [
    {
        "replace": "        if nums[lo] <= nums[mid]:  # left half [lo..mid] is sorted",
        "with":    "        if nums[lo] < nums[mid]:  # left half [lo..mid] is sorted",
        "fix": "use <=: when lo == mid the one-element left half is sorted",
        "why": "With two elements mid equals lo, so nums[lo] < nums[mid] is false and the search wrongly treats the right half as sorted; [3, 1] with target 1 returns -1.",
        "decoys": [
            {"line": "        mid = (lo + hi) // 2", "change": "should be (lo + hi + 1) // 2"},
            {"line": "            if nums[mid] < target <= nums[hi]:", "change": "should be nums[mid] <= target"},
            {"line": "    while lo <= hi:", "change": "should be lo < hi"},
        ],
    },
    {
        "replace": "            if nums[lo] <= target < nums[mid]:",
        "with":    "            if nums[lo] < target < nums[mid]:",
        "fix": "the sorted left half includes its first element: nums[lo] <= target",
        "why": "A target equal to nums[lo] is sent to the right half and never found; [4, 5, 6, 7, 0, 1, 2] with target 4 returns -1.",
        "decoys": [
            {"line": "        if nums[mid] == target:", "change": "should be nums[mid] >= target"},
            {"line": "        if nums[lo] <= nums[mid]:  # left half [lo..mid] is sorted", "change": "should compare nums[lo] with nums[hi]"},
            {"line": "    return -1", "change": "should return lo"},
        ],
    },
    {
        "replace": "            if nums[mid] < target <= nums[hi]:",
        "with":    "            if nums[mid] < target < nums[hi]:",
        "fix": "the sorted right half includes its last element: target <= nums[hi]",
        "why": "A target equal to nums[hi] is sent to the left half and never found; [5, 1, 3] with target 3 returns -1.",
        "decoys": [
            {"line": "            return mid", "change": "should return nums[mid]"},
            {"line": "            if nums[lo] <= target < nums[mid]:", "change": "should be target <= nums[mid]"},
            {"line": "    lo, hi = 0, len(nums) - 1", "change": "should be hi = len(nums)"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
