# Design: Implement a Tracker

*22 problems · Reading time ~35 min*

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

## Advanced patterns

The parts above carry you through the Easy and Medium problems. Each Hard problem leans on one extra idea: a reason why bookkeeping that looks expensive is O(1), or a way to postpone work until it is free. Here are the seven.

### Count buckets with an extreme that moves by one

**When it shows up.** The question is about frequencies, and you need the least or most frequent key on demand in O(1): "evict the least frequently used", "return a key with the maximal count", "pop the most frequent element, ties to the most recent".

**The intuition.** A heap keyed by count cannot find the key whose count changed. The observation that kills the heap is that each operation changes one key's count by exactly one. So a key only ever moves to an *adjacent* bucket, and the extreme count (the minimum or maximum over all keys) can only change by one step, at a moment you can see happening. In LFU Cache, `min_freq` changes only when a key leaves the bucket `min_freq` and leaves it empty, and then the new minimum is exactly `min_freq + 1`, because the key you just moved is sitting there. In Maximum Frequency Stack, `maxfreq` drops by exactly one when its group empties. In All O`one, where counts go both up and down, the buckets themselves are kept as a sorted doubly linked list of distinct counts, and a new bucket is always spliced in right next to the old one, so the list stays sorted with O(1) local edits and the min and max are simply its two ends. The tie-break lives *inside* the bucket: an ordered dict for recency in LFU, a stack in Maximum Frequency Stack.

```text
 LFU, capacity 3.  before get(3):   min_freq = 1
   freq 1: [3]            freq 2: [1, 4]
                         oldest ^     ^ newest
 get(3): 3 leaves freq 1; it empties and 1 == min_freq
   freq 1: [ ]            freq 2: [1, 4, 3]
   min_freq = 2   (jump by one: 3 is sitting there)
 put(5) when full: evict the oldest in freq 2 -> key 1
```

**Where you'll use it.** LFU Cache, All O`one Data Structure, Maximum Frequency Stack. Beyond: bucket sort in Top K Frequent Elements (347).

### Keep every version and answer "as of t" with a right bisect

**When it shows up.** Queries ask about the past: "the value at timestamp t", "the value at snapshot k", and writes arrive in time order.

**The intuition.** Copying the whole state at every snapshot is O(n) per snapshot and O(n * snaps) memory. Store *changes* instead: each key (or each cell) gets an append-only list of `(time, value)` pairs, one per write. Because the clock only moves forward, appending keeps the list sorted for free, so you never sort and never insert in the middle. The value "as of t" is the last pair with time `<= t`, which is `bisect_right(times, t) - 1`. The clock does not have to be a user's timestamp: in Snapshot Array it is your own counter, the snap id, and `snap()` just increments it. Overwrite the last pair when a cell is written twice in one period, and seed each list with a default pair so the bisect always has something to its left.

```text
 Snapshot Array, cell 2, history as (snap_id, value):
   [ (0,0) (1,7) (3,4) ]        current snap_id = 4
 get(2, snap=2): bisect_right(ids [0,1,3], 2) = 2
                 index 2 - 1 = 1          -> 7
 get(2, snap=3): bisect_right(..., 3) = 3 -> index 2 -> 4
 snap(): returns 4, snap_id becomes 5; nothing is copied
```

**Where you'll use it.** Time Based Key-Value Store, Snapshot Array. Beyond: Online Election (911) precomputes the leader after each vote and answers "leader at time t" with the same right bisect.

### Record the operation, not its effect

**When it shows up.** One operation touches every element ("flip all bits", "add x to everything", "clear all forward history"), but reads only ever look at one element or at an aggregate.

**The intuition.** Do not perform the global operation; store it as a *lens* that every read looks through. In Design Bitset the lens is one flag: the bit a user sees is `physical[i] XOR flipped`, so `flip()` toggles the flag and every logical bit inverts at once. The aggregate you are asked for is maintained by formula instead of recount: after a flip, `ones = size - ones`. The one place this bites is a point write while the lens is on: you must read the *logical* bit first, and if it needs to change, toggle the physical bit, so that it reads correctly through the lens. Browser History uses the same idea in a simpler form: "clear forward history" is not deletion, it is moving a logical end bound, and the old entries are overwritten later for free.

