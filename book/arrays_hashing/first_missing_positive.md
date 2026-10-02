# First Missing Positive
*LeetCode 41 · Hard · Pattern: Index as hash (in-place cyclic placement) · Reading time ~9 min*

## What the problem is really asking

You get an unsorted array of integers, which may include negatives, zeros, duplicates and huge values. Return the smallest positive integer (1, 2, 3, ...) that does not appear in it. So far that is an easy problem. The catch is the budget: O(n) time and O(1) extra space. No sorting (that is O(n log n)), and no hash set (that is O(n) extra memory).

The answer is a single positive integer. What makes it hard is that the two obvious tools are each forbidden by one half of the budget: sorting fails on time, a set fails on space. You must find a third tool, and the only memory you are allowed to use is the array you were given.

```text
nums = [ 3,  4, -1,  1 ]

positives present:  1 . 3 4
                    ^ ^ ^ ^
candidates:         1 2 3 4 5 ...
                      ^
                      first gap -> answer 2
```

## Do it by hand first

On paper you would not sort. You would draw a row of boxes labelled 1, 2, 3, 4, walk through the array, and tick the box for each value you see. Values like -1 or 99 have no box, so you ignore them. Then you read the boxes left to right, and the first empty box is the answer.

```text
read 3  -> tick box 3      boxes:  1  2  3  4
read 4  -> tick box 4             [ ][ ][x][ ]
read -1 -> no box, ignore         [ ][ ][x][x]
read 1  -> tick box 1             [x][ ][x][x]
                                      ^ first empty box: 2
```

Why only four boxes? Because there are four numbers. Four numbers can fill at most four boxes, so somewhere among 1..5 there must be a gap. Your hand kept track of a row of n boxes indexed by value. That row is the seed of the data structure, and the whole problem is: where do you keep n boxes when you are allowed no extra memory?

## The first honest attempt

Try candidate 1: scan the whole array for it. Found? Try 2: scan the whole array again. Keep going until a scan fails. That is O(n^2) time and O(1) space.

```text
candidate 1:  [ 3,  4, -1,  1 ]   scan ->>>>>>>>>> found at 3
candidate 2:  [ 3,  4, -1,  1 ]   scan ->>>>>>>>>> not found
                                  answer 2
worst case [1,2,...,n]: n+1 full scans = O(n^2)
```

The waste is the membership test. Each candidate rereads the whole array from scratch, because nothing remembers what earlier scans saw. A hash set built once fixes the time to O(n) but costs O(n) memory, which is exactly the forbidden part. We want the set without paying for it.

## The turning point

**Claim: the answer is always in 1..n+1, so only values 1..n matter, and the array's own n slots can serve as the boxes: value v is "ticked" by placing it at index v - 1.**

First, the bound. With n numbers, if every value 1..n is present then the array is a permutation of 1..n and the answer is n + 1. Otherwise some value in 1..n is missing and the answer is at most n. Either way the answer is in 1..n+1. Values that are zero, negative, or larger than n can never be the answer and can never prevent a smaller answer, so they are noise.

Second, the storage. We need n boxes for the values 1..n, and the array has exactly n slots. Give each value a home: value v lives at index v - 1. If we can rearrange the array so that every in-range value sits at its home, then the scan "first index i where `nums[i] != i + 1`" finds the first missing value. The array is its own hash set, with the hash function `v -> v - 1`.

How do we rearrange in place? Walk `i` from left to right. While the value at `i` is in range and not yet home, swap it into its home. The value that was sitting at that home gets kicked back to `i`, and it might belong somewhere too, so we keep going (a `while`, not an `if`). It is like parking bays: each car numbered 1..n drives to its bay, evicting whoever is there, who then drives to *their* bay, and so on until the car standing at `i` has no bay (out of range) or its bay already holds its twin (a duplicate).

That last condition is the duplicate guard. With `[1, 1]`, the second 1 wants to go to index 0, which already holds a 1. Swapping would exchange two identical values forever. So the loop condition is:

```python
while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
    home = nums[i] - 1
    nums[i], nums[home] = nums[home], nums[i]
```

Why is this linear even with a `while` inside a `for`? Each swap puts one value into its home slot for good, and a value at home is never moved again (the guard refuses to swap a value onto a slot that already holds an equal value, and a slot holding its own value is exactly that case). There are only n homes, so there are at most n swaps in the whole run, no matter how they are distributed across `i`.

