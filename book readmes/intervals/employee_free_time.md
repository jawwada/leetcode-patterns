# Employee Free Time
*LeetCode 759 · Hard · Pattern: K-way merge of sorted interval lists with a min-heap, emitting gaps · Reading time ~10 min*

## The problem

schedule[i] is the sorted, non-overlapping list of working intervals of employee i. Return the finite intervals of
positive length during which every employee is free, in sorted order.

```text
Example: [[[1,2],[5,6]],[[1,3]],[[4,10]]] -> [[3,4]].
  [[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]] -> [[5,6],[7,9]].
```

## What the problem is really asking

There are k employees. Each one has a list of working intervals, already sorted by start and pairwise disjoint within that employee. You want the stretches of time when **nobody** is working, the common free time. Only finite stretches count (the time before the first shift and after the last one is unbounded, so ignore it), and only stretches of positive length count. If one person stops at 4 and another starts at 4, there is no gap.

Restated: take the union of everyone's busy time and return the holes in it. That is Merge Intervals followed by "read off the gaps between consecutive merged blocks". The answer is a sorted list of intervals.

What makes it Hard is not the idea but the structure of the input. The intervals come in k separate sorted lists, and the clean solution respects that instead of throwing all N intervals into one big sort.

Running example: `[[[1,3],[6,7]], [[2,4]], [[2,5],[9,12]]]`, answer `[[5,6],[7,9]]`.

```text
E0        [=======]           [===]
E1            [=======]
E2            [===========]               [===========]
union     [===============]   [===]       [===========]
      +---+---+---+---+---+---+---+---+---+---+---+---+
      0   1   2   3   4   5   6   7   8   9   10  11  12
                          ^^^^^   ^^^^^^^^^
                          free     free
                          [5,6]    [7,9]
```

## Do it by hand first

Lay the three rows on top of each other on graph paper and run a pencil along the time axis. Keep one number in your head: **"someone is busy until at least here"**. Call it the reach.

You start at the earliest shift, which is E0's `[1,3]`, so reach = 3. The next earliest start anywhere is 2 (E1 and E2 both start at 2). Since 2 <= 3 there is no gap, and reach grows to 4, then to 5. The next earliest start anywhere is 6, from E0's second shift. 6 > 5, so the stretch from 5 to 6 had nobody in it. Write down `[5,6]`, and reach becomes 7. The next start is 9, from E2. 9 > 7, so write `[7,9]`, and reach becomes 12. No shifts are left.

```text
 next earliest start anywhere   vs reach   result
 1  (E0 [1,3])                  -          reach 3
 2  (E1 [2,4])                  2 <= 3     reach 4
 2  (E2 [2,5])                  2 <= 4     reach 5
 6  (E0 [6,7])                  6 >  5     gap [5,6], reach 7
 9  (E2 [9,12])                 9 >  7     gap [7,9], reach 12
```

Your hand tracked two things. One was the reach, which is Merge Intervals' running end. The other, the part that is actually new, was a way to repeatedly find **"the next earliest start across all k rows"**. Your eye did that by glancing at the first unread shift of each row and picking the leftmost. That glance is a k-way merge, and the structure for "smallest of k fronts" is a min-heap.

## The first honest attempt

There are two honest attempts, and both are worth saying out loud.

**Attempt A (definitional).** A free interval starts at some shift's end `a` and finishes at some shift's start `b` with `a < b`, and no shift of anyone covers any point strictly between them. So try every pair (end, start) and check every shift. With N total shifts that is N^2 pairs times N checks, O(N^3).

```text
 candidate (a,b) = (3, 6)?  check all N shifts:
   E0[1,3] ok  E0[6,7] ok  E1[2,4] covers 3..4 -> reject
 candidate (a,b) = (4, 6)?  check all N shifts again...
   E2[2,5] covers 4..5 -> reject
 candidate (5, 6)? check all N shifts again... accept
```

The repeated work: for every candidate we rescan every shift. In time order, though, only one fact decides whether a gap opens before a start, namely the largest end seen so far.

