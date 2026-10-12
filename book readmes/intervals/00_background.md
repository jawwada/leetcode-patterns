# Intervals and Sweep Lines
*8 problems · Reading time ~25 min*

## The chapter

An interval is a start and an end on a line. This chapter teaches how sorting by start or by end makes merging,
choosing and counting overlapping intervals a single sweep, and how a sweep line that walks several sorted streams at
once answers questions about free time, query coverage and the area of a union of rectangles.

Problems, in reading order:

1. [Merge Intervals](merge_intervals.md) · Medium
2. [Insert Interval](insert_interval.md) · Medium
3. [Non-overlapping Intervals](non_overlapping_intervals.md) · Medium
4. [Meeting Rooms II](meeting_rooms_ii.md) · Medium
5. [Employee Free Time](employee_free_time.md) · Hard
6. [Minimum Interval to Include Each Query](minimum_interval_to_include_each_query.md) · Hard
7. [My Calendar III](my_calendar_iii.md) · Hard
8. [Rectangle Area II](rectangle_area_ii.md) · Hard

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

## Advanced patterns

The basic material gives you one sort and one running value. The Hard problems in this chapter push on that in three ways. The state the line carries becomes a *set* rather than a number. The input arrives in several streams instead of one. And the line has to move through a second dimension. The six patterns below are the moves that make those pushes manageable. Each one is still "sort, then sweep with a small state"; what changes is what you sort and what the state is.

### 1. Choosing the sort key: start for merging, end for choosing

**When it shows up**: any time the problem asks you to *pick* intervals (keep the most, remove the fewest, shoot the fewest arrows, attend the most events), not to combine them.

**The intuition**: sorting by start is right when every bar will end up in the answer in some form, because then you only care about who arrives next. When you are choosing, the question is different: which bar should win a collision? The bar that ends earliest leaves the most room for everything after it. The exchange argument makes this exact. Take any optimal choice. Its first bar ends no earlier than the globally earliest-ending bar `g`, so swapping `g` in breaks nothing to the right and keeps the count the same. Repeat on what is left. Sorting by start gives no such guarantee, because an early-starting bar can be enormously long and block everything.

```text
[1,10]  [=================]
[2,3]     [=]
[4,5]         [=]
[6,7]             [=]
        +-+-+-+-+-+-+-+-+-+
        1       5        10

 sorted by START: [1,10] first, kept, free at 10
                  [2,3] [4,5] [6,7] all collide   -> 1 kept
 sorted by END:   [2,3] free at 3, [4,5] free at 5,
                  [6,7] free at 7, [1,10] collides -> 3 kept
```

**Where you'll use it**: Non-overlapping Intervals is built on it. Beyond the chapter: Minimum Number of Arrows to Burst Balloons (452) and Maximum Number of Events That Can Be Attended (1353), where the same earliest-end rule is applied day by day through a heap of end times.

### 2. A heap of the live set, keyed by what you will ask

**When it shows up**: the sweep needs more than a count of the bars under the line. It needs a property of one of them: the one that ends first, the shortest, the tallest.

**The intuition**: as the line moves right, bars enter at their starts and must leave at their ends. You could keep the live bars in a list, but then every question scans the list. The observation is that at each stop you ask only *one* question, and that question names an extreme: "has the earliest-ending bar ended yet?" or "which live bar is shortest?". A min-heap keyed on exactly that quantity answers it in O(1) and updates in O(log n). In Meeting Rooms II the key is the end time, so the bars that must leave are precisely the ones on top, and the heap's size is the number of rooms in use. Pick the key to match the question, and the heap turns a set into a single readable value.

```text
 meetings (half-open): [1,5) [2,7) [4,6) [6,9)
 start  heap of ends (array)    rooms in use
   1    [5]                     1
   2    [5, 7]                  2
   4    [5, 7, 6]               3  <- peak
   6    pop 5, pop 6, push 9
        [7, 9]                  2
           7
          /        at start 6: the top (5) has ended, pop;
         9         the new top (6) has ended, pop; 7 stays
```

**Where you'll use it**: Meeting Rooms II (key = end), Minimum Interval to Include Each Query (key = size). Beyond the chapter: The Skyline Problem (218), where the key is the negated height.

### 3. K-way merge of sorted streams, with a reach that exposes gaps

