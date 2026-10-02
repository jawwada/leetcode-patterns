# Intervals and Sweep Lines
*8 problems · Reading time ~12 min*

## Why this chapter exists

An interval is the simplest thing that has a length: a meeting from 9 to 10, a shift from 2 to 5, a booking from day 10 to day 40, a rectangle's shadow on the x-axis. Interval problems ask one of a small number of questions about a pile of these: what do they cover together, where do they collide, how many are stacked at the worst moment, and where are the holes. The questions look different on the page, but every one of them yields to the same two moves: put the intervals in order along the line, then walk the line once while carrying a tiny amount of state.

The eight problems fall into four families:

- **Merging** (Merge Intervals, Insert Interval): collapse overlapping bars into the fewest bars that cover the same points.
- **Choosing** (Non-overlapping Intervals): keep as many bars as possible so that none collide, which means picking a sort order that makes greed safe.
- **Counting the stack** (Meeting Rooms II, My Calendar III): find the largest number of bars covering a single point, with a heap of end times or with +1/-1 events.
- **Sweeping with a question in hand** (Employee Free Time, Minimum Interval to Include Each Query, Rectangle Area II): walk a line through several sorted streams at once and answer something at each stop. That might be a gap, the smallest live bar, or the covered length of a slice of the plane.

## What it is

An interval `[s, e]` is a pair of numbers with `s <= e`. Picture it as a bar sitting above a number line, its left edge at `s` and its right edge at `e`. In memory it is just two numbers, usually a two-element list, so a problem's input is a list of pairs in no particular order.

```text
 the thing: bars above a number line

A           [===========]
B  [===========]
C                             [=====]
D     [==]
   +--+--+--+--+--+--+--+--+--+--+--+
   1  2  3  4  5  6  7  8  9  10 11 12

 how it is stored: a list of pairs, in input order

 intervals = [[4, 8], [1, 5], [10, 12], [2, 3]]
               A       B       C         D
 intervals[1]    -> [1, 5]   (B)
 intervals[1][0] -> 1        (B's start)
```

**Endpoint conventions matter.** Before writing a line of code, decide whether `[1,4]` and `[4,5]` collide. Problems in this chapter use three conventions:

```text
 closed [s, e]      both ends included; [1,4] and [4,5] share 4
 half-open [s, e)   end excluded; a meeting ending at 4 frees
                    the room for one starting at 4
 touching = ok      Non-overlapping Intervals: [1,2],[2,3] fine
```

The whole difference shows up as `<` versus `<=` in one comparison. Read the statement, then write that comparison with intent.

**Six ways two intervals can relate.** Take two intervals A and B. Up to swapping names, here is everything that can happen:

```text
 1. B before A      B [==]
                    A        [=====]
 2. B overlaps      B   [====]
    A's head        A      [=====]
 3. B inside A      B        [==]
                    A      [=======]
 4. A inside B      B    [==========]
                    A      [=====]
 5. B overlaps      B          [=====]
    A's tail        A      [=====]
 6. B after A       B               [==]
                    A      [=====]
```

Six cases is a lot to keep in your head, and a pairwise loop that tests all of them on every pair is O(n^2) before it does anything useful. Now sort by start. If you walk the bars left to right and A is the bar you already hold, the next bar B has `b.start >= a.start`. That kills cases 1, 2 and 4, because B cannot begin before A. Three cases remain:

```text
 sorted by start, A seen first, B next:

 3. nested      A [========]       b.start <= a.end
                B    [==]          -> overlap
 5. tail        A [=====]          b.start <= a.end
                B     [======]     -> overlap
 6. after       A [=====]          b.start >  a.end
                B          [===]   -> disjoint
```

One comparison, `b.start <= a.end`, separates "overlap" from "disjoint". One `max(a.end, b.end)` handles nested and tail together, since the merged end is whichever right edge reaches further. That is what sorting buys you. It turns a 2D question (every pair) into a 1D walk (each bar against one running state).

**The sweep line.** Now forget pairs entirely. Imagine a vertical line sliding left to right across the number line. Interesting things happen only at endpoints: a bar starts (the line enters it) or a bar ends (the line leaves it). Turn every interval into two **events**: `(s, +1)` and `(e, -1)`. Sort the events by time, walk them, and keep a running count. That count is the number of bars the line is inside at that moment.

```text
 bars:  A [1,5)  B [2,7)  C [6,9)

A  [===========)
B     [==============)
C                 [========)
   +--+--+--+--+--+--+--+--+
   1  2  3  4  5  6  7  8  9

 events sorted: (1,+1) (2,+1) (5,-1) (6,+1) (7,-1) (9,-1)
 running count:   1      2      1      2      1      0
                         ^             ^
                     peak 2        peak 2
```

