"""
Split Array Largest Sum (LeetCode 410) - Medium-Hard
Area: binary search
Key operations: binary search on the answer (a cap), greedy count of pieces under the cap, hi = mid when pieces <= k

Split nums into k non-empty contiguous pieces so that the largest piece sum is as small as
possible; return that largest sum.
Example: nums = [7, 2, 5, 10, 8], k = 2 -> 18 (pieces [7, 2, 5] | [10, 8])
"""
import sys
from itertools import combinations
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int], k: int) -> int:
    """Try every placement of k - 1 cuts among the n - 1 gaps, sum the pieces, keep the smallest
    largest piece. C(n-1, k-1) placements of O(n) each: exponential. The wasted work: almost every
    placement is hopeless, and placements sharing a prefix of cuts re-sum the same pieces."""
    n = len(nums)
    best = sum(nums)
    for cuts in combinations(range(1, n), k - 1):
        bounds = (0, *cuts, n)
        largest = max(sum(nums[a:b]) for a, b in zip(bounds, bounds[1:]))
        best = min(best, largest)
    return best


# --- optimal ---
def solve(nums: List[int], k: int) -> int:
    """Binary search the cap in [max(nums), sum(nums)]. feasible(cap) = greedy pieces(cap) <= k is
    monotone: a bigger cap never needs more pieces. O(n log sum(nums)) time, O(1) space."""
    def pieces(cap: int) -> int:
        count, cur = 1, 0  # greedy: fewest pieces with every piece sum <= cap
        for x in nums:
            if cur + x > cap:
                log(f"    piece {count} closed at sum {cur} ({cur} + {x} > {cap}); piece {count + 1} starts with {x}")
                count += 1
                cur = 0
            cur += x
        log(f"    piece {count} closed at sum {cur} (end) -> {count} pieces under cap {cap}")
        return count

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        log(f"cap range [{lo}..{hi}], try cap {mid}")
        if pieces(mid) <= k:
            hi = mid
            log(f"    at most {k} pieces: feasible, the answer is {mid} or less, hi = {hi}")
        else:
            lo = mid + 1
            log(f"    more than {k} pieces: cap too small, lo = {lo}")
    log(f"lo == hi == {lo}: the smallest feasible cap")
    return lo


# --- demo ---
def demo():
    return solve([7, 2, 5, 10, 8], 2)


# --- tests ---
def tests():
    assert solve([7, 2, 5, 10, 8], 2) == 18
    assert solve([1, 2, 3, 4, 5], 2) == 9
    assert solve([1, 4, 4], 3) == 4
    assert solve([5], 1) == 5  # single element
    assert solve([2, 3, 1, 2, 4, 3], 6) == 4  # k == n: the largest element
    assert solve([2, 3, 1, 2, 4, 3], 1) == 15  # k == 1: the whole sum
    assert solve([9, 9, 9], 2) == 18  # a piece exactly at the cap is allowed
    assert solve([0, 0, 0], 2) == 0
    import random
    rng = random.Random(410)
    for _ in range(200):
        nums = [rng.randint(0, 15) for _ in range(rng.randint(1, 8))]
        k = rng.randint(1, len(nums))
        assert solve(nums, k) == brute_force(nums, k), (nums, k)


# --- bugs ---
BUGS = [
    {
        "replace": "            if cur + x > cap:",
        "with":    "            if cur + x >= cap:",
        "fix": "a piece may sum to exactly cap, so cut only when cur + x > cap",
        "why": "A piece that lands exactly on the cap is cut one element early, so the greedy count is too high and feasible caps are rejected; [9, 9, 9] with k = 2 gives 19 instead of 18.",
        "decoys": [
            {"line": "            cur += x", "change": "should be cur = x"},
            {"line": "    lo, hi = max(nums), sum(nums)", "change": "should be hi = sum(nums) + 1"},
            {"line": "        if pieces(mid) <= k:", "change": "should be < k"},
        ],
    },
    {
        "replace": "        if pieces(mid) <= k:",
        "with":    "        if pieces(mid) == k:",
        "fix": "fewer than k pieces is still feasible (split any piece further), so test <= k",
        "why": "A cap that needs fewer than k pieces is wrongly treated as infeasible and the search drifts upward; [1, 4, 4] with k = 3 returns 9 instead of 4.",
        "decoys": [
            {"line": "            hi = mid", "change": "should be hi = mid - 1"},
            {"line": "        count, cur = 1, 0  # greedy: fewest pieces with every piece sum <= cap", "change": "should start count at 0"},
            {"line": "    return lo", "change": "should return hi"},
        ],
    },
    {
        "replace": "    lo, hi = max(nums), sum(nums)",
        "with":    "    lo, hi = 0, sum(nums)",
        "fix": "start lo at max(nums): every element must fit in its own piece",
        "why": "With a cap below the largest element the greedy still places that element, so the count can look feasible for an impossible cap; [2, 3, 1, 2, 4, 3] with k = 6 returns 2 instead of 4.",
        "decoys": [
            {"line": "        mid = (lo + hi) // 2", "change": "should be (lo + hi + 1) // 2"},
            {"line": "            lo = mid + 1", "change": "should be lo = mid"},
            {"line": "            if cur + x > cap:", "change": "should be cur > cap"},
        ],
    },
    {
        "replace": "        count, cur = 1, 0  # greedy: fewest pieces with every piece sum <= cap",
        "with":    "        count, cur = 0, 0  # greedy: fewest pieces with every piece sum <= cap",
        "fix": "the first piece exists before any cut, so count starts at 1",
        "why": "Every count is one too low, so caps that need k + 1 pieces pass the test; [7, 2, 5, 10, 8] with k = 2 returns 14 instead of 18.",
        "decoys": [
            {"line": "                count += 1", "change": "should run after cur += x"},
            {"line": "                cur = 0", "change": "should be cur = x"},
            {"line": "        return count", "change": "should return count - 1"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
