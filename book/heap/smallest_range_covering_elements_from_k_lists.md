# Smallest Range Covering Elements from K Lists

*LeetCode 632 · Hard · Pattern: K-way merge with a min-heap of list pointers (track the running max) · Reading time ~10 min*

## What the problem is really asking

You get `k` sorted lists of integers. Find the narrowest interval `[a, b]` on the number line that contains at least one number from every list. If two intervals have the same width `b - a`, the one with the smaller `a` wins.

The answer is a pair of numbers, and you can show that both ends can be taken from the input values. If an optimal interval had an end that was not an input value, you could pull that end inward to the nearest chosen value without losing coverage. So the search space is "pick one element from each list", and the interval for a pick is `[min of the picks, max of the picks]`. The hard part is that the number of picks is the product of the list lengths.

```text
L0:  1  5  8
L1:  4  12
L2:  7  8  10

on a number line:
       1  2  3  4  5  6  7  8  9 10 11 12
L0:    o           o        o
L1:             o                       o
L2:                      o  o     o
                |--------|
best: [4, 7]  -> 4 from L1, 5 from L0, 7 from L2
       width 3
```

## Do it by hand first

Put one finger on each list, at the first element. The three fingers sit on 1, 4 and 7. The span from the lowest finger to the highest is `[1, 7]`, which covers every list, because every list has a finger inside it. Width 6.

How do you make it narrower? Moving the highest finger right only widens the span. Moving a middle finger right does nothing to either end, or pushes the top up. The only move that can shrink the span is to raise the bottom, and the only way to raise the bottom is to move the finger that is on the bottom. So you move the finger on 1 to the next element of its list, 5. Now the fingers read 5, 4, 7, giving `[4, 7]`, width 3. Better.

```text
fingers:  L0@1  L1@4  L2@7    span [1,7]  w=6
move the lowest (L0) ->
fingers:  L0@5  L1@4  L2@7    span [4,7]  w=3
move the lowest (L1) ->
fingers:  L0@5  L1@12 L2@7    span [5,12] w=7
```

Your hand tracked two things: which finger is lowest, which is a minimum over `k` changing values, and how high the highest finger is. The second one is easier than it looks, because fingers only ever move right, so the highest value never drops.

## The first honest attempt

Every valid interval starts and ends at input values. So try every pair `(lo, hi)` of distinct values with `lo <= hi`, and for each pair check whether every list has an element in `[lo, hi]`. With `N` total elements, that is O(N^2) pairs, each with an O(N) check, so O(N^3).

A smarter brute force fixes `lo` and notices that `hi` is forced. For each list, take its first element `>= lo`. The interval must reach the largest of those. That makes it O(N) per `lo`, or O(N^2) total, or O(N k) with binary search.

Now look at what changes as `lo` steps through the values in sorted order:

```text
lo = 1:  first >= lo in each list:  L0:1  L1:4  L2:7
lo = 4:                             L0:5  L1:4  L2:7
lo = 5:                             L0:5  L1:12 L2:7
lo = 7:                             L0:8  L1:12 L2:7
            only ONE column changes per step,
            yet the brute force recomputes all k
```

Each step changes exactly one list's pointer, the list that owned the previous `lo`, yet the brute force recomputes all `k`.

## The turning point

**Claim: if the current picks have minimum `m` from list `i`, then every interval that uses list `i`'s element `m` and is narrower than the current one has already been seen, so you can advance list `i` and never look back.**

Why: you got to this state by advancing pointers in increasing order of value, so the other lists' pointers sit at their first elements that are at or above some earlier minimum. For an interval to use `m` as its list-`i` representative with a smaller right end, some other list would need an element in `[m, current max)` that is lower than its current pointer. But each pointer is already at the smallest element not yet passed over, and anything to its left is below an earlier minimum and so below `m`. So the current interval is the best one that keeps `m`. Discard `m` by advancing list `i`.

That gives a k-way merge with one extra variable:

- A **min-heap** of `(value, list, index)`, one entry per list: the current pointers. The root is the low end of the current interval.
- A plain integer **`cur_max`**, the largest value among the current pointers. It is updated only on push, by `max(cur_max, pushed)`. It never decreases, because pointers only move right and the old maximum is still in the heap unless it was the minimum (which only happens when all pointers are equal).

Each step: pop the root `(val, i, j)`, and score `[val, cur_max]` (replace the best only on strictly smaller width, so earlier starts win ties). If list `i` has no next element, stop. Otherwise push its next element and update `cur_max`.

Why stop when one list runs out? Every future interval would need a representative from list `i`, and all of list `i`'s elements are now behind the pointer. Any interval using one of them was already scored.

## Watch it work

Lists `L0 = 1 5 8`, `L1 = 4 12`, `L2 = 7 8 10`. Heap entries are drawn as `value/list`. The number line shows the current pointers as `^` and the window as `|---|`.

