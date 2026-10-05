"""
Find Median from Data Stream (LeetCode 295) - Medium-Hard
Area: heap
Key operations: push into the max-heap low, move its max to the min-heap high, rebalance sizes, read the roots

Numbers arrive one at a time; after each one report the median of everything seen so far (the
middle value for an odd count, the mean of the two middle values for an even count).
Here solve(nums) returns the list of medians after each addition.
Example: [5, 15, 1, 3, 8] -> [5.0, 10.0, 5.0, 4.0, 5.0]
"""
import heapq
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[float]:
    """Append, then sort everything and read the middle after each addition. O(n log n) per
    addition: the full order of both halves is rebuilt although only the seam matters."""
    seen, medians = [], []
    for x in nums:
        seen.append(x)
        a = sorted(seen)
        m = len(a) // 2
        medians.append(float(a[m]) if len(a) % 2 else (a[m - 1] + a[m]) / 2)
    return medians


# --- optimal ---
def solve(nums: List[int]) -> List[float]:
    """low is a max-heap (negated) of the smaller half, high a min-heap of the larger half; the
    median sits at their roots. Invariant: every low <= every high and len(low) - len(high) is 0
    or 1. O(log n) per addition, O(1) per median."""
    low, high, medians = [], [], []
    for x in nums:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))
        if len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        if len(low) > len(high):
            medians.append(float(-low[0]))
        else:
            medians.append((-low[0] + high[0]) / 2)
    return medians


# --- demo ---
def demo():
    return solve([5, 15, 1, 3, 8])


# --- bugs ---
BUGS = [
    {
        "replace": "        heapq.heappush(high, -heapq.heappop(low))",
        "with":    "        heapq.heappush(high, heapq.heappop(low))",
        "fix": "negate the value when it crosses from low (negated) to high",
        "why": "low stores -x, so the popped value must be negated back before entering high; otherwise high holds negatives, every median comes out with the wrong sign and [1, 2] reports -1.5 instead of 1.5.",
        "decoys": [
            {"line": "        heapq.heappush(low, -x)", "change": "should push x without the minus"},
            {"line": "            heapq.heappush(low, -heapq.heappop(high))", "change": "should push heapq.heappop(high) as is"},
            {"line": "            medians.append(float(-low[0]))", "change": "should be float(low[0])"},
        ],
    },
    {
        "replace": "        if len(high) > len(low):",
        "with":    "        if len(high) >= len(low):",
        "fix": "rebalance only when high is strictly bigger; equal is fine",
        "why": "With >= a balanced pair is unbalanced again, so low always holds one extra value and even counts read a single root: [1, 2] gives 2.0 instead of 1.5.",
        "decoys": [
            {"line": "        if len(low) > len(high):", "change": "should be len(low) >= len(high)"},
            {"line": "        heapq.heappush(high, -heapq.heappop(low))", "change": "should only run when x > high[0]"},
            {"line": "    low, high, medians = [], [], []", "change": "high should start as [float('inf')]"},
        ],
    },
    {
        "replace": "            medians.append((-low[0] + high[0]) / 2)",
        "with":    "            medians.append((-low[0] + high[0]) // 2)",
        "fix": "use true division: an even count's median can be a half",
        "why": "Floor division truncates the mean of the two middle values: [1, 2] reports 1 instead of 1.5.",
        "decoys": [
            {"line": "            medians.append(float(-low[0]))", "change": "should average -low[0] and high[0]"},
            {"line": "        if len(low) > len(high):", "change": "should compare with len(high) + 1"},
            {"line": "    return medians", "change": "should return medians[-1]"},
        ],
    },
    {
        "replace": "        if len(low) > len(high):",
        "with":    "        if len(low) >= len(high):",
        "fix": "a single root is the median only when low is strictly bigger",
        "why": "With >= an even count also reads only max(low): [1, 2] reports 1.0 instead of 1.5.",
        "decoys": [
            {"line": "        if len(high) > len(low):", "change": "should be len(high) > len(low) + 1"},
            {"line": "        heapq.heappush(low, -x)", "change": "should push into high when x is large"},
            {"line": "            medians.append((-low[0] + high[0]) / 2)", "change": "should be (low[0] + high[0]) / 2"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
