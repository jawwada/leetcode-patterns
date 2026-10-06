"""
Subarray Sum Equals K (LeetCode 560)
Count the contiguous subarrays whose sum is exactly k (numbers may be negative).
  nums = [1, 2, 3], k = 3  ->  2   ([1, 2] and [3])

Idea: sum(i..j) = prefix[j] - prefix[i-1]. So a subarray ending here sums to k
      exactly when some earlier prefix equals (prefix - k). Count earlier prefixes in a dict.

Pseudocode:
  counts = {0: 1}                 # empty prefix seen once
  prefix = 0
  for num in nums:
      prefix += num
      answer += counts[prefix - k]
      counts[prefix] += 1

Time O(n), space O(n).
"""


def subarray_sum(nums, k):
    counts = {0: 1}                      # prefix sum -> how many times seen
    prefix = 0
    answer = 0
    for num in nums:
        prefix += num
        answer += counts.get(prefix - k, 0)        # earlier prefixes that leave k
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer


if __name__ == "__main__":
    print(subarray_sum([1, 2, 3], 3))    # 2
    print(subarray_sum([1, 1, 1], 2))    # 2
    print(subarray_sum([1, -1, 0], 0))   # 3
