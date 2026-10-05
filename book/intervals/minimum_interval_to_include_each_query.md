# Minimum Interval to Include Each Query
*LeetCode 1851 · Hard · Pattern: Offline queries sorted + sweep by start + min-heap by size with lazy removal · Reading time ~10 min*

## The problem

Given intervals [left, right] and queries q, answer each query with the size (right - left + 1) of the smallest
interval containing q, or -1 if none does. Answers must be returned in the original query order.

```text
Example: intervals=[[1,4],[2,4],[3,6],[4,4]], queries=[2,3,4,5]
  -> [3,3,1,4].
```

## What the problem is really asking

You have n closed intervals `[left, right]` and m query points. For each query q, find the **shortest** interval that contains it (`left <= q <= right`) and report its size, `right - left + 1`, counting integer points. If no interval contains q, report -1. Answers go back in the **original** query order.

The answer is a list of m integers. Each query alone is easy. The hard part is scale: n and m are both up to 10^5, so testing every interval against every query (10^10 checks) is out. You need the queries to share work.

Running example: `intervals = [[2,3],[2,5],[1,8],[20,25]]`, `queries = [2,19,5,22]`, answer `[2,-1,4,6]`.

```text
[1,8]      [=============]                 size 8
[2,3]        [=]                           size 2
[2,5]        [=====]                       size 4
[20,25]                                          [=========]
         |-+-+-+-+-|-+-+-+-+-|-+-+-+-+-|-+-+-+-+-|-+-+-+-+-|
         0         5         10        15        20        25
             ^     ^                           ^     ^
             q=2   q=5                       q=19   q=22

 q=2  -> inside [1,8],[2,3],[2,5]; shortest [2,3]   -> 2
 q=19 -> inside nothing                             -> -1
 q=5  -> inside [1,8],[2,5]; shortest [2,5]         -> 4
 q=22 -> inside [20,25]                             -> 6
```

## Do it by hand first

Answer the queries on paper. You would not go in the given order 2, 19, 5, 22. You would sweep your pencil left to right across the number line and answer each query as you pass it: 2, then 5, then 19, then 22. Why? Because as the pencil moves right, the set of intervals "under" it changes gradually. Intervals switch on when you pass their left edge and switch off when you pass their right edge.

```text
 pencil at 2:  switched on so far: [1,8] [2,3] [2,5]
               still alive:        all three
               shortest alive:     [2,3] -> 2
 pencil at 5:  switched on so far: same three
               [2,3] died at 3     alive: [1,8] [2,5]
               shortest alive:     [2,5] -> 4
 pencil at 19: [2,5] died, [1,8] died  -> nothing -> -1
 pencil at 22: [20,25] switched on  -> 6
```

What did your hand track? A pool of intervals that had switched on, from which you always wanted the **shortest one that is still alive**. You also kept a note of which original slot each answer belongs in, since you answered out of order.

## The first honest attempt

"For each query, scan all intervals, keep the smallest size among those containing q."

That is O(n * m) time and O(1) extra space. Here is the waste, drawn for queries 2 and 5 in sorted order:

```text
            [1,8]  [2,3]  [2,5]  [20,25]
 q=2 tests:  yes    yes    yes    no
 q=5 tests:  yes    no     yes    no
             ^^^           ^^^
     same intervals re-verified; between 2 and 5 only
     one thing changed: [2,3] ended at 3
```

Neighbouring queries (in sorted order) share almost their entire candidate set. The brute force rediscovers the set from zero every time, and then re-finds its minimum from zero too.

A middle attempt is "sort intervals by size, and for each query take the first one that contains it". That is still O(n) per query in the worst case, because many short intervals may not contain q. The ordering by size helps with "minimum", but not with "contains".

## The turning point

**Claim: if you answer queries in increasing order, the intervals that have started (`left <= q`) only ever grow as a set, so they can be added once each with a moving pointer. The intervals that have ended (`right < q`) only need to be thrown out when they would otherwise be reported, which is exactly when they reach the top of a min-heap.**

This splits "contains q" into its two halves and handles each with a monotone tool.

**Half 1, `left <= q`: a pointer.** Sort intervals by left. Keep an index `i`. For each query (ascending), advance `i` while `intervals[i].left <= q`, pushing each such interval into a candidate pool. Because queries only increase, an interval that started for one query has started for all later ones. The pointer only moves forward, n steps total across all queries.

**Half 2, `right >= q` and smallest size: a heap with lazy deletion.** The pool is a min-heap keyed by `(size, right)`. We want the smallest size among candidates whose `right >= q`. Some candidates in the heap may already be dead (`right < q`). Do we need to remove them all? No. We only ever *read the top*. So before answering, pop the top while it is dead. Once the top is alive, it is the answer, even if dead entries remain lower down. They are harmless because they are not the top, and when one surfaces later, it will be popped then.

```text
 heap as triangle            meaning
       (4,5)                 top: size 4, alive iff 5 >= q
       /                     below: (8,8)
    (8,8)                    entries can be dead anywhere;
 array: [(4,5),(8,8)]        we only pop dead ones that
                             reach the top
```

Why is lazy deletion safe? An entry popped for being dead at q has `right < q`. Every later query is at least q, so it is dead for those too, and removing it is permanent and correct. An entry left in the heap is never returned unless it is at the top *and* passed the alive check. Each interval is pushed once and popped at most once, so the total heap work is O(n log n) no matter how the queries fall.

