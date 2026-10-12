---
rank: 104
slug: reorder_list
---

Given the head of a singly linked list `L0 → L1 → … → Ln`, reorder it in place into `L0 → Ln → L1 → Ln-1 → L2 → …`, relinking the nodes rather than copying their values. `1 → 2 → 3 → 4 → 5` becomes `1 → 5 → 2 → 4 → 3`.

The brute force copies the nodes into an array and relinks them with two indices closing in from both ends: `O(n)` time, but `O(n)` extra space. Without the array the order looks hard, because it reads the list from both ends at once and a singly linked list can only be read forward. Split it in two, though, and the answer takes the first half forward and the second half backward, one node from each in turn. Reverse the second half in place and both halves read forward, so the answer is a zipper of two forward lists. That is three steps, each one already known: slow and fast pointers find the end of the first half, a cut and a reversal (#6) turn the second half around, and a weave alternates the halves.

Picture folding the list at its middle like a strip of paper, so that the tail lies reversed under the head, and reading down the zigzag. Fast moves two nodes for every one that slow moves, so when fast has no double step left, slow stands on index `(n - 1) / 2` rounded down, the last node of the first half. With an odd count the first half keeps the extra node, which is right, since the middle node ends the woven list. The second half is never longer, so the weave runs while it has nodes, and each step saves both `next` pointers before it relinks `first → second → the rest of the first half`.

```text
1       2       3        first half, read forward
  \   /   \   /          the woven list zigzags: 1 → 5 → 2 → 4 → 3
    5       4            second half, reversed

start     1 → 2 → 3 → 4 → 5
middle    slow 1, 2, 3   fast 1, 3, 5     fast.next is null: slow ends on 3
cut       first 1 → 2 → 3      second 4 → 5
reverse   first 1 → 2 → 3      second 5 → 4
weave 1   1 → 5, 5 → 2   list 1 → 5 → 2 → 3          second left 4
weave 2   2 → 4, 4 → 3   list 1 → 5 → 2 → 4 → 3      second left null
```

```pseudo
FUNCTION ReverseList(head)
    prev ← null
    curr ← head
    WHILE curr ≠ null
        next_node ← curr.next              // save the rest before the cut
        curr.next ← prev
        prev ← curr
        curr ← next_node
    RETURN prev

FUNCTION ReorderList(head)
    IF head = null
        RETURN
    slow ← head
    fast ← head
    WHILE fast.next ≠ null AND fast.next.next ≠ null
        slow ← slow.next                   // ends on the first half's last node
        fast ← fast.next.next
    second ← slow.next
    slow.next ← null                       // cut after the first half
    second ← ReverseList(second)
    first ← head
    WHILE second ≠ null                    // the second half is never longer
        next_first ← first.next            // save both rests before relinking
        next_second ← second.next
        first.next ← second
        second.next ← next_first
        first ← next_first
        second ← next_second
```

Each step walks the list at most once, so the reorder takes `O(n)` time with a handful of pointers, `O(1)` space. Reach for middle plus reversal whenever a list problem pairs its front with its back: Palindrome Linked List compares the first half with the reversed second, Maximum Twin Sum of a Linked List adds them pair by pair, and Middle of the Linked List is the first step alone, written `WHILE fast ≠ null AND fast.next ≠ null` because it wants the second middle of an even-length list. The classic mistake is skipping the cut. The first half's last node then still points into the second half, so on the example `3 → 4` survives while the weave adds `4 → 3`, and the list ends in a cycle, `1 → 5 → 2 → 4 → 3 → 4 → 3 → …`.

*Practice:* LC 143 Reorder List · LC 876 Middle of the Linked List · LC 234 Palindrome Linked List · LC 2130 Maximum Twin Sum of a Linked List
