# Merge k Sorted Lists

*LeetCode 23 · Hard · Pattern: k-way merge with a heap (merge k sorted feeds) · Reading time ~9 min*

## What the problem is really asking

You are handed `k` singly linked lists, each already sorted ascending. Splice them into one sorted linked list and return its head. Some lists may be empty, and the array of lists may itself be empty.

The answer is a linked list made of the same nodes, in a new order. The input is not random: it is `k` sorted runs. Any solution that ignores that structure is paying for comparisons whose results are already known. The real question is how little work it takes to decide, again and again, which node comes next.

```text
L0:  1 -> 4 -> 5
L1:  1 -> 3 -> 4
L2:  2 -> 6

out: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6
```

Earlier problems in this chapter used the heap to hold a fixed pool of candidates (the k largest so far, the rested letters). Here the pool is a moving frontier: exactly one candidate per list, refilled from the list you just took from.

## Do it by hand first

Lay the three lists out as three face-up decks of cards, smallest card on top. To build the merged pile you never look below the top cards. You compare the three visible tops, take the smallest, and turn over the next card of the deck it came from.

```text
tops:  L0=1  L1=1  L2=2     take 1 (L0)  -> L0 shows 4
tops:  L0=4  L1=1  L2=2     take 1 (L1)  -> L1 shows 3
tops:  L0=4  L1=3  L2=2     take 2 (L2)  -> L2 shows 6
tops:  L0=4  L1=3  L2=6     take 3 (L1)  -> L1 shows 4
...
```

What did your hand keep track of? A set of exactly `k` visible cards, one per non-empty deck, and the ability to grab the smallest of them. After each grab, one card leaves the set and at most one card, from the same deck, joins it. That set is the seed of the data structure.

## The first honest attempt

There are two brute forces a strong candidate mentions.

**Dump and sort.** Walk every list, copy all `N` values into an array, sort, rebuild a list. That is O(N log N). It throws away the sortedness: the sort re-compares 1 against 4 against 5 inside `L0`, which the input already told you.

**Scan the tops.** Keep a pointer per list, and at each step scan all `k` pointers for the minimum. That uses the sortedness, but each of the `N` outputs pays O(k) for the scan, so O(N k) total. Look at what the scans compare:

```text
             L0 L1 L2
step 1 scans: 1  1  2      -> pick L0
step 2 scans: 4  1  2      -> pick L1   only L0 changed
step 3 scans: 4  3  2      -> pick L2   only L1 changed
step 4 scans: 4  3  6      -> pick L1   only L2 changed
       every step re-compares all k tops, though k-1
       of them are the same as last step
```

Between two steps only one of the `k` tops changes. The scan re-learns the order of the other `k - 1` tops from scratch every time. With `k = 10,000` lists that is 9,999 wasted comparisons per output node.

## The turning point

**Claim: the next output node is always one of the current `k` list heads, and after taking it only that one list's head changes.**

The first half is plain sortedness: every node still waiting in list `i` is at least that list's current head, so the overall minimum of everything not yet output is the minimum of the heads. The second half is the waste the scan ignored. We need a structure that holds `k` items, returns the smallest, and lets us replace one item cheaply. That is exactly what a min-heap is for: `pop` and `push` are O(log k), and the minimum is always at index 0.

So the algorithm is:

1. Push `(val, list_index, node)` for the head of every non-empty list. Heapify.
2. Pop the smallest. Append its node to the output tail.
3. If that node has a `next`, push `(next.val, list_index, next)`.
4. Repeat until the heap is empty.

The `list_index` in the tuple is not decoration. When two values tie, Python compares the next field of the tuple. Without an integer there, it would try `ListNode < ListNode` and raise `TypeError`. The index is unique per list and always comparable, so the tuple comparison never reaches the node.

```text
heap entry:  ( val , i , node )
               |     |    '-- payload, never compared
               |     '------- tiebreaker, unique per list
               '------------- priority
```

## Watch it work

Lists `L0 = 1 4 5`, `L1 = 1 3 4`, `L2 = 2 6`. Heap entries are drawn as `value/list`, for example `4/L0`. The `^` under each list marks the node currently sitting in the heap.

Frame 1: seed the heap with the three heads.

```text
L0: 1 4 5    L1: 1 3 4    L2: 2 6
    ^            ^            ^
        1/L0
       /    \
    1/L1    2/L2
array: [1/L0, 1/L1, 2/L2]      out: -
```

The tie between the two 1s is broken by list index, so `1/L0` is the root.

Frame 2: pop `1/L0`, push its successor `4/L0`.

```text
L0: 1 4 5    L1: 1 3 4    L2: 2 6
      ^          ^            ^
        1/L1
       /    \
    2/L2    4/L0
array: [1/L1, 2/L2, 4/L0]      out: 1
```

