# Heaps and Priority Queues

*20 problems · Reading time ~23 min*

## Why this chapter exists

Many problems never need everything in order. They need one thing, over and over: "what is the smallest (or largest) item
right now?", asked while items keep arriving and leaving. Sorting answers that question once and then goes stale the moment
a new item shows up. A heap answers it forever, at a cost of `log n` per change.

The twenty problems in this chapter fall into a handful of families:

- **Keep the k best.** Hold exactly k items and throw out the weakest whenever a better one arrives (k-th largest in a
  stream, k closest points, top k frequent words).
- **Select without sorting.** When the whole array is already in hand, partitioning beats a heap (k-th largest in an array).
- **Greedy scheduling by count.** Always spend the most plentiful thing next, and park what you just used until it cools
  down (task scheduler, reorganize string, rearrange string k apart).
- **k-way merge.** Many sorted sequences, one global order: the heap holds one "front" item per sequence (merge k lists,
  k-th smallest prime fraction, smallest range, Twitter feed).
- **Two heaps facing each other.** Split the data into a low half and a high half and keep them balanced (median of a
  stream).
- **Unlock, then pick the best unlocked.** Sort by a threshold, sweep, and push everything you have unlocked into a heap;
  pop the best when you must commit (IPO, refueling stops, course schedule III, team performance).
- **Shrink the extreme.** Repeatedly take the current maximum and transform it (minimize deviation).
- **Event simulation and sweeps.** Heaps keyed on time or height (meeting rooms III, the skyline, trapping rain water II).

## What it is

You met the FIFO queue and the deque in the "Queues and Deques" chapter: items leave in arrival order, so the
oldest leaves first. A priority queue keeps that interface (push, pop, peek) but changes the rule: the most urgent item
leaves first. A heap is the usual way to build one.

### The priority queue: the most urgent item leaves first

Picture a hospital emergency room: people are not seen in arrival order; the most urgent patient goes
next, however recently they arrived. That is a **priority queue**: every item carries a priority, and dequeue always
removes the item with the best priority (the smallest key, by convention). Its operations:

- **push(item, key)**: add an item.
- **pop**: remove and return the item with the smallest key.
- **peek**: look at that item without removing it.
- **decrease-key** (the idea): an item already inside becomes more urgent, and the structure must notice.

```text
priority queue (smaller key = more urgent)

push (7,"cut") (2,"stroke") (5,"fracture") (2,"burn")

          +------------------------------+
push ---> | 7 cut  2 stroke  5 fracture  | ---> pop gives
          |      2 burn                  |      a key-2 item,
          +------------------------------+      then the other,
                                                then 5, then 7
```

"Priority queue" names a contract, not a memory layout, which makes it an *abstract* data type. Several layouts honour
it:

| Implementation | push | pop min | peek |
|---|---|---|---|
| unsorted list | O(1): append | O(n): scan for the min | O(n) |
| sorted list (min at the end) | O(n): insert shifts items | O(1): pop from the end | O(1) |
| binary heap | O(log n): sift up | O(log n): sift down | O(1) |

