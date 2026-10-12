---
rank: 6
slug: floyd_cycle_detection
---

Given the head of a linked list whose last node may link back to an earlier node, decide whether there is a cycle and return the node where it begins, using `O(1)` extra space. In the list `1 → 2 → … → 7` whose tail links back to node `3`, the answer is node `3`.

The brute force keeps a hash set of visited nodes and returns the first node seen twice: `O(n)` time, but `O(n)` space. Floyd's idea replaces the memory with a difference in speed. A slow pointer moves one step at a time and a fast pointer two. Without a cycle, fast runs off the end. With one, both pointers end up circling the loop, and because fast gains exactly one node per step, the gap between them shrinks by one each step and closes on a meeting instead of jumping over it.

Finding the entry takes one more observation. Say the tail holds `a` nodes before the entry, the cycle holds `c`, and the pointers meet `b` steps past the entry. Fast has walked twice as far as slow and stands on the same node, so the extra distance, which equals slow's whole walk, is a whole number of laps. Slow's walk is `a` steps of tail plus `b` steps into the cycle, plus any full laps, so `a + b = k·c` for some whole `k`, that is `a = k·c - b`. Walking `a` steps from the meeting point therefore lands exactly on the entry, and so does walking `a` steps from the head. Restart one pointer at the head, step both by one, and they meet at the entry.

```text
1 → 2 → 3 → 4 → 5          tail: a = 2 nodes (1, 2), entry 3
        ↑       │          cycle: c = 5 nodes (3, 4, 5, 6, 7)
        │       ↓
        7 ←──── 6
phase 1   slow  fast        phase 2   from_head  from_meet
start      1     1          start         1          6
step 1     2     3          step 1        2          7
step 2     3     5          step 2        3          3    meet at the entry
step 3     4     7
step 4     5     4
step 5     6     6    meet at 6, b = 3 steps past the entry (3 → 4 → 5 → 6)
a + b = 2 + 3 = 5 = 1·c, so a = 1·5 - 3: two steps from 6 reach 3
```

```pseudo
FUNCTION MeetingPoint(head)
    slow ← head
    fast ← head
    WHILE fast ≠ null AND fast.next ≠ null
        slow ← slow.next
        fast ← fast.next.next
        IF slow = fast                     // the same node, not an equal value
            RETURN slow
    RETURN null                            // fast fell off the end: no cycle

FUNCTION CycleEntry(head)
    meet ← MeetingPoint(head)
    IF meet = null
        RETURN null
    from_head ← head
    from_meet ← meet
    WHILE from_head ≠ from_meet            // both are a steps from the entry
        from_head ← from_head.next
        from_meet ← from_meet.next
    RETURN from_head
```

Slow takes at most `n` steps before the meeting and the second phase takes `a` more, so the search is `O(n)` time with `O(1)` space. The same two pointers work on any sequence where each value determines the next, an implicit linked list. In Find the Duplicate Number, index `i` points to `nums[i]`; the duplicate is the only node with more than one arrow coming in, so it is the entry of the cycle. In Happy Number, each number points to the sum of the squares of its digits, and the number is happy exactly when the cycle its walk falls into is `1 → 1`. The classic mistake is testing `slow = fast` before the first move, where both sit on the head, or comparing values instead of nodes, which finds a cycle in `5 → 5 → 5`.

*Practice:* LC 141 Linked List Cycle · LC 142 Linked List Cycle II · LC 287 Find the Duplicate Number · LC 202 Happy Number
