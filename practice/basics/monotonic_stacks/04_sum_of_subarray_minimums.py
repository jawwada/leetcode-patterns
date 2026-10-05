"""
Sum of Subarray Minimums (LeetCode 907) - Basics
Area: monotonic stacks
Key operations: pop while top >= current (or at the end sentinel), count the subarrays whose minimum is the popped element, push index

Return the sum of min(b) over every contiguous subarray b, modulo 10^9 + 7. An element is the minimum
of (i - left) * (right - i) subarrays, where left is its previous strictly-smaller index and right its
next smaller-or-equal index; one increasing stack finds both at the moment the element is popped.
Example: [3, 1, 2, 4] -> 17  (3 + 1 + 2 + 4 + 1 + 1 + 2 + 1 + 1 + 1)
"""
from typing import List


# --- brute force ---
def brute_force(nums: List[int]) -> int:
    """Running minimum of every subarray [l..r]. O(n^2); the optimal method never looks at a subarray, only at each element's reach."""
    total = 0
    for l in range(len(nums)):
        m = nums[l]
        for r in range(l, len(nums)):
            m = min(m, nums[r])
            total += m
    return total % (10**9 + 7)


# --- optimal ---
def solve(nums: List[int]) -> int:
    """Indices on a strictly increasing stack; popping j at i means j is the minimum of (j - left) * (i - j) subarrays. O(n)."""
    n = len(nums)
    stack = []  # indices; nums strictly increasing bottom -> top
    total = 0
    for i in range(n + 1):  # i == n is the sentinel that pops everything
        while stack and (i == n or nums[stack[-1]] >= nums[i]):
            j = stack.pop()
            left = stack[-1] if stack else -1
            total += nums[j] * (j - left) * (i - j)
        if i < n:
            stack.append(i)
    return total % (10**9 + 7)


# --- demo ---
def demo():
    return solve([3, 1, 2, 4])


# --- bugs ---
BUGS = [
    {
        "replace": "            left = stack[-1] if stack else -1",
        "with":    "            left = stack[-1] if stack else 0",
        "fix": "with nothing under it the element reaches index 0, so its left boundary is -1 (one before the array)",
        "why": "[3, 1, 2, 4] gives index 0 a left of 0 and (0 - 0) = 0 subarrays, dropping the lone [3]: 14 instead of 17.",
        "decoys": [
            {"line": "            j = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "        if i < n:", "change": "should be i <= n"},
            {"line": "    return total % (10**9 + 7)", "change": "should return total"},
        ],
    },
    {
        "replace": "            total += nums[j] * (j - left) * (i - j)",
        "with":    "            total += nums[j] * (j - left) * (i - j + 1)",
        "fix": "the right end runs over [j, i), that is i - j choices; i itself is smaller-or-equal and excluded",
        "why": "Every popped element is credited with one extra subarray: [3, 1, 2, 4] sums to 27 instead of 17.",
        "decoys": [
            {"line": "        while stack and (i == n or nums[stack[-1]] >= nums[i]):", "change": "should be > for ties"},
            {"line": "            stack.append(i)", "change": "should append nums[i]"},
            {"line": "    total = 0", "change": "should start at nums[0]"},
        ],
    },
    {
        "replace": "    for i in range(n + 1):  # i == n is the sentinel that pops everything",
        "with":    "    for i in range(n):  # i == n is the sentinel that pops everything",
        "fix": "loop to n inclusive: the sentinel pass pops every index still waiting and counts its subarrays",
        "why": "Without the sentinel the survivors are never popped: [3, 1, 2, 4] counts only the 3 and returns 3.",
        "decoys": [
            {"line": "    n = len(nums)", "change": "should be len(nums) - 1"},
            {"line": "    stack = []  # indices; nums strictly increasing bottom -> top", "change": "should start as [-1]"},
            {"line": "            left = stack[-1] if stack else -1", "change": "should be nums[stack[-1]]"},
        ],
    },
]

if __name__ == "__main__":
    print("result:", demo())