The two list versions each make one operation free by making the other linear. If you push n items and pop n items,
both lists cost O(n^2) in total. The heap refuses that trade: it keeps the items *just ordered enough* for the minimum
to sit on top, and pays O(log n) on both sides. Decrease-key fits the same mould: in a
heap, a smaller key can only need to move up, so one sift-up fixes it in O(log n), provided you know where the item
sits (Python's `heapq` does not track that, which is why we will push a fresh copy and skip the stale one instead).

### The binary heap

A binary heap is a complete binary tree with one rule about values: every parent is no larger than its children (for a
min-heap). "Complete" means every level is full except possibly the last, and the last level fills left to right. That
shape is what lets us throw away the pointers and store the tree in a flat array.

Draw it as a triangle first. Here is a min-heap holding six numbers:

```text
              level 0           1          <- root = minimum
                             /     \
              level 1       3       2
                           / \     /
              level 2     7   4   5     <- filled left to right
```

Now read it off level by level, left to right, and write it into an array. That array is the only thing in memory:

```text
index   0   1   2   3   4   5
      +---+---+---+---+---+---+
heap  | 1 | 3 | 2 | 7 | 4 | 5 |
      +---+---+---+---+---+---+
        ^   ^-----^   ^---------^
      lvl 0  lvl 1      lvl 2
```

No node stores a pointer. The positions of a node's relatives are pure arithmetic on its index `i`:

```text
parent(i) = (i - 1) // 2
left(i)   = 2*i + 1
right(i)  = 2*i + 2

   i=1 (value 3): parent (1-1)//2 = 0   children 3, 4
   i=2 (value 2): parent (2-1)//2 = 0   children 5, 6(none)
   i=4 (value 4): parent (4-1)//2 = 1   children 9, 10(none)

        [0]
       /   \
    [1]     [2]
    / \     / \
  [3] [4] [5] [6]
```

Two facts fall straight out of this layout. First, the minimum is always `heap[0]`, so peeking is free. Second, a complete
tree with n nodes has height `floor(log2 n)`, so any walk from the root to a leaf, or from a leaf up to the root, touches
at most about `log2 n` slots. Every heap operation is one such walk.

Notice what the rule does NOT say. It says nothing about left versus right, and nothing about cousins. In the drawing, 7
sits below 3 while 2, which is smaller than both 3 and 7, sits on the other side. A heap is only partially ordered: each
root-to-leaf path is sorted, and that is all. That weakness is exactly why it is cheap to maintain.

## Operations and what they cost

First the priority-queue baselines, then the heap itself.

| Operation | Cost | Why |
|---|---|---|
| priority queue on an unsorted list: push / pop | O(1) / O(n) | append; scan for the min |
| priority queue on a sorted list: push / pop | O(n) / O(1) | insert shifts items; min is at an end |
| heap decrease-key (position known) | O(log n) | a smaller key only sifts up |
| peek min (`heap[0]`) | O(1) | the root is the minimum by the heap rule |
| push | O(log n) | append at the end, then sift up one path |
| pop min | O(log n) | move the last item to the root, then sift down one path |
| pushpop / replace | O(log n) | one sift instead of two |
| heapify a list | O(n) | most nodes are near the bottom and sift only a short distance |
| find an arbitrary value | O(n) | the heap rule gives no search order across branches |
| delete an arbitrary value | O(n) find + O(log n) fix | so we usually delete lazily instead |
| n pops in a row | O(n log n) | that is heapsort |

**Push = append, then sift up.** Push 0 onto the heap above. It goes into the first free slot (index 6), which keeps the
shape complete, then it swaps with its parent as long as it is smaller than the parent.

```text
Frame 1: append 0 at index 6, parent = (6-1)//2 = 2
            1
          /   \
         3     2         [1, 3, 2, 7, 4, 5, 0]
        / \   / \                           ^ i=6
       7   4 5   0
Frame 2: 0 < parent 2 -> swap; now i=2, parent = 0
            1
          /   \
         3     0         [1, 3, 0, 7, 4, 5, 2]
        / \   / \               ^ i=2
       7   4 5   2
Frame 3: 0 < parent 1 -> swap; i=0 is the root, stop
            0
          /   \
         3     1         [0, 3, 1, 7, 4, 5, 2]
        / \   / \         ^ i=0
       7   4 5   2
```

Only the path 6 -> 2 -> 0 was touched. The subtree under 3 was never looked at.

**Pop = take the root, move the last item up, sift down.** Pop from `[0, 3, 1, 7, 4, 5, 2]`. The root 0 is the answer. To
keep the shape complete, the last item (2) moves into the hole at the root, then it swaps with its smaller child while
that child is smaller than it.

```text
Frame 1: return 0; move last item 2 to the root
            2
          /   \
         3     1         [2, 3, 1, 7, 4, 5]
        / \   /           ^ i=0, children at 1 and 2
       7   4 5
Frame 2: smaller child is 1 (i=2), 1 < 2 -> swap
            1
          /   \
         3     2         [1, 3, 2, 7, 4, 5]
        / \   /                 ^ i=2, children at 5 and 6
       7   4 5
Frame 3: only child is 5 (i=5), 2 < 5 -> stop
         result: [1, 3, 2, 7, 4, 5], heap rule holds
```

Why the smaller child? Because whichever child moves up becomes the parent of the other child. Promoting the smaller one
keeps the rule true for its sibling; promoting the larger one would put a big value above a smaller one.

**Heapify is O(n), not O(n log n).** Turning an arbitrary list into a heap does not push items one at a time. It sifts
down every internal node, starting from the last internal node `n//2 - 1` and walking back to index 0. Take
`[9, 5, 8, 1, 3, 2]`:

```text
start          i=2 (8 vs 2)     i=1 (5 vs 1)     i=0 (9 down)
[9,5,8,1,3,2]  [9,5,2,1,3,8]    [9,1,2,5,3,8]    [1,3,2,5,9,8]

       9               9               9               1
     /   \           /   \           /   \           /   \
    5     8         5     2         1     2         3     2
   / \   /         / \   /         / \   /         / \   /
  1   3 2         1   3 8         5   3 8         5   9 8
```

At i=0 the 9 sank two levels: swap with 1, then swap with 3. The cost argument: half the nodes are leaves and sift zero
levels, a quarter sift at most one level, an eighth at most two, and so on. The sum `n/4*1 + n/8*2 + n/16*3 + ...` is
bounded by n. The few nodes that sink far are the few nodes near the top.

**Lazy deletion.** Removing an item from the middle of a heap means finding it, which is O(n). The standard escape: do not
remove it. Record that it is dead (in a counter or a set), leave it in the heap, and whenever a dead item surfaces at the
root, pop and discard it before answering. Each item is pushed once and discarded once, so the total cost stays
O(n log n). The skyline problem and every "remove by key" heap use this.

## The invariant

Everything rests on one property:

> For every index i > 0, `heap[parent(i)] <= heap[i]`.

From it follows `heap[0]` is the minimum, because every node is reachable from the root by a path of non-decreasing values.
Push and pop each break the property at exactly one spot, and the sift repairs it along one path.

```text
LEGAL min-heap                ILLEGAL (7 above 4)
        1                             1
      /   \                         /   \
     3     2                       7     2
    / \   /                       / \   /
   7   4 5                       3   4 5
[1, 3, 2, 7, 4, 5]            [1, 7, 2, 3, 4, 5]
 every parent <= children      heap[1]=7 > heap[4]=4
```

Note what is legal: 7 and 2 are in "the wrong order" relative to each other if you read the array left to right, and
that is fine. The array of a heap is not sorted, and you must never read `heap[1]` and assume it is the second-smallest.
The second-smallest is one of `heap[1]` or `heap[2]`, and you do not know which without looking at both.

## How to picture it

Picture a triangle with the most urgent item at the apex. Items enter at the bottom right and bubble up until something
above them is more urgent. When the apex leaves, the last item is dropped into the apex position and sinks down the
cheaper side until it rests.

Two refinements of this picture carry you through the chapter:

```text
size-k club (keep the k best)    k-way merge
apex = weakest member            apex = smallest front item

       [weakest]                 list A: 1 -> 4 -> 9
       /       \                 list B: 2 -> 3 -> 8
   [ ... k members ... ]         list C: 5 -> 6
                                 heap holds {1, 2, 5}
newcomer < apex: bounces off     pop 1, push its successor 4
newcomer > apex: replaces apex   heap holds {2, 4, 5}
```

In the first picture the heap is a bouncer: it only ever compares a newcomer with the single worst member. In the second
the heap is a referee: it holds one candidate per sorted source and always knows which source to advance. Both pictures
share the same reason for being fast: the heap never orders what it does not have to.

## Advanced patterns

The size-k club carries you through the Easy and Medium problems. The Hard ones pair the heap with something: a second
heap, a queue, a sort, a sweep, or a moving boundary.

### Two heaps facing each other

**When it shows up**: you need the middle of a changing collection (a median, a percentile split), or the items fall into
two groups with different questions asked of each.

**The intuition**: one heap shows only an extreme, but the median is where two extremes meet: the largest of the
lower half and the smallest of the upper half. So split the data. Keep the lower half in a
max-heap (`small`) and the upper half in a min-heap (`large`), with their roots facing each other across the middle.
Two rules keep the split honest: every item in `small` is `<=` every item in `large`, and the sizes differ by at most one.
A new number goes into `small`, the largest of `small` moves to `large`, and if `large` became bigger, its smallest moves
back. Each step is one push and one pop, so O(log n), and the median is read from the roots in O(1).

```text
stream 5, 15, 1, 3   -> after all four:

     small (max-heap)          large (min-heap)
     lower half                upper half
        [3]   <- root   |   root ->  [5]
        /               |            /
      [1]               |         [15]

 small = {1, 3}  |  large = {5, 15}
 sizes equal -> median = (3 + 5) / 2 = 4.0
```

The "two heaps, two jobs" shape also appears without a median: in Meeting Rooms III free rooms (by number) and busy
rooms (by end time) move between two heaps.

**Where you'll use it**: Find Median from Data Stream; Meeting Rooms III. Beyond the chapter: Sliding Window Median
(LeetCode 480), which adds lazy deletion to the two heaps.

### k-way merge over a frontier, with the other extreme on the side

**When it shows up**: several sorted sequences (stored or merely implied by a formula) and you want the global order, the
k-th item overall, or a window that touches every sequence.

**The intuition**: the next item overall must be some sequence's front, since everything behind a front is larger. So
the heap holds only the fronts, one per sequence. Pop the smallest front and push
its successor; the heap size stays at k, so every step is O(log k). Two refinements make the Hard versions work. First,
the sequences do not have to exist: in Kth Smallest Prime Fraction each row `arr[i] / arr[j]` is sorted by construction,
and its "successor" is computed on the fly, so the grid is never built. Second, the heap gives you only the minimum, but
some problems need the maximum of the fronts too. Keep that maximum in a plain variable beside the heap: fronts only
ever move forward, so the maximum only ever grows, and one `max(...)` per push maintains it.

```text
Smallest Range, lists:
  L0: 4 10 15 24 26     L1: 0 9 12 20     L2: 5 18 22 30

frontier after 8 pops:   L0 -> 24   L1 -> 20   L2 -> 22
heap of fronts = {20, 22, 24}     cur_max (on the side) = 24

pop 20 (from L1): range [20, 24], width 4 -> best so far
L1 is now exhausted -> no range can cover L1 any more, stop
answer [20, 24]
```

Minimize Deviation runs the mirror image: a max-heap holds every value, a plain variable holds the minimum, and each step
shrinks the maximum (halving an even top) while the minimum can only be lowered by the newcomer.

**Where you'll use it**: Merge k Sorted Lists; Kth Smallest Prime Fraction; Smallest Range Covering Elements from K
Lists; Design Twitter; Minimize Deviation in Array. Beyond: Find K Pairs with Smallest Sums (LeetCode 373).

### Greedy chooser plus a cooldown queue

**When it shows up**: you must emit items one at a time, always preferring the most plentiful, but an item just used may
not be used again for a fixed number of steps ("cooldown n", "no two adjacent equal", "at least k apart").

**The intuition**: "most plentiful first" is a priority rule, so it wants a max-heap of counts. "Wait k steps" is an
arrival-order rule (used first, usable first), which is FIFO, so it wants a deque: the plain FIFO queue from the
Queues chapter. Combine them: pop the top count, use it, decrement, and park it at the back of the queue
stamped with the time it becomes legal again. Each step, if the item at the front of the queue is ready, it goes back into the heap. A shared cooldown keeps the queue sorted by ready time for free, so no second heap is needed.

```text
tasks A A A B B C, cooldown n = 2  (count, ready-after time)

t  run   heap (count)      cooldown queue (front first)
1   A    B:2  C:1          A:2 ready after t=3
2   B    C:1               A:2 @3   B:1 @4
3   C    A:2 (back in)     B:1 @4
4   A    B:1 (back in)     A:1 @6
5   B    -                 A:1 @6
6   _    A:1 (back in)     -           <- idle: heap was empty
7   A    -                 -           total 7: A B C A B _ A
```

**Where you'll use it**: Task Scheduler; Reorganize String (cooldown of one, so the "queue" is a single parked item);
Rearrange String k Distance Apart (cooldown queue of length k, and failure when the heap empties while items still wait).

### Unlock along one key, choose by another

**When it shows up**: each item has two attributes that play different roles: one decides *whether* you may take it (a
capital threshold, an efficiency floor, a position you must reach), the other decides *how good* it is (profit, speed).

**The intuition**: sort by the gatekeeping key and sweep a pointer along it. Every item the pointer passes stays
available forever, so it goes into a heap ordered by the value key. When you must commit,
the heap's top is the best item you are currently allowed to take. The sort makes "allowed" a growing prefix; the heap
answers "best of that prefix" in O(log n). In Maximum Performance of a Team the sweep goes
by efficiency from high to low, so the current item is the bottleneck of any team built so far, and a size-k min-heap of
speeds keeps the k fastest teammates available.

```text
IPO: k = 2, w = 0, projects (capital, profit) sorted by capital:
     (0,1)  (1,2)  (1,3)

round 1: w=0, pointer unlocks (0,1)
         max-heap of profits = {1}        take 1 -> w = 1
round 2: w=1, pointer unlocks (1,2) (1,3)
         max-heap of profits = {2, 3}     take 3 -> w = 4

       sorted by capital  -->  pointer only moves right
       [ (0,1) | (1,2) (1,3) ]
                ^ after round 1        answer: w = 4
```

**Where you'll use it**: IPO; Maximum Performance of a Team; Minimum Number of Refueling Stops (stations unlock by
position). Beyond: Maximum Number of Events That Can Be Attended (LeetCode 1353).