**Difference arrays.** When coordinates are small integers, you can store the events in an array instead of sorting a list: `diff[s] += 1`, `diff[e] -= 1`, then take a prefix sum. The prefix sum at position `t` is the number of intervals covering `t`.

```text
 index   0  1  2  3  4  5  6  7  8  9
 diff    0 +1 +1  0  0 -1 +1 -1  0 -1
 prefix  0  1  2  2  2  1  2  1  1  0
              ^-- covered by A and B from 2 up to 5
```

**Coordinate compression.** When coordinates go up to 10^9, you cannot allocate that array. But only the endpoints matter, so collect the distinct endpoints, sort them, and give each one a small index. The 1e9-wide line becomes a short array of "slots between consecutive endpoints", and each slot keeps its true width for later arithmetic.

```text
 real coords:  3        1000      999999999
 sorted ids:   0        1         2
 slots:        [3,1000) width 997, [1000,999999999) width ...
```

My Calendar III uses a sparse version of the difference array (a dictionary plus a sorted key list). Rectangle Area II uses compression implicitly: it only ever looks at the sorted x-events and the sorted y-endpoints.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Sort n intervals by start or end | O(n log n) | comparison sort; usually the dominant cost |
| Overlap test of two intervals | O(1) | `a.s <= b.e and b.s <= a.e` (closed) |
| Merge into the running interval | O(1) | `end = max(end, e)` once sorted |
| Build 2n sweep events and sort them | O(n log n) | twice as many items as intervals |
| One sweep over sorted events | O(n) | one counter update per event |
| Difference array build + prefix sum | O(n + C) | C = coordinate range; only when C is small |
| Coordinate compression | O(n log n) | sort distinct endpoints, map to ranks |
| Heap of end times: push / pop min | O(log n) | earliest-finishing bar sits on top |
| Insert a boundary into a sorted list | O(n) | `bisect.insort` finds in log n, shifts in n |

**Merging into a running interval.** The running interval `cur` is the only state. Each new bar either extends it or closes it.

```text
 cur = [1, 5]      next = [4, 8]   4 <= 5 -> extend
 cur = [1, 8]      next = [10,12]  10 > 8 -> emit [1,8],
 cur = [10,12]                              start fresh
```

**A heap of end times.** When you need to know which of the currently open bars ends first, keep their ends in a min-heap. The triangle is how to think about it; the array is how Python stores it (children of index i live at 2i+1 and 2i+2).

```text
 open bars end at 12, 19, 20

        12            heap array: [12, 19, 20]
       /  \                         ^ top = soonest end
     19    20
 pop when the next start >= 12: that bar has left
```

**Sweep with a counter.** Sort the events and walk them. At equal times, the order of a `-1` and a `+1` decides whether touching bars count as overlapping. Sorting tuples `(t, delta)` puts `-1` before `+1` automatically, which is the half-open convention.

```text
 events (5,-1) and (5,+1) at the same time:
   sorted -> (5,-1), (5,+1)
   count:  2 -> 1 -> 2        (never 3: touching != overlap)
```

## The invariant

Every technique in this chapter protects one sentence:

> **Everything to the left of the sweep line is finished, and the state you carry summarises it completely.**

For merging, the state is the running interval: every bar to its left has been emitted or absorbed, and nothing to the right can reach back past its start, because of the sort. For counting, the state is a counter or a heap: it equals exactly the set of bars the line is currently inside. You never revisit a bar, and that is why one pass is enough.

```text
 LEGAL (sorted by start)

 done   [==]  [====]               emitted, never touched again
 cur              [=======]        the running state
 next                 [====]       starts >= cur.start: it can
                                   only touch cur, nothing older

 ILLEGAL (not sorted)

 done   [==]  [====]               already emitted...
 cur              [=======]
 next  [=========]                 starts behind cur and
                                   overlaps emitted bars:
                                   the summary is now wrong
```

In the illegal picture, a bar arrives behind the line. The bars it overlaps were already emitted, so the one-state summary cannot fix them. Sorting is what makes the invariant possible.

## How to picture it

Keep two pictures, and switch between them.

**Bars above a number line, with a vertical line moving right.** The line carries a small payload: a running interval, a count, a heap of right edges. It stops only at endpoints. Everything left of it is settled; everything right of it is unseen.

```text
          sweep -->
 [=====]     |
    [========|==]
             |  [====]
         [===|=====]
 +--+--+--+--+--+--+--+--+
             ^ line at x; count = 3 bars cut
```

**The skyline of stacked bars.** If you pile the bars on top of each other, the height of the pile at each x is the coverage count. "Minimum rooms", "max k-booking", and "is anyone busy here" are all questions about this skyline. The +1/-1 events are the steps of the skyline, and a prefix sum redraws it.

```text
 height
   3 |        +--+
   2 |     +--+  +--+
   1 |  +--+        +-----+
   0 +--+-----------------+---
        1  2  3  4  5  6  7
```

