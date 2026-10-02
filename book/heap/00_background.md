# Heaps and Priority Queues

*20 problems · Reading time ~18 min*

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

| Operation | Cost | Why |
|---|---|---|
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
5. **Forgetting to trim to k after building.** After `heapify(nums)`, pop until `len(h) <= k`.
6. **Sorting with `heapq` inside a loop.** `heapify` once, then push and pop; calling `sorted` per step undoes the point.
7. **Mutating an item that is already in the heap.** Its position is now wrong. Push a fresh entry and lazily skip the old.
8. **Lazy deletion without cleaning the top before reading it.** Always pop dead items off the root before `h[0]`.
9. **Negating strings by hand** (`-word` fails). Use a wrapper class or a key that is naturally a number.
10. **Pushing all n items when only k matter.** That is O(n log n) and O(n) memory; cap the heap at k.

## The journey ahead

1. **Kth Largest Element in a Stream** — the size-k min-heap: the weakest member of the top-k club is the answer.
2. **Kth Largest Element in an Array** — same question on static data; quickselect beats the heap and shows when not to use one.
3. **K Closest Points to Origin** — size-k club again, but now the bouncer is the farthest point, so the heap flips to a max-heap by negation.
4. **Top K Frequent Words** — the ordering has two keys and one is a string, so you write the comparison yourself.
5. **Task Scheduler** — the heap stops being a filter and becomes a greedy chooser, paired with a cooldown queue.
6. **Reorganize String** — the same greedy with a cooldown of exactly one, plus a counting argument for when it is impossible.
7. **Rearrange String k Distance Apart** — generalises the parking spot to a queue of length k.
8. **Merge k Sorted Lists** — the heap holds one front item per list: the k-way merge.
9. **Kth Smallest Prime Fraction** — a k-way merge over rows that are never materialised.
10. **Smallest Range Covering Elements from K Lists** — k-way merge plus a running maximum beside the heap.
11. **Design Twitter** — k-way merge inside a design problem, with time stamps as keys.
12. **Find Median from Data Stream** — two heaps holding the lower and upper halves, kept balanced.
13. **IPO** — sort by threshold, push unlocked items into a max-heap, pop the best when you commit.
14. **Minimum Number of Refueling Stops** — unlock-then-choose, but you only commit when you are stuck.
15. **Course Schedule III** — sort by deadline, keep a max-heap of chosen durations and swap out the longest.
16. **Maximum Performance of a Team** — sort by the bottleneck and keep the best k other values in a min-heap.
17. **Minimize Deviation in Array** — normalise every value to its maximum, then repeatedly shrink the top.
18. **Meeting Rooms III** — two heaps (free rooms by id, busy rooms by end time) driven by a sorted sweep.
19. **The Skyline Problem** — sweep line events with a max-heap of heights and lazy deletion.
20. **Trapping Rain Water II** — a min-heap frontier that grows inward from the border, lowest wall first.