**When it shows up**: the input is already several sorted lists (one per person, machine, or file), and you want the global order without paying for a full re-sort. Or you want the *complement* of a union: the free time, the holes, the uncovered stretches.

**The intuition**: inside one sorted list, the first unread item is the earliest of that list. So the globally earliest unread item is the earliest of the k fronts, and a heap holding one front per list hands it to you in O(log k). Pop it and push the next item from the same list. Feed the popped bars into Merge Intervals' running end, which here is called the *reach*: "someone is busy at least until here". A start that lands strictly beyond the reach proves that nobody covers the stretch between them, because every bar that could cover it has already been popped. The complement of the union appears without ever building the union.

```text
 E0 [1,3] [8,9]   E1 [2,4]   E2 [6,7]

 mid-run, after popping [1,3] and [2,4]:
 fronts heap: [(6,E2), (8,E0)]        reach = 4
 next pop: 6 > 4  -> gap [4,6], reach = 7
 next pop: 8 > 7  -> gap [7,8], reach = 9

busy   [========]     [==]  [==]
free            [=====]  [==]
       +--+--+--+--+--+--+--+--+--+
       1     3     5     7     9
```

**Where you'll use it**: Employee Free Time. Beyond the chapter: Merge k Sorted Lists (23) is the same frontier without the reach, and Interval List Intersections (986) is the k = 2 case with two pointers.

### 4. Offline queries swept alongside intervals, with lazy deletion

**When it shows up**: many point queries, each asking about the intervals that contain it, with n and m both near 10^5. You see all the queries before you answer any.

**The intuition**: "contains q" means two conditions, `left <= q` and `right >= q`. If you answer queries in increasing order, the first condition only ever admits more intervals, so a pointer through intervals sorted by left adds each one exactly once. The second condition only ever *removes* intervals, and an interval that has ended for one query has ended for every later one. That permanence is what makes lazy deletion safe: leave dead intervals in the heap and throw one away only when it reaches the top and would otherwise be reported. Each interval is pushed once and popped at most once, however the queries fall. Sort query *indices*, not values, so each answer goes back to its original slot.

```text
 intervals [1,4] [2,9] [3,5]    queries (slot:value) 0:6 1:3 2:8
 heap key = (size, right); swept order 3, 6, 8

 q=3  push all three   heap {(3,5) (4,4) (8,9)}
      top (3,5): 5 >= 3 alive          ans[1] = 3
 q=6  top (3,5): 5 < 6 dead, pop
      top (4,4): 4 < 6 dead, pop
      top (8,9): alive                 ans[0] = 8
 q=8  top (8,9): alive                 ans[2] = 8
 answer in input order: [8, 3, 8]
```

**Where you'll use it**: Minimum Interval to Include Each Query. Beyond the chapter: Number of Flowers in Full Bloom (2251), where the heap collapses into two `bisect` counts.

### 5. A sparse difference map, maintained online

**When it shows up**: bookings arrive one at a time, and after each one you must report a coverage fact (the peak overlap, whether a triple booking exists), with coordinates far too large for an array.

**The intuition**: coverage is a step function. It changes only at boundaries, and the size of each step is (starts there) minus (ends there). So store just that: a dictionary from boundary to net change, plus a sorted list of the boundaries. A new booking touches two entries. A prefix sum along the sorted boundaries redraws the whole skyline, and its maximum is the peak. Ends and starts at the same coordinate land in one slot and cancel *before* the sweep reads them, which is exactly the half-open convention without any special-case code. This is coordinate compression done lazily: a boundary gets a slot only when some booking mentions it.

```text
 after [3,8) and [5,12):
 point   3   5   8  12
 delta  +1  +1  -1  -1
 prefix  1   2   1   0        peak 2

 book [8,10): delta[8] = -1 + 1 = 0, new point 10
 point   3   5   8  10  12
 delta  +1  +1   0  -1  -1
 prefix  1   2   2   1   0    peak 2 (8 is a seam,
                              not a third layer)
```

**Where you'll use it**: My Calendar III. Beyond the chapter: My Calendar I and II (729, 731), and Car Pooling (1094) when coordinates are small enough for a plain array.

### 6. Sweep one axis, measure the other

**When it shows up**: rectangles, or anything with two interval dimensions, and a question about the union: total area, perimeter, whether they tile.

