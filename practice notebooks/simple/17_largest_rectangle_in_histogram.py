"""
Largest Rectangle in Histogram (LeetCode 84)
Return the area of the largest rectangle that fits under the bars.
  [2, 1, 5, 6, 2, 3]  ->  10   (height 5 across bars 5 and 6)

Idea: keep a stack of bars with increasing heights. When a shorter bar arrives,
      each taller bar popped has found its right edge; its left edge is the new top.

Pseudocode:
  stack = []; append a 0 bar to flush everything at the end
  for i, h in heights + [0]:
      while stack and heights[stack top] >= h:
          height = heights[pop]
          left = stack top + 1 (or 0 if empty)
          best = max(best, height * (i - left))
      push i

Time O(n), space O(n).
"""


def largest_rectangle_area(heights):
    bars = heights + [0]                 # sentinel flushes the stack
    stack = []                           # indices, heights increasing
    best = 0
    for i, h in enumerate(bars):
        while stack and bars[stack[-1]] >= h:   # bar on top can't extend right
            height = bars[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best


if __name__ == "__main__":
    print(largest_rectangle_area([2, 1, 5, 6, 2, 3]))  # 10
    print(largest_rectangle_area([2, 4]))              # 4
    print(largest_rectangle_area([3, 3, 3]))           # 9
