---
rank: 30
slug: subsets
---

Given an array of distinct integers, return all of its subsets, the power set, each exactly once and in any order. For `[1, 2, 3]` there are `2^3 = 8` of them: `[]`, `[1]`, `[1, 2]`, `[1, 2, 3]`, `[1, 3]`, `[2]`, `[2, 3]` and `[3]`.

Each element faces one yes-or-no decision, so there are `2^n` subsets, and any method that lists them pays at least that much. Backtracking grows them as a tree. The root is the empty subset, and each child appends one more element, always one that lies to the right of everything its parent holds. That rule is what makes every subset appear exactly once, in index order: `[1, 2]` is built, `[2, 1]` never is. The recursion carries the rule as a `start` index. At a node the loop tries each `i` from `start` on: append `nums[i]` (choose), recurse with `start = i + 1`, then pop it again (un-choose), so the next sibling begins from the same path its parent had.

Unlike permutations (#31), where only the leaves are answers, every node of this tree is a subset, so a call records its path the moment it begins, before the loop. One shared list, `path`, carries the whole search: it grows on the way down and shrinks on the way up, a stack that always spells the route from the root to the current node.

```text
                       []
         ┌─────────────┼─────────────┐
        [1]           [2]           [3]
     ┌───┴───┐         │
   [1,2]   [1,3]     [2,3]
     │
  [1,2,3]

recorded in preorder: [] [1] [1,2] [1,2,3] [1,3] [2] [2,3] [3]
below [2] the loop starts at index 2, so only 3 may follow: no [2,1]
```

```pseudo
FUNCTION Backtrack(nums, start, path, result)
    result.append(path.copy())             // every node is a subset
    FOR i FROM start TO len(nums) - 1
        path.append(nums[i])               // choose
        Backtrack(nums, i + 1, path, result)   // only later indices below
        path.pop()                         // un-choose

FUNCTION Subsets(nums)
    result ← empty list
    Backtrack(nums, 0, empty list, result)
    RETURN result
```

The tree has `2^n` nodes and copying a path costs up to `O(n)`, so the time is `O(n · 2^n)`; beyond the output, the space is the `O(n)` path and recursion depth. Reach for this template when a problem asks for all subsets or all combinations of a small input (n up to about 20), or when a search has to try every selection. With duplicates in the input (LC 90), sort first and skip `nums[i]` when `i > start` and `nums[i] = nums[i - 1]`: equal values then sit side by side, and on one level only the first of a run may open a branch, which stops `[1, 2, 2]` from producing `[1, 2]` twice. The same `2^n` subsets also come out of a plain loop over bitmasks (#137). The classic mistake is `result.append(path)` without the copy: every entry is then the same list object, and for `[1, 2, 3]` the search ends with eight references to one empty list.

*Practice:* LC 78 Subsets · LC 90 Subsets II · LC 1863 Sum of All Subset XOR Totals