**The intuition**: move a vertical line across x. Rectangles enter at x1 and leave at x2, and between two consecutive x-events the line cuts the same set of rectangles, so the covered length on the line is constant. Area is then a sum of slabs, each (width between events) times (covered length). Measuring that length is a 1D problem: merge the active y-intervals, or compress the y-coordinates into elementary segments and keep a cover count per segment, counting the widths of segments with count > 0. Add each slab *before* applying the event at its right edge, because the slab belongs to the old active set. Keeping per-segment cover counts in a segment tree is the step that takes this from O(n^2) to O(n log n).

```text
 rectangles A [0,0,2,2]  B [1,0,2,3]  C [1,0,3,1]
 line inside strip x in [1,2): active y = (0,2) (0,1) (0,3)

 ys       0     1     2     3
 segment  [0,1) [1,2) [2,3)
 count      3     2     1      every segment covered
 covered = 1 + 1 + 1 = 3      slab = width 1 * 3 = 3
```

**Where you'll use it**: Rectangle Area II. Beyond the chapter: Perfect Rectangle (391) and The Skyline Problem (218), which sweeps the same x-events with a heap of heights as the state.

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

The eight problems climb in one direction: the state the sweep carries gets richer. It starts as one running interval, becomes a single number, then a heap of live bars, then a map of boundaries, and finally a whole set of intervals measured at every stop. Each problem keeps what the previous one taught and changes exactly one thing.

### Foundations: one sort, one running value

**Merge Intervals.** Overlapping bars in random order, collapse them. The naive instinct is to compare every pair and keep merging until nothing changes, which is quadratic and fiddly. The question worth asking is: what order makes a single comparison enough? Sorting by start does, and the running interval plus `end = max(end, e)` is the base move every later problem reuses.

**Insert Interval.** The list is already sorted and disjoint, and one new bar arrives. You could append and re-run Merge Intervals in O(n log n), but that ignores what you were given. The new idea is to see the answer as three contiguous phases (bars wholly left, bars that fuse with the newcomer, bars wholly right), which is O(n) and teaches you to exploit sortedness rather than re-create it.

**Non-overlapping Intervals.** Now you choose instead of combine: remove the fewest bars so the rest never collide. The trap is to keep the sort by start, which happily keeps a giant bar that blocks everything. This is the first time the sort key changes. Sorting by end and keeping whatever fits is provably optimal by an exchange argument, and that argument is the template for every interval greedy you will meet.

### Carrying a set, not a number

**Meeting Rooms II.** How many rooms do the meetings need? A single running end no longer suffices, because several meetings are open at once and you must know which frees up first. The curious question is "when a new meeting starts, who has left?", and the answer is always the meetings with the smallest end times. A min-heap of end times becomes the state, and its size at each start is the room count. Pattern 2 starts here.

**Employee Free Time.** Each employee's schedule is already sorted, and you want the times when nobody works. Flattening and re-sorting works, but it throws away the order you were given. The new idea is the k-way merge: a heap holding only each employee's next shift produces the global order, and Merge Intervals' reach turns "this start is beyond everything seen" into a gap. It builds on Meeting Rooms II by using the heap as a frontier over streams instead of a live set.

**Minimum Interval to Include Each Query.** Now the questions are points, a hundred thousand of them, each asking for the shortest interval that contains it. Testing every pair is 10^10 checks. The leap is to treat the queries as a second sorted stream: sweep both together, admit intervals with a forward-only pointer, and keep a heap keyed by size whose dead entries are thrown away lazily, only when they surface. It combines the live-set heap of Meeting Rooms II with the two-stream sweep of Employee Free Time.

### Events and the plane

**My Calendar III.** Bookings arrive one by one, and after each you report the peak overlap. There is no batch to sort and the coordinates reach 10^9. The new idea drops the heap entirely: store only the net +1/-1 change at each boundary in a sparse map, and a prefix sum redraws the skyline on demand. It is Meeting Rooms II's count rebuilt for an online setting, and it introduces the event view that the last problem needs.

**Rectangle Area II.** The union of rectangles can be any jagged shape, and inclusion-exclusion has 2^n terms. The question that unlocks it is: what does a vertical line see, and when does that change? Sweep x with enter and leave events (My Calendar III's events), and at each stop measure the covered y-length with Merge Intervals (the first problem). Every earlier idea appears at once, and the step to a segment tree is the natural follow-up.