```text
 Bitset, size 5.     logical = physical XOR flipped
   flipped=0  physical 1 0 0 1 0  logical 1 0 0 1 0  ones=2
 flip():   only the flag and the tally change
   flipped=1  physical 1 0 0 1 0  logical 0 1 1 0 1  ones=3
 fix(0):   logical bit 0 is 0 -> toggle physical bit 0
   flipped=1  physical 0 0 0 1 0  logical 1 1 1 0 1  ones=4
```

**Where you'll use it.** Design Bitset, Design Browser History. Beyond: Fancy Sequence (1622) keeps a global "multiply then add" lens and stores each new value pre-divided through it.

### Lazy deletion with a validity test that cannot be fooled

**When it shows up.** You need "the smallest available" (smallest stack with room, cheapest unrented copy) while items keep being removed, changed and returned, in places a heap cannot reach.

**The intuition.** A heap can only hand you its top; it cannot find an arbitrary entry to remove. So keep the truth somewhere else (a map, a list of stacks), push a fresh heap entry whenever something becomes available, and never remove entries when they go stale. Instead, when you look at the top, test it against the truth and pop it if it fails; repeat until the top passes. Each entry is popped at most once, so cleaning is O(log n) amortised. The subtle part is the *test*. "Does the item look available right now?" is not enough when an item can leave and come back: the old entry from its previous stay passes the test again and you report it twice. Either make the test exactly the current fact and tolerate harmless duplicates (Dinner Plate Stacks asks "is this index inside the list and is that stack not full?"), or stamp every entry with a version that is bumped on every change, so a stale entry can never match again (Movie Rental).

```text
 Movie Rental, copy (shop 0, movie 1); entries (price,shop,ver)
   start:   heap [(5,0,v0)]                     ver = 0
   rent:    ver = 1; (5,0,v0) is stale, left in heap
   drop:    ver = 2; push (5,0,v2)
            heap [(5,0,v0) (5,0,v2)]
   search:  top (5,0,v0): v0 != current v2 -> pop, discard
            top (5,0,v2): matches           -> report shop 0
```

**Where you'll use it.** Dinner Plate Stacks, Design Movie Rental System. Beyond: Stock Price Fluctuation (2034) and Sliding Window Median (480) both keep heaps honest the same way.

### Sorted disjoint intervals as a flat list of boundaries

**When it shows up.** The state is a set of covered points that arrives or leaves in chunks: "add range / remove range / is [l, r) fully tracked?", or "summarise the stream as disjoint intervals".

**The intuition.** Keep the intervals sorted, disjoint and merged at all times. Then any new point or range interacts only with a *contiguous* run of intervals, found by binary search, and everything strictly inside the new range is swallowed. Range Module goes one step further and flattens the intervals into one sorted list of boundaries `[l0, r0, l1, r1, ...]`. Now the insertion position of a coordinate tells you where it is: odd means inside a block, even means in a gap. `addRange(l, r)` deletes the boundaries between `i = bisect_left(ends, l)` and `j = bisect_right(ends, r)`, then keeps `l` as a new opener only if `i` is even and `r` as a new closer only if `j` is even. `removeRange` is the mirror image, with odd instead of even. Each boundary is inserted once and deleted once, so the work is amortised over the operations that created it.

```text
 ends:  [10, 14, 16, 20, 30, 40]  blocks [10,14) [16,20) [30,40)
 index:   0   1   2   3   4   5   even = opener, odd = closer
 addRange(12, 18):  i = bisect_left(ends, 12)  = 1  (odd)
                    j = bisect_right(ends, 18) = 3  (odd)
   delete ends[1:3] = [14, 16]; i, j odd -> add nothing
   ends:  [10, 20, 30, 40]           two blocks merged
 removeRange(32, 35): i = j = 3 (both odd) -> insert 32, 35
   ends:  [10, 20, 30, 32, 35, 40]   block [30,40) split
```

**Where you'll use it.** Data Stream as Disjoint Intervals (the point version, using `starts` and `ends` lists and the left and right neighbours), Range Module (the range version). Beyond: My Calendar I/II (729, 731) and Count Integers in Intervals (2276).

### Prefix sums that survive updates: the Fenwick tree

**When it shows up.** Point updates and range-sum queries interleave, both up to about 10^4 to 10^5 times, so neither "recompute the prefix sums" nor "sum the range by scanning" fits.

