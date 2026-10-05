"""
Binary Search Variants - Basics
Area: searches
Key operations: mid = (lo + hi) // 2, keep the half that can still hold the answer, lower_bound (first >= x), upper_bound (first > x)

On a sorted array find the index of x (or -1), the first index whose value is >= x (lower bound), the
first index whose value is > x (upper bound), and count = upper - lower. Both bounds use the half-open
range [lo, hi) and may return len(nums).
Example: [1, 2, 2, 2, 5, 7], x=2 -> index 2, lower 1, upper 4, count 3
"""
import sys
import bisect
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


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
        log(f"classic: lo={lo} mid={mid} hi={hi}, nums[mid]={nums[mid]}\n" + marks(nums, lo, mid, hi))
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
        log(f"lower: lo={lo} mid={mid} hi={hi}, nums[mid]={nums[mid]} {'< x: answer is right of mid' if nums[mid] < x else '>= x: mid could be it, keep it'}\n" + marks(nums, lo, mid, hi))
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
        log(f"upper: lo={lo} mid={mid} hi={hi}, nums[mid]={nums[mid]} {'<= x: answer is right of mid' if nums[mid] <= x else '> x: mid could be it, keep it'}\n" + marks(nums, lo, mid, hi))
        if nums[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def solve(nums, x):
    """Three O(log n) searches; count of x = upper - lower."""
    idx, lo, hi = classic(nums, x), lower_bound(nums, x), upper_bound(nums, x)
    log(f"x={x}: index {idx}; lower={lo} upper={hi} -> x occupies indices {lo}..{hi - 1}, count {hi - lo}")
    return {"index": idx, "lower": lo, "upper": hi, "count": hi - lo}


# --- demo ---
def demo():
    return solve([1, 2, 2, 2, 5, 7], 2)


# --- tests ---
def tests():
    assert solve([1, 2, 2, 2, 5, 7], 2) == {"index": 2, "lower": 1, "upper": 4, "count": 3}
    assert solve([1, 2, 2, 2, 5, 7], 3) == {"index": -1, "lower": 4, "upper": 4, "count": 0}  # absent, in the middle
    assert solve([1, 2, 2, 2, 5, 7], 0) == {"index": -1, "lower": 0, "upper": 0, "count": 0}  # smaller than all
    assert solve([1, 2, 2, 2, 5, 7], 9) == {"index": -1, "lower": 6, "upper": 6, "count": 0}  # bigger than all
    assert solve([1, 2, 2, 2, 5, 7], 7) == {"index": 5, "lower": 5, "upper": 6, "count": 1}  # last element
    assert solve([], 4) == {"index": -1, "lower": 0, "upper": 0, "count": 0}
    assert solve([4], 4) == {"index": 0, "lower": 0, "upper": 1, "count": 1}
    assert solve([4, 4, 4], 4) == {"index": 1, "lower": 0, "upper": 3, "count": 3}
    import random
    rng = random.Random(7)
    for _ in range(200):
        nums = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 10)))
        x = rng.randint(-1, 10)
        got, want = solve(nums, x), brute_force(nums, x)
        assert got["lower"] == want["lower"] == bisect.bisect_left(nums, x), (nums, x)
        assert got["upper"] == want["upper"] == bisect.bisect_right(nums, x), (nums, x)
        assert got["count"] == want["count"] == nums.count(x)
        assert (got["index"] == -1) == (want["index"] == -1), (nums, x)
        assert got["index"] == -1 or nums[got["index"]] == x    # any index of x is a valid classic answer


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
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
