# Linked lists

A singly linked list is a chain of nodes, each holding a value and a pointer `next` to the following node (or `None` at the end). Nothing is indexed: to reach the k-th node you walk k steps. In exchange, splicing a node in or out is a pointer change, not a shift of everything behind it. Every exercise here is about moving a few pointers in the right order, and the only thing that ever goes wrong is losing the rest of the list by overwriting a pointer before you saved what it pointed to.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
```

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| walk to index k | O(k) | `for _ in range(k): node = node.next` |
| insert after a known node | O(1) | `new.next = node.next; node.next = new` (two writes, this order) |
| delete the node after a known node | O(1) | `node.next = node.next.next` |
| find by value | O(n) | walk with `prev` so you can unlink the hit |
| reverse in place | O(n) time, O(1) space | three pointers: prev, cur, nxt |
| middle / cycle detection | O(n) time, O(1) space | fast moves 2, slow moves 1 |
| merge two sorted lists | O(n + m) | relink the existing nodes, no allocation |

Two tools remove almost every special case:

- **Dummy head.** `dummy = ListNode(0, head)` makes "insert at index 0" and "delete the head" the same code as every other position; return `dummy.next` at the end.
- **Tail pointer.** When building a result, keep `tail` on the last node attached and append with `tail.next = node; tail = node`.

## Drawn example: reverse 1 -> 2 -> 3 in place

```
prev=None  cur=1 -> 2 -> 3                nxt = cur.next   (save 2 BEFORE cutting)
           cur.next = prev                 1 -> None       (the cut)
prev=1     cur=2 -> 3   nxt=2 -> 3        prev, cur = cur, nxt

           nxt = 3 ; cur.next = prev       2 -> 1 -> None
prev=2->1  cur=3        nxt=3

           nxt = None ; cur.next = prev    3 -> 2 -> 1 -> None
prev=3->2->1  cur=None                     loop ends: return prev
```

Fast and slow on 1 -> 2 -> 3 -> 4 (even length):

```
start  1(slow,fast) -> 2 -> 3 -> 4
step   1 -> 2(slow) -> 3(fast) -> 4
step   1 -> 2 -> 3(slow) -> 4      fast = None  -> stop; slow is the RIGHT middle
```

`while fast and fast.next` stops with `fast` on the last node (odd length) or at `None` (even length); either way `slow` is the middle, and for even lengths it is the second of the two middles.

## The invariant to say out loud

"Save next before you cut." Whenever you are about to overwrite `node.next`, the old value must already be in a variable (`nxt`, `tail`, `group_next`) or you have just lost the rest of the list. The second thing to say: "where is my dummy, and am I returning `dummy.next`?"

## Exercises

| File | Drills |
|---|---|
| `01_build_print_insert_delete.py` | walk from a dummy to the node before the slot, splice in, unlink by skipping over |
| `02_reverse_iterative_and_recursive.py` | prev/cur/nxt three-pointer reversal and the recursive unwind |
| `03_middle_with_fast_and_slow.py` | `while fast and fast.next`; even length gives the right middle |
| `04_detect_cycle_floyd.py` | tortoise and hare meet inside the cycle; reset to head to find the entry index |
| `05_merge_two_sorted.py` | dummy head + tail, attach the smaller head, attach the leftover whole |
| `06_palindrome_linked_list.py` (LC 234) | middle, reverse the second half in place, compare, O(1) space |
| `07_reverse_nodes_in_k_group.py` (LC 25) | probe k ahead, reverse one group with prev seeded to the next group, re-hook |
| `08_add_two_numbers.py` (LC 2) | two lists of unequal length, carry, loop while a carry is pending |