### The regret heap: commit now, undo the worst later

**When it shows up**: you must decide on each item as it arrives, a later item may reveal that an earlier decision was
wasteful, and every decision costs the same one unit of the answer (one stop, one course).

**The intuition**: say yes optimistically and keep your choices in a max-heap ordered by how much they cost. When the plan breaks (the deadline is overshot, the car is stranded), the cheapest repair
is to undo the single most expensive choice, which is the heap's top. Since every choice counts as one, swapping an
expensive one for a cheaper one never lowers the count and always frees the most room. Refueling Stops runs it the other
way round: you drive past stations without stopping, keep their fuel in a max-heap, and only when you are stuck do you
"retroactively" stop at the biggest station you passed. Both are exchange arguments: any optimal plan can be swapped,
one choice at a time, into the greedy one.

```text
Course Schedule III: courses (duration, deadline) by deadline
  (5,5) (4,6) (2,6)

take (5,5): time 5 <= 5  ok        heap {5}
take (4,6): time 9 >  6  broken!   heap {5, 4}
   regret the longest: drop 5 -> time 4     heap {4}
take (2,6): time 6 <= 6  ok        heap {4, 2}
answer: 2 courses (the 5-day course was the wrong bet)
```

**Where you'll use it**: Course Schedule III; Minimum Number of Refueling Stops. Beyond: Furthest Building You Can Reach
(LeetCode 1642), where ladders are spent first and the smallest climb is regretted into bricks.

