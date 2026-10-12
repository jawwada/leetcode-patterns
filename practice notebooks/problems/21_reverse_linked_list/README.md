# Reverse Linked List (LeetCode 206)

**Area:** linked list · **Difficulty:** Medium · **Key operations:** save nxt, flip cur.next to prev, advance prev and cur, return prev

## Problem

Given the head of a singly linked list, reverse the list in place and return the new head. The list may be empty.

## Example

```
1 -> 2 -> 3 -> 4 -> 5 -> None      becomes      5 -> 4 -> 3 -> 2 -> 1 -> None
```

## Brute force

Walk the list copying the values into an array, reverse the array, and build a brand-new linked list from it.

O(n) time, O(n) extra space. The wasted work: n new nodes (or an n-element array) are allocated just to express an order that the existing `next` pointers can hold, if each one is re-aimed at its predecessor.

## From brute force to optimal

Reversing means every node's `next` should point to its predecessor instead of its successor. That can be done in one pass with three pointers: `prev` (the node behind), `cur` (the node being flipped), and `nxt` (a saved copy of `cur.next`). The only danger is losing the rest of the list the moment you overwrite `cur.next`, so save it in `nxt` first. The invariant: `prev` heads a fully reversed prefix, `cur` heads the untouched suffix. When `cur` runs off the end, `prev` is the new head.

## Intuition

Two chains meet at the boundary between `prev` and `cur`: a reversed chain growing to the left and an untouched chain shrinking to the right.

```
None <- 1 <- 2       3 -> 4 -> 5 -> None
        prev        cur  nxt
```

Each step detaches `cur` from the right chain and pushes it onto the front of the left chain, like moving the top card from one pile to another. Flip one arrow at a time; stash the next card before you flip, so the right pile is never lost.

## Walkthrough

```
None                 |    1 ->  2 ->  3 ->  4 ->  5 -> None
prev                      cur   nxt
    save nxt = 2; flip 1.next -> None; prev = 1, cur = 2

None <-  1           |    2 ->  3 ->  4 ->  5 -> None
       prev               cur   nxt
    save nxt = 3; flip 2.next -> 1; prev = 2, cur = 3

None <-  1 <-  2     |    3 ->  4 ->  5 -> None
             prev         cur   nxt
    save nxt = 4; flip 3.next -> 2; prev = 3, cur = 4

None <-  1 <-  2 <-  3   |    4 ->  5 -> None
                   prev       cur   nxt
    save nxt = 5; flip 4.next -> 3; prev = 4, cur = 5

None <-  1 <-  2 <-  3 <-  4   |    5 -> None
                         prev       cur
    save nxt = None; flip 5.next -> 4; prev = 5, cur = None

None <-  1 <-  2 <-  3 <-  4 <-  5   |   None
cur is None -> return prev = 5:  5 -> 4 -> 3 -> 2 -> 1 -> None
```

## Steps

1. `prev = None`, `cur = head`.
2. While `cur` is not None: `nxt = cur.next`; `cur.next = prev`; `prev = cur`; `cur = nxt`.
3. Return `prev`.

## Complexity

O(n) time: one pass, constant work per node. O(1) extra space: three pointers, no new nodes.

## Pitfalls

- **Advancing with `cur.next` after the flip.** `cur.next` now points backwards, so `cur = cur.next` walks the wrong way and stops immediately. Advance with the saved `nxt`.
- **Returning `head`.** The old head is now the tail with `next = None`; it reads as a one-element list. The new head is `prev`.
- **`while cur.next` instead of `while cur`.** The last node is never flipped and drops out of the result; an empty list raises on `None.next`.
- **Saving `nxt` after overwriting `cur.next`.** The rest of the list is gone. Save first, flip second.
- **Forgetting the empty list.** With `prev = None` and `cur = head = None` the loop does not run and `None` is returned, which is right; do not add a special case that breaks it.
