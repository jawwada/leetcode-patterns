## Intervals and Sweep Line

> Lay the intervals on a number line and sweep a vertical line from left to right. Sort once, and every decision only needs what the line is touching right now: the block being merged, the room that frees up first, or a running count of open intervals.

The heap handed you the cheapest item next. Intervals add a second habit, sorting once: after one sort by start, a single left-to-right sweep answers most interval questions, and a heap of end times returns when you must know which meeting finishes first.

**Reach for it when** the input is pairs `[start, end]` (meetings, bookings, ranges, buildings, rectangles) and the question is about overlap: merge them, insert one, intersect two lists of them, keep the most / remove the fewest so that none overlap, find how many are open at once (rooms), find the free gaps, or answer "which intervals contain point q?".

### The picture

```text
0   2   4   6   8   10  12  14  16  18
  [===]                                     [1,3]
    [=======]                               [2,6]    2 <= 3: same block, its end stretches to 6
                [===]                       [8,10]   8 > 6: block [1,6] is final, open a new one
                  [=====]                   [9,12]   9 <= 10: stretch to 12
                              [=====]       [15,18]  15 > 12: block [8,12] is final
  [=========]   [=======]     [=====]       merged:  [1,6] [8,12] [15,18]
```

Compare every pair and you pay O(n²); merge until nothing changes and it is O(n³). After sorting by start, an interval can only overlap the block you are building *right now*: every later interval starts even later, so once one starts past the block's end, that block is final and never looked at again. One sort and one sweep: O(n log n).

### Overlap in one line

```text
two intervals overlap  <=>  each one starts before the other one ends

  a [=======)              a [=======)                a [=====)
  b     [=======)          b         [=======)        b           [=====)
    overlap                  touching: a.end == b.start   apart

half-open [s, e)   a.start <  b.end and b.start <  a.end     meetings, bookings
closed    [s, e]   a.start <= b.end and b.start <= a.end     merge intervals, "touching overlaps"
```

It is easier to say when two intervals do *not* overlap: one ends before the other starts. Negate that and you get the one-liner above, which handles partial, nested and identical intervals with no case analysis. When they do overlap, the common part is `[max(a.start, b.start), min(a.end, b.end)]`.

The only real question is what happens at a shared endpoint, and the problem statement decides it. Take `[1, 2]` and `[2, 3]`. Merge Intervals (56) and Insert Interval (57), which merge whatever overlaps, treat ends as closed: the two form one block `[1, 3]`, and the test is `start <= block_end`. Interval List Intersections (986), the common parts of two lists, is closed too: the two share the point 2, and a pair meets when `max(starts) <= min(ends)`.

Rooms and bookings are half-open, `[s, e)`. In Meeting Rooms II (253), the fewest rooms that hold a set of meetings, and in My Calendar I (729) and III (732), which take bookings one at a time, a meeting that ends at 2 leaves its room free for one that starts at 2, so a room is free when `end <= start`.

Two more problems read touching the same way. Non-overlapping Intervals (435), which removes the fewest intervals so that none overlap, keeps `[1, 2]` and `[2, 3]` together: an interval stays when `start >= kept_end`. Employee Free Time (759), the gaps when everyone is free, finds no gap between busy blocks that touch, so a gap opens only when `start > busy_until`.

### From idea to code

*Sort by start, then sweep: to merge, keep one "current" block that each interval either stretches or closes; to count, keep the end times of what is still running, free what has ended, then add the newcomer.*

For merging, as in Merge Intervals and Insert Interval, the **State** is the block being built, `merged[-1]`, whose **Definition** is the union of everything so far that chains into it; every block before it is finished. The **Invariant** is that `merged` is sorted, disjoint, and covers exactly the intervals seen so far. A **Step** stretches the block to `max(merged[-1][1], end)`, the `max` because the newcomer may be nested inside, or opens a new block when the newcomer starts past the block's end.

There is no **Fix**, because after the sort only `merged[-1]` can be touched. The **Record** happens when a block becomes final: the moment an interval starts after its end, or when the input ends. The **Init** is the sort by start, `sorted(intervals)`, which orders lists by start and then by end, and an empty `merged`; the **Return** is `merged`, `[]` for empty input.

For counting how many run at once, as in Meeting Rooms II, the state is `ends`, a min-heap of the end times of the meetings still running at the current start, so `ends[0]` is the room that frees up first. The invariant, after the fix, is that every end in the heap is later than `start`.

The fix frees every room whose meeting is over, `while ends and ends[0] <= start: heappop(ends)`. The step pushes the newcomer's end, because it takes a room, and the record is `rooms = max(rooms, len(ends))` right after the push. Init sorts by start with an empty heap; the return is `rooms`.

