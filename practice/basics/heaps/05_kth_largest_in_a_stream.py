"""
Kth Largest Element in a Stream (LeetCode 703) - Basics
Area: heaps
Key operations: keep a min-heap of exactly k values, heappush then heappop when it overflows, answer is heap[0]

Design KthLargest(k, nums) with add(val) returning the k-th largest value seen so far (duplicates count).
Keep a min-heap of the k largest values: every add pushes, pops the root when the heap holds k + 1, and
answers with the root. solve(k, nums, adds) returns the answer after each add.
Example: k=3, nums=[4, 5, 8, 2], adds=[3, 5, 10, 9, 4] -> [4, 5, 5, 8, 8]
"""
import heapq
from typing import List


# --- brute force ---
def brute_force(k: int, nums: List[int], adds: List[int]) -> List[int]:
    """Keep everything, sort after every add and index from the end. O(n log n) per add."""
    seen, out = list(nums), []
    for v in adds:
        seen.append(v)
        out.append(sorted(seen)[-k])
    return out


# --- optimal ---
class KthLargest:
    """Min-heap of the k largest values seen; its root is the k-th largest. add is O(log k)."""

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            dropped = heapq.heappop(self.heap)
        return self.heap[0]


def solve(k: int, nums: List[int], adds: List[int]) -> List[int]:
    kth = KthLargest(k, nums)
    return [kth.add(v) for v in adds]


# --- demo ---
def demo():
    return solve(3, [4, 5, 8, 2], [3, 5, 10, 9, 4])


# --- bugs ---
BUGS = [
    {
        "replace": "        if len(self.heap) > self.k:",
        "with":    "        if len(self.heap) >= self.k:",
        "fix": "pop only when the heap holds k + 1 values; it must keep exactly k, the root being the k-th largest",
        "why": "At >= k the heap is trimmed to k - 1 values, so the root is the (k-1)-th largest: the example answers 5 instead of 4 on the first add.",
        "decoys": [
            {"line": "        heapq.heappush(self.heap, val)", "change": "should be heappushpop"},
            {"line": "        for x in nums:", "change": "should iterate nums[:k]"},
            {"line": "    return [kth.add(v) for v in adds]", "change": "should sort the results"},
        ],
    },
    {
        "replace": "        return self.heap[0]",
        "with":    "        return self.heap[-1]",
        "fix": "the k-th largest is the heap's ROOT at index 0, the smallest of the k kept",
        "why": "heap[-1] is just the last slot of the array, not the max and not the min: k=3 on [4, 5, 8] returns 8 instead of 4.",
        "decoys": [
            {"line": "            dropped = heapq.heappop(self.heap)", "change": "should be self.heap.pop()"},
            {"line": "        self.heap = []", "change": "should be list(nums)"},
            {"line": "        self.k = k", "change": "should be k - 1"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
