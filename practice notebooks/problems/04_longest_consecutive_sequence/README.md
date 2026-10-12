# Longest Consecutive Sequence (LeetCode 128)

**Area:** arrays & hashing · **Difficulty:** Medium · **Key operations:** put the values in a set, skip x when x - 1 is present, walk x, x+1, x+2, ... while present

## Problem

Given an unsorted integer array, return the length of the longest run of consecutive integer **values** (positions do not matter). The algorithm must run in O(n) time.

## Example

```
nums   = [100, 4, 200, 1, 3, 2]
answer = 4            the run 1, 2, 3, 4
```

## Brute force

From every element `x`, count upward: is `x + 1` in the array? `x + 2`? Each check is a linear scan of the list.

O(n³) worst case, O(1) space. Two kinds of wasted work: every membership test is a full scan, and a run is re-walked from *every one of its members*: the run 1-2-3-4 is measured from 1, again from 2, from 3 and from 4. Sorting first and scanning gives O(n log n), but the problem demands O(n).

## From brute force to optimal

Fix the two wastes separately.

1. Membership scans: put the values in a set, so `x + 1 in values` is O(1).
2. Re-walking: a run has exactly one natural starting point, the value `x` whose predecessor `x - 1` is **not** in the set. Only walk upward from those. Every value then belongs to exactly one walk (the walk started at its run's minimum), so the total number of steps across all walks is at most n.

The nested loop looks quadratic, but the `x - 1` check makes it amortised linear.

## Intuition

Lay the distinct values out as dots on a number line. Runs are the maximal unbroken stretches of dots. Look at each dot once: if the dot to its left is present, it is in the middle of a stretch and someone else will measure that stretch, so skip it. If the left neighbour is missing, this dot is the left end of a stretch: walk right until the first gap and record the length. Each dot is stepped on by exactly one walk, which is the whole trick.

## Walkthrough

The set iterates in its own order; this is the order the script prints.

```
values on the number line:   1  2  3  4  . . .  100  . . .  200

x=1    0 absent -> run start, walk up:
         2 present   run [1, 2]          length 2
         3 present   run [1, 2, 3]       length 3
         4 present   run [1, 2, 3, 4]    length 4
         5 absent    run ends at 4       length 4, best 4
x=2    1 present -> not a run start, skip
x=3    2 present -> not a run start, skip
x=100  99 absent -> run start, walk up:
         101 absent  run ends at 100     length 1, best 4
x=4    3 present -> not a run start, skip
x=200  199 absent -> run start, walk up:
         201 absent  run ends at 200     length 1, best 4

return 4
```

Three walks in total (from 1, 100 and 200), and the values 2, 3, 4 are each stepped on once, inside the walk from 1.

## Steps

1. `values = set(nums)` (also removes duplicates), `best = 0`.
2. For each `x` in `values`: if `x - 1` is in `values`, skip it.
3. Otherwise `length = 1`; while `x + length` is in `values`, `length += 1`.
4. `best = max(best, length)`.
5. Return `best` (0 for an empty array).

## Complexity

O(n) time: building the set is O(n), and across all walks each value is visited at most once, plus one O(1) skip check per value. O(n) space for the set.

## Pitfalls

- **Testing the wrong neighbour.** `if x + 1 in values` skips everything except the *top* of each run, and a walk up from the top stops at once, so the example returns 1. A run start is a value whose `x - 1` is absent.
- **Forgetting `max`.** `best = length` keeps only the length of whichever run start the set visits last; a long run measured earlier is forgotten.
- **`break` instead of `continue`.** A value that is not a run start only means *this* value is skipped; `break` abandons the loop and any run whose start comes later is never measured.
- **Dropping the `x - 1` check.** Without it every member walks its whole run and the algorithm is O(n²) on one long run, although it still returns the right answer.
- **Iterating the list instead of the set.** Duplicates re-walk the same run; iterating `values` visits each distinct start once.
