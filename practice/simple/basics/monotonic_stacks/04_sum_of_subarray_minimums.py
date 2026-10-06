"""
Sum of Subarray Minimums (basics: monotonic_stacks)
Return the sum of min(b) over every contiguous subarray b, modulo 10^9 + 7.
  [3, 1, 2, 4]  ->  17   (3 + 1 + 2 + 4 + 1 + 1 + 2 + 1 + 1 + 1)

Idea: element j is the minimum of (j - left) * (right - j) subarrays, where left is its previous
      strictly smaller index and right its next smaller-or-equal index. An increasing stack
      knows both when j is popped: left is the index under j, right is the current i.

Pseudocode:
  stack = [];  total = 0                 # indices, values increasing bottom -> top
  for i in 0..n:                         # i == n is a sentinel that pops everything
      while stack is not empty and (i == n or nums[top] >= nums[i]):
          j = pop
          left = new top, or -1 if the stack is empty
          total += nums[j] * (j - left) * (i - j)
      if i < n: push i
  return total % (10^9 + 7)

Time O(n), space O(n).
"""


def sum_of_subarray_minimums(nums):
    n = len(nums)
    stack = []                           # indices, values increasing bottom -> top
    total = 0
    for i in range(n + 1):               # i == n: sentinel that pops everything
        while stack and (i == n or nums[stack[-1]] >= nums[i]):   # >= : ties counted once
            j = stack.pop()              # nums[i] ends j's reach on the right
            left = stack[-1] if stack else -1        # previous strictly smaller
            total += nums[j] * (j - left) * (i - j)  # j is the min of that many subarrays
        if i < n:
            stack.append(i)
    return total % (10**9 + 7)


if __name__ == "__main__":
    print(sum_of_subarray_minimums([3, 1, 2, 4]))         # 17
    print(sum_of_subarray_minimums([11, 81, 94, 43, 3]))  # 444
    print(sum_of_subarray_minimums([2, 2]))               # 6