Rectangle Area II lifts this into two dimensions. The vertical line now cuts a set of y-intervals, and the skyline becomes "how much of the line is covered", multiplied by how far the line moves.

## Signals in a problem statement

- "intervals", "meetings", "bookings", "shifts", "ranges", `[start, end]` pairs: you are in this chapter.
- "merge", "union", "total covered length": sort by start, keep a running interval.
- "minimum number to remove so none overlap", "maximum number of non-overlapping", "activities", "arrows to burst balloons": greedy by earliest end.
- "minimum rooms / platforms / servers", "maximum concurrent", "k-booking": count the stack with a heap of ends or with +1/-1 events.
- "free time common to all", "gaps": take the union, then its complement.
- Many queries asking "which interval contains this point": answer them offline, sorted, and sweep.
- Coordinates up to 1e9 with n up to a few hundred or thousand: compress coordinates or use a sparse map of events.
- "area of the union of rectangles": sweep one axis, merge intervals on the other.

Counter-signals:
- Intervals arrive online and you must answer range-sum or range-max queries with updates: you need a segment tree or Fenwick tree (the follow-ups of My Calendar III and Rectangle Area II).
- "subarray" or "substring" with a contiguous window over an array of values: that is a sliding window, not intervals.
- You must pick intervals to maximise total weight (not count): greedy fails, so use DP plus binary search (weighted interval scheduling).

## Python toolbox

Sorting by one end, and the tuple order of events:

```python
intervals.sort(key=lambda iv: iv[0])      # by start
intervals.sort(key=lambda iv: iv[1])      # by end (scheduling)
events = [(s, 1) for s, e in ivs] + [(e, -1) for s, e in ivs]
events.sort()          # at equal t, -1 comes before +1
```

Min-heap of end times (heapq is min-only; negate for max):

```python
import heapq
ends = []
heapq.heappush(ends, 12)
while ends and ends[0] <= start:   # peek is ends[0]
    heapq.heappop(ends)
```

Tuples in a heap compare element by element, so `(start, employee, index)` breaks ties without comparing objects. Keep the object out of the tuple, or add an index before it.

Prefix sums and a sorted key list for sparse coordinates:

```python
from itertools import accumulate
from bisect import insort
cover = list(accumulate(diff))      # difference -> counts
insort(points, p)                   # keep keys sorted
```

`sorted` is stable, so sorting by a secondary key and then by a primary key gives a two-level order. There is no balanced BST in the standard library; `sortedcontainers.SortedList` is not available on every judge, so do not rely on it.

## Mistakes people make

1. **`<` where you needed `<=`** (or the reverse). Fix: write down the endpoint convention from the statement before coding the comparison.
2. **`end = e` instead of `end = max(end, e)`** when merging. A short bar nested inside a long one shrinks the merge. Fix: always take the max.
3. **Forgetting to sort**, or sorting by the wrong end. Fix: merging and counting sort by start; choosing (scheduling) sorts by end.
4. **Mutating the caller's intervals** while merging (`merged.append(iv)` then editing `merged[-1]`). Fix: copy with `iv[:]` when you will write to it.
5. **Wrong tie order at equal times** in an event sweep. Fix: for half-open intervals put ends before starts, which `(t, -1) < (t, +1)` does for you.
6. **Popping only one expired item** from a heap when several have expired. Fix: use `while`, not `if`, unless you can argue why one pop suffices.
7. **Losing the original order of queries** after sorting them for an offline sweep. Fix: sort indices, not values, and write answers by index.
8. **Adding the slab after updating the active set** in a 2D sweep. Fix: the strip to the left of x belongs to the old set, so accumulate first, then apply the event.
9. **Emitting zero-length gaps** when one interval ends exactly where the next starts. Fix: emit only when `start > reach`.
10. **Allocating a 1e9 array** for a difference array. Fix: compress coordinates or use a dict plus sorted keys.

## The journey ahead

1. **Merge Intervals**: sort by start and keep one running interval. This is the base move every later problem reuses.
2. **Insert Interval**: the input is already sorted, so skip the sort and see the answer as three contiguous phases (left, fused, right).
3. **Non-overlapping Intervals**: the first time the sort key changes. Sorting by end makes greedy provably safe, via an exchange argument.
4. **Meeting Rooms II**: stop merging and start counting the stack, with a min-heap of end times as the state the sweep carries.
5. **Employee Free Time**: several pre-sorted lists, k-way merged by a heap, while the merge's "reach" exposes gaps.
6. **Minimum Interval to Include Each Query**: sort the questions too (offline), sweep both streams, and use a heap with lazy deletion.
7. **My Calendar III**: drop heaps for pure +1/-1 events in a sparse difference array, rebuilt as bookings arrive online.
8. **Rectangle Area II**: the closing problem. Sweep in x, merge intervals in y, and multiply. Every earlier idea appears at once.
