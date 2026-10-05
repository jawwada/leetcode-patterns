# Data Stream as Disjoint Intervals

*LeetCode 352 · Hard · Pattern: Sorted disjoint intervals with bisect · Reading time ~11 min*

## The problem

Non-negative integers arrive one at a time. Implement SummaryRanges with addNum(value) and getIntervals(), which
returns the values seen so far as a sorted list of disjoint closed intervals, with consecutive integers merged.

```text
Example: add 1 -> [[1,1]]; add 3 -> [[1,1],[3,3]]; add 7 ->
  [[1,1],[3,3],[7,7]]; add 2 -> [[1,3],[7,7]]; add 6 ->
  [[1,3],[6,7]].
```

## What the problem is really asking

Numbers arrive one at a time. Every so often someone asks: "describe everything you have seen so far, as compactly as
possible." The compact description is a list of closed intervals `[start, end]`, sorted, never overlapping, and never
touching: if you have seen 1, 2 and 3, the answer is `[1,3]`, not `[1,1],[2,3]`. Duplicates change nothing.

So the answer object is a sorted run-length summary of a set of integers. You could also think of it as a number line
painted in black and white, where the answer lists the black stretches.

```text
values seen: 1 3 7 2 6

number line:
   0  1  2  3  4  5  6  7  8
   .  #  #  #  .  .  #  #  .
      [-----]        [--]
      [1,3]          [6,7]

answer: [[1,3],[6,7]]
```

What makes it hard is the interleaving. If you only had to produce the summary once at the end, you would sort and sweep
and be done. Here `addNum` and `getIntervals` alternate, possibly thousands of times, and each `getIntervals` must
reflect every value added so far. The question is how much of the previous answer you can reuse when one more value
lands.

## Do it by hand first

Take the stream 1, 3, 7, 2, 6. Keep a sheet of paper with the current intervals written left to right.

```text
add 1:  [1,1]
add 3:  [1,1] [3,3]           3 is not next to 1 -> new
add 7:  [1,1] [3,3] [7,7]     7 is far from 3 -> new
add 2:  [1,1] [3,3] [7,7]
         ^end+1   ^start-1    2 glues [1,1] and [3,3]
        [1,3] [7,7]
add 6:  [1,3] [7,7]
                ^start-1      6 stretches [7,7] left
        [1,3] [6,7]
```

Notice what your eye did on each step. It never re-read the whole sheet. It found the spot where the new number would
sit, glanced at the interval just to its left and the interval just to its right, and made a decision. When 2 arrived,
you did not care about `[7,7]` at all.

That is the seed: the hand kept a sorted list of intervals and, for each new value, looked only at its two neighbours.

## The first honest attempt

Put every value into a set. `addNum` is a set insert, O(1). `getIntervals` sorts the set and walks it, opening a new
interval whenever the next value is not the previous plus one.

That is correct and very easy to say out loud. Its cost is O(n log n) per `getIntervals` with n distinct values seen.
If the calls alternate, the total is O(q · n log n), and with 3·10^4 calls that is a lot of sorting.

The waste is visible if you draw two consecutive queries:

```text
query after 1,3,7,2:
  sort  -> 1 2 3 7
  sweep -> [1,3] [7,7]

add 6, query again:
  sort  -> 1 2 3 6 7      <- re-sorts 1,2,3,7 again
  sweep -> [1,3] [6,7]    <- re-merges 1,2,3 again
           ~~~~~
           unchanged, rebuilt anyway
```

`[1,3]` was computed, thrown away, and computed again. Adding one value can change at most a couple of intervals,
yet the brute force rebuilds all of them.

## The turning point

**Claim: if the intervals are kept sorted and disjoint at all times, a new value v can only interact with two of them:
the last interval that starts at or before v, and the first interval that starts after v.**

Why only those two? Because the intervals are disjoint and sorted, every interval further left ends before the left
neighbour starts, so it is at least two away from v. Every interval further right starts after the right neighbour
ends, so it is far from v too. The only questions left are local:

- Does the left neighbour already contain v? Then nothing changes.
- Does the left neighbour end at exactly v - 1? Then v extends it.
- Does the right neighbour start at exactly v + 1? Then v extends it the other way.
- Both? Then v fills a one-wide gap and the two neighbours become one interval.
- Neither? Then v is a new singleton `[v, v]`.

```text
five cases, v = the new value, L = left nbr, R = right nbr

covered:     L=[a ...v... b]          -> no change
touch L:     L=[a, v-1]   v           -> L=[a, v]
touch R:            v   R=[v+1, b]    -> R=[v, b]
bridge:   L=[a,v-1] v R=[v+1,b]       -> [a, b]  (R deleted)
alone:    L=[..]  .  v  .  R=[..]     -> insert [v, v]
```

The structure that turns this into an algorithm is two parallel sorted lists, `starts` and `ends`, where
`starts[k]` and `ends[k]` describe interval k. Sortedness of `starts` lets a binary search locate the neighbours:
`i = bisect_right(starts, v)` is the number of intervals whose start is at most v, so interval `i - 1` is the left
neighbour and interval `i` is the right neighbour.

Why `bisect_right` and not `bisect_left`? If v equals some start exactly, we want that interval to be the left
neighbour (it contains v). `bisect_right` puts i just past it, so `i - 1` points at it. `bisect_left` would put i at it
and you would look at the wrong interval on the left.

