---
rank: 1
slug: two_sum
---

Given an array of integers and a target, return the indices of the two numbers that add up to the target; exactly one such pair exists. In `[2, 7, 11, 15]` with target `9` the answer is `[0, 1]`, because `2 + 7 = 9`.

The brute force tries every pair, `n(n - 1) / 2` of them, for `O(n²)` time. Its waste is that every number keeps asking the same question, "did my partner appear earlier?", and answers it by rescanning the past. A hash map answers that question in `O(1)`. Walk the array once; at index `i` the partner the current number needs is `target - nums[i]`. If that value is already a key in the map, the pair is complete. If not, store the current number with its index and move on, so that a later number can find it.

Picture the map as the memory of everything to the left of the pointer. Each number looks backward exactly once, through the map, instead of across the whole prefix. Checking before storing is what stops a number from pairing with itself when the target is twice its value.

```text
target = 9
  i   nums[i]   need = 9 - nums[i]   need in seen?   seen after the step
  0      2              7                 no          {2: 0}
  1      7              2              yes → 0        stop: answer [0, 1]
```

```pseudo
FUNCTION TwoSum(nums, target)
    seen ← empty map                       // value → index
    FOR i FROM 0 TO len(nums) - 1
        need ← target - nums[i]
        IF need IN seen                    // partner appeared earlier
            RETURN [seen[need], i]
        seen[nums[i]] ← i                  // store only after checking
    RETURN empty list
```

One pass with constant-time lookups gives `O(n)` time, and the map costs `O(n)` space. Reach for this pattern whenever a problem asks for a pair with a fixed sum, difference or other exact relationship and the input is unsorted: the map turns "search the past" into a single lookup. When the array is sorted, two pointers closing in from both ends do the same job in `O(1)` space; that loop is the heart of 3Sum (#7). The classic mistake is storing `nums[i]` before the lookup, which pairs `3` with itself for target `6` in `[3, 2, 4]` and returns `[0, 0]`.

*Practice:* LC 1 Two Sum · LC 167 Two Sum II - Input Array Is Sorted · LC 454 4Sum II · LC 15 3Sum
