"""
Trapping Rain Water (LeetCode 42) - Medium-Hard
Area: two pointers
Key operations: compare the two ends, settle the lower side, update that side's running max, add max - height

Given an elevation map height[i] (bars of width 1), return how much water it traps after
raining. The water above bar i is min(tallest bar to its left, tallest bar to its right) - height[i].
Example: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] -> 6
"""
from typing import List


# --- brute force ---
def brute_force(height: List[int]) -> int:
    """For every bar scan left for the tallest bar and right for the tallest bar, add
    min(left, right) - height[i]. O(n^2): the two scans redo almost the same work for every bar."""
    water = 0
    for i in range(len(height)):
        left_max = max(height[:i + 1])
        right_max = max(height[i:])
        water += min(left_max, right_max) - height[i]
    return water


# --- optimal ---
def solve(height: List[int]) -> int:
    """Two pointers closing in, each carrying the tallest bar it has passed. The end with the
    lower bar is settled: its water is fixed by its own running max, because the other side
    already holds a taller bar. Every bar is settled once: O(n) time, O(1) space."""
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


# --- demo ---
def demo():
    return solve([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])


# --- bugs ---
BUGS = [
    {
        "replace": "            left_max = max(left_max, height[left])",
        "with":    "            left_max = height[left]",
        "fix": "keep the running maximum: left_max = max(left_max, height[left])",
        "why": "Overwriting left_max with the current bar forgets the wall behind it, so a dip on the left side like [1, 0, 2, 0, 3] gets 0 water above the 0s instead of 1 and 2.",
        "decoys": [
            {"line": "        if height[left] < height[right]:", "change": "should be <= so equal ends settle the left side"},
            {"line": "            right -= 1", "change": "should run before the water is added"},
            {"line": "    while left < right:", "change": "should be left <= right so the last bar is settled too"},
        ],
    },
    {
        "replace": "            right_max = max(right_max, height[right])",
        "with":    "            right_max = max(left_max, height[right])",
        "fix": "the right side keeps its own maximum: max(right_max, height[right])",
        "why": "The copy-paste slip feeds the left wall into the right side, so on [3, 0, 1] the right pointer settles index 1 with right_max 0 and adds 0 instead of 1.",
        "decoys": [
            {"line": "            water += left_max - height[left]", "change": "should add min(left_max, right_max) - height[left]"},
            {"line": "            left += 1", "change": "should run before left_max is updated"},
            {"line": "    left_max = right_max = 0", "change": "should start at height[0] and height[-1]"},
        ],
    },
    {
        "replace": "    while left < right:",
        "with":    "    while left < right - 1:",
        "fix": "loop while left < right: the bar under the second pointer still needs settling",
        "why": "Stopping one step early leaves one bar unsettled; on [2, 0, 2] the loop settles only index 2, the 0 is never visited and the answer is 0 instead of 2.",
        "decoys": [
            {"line": "        if height[left] < height[right]:", "change": "should compare left_max < right_max instead"},
            {"line": "            water += right_max - height[right]", "change": "should add right_max - height[right - 1]"},
            {"line": "    return water", "change": "should return water - left_max"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