**Attempt B (flatten and merge).** Pour all N shifts into one list, sort by start, and run Merge Intervals while tracking reach. Every time a start exceeds reach, emit `[reach, start]`. That is O(N log N) time and O(N) space, and it is correct. Most interviewers will accept it.

Where is its waste? Each employee's list arrived already sorted. Sorting all N items rediscovers that order:

```text
 E0: [1,3] [6,7]          already in order
 E1: [2,4]                already in order
 E2: [2,5] [9,12]         already in order
 flatten+sort: N log N comparisons to re-learn
               what we were told, plus O(N) memory
```

When k is small and N is large (say 5 employees with 100,000 shifts each), `log k` is much less than `log N`. More importantly, a merge can run on streams, consuming each schedule lazily without materialising the whole thing.

## The turning point

**Claim: to visit all shifts in global start order, you only ever need to compare the first unvisited shift of each employee, so a min-heap holding one entry per employee produces the global order in O(log k) per shift.**

Justify it. Consider any employee's list. Its shifts are sorted, so its first unvisited shift starts no later than any of its other unvisited shifts. Therefore the globally earliest unvisited shift is the earliest among the k fronts. Pop it from the heap, then push that employee's next shift, which is its new front. The heap never holds more than k entries, one per employee who still has shifts left.

```text
 fronts heap (start, emp, idx)       what it represents
                                     
        (1,0,0)                      E0: [1,3] | [6,7]
        /     \                      E1: [2,4] |
   (2,1,0)   (2,2,0)                 E2: [2,5] | [9,12]
                                          ^ front of each
 array: [(1,0,0),(2,1,0),(2,2,0)]
```

That is exactly how Merge k Sorted Lists works, with the "append node to output" step replaced by Merge Intervals' step. It runs on the popped shift `[s, e]` with a running `reach`:

- if `s > reach`, the time `(reach, s)` is free for everyone, so emit `[reach, s]`;
- then `reach = max(reach, e)`.

Why `>` and not `>=`? If `s == reach`, one shift ends exactly when another begins, and that gap has zero length, which the problem excludes. Why `max`? A shift can be nested inside the busy block so far. Suppose a fourth employee worked `[3,4]`. It pops right after E2's `[2,5]`, and `reach = 4` would shrink the block, so the start 6 would emit `[4,6]`, even though E2 is busy until 5.

Why put `emp` and `idx` in the tuple? So the heap knows where to fetch the next shift. Also, because Python compares tuples element by element, two equal starts fall back to comparing `emp` (an int), never to comparing `Interval` objects, which would raise a `TypeError`. Notice that the two start-2 entries tie on start and are broken by employee index, 1 before 2.

One more design point: the reach starts as "unset" (`None`), not 0 or minus infinity. The time before the first shift is not a finite free interval, so the first popped shift must only set reach, never emit.

## Watch it work

Schedules: E0 `[1,3],[6,7]`, E1 `[2,4]`, E2 `[2,5],[9,12]`. State: heap array, reach, output.

**Frame 1.** Seed the heap with each employee's first shift and heapify.

```text
 heap = [(1,0,0), (2,1,0), (2,2,0)]       reach = None
          E0[1,3]  E1[2,4]  E2[2,5]       free  = []
```

Three fronts, one per employee.

**Frame 2.** Pop `(1,0,0)`, which is E0 `[1,3]`. Reach is unset, so no gap. Reach = 3. Push E0's next, `(6,0,1)`.

```text
 popped E0[1,3]                           reach = 3
 heap = [(2,1,0), (2,2,0), (6,0,1)]       free  = []
 busy:  1..3
```

The heap is refilled from the row that just gave up its front.

**Frame 3.** Pop `(2,1,0)`, which is E1 `[2,4]`. 2 > 3? No. Reach = max(3,4) = 4. E1 has no more shifts, so push nothing.

```text
 popped E1[2,4]                           reach = 4
 heap = [(2,2,0), (6,0,1)]                free  = []
 busy:  1 ... 4
```