The record reads how many meetings run at this instant, so it must come after both other lines. Move the freeing loop below the count and the back-to-back meetings `[1, 5]`, `[5, 9]` need 2 rooms; move the count above the push and `[[1, 5], [2, 6], [3, 7]]` needs only 2 rooms instead of 3. Freeing before the push also reads naturally: the newcomer may take a room whose meeting ended exactly at its start.

The cell below holds both templates. Merge Intervals merges every overlapping pair, touching included: `[[1, 3], [2, 6], [8, 10], [15, 18]]` becomes `[[1, 6], [8, 10], [15, 18]]`. Meeting Rooms II asks for the fewest rooms so that no two meetings share a room at the same time, where a meeting may start exactly when another ends: `[[0, 30], [5, 10], [15, 20]]` needs 2. The `overlaps` helper is the one-liner for half-open ends.

<!-- cell -->

```python
def merge(intervals):
    intervals = sorted(intervals)                     # INIT: by start (ties by end)
    merged = []                                       # STATE: finished blocks + the current one, merged[-1]
    for start, end in intervals:
        if merged and start <= merged[-1][1]:         # starts inside the current block:
            merged[-1][1] = max(merged[-1][1], end)   # STEP: stretch it (max: it may be nested)
        else:
            merged.append([start, end])               # STEP + RECORD: the block before is final; open a new one
    return merged                                     # RETURN


def overlaps(a, b):                                   # half-open [s, e): touching is NOT overlapping
    return a[0] < b[1] and b[0] < a[1]


def min_rooms_heap(meetings):
    meetings = sorted(meetings)              # INIT: by start
    ends, rooms = [], 0                      # STATE: min-heap of end times of the meetings running now
    for start, end in meetings:
        while ends and ends[0] <= start:     # FIX: free every room whose meeting is over (half-open: <=)
            heapq.heappop(ends)
        heapq.heappush(ends, end)            # STEP: this meeting takes a room
        rooms = max(rooms, len(ends))        # RECORD: rooms in use right now
    return rooms                             # RETURN


print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))     # [[1, 6], [8, 10], [15, 18]]
print(merge([[1, 4], [4, 5]]), overlaps([1, 4], [4, 5]), overlaps([1, 9], [3, 4]))   # [[1, 5]] False True
print(min_rooms_heap([[0, 30], [5, 10], [15, 20]]), min_rooms_heap([[1, 5], [5, 9]]))  # 2 1
```

<!-- cell -->

**Try it**
- Change `max(merged[-1][1], end)` to plain `end` and run `merge([[1, 10], [2, 3], [4, 5]])`: `[[1, 3], [4, 5]]`. The nested `[2, 3]` shrank the block.
- Change `<=` to `<` in `merge`: `merge([[1, 4], [4, 5]])` now gives `[[1, 4], [4, 5]]`. Closed or half-open is a decision you read from the problem, then write once.
- Delete the INIT line, so that the loop sees the input order, and run `merge([[8, 10], [1, 3], [2, 6]])`: `[[8, 10]]`. The test only looks at the block's end, so `[1, 3]` and `[2, 6]` were swallowed by a block they never touch.
- In `min_rooms_heap`, move the `while` loop below the RECORD line: `min_rooms_heap([[1, 5], [5, 9]])` needs 2 rooms. The room was freed one step too late.

<!-- cell -->

The peak is the answer, and the reason is worth saying out loud. At the busiest instant that many meetings run at once, and each needs its own room, so fewer rooms is impossible. That many is also enough: hand out rooms in start order, each to a room whose meeting has ended. One is always free, because otherwise one more meeting than the peak would be running at that moment.

### Watch it work

Fed in a shuffled order, the sweep still sees the intervals sorted. The trace prints, for each interval, whether it stretched the open block or closed it, and the blocks built so far.

<!-- cell -->

```python
def trace_merge(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            old = merged[-1][1]
            merged[-1][1] = max(old, end)
            note = f"{start} <= {old}: stretch to {merged[-1][1]}"
        else:
            note = f"{start} > {merged[-1][1]}: {merged[-1]} is final" if merged else "open the first block"
            merged.append([start, end])
        print(f"[{start:>2},{end:>3}]  {note:<26} merged={merged}")


trace_merge([[8, 10], [1, 3], [15, 18], [2, 6], [9, 12]])
```

<!-- cell -->

**Try it**
- Run `trace_merge([[1, 10], [2, 3], [4, 5]])`: the block stays `[1, 10]` while the small intervals are swallowed. That is the `max` at work.
- Run `trace_merge([[1, 2], [2, 3], [3, 4]])`: each touches the next, so the chain becomes one block `[1, 4]`.
- Run `trace_merge([[1, 2], [3, 4], [2, 3]])`: one block `[1, 4]`. Without the sort the loop gives `[[1, 2], [3, 4]]`: a late interval can bridge two blocks that were already closed.

