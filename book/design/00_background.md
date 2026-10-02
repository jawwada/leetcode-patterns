# Design: Implement a Tracker

*22 problems · Reading time ~22 min*

## Why this chapter exists

Most interview problems hand you one input and ask for one answer. Design problems hand you a class with a few method names and say: "these calls will arrive in any order, thousands of times, make each one fast." There is no single answer to compute. There is a *state* you keep between calls, and every call either changes that state or reads from it. I call this the "implement a tracker" format, because what you are building is a small object that tracks something — a window of numbers, a set of keys, a history of pages, a cache — and answers questions about it on demand.

The skill being tested is not cleverness with one algorithm. It is the engineering habit of starting from the API, asking what each operation must know, and picking the cheapest structure that knows it. The families in this chapter:

- **Sliding windows over a stream** (moving average, hit counter): keep only what is still inside the window, update a running total by what enters and what leaves.
- **Keyed state** (logger, hash map, underground system): one hash map entry per key holds the single fact that decides future answers.
- **Combined structures** (random set, LRU, LFU, All O`one, max-frequency stack): two structures that each answer a different question, kept in sync by every write.
- **Versioned state** (browser history, time-based store, snapshot array): remember the past and answer "what was true at time t".
- **Lazy work** (bitset, dinner plates, movie rental): defer the expensive part of an update until someone actually looks.
- **Ordered sets of ranges** (disjoint intervals, range module, 2D range sums, majority in subarray): sorted intervals, bisect and Fenwick trees.
- **Building the structure itself** (file system, skiplist): the tracker is a tree or a multi-level list you assemble from nodes.

## What it is

A tracker is a class whose fields are the memory and whose methods are the questions. Draw it as a box with doors:

```text
            calls arrive in any order
   put(k,v)    get(k)     remove(k)    getRandom()
      |          |            |             |
      v          v            v             v
   +----------------------------------------------+
   |  STATE (fields)                              |
   |    structure A  <-- answers question 1       |
   |    structure B  <-- answers question 2       |
   |    small scalars: total, cur, minFreq, ...   |
   +----------------------------------------------+
      |          |            |             |
      v          v            v             v
   None       value        bool          value
```

The method I use on every problem, in this order, out loud:

**1. List the operations with their inputs, outputs and budget.** Write them on the board as a table. The budget is usually stated ("each in O(1) average") or implied by the constraints (10^5 calls means each call must be O(log n) or better). Note any promises: "timestamps are non-decreasing", "every queried route has at least one trip", "keys are ints up to 10^6". Promises are free information.

**2. For each operation, ask what it must know at the moment it is called.** Not how to compute it — what fact it needs. `get(k)` needs "where is k's value". `getRandom()` needs "an element at a uniformly random position". `evict()` needs "which key was least recently used". `getHits(t)` needs "how many stored hits are newer than t - 300".

**3. Pick one structure per question.** Each fact maps to a structure that answers it cheaply: "where is k" is a hash map; "random position" is a dense array; "oldest first" is a queue or a linked list; "smallest" is a heap; "first one at or after x" is a sorted list with bisect.

**4. Combine them, and decide who points at whom.** Two structures holding the same items must be able to find each other's copy in O(1) — usually the hash map stores a pointer or an index into the other structure.

**5. Walk every operation through the combined state and price it.** This is where most designs break: the structure you picked for question 1 makes operation 3 slow. If an operation is over budget, either add a structure that answers its question, or make the answer lazy.

The step people skip is deciding **what to remember and what to forget**. A tracker is only as fast as its memory is small. The moving average forgets values once they slide out; the logger forgets every print except the latest per message; the underground system folds each finished trip into a (sum, count) pair and forgets the trip. Ask of every piece of data: "can any future call's answer depend on this?" If no, drop it now. If yes, ask "in what compressed form?" — a sum instead of a list, a latest timestamp instead of all timestamps, a count instead of the items.

**Talking it through with the interviewer.** Narrate the method, not the code. A good opening sounds like: "There are three operations. `get` needs lookup by key, `put` needs lookup plus knowing who to evict, eviction needs recency order. A dict gives lookup, a doubly linked list gives recency with O(1) moves, so the dict will store list nodes." Then state the costs per operation before writing anything, and invite correction: "Is amortised O(1) acceptable for the resize?" When asked a follow-up ("what if memory is bounded?", "what if timestamps arrive out of order?", "what if this is called from many threads?"), point to exactly which promise it breaks and which structure has to change. That is the conversation they want.

## Operations and what they cost

This is the toolbox: a few parts that combine into nearly every tracker in the chapter.

| Part | Answers | Operation cost | Why |
|---|---|---|---|
| Hash map | "where/what is key k" | O(1) average get/set/delete | address computed from the key |
| Deque (queue) | "oldest / newest item" | O(1) push/pop at both ends | ring buffer with two cursors |
| Hash map + doubly linked list | lookup + order you can rearrange | O(1) lookup, move, unlink | map stores the node, node knows its neighbours |
| Array + index map | membership + uniform random pick | O(1) insert, delete, random | swap victim with last, pop tail |
| Heap (one or two) | "current smallest / largest" | O(log n) push/pop, O(1) peek | sift along one root-to-leaf path |
| Sorted list + bisect | "first item >= x", ranges | O(log n) search, O(n) insert | binary search on order, insert shifts |
| Buckets by count | "any key with count c" | O(1) move between buckets | count is the bucket index |
| Lazy deletion | delete from a heap you cannot search | O(1) mark, cost paid on pop | skip stale entries when they surface |
| Running aggregate | sum, count, max so far | O(1) per update | fold each change in as it happens |

**Hash map + doubly linked list.** The map finds a node in O(1); the node's prev/next pointers let you unlink it and re-insert it at the head in O(1). Sentinels at both ends remove every edge case.

```text
 map: { A:*, B:*, C:* }   each * points at a node below
        |     |     |
        v     v     v
 HEAD <-> [C] <-> [A] <-> [B] <-> TAIL
 most recent                 least recent

 touch(B): unlink B (fix A.next, TAIL.prev), insert after HEAD
 HEAD <-> [B] <-> [C] <-> [A] <-> TAIL
```

**Array + index map.** The array gives positions 0..n-1 with no holes, so a random index is a uniform pick. The map says where each value sits, so deletion never searches. Deleting from the middle copies the last element into the hole.

```text
 vals: [ 5 | 8 | 2 | 9 ]      idx: {5:0, 8:1, 2:2, 9:3}
              ^ remove 8
 copy last into hole:  [ 5 | 9 | 2 | 9 ]  idx[9] = 1
 pop tail:             [ 5 | 9 | 2 ]      del idx[8]
```

**Two heaps.** A max-heap holds the lower half, a min-heap the upper half; the two tops sit either side of the median. Each heap is a triangle in your head and a flat array in memory.

```text
  lower (max-heap)        upper (min-heap)
        5                       7
       / \                     / \
      3   4                   9   8
  array: [5, 3, 4]        array: [7, 9, 8]
  median sits between 5 and 7; sizes differ by <= 1
```

**Sorted list + bisect.** Keep items in order; `bisect` finds a position in O(log n). Versions sorted by time and disjoint intervals sorted by start both live here.

```text
 times:  [ 1 | 4 | 4 | 9 | 12 ]
 bisect_right(times, 5) = 3   -> answer is times[2] = 4
 "latest version at or before t=5"
```

**Buckets.** When the key question is "a key with count c" or "the max count", index by the count itself. Moving a key from count c to c+1 is a removal from one bucket and an add to the next.

```text
 count:  1        2        3
       {d,e}    {b}      {a,c}      maxCount = 3
 inc(b): b leaves bucket 2, joins bucket 3
       {d,e}    { }      {a,c,b}
```

**Lazy deletion.** A heap cannot find an arbitrary entry to remove. So do not remove it: keep the authoritative truth in a map, and when an entry reaches the top, check it against the truth; if stale, pop and discard it.

```text
 heap: [ (2,x) (5,y) (3,z) ]     truth: {x: gone, y: 5, z: 3}
 peek -> (2,x)  x is gone in truth -> pop, discard
 peek -> (3,z)  matches truth      -> real answer
```

## The invariant

Every tracker protects one property: **all the structures describe the same set of items, and every stored scalar equals what you would get by recomputing it from scratch.** If the dict says value 9 is at index 1, then `vals[1]` is 9. If `total` is 18, the queue sums to 18. If the map holds node B, B is linked into the list. Each write must restore this before it returns; each read may assume it.

```text
 LEGAL                              ILLEGAL
 vals: [5, 9, 2]                    vals: [5, 9, 2]
 idx:  {5:0, 9:1, 2:2}              idx:  {5:0, 9:3, 2:2, 8:1}
 every key <-> every slot           9 points past the end;
                                    8 is in idx but not in vals
```

The illegal state above is what you get if `remove(8)` forgets to update the moved element's index and forgets to delete the victim. Nothing crashes immediately; a later `remove(9)` writes into slot 3 and corrupts the array. That is why, for every write, you list every structure and say what changes in each.

## How to picture it

Picture a ledger with several columns that must always agree, and a clerk who answers questions by glancing at exactly one column. Each operation is a transaction: it touches a few rows across columns and leaves the ledger balanced.

```text
  column A (map)   column B (list/array)   scalars
  -------------    ---------------------   -------
  key -> where     items in some order     total=..
  ...              ...                     size=..
         \             /
          one write touches both, then balances
  query: read ONE column, O(1) or O(log n)
```

For windowed problems, overlay a second picture: a bracket sliding right along a timeline, with the clerk only ever writing at the right edge and erasing at the left.

## Signals in a problem statement

- "Implement the `X` class" with several methods: you are in this chapter.
- "Each function must run in O(1) average": you need a hash map plus something that gives the order or randomness the map cannot.
- "stream", "next(val)", "the last k values", "in the past 300 seconds": queue plus running aggregate.
- "timestamps are strictly increasing / non-decreasing": expired data is always a prefix; a queue suffices, and binary search over a list appended in time order works without sorting.
- "least recently used", "evict", "capacity": hash map + doubly linked list.
- "least frequently used", "most frequent", "max frequency": buckets by count.
- "get value at timestamp", "snapshot", "undo", "back/forward": versioned list per key, or array + cursor.
- "getRandom uniformly": dense array + index map.
- "add range / remove range / query range", "merge intervals as they arrive": sorted disjoint intervals with bisect.
- "cheapest / smallest available" with removals: heap with lazy deletion.
- Counter-signals: a single query over a fixed input with no repeated calls is not a design problem; solve it directly. If every operation is only "read", precompute once (prefix sums) instead of building a tracker. If timestamps can arrive out of order, the queue tricks break and you need a sorted structure.

## Python toolbox

```python
from collections import deque, OrderedDict, defaultdict
q = deque(maxlen=3)            # appends evict from the left
q.append(x); q.popleft()       # O(1) both ends; q[0] is oldest

od = OrderedDict()             # dict + linked list built in
od.move_to_end(k)              # O(1) "mark recently used"
od.popitem(last=False)         # O(1) pop the oldest key

import heapq                   # min-heap only, on a plain list
heapq.heappush(h, (-cnt, seq, key))  # max via negation
while h and stale(h[0]):       # lazy deletion
    heapq.heappop(h)

import bisect
i = bisect.bisect_right(times, t) - 1  # last times[i] <= t
bisect.insort(lst, x)          # O(log n) search + O(n) shift

groups = defaultdict(list)     # value -> positions
random.choice(vals)            # O(1) on a list, not on a set
```

Quirks worth knowing: `heapq` compares whole tuples, so a tie on the first field compares the second — put a counter there before anything uncomparable. `random.choice` on a `set` raises a TypeError. `dict` preserves insertion order but cannot move a key to the end in O(1); `OrderedDict` can. `bisect` needs the list already sorted; appending timestamps that only increase keeps it sorted for free.

## Mistakes people make

1. **Updating one structure and forgetting the other.** Fix: for each write method, list every field and say what changes in each before coding.
2. **Swap-with-last when the victim is the last element.** Fix: write the moved element's index first, then delete the victim's key, so the self-swap still ends correct.
3. **Dividing by the capacity during warm-up.** Fix: divide by the current number of items, not the maximum.
4. **Off-by-one window boundaries.** Fix: write the window as a half-open interval, e.g. hits with `t - 300 < ts <= t`, and test exactly at the edge.
5. **Forgetting to evict on reads.** Fix: if a read can happen after time passes with no writes, the read must also evict expired data.
6. **Treating 0 as "missing".** Fix: test `key in d` or compare against a sentinel like -1, never truthiness of the value.
7. **Unbounded memory in a "stream".** Fix: ask what can never matter again and drop it, or merge equal timestamps into (t, count).
8. **Heap ties comparing incomparable objects.** Fix: insert a monotonically increasing counter as the tie-breaker field.
9. **Clamping a cursor to the array length instead of the logical end.** Fix: track the logical end separately whenever "clearing" is done by moving a bound.
10. **Not stating the amortised nature of a cost.** Fix: say "O(1) amortised, one O(n) resize per doubling" out loud before the interviewer asks.

## The journey ahead

1. **Moving Average from Data Stream** — a queue plus a running sum; update by what enters and leaves.
2. **Logger Rate Limiter** — one hash map value per key holding the only fact that matters.
3. **Design Hit Counter** — the window is in time, not count; eviction becomes a loop, same-time hits merge.
4. **Design HashMap** — opens the hash map itself: buckets, chaining, resizing, amortised O(1).
5. **Insert Delete GetRandom O(1)** — the first true combination: array + index map with swap-with-last.
6. **Design Browser History** — array + cursor; "clearing" becomes moving a logical end.
7. **Design Underground System** — two maps with two lifetimes; aggregate into (sum, count).
8. **Time Based Key-Value Store** — keep every version; sorted list per key + bisect.
9. **Snapshot Array** — versioned lists per index, snapshot as a clock tick.
10. **Design Bitset** — lazy global flip flag and a maintained count.
11. **LRU Cache** — hash map + doubly linked list, the canonical combination.
12. **LFU Cache** — LRU lists inside frequency buckets plus a min-frequency pointer.
13. **All O`one Data Structure** — count buckets in a linked list so min and max sit at the ends.
14. **Maximum Frequency Stack** — buckets as stacks with a max pointer; recency comes free.
15. **Dinner Plate Stacks** — list of stacks plus a heap of free slots with lazy invalidation.
16. **Data Stream as Disjoint Intervals** — sorted disjoint intervals, merging neighbours on insert.
17. **Range Module** — the same intervals with range add and remove that split and swallow.
18. **Range Sum Query 2D Mutable** — a 2D Fenwick tree when point updates and range sums interleave.
19. **Online Majority Element in Subarray** — value to positions + bisect, with random sampling.
20. **Design Movie Rental System** — several heap views of the same records, lazy deletion by version.
21. **Design In-Memory File System** — a trie whose edges are path components.
22. **Design Skiplist** — build the ordered structure itself from stacked linked lists.
