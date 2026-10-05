"""
Sliding Window Maximum (LeetCode 239) - Medium-Hard
Area: sliding window
Key operations: pop back while smaller or equal, push index, pop front when it leaves the window, read the max at the front

Given nums and a window size k, return the maximum of every contiguous window of k elements,
left to right.
Example: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3 -> [3, 3, 5, 5, 6, 7]
"""
import sys
from collections import deque
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int], k: int) -> List[int]:
    """Take max() of every window. O(n*k): neighbouring windows share k-1 elements that are
    rescanned, most of which are dominated and could never be a maximum again."""
    out = []
    for i in range(len(nums) - k + 1):
        out.append(max(nums[i:i + k]))
    return out


# --- optimal ---
def solve(nums: List[int], k: int) -> List[int]:
    """Deque of indices whose values decrease front to back: the front is the window max. A new
    value evicts smaller-or-equal values from the back; the front expires when it leaves the
    window. Each index is pushed and popped once: O(n) time, O(k) space."""
    dq = deque()  # indices; nums[dq[0]] >= nums[dq[1]] >= ...
    out = []
    log(f"nums {nums} k {k}")
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            log(f"i={i} x={x:2d}  pop back {dq[-1]} ({nums[dq[-1]]} <= {x})")
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            log(f"i={i} x={x:2d}  pop front {dq[0]} (left the window, {dq[0]} <= {i - k})")
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
        log(f"i={i} x={x:2d}  push {i}  deque front->back {[(j, nums[j]) for j in dq]}  window [{max(0, i - k + 1)}..{i}] {nums[max(0, i - k + 1):i + 1]}  out {out}")
    return out


# --- demo ---
def demo():
    return solve([1, 3, -1, -3, 5, 3, 6, 7], 3)


# --- tests ---
def tests():
    assert solve([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert solve([1], 1) == [1]
    assert solve([9, 8, 7, 6], 2) == [9, 8, 7]  # the front expires every step
    assert solve([1, 2, 3, 4], 2) == [2, 3, 4]
    assert solve([4, 4, 4], 2) == [4, 4]  # equal values
    assert solve([1, 2, 3], 3) == [3]
    assert solve([5, 1, 1, 1], 2) == [5, 1, 1]
    assert solve([-2, -1], 1) == [-2, -1]
    import random
    random.seed(1)
    for _ in range(200):
        n = random.randint(1, 12)
        a = [random.randint(-5, 9) for _ in range(n)]
        k = random.randint(1, n)
        assert solve(a, k) == brute_force(a, k), (a, k)


# --- bugs ---
BUGS = [
    {
        "replace": "        if dq[0] <= i - k:",
        "with":    "        if dq[0] < i - k:",
        "fix": "the front leaves the window as soon as its index is <= i - k",
        "why": "Index i - k is already outside [i-k+1..i], so the front lingers one step too long: on [5, 1, 1, 1] with k = 2 the second window reports 5 instead of 1.",
        "decoys": [
            {"line": "        while dq and nums[dq[-1]] <= x:", "change": "should be < so equal values stay"},
            {"line": "        dq.append(i)", "change": "should run before the back is popped"},
            {"line": "    dq = deque()  # indices; nums[dq[0]] >= nums[dq[1]] >= ...", "change": "should start with index 0 inside"},
        ],
    },
    {
        "replace": "        if i >= k - 1:",
        "with":    "        if i >= k:",
        "fix": "the first full window ends at index k - 1",
        "why": "The first window's maximum is skipped, so the output is one element short: [1, 2, 3] with k = 3 returns [] instead of [3].",
        "decoys": [
            {"line": "            dq.popleft()", "change": "should be dq.pop()"},
            {"line": "            out.append(nums[dq[0]])", "change": "should append dq[0], the index"},
            {"line": "    return out", "change": "should return out[1:]"},
        ],
    },
    {
        "replace": "            out.append(nums[dq[0]])",
        "with":    "            out.append(nums[dq[-1]])",
        "fix": "the maximum sits at the front: nums[dq[0]]",
        "why": "The back of the deque is the newest survivor, the smallest candidate, so [1, 3, -1] with k = 3 reports -1 instead of 3.",
        "decoys": [
            {"line": "        if dq[0] <= i - k:", "change": "should be dq[0] < i - k + 1"},
            {"line": "            dq.pop()", "change": "should be dq.popleft()"},
            {"line": "        while dq and nums[dq[-1]] <= x:", "change": "should compare nums[dq[0]] <= x"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