The heap shrinks: E1 is exhausted.

**Frame 4.** Pop `(2,2,0)`, which is E2 `[2,5]`. 2 > 4? No. Reach = 5. Push E2's next, `(9,2,1)`.

```text
 popped E2[2,5]                           reach = 5
 heap = [(6,0,1), (9,2,1)]                free  = []
 busy:  1 ..... 5
```

The first busy block `[1,5]` is complete, but we do not know that until the next pop.

**Frame 5.** Pop `(6,0,1)`, which is E0 `[6,7]`. 6 > 5? Yes, so emit `[5,6]`. Reach = 7. E0 is exhausted.

```text
 popped E0[6,7]                           reach = 7
 heap = [(9,2,1)]                         free  = [[5,6]]
 busy:  1 ..... 5    6..7
 free:          [5,6]
```

The gap is found the moment a start overshoots the reach.

**Frame 6.** Pop `(9,2,1)`, which is E2 `[9,12]`. 9 > 7? Yes, so emit `[7,9]`. Reach = 12. The heap is empty, so stop.

```text
 popped E2[9,12]                          reach = 12
 heap = []                                free  = [[5,6],[7,9]]
 busy:  1 ..... 5    6..7       9 ..... 12
 free:          [5,6]    [7,9]
```

The output `[[5,6],[7,9]]` matches the solution.

Invariant across frames: the popped shifts came out in non-decreasing start order, reach was the right edge of the union of everything popped so far, and every positive-length hole in that union to the left of reach had been emitted.

## Why it is correct

Two facts compose.

**Order.** The heap pops shifts in global non-decreasing start order. Suppose shift `x` is popped while some unpopped shift `y` has `y.start < x.start`. Then `y`'s employee has a front `f` with `f.start <= y.start < x.start` (fronts are the earliest unvisited in their row), and `f` is in the heap. So the heap minimum is at most `f.start < x.start`, which contradicts popping `x`.

**Gaps.** Given shifts in start order, the reach rule is Merge Intervals. After processing a prefix, reach is the right end of the last merged block, and earlier blocks are closed (every later start is at least the current start). A new start `s > reach` means no shift seen so far covers `(reach, s)`. No shift yet to come covers it either, because they all start at `s` or later. So `(reach, s)` is a hole in the union with positive length, and it is maximal: its left end is a busy end, and its right end is a busy start. Conversely, every hole in the union lies between two consecutive merged blocks, and the pop that opens the right block is exactly when we emit it. Holes before the first shift and after the last are never emitted, because reach starts unset and no pop follows the last one.

## Cost

- **Time O(N log k).** Each of N shifts is pushed and popped once, and the heap holds at most k entries. Heapifying the first k entries is O(k).
- **Space O(k)** for the heap, plus the output.

Flatten-and-sort is O(N log N) time and O(N) space. The brute force over (end, start) pairs is O(N^3).

## Variations you will meet

- **Two people, find a common slot of length d** (1229, Meeting Scheduler). Here you want overlaps, not gaps. With two sorted lists, use two pointers (the k = 2 special case of the heap): advance the one that ends first and test `min(ends) - max(starts) >= d`.
- **Interval List Intersections** (986). Two sorted lists, two pointers, emit `[max(starts), min(ends)]` when it is non-empty, and advance the list whose interval ends first.
- **Free time within working hours [L, R]**. Clip at both ends: initialise reach to L instead of unset, and after the loop emit `[reach, R]` if reach < R.
- **Free time common to at least m of k people**. The union no longer suffices. Switch to +1/-1 events and emit stretches where the busy count drops below k - m + 1. That is the sweep of My Calendar III.

## What to carry forward

When the input is many already-sorted lists, a heap of their fronts replaces the global sort, and Merge Intervals' reach turns "start > reach" into "here is a hole". The next problem, Minimum Interval to Include Each Query, also sweeps two sorted streams (intervals and queries), but the heap now ranks intervals by size and throws out expired ones lazily.
