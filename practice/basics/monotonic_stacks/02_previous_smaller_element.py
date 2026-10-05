"""
Previous Smaller Element - Basics
Area: monotonic stacks
Key operations: pop while top >= current, answer is the survivor under the current, push current

For each element return the nearest element to its LEFT that is strictly smaller, or -1.
Example: [3, 1, 4, 1, 5] -> [-1, -1, 1, -1, 1]
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Scan left from every index until a smaller value. O(n^2)."""
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if nums[j] < nums[i]:
                ans[i] = nums[j]
                break
    return ans


# --- optimal ---
def solve(nums: List[int]) -> List[int]:
    """Stack of values strictly increasing bottom to top; after popping everything >= x the top is x's answer. O(n)."""
    ans = [-1] * len(nums)
    stack = []  # values increasing bottom -> top
    for i, x in enumerate(nums):
        while stack and stack[-1] >= x:
            popped = stack.pop()
        ans[i] = stack[-1] if stack else -1
        stack.append(x)
    return ans


# --- demo ---
def demo():
    return solve([3, 1, 4, 1, 5])


# --- bugs ---
BUGS = [
    {
        "replace": "        while stack and stack[-1] >= x:",
        "with":    "        while stack and stack[-1] > x:",
        "fix": "pop equal values too: 'smaller' is strict, so an equal survivor must not be reported as the answer",
        "why": "[2, 2] keeps the first 2 on the stack and reports it as the previous smaller of the second 2 instead of -1.",
        "decoys": [
            {"line": "        stack.append(x)", "change": "should append i"},
            {"line": "    ans = [-1] * len(nums)", "change": "should be [0] * len(nums)"},
            {"line": "    return ans", "change": "should return ans[::-1]"},
        ],
    },
    {
        "replace": "        ans[i] = stack[-1] if stack else -1",
        "with":    "        ans[i] = stack[0] if stack else -1",
        "fix": "the answer is the TOP survivor (nearest smaller), not the bottom (smallest so far)",
        "why": "[1, 2, 3] reports 1 for the 3 because stack[0] is the overall minimum, but the nearest smaller is 2.",
        "decoys": [
            {"line": "            popped = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    for i, x in enumerate(nums):", "change": "should iterate reversed(nums)"},
            {"line": "    stack = []  # values increasing bottom -> top", "change": "should start as [-1]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