Parallel lists rather than a list of pairs is a convenience: `bisect` works directly on `starts`, and an extension is
a single assignment into one list. `getIntervals` then just zips the two lists together, O(k) for k intervals.

There is a cost hidden in Python: inserting into or deleting from the middle of a list shifts the tail, O(k). In Java
or C++ you would use a TreeMap or `std::map` and pay O(log k). Even with the shift, this is far cheaper than a full
sort per query: the shift is a single fast memory move, and in the common cases (covered, touch one side) nothing moves
at all.

## Watch it work

Stream 1, 3, 7, 2, 6, 2. Each frame shows `starts`, `ends`, and `i = bisect_right(starts, v)`.

Frame 1: add 1.

```text
starts []        i = 0
ends   []        no left, no right
-> alone: insert at 0
starts [1]
ends   [1]
```

Empty lists, so the value becomes the first singleton.

Frame 2: add 3, then add 7.

```text
add 3: starts [1]    i=1  left=[1,1] ends at 1, not 2
       -> alone: starts [1,3]   ends [1,3]
add 7: starts [1,3]  i=2  left=[3,3] ends at 3, not 6
       -> alone: starts [1,3,7] ends [1,3,7]
```

Neither value is adjacent to anything, so both become singletons at the position bisect gave.

Frame 3: add 2.

```text
starts [1, 3, 7]      i = 1
        ^  ^
     left  right
left  = [1,1]: ends at 1 == 2-1   touch left
right = [3,3]: starts at 3 == 2+1 touch right
-> bridge: ends[0] = ends[1] = 3, delete index 1
starts [1, 7]
ends   [3, 7]
```

The bridge case: two intervals become one and the lists shrink by one.

Frame 4: add 6.

```text
starts [1, 7]   ends [3, 7]    i = 1
left  = [1,3]: ends at 3, not 5
right = [7,7]: starts at 7 == 6+1  touch right
-> starts[1] = 6
starts [1, 6]
ends   [3, 7]
```

Only the right neighbour's start moves; nothing is inserted.

Frame 5: add 2 again.

```text
starts [1, 6]   ends [3, 7]    i = 1
left  = [1,3]: ends[0] = 3 >= 2  covered
-> return, no change
```

The duplicate is caught by the first check and never creates an overlap. `getIntervals` now returns
`[[1,3],[6,7]]`.

Across every frame the two lists stayed sorted, every interval had `start <= end`, and consecutive intervals were
separated by at least one missing integer (`ends[k] + 1 < starts[k+1]`). Every step only touched index `i - 1` or `i`.

## Why it is correct

The invariant is: `starts` is strictly increasing, `ends[k] >= starts[k]`, and `ends[k] + 1 < starts[k + 1]` for all
k. In words, the intervals are sorted, non-empty, and separated by real gaps. Together with "the union of the intervals
equals the set of values seen", that is exactly the definition of the required answer, so `getIntervals` is correct
whenever the invariant holds.

Now check each case preserves it when v arrives.

- Covered: nothing changes, and v was already in the union. Fine.
- Touch left only: `ends[i-1]` becomes v. The gap to the right neighbour is still at least one, because "touch right"
  was false, so `starts[i] > v + 1`.
- Touch right only: symmetric, `starts[i]` becomes v and the left gap is still real because "touch left" was false.
- Bridge: the left interval absorbs v and the whole right interval. The new interval's gaps to its outer neighbours
  are the old gaps, already real.
- Alone: `[v, v]` is inserted at position i. Left neighbour ends before v - 1, right neighbour starts after v + 1, so
  both gaps are real, and sortedness holds because bisect chose the position.

In every case the union grows by exactly {v}. The covered check must come first: with intervals `[1,5]` and v = 3,
neither "touch" test fires (5 is not 2, and nothing starts at 4), so without the check v would fall through to
"alone" and `[3,3]` would be inserted inside `[1,5]`, breaking disjointness.

## Cost

- `addNum`: O(log k) to bisect plus O(k) worst case for a list insert or delete, where k is the number of intervals.
  With a balanced tree map it is O(log k) total.
- `getIntervals`: O(k) to zip the lists.
- Space: O(k), never more than the number of distinct values, and often much less because merging collapses runs.

The brute force is O(1) per add and O(n log n) per query with n distinct values; since k <= n and the query is usually
the frequent operation, the incremental version wins.

## Variations you will meet

- **Many merges, few distinct intervals.** The follow-up on LeetCode asks what happens if there are lots of merges and
  the number of intervals is small compared to the stream. Then k is tiny and every operation is effectively constant;
  the incremental design is ideal. If instead getIntervals is rare and adds are huge, the brute force set plus sort on
  demand can win, because it makes `addNum` truly O(1).
- **Insert Interval (LeetCode 57).** Instead of a single point you insert a whole interval. The neighbours are no
  longer just two: the new interval may swallow many existing ones. Find the first and last affected interval with two
  bisects and replace that slice. That is exactly the step up taken by the next problem.
- **Removing values.** If a value can be removed, an interval may split in two. Points are now the wrong unit; you
  want boundaries, which is the representation of Range Module.
- **Count of covered integers.** Keep a running total of `end - start + 1` and adjust it in each case; it costs nothing
  extra.

## What to carry forward

A set kept sorted and disjoint at all times is only ever disturbed locally: binary search finds the neighbours, and a
handful of cases repair them. The next problem, Range Module, adds and removes whole ranges instead of single points,
and replaces the pair-of-lists with a single list of boundaries whose parity tells you inside from outside.
