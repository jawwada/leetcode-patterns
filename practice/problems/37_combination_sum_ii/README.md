# Combination Sum II (LeetCode 40)

**Area:** backtracking · **Difficulty:** Medium · **Key operations:** sort, break when candidate > remaining, skip a duplicate sibling (i > start), append / recurse from i + 1 / pop

## Problem

Given a list of candidates (values may repeat) and a target, return every unique combination whose sum is `target`. Each index may be used at most once, and two combinations are the same if they hold the same values (so `[1, 7]` built from either copy of the 1 counts once). Return the combinations sorted.

## Example

```
candidates = [10, 1, 2, 7, 6, 1, 5], target = 8
-> [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

There are two 1s, so `[1, 7]` could be formed two ways; it is reported once.

## Brute force

Enumerate every subset of indices with a bitmask from `0` to `2^n - 1`, decode the chosen values, keep the subsets whose sum is `target`, and dedupe by inserting the sorted tuple into a set.

O(n · 2^n) time, O(2^n) space for the set. Two kinds of wasted work: subsets whose running sum is already past the target are still fully decoded and summed, and combinations that differ only in *which* copy of a repeated value they use (the two 1s) are generated separately and only collapsed at the end.

## From brute force to optimal

Both wastes disappear once the candidates are sorted and the subsets are built depth first, one value at a time.

1. **Overshoot.** Values are positive, so when `nums[i] > remaining` every later value is larger too: `break` out of the loop instead of trying them.
2. **Duplicates.** Equal values are now adjacent. At one level of the tree, choosing the second copy of a value produces exactly the subtree already explored for the first copy, so skip a value equal to its left sibling (`i > start and nums[i] == nums[i - 1]`). The comparison is with `start`, not `0`: the second 1 is still allowed as a *child* of the first 1, which is how `[1, 1, 6]` is found.

Recursing from `i + 1` enforces "each index at most once". The DFS now visits only prefixes of distinct, still-feasible combinations.

## Intuition

Picture a tree where each node holds the amount still needed and its children are the remaining candidates in ascending order. Two cuts prune it: a child bigger than the amount needed truncates the whole rest of its row (nothing to the right can fit either), and a child with the same value as its left neighbour is crossed out (its subtree is a copy). What is left of the tree is exactly the set of unique combinations, each reached once.

## Walkthrough

Sorted `nums = [1, 1, 2, 5, 6, 7, 10]`, `target = 8`. Indentation is the depth of the path; `rem` is what is still needed.

```
path []        rem 8   choices 1 1 2 5 6 7 10
  take 1 (i=0)
  path [1]       rem 7   choices 1 2 5 6 7 10
    take 1 (i=1): allowed, it is a child of the first 1, not a sibling
    path [1,1]     rem 6   choices 2 5 6 7 10
      path [1,1,2] rem 4   5 > 4 -> break
      path [1,1,5] rem 1   6 > 1 -> break
      path [1,1,6] rem 0   RECORD [1,1,6]
      7 > 6 -> break
    path [1,2]     rem 5   choices 5 6 7 10
      path [1,2,5] rem 0   RECORD [1,2,5]
      6 > 5 -> break
    path [1,5]     rem 2   6 > 2 -> break
    path [1,6]     rem 1   7 > 1 -> break
    path [1,7]     rem 0   RECORD [1,7]
    10 > 7 -> break
  skip i=1: nums[1] = 1 equals its left sibling nums[0]   (would redo the whole subtree above)
  path [2]       rem 6   choices 5 6 7 10
    path [2,5]     rem 1   6 > 1 -> break
    path [2,6]     rem 0   RECORD [2,6]
    7 > 6 -> break
  path [5]       rem 3   6 > 3 -> break
  path [6]       rem 2   7 > 2 -> break
  path [7]       rem 1   10 > 1 -> break
  10 > 8 -> break
result sorted: [[1,1,6], [1,2,5], [1,7], [2,6]]
```

Every `break` throws away all the larger candidates at once; the single `skip` at the root removes a duplicate of the biggest subtree in the search.

## Steps

1. `nums = sorted(candidates)`, `result = []`, `path = []`.
2. `dfs(start, remaining)`: if `remaining == 0`, record a copy of `path` and return.
3. For `i` from `start` to the end: if `nums[i] > remaining`, `break`.
4. If `i > start` and `nums[i] == nums[i - 1]`, `continue`.
5. Append `nums[i]`, call `dfs(i + 1, remaining - nums[i])`, pop.
6. Call `dfs(0, target)`; return `sorted(result)`.

## Complexity

O(2^n) time in the worst case (each index in or out), with the two prunings removing most of it in practice. O(n) extra space for the path and recursion, beyond the output.

## Pitfalls

- **Recursing from `i` instead of `i + 1`.** The same index can then be reused: `[2, 2]` with target 6 yields `[2, 2, 2]`. Use `i + 1` here, `i` only in Combination Sum I where reuse is allowed.
- **`i > 0` instead of `i > start` in the skip rule.** This also skips the second 1 when it is a *child* of the first 1, losing `[1, 1, 6]`. The rule is about siblings at the same level.
- **`>=` instead of `>` in the break.** A candidate equal to what is left completes a combination; breaking before taking it loses `[1, 7]` and `[2, 6]`.
- **Forgetting to sort.** Both the break and the skip rule assume adjacent duplicates and ascending order; on unsorted input they are wrong, not just slow.
- **Sorting in place.** `candidates.sort()` mutates the caller's list; `sorted(candidates)` does not.
