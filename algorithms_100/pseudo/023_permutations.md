---
rank: 23
slug: permutations
---

Given an array of distinct integers, return every ordering of its elements, in any order. `[1, 2, 3]` has `3! = 6` permutations: `[1, 2, 3]`, `[1, 3, 2]`, `[2, 1, 3]`, `[2, 3, 1]`, `[3, 1, 2]` and `[3, 2, 1]`.

A permutation fills n slots from left to right: n choices for the first slot, `n - 1` for the second, down to one for the last. Backtracking walks exactly that decision tree. The `path` holds the slots filled so far, and a `used` array of booleans remembers which indices already sit in it, so every level loops over all the indices from 0 again and skips only the used ones. That is the difference from subsets (#22): there is no start index, because order matters here and `2` may come before `1`, as long as it has not been placed already. Each choice is undone in reverse, pop the value and then clear its flag, so the next sibling sees exactly the state its parent saw.

Only a full path is an answer. The tree is a fan that narrows by one at every level, n branches at the root and `n - 1` under each child, and its `n!` leaves are the permutations, each recorded as a copy when the length of the path reaches n.

```text
                          []                             3 choices
         ┌─────────────────┼─────────────────┐
        [1]               [2]               [3]          2 choices each
     ┌───┴───┐         ┌───┴───┐         ┌───┴───┐
   [1,2]   [1,3]     [2,1]   [2,3]     [3,1]   [3,2]     1 choice each
     │       │         │       │         │       │
  [1,2,3] [1,3,2]   [2,1,3] [2,3,1]   [3,1,2] [3,2,1]    6 leaves = 3 × 2 × 1

at [2,1] used = [T, T, F]: the loop skips indices 0 and 1 and appends 3
```

```pseudo
FUNCTION Backtrack(nums, used, path, result)
    IF len(path) = len(nums)
        result.append(path.copy())          // every slot is filled
        RETURN
    FOR i FROM 0 TO len(nums) - 1
        IF used[i]
            CONTINUE                        // already in the path
        used[i] ← true                      // choose
        path.append(nums[i])
        Backtrack(nums, used, path, result)
        path.pop()                          // un-choose, in reverse order
        used[i] ← false

FUNCTION Permutations(nums)
    used ← array of len(nums) copies of false
    result ← empty list
    Backtrack(nums, used, empty list, result)
    RETURN result
```

There are `n!` leaves and fewer than `e · n!` nodes in all, and each node scans at most n flags, so the time is `O(n · n!)`; the space beyond the output is `O(n)` for the path, the flags and the recursion. Reach for it when a problem wants every ordering or arrangement, which is only feasible for small n: `8!` is 40,320, while `12!` is already about 479 million. With duplicates in the input (LC 47), sort first and also skip `i` when `nums[i] = nums[i - 1]` and `used[i - 1]` is false: equal values must then enter the path from left to right, so each distinct ordering is built once. When only the next ordering in lexicographic order is needed (LC 31), it can be found in place in `O(n)` without any tree. The classic mistake is forgetting `used[i] ← false` on the way back: the flags stay set after the first leaf, and `[1, 2, 3]` returns only `[[1, 2, 3]]`.

*Practice:* LC 46 Permutations · LC 47 Permutations II · LC 31 Next Permutation
