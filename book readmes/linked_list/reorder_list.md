# Reorder List
*LeetCode 143 · Medium · Pattern: Find middle + reverse second half + interleave · Reading time ~8 min*

## The problem

Given L0 -> L1 -> ... -> Ln, reorder it in place to L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ..., changing only node
links, not values.

```text
Example: 1->2->3->4->5 becomes 1->5->2->4->3.
```

## What the problem is really asking

Take a list L0 -> L1 -> ... -> Ln and rearrange its nodes into L0 -> Ln -> L1 -> Ln-1 -> L2 -> ... : first, last, second, second-to-last, and so on, alternating inward from both ends. You must move nodes by relinking, not by swapping values, and you return nothing; the list is changed in place.

```text
  before:  1 -> 2 -> 3 -> 4 -> 5
           front ->       <- back

  after:   1 -> 5 -> 2 -> 4 -> 3
           F    B    F    B    F
```

The answer is a rewired list. What makes it hard is the same thing as in the previous problem: half the nodes are consumed from the back, and a singly linked list has no way to step backwards. On top of that, every relink must happen without losing the rest of the list.

## Do it by hand first

With five cards in a row, you would take one from the left, one from the right, one from the left, and so on, until you meet in the middle.

```text
  row:   [1] [2] [3] [4] [5]
          L               R     take 1, take 5
              L       R         take 2, take 4
                  LR            take 3
  pile:  1 5 2 4 3
```

Your hand kept two cursors: one moving right from the front and one moving *left* from the back. The front cursor is free on a linked list. The back cursor is the problem, and it only ever travels over the back half, from the end toward the middle.

## The first honest attempt

Put every node into an array; now you have random access. Use i from the front and j from the back, linking `nodes[i] -> nodes[j] -> nodes[i+1]`, and finally set the last node's next to None. O(n) time, O(n) space.

```text
  list:   1 -> 2 -> 3 -> 4 -> 5
  array: [n1, n2, n3, n4, n5]    a full index of every node
           i               j
```

It is correct, but the array is a full copy of the list's structure built for one reason: to read the back half in reverse. The front half never needed it at all. We are paying O(n) memory for backward access to n/2 nodes.

## The turning point

**Claim: the reordered list is exactly the front half merged, alternately, with the back half reversed; and both "halves" and "reversed" can be produced in place.**

Look at the order the back nodes are used: 5, then 4. That is the back half `4 -> 5` read backwards. If we physically reverse it to `5 -> 4`, the back cursor becomes an ordinary forward pointer. And the target order is then: take one from the front list, one from the reversed back list, repeat. That is a plain zip of two lists.

So the problem decomposes into three subroutines you already own.

*Find the middle.* Slow and fast pointers, like Palindrome Linked List, but this time with the loop `while fast.next and fast.next.next`, so slow stops on the **last node of the first half** (node 3 for five nodes, node 2 for four). We stop one earlier than in the palindrome problem because we need to *cut* after slow, and you can only cut a link from the node before it.

*Cut and reverse.* Save `second = slow.next`, then set `slow.next = None`. This cut is not optional: without it the first half still runs into the back half, and after reversing and splicing you create a cycle. Then reverse `second` with the three-pointer reversal.

*Zip.* With `first` on the front half and `second` on the reversed back half, repeatedly: save both nexts, link `first -> second -> (old first.next)`, and advance both to their saved nexts. Stop when `second` runs out. The front half is equal in length or one longer, so the last front node is already in place with next None.

The zip is the moment where you can lose nodes. Before touching `first.next`, save it; before touching `second.next`, save it. Both saves happen first, then both links, then both advances.

## Watch it work

List `1 -> 2 -> 3 -> 4 -> 5`.

Frame 1 — find the middle.

```text
  start:   S,F at 1
  round 1: S = 2, F = 3
  round 2: S = 3, F = 5   (F.next is None: stop)

  1 -> 2 -> 3 -> 4 -> 5 -> None
            S         F
```

Slow is on node 3, the last node of the first half.

Frame 2 — cut and reverse.

```text
  first:   1 -> 2 -> 3 -> None
  second:  4 -> 5 -> None      (cut: 3.next = None)
  reverse: 5 -> 4 -> None

  first = 1        second = 5
```

The back half now reads 5, 4, exactly the order the back cursor needs.

Frame 3 — zip step 1.

```text
  saved: n1 = 2, n2 = 4
  link:  1.next = 5,  5.next = 2

  1 -> 5 -> 2 -> 3 -> None
            first      second = 4 -> None
```

Node 5 is spliced between 1 and 2; both pointers move to their saved nexts.

Frame 4 — zip step 2.

```text
  saved: n1 = 3, n2 = None
  link:  2.next = 4,  4.next = 3

  1 -> 5 -> 2 -> 4 -> 3 -> None
                      first     second = None
```

Node 4 is spliced between 2 and 3; second is now None, so the loop ends.

Frame 5 — result.

```text
  1 -> 5 -> 2 -> 4 -> 3 -> None
  F    B    F    B    F
```

Node 3 never moved: the cut in Frame 2 already made it the tail.

At every zip step the list from `head` up to `first` was correctly reordered, `first` led into the untouched rest of the front half, and `second` led into the untouched rest of the reversed back half. Each step moved one node from each.

## Why it is correct

After Frame 2, the front list is L0..Lm and the back list is Ln, Ln-1, ..., Lm+1, where m = floor(n/2) for nodes indexed 0..n, so the front list has the same number of nodes as the back or exactly one more. The target is the alternation L0, Ln, L1, Ln-1, ..., which is the alternation of these two lists starting with the front.

Invariant before each zip step: the nodes already linked from head form a correct prefix of the target ending at the node before `first`, and its last link points to `first`; `first` and `second` head the unused parts of the two lists. One step links `first -> second -> first's old next`, extending the prefix by two in the right order and preserving the invariant. When `second` is None the back list is used up; the front has at most one node left, which is already the tail with next None because of the cut. Every node is linked exactly once, so nothing is lost and no cycle forms.

## Cost

- **Time: O(n).** Half a pass to find the middle, a pass over the back half to reverse it, and one zip pass.
- **Space: O(1).** A constant number of pointers; only links are changed.
- The array version is O(n) time and O(n) space.

## Variations you will meet

- **Palindrome Linked List (previous problem).** Same middle and reverse steps; compare the halves instead of zipping them.
- **Odd Even Linked List (LeetCode 328).** Also a regrouping in place, but by position parity: two running tails, no reversal, then attach evens after odds.
- **Merge Two Sorted Lists.** The zip here is a merge whose "comparison" is just alternation; if the halves had to interleave by value, you would compare heads instead.
- **Reorder starting from the back (Ln, L0, Ln-1, L1, ...).** Same three steps; start the zip with the reversed half.

## What to carry forward

Middle, cut, reverse, zip: four moves that turn "consume from both ends" into "walk two lists forward". The next problem, Copy List with Random Pointer, also weaves a second list into the first, but the second list is made of brand-new nodes, and the weave itself becomes the lookup table.
