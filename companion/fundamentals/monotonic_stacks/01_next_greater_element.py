"""
Next Greater Element - Fundamentals
Chapter: fundamentals/monotonic_stacks
Key operations: pop while top < current, record answer for popped, push current

For each element return the first element to its right that is strictly greater, or -1. The stack
holds the indices still waiting for their answer, with values decreasing bottom to top; a new
element answers every waiting element it beats.
Example: [2, 1, 2, 4, 3] -> [4, 2, 4, -1, -1]
"""


# --- algorithm ---
def next_greater_element(nums):
    """Stack of indices with no greater element seen yet; values decrease bottom to top. O(n)."""
    n = len(nums)
    answer = [-1] * n                       # -1 stays for elements nothing ever beats
    stack = []                              # indices; nums[...] decreasing bottom -> top
    for i in range(n):
        while len(stack) > 0 and nums[stack[-1]] < nums[i]:   # strictly smaller tops are answered
            j = stack.pop()
            answer[j] = nums[i]             # nums[i] is the first greater element right of j
        stack.append(i)
    return answer


# --- try it ---
print(next_greater_element([2, 1, 2, 4, 3]))      # -> [4, 2, 4, -1, -1]
print(next_greater_element([1, 3, 2, 4]))         # -> [3, 4, 4, -1]
print(next_greater_element([5, 4, 3]))            # -> [-1, -1, -1]
print(next_greater_element([2, 2, 3]))            # -> [3, 3, -1]