<!-- cell -->

### Where it goes wrong

Most interval bugs are one wrong comparison, so each trap below names the comparison and the input that exposes it.

1. **Sorting by the wrong key, or not at all.** Merging and rooms: sort by start. "Keep the most / remove the fewest": sort by **end**. With `[[1, 100], [2, 3], [4, 5]]`, keeping greedily in start order keeps `[1, 100]` and removes 2; end order removes only 1.
2. **`end` instead of `max(...)`** when stretching: a nested interval shrinks the block (`[[1, 10], [2, 3], [4, 5]]` → `[[1, 3], [4, 5]]`).
3. **Comparing with the previous interval instead of the block.** After the nested `[2, 3]`, the previous end (3) is below the block's end (10), so `[[1, 10], [2, 3], [4, 5]]` becomes `[[1, 10], [4, 5]]`. Always compare with `merged[-1]`.
4. **`<` vs `<=` at a shared endpoint.** Closed ends (merge): `[1, 4]` and `[4, 5]` overlap. Half-open (meetings): a meeting ending at 10 frees its room for one starting at 10.
5. **Editing the caller's lists.** `merged.append(iv)` followed by `merged[-1][1] = ...` changes the input in place: after `merge([[1, 3], [2, 4]])` the caller's `[1, 3]` reads `[1, 4]`. Append a fresh `[start, end]`.
6. **Offline answers in the wrong order.** If you sort the queries to sweep them, store each answer under its original query, then rebuild the original order. Returned in sorted order, the queries `[2, 19, 5, 22]` of `min_interval` below get `[2, 4, -1, 6]` instead of `[2, -1, 4, 6]`.
7. **The +1/−1 order at equal times.** For half-open intervals the −1 must come before the +1 at the same time, or back-to-back meetings count as overlapping: `[[1, 5], [5, 9]]` needs 2 rooms instead of 1. Sorting `(time, delta)` tuples does it for free: −1 sorts first.
8. **Adding a strip with the new set.** In a 2-D sweep, as in Rectangle Area II, the area of a union of rectangles, add the strip to the left of x with the *old* active set, then apply the event at x. The other order loses area: on the three rectangles of the example at the end of the section, the last strip `[2, 3]` is measured after `[1, 0, 3, 1]` has switched off, and the area comes out 5 instead of 6.

### Edge cases to say out loud

Empty list · one interval · touching ends (closed vs half-open) · nested intervals · identical intervals · unsorted input · zero-length intervals `[5, 5]` · negative coordinates · inserting before all, after all, or around all. The cell checks the merge and rooms templates against them, and the insert cases come with Insert Interval below.

<!-- cell -->

