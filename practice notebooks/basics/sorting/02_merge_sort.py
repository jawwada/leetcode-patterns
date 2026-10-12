"""
Merge Sort - Basics
Area: sorting
Key operations: split in half, sort each half recursively, merge two sorted runs with two pointers taking the left on ties

Split the array in half, sort each half, and merge the two sorted runs: repeatedly take the smaller
head, the left one on ties (that is what keeps the sort stable), then append whatever run is left over.
O(n log n) in every case, O(n) extra space for the merged runs.
Example: [5, 2, 4, 6, 1, 3] -> [1, 2, 3, 4, 5, 6]
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Python's sorted (Timsort), the reference for every sorting exercise. O(n log n)."""
    return sorted(nums)


# --- optimal ---
def merge(left: List[int], right: List[int]) -> List[int]:
    """Two pointers over two sorted runs; take the smaller head, left wins ties. O(len(left) + len(right))."""
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out += left[i:] + right[j:]
    return out


def solve(nums: List[int]) -> List[int]:
    """Split, sort both halves, merge. O(n log n): log n levels of O(n) merging."""
    if len(nums) <= 1:
        return list(nums)
    mid = len(nums) // 2
    left = solve(nums[:mid])
    right = solve(nums[mid:])
    return merge(left, right)


# --- demo ---
def demo():
    return solve([5, 2, 4, 6, 1, 3])


# --- bugs ---
BUGS = [
    {
        "replace": "    out += left[i:] + right[j:]",
        "with":    "    out += left[i:]",
        "fix": "append the leftovers of BOTH runs; only one of them is empty when the loop ends",
        "why": "When the left run empties first the rest of the right run is dropped: merge([1], [2, 3]) returns [1].",
        "decoys": [
            {"line": "        if left[i] <= right[j]:", "change": "should be < for stability"},
            {"line": "            j += 1", "change": "should be j = i + 1"},
            {"line": "    out, i, j = [], 0, 0", "change": "should start i and j at 1"},
        ],
    },
    {
        "replace": "    if len(nums) <= 1:",
        "with":    "    if len(nums) < 1:",
        "fix": "a run of ONE element is already sorted and must stop the recursion",
        "why": "A single element splits into [] and itself forever: solve([1]) recurses until RecursionError.",
        "decoys": [
            {"line": "    mid = len(nums) // 2", "change": "should be (len(nums) + 1) // 2"},
            {"line": "    right = solve(nums[mid:])", "change": "should be nums[mid + 1:]"},
            {"line": "    return merge(left, right)", "change": "should be merge(right, left)"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
