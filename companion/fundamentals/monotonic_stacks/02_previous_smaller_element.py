"""
Previous Smaller Element - Fundamentals
Chapter: fundamentals/monotonic_stacks
Key operations: pop while top >= current, answer is the survivor under the current, push current

For each element return the nearest element to its LEFT that is strictly smaller, or -1. The stack
holds values strictly increasing bottom to top; after popping everything >= the current value, the
top is the current element's answer.
Example: [3, 1, 4, 1, 5] -> [-1, -1, 1, -1, 1]
"""


# --- algorithm ---
def previous_smaller_element(nums):
    """Stack of values increasing bottom to top; the survivor under x is x's answer. O(n)."""
    n = len(nums)
    answer = [-1] * n
    stack = []                              # values; increasing bottom -> top
    for i in range(n):
        while len(stack) > 0 and stack[-1] >= nums[i]:   # >= : equal values are not "smaller"
            stack.pop()                     # a popped value can never be anyone's answer later
        if len(stack) > 0:
            answer[i] = stack[-1]           # the nearest smaller value to the left survived
        stack.append(nums[i])
    return answer


# --- try it ---
print(previous_smaller_element([3, 1, 4, 1, 5]))      # -> [-1, -1, 1, -1, 1]
print(previous_smaller_element([1, 2, 3]))            # -> [-1, 1, 2]
print(previous_smaller_element([3, 2, 1]))            # -> [-1, -1, -1]
print(previous_smaller_element([2, 2, 1, 3]))         # -> [-1, -1, -1, 1]