`L0`'s pointer advanced by one; the other two pointers did not move.

Frame 3: pop `1/L1`, push `3/L1`.

```text
L0: 1 4 5    L1: 1 3 4    L2: 2 6
      ^            ^          ^
        2/L2
       /    \
    4/L0    3/L1
array: [2/L2, 4/L0, 3/L1]      out: 1 1
```

`3/L1` went in at the end of the array. Its parent `2/L2` is smaller, so it did not sift up.

Frame 4: pop `2/L2`, push `6/L2`.

```text
L0: 1 4 5    L1: 1 3 4    L2: 2 6
      ^            ^            ^
        3/L1
       /    \
    4/L0    6/L2
array: [3/L1, 4/L0, 6/L2]      out: 1 1 2
```

The heap still holds exactly one entry per list.

Frame 5: pop `3/L1`, push `4/L1`.

```text
L0: 1 4 5    L1: 1 3 4    L2: 2 6
      ^              ^          ^
        4/L0
       /    \
    6/L2    4/L1
array: [4/L0, 6/L2, 4/L1]      out: 1 1 2 3
```

Two 4s are present; `4/L0` wins the tie because 0 < 1.

Frame 6: pop `4/L0`, push `5/L0`.

```text
        4/L1
       /    \
    6/L2    5/L0
array: [4/L1, 6/L2, 5/L0]      out: 1 1 2 3 4
```

Frame 7: pop `4/L1` (L1 is now empty, nothing pushed), pop `5/L0` (L0 empty), pop `6/L2` (L2 empty).

```text
after 4/L1:  array [5/L0, 6/L2]   out: 1 1 2 3 4 4
after 5/L0:  array [6/L2]         out: ... 4 4 5
after 6/L2:  array [ ]            out: 1 1 2 3 4 4 5 6
```

As lists run dry the heap shrinks, and the loop ends when the heap is empty.

What stayed true in every frame: the heap held exactly one entry for each list that still had nodes, and that entry was the list's first not-yet-output node. The root was therefore the smallest node not yet output. The output was always a sorted prefix of the final answer.

## Why it is correct

**Invariant.** Before each pop: (a) the output so far is sorted and every node in it is less than or equal to every node not yet output; (b) the heap contains, for each list with remaining nodes, exactly its first remaining node.

**Initialisation.** The output is empty, and the heap holds every non-empty list's head, so (a) and (b) hold.

**Step.** By (b) and sortedness of each list, every remaining node is at least the head of its own list, so the heap root is the global minimum of what remains. Appending it keeps (a). Removing it and pushing its `next` (if any) makes the heap again hold the first remaining node of that list. The other lists did not change. So (b) holds.

**Termination.** Every node is pushed once and popped once. When the heap is empty, by (b) no list has remaining nodes, so every node has been output in sorted order.

One detail: the solution reuses the original nodes, so the last node popped is the end of some input list and its `next` is already `None`. The merged list ends cleanly without an explicit cut.

## Cost

- **Time: O(N log k).** Each of the `N` nodes is pushed and popped exactly once, and the heap never holds more than `k` entries. The initial heapify is O(k).
- **Space: O(k)** for the heap. The output reuses the input nodes, so no extra list is built.

Compare the levels. Dump and sort costs O(N log N). Scanning the tops costs O(N k). The heap costs O(N log k), better than both whenever `k` is much smaller than `N` and `k` is more than a handful. A fourth approach, pairwise divide and conquer (merge lists 0+1, 2+3, ..., then repeat), also achieves O(N log k) time with O(1) extra space if done iteratively. It is a good answer when the interviewer asks you to avoid the heap.

## Variations you will meet

- **Merge k sorted arrays** (or "Find K Pairs with Smallest Sums", LeetCode 373). Same heap, but the payload is `(row, col)` instead of a node pointer, and "next" means `col + 1`. That is the template for the next problem.
- **Kth Smallest Element in a Sorted Matrix** (LeetCode 378). Each row is a sorted list. Seed the heap with column 0 and pop `k` times. You stop early rather than merging everything, so the cost is O(k log n).
- **External sort of files too big for memory.** Each sorted chunk on disk is a "list". You keep one buffered record per chunk in the heap and merge onto the output file. It is the same algorithm with I/O in place of pointer moves.
- **Merge without a heap.** Divide and conquer, as above. It is worth knowing because it shows the `log k` comes from the depth of a merge tree, not from heaps specifically.

## What to carry forward

A k-way merge is a heap holding one head per sorted feed: pop the root, refill from that feed only. Put a unique integer between the key and the payload so ties never compare payloads.

The next problem, K-th Smallest Prime Fraction, has no lists in its input at all. The work is to see that the fractions secretly form `n` sorted rows, and then run this same merge for only `k` steps.
