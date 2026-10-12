# Remove Nth Node From End of List (LeetCode 19)

**Area:** linked list · **Difficulty:** Medium · **Key operations:** dummy head, open a gap of n+1, slide both pointers, splice slow.next = slow.next.next

## Problem

Given the head of a singly linked list and an integer `n`, remove the `n`-th node from the end and return the head. `n` is valid: `1 <= n <= length`.

## Example

```
1 -> 2 -> 3 -> 4 -> 5, n = 2
          ^ 4 is the 2nd from the end

1 -> 2 -> 3 -> 5
```

## Brute force

Pass 1: walk the list and count its length `L`. Pass 2: walk to the node at position `L - n - 1` (the predecessor of the victim) and set its `next` to skip one node. A dummy node in front of the head makes the predecessor exist even when the victim is the first node.

O(n) time, O(1) space, but two full traversals. The wasted work: the first pass exists only to translate "n from the end" into "L - n from the start", so every node is visited twice to learn a single number.

## From brute force to optimal

We never needed `L` itself, only a pointer that is exactly `n + 1` links behind the end. Carry that distance with us. Start two pointers at the dummy, advance `fast` by `n + 1` links, then move both at the same speed. The gap stays `n + 1`, so when `fast` steps off the end (`None`), `slow` is `n + 1` from the end, which is the predecessor of the node to remove. One pass, no counting, and the dummy means removing the head is the same splice as any other.

## Intuition

Picture a measuring stick of length `n + 1` laid along the list with its back end on the dummy. Slide the stick to the right one node at a time. When the front end falls off the end of the list, the back end rests on the node just before the one you want to delete. You never had to know how long the list is; the stick measured from the end for you.

## Walkthrough

`[slow]` and `[fast]` mark the two pointers; the dummy sits in front of the head.

```
start    dummy[slow+fast] -> 1 -> 2 -> 3 -> 4 -> 5 -> None
gap 3    dummy[slow] -> 1 -> 2 -> 3[fast] -> 4 -> 5 -> None      fast moved n + 1 = 3 links
slide    dummy -> 1[slow] -> 2 -> 3 -> 4[fast] -> 5 -> None
slide    dummy -> 1 -> 2[slow] -> 3 -> 4 -> 5[fast] -> None
slide    dummy -> 1 -> 2 -> 3[slow] -> 4 -> 5 -> None[fast]      fast is off the end

splice   slow.next = slow.next.next   (3 now points to 5, 4 is dropped)
result   dummy -> 1 -> 2 -> 3 -> 5 -> None      return dummy.next
```

Removing the head works the same way: for `1 -> 2`, `n = 2`, after the gap `fast` is already `None`, `slow` stays on the dummy, and `dummy.next = dummy.next.next` makes `2` the new head.

## Steps

1. `dummy = ListNode(_, head)`; `slow = fast = dummy`.
2. Advance `fast` by `n + 1` links.
3. While `fast` is not `None`: advance `slow` and `fast` together.
4. `slow.next = slow.next.next`.
5. Return `dummy.next`.

## Complexity

O(n) time, a single pass with two pointers. O(1) extra space.

## Pitfalls

- **Gap of `n` instead of `n + 1`.** With a gap of `n`, `slow` stops on the victim rather than before it, so the wrong node is unlinked; for `n = 1` `slow` stops on the tail and `slow.next.next` reads the `next` of `None`.
- **Returning `head` instead of `dummy.next`.** When the victim is the first node, the list now begins at `dummy.next`. `[1]` with `n = 1` would return `[1]` instead of `[]`.
- **`while fast.next` instead of `while fast`.** Stopping one link early leaves `slow` one node too far left, so the `(n+1)`-th node from the end is removed; when `n` equals the length, `fast` is already `None` and `fast.next` crashes.
- **No dummy.** Without it, removing the head needs a special case, and `slow` has nowhere to stand when the victim is the first node.
- **Advancing `slow` during the gap phase.** Only `fast` moves while the gap opens; the slide phase is where both move.
