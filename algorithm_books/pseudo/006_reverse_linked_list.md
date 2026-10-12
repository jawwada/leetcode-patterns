---
rank: 6
slug: reverse_linked_list
---

Given the head of a singly linked list, reverse the list in place and return the new head. `1 → 2 → 3 → 4 → 5` becomes `5 → 4 → 3 → 2 → 1`, built from the same five nodes.

There is no index to swap by, and copying the values into a new list wastes `O(n)` space. The insight is that reversing a list means turning every `next` arrow around, and an arrow can be turned the moment we stand on its node, provided we first save where it pointed. So walk the list once with three pointers. `curr` is the node being processed, `prev` is the node it must now point back to, and `next_node` holds the rest of the list for the instant its link is cut. Every step saves, turns and advances: `next_node ← curr.next`, then `curr.next ← prev`, then `prev` and `curr` each move one node forward.

Picture two chains. `prev` heads the reversed part, `curr` heads the part still in its original order, and each step lifts the front node off the second chain and lays it on the front of the first, like moving plates from one stack to another. The invariant is that the two chains together hold every node, none lost and none repeated. When `curr` runs off the end, the first chain is the whole list reversed, and `prev` is its head.

```text
step   prev (reversed part)         curr (still to reverse)
start  null                         1 → 2 → 3 → 4 → 5 → null
1      1 → null                     2 → 3 → 4 → 5 → null
2      2 → 1 → null                 3 → 4 → 5 → null
3      3 → 2 → 1 → null             4 → 5 → null
4      4 → 3 → 2 → 1 → null         5 → null
5      5 → 4 → 3 → 2 → 1 → null     null            return prev
```

```pseudo
FUNCTION ReverseList(head)
    prev ← null                            // head of the reversed part
    curr ← head                            // head of the part still to reverse
    WHILE curr ≠ null
        next_node ← curr.next              // save the rest before the cut
        curr.next ← prev                   // turn this arrow around
        prev ← curr                        // the reversed part gains curr
        curr ← next_node                   // step into the saved rest
    RETURN prev                            // curr ran off the end
```

Each node is visited once and only three pointers are kept, so the reversal costs `O(n)` time and `O(1)` space. The recursive version reverses everything after the head first, then hooks the head behind its old neighbor with `head.next.next ← head` and `head.next ← null`; it is shorter but holds `O(n)` frames on the call stack, which overflows on a long enough list. Reach for this loop whenever a problem reverses a list or a stretch of one: between two positions, in groups of `k`, or the second half of a list to compare it with the first. The classic mistake is writing `curr.next ← prev` before saving `curr.next`, which cuts the rest of the list loose; the runner-up is returning `curr`, which is `null` at the end, instead of `prev`.

*Practice:* LC 206 Reverse Linked List · LC 92 Reverse Linked List II · LC 25 Reverse Nodes in k-Group · LC 234 Palindrome Linked List