```python
assert merge([]) == []
assert merge([[5, 5]]) == [[5, 5]]                          # zero length is still an interval
assert merge([[1, 10], [2, 3]]) == [[1, 10]]                # nested: max keeps the 10
assert merge([[8, 9], [1, 3], [2, 4]]) == [[1, 4], [8, 9]]  # unsorted input
assert merge([[1, 2], [1, 2]]) == [[1, 2]]                  # identical
assert merge([[-5, -1], [-2, 0]]) == [[-5, 0]]
assert not overlaps([1, 2], [2, 3]) and overlaps([1, 3], [2, 2.5])
assert min_rooms_heap([]) == 0 and min_rooms_heap([[1, 2]]) == 1
ivs = [[1, 3], [2, 4]]
merge(ivs)
assert ivs == [[1, 3], [2, 4]]                              # the caller's lists are untouched
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Predict `merge([[1, 4], [0, 0]])` before running it: `[[0, 0], [1, 4]]` (they don't touch).
- Rewrite the loop as `for iv in intervals:` with `merged.append(iv)` and `iv[0]`, `iv[1]` inside: the last assert fails, because the caller's `[1, 3]` became `[1, 4]`. `sorted` copied the outer list, not the inner ones.
- What should `min_rooms_heap([[1, 3], [1, 3], [1, 3]])` return? Write the assert first (3).

<!-- cell -->

### Variations

Every variation below changes one of three things: the sort key, what the sweep carries, or whether the input arrives all at once.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Merge** | the template | Merge Intervals (56) |
| **Insert into a sorted, disjoint list** | no sort: copy what ends before, swallow what overlaps, copy the rest | Insert Interval (57) |
| **Keep the most / remove the fewest** | sort by END; keep an interval if it starts at or after the last kept end | Non-overlapping Intervals (435); Minimum Number of Arrows to Burst Balloons (452): the fewest arrows that burst every balloon |
| **How many at once** | the rooms template, or +1/−1 events with ends first at equal times; Car Pooling compares the peak with a capacity | Meeting Rooms II (253); Car Pooling (1094): whether one car of a given capacity can carry every trip |
| **Intersect two sorted lists** | two pointers; the common part is `[max starts, min ends]`; advance whichever ends first | Interval List Intersections (986) |
| **Free gaps** | merge everyone's busy time; the holes between blocks are free | Employee Free Time (759) |
| **Bookings one at a time** | keep accepted bookings sorted; check only the two neighbours with `bisect` | My Calendar I (729) |
| **Covered intervals** | sort by `(start, -end)`; an interval is covered iff its end ≤ the largest end so far | Remove Covered Intervals (1288): how many intervals no other interval contains |
| **Cover a range with the fewest intervals** | jump-game reach, in [Greedy](18_Greedy.ipynb#topic-greedy) | Minimum Number of Taps to Open to Water a Garden (1326): the fewest taps that water a garden `[0, n]` |
| **At least two points in every interval** | sort by end, place points at the right end, in [Greedy](18_Greedy.ipynb#topic-greedy) | Set Intersection Size At Least Two (757): the fewest points that hit every interval twice |
| **Rooms with ids, delayed meetings** | two heaps, free ids and busy ends, in [Heaps](16_Heaps.ipynb#topic-heaps) | Meeting Rooms III (2402): the room that hosts the most meetings |
| *Second pass:* **point queries** | sort the queries offline; push intervals that have started; lazily pop those that ended | Minimum Interval to Include Each Query (1851): the smallest interval holding each query point |
| *Second pass:* **running bookings** | difference map: +1 at start, −1 at end; sweep the sorted keys | My Calendar II (731): no triple bookings; My Calendar III (732) |
| *Second pass:* **area of a union** | sweep x; each strip adds width × union length of the active y-intervals | Rectangle Area II (850) |

The first variation drops the sort. Insert Interval is given a sorted, disjoint list and one new interval, and asks for the list with the new interval merged in: `[[1, 3], [6, 9]]` with `[2, 5]` becomes `[[1, 5], [6, 9]]`. The intervals that touch the new one form a single run.

```text
[1,2]   [3,5]   [6,7]   [8,10]   [12,16]          new = [4,8]
copy    swallow swallow swallow  copy             ->  [1,2] [3,10] [12,16]
```

So the code has three phases and no sort: copy every interval that ends before the new one starts, swallow every interval that starts at or before its end, touching included, and copy the rest. Each interval is looked at once.

<!-- cell -->

```python
def insert(intervals, new):
    out, i, n = [], 0, len(intervals)        # STATE: out = the answer so far; i = next interval to look at
    start, end = new                         # STATE: the new interval, growing as it swallows others
    while i < n and intervals[i][1] < start:     # 1. ends before new starts: copy it untouched
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:      # 2. overlaps (touching counts):
        start = min(start, intervals[i][0])      # STEP: swallow it
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])                     # RECORD: the grown new interval
    return out + intervals[i:]                   # RETURN: 3. the rest starts after new ends


print(insert([[1, 3], [6, 9]], [2, 5]))                              # [[1, 5], [6, 9]]
print(insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))   # [[1, 2], [3, 10], [12, 16]]
```

<!-- cell -->

**Try it**
- Insert at the very end, `insert([[1, 2]], [5, 6])`, at the very front, `insert([[3, 4]], [1, 2])`, and around everything, `insert([[3, 4], [5, 6]], [1, 9])`: phase 2 is empty in the first two calls and swallows both intervals in the third, and the `append` between the loops lands in the right place every time.
- Change phase 1's `<` to `<=` and run `insert([[1, 2]], [2, 3])`: `[[1, 2], [2, 3]]` instead of `[[1, 3]]`. The touching interval was copied instead of swallowed.
- Run `insert([], [4, 8])`: `[[4, 8]]`, with both loops skipped. This is O(n) while `merge` is O(n log n); point at the line that is missing.

<!-- cell -->

The second variation changes the sort key. Non-overlapping Intervals asks for the fewest intervals to remove so that the rest are pairwise disjoint, touching allowed: `[[1, 2], [2, 3], [3, 4], [1, 3]]` removes 1. To fit the most intervals, always keep the one that *ends* first, because it leaves the most room for everything after it.

The proof is an exchange argument, the greedy proof that [Greedy](18_Greedy.ipynb#topic-greedy) spells out: any best answer can swap its first interval for the earliest-ending one without creating a clash, so the greedy never loses. In code, sort by end once, keep an interval when it starts at or after the last kept end, and count every other interval as a removal.

<!-- cell -->

```python
def erase_overlap_intervals(intervals):
    intervals = sorted(intervals, key=lambda iv: iv[1])   # INIT: earliest END first
    kept_end, removed = -math.inf, 0         # STATE: kept_end = end of the last kept interval
    for start, end in intervals:
        if start >= kept_end:                # fits after the last kept one (touching is fine)
            kept_end = end                   # STEP: keep it
        else:
            removed += 1                     # RECORD: it clashes with a kept one that ends no later
    return removed                           # RETURN


