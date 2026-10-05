"""
Next Greater Element - Basics
Area: monotonic stacks
Key operations: pop while top < current, record answer for popped, push current

For each element return the first element to its right that is strictly greater, or -1.
Example: [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(nums: List[int]) -> List[int]:
    """Scan right from every index until a greater value. O(n^2)."""
    n = len(nums)
    ans = [-1] * n
    for i in range(n):
        for j in range(i + 1, n):
            if nums[j] > nums[i]:
                ans[i] = nums[j]
                break
    return ans


# --- optimal ---
def solve(nums: List[int]) -> List[int]:
    """Stack of indices with no greater element seen yet; values decrease bottom to top. O(n)."""
    n = len(nums)
    ans = [-1] * n
    stack = []  # indices; nums[stack] decreasing bottom -> top
    for i, x in enumerate(nums):
        log(f"i={i} x={x} | stack top->bottom {[nums[j] for j in reversed(stack)]}")
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            ans[j] = x
            log(f"    pop index {j} value {nums[j]} < {x}: ans[{j}] = {x}")
        stack.append(i)
        log(f"    push index {i}; ans {ans}")
    return ans


# --- demo ---
def demo():
    return solve([2, 1, 2, 4, 3])


# --- tests ---
def tests():
    assert solve([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert solve([1, 2, 3]) == [2, 3, -1]
    assert solve([3, 2, 1]) == [-1, -1, -1]
    assert solve([2, 2, 2]) == [-1, -1, -1]  # equal is not greater
    assert solve([]) == []
    import random
    for _ in range(200):
        a = [random.randint(1, 9) for _ in range(random.randint(0, 10))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "        while stack and nums[stack[-1]] < x:",
        "with":    "        while stack and nums[stack[-1]] > x:",
        "fix": "should be < x, pop while the top is smaller",
        "why": "Popping greater tops turns the stack increasing and records smaller values as 'next greater': [2, 1, 2] gives wrong answers.",
        "decoys": [
            {"line": "            ans[j] = x", "change": "should be ans[j] = i"},
            {"line": "        stack.append(i)", "change": "should append x"},
            {"line": "    ans = [-1] * n", "change": "should be [0] * n"},
        ],
    },
    {
        "replace": "            ans[j] = x",
        "with":    "            ans[j] = nums[stack[-1]] if stack else -1",
        "fix": "should be ans[j] = x, the current value",
        "why": "After the pop, stack[-1] is an older, larger element to the LEFT, not the next greater to the right.",
        "decoys": [
            {"line": "        while stack and nums[stack[-1]] < x:", "change": "should be <= to handle duplicates"},
            {"line": "            j = stack.pop()", "change": "should be stack.pop(0)"},
            {"line": "    return ans", "change": "should return ans[1:] + [-1]"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
