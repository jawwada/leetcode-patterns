# Merge k Sorted Lists (LeetCode 23)

**Area:** heap · **Difficulty:** Medium-Hard · **Key operations:** heap of the k current heads as (value, list_index, node_index), pop the smallest, push that list's next element

## Problem

Given `k` lists, each sorted in ascending order, merge them into one sorted list. LeetCode uses linked lists; the practice script uses plain Python lists, with `node_index` playing the role of the node pointer, so the heap logic is the same and the code stays short.

## Example

```
lists  = [[1, 4, 5],
          [1, 3, 4],
          [2, 6]]
merged = [1, 1, 2, 3, 4, 4, 5, 6]
```

## Brute force

Concatenate all values and sort.

O(N log N) for N values in total, O(N) space. The wasted work: the input is already `k` sorted runs, and a general sort ignores that completely, re-comparing values whose relative order is already known. (A second naive idea, scanning the `k` current heads for the minimum at each step, is O(N · k).)

## From brute force to optimal

Values inside one list never need comparing; they are already in order. The only real decision at each step is "which of the `k` current heads is smallest?". A linear scan answers it in O(k); a min-heap holding exactly the `k` heads answers it in O(log k). After taking the smallest head, push the next element of the *same* list so that list keeps a head in the heap. N outputs times log k each gives O(N log k).

Heap entries are `(value, list_index, node_index)`. The list index breaks ties between equal values (and, with real nodes, prevents Python from trying to compare the nodes themselves); the node index says where that list's frontier is.

## Intuition

Treat the `k` lists as `k` face-up decks. The heap holds the top card of each deck. Draw the smallest top card, put it on the output pile, then flip the next card of that same deck onto the heap. Repeat until every deck is empty. Geometrically: `k` rows of numbers with a frontier pointer at the start of each row; the heap contains exactly the `k` pointed-at values with the smallest at its apex. Pop the apex, advance that row's pointer one step right, push the newly exposed value. The frontier sweeps every row left to right exactly once.

## Walkthrough

Heap drawn as its array of `(value, list, pos)`; `remaining` shows what is left of each list that still has a head in the heap.

```
heads -> heap [(1,0,0), (1,1,0), (2,2,0)]              remaining {0: [1,4,5], 1: [1,3,4], 2: [2,6]}
pop 1 (list 0, pos 0)  merged [1]           push 4   heap [(1,1,0), (2,2,0), (4,0,1)]   {0: [4,5], 1: [1,3,4], 2: [2,6]}
pop 1 (list 1, pos 0)  merged [1,1]         push 3   heap [(2,2,0), (4,0,1), (3,1,1)]   {0: [4,5], 1: [3,4],   2: [2,6]}
pop 2 (list 2, pos 0)  merged [1,1,2]       push 6   heap [(3,1,1), (4,0,1), (6,2,1)]   {0: [4,5], 1: [3,4],   2: [6]}
pop 3 (list 1, pos 1)  merged [1,1,2,3]     push 4   heap [(4,0,1), (6,2,1), (4,1,2)]   {0: [4,5], 1: [4],     2: [6]}
pop 4 (list 0, pos 1)  merged [1,1,2,3,4]   push 5   heap [(4,1,2), (6,2,1), (5,0,2)]   {0: [5],   1: [4],     2: [6]}
pop 4 (list 1, pos 2)  merged [..,4,4]      list 1 exhausted, nothing to push
                                                     heap [(5,0,2), (6,2,1)]            {0: [5],   2: [6]}
pop 5 (list 0, pos 2)  merged [..,4,4,5]             heap [(6,2,1)]                     {2: [6]}
pop 6 (list 2, pos 1)  merged [1,1,2,3,4,4,5,6]      heap []
```

The two 4's: `(4, 0, 1)` pops before `(4, 1, 2)` because the list index breaks the tie. The heap never holds more than 3 entries.

## Steps

1. Seed the heap with `(row[0], i, 0)` for every **non-empty** list `i`; `heapify`.
2. While the heap is non-empty: pop `(val, i, j)`, append `val` to the output.
3. If `j + 1 < len(lists[i])`: push `(lists[i][j + 1], i, j + 1)`, the next head of the same list.
4. Return the output.

## Complexity

O(N log k) time: each of the N values is pushed and popped once on a heap of at most k entries. O(k) heap space (plus the output).

## Pitfalls

- **`<=` when advancing.** `j + 1 <= len(lists[i])` pushes `lists[i][len]`: IndexError at the end of every list.
- **Not skipping empty lists when seeding.** `row[0]` on an empty list raises before merging starts; `[[]]` and `[[], [1], []]` are standard test inputs.
- **`heap.pop()` instead of `heappop`.** `list.pop()` takes the last array slot, an arbitrary leaf of the heap, so values come out unsorted.
- **Wrong tuple order.** `(i, value, j)` orders the heap by list index, not value, and the popped tuple is unpacked wrongly.
- **With real linked lists: pushing `(val, node)` without the index tiebreaker.** Equal values make Python compare two `ListNode`s and raise `TypeError`.
