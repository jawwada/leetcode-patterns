# Merge Two Sorted Lists

*LeetCode 21 · Easy · Pattern: Dummy head + two-pointer merge · Reading time ~6 min*

## What the problem is really asking

You hold two chains, each already in ascending order. Produce one ascending chain that contains every node from both, by
re-linking the nodes you were given rather than making new ones. The answer is the head of the combined chain.

The interesting part is that the output has no first node yet when you start, and you do not know which input it will
come from. Every append is "attach to the end of the output", but at the start there is no end.

```text
l1:  [1] -> [4]
l2:  [2] -> [3] -> [5]

out: [1] -> [2] -> [3] -> [4] -> [5]
      l1     l2     l2     l1     l2    (where each came from)
```

## Do it by hand first

Put two sorted piles of cards face up. To merge them you look at the two top cards, take the smaller, and place it on the
output pile. Repeat. When one pile runs out, you drop the whole other pile on top, since it is already in order.

```text
 tops: 1 vs 2 -> take 1      tops: 4 vs 2 -> take 2
 tops: 4 vs 3 -> take 3      tops: 4 vs 5 -> take 4
 l1 empty -> append the rest of l2: [5]
```

Your hand tracked three things: the top of each pile, and where the output pile ends. That is `l1`, `l2`, and `tail`.

## The first honest attempt

Gather every value from both lists into a Python list, sort it, and build a fresh chain. O((m+n) log(m+n)) time and
O(m+n) space.

The waste is the sort. Sorting starts from scratch, as if the values had no order, but each input is already sorted.
The only unknown is how the two sequences interleave:

```text
sort sees:   1 4 2 3 5          (order thrown away)
truth:       1 4 | 2 3 5        (two runs already sorted)
             only the interleaving is missing
```

It also allocates m+n new nodes when the problem gave you exactly the nodes you need.

## The turning point

**Claim: the smallest node not yet placed is always at the head of `l1` or the head of `l2`.**

Each list is sorted, so its head is its smallest remaining node. The overall smallest remaining is the smaller of the two
heads. One comparison picks the next output node, and we never need to look deeper than the fronts.

To turn this into code we need an output chain we can append to. Keep a `tail` reference on its last node; appending is
`tail.next = chosen` then `tail = tail.next`. The only problem is the very first append, when there is no last node.
Instead of an `if` for that case, create a **dummy** node and start `tail` there. The real merged list will hang off
`dummy.next`. Every append, including the first, now looks the same.

```text
 [D]            tail = D, empty output
 [D] -> [1]     after first append, tail = [1]
 answer = D.next
```

When one input runs out, the other is already sorted and every node in it is at least as large as everything placed so
far, so one assignment attaches all of it: `tail.next = l1 or l2`.

## Watch it work

`l1 = 1 -> 4`, `l2 = 2 -> 3 -> 5`. `out` shows the output chain from `D` up to `tail`.

```text
Frame 1: start
 out: [D]                       l1: [1] -> [4]
      tail                      l2: [2] -> [3] -> [5]
```

The dummy is the whole output; `tail` sits on it.

```text
Frame 2: 1 <= 2, take l1's head
 out: [D] -> [1]                l1: [4]
             tail               l2: [2] -> [3] -> [5]
```

`D.next = [1]`, `l1` advanced. Node 1 still points at 4 in memory, but the next append will overwrite that arrow.

```text
Frame 3: 4 > 2, take l2's head
 out: [D] -> [1] -> [2]         l1: [4]
                    tail        l2: [3] -> [5]
```

`[1].next` was rewritten from 4 to 2; `tail` moved to 2.

```text
Frame 4: 4 > 3, take l2's head
 out: [D] -> [1] -> [2] -> [3]  l1: [4]
                           tail l2: [5]
```

Again l2 wins; node 2 already pointed at 3, so this write changed nothing visible.

```text
Frame 5: 4 <= 5, take l1's head
 out: D -> 1 -> 2 -> 3 -> [4]   l1: None
                         tail   l2: [5]
```

`l1` is exhausted, so the loop ends.

```text
Frame 6: tail.next = l1 or l2  ->  [5]
 out: D -> 1 -> 2 -> 3 -> 4 -> [5] -> None
 return D.next = [1]
```

The leftover chain is attached in one write and the answer starts after the dummy.

Across all frames, the chain from `D.next` to `tail` was sorted and contained exactly the nodes taken so far, and every
remaining node was at least as large as `tail`.

## Why it is correct

Invariant before each comparison: the output chain `D.next ... tail` holds the k smallest nodes overall, in order, and
`l1`, `l2` head the remaining nodes of each input, still sorted.

Each step appends the smaller head. Because both remainders are sorted, that head is the smallest of all remaining nodes,
so the output grows to the k+1 smallest, still in order. When one remainder is empty, the other is sorted and every node
in it is at least the current `tail` value, so attaching it whole keeps the order. Every node is placed exactly once.

## Cost

- Time: O(m + n), one comparison per placed node, plus one write for the leftovers.
- Space: O(1) extra, just the dummy and three references; nodes are reused, not copied.

## Variations you will meet

- **Merge k sorted lists.** The "smaller of two heads" becomes "smallest of k heads", which a heap answers in O(log k).
  Or merge pairs in rounds like merge sort.
- **Sort a linked list.** Merge sort: split at the middle with slow/fast pointers, sort each half, and merge with exactly
  this routine.
- **Merge sorted arrays in place** (LeetCode 88). No arrows to rewire, so fill from the back to avoid overwriting.
- **Recursive merge.** Return the smaller head with its `next` set to the merge of the rest. Elegant, but O(m+n) stack.

## What to carry forward

A dummy node gives the output a fixed starting point, and a `tail` pointer makes every append the same two lines. The
next problem keeps that dummy-and-tail skeleton but creates new nodes and carries a digit from one step to the next.