**Remembering original order.** Sort the query *indices* by value, not the values themselves. Then `ans[idx] = ...` writes each answer back into its slot. This is what "offline" means: you see all the queries up front and may answer them in any order you like.

**Why `(size, right)` as the key?** Size is what we minimise. Right is needed for the alive check, and as a tiebreaker it is harmless.

Watch the comparison operators. Dead means `right < q`. A query sitting exactly on the right endpoint is contained, because the intervals are closed. Size is `right - left + 1`.

## Watch it work

Sorted intervals by left: `[1,8], [2,3], [2,5], [20,25]`. Query order by value: `q=2 (slot 0), q=5 (slot 2), q=19 (slot 1), q=22 (slot 3)`. State: pointer `i`, heap array, `ans`.

**Frame 1.** Set up. Nothing has started yet.

```text
 intervals: [1,8] [2,3] [2,5] [20,25]     i=0
            ^
 queries in order: 2(s0) 5(s2) 19(s1) 22(s3)
 heap = []      ans = [-1, -1, -1, -1]
```

Both streams are sorted, and the sweep will move right through both.

**Frame 2.** q=2 (slot 0). Push every interval with left <= 2: `[1,8]` gives (8,8), `[2,3]` gives (2,3), `[2,5]` gives (4,5). The top is (2,3), and 3 >= 2, so it is alive.

```text
 intervals: [1,8] [2,3] [2,5] [20,25]     i=3
                              ^ (20 > 2, stop)
          (2,3)        heap = [(2,3),(8,8),(4,5)]
          /   \        ans  = [2, -1, -1, -1]
      (8,8)   (4,5)
```

The pointer moved three steps, and it will never revisit them.

**Frame 3.** q=5 (slot 2). Nothing new starts (20 > 5). Top (2,3): 3 < 5, so it is dead. Pop it. New top (4,5): 5 >= 5, so it is alive.

```text
 pop (2,3) dead        heap = [(4,5),(8,8)]
          (4,5)        ans  = [2, -1, 4, -1]
          /
      (8,8)
```

`q == right` counts as inside, which is why the test is `<`.

**Frame 4.** q=19 (slot 1). Nothing new starts. Top (4,5): 5 < 19, so pop it. Top (8,8): 8 < 19, so pop it. The heap is empty, so this answer stays -1.

```text
 pop (4,5), pop (8,8)  heap = []
                       ans  = [2, -1, 4, -1]
 nothing covers 19
```

Two dead entries are cleared in one query. Each costs a pop only once in its life.

**Frame 5.** q=22 (slot 3). Push `[20,25]` as (6,25). The top is alive (25 >= 22).

```text
 intervals: [1,8] [2,3] [2,5] [20,25]     i=4 (done)
          (6,25)       heap = [(6,25)]
                       ans  = [2, -1, 4, 6]
```

The final answer, in original order, is `[2, -1, 4, 6]`. The solution returns the same.

Invariant across frames: after advancing for query q, the heap contained every interval with `left <= q` that had not been popped, everything popped was dead for q and all later queries, and the top after cleanup was the shortest interval containing q.

## Why it is correct

Fix a query q, processed after all smaller queries.

1. **Every interval containing q is either in the heap or was never needed.** An interval with `left <= q` was pushed by the pointer at or before this query. It can have been popped only if it was dead at some earlier query q' <= q, meaning `right < q' <= q`, so it does not contain q. So every interval containing q is still in the heap.
2. **Nothing in the heap with `left > q`.** The pointer stops at the first `left > q`, and intervals are sorted by left.
3. **The top after cleanup is the answer.** Cleanup pops only dead tops, which never contain q. When it stops, the top has `right >= q` and, by fact 2, `left <= q`, so it contains q. It is the minimum `(size, right)` among everything in the heap, a superset of the containing intervals, so its size is the minimum size among them. If the heap empties, no interval contains q, so the answer is -1.

Writing to `ans[idx]` puts each answer in its original slot.

## Cost

- **Time O(n log n + m log m).** Sorting intervals and query indices dominates. Across all queries the pointer advances n times, and each interval is pushed once and popped at most once, so heap work is O(n log n). Each query also does O(1) peeks.
- **Space O(n + m).** The heap holds up to n entries, plus the sorted index list and the answer array.

The brute force is O(n * m). For n = m = 10^5, that is 10^10 against roughly 3.4 * 10^6.

## Variations you will meet

- **Online queries** (you must answer each before seeing the next). Offline sorting is no longer allowed. One approach is a segment tree over compressed coordinates storing the min size per point, built by "range chmin" updates, then point queries.
- **Count of intervals containing each query** instead of the minimum (2251, Number of Flowers in Full Bloom). Simpler: `bisect` the sorted lefts and the sorted rights, and the count is `#left <= q` minus `#right < q`. No heap needed.
- **Largest interval, or the one with the earliest right end.** Change the heap key. The lazy-deletion skeleton is identical.
- **Queries are intervals, not points** ("smallest interval covering [a, b]"). Sort queries by a, push intervals with left <= a, and the alive test becomes `right >= b`. Since b is not monotone in a, lazy deletion is no longer permanent, and you need a different structure.

## What to carry forward

When many questions ask about a point on the line, sort the questions too and sweep both streams together. The "started" condition becomes a forward-only pointer, and the "not yet ended" condition becomes lazy pops off a heap ordered by what you minimise. The next problem, My Calendar III, keeps the sweep but drops the heap: it counts overlap with pure +1/-1 events, and it must rebuild the answer as bookings arrive online.
