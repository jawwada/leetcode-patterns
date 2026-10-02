"""
Top K Frequent Elements (LeetCode 347)  — Medium
Pattern: Frequency count + bucket sort

Problem
-------
Given an integer array nums and an integer k, return the k most frequent elements
(any order). The answer is guaranteed unique.
Example: nums = [1,1,1,2,2,3], k = 2 -> [1, 2].

Brute force
-----------
Count frequencies with a dict, then sort the distinct values by count descending and
take the first k. O(n log n) time, O(n) space. The wasted work is the full sort: we
only need the top k, yet sorting fully orders ALL distinct values, including the
ones we will discard.

From brute force to optimal
---------------------------
Sorting is overkill because the sort keys (frequencies) live in a tiny known range:
a frequency is an integer between 1 and n. Whenever keys are small bounded integers
you can bucket instead of compare-sort. Make an array of n + 1 buckets where
bucket[f] holds every value that occurs exactly f times. Then walk the buckets from
the highest frequency downward, collecting values until you have k. That is O(n)
with no comparisons. (A size-k min-heap is the O(n log k) middle ground and worth
mentioning.)

Intuition
---------
Frequencies are counting numbers bounded by n, so they can be used directly as
array indices. Placing each value at the index equal to its frequency sorts the
values by frequency for free; reading the array backwards yields the most frequent
first.

Geometric view
--------------
Picture a row of n + 1 shelves labelled 0..n. Each distinct value is placed on the
shelf whose label equals its count. The algorithm then sweeps the shelves from the
right end (highest counts) leftwards, sweeping values into the answer until k are
collected.

Steps
-----
1. Count occurrences with Counter.
2. Create buckets = [[] for _ in range(len(nums) + 1)].
3. For each (value, freq), append value to buckets[freq].
4. Iterate freq from len(nums) down to 1, extending the answer with that bucket.
5. Stop and return once the answer has k values.

Complexity: O(n) time, O(n) space — counting is one pass, bucketing is one pass over
distinct values, the backward sweep touches each bucket once.
Pitfalls: buckets must be size n + 1 (an element can appear n times); slicing the
answer to exactly k when a bucket pushes you past k; sorting the whole Counter when
the interviewer asks for better than O(n log n).
"""
from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
        for value, count in freq.items():
            buckets[count].append(value)
        result: List[int] = []
        for count in range(len(nums), 0, -1):  # highest frequency first
            for value in buckets[count]:
                result.append(value)
                if len(result) == k:
                    return result
        return result


def brute_force(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    ordered = sorted(freq, key=lambda v: freq[v], reverse=True)
    return ordered[:k]


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert s.topKFrequent([1], 1) == [1]
    assert sorted(s.topKFrequent([4, 4, 4, 5, 5, 6, 6, 6, 6], 2)) == [4, 6]
    assert sorted(s.topKFrequent([7, 7, 7, 7], 1)) == [7]
    for nums, k in [([1, 1, 1, 2, 2, 3], 2), ([1], 1), ([4, 4, 4, 5, 5, 6, 6, 6, 6], 2), ([7, 7, 7, 7], 1)]:
        assert sorted(s.topKFrequent(nums, k)) == sorted(brute_force(nums, k))
    print("ok")