print(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))   # 1
print(erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]))           # 2
print(erase_overlap_intervals([[1, 100], [2, 3], [4, 5]]))         # 1
```

<!-- cell -->

**Try it**
- Sort by start instead (`key=lambda iv: iv[0]`) and rerun the last call: 2 instead of 1. `[1, 100]` is kept first and blocks everything.
- Sort by length (`key=lambda iv: iv[1] - iv[0]`) and run `erase_overlap_intervals([[1, 5], [4, 6], [5, 10]])`: 2 instead of 1. The short `[4, 6]` clashes with both of the others.
- Change `>=` to `>`: `erase_overlap_intervals([[1, 2], [2, 3]])` now removes 1 instead of 0, as if touching intervals overlapped.
- Adapt the loop to Minimum Number of Arrows to Burst Balloons (452), where each balloon is a closed interval and one arrow bursts every balloon it passes through: sort by end and shoot a new arrow only when `start > arrow`. `[[10, 16], [2, 8], [1, 6], [7, 12]]` needs 2 arrows, and so does `[[1, 2], [2, 3], [3, 4], [4, 5]]`.

<!-- cell -->

The rooms count has a second form, with no heap at all. The room count is the largest number of meetings running at the same instant, so turn each meeting into two events, +1 at its start and −1 at its end, and keep a running total: `[[0, 30], [5, 10], [15, 20]]` peaks at 2.

```text
meetings [0,30) [5,10) [15,20)
time      0    5   10   15   20   30
event    +1   +1   -1   +1   -1   -1
open      1    2    1    2    1    0          peak = 2 rooms
```

Sort the events as `(time, delta)` tuples, so that at equal times the −1 comes first and a room freed at 5 is free for a meeting that starts at 5. The running total after each event is the number of meetings open, and its peak is the answer.

<!-- cell -->

```python
def min_rooms_sweep(meetings):
    events = sorted([(s, 1) for s, e in meetings] + [(e, -1) for s, e in meetings])   # INIT: (t, -1) before (t, 1)
    open_now = rooms = 0                     # STATE: open_now = meetings running after this event
    for _, delta in events:
        open_now += delta                    # STEP
        rooms = max(rooms, open_now)         # RECORD
    return rooms                             # RETURN


print(min_rooms_sweep([[0, 30], [5, 10], [15, 20]]), min_rooms_sweep([[1, 5], [5, 9]]))   # 2 1
```

<!-- cell -->

**Try it**
- Sort on time only, `sorted(..., key=lambda ev: ev[0])`: `[[1, 5], [5, 9]]` needs 2 rooms. Python's sort is stable, so at time 5 the start (listed first) is now processed before the end.
- Print `events` for the first call and run the totals by hand: 1, 2, 1, 2, 1, 0.
- Compare with the heap on random meetings (`start < end`): the two always agree, because both measure the largest number of meetings open at once.

<!-- cell -->

The two forms answer different follow-ups. The heap knows *which* room frees up next, which Meeting Rooms III needs when it hands each meeting the lowest free room; the sweep is shorter and also works when bookings arrive one at a time, as in My Calendar III below. Car Pooling asks whether a car with a given capacity can serve trips `[passengers, from, to]`, and it is this sweep with the peak compared against the capacity.

Meeting Rooms II promises `start < end`, and the promise matters: with zero-length meetings the two forms disagree, `[[5, 5], [5, 5]]` being 1 for the heap and 0 for the sweep.

Two sorted lists need no sweep line at all, only two fingers. Interval List Intersections asks for the common parts of two sorted, disjoint lists of closed intervals: `[[0, 2], [5, 10]]` and `[[1, 5], [8, 12]]` share `[[1, 2], [5, 5], [8, 10]]`. The current pair meets on `[max of the starts, min of the ends]` when that is non-empty. Then drop the interval that ends first: it can't meet anything later in the other list, because everything there starts even later.

<!-- cell -->

```python
def interval_intersection(A, B):             # 986: both sorted and disjoint, closed ends
    i = j = 0                                # STATE: the current interval of each list
    out = []
    while i < len(A) and j < len(B):
        lo = max(A[i][0], B[j][0])           # the common part starts at the later start
        hi = min(A[i][1], B[j][1])           # ... and ends at the earlier end
        if lo <= hi:                         # RECORD: they meet (touching counts)
            out.append([lo, hi])
        if A[i][1] < B[j][1]:                # STEP: the one that ends first can't meet anything later
            i += 1
        else:
            j += 1
    return out                               # RETURN