### Event sweep with a heap of active items and lazy deletion

**When it shows up**: things start and end along a line (time, x-coordinate), and at each event you need the best of the
items that are currently active (tallest building, earliest-freeing room).

**The intuition**: sort the start and end events and walk them left to right. A start pushes its item; an end should
remove it, but deleting from a heap's middle is O(n). Since you only ever read the top, a buried dead item is harmless. Store each item's end with it, and before
reading the top, pop while the top's end has passed. Every item is pushed once and popped at most once, so the sweep is
O(n log n) total, however long dead items sit buried.

```text
Skyline: buildings [left, right, height]
  [2,9,10]  [3,7,15]  [5,12,12]

event x=7, heap (height, end) before cleaning:
   top -> (15, end 7)   dead: 7 <= 7, pop it
          (12, end 12)  alive -> new top, outline = 12
          (10, end 9)   alive, buried
          (0,  end inf) sentinel
event x=9: (10, end 9) dies, but it is buried under 12:
           nothing to do, outline stays 12
event x=12: pop (12,12), then (10,9); top = sentinel 0
outline: [2,10] [3,15] [7,12] [12,0]
```

**Where you'll use it**: The Skyline Problem (max-heap of heights, lazy deletion); Meeting Rooms III (min-heap of busy
rooms by end time, released as the sweep passes them). Beyond: Sliding Window Median (LeetCode 480).

