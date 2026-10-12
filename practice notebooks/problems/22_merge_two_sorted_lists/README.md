# Merge Two Sorted Lists (LeetCode 21)

**Area:** linked list · **Difficulty:** Medium · **Key operations:** dummy head, tail pointer, attach the smaller front node, advance that list, attach the leftover

## Problem

You are given the heads of two sorted singly linked lists. Merge them into one sorted list by splicing the existing nodes together (no new nodes for the values) and return the head of the merged list. Either list may be empty.

## Example

```
l1: 1 -> 2 -> 4 -> None
l2: 1 -> 3 -> 4 -> None
out: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None
```

## Brute force

Walk both lists collecting every value into an array, sort it, and build a new linked list.

O((m+n) log(m+n)) time, O(m+n) space. The wasted work: the sort ignores that each input is already sorted (the only unknown is how the two sequences interleave), and the new nodes duplicate ones that could simply be relinked.

## From brute force to optimal

The smallest remaining value overall is always one of the two list fronts, so one comparison decides the next output node. Keep a `tail` pointer at the end of the merged list: attach the smaller front node to `tail.next`, advance that list, and advance `tail`. When one list is exhausted the other is already sorted, so attach it whole in O(1).

Two details make the code clean. A `dummy` node before the real head removes the "is this the first node?" special case: the answer is `dummy.next`. And `tail.next = l1 or l2` attaches whichever list is non-empty (or None if both are).

## Intuition

Two face-up decks of sorted cards. Repeatedly take the smaller top card and lay it on the output pile. When one deck runs out, drop the other deck on top as it is. Because we move the existing nodes rather than copy their values, this is a splice: `tail` is the last card on the output pile, and each step hooks one input front onto it.

```
out:  dummy -> 1 -> 1 -> 2        l1: 4 -> None
                        tail      l2: 3 -> 4 -> None
```

## Walkthrough

`l1 = 1 -> 2 -> 4`, `l2 = 1 -> 3 -> 4`. `tail` starts on the dummy.

```
l1: 1 -> 2 -> 4    l2: 1 -> 3 -> 4     1 <= 1  take l1    merged: dummy -> 1               tail = 1
l1: 2 -> 4         l2: 1 -> 3 -> 4     2 >  1  take l2    merged: dummy -> 1 -> 1          tail = 1
l1: 2 -> 4         l2: 3 -> 4          2 <= 3  take l1    merged: dummy -> 1 -> 1 -> 2     tail = 2
l1: 4              l2: 3 -> 4          4 >  3  take l2    merged: dummy -> 1 -> 1 -> 2 -> 3     tail = 3
l1: 4              l2: 4               4 <= 4  take l1    merged: dummy -> 1 -> 1 -> 2 -> 3 -> 4     tail = 4
l1: None           l2: 4               l1 is empty: attach the rest of l2 behind tail
result: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None   (dummy.next)
```

## Steps

1. `dummy = ListNode()`, `tail = dummy`.
2. While both `l1` and `l2` are non-empty: if `l1.val <= l2.val`, `tail.next = l1` and `l1 = l1.next`; else `tail.next = l2` and `l2 = l2.next`. Then `tail = tail.next`.
3. `tail.next = l1 or l2` (whichever still has nodes).
4. Return `dummy.next`.

## Complexity

O(m + n) time: each node is looked at once and relinked once. O(1) extra space: one dummy node and two pointers.

## Pitfalls

- **`while l1 or l2`.** Once one list is empty the comparison reads `.val` on None and raises. Loop while *both* exist and attach the leftover afterwards.
- **Attaching only one leftover.** `tail.next = l1` drops the rest of `l2` whenever `l1` runs out first. Use `l1 or l2`.
- **Returning `dummy`.** The placeholder's value 0 appears at the front. The merged list starts at `dummy.next`.
- **Forgetting to advance `tail`.** The next attachment overwrites `tail.next` and the merged list stays one node long.
- **`<` vs `<=`.** Either produces a sorted list; `<=` keeps the merge stable (ties take from `l1` first).