print(interval_intersection([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]))
# [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
```

<!-- cell -->

**Try it**
- Change `lo <= hi` to `lo < hi`: `[[1, 2], [8, 10], [15, 23]]`. The single-point intersections `[5, 5]`, `[24, 24]`, `[25, 25]` are lost.
- Advance the pointer that ends *later* (swap `i += 1` and `j += 1`): only `[[1, 2]]` is found. You threw away the interval that could still meet the next one.
- Print `i, j` at the top of the loop: each step moves exactly one pointer, so the loop runs at most `len(A) + len(B)` times.

<!-- cell -->

The merge template also answers questions about what is *not* covered. Employee Free Time gives each employee's sorted busy intervals and asks for the finite gaps when *everyone* is free: `[[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]` gives `[[3, 4]]`. Free time for everyone is what is left after the union of everyone's busy time, so merge all the busy intervals; the holes between consecutive blocks are the answer.

<!-- cell -->

```python
def employee_free_time(schedules):
    busy = merge([iv for person in schedules for iv in person])   # STATE: everyone's busy time, merged
    return [[a[1], b[0]] for a, b in zip(busy, busy[1:])]         # RETURN: the holes between blocks


print(employee_free_time([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]))          # [[3, 4]]
print(employee_free_time([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]))  # [[5, 6], [7, 9]]
```

<!-- cell -->

**Try it**
- Add a person who works `[[3, 4]]` to the first call: the answer becomes `[]`. Touching blocks merge (`<=`), so no zero-length gap can appear.
- Print `busy` for the second call: `[[1, 5], [6, 7], [9, 12]]`, and read the gaps straight off it.
- Each employee's list is already sorted, so rewrite it as a heap k-way merge, one head per employee like `merge_sorted` in [Heaps](16_Heaps.ipynb#topic-heaps): pop the earliest start, record a gap if it starts after the latest end so far, push that employee's next interval. It prints the same answers in O(N log k) instead of O(N log N). On LeetCode the intervals arrive as `Interval` objects, so read `.start` and `.end` there.

<!-- cell -->

When bookings arrive one at a time, the sweep gives way to a sorted list. My Calendar I is a class-shaped question, like those in [Design Problems](00_Topic_Index.ipynb#s24): `book(start, end)` accepts a half-open booking and returns `True` only if it overlaps no accepted booking, so `(10, 20)` is accepted, `(15, 25)` refused and `(20, 30)` accepted. Keep the accepted bookings sorted; then only the two neighbours of the new booking can overlap it, the one just before, if it ends after `start`, and the one just after, if it starts before `end`.

<!-- cell -->

```python
class MyCalendar:                                # 729
    def __init__(self):
        self.starts, self.ends = [], []          # STATE: accepted bookings, sorted and disjoint

    def book(self, start, end):                  # half-open [start, end)
        i = bisect.bisect_right(self.starts, start)          # bookings 0..i-1 start at or before `start`
        if (i > 0 and self.ends[i - 1] > start) or (i < len(self.starts) and self.starts[i] < end):
            return False                         # RETURN: it overlaps a neighbour
        self.starts.insert(i, start)             # STEP: keep both lists sorted
        self.ends.insert(i, end)
        return True                              # RETURN


cal1 = MyCalendar()
print([cal1.book(s, e) for s, e in [(10, 20), (15, 25), (20, 30)]])   # [True, False, True]
```

<!-- cell -->

**Try it**
- Then book `(5, 10)`: `True`. It ends exactly where `(10, 20)` starts, and the ends are half-open.
- Change `self.ends[i - 1] > start` to `>=`: the third booking `(20, 30)` is now rejected (`[True, False, False]`). Touching bookings clash.
- Check only the booking before (drop the second condition): on a fresh calendar holding `(20, 30)`, `book(15, 25)` is accepted, although they overlap.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic. They are offline queries, a difference map and a sweep over rectangles, built from the sweep and the heap of the core.

Minimum Interval to Include Each Query gives intervals `[left, right]` and query points, and asks for the size, `right − left + 1`, of the smallest interval containing each query, or −1: intervals `[[1, 4], [2, 4], [3, 6], [4, 4]]` with queries `[2, 3, 4, 5]` give `[3, 3, 1, 4]`. Answer the queries *offline*, which means all of them are known up front and may be answered in whatever order is convenient, here increasing.

```text
intervals sorted by left: [1,4] [2,4] [3,6] [4,4]          (sizes 4, 3, 4, 1)
q = 2: push [1,4] [2,4]                          top [2,4]  -> 3
q = 3: push [3,6]                                top [2,4]  -> 3
q = 4: push [4,4]                                top [4,4]  -> 1
q = 5: pop [4,4], [2,4], [1,4] (they ended)      top [3,6]  -> 4
```

As the query point moves right, intervals that have *started* join a min-heap keyed by size. Intervals that have *ended* are dead for this and every later query, so they are popped lazily, only when they reach the top. A dict keeps each query's answer, which puts the answers back in the original order at the end.

<!-- cell -->

```python
def min_interval(intervals, queries):
    intervals = sorted(intervals)                # INIT: by left end
    heap, i, best = [], 0, {}                    # STATE: heap = (size, right) of intervals that have started
    for q in sorted(set(queries)):               # offline: queries in increasing order
        while i < len(intervals) and intervals[i][0] <= q:     # every interval that has started by q ...
            left, right = intervals[i]
            heapq.heappush(heap, (right - left + 1, right))    # STEP: ... joins the candidates
            i += 1
        while heap and heap[0][1] < q:           # FIX: lazy deletion, the top ended before q
            heapq.heappop(heap)
        best[q] = heap[0][0] if heap else -1     # RECORD
    return [best[q] for q in queries]            # RETURN: back in the original order


print(min_interval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]))      # [3, 3, 1, 4]
print(min_interval([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]))  # [2, -1, 4, 6]
```

<!-- cell -->

**Try it**
- Change `heap[0][1] < q` to `<=`: the first call gives `[3, 3, 4, 4]`. A query equal to an interval's right end is inside it, so `[4, 4]` must answer q = 4.
- Return `[best[q] for q in sorted(queries)]` instead: the second call gives `[2, 4, -1, 6]`, right numbers in the wrong order.
- Print `heap` after the expiry loop for each query of the second call: at q = 19 everything has ended, the heap is empty, and the answer is −1.

<!-- cell -->

The +1/−1 sweep also works online, one booking at a time. My Calendar III accepts every booking and, after each one, reports the largest number of bookings that overlap at some instant: after `(10, 20)`, `(50, 60)` and `(10, 40)` the answer is 2, and `(5, 15)` makes it 3. The number of events open at time t is the starts at or before t minus the ends at or before t.

So store only the changes, +1 at each start and −1 at each end; sweeping the keys in sorted order and summing rebuilds the count everywhere, and its peak is the answer. That is a difference array from [Prefix Sums](05_Prefix_Sums.ipynb#topic-prefix-sums), a list of changes rather than of values, here on a sparse, unbounded timeline.

Each `book` below sorts the keys, O(n log n). A key list kept sorted with `bisect.insort` makes it O(n), and a lazy segment tree over the coordinate range C makes it O(log C) ([Segment Trees](15_Segment_Trees.ipynb#topic-segment-trees) builds it).

<!-- cell -->

```python
class MyCalendarThree:
    def __init__(self):
        self.delta = defaultdict(int)            # STATE: time -> change in the number of open events

    def book(self, start, end):                  # half-open [start, end)
        self.delta[start] += 1                   # STEP: one more event from start ...
        self.delta[end] -= 1                     # ... until end
        open_now = best = 0
        for t in sorted(self.delta):             # sweep the boundaries left to right
            open_now += self.delta[t]
            best = max(best, open_now)           # RECORD
        return best                              # RETURN