### Pop the cheapest boundary: Dijkstra's shape

**When it shows up**: something spreads from a boundary inward (water, cost, time), and the value of a cell depends on
the cheapest route to the boundary, measured by a maximum or a sum along the route.

**The intuition**: keep the current boundary of the explored region in a min-heap. The lowest boundary cell is the
weakest point of the whole dam: nothing inside can drain out through anything lower. So pop it, and settle each
unvisited neighbour for good, at level `max(popped level, neighbour height)`; then that neighbour joins the boundary.
Settling a cell behind a higher wall first could miss a cheaper escape through the lower one. It is Dijkstra's algorithm, with "path cost" replaced by "highest wall on the way
out".

```text
Trapping Rain Water II
  heights          boundary in heap: all 3s and the 2
   3 3 3
   3 1 3           pop 2 (row 2, col 1): lowest dam cell
   3 2 3           its neighbour 1 -> level max(2, 1) = 2
                   water there = 2 - 1 = 1; push level 2
                   the 3s pop next, nothing left to settle
  answer: 1        (the water leaks out over the 2)
```

**Where you'll use it**: Trapping Rain Water II. Beyond: Swim in Rising Water (LeetCode 778) and Path With Minimum
Effort (LeetCode 1631), both "minimise the maximum along a path" with the same heap.

