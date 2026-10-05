# Heaps

A binary heap is a complete binary tree stored in a flat array, with one rule: every parent is no bigger than its children (min-heap). The tree shape lives in the indices alone: the children of `i` are `2i+1` and `2i+2`, the parent of `i` is `(i-1)//2`, and the last parent is `n//2 - 1`. Because the tree is complete its height is `log n`, and every operation repairs the rule by walking one element along a single root-to-leaf path. The root `heap[0]` is always the minimum; nothing else is sorted.

Python's `heapq` is a min-heap over an ordinary list. There is no max-heap: push `-x` instead, or `(-priority, counter, payload)` when you carry data along.

## Core operations and cost

| Operation | heapq | Cost | How |
|---|---|---|---|
| peek the minimum | `heap[0]` | O(1) | it is the root |
| push | `heappush(h, x)` | O(log n) | append at the end, float up while smaller than the parent |
| pop the minimum | `heappop(h)` | O(log n) | move the LAST element to the root, sink it toward the smaller child |
| build from a list | `heapify(h)` | O(n) | sift down every parent from `n//2 - 1` to 0; cheaper than n pushes |
| push then pop | `heappushpop(h, x)` | O(log n) | returns x itself when x <= root (nothing changes); the size-k pattern |
| pop then push | `heapreplace(h, x)` | O(log n) | returns the old root even when x is smaller |
| k smallest / largest | `nsmallest(k, it)`, `nlargest(k, it)` | O(n log k) | a size-k heap under the hood |
| find or delete an arbitrary value | - | O(n) | heaps do not support lookups; use lazy deletion or a dict on the side |

## Array and tree are the same thing

```
index  0  1  2  3  4  5  6
value  1  2  3  4  9  6  7

              1                level 0: index 0
           /     \
          2       3            level 1: indices 1..2
         / \     / \
        4   9   6   7          level 2: indices 3..6
```

The traces draw this as `1 | 2 3 | 4 9 6 7`: one group per level.

## Drawn example: heapify [9, 4, 7, 1, 2, 6, 3]

```
start           9 | 4 7 | 1 2 6 3      n=7, last parent = 7//2 - 1 = 2
sift index 2    7 vs children 6, 3     3 is smaller and 3 < 7: swap
                9 | 4 3 | 1 2 6 7
sift index 1    4 vs children 1, 2     1 < 4: swap
                9 | 1 3 | 4 2 6 7
sift index 0    9 vs children 1, 3     1 < 9: swap
                1 | 9 3 | 4 2 6 7      9 now at index 1, children 4, 2
                                       2 < 9: swap
                1 | 2 3 | 4 9 6 7      done: every parent <= its children
```

Then `heappop`: take 1, move the last element 7 to the root, sink it: `7 | 2 3 | 4 9 6` -> `2 | 7 3 | 4 9 6` -> `2 | 4 3 | 7 9 6`.

## Two patterns you will use constantly

- **Size-k min-heap for the k largest.** The root is the smallest of the k best, the gatekeeper. A new value gets in only if it beats the root, and the root is what leaves (`heappushpop`). After the stream, `heap[0]` is the k-th largest. Mirror it (max-heap by negation) for the k smallest.
- **Tuples for priority queues.** Push `(-priority, arrival, payload)`. The minus turns the min-heap into a max-heap on priority, the arrival counter makes ties first-in-first-out, and the payload is never compared, so it may be a dict or an object without `__lt__`.

## The invariant to say out loud

"Every parent is no bigger than its children, so the root is the minimum. I only ever disturb one element, and I repair the heap by walking that element along one path: up from the end on push, down toward the smaller child on pop."

## Exercises

| File | Drills |
|---|---|
| `01_heapify_by_hand.py` | Floyd's O(n) build: sift down from the last parent to the root, smaller child, stop when both children are bigger |
| `02_push_and_pop_by_hand.py` | push = append + float up via `(i-1)//2`; pop = last element to the root + sink toward the smaller child |
| `03_top_k_with_size_k_min_heap.py` | the size-k pattern: fill to k, then `heappushpop` only when the new value beats the root |
| `04_max_heap_by_negation_and_tuples.py` | max-heap from a min-heap with `-priority`; `(priority, counter, payload)` so payloads are never compared |
| `05_kth_largest_in_a_stream.py` | LeetCode 703: a class holding a size-k heap, `add` pushes, pops on overflow, answers with `heap[0]` |
| `06_merge_k_sorted_arrays.py` | one candidate per array as `(value, array, position)`; pop the min, push its successor |