## Watch it work

`nums = [3, 4, -1, 1]`, n = 4. Homes: value v belongs at index v - 1.

```text
Frame 1   idx:   0   1   2   3
          nums: [3,  4, -1,  1]
                 ^i  3 wants idx 2 (holds -1) -> swap
          nums: [-1, 4,  3,  1]
```
3 goes home; -1 is kicked back to index 0.

```text
Frame 2   idx:   0   1   2   3
          nums: [-1, 4,  3,  1]
                 ^i  -1 out of range -> stop at i=0
                     ^i  4 wants idx 3 (holds 1) -> swap
          nums: [-1, 1,  3,  4]
```
Nothing to do for -1. At i = 1, 4 goes home and 1 is kicked back to index 1.

```text
Frame 3   idx:   0   1   2   3
          nums: [-1, 1,  3,  4]
                     ^i  1 wants idx 0 (holds -1) -> swap
          nums: [ 1, -1, 3,  4]
```
Still at i = 1, the evicted 1 now goes home; -1 lands at index 1.

```text
Frame 4   idx:   0   1   2   3
          nums: [ 1, -1, 3,  4]
                     ^i  -1 out of range -> stop
                         ^i  3 already home
                             ^i  4 already home
```
Placement is finished after three swaps in total.

```text
Frame 5   idx:   0   1   2   3
          want:  1   2   3   4
          nums: [1, -1,  3,  4]
                 ok  X
          first mismatch at idx 1  ->  answer 1 + 1 = 2
```
The second pass finds the first slot that does not hold its own number.

Across the frames, once a value reached its home (3 in Frame 1, 4 in Frame 2, 1 in Frame 3) it never moved again. The values left stranded are exactly the noise: here the -1.

## Why it is correct

There are two claims to check.

**After the first pass, every value v in 1..n that occurs in the array sits at index v - 1.** Swaps only rearrange, so the multiset of values never changes. A value at its home is never moved again, as argued above. When the `while` loop at index `i` stops, the value at `i` is either out of range, or a value whose home already holds an equal value, or already at home itself. Later iterations only write into slot `i` if `i` is the home of the value being placed, in which case slot `i` becomes correct. So when the loop ends, every slot either holds its own value, or holds noise or a duplicate whose twin is home. Hence any in-range value that occurs has a copy at its home.

**The second pass returns the smallest missing positive.** Scanning `i = 0, 1, ...`, every slot before the first mismatch holds `i + 1`, so 1..i are all present. At the first mismatch, `i + 1` is absent, because if it were present it would be at its home, which is this very slot. If there is no mismatch, 1..n are all present, and since the answer lies in 1..n+1, it is n + 1.

## Cost

- **Time O(n):** the outer loop is n steps, the total number of swaps across all `while` loops is at most n because each one homes a value permanently, and the second pass is n steps.
- **Space O(1) extra:** only a few indices; the array itself is the table.

The brute force is O(n^2) time, O(1) space; the hash-set version is O(n) time and O(n) space. This solution takes the best of each, at the price of mutating the input.

## Variations you will meet

- **Sign marking instead of swapping.** First replace every value outside 1..n with n + 1. Then for each `|v|` in 1..n, make `nums[|v| - 1]` negative. The first index still positive is the answer. Same O(n)/O(1), no swaps, but the "tick" is the sign bit rather than the slot's content.
- **Find All Numbers Disappeared in an Array (448) and Set Mismatch (645).** Same cyclic placement, but the second pass collects *every* mismatch, and in 645 the value sitting in the wrong slot is the duplicate.
- **Find the Duplicate Number (287).** Values are in 1..n with n + 1 slots and you may not modify the array, so swapping is out; the "value as pointer" view turns it into cycle detection on a linked list.
- **Do not mutate the input.** If the interviewer forbids it, you cannot meet O(1) space; say so and fall back to a hash set. Ask before you swap.

## What to carry forward

When the answer is trapped in 1..n, the array is its own hash table: send each value to index v - 1 and read off the first slot that is wrong. The next problem, Maximum Gap, uses the same pigeonhole counting (n values, a bounded range, so something is forced) but builds buckets over value *ranges* instead of single values.
