"""
Top K Largest with a Size-k Min-Heap - Basics
Area: heaps
Key operations: fill the heap to k, compare a new value with the root, heappushpop to replace the root, read the root as the k-th largest

Return the k largest values of a stream (1 <= k), in ascending order, using a min-heap that holds at
most k values: its root is the smallest of the best, so a new value gets in only when it beats the root,
and the root is what leaves. The heap never grows past k, so each step costs O(log k).
Example: nums=[3, 1, 5, 12, 2, 11], k=3 -> [5, 11, 12]
"""
import sys
import heapq
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int], k: int) -> List[int]:
    """Sort everything and keep the tail. O(n log n), sorts n - k values that could never be in the answer."""
    return sorted(nums)[-k:]


# --- optimal ---
def solve(nums: List[int], k: int) -> List[int]:
    """Min-heap of the k largest so far; the root is the gatekeeper. O(n log k)."""
    heap = []
    for x in nums:
        log(f"x={x:>2}: " + (f"heap has {len(heap)} < k, push" if len(heap) < k else f"beats root {heap[0]}, push x and pop the root" if x > heap[0] else f"not above root {heap[0]}, skip"))
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heappushpop(heap, x)
        log(f"       heap {heap}   k-th largest so far = root {heap[0]}, best {sorted(heap)}")
    return sorted(heap)


# --- demo ---
def demo():
    return solve([3, 1, 5, 12, 2, 11], 3)


# --- tests ---
def tests():
    assert solve([3, 1, 5, 12, 2, 11], 3) == [5, 11, 12]
    assert solve([], 2) == []
    assert solve([4], 1) == [4]
    assert solve([4, 9], 5) == [4, 9]  # k larger than the stream: everything
    assert solve([7, 7, 7, 1], 2) == [7, 7]
    assert solve([5, 4, 3, 2, 1], 2) == [4, 5]
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(0, 12))]
        k = rng.randint(1, 6)
        assert solve(a, k) == brute_force(a, k), (a, k)


# --- bugs ---
BUGS = [
    {
        "replace": "        elif x > heap[0]:",
        "with":    "        elif x < heap[0]:",
        "fix": "a value enters only when it is BIGGER than the root, the smallest of the current best",
        "why": "Reversed, the heap collects small values: [3, 1, 5, 12, 2, 11] with k=3 answers [1, 2, 3].",
        "decoys": [
            {"line": "        if len(heap) < k:", "change": "should be <= k"},
            {"line": "            heapq.heappushpop(heap, x)", "change": "should be heappush then heappop"},
            {"line": "    return sorted(heap)", "change": "should return heap"},
        ],
    },
    {
        "replace": "        if len(heap) < k:",
        "with":    "        if len(heap) <= k:",
        "fix": "push freely only while the heap has FEWER than k values; at k the root must compete",
        "why": "The heap grows to k + 1, so the answer has one extra value: k=3 on the example returns four numbers.",
        "decoys": [
            {"line": "        elif x > heap[0]:", "change": "should be >= to keep duplicates"},
            {"line": "            heapq.heappush(heap, x)", "change": "should be heappushpop"},
            {"line": "    heap = []", "change": "should start as sorted(nums[:k])"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