## Signals in a problem statement

Point here:

- "k-th largest", "k-th smallest", "top k", "k closest", "k most frequent".
- "stream", "add a number then report", "after each insertion" (the data never stops, so a one-time sort is useless).
- "merge k sorted ...", "k sorted lists", "smallest element across several sorted rows".
- "median" of a changing collection (two heaps).
- "at each step choose the largest / cheapest / earliest available" (greedy with a priority queue).
- "cooldown", "no two adjacent equal", "at least n apart" with counts (most-frequent-first plus parking).
- "rooms", "servers", "machines" that become free at times (heap keyed on end time).
- "maximum profit with limited picks after unlocking", "at most k projects", "minimum number of stops".
- A 2D grid where water, fire, or cost spreads from the border by lowest value first (Dijkstra-like heap frontier).

Point elsewhere:

- "contiguous subarray" with a window: a monotonic deque or sliding window is usually O(n), better than a heap's O(n log k).
- The whole input is static and you need only one k-th element: quickselect is O(n) average.
- Values are small integers (counts up to n, letters): bucket sort or counting beats a heap.
- "next greater element", "span", histogram areas: monotonic stack, not a heap.
- You need both ends and arbitrary deletion with order: a sorted container or a balanced tree.

## Python toolbox

`heapq` works on a plain list and is a **min-heap only**. Three quirks drive almost every bug.

