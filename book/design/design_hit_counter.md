# Design Hit Counter

*LeetCode 362 · Medium · Pattern: Sliding window queue with running sum · Reading time ~7 min*

## What the problem is really asking

Two methods. `hit(timestamp)` records one event. `getHits(timestamp)` returns how many events happened in the last 300 seconds, meaning with hit time `ts` in the half-open window `(timestamp - 300, timestamp]`. Timestamps never go down, and many hits may share one timestamp.

The answer is an integer, and the object is a counter over a sliding time window. Compared with the moving average, two things change. The window is measured in seconds, not in number of items, so a single call can expire many hits at once — or none. And a read can happen after a long silence, so reads must expire data too.

```text
 hits at:  1  1  2            300
 getHits(301): window is (1, 301]
             x  x  .            .
             1 and 1 are out (1 <= 1), 2 and 300 are in -> 2
```

## Do it by hand first

Write hits on a timeline as tally marks. To answer `getHits(301)`, slide a 300-wide bracket so its right edge sits at 301; its left edge is at 1, exclusive. Count the marks under it.

```text
 timeline: 1   2   ...   300  301
 marks:    ||  |          |
 bracket:     (----------------]
              1               301
 count = 1 (at 2) + 1 (at 300) = 2
```

Now ask again at 302. You would not recount: you would erase the marks that fell off the left edge (the one at 2) and subtract them from your previous total. Your hand kept two things: the marks still under the bracket, in time order so the oldest is easy to find, and the running count. That is a queue plus a total — the moving average's state, with eviction driven by time instead of length.

## The first honest attempt

Append every timestamp to a list. `getHits(t)` scans the whole list and counts entries with `t - 300 < ts <= t`. `hit` is O(1); `getHits` is O(n) over all hits ever recorded; memory grows forever.

```text
 list:  1 1 2 300 302 ... 4800 | 4900 5000 5001 5001
        \_____________________/  \_________________/
         expired long ago:       inside the window:
         rechecked every query   recounted every query
 getHits(5001) scans all of it, from the very first hit
```

The repeated work has two parts: hits that are permanently expired get re-examined on every query, and hits that are known to be inside get re-counted on every query.

## The turning point

**Claim: because timestamps never decrease, the expired hits are always a prefix of arrival order, and once expired they stay expired.**

Justification: the window's left edge `t - 300` only moves right as t grows. A hit with `ts <= t - 300` will satisfy `ts <= t' - 300` for every later `t' >= t`. And since hits arrive in non-decreasing time, all hits older than a given expired hit arrived before it — so the expired set is exactly a run at the front.

So the right structure is a queue: push hits at the back, pop expired ones from the front. Keep `total` equal to the number of hits in the queue, so `getHits` is "evict, then return total". Eviction is now a `while` loop, not a single `if` as in the moving average, because one long gap can expire many hits at once. But every hit is popped at most once over the object's whole life, so the loop's total work is bounded by the number of hits: O(1) amortised per operation.

One more refinement handles bursts. If a million hits share timestamp 5, the queue holds a million identical entries. Collapse them: store `(timestamp, count)` pairs, and when a hit arrives with the same timestamp as the back pair, increment that count. Now the queue holds at most one pair per distinct second inside the window — at most 300 pairs, no matter the traffic. Eviction subtracts a whole pair's count at once.

What the tracker remembers: the in-window hits, grouped by second, and their total. What it forgets: every hit older than 300 seconds, immediately and permanently.

```text
 _evict(t):
   while window and window[0].ts <= t - 300:
       total -= window.popleft().count
```

## Watch it work

Operations: hit(1) hit(1) hit(2) hit(300) getHits(300) getHits(301) getHits(302) hit(302) getHits(601). Queue front on the left.

```text
Frame 1  hit(1), hit(1)
 window: [(1,2)]                 total = 2
```
The second hit at 1 bumps the back pair's count instead of adding a pair.

```text
Frame 2  hit(2), hit(300)
 window: [(1,2) (2,1) (300,1)]   total = 4
 evict threshold 300-300 = 0: nothing <= 0
```
New seconds append new pairs; nothing has expired yet.

```text
Frame 3  getHits(300) -> 4
 window: [(1,2) (2,1) (300,1)]   total = 4
 window is (0, 300]: all four inside
```
Read evicts first, finds nothing, returns the maintained total.

```text
Frame 4  getHits(301) -> 2
 threshold 1: pop (1,2)  total 4 - 2 = 2
 window: [(2,1) (300,1)]         total = 2
```
One pop removes both hits at second 1 at once.

```text
Frame 5  getHits(302) -> 1 ; hit(302)
 threshold 2: pop (2,1)  total = 1
 window: [(300,1)]               -> returns 1
 hit(302):
 window: [(300,1) (302,1)]       total = 2
```
The read expires second 2; the hit then appends a new pair.

```text
Frame 6  getHits(601) -> 1
 threshold 301: pop (300,1)  total = 1
 window: [(302,1)]               total = 1
```
A long gap: the loop pops until the front is newer than 301.

Across all frames, `total` equals the sum of counts in the queue, the queue is sorted by timestamp with distinct seconds, and nothing in it is older than the last eviction threshold.

## Why it is correct

Invariant after every operation at time t: the queue holds, in increasing timestamp order, one pair per distinct second among hits with `ts > t - 300`, and `total` is the sum of their counts. `hit(t)` adds to the back (merging if the second matches), which keeps order because t is at least every stored timestamp; then it evicts. `getHits(t)` evicts: since expired pairs form a prefix (the claim above), popping from the front while the front is expired removes exactly the expired set and nothing else. After that, `total` is exactly the count of hits in `(t - 300, t]`.

## Cost

- **Time:** O(1) amortised per operation — each pair is appended once and popped once; a single call may pop many, but the total over all calls is bounded by the pairs ever created.
- **Space:** O(min(n, 300)) pairs — one per distinct second inside the window, thanks to merging.

Without merging, it is still O(1) amortised, but space is O(hits in the last 300 s), which is unbounded under bursts.

## Variations you will meet

- **Fixed-size circular buffer (the classic follow-up).** Use two arrays of length 300, `times[i]` and `counts[i]`, indexed by `ts % 300`. On a hit, if `times[i] != ts` the slot is stale: overwrite it with count 1. `getHits` sums the 300 slots whose time is within the window. That is O(300) per read but strictly constant memory and no allocation — good for high write rates.
- **Concurrent hits from many threads.** The buffer version shards well; the deque version needs a lock around evict-and-read. Interviewers ask this to see whether you know which state is shared.
- **Out-of-order timestamps.** The "expired is a prefix" claim breaks; use a sorted structure (or a bucketed circular buffer, which does not care about order within the window).
- **Hits per user.** One queue per key in a hash map — the logger and the hit counter combined.

## What to carry forward

When time only moves forward, expired data is a prefix of a queue and each item is evicted once: amortised O(1), and merging equal timestamps bounds memory. The next problem opens up the hash map we have been leaning on, to see why its O(1) is honest.