cal = MyCalendarThree()
print([cal.book(s, e) for s, e in [(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)]])
# [1, 1, 2, 3, 3, 3]
```

<!-- cell -->

**Try it**
- On a fresh calendar, book `(1, 5)` and then `(5, 9)`: both return 1. At time 5 the −1 and the +1 land on the same key and cancel, which is the half-open rule.
- Print `sorted(cal.delta.items())` after the six bookings and add the values up by hand: the running sum goes 2, 3, 2, 1, 2, 1, 2, 1, 0, so the peak is 3.
- Turn the class into My Calendar II (731), which rejects a booking that would make a triple booking: add the two deltas, sweep, and if the peak reaches 3, take them back and return `False`. The six bookings above now give `[True, True, True, False, True, True]`.

<!-- cell -->

The last pattern turns the sweep sideways and runs the merge inside it. Rectangle Area II asks for the area covered by the union of axis-aligned rectangles `[x1, y1, x2, y2]`, modulo 10⁹ + 7, with overlaps counted once: `[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]]` covers 6. Python's integers never overflow, so a single modulo at the end is enough.

Area is a sum of thin strips. Sweep a vertical line through the x-edges: between two consecutive edges the set of rectangles the line cuts does not change, so that strip adds its width times the union length of their y-intervals, the merge template in one dimension. In the example the strips `[0, 1]`, `[1, 2]` and `[2, 3]` cover heights 2, 3 and 1, so the area is 6. Measure each strip with the old set, before the event at its right edge switches a rectangle on or off; that is trap 8.

### Say it in the interview

> "Comparing every pair is O(n²). If I sort by start, an interval can only overlap the block I'm currently building, because everything after it starts even later. So I sort once and sweep once, keeping `merged[-1]` as the open block: O(n log n) time, O(n) for the output.
>
> For 'how many rooms', I keep a min-heap of the end times of running meetings: free the ended ones, add the newcomer, and the largest heap size is the answer. Fewer rooms is impossible, because at that moment that many meetings run at once; and it is enough, because a newcomer always finds a room whose meeting has ended."

Say which ends are closed *before* you write the comparison ("touching intervals merge, so `<=`"), and point at the `max` when you stretch: "max, because the next interval may be nested inside the block".

Likely follow-ups and your answers:

- *Do touching intervals overlap?* → ask. Closed ends mean `<=`, half-open ends mean `<`.
- *The list is already sorted, insert one interval?* → three phases, O(n), no sort.
- *Which room does each meeting get?* → a heap of `(end, room)` plus a heap of free room ids (Meeting Rooms III).
- *Bookings arrive one by one?* → sorted starts plus `bisect` (My Calendar I), or the delta map for counts (My Calendar III).
- *Intersect two lists of intervals?* → two pointers; advance the one that ends first.
- *Fewest arrows, or keep the most intervals?* → sort by end.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Employee Free Time | `intervals/employee_free_time.py` | free time = the gaps between merged busy blocks; a heap merges the k sorted schedules in O(N log k) |
| Insert Interval | `intervals/insert_interval.py` | already sorted: copy what ends before, swallow what overlaps, copy the rest; O(n), no sort |
| Meeting Rooms II | `intervals/meeting_rooms_ii.py` · `practice/simple/49_meeting_rooms_ii.py` | sort by start; free ended rooms, push the end, count (or +1/−1 events, ends first); the peak is the answer |
| Merge Intervals | `intervals/merge_intervals.py` · `practice/simple/48_merge_intervals.py` | sort by start; only the last block can overlap; stretch its end with max |
| Minimum Interval to Include Each Query | `intervals/minimum_interval_to_include_each_query.py` | sort the queries offline; push started intervals by size; lazily pop the ended ones |
| My Calendar III | `intervals/my_calendar_iii.py` | difference map, +1 at start and −1 at end; the peak of the running sum is the answer |
| Non-overlapping Intervals | `intervals/non_overlapping_intervals.py` | keep the interval that ends first (exchange argument); count those starting before the kept end |
| Rectangle Area II | `intervals/rectangle_area_ii.py` | sweep x; each strip adds width × union length of the active y-intervals |

### Self-check

1. To keep the most non-overlapping intervals, why sort by *end*, and not by start or by length?
<details><summary>Answer</summary>The interval that ends first leaves the most room for everything after it, and any best answer can swap its first interval for that one without a clash. Start order can grab a long blocker such as <code>[1, 100]</code>. Length order fails too: in <code>[[1, 5], [4, 6], [5, 10]]</code> the shortest, <code>[4, 6]</code>, clashes with both others, while <code>[1, 5]</code> and <code>[5, 10]</code> fit together.</details>

2. In the rooms loop, why must `rooms = max(...)` come after both the freeing loop and the push?
<details><summary>Answer</summary>It reads how many meetings run at this instant. Before the freeing loop, meetings that already ended are still counted (<code>[1, 5]</code>, <code>[5, 9]</code> would need 2 rooms). Before the push, the newcomer is missing (<code>[[1, 5], [2, 6], [3, 7]]</code> would say 2 instead of 3).</details>

3. Write the overlap test for two closed intervals `a` and `b` without any `if`.
<details><summary>Answer</summary><code>a[0] &lt;= b[1] and b[0] &lt;= a[1]</code>. The common part is <code>[max(a[0], b[0]), min(a[1], b[1])]</code>, which is non-empty exactly when the test is true.</details>

4. Why does `merge` compare each interval with `merged[-1]` and not with the interval just before it?
<details><summary>Answer</summary>The block can reach further than the last interval: after <code>[1, 10]</code> and the nested <code>[2, 3]</code>, the previous end is 3 but the block ends at 10. Comparing with the previous interval would split <code>[4, 5]</code> off a block that already covers it.</details>
