"""
Product of Array Except Self (LeetCode 238)
For each index, return the product of every other number (no division).
  [1, 2, 3, 4]  ->  [24, 12, 8, 6]

Idea: answer[i] = (product of everything left of i) * (product of everything right of i).
      One sweep left-to-right writes the left products, one sweep back multiplies in the right ones.

Pseudocode:
  answer = [1] * n
  prefix = 1
  for i left to right:  answer[i] = prefix;  prefix *= nums[i]
  suffix = 1
  for i right to left:  answer[i] *= suffix; suffix *= nums[i]

Time O(n), space O(1) extra (besides the output).
"""


def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    prefix = 1                           # product of nums[0..i-1]
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1                           # product of nums[i+1..n-1]
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer


if __name__ == "__main__":
    print(product_except_self([1, 2, 3, 4]))        # [24, 12, 8, 6]
    print(product_except_self([-1, 1, 0, -3, 3]))   # [0, 0, 9, 0, 0]
