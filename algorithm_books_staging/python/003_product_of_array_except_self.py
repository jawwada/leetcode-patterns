"""
Product of Array Except Self - Prefix and Suffix Products

Given an integer array, return an array whose entry i is the product of every
element except nums[i], without using division:
[1, 2, 3, 4] -> [24, 12, 8, 6].
"""


# --- algorithm ---
def product_except_self(nums):
    """answer[i] = product left of i times product right of i, one pass each
    way. O(n) time, O(1) extra space besides the output."""
    n = len(nums)
    answer = [1] * n
    prefix = 1                      # product of nums[0..i-1]
    for i in range(n):
        answer[i] = prefix          # everything left of i
        prefix *= nums[i]           # only now let nums[i] in
    suffix = 1                      # product of nums[i+1..n-1]
    for i in range(n - 1, -1, -1):  # right to left
        answer[i] *= suffix         # times everything right of i
        suffix *= nums[i]
    return answer


# --- try it ---
print(product_except_self([1, 2, 3, 4]))        # -> [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))   # -> [0, 0, 9, 0, 0]
print(product_except_self([0, 0, 2]))           # -> [0, 0, 0]
print(product_except_self([2, -3, 4]))          # -> [-12, 8, -6]
