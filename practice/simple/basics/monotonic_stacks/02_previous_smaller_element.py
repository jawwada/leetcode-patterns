"""
Previous Smaller Element (basics: monotonic_stacks)
For each element, return the nearest element to its left that is strictly smaller, or -1.
  [3, 1, 4, 1, 5]  ->  [-1, -1, 1, -1, 1]

Idea: keep a stack of values increasing bottom to top. Before pushing x, pop every value
      >= x: x is nearer and no bigger, so those values can never answer anyone again.
      Whatever is left on top is the nearest smaller value to the left of x.

Pseudocode:
  ans = [];  stack = []                  # values, increasing bottom -> top
  for x in nums:
      while stack is not empty and top >= x: pop
      ans.append(top if stack is not empty else -1)
      push x
  return ans

Time O(n), space O(n).
"""


def previous_smaller_element(nums):
    ans = []
    stack = []                           # values, increasing bottom -> top
    for x in nums:
        while stack and stack[-1] >= x:  # >= : an equal value is not smaller
            stack.pop()
        ans.append(stack[-1] if stack else -1)   # top survivor = nearest smaller
        stack.append(x)
    return ans


if __name__ == "__main__":
    print(previous_smaller_element([3, 1, 4, 1, 5]))  # [-1, -1, 1, -1, 1]
    print(previous_smaller_element([1, 2, 3]))        # [-1, 1, 2]
    print(previous_smaller_element([2, 2]))           # [-1, -1]