Tuples compare lexicographically, so the first field is the priority and later fields break ties:

```python
import heapq
h = []
heapq.heappush(h, (dist, idx, point))  # tie on dist -> idx
d, i, p = heapq.heappop(h)              # smallest dist first
```

Put a unique counter before any field that cannot be compared (dicts, ListNode objects), or the tie-break crashes.

There is no max-heap. Negate numbers to flip the order, and negate back when you read:

```python
heapq.heappush(h, -count)       # largest count -> smallest key
biggest = -h[0]
```

You cannot negate a string. When ties must break on a string in reverse order, write a tiny class with `__lt__`.

Building, combined operations, and lazy deletion:

```python
heapq.heapify(nums)                # in place, O(n)
heapq.heappushpop(h, x)            # push then pop, one sift
heapq.heapreplace(h, x)            # pop then push, one sift
heapq.nlargest(k, nums)            # fine for one-off use
dead = Counter()                   # lazy deletion ledger
while h and dead[h[0]]:
    dead[heapq.heappop(h)] -= 1
```

Helpers you will pair with heaps: `collections.Counter` for frequencies, `collections.deque` for cooldown queues,
`sorted(..., key=...)` for the threshold sweeps.

## Mistakes people make

1. **Using a min-heap when you meant a max-heap.** Push `-x`, and remember to negate again when you read `h[0]` or pop.
2. **Reading `heap[1]` as the second smallest.** Only `heap[0]` has meaning; pop to get the next one.
3. **Tuples whose tie-break field is not comparable.** Insert a counter: `(priority, seq, obj)`.
4. **Keeping a max-heap for "k largest".** The bouncer of the k largest is the smallest of them, so use a min-heap of size k.
5. **Sorting with `heapq` inside a loop.** `heapify` once, then push and pop; calling `sorted` per step undoes the point.
6. **Mutating an item that is already in the heap.** Its position is now wrong. Push a fresh entry and lazily skip the old.
7. **Lazy deletion without cleaning the top before reading it.** Always pop dead items off the root before `h[0]`.
8. **Negating strings by hand** (`-word` fails). Use a wrapper class or a key that is naturally a number.
9. **Pushing all n items when only k matter.** That is O(n log n) and O(n) memory; cap the heap at k (and if you
   did `heapify` everything, pop until `len(h) <= k`).

## The journey ahead

The problems climb from the heap as a filter, through the heap as a chooser and a merger, to the Hard end, where the heap
is one part of a larger machine.

### Warm-up: the size-k club

**Kth Largest Element in a Stream.** Numbers keep arriving; after each, name the k-th largest. Re-sorting
every time is the obvious waste. The insight is that only k numbers matter and the answer is the *weakest* of them, so
the tool is a min-heap of size k, not a max-heap.

**Kth Largest Element in an Array.** The same question on a static array. Does the heap still win? No: quickselect
partitions around a pivot and discards the half that cannot hold the answer, O(n) on average. The lesson is the
counter-signal: a heap earns its keep when data streams or changes.

**K Closest Points to Origin.** Back to the size-k club, but "closest" means the *smallest* k distances, so the bouncer
is now the farthest kept point and the heap must flip to a max-heap. With `heapq` that means negating the distance. It
also shows that you can compare squared distances and skip the square root, since the order does not change.

**Top K Frequent Words.** The ranking now has two keys: higher count, then the alphabetically smaller word.
You cannot negate a string, yet the size-k min-heap needs reverse string order at its root, so you write the comparison
yourself and test the tie-break on a tiny example.

### The heap as a greedy chooser

