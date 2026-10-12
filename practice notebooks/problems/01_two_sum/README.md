# Two Sum (LeetCode 1)

**Area:** arrays & hashing · **Difficulty:** Medium · **Key operations:** compute the complement, look it up in a dict, insert after the check, return indices

## Problem

Given an unsorted array of integers `nums` and an integer `target`, return the **indices** of the two numbers that add up to `target`. Exactly one answer exists, and the same element may not be used twice.

## Example

```
nums   = [3, 5, 2, 7, 11]   target = 9
answer = [2, 3]             because nums[2] + nums[3] = 2 + 7 = 9
```

## Brute force

For every index `i`, scan every `j > i` and test `nums[i] + nums[j] == target`.

O(n²) time, O(1) space. The wasted work: once `nums[i]` is fixed we already know the *one* value we are looking for, `target - nums[i]`, yet we re-read the whole suffix to find out whether it is there and where.

## From brute force to optimal

The inner loop answers a membership question: "is `target - nums[i]` in the array, and at which index?" Membership plus lookup-by-value is exactly what a dict does in O(1), so replace the scan with a dict from value to index.

To respect "no reuse" and to stay in one pass, fill the dict lazily: *before* inserting `nums[i]`, ask whether its complement is already present. Any valid pair `(i, j)` with `i < j` is discovered when the cursor reaches `j`, because `nums[i]` was inserted earlier. One pass, one dict probe and one insert per element.

## Intuition

Each number has exactly one partner that would complete the sum. Walk left to right carrying a bag of everything already seen, keyed by value. At each step ask the bag one question (is my partner in there?) and then drop yourself in. A pair is found by whichever of its members comes second, so one pass is enough, and because you ask before you drop yourself in, a number can never be paired with itself.

## Walkthrough

`seen` maps value to index. Each row shows the dict *before* the current element is inserted.

```
nums   3   5   2   7  11     target 9

i=0  v=3   need 9-3 = 6   seen {}                  6 absent  -> seen[3] = 0
i=1  v=5   need 9-5 = 4   seen {3:0}               4 absent  -> seen[5] = 1
i=2  v=2   need 9-2 = 7   seen {3:0, 5:1}          7 absent  -> seen[2] = 2
i=3  v=7   need 9-7 = 2   seen {3:0, 5:1, 2:2}     2 present at index 2 -> return [2, 3]
```

Index 4 (11) is never looked at: the answer is returned as soon as the second member of the pair arrives.

## Steps

1. `seen = {}` (value -> index).
2. For each index `i` with value `v`: compute `need = target - v`.
3. If `need` is in `seen`, return `[seen[need], i]`.
4. Otherwise store `seen[v] = i` and continue.
5. Return `[]` if the loop ends (the problem guarantees it will not).

## Complexity

O(n) time: one dict lookup and one insert per element. O(n) space for the dict.

## Pitfalls

- **Wrong complement.** `need = v - target` asks for the wrong partner; on the example it pairs 11 with the earlier 2 and returns `[2, 4]`, whose sum is 13. The complement is `target - v`.
- **Returning values instead of indices.** `[need, v]` gives `[2, 7]` for the example instead of `[2, 3]`. The problem asks for positions.
- **Swapped key and value.** `seen[i] = v` makes `need in seen` test indices instead of numbers; `[2, 7, 11, 15]` with target 9 never finds the 2 and returns `[]`.
- **Inserting before checking.** If `seen[v] = i` runs before the lookup, an element pairs with itself: `[3, 2, 4]` with target 6 returns `[0, 0]` instead of `[1, 2]`.
- **Assuming the array is sorted.** Two pointers need a sorted array; this one is not, and sorting would scramble the indices you must return.
