"""
Sliding Window Maximum (LeetCode 239) - Medium-Hard
Area: sliding window
Key operations: pop back while smaller or equal, push index, pop front when it leaves the window, read the max at the front

Given nums and a window size k, return the maximum of every contiguous window of k elements,
left to right.
Example: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3 -> [3, 3, 5, 5, 6, 7]
"""
from collections import deque
from typing import List


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
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


# --- demo ---
def demo():
    return solve([1, 3, -1, -3, 5, 3, 6, 7], 3)


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
    print("result:", demo())