**Task Scheduler.** Tasks with a cooldown between repeats: what is the shortest schedule? Running whatever is
available strands the most frequent task at the end, separated by idle gaps. The new idea is "most remaining first" from
a max-heap, paired with a FIFO cooldown queue: the chapter's two queues working together.

**Reorganize String.** No two neighbours may be equal: Task Scheduler with a cooldown of one, so the queue
shrinks to one parked letter. New is a counting test for impossibility: a letter occurring more than `(n + 1) // 2`
times cannot be separated.

**Rearrange String k Distance Apart.** Equal letters must be k apart, so the parked letter becomes a real queue of
length k. Failure now shows up inside the greedy: the heap runs dry while letters still wait in the queue.

### Merging many sorted sources

**Merge k Sorted Lists.** Merging k lists pairwise is slow. The k-way merge keeps one front node per list in a min-heap,
for O(N log k). The practical lesson: `ListNode` objects do not compare, so the tuple needs a counter in the middle.

**Kth Smallest Prime Fraction.** The fractions `arr[i] / arr[j]` form a grid of sorted rows, but building it costs n
squared. The new idea: merge rows that exist only as a formula, with index pairs in the heap and successors computed on
demand.

**Smallest Range Covering Elements from K Lists.** The narrowest interval touching every list needs both the smallest
and the largest front, and a heap gives only one. Keep the maximum in a variable beside the heap (fronts only move
forward), and stop when the first list runs out.

**Design Twitter.** The k-way merge moves inside a class: a feed is the ten newest tweets across followees, each a
sorted source keyed by time stamp. The puzzle is choosing per-user structures so posting is O(1) and the merge touches
only ten tweets.

### Two heaps

**Find Median from Data Stream.** The median sits where no single heap looks. Two heaps face each other, lower
half in a max-heap, upper half in a min-heap. The new skill is keeping a two-part invariant (order across, sizes within
one) with a fixed push-pop-rebalance routine instead of special cases.

### Unlock, choose, regret

**IPO.** At most k projects, each gated by a minimum capital. Sorting by profit stalls on projects you cannot afford.
Instead sort by the gate, sweep a pointer that unlocks projects as capital grows, and pick from a max-heap of unlocked
profits.

**Minimum Number of Refueling Stops.** Unlock-then-choose with a twist in timing: never decide at a station. Drive
past, remember its fuel in a max-heap, and only when stranded "go back in time" to the biggest tank you passed: the first
regret-style greedy.

**Course Schedule III.** Sorting by deadline is natural, but a long course taken early can block several short ones.
The regret heap fixes it: take every course, and when a deadline breaks, drop the longest so far, which frees the most
time for the same cost of one course.

**Maximum Performance of a Team.** Sum of speeds times minimum efficiency: two attributes pull against each other.
Sort by efficiency descending so the current engineer is the bottleneck, and keep the k fastest so far in a size-k
min-heap: the warm-up club, now driven by a sort.

### The Hard end: extremes, sweeps and frontiers

**Minimize Deviation in Array.** Odd numbers may double, even ones may halve, and moves in two directions make the
search feel huge. Normalise first (double every odd) so values only go down, then keep halving the heap's maximum while
tracking the minimum on the side: the mirror of Smallest Range.

**Meeting Rooms III.** Each meeting takes the lowest free room or waits for the earliest-freeing one; minute-by-minute
simulation is too slow. Two heaps (free rooms by number, busy rooms by end time) plus a time-sorted sweep combine the
two-heaps idea with an event sweep.

**The Skyline Problem.** The outline changes only at building edges, so sweep them and ask for the tallest standing
building. An ending building must leave a max-heap from the middle; lazy deletion leaves it there until it surfaces.

**Trapping Rain Water II.** In 2D, a cell's water depends on the lowest wall along its best escape route, so the 1D
two-pointer trick fails. A min-heap holds the explored region's boundary and breaches the lowest point first: Dijkstra in
disguise, and the bridge to the graphs chapter.