**The intuition.** A prefix-sum array answers a query in O(1) but an update has to rewrite O(n) entries; a plain array is the other way round. A Fenwick tree sits in the middle. Slot `t[i]` stores the sum of a block that ends at i and reaches back `lowbit(i) = i & -i` cells. Every prefix `[1, k]` is the disjoint union of the blocks you visit by repeatedly stripping the lowest set bit of k, and every index lies in the blocks you visit by repeatedly *adding* its lowest set bit. Both walks have at most log2(n) + 1 steps. In two dimensions you nest the idea, a Fenwick tree whose slots are Fenwick trees, so both operations cost O(log m * log n), and any rectangle is four prefix rectangles combined by inclusion-exclusion. Since the problem's update is "set to v", keep a copy of the matrix and push the delta `v - old`.

```text
 block t[i] covers (i - lowbit(i), i]
 index:   1   2   3   4   5   6   7   8
 t[1]:    [-]
 t[2]:    [-----]
 t[3]:            [-]
 t[4]:    [-------------]
 t[5]:                    [-]
 t[6]:                    [-----]
 t[7]:                            [-]
 t[8]:    [-----------------------------]
 prefix(7) = t[7] + t[6] + t[4]     walk 7 -> 6 -> 4 -> 0
 update(3) touches t[3], t[4], t[8] walk 3 -> 4 -> 8
```

**Where you'll use it.** Range Sum Query 2D - Mutable. Beyond: Range Sum Query - Mutable (307) is the 1D version, and Count of Smaller Numbers After Self (315) uses a Fenwick tree over values.

### Randomness as a design tool

**When it shows up.** A deterministic structure would need heavy machinery (rebalancing, segment trees of candidates), but a random choice has a tiny chance of going badly: "expected O(log n) without a library", "the majority element of any subarray", "return a uniformly random element".

**The intuition.** Both uses put randomness inside the algorithm, so no input can defeat it. *Sample to guess, structure to check*: in Online Majority Element, a value that fills more than half of `[left, right]` is hit by a random position with probability above 1/2, so 20 samples all miss with probability below 2^-20, about one in a million. Each guess is verified exactly with the value's sorted position list and two bisects, so a wrong element is never returned. *Random shape instead of rebalancing*: in Design Skiplist each new node flips coins for its height, so row i holds about n / 2^i nodes, there are about log2 n rows, and a search moves right O(1) expected times per row before dropping down. The coin flips replace rebalancing.

```text
 search(6): move right while next < 6, else drop a row
 row 2: H ================> 4 ----------------> 8
                            |  next 8 >= 6: drop
 row 1: H ------> 2 ------> 4 ------> 6 ------> 8
                            |  next 6 >= 6: drop
 row 0: H -> 1 -> 2 -> 3 -> 4 => 5 -> 6 -> 7 -> 8
                                 ^ next is 6: found
```

**Where you'll use it.** Design Skiplist, Online Majority Element in Subarray, Insert Delete GetRandom O(1). Beyond: Linked List Random Node (382) uses reservoir sampling, the streaming cousin.

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

Each problem adds one new part, or one new reason a part is cheap; the Hard problems combine parts you have already built.

### Warm-up: a stream, a window, a key

**Moving Average from Data Stream.** The naive version keeps every value and sums the last k on each call, O(k) of repeated work for an answer that changes by only two numbers. The new sum is the old sum plus what entered minus what left: a queue for "what leaves next" and one running scalar, and the habit of updating state by the change.

**Logger Rate Limiter.** Now the stream is keyed by message, and the tempting design stores every print time per message. Ask "what is the only fact a future call needs?": one number per message, its next allowed time. It teaches compressing state to the one fact that decides every future answer.

**Design Hit Counter.** Back to a window, but measured in seconds rather than in items, so one call may expire many old hits at once and eviction becomes a while loop. A million hits in the same second should not be a million queue entries, so equal timestamps merge into `(t, count)`.

### Opening the box and the first combinations

**Design HashMap.** Every problem so far trusted a dict to be O(1); here you build one. Buckets, chaining and resizing when the load factor grows explain exactly when that O(1) is an average and when it is amortised.

**Insert Delete GetRandom O(1).** A set gives O(1) insert and delete but no random access; an array gives random access but O(n) delete. The puzzle is to get all three, and the answer is the first real combination: an array of values plus a map from value to index, joined by the swap-with-last delete. From here on, every design is "which two structures, and who points at whom".

**Design Browser History.** The trap is to delete the forward pages on every visit. Instead, keep an array and a cursor, and treat "clear forward history" as moving a logical end bound; stale entries are overwritten later for free. Clearing data becomes a number you change rather than work you do.

