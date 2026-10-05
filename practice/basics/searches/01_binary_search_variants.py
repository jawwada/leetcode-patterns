"""
Binary Search Variants - Basics
Area: searches
Key operations: mid = (lo + hi) // 2, keep the half that can still hold the answer, lower_bound (first >= x), upper_bound (first > x)

On a sorted array find the index of x (or -1), the first index whose value is >= x (lower bound), the
first index whose value is > x (upper bound), and count = upper - lower. Both bounds use the half-open
range [lo, hi) and may return len(nums).
Example: [1, 2, 2, 2, 5, 7], x=2 -> index 2, lower 1, upper 4, count 3
"""
from typing import List


def marks(nums, lo, mid, hi):
    """Trace only: the array on one line, ^L ^M ^H under lo, mid, hi (a | marks index len(nums))."""
    tags = {}
    for name, i in (("L", lo), ("M", mid), ("H", hi)):
        tags[i] = tags.get(i, "") + name
    row = "".join(f"{v:>5}" for v in nums) + "    |"
    under = "".join(f"{'^' + tags[i] if i in tags else '':>5}" for i in range(len(nums) + 1))
    return row + "\n" + under


# --- brute force ---
def brute_force(nums: List[int], x: int) -> dict:
    """Linear scans: first equal, first >= x, first > x. O(n) each, ignores that the array is sorted."""
    index = next((i for i, v in enumerate(nums) if v == x), -1)
    lower = next((i for i, v in enumerate(nums) if v >= x), len(nums))
    upper = next((i for i, v in enumerate(nums) if v > x), len(nums))
    return {"index": index, "lower": lower, "upper": upper, "count": upper - lower}


# --- optimal ---
def classic(nums, x):
    """Closed range [lo, hi]; stop when it is empty. O(log n)."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == x:
            return mid
        elif nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(nums, x):
    """First index with nums[i] >= x. Half-open [lo, hi); lo is always the first index that might still be the answer."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums, x):
    """First index with nums[i] > x: same loop, the only change is <= instead of <."""
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def solve(nums, x):
    """Three O(log n) searches; count of x = upper - lower."""
    idx, lo, hi = classic(nums, x), lower_bound(nums, x), upper_bound(nums, x)
    return {"index": idx, "lower": lo, "upper": hi, "count": hi - lo}


# --- demo ---
def demo():
    return solve([1, 2, 2, 2, 5, 7], 2)


# --- bugs ---
BUGS = [
    {
        "replace": "    while lo <= hi:",
        "with":    "    while lo < hi:",
        "fix": "the closed range [lo, hi] still holds one candidate when lo == hi, so loop while lo <= hi",
        "why": "The last candidate is never examined: searching 7 in [1, 2, 2, 2, 5, 7] narrows to lo = hi = 5 and returns -1.",
        "decoys": [
            {"line": "        if nums[mid] == x:", "change": "should be nums[mid] is x"},
            {"line": "            hi = mid - 1", "change": "should be hi = mid"},
            {"line": "    lo, hi = 0, len(nums) - 1", "change": "should be 0, len(nums)"},
        ],
    },
    {
        "replace": "        if nums[mid] < x:",
        "with":    "        if nums[mid] <= x:",
        "fix": "lower_bound keeps mid when nums[mid] >= x; only strictly smaller values are discarded",
        "why": "With <= the loop skips past every x and lower_bound becomes upper_bound: count of 2 in [1, 2, 2, 2, 5, 7] is 0.",
        "decoys": [
            {"line": "        if nums[mid] <= x:", "change": "should be < to be consistent with lower_bound"},
            {"line": "    idx, lo, hi = classic(nums, x), lower_bound(nums, x), upper_bound(nums, x)", "change": "should call upper_bound before lower_bound"},
            {"line": "    return -1", "change": "should return lo"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
