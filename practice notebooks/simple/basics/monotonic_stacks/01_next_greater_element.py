"""
Next Greater Element (basics: monotonic_stacks)
For each element, return the first element to its right that is strictly greater, or -1.
  [2, 1, 2, 4, 3]  ->  [4, 2, 4, -1, -1]

Idea: keep a stack of indices still waiting for a bigger value (values decrease bottom to top).
      A new value x answers every smaller value on top of the stack, then waits itself.

Pseudocode:
  ans = [-1] * n;  stack = []            # indices still waiting
  for i, x in nums:
      while stack is not empty and nums[top] < x:
          j = pop;  ans[j] = x           # x is j's next greater
      push i
  return ans

Time O(n) (each index is pushed and popped at most once), space O(n).
"""


def next_greater_element(nums):
    ans = [-1] * len(nums)
    stack = []                           # indices still waiting
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:   # x beats the top
            j = stack.pop()
            ans[j] = x                   # x is j's next greater
        stack.append(i)                  # i waits for its own answer
    return ans


if __name__ == "__main__":
    print(next_greater_element([2, 1, 2, 4, 3]))  # [4, 2, 4, -1, -1]
    print(next_greater_element([1, 2, 3]))        # [2, 3, -1]
    print(next_greater_element([3, 3, 1]))        # [-1, -1, -1]