**Design Underground System.** Two kinds of state with different lifetimes: a trip in progress (keyed by customer, deleted at check-out) and route statistics (kept forever). How much of a finished trip must you keep? Only `(sum, count)` per route: the logger's lesson applied to aggregates.

### Remembering the past, and doing work lazily

**Time Based Key-Value Store.** For the first time the past matters: `get(key, t)` asks for the value as of time t, so you cannot overwrite. Keeping every version sounds expensive until you notice that timestamps only increase, so appending keeps each key's list sorted and a right bisect answers the query in O(log n).

**Snapshot Array.** Same versioned-list idea, but the obvious design copies the whole array on every `snap()`, which is O(n) per snapshot. Store changes per cell instead, with the snap id as your own clock, and `snap()` becomes a counter increment.

**Design Bitset.** `flip()` touches every bit, and calls may arrive 10^5 times. The puzzle is to make a global operation O(1), and the answer is to record it as a flag that every read looks through, while keeping the count of ones by formula. Browser History moved a bound; this toggles a lens.

### Order on top of a map

**LRU Cache.** The classic: lookup by key and a recency order that changes on every access, both in O(1). An array of keys would need O(n) shifts on every touch; a doubly linked list moves a node in O(1) if something can hand you that node, and the dict does. This is the canonical "map stores a pointer into the second structure" design, with sentinels removing every edge case.

**LFU Cache.** Eviction now asks two nested questions: which count is smallest, and among those keys, which is least recent. The second is an LRU list inside each count bucket; the first looks like it needs a heap, until you see that counts move by one, so `min_freq` only ever jumps to `min_freq + 1` at a moment you can see. This is the first use of the "extreme moves by one" argument.

**All O`one Data Structure.** Counts now go both up and down, and you must report a max and a min key in O(1). The buckets themselves become a sorted doubly linked list of distinct counts, and because a key only moves to an adjacent count, a new bucket is always spliced in next to the old one. The two answers sit at its ends.

**Maximum Frequency Stack.** Pop the most frequent value, ties going to the most recent push, which sounds like LFU with a recency clock. The surprise is that you need no per-key pointers at all: if each frequency level is a stack and a value stays in every lower level it has reached, a pop never has to move anything. Same "max moves by one" argument as LFU, with a far simpler structure.

### The Hard end: lazy heaps, ranges, trees, randomness

**Dinner Plate Stacks.** `push` must find the leftmost stack with room, and scanning is O(n). Room only appears when a plate is popped, at a known index, so a min-heap of candidate indices answers `push`; the twist is that entries go stale when stacks refill or are trimmed away. This is the chapter's first heap with lazy deletion.

**Data Stream as Disjoint Intervals.** Points arrive one by one and you must report the covered set as merged intervals. Keeping the intervals sorted and disjoint means a new point can only touch its two neighbours, found with one bisect, giving five local cases: covered, extend left, extend right, bridge, alone.

**Range Module.** Now whole ranges are added and removed, so one call may swallow many intervals or split one in two. Flattening the intervals into a single sorted list of boundaries turns all three operations into "bisect twice, read parity, replace a slice".

**Range Sum Query 2D - Mutable.** Updates and rectangle sums interleave, so neither a prefix-sum table (slow update) nor a raw matrix (slow query) works. The Fenwick tree splits every prefix into O(log n) power-of-two blocks, and nesting it gives O(log m * log n) for both. Here the part you need is not in the stdlib, so you build it from its invariant.

**Online Majority Element in Subarray.** Each query asks whether some value fills at least a threshold of a subarray, and a full scan per query is too slow. Counting any one value in a range is easy with its sorted position list and two bisects; the hard part is guessing which value to count, and random sampling does that with failure probability below one in a million.

**Design Movie Rental System.** Several ordered views of the same records (cheapest copy of a movie, cheapest rented copies overall) must stay consistent as copies are rented and dropped. Each view is a heap with lazy deletion, as in Dinner Plate Stacks, but a copy can leave and come back, so the naive "is it available?" test reports ghosts. Version stamps on every entry fix that: many views, one truth.

**Design In-Memory File System.** Paths look like strings, but their meaning is "this name inside that parent", so the right index is a tree of dictionaries, a trie whose edges are path components. Every operation is a walk of one lookup per component.

**Design Skiplist.** The last step is to build an ordered structure from scratch without a balanced tree. Sorted linked lists stacked into express lanes, with random coin-flip heights, give expected O(log n) search, insert and erase with no rebalancing. Sentinels from LRU and randomness from the majority problem both come back.