Frame 1: seed with the first element of each list. `cur_max = 7`.

```text
        1/L0
       /    \
    4/L1    7/L2          cur_max = 7
array: [1/L0, 4/L1, 7/L2]

 1  2  3  4  5  6  7  8  9 10 11 12
 ^        ^        ^
 |-----------------|      best = [1,7]  w=6
```

The window spans every list, because every list contributes one pointer.

Frame 2: pop `1/L0`, score `[1, 7]` (width 6, not strictly better than the seeded best). Push `5/L0`; max stays 7.

```text
        4/L1
       /    \
    7/L2    5/L0          cur_max = 7
array: [4/L1, 7/L2, 5/L0]

 1  2  3  4  5  6  7  8  9 10 11 12
          ^  ^     ^
          |--------|      next window [4,7]
```

L0's pointer moved from 1 to 5, and the left edge jumped to the new minimum, 4.

Frame 3: pop `4/L1`, score `[4, 7]`: width 3 < 6, **new best**. Push `12/L1`; `cur_max` becomes 12.

```text
        5/L0
       /    \
    7/L2   12/L1          cur_max = 12
array: [5/L0, 7/L2, 12/L1]

 1  2  3  4  5  6  7  8  9 10 11 12
             ^     ^              ^
             |--------------------|   next window [5,12]
best = [4,7]  w=3
```

Moving L1 cost a lot: its next element is 12, so the right edge jumped.

Frame 4: pop `5/L0`, score `[5, 12]` (width 7, no). Push `8/L0`.

```text
        7/L2
       /    \
   12/L1    8/L0          cur_max = 12
array: [7/L2, 12/L1, 8/L0]
window next: [7, 12]
```

Frame 5: pop `7/L2`, score `[7, 12]` (width 5, no). Push `8/L2`.

```text
        8/L0
       /    \
   12/L1    8/L2          cur_max = 12
array: [8/L0, 12/L1, 8/L2]
window next: [8, 12]
```

The two 8s tie on value and the list index puts `8/L0` at the root.

Frame 6: pop `8/L0`, score `[8, 12]` (width 4, no). L0 has no element after 8, so stop.

```text
L0: 1  5  8  |end      no future window can cover L0
answer: [4, 7]
```

In every frame the heap held exactly one pointer per list. The root was the window's left edge, `cur_max` was its right edge, and `cur_max` only moved right.

## Why it is correct

**Invariant.** Before each pop: (a) the heap holds one current element per list, and `cur_max` is the largest of them; (b) no interval narrower than the best found so far can use an element that lies before its list's pointer (every such interval was scored or is dominated by one that was).

Popping the minimum `m` from list `i` and scoring `[m, cur_max]` covers the best interval that uses `m` for list `i`, by the turning-point argument. For any other list, the narrowest representative at or above `m` is its current pointer, because everything before the pointer is below an earlier minimum, which is at most `m`. So advancing list `i` loses nothing and keeps (b). Pushing the next element and taking the max keeps (a).

**Termination.** When list `i` is exhausted at a pop, every interval still unscored would need a representative of list `i` after its last element, and no such element exists. So the best scored interval is the answer.

**Ties.** Scoring with `<` instead of `<=` keeps the first interval found at a given width. Intervals are found in increasing order of left end, so that is the one with the smallest `a`.

## Cost

- **Time: O(N log k).** Each of the `N` elements is pushed at most once and popped at most once, on a heap of at most `k` entries. Updating `cur_max` is O(1).
- **Space: O(k)** for the heap.

The brute forces are O(N^3) over all pairs, and O(N k) with "forced `hi` per `lo`". The heap removes the factor of `k` by recomputing only the one pointer that moved.

## Variations you will meet

- **Minimum Window Substring (LeetCode 76).** The same "cover every category" goal on a single sequence. Merge all lists into one sorted list of `(value, list)` tags, and this problem becomes exactly a sliding window that must contain every list id at least once. That gives a second O(N log N) solution.
- **Pick one element per list to minimise max minus min.** That is this problem, phrased without intervals. Spot it in disguise, for example "choose one server from each region to minimise latency spread".
- **Lists are not sorted.** Sort each list first, at O(N log N) total, then run the merge.
- **Need the range to cover at least `t` of the `k` lists.** The heap no longer helps directly. Use the merged-list sliding window with a count of distinct lists in the window.

## What to carry forward

A k-way merge can carry state beyond the root. Here a running maximum that only grows, together with the heap minimum, defines a window that always covers every list, and you shrink it by advancing whichever list owns the minimum.

The next problem, Design Twitter, takes the merge out of a one-shot function and into a long-lived system. Each user's timeline is a sorted feed, and a news feed request runs a short k-way merge that stops after 10 items.
