# Remove Nth Node From End of List

*LeetCode 19 · Medium · Pattern: Two pointers with fixed gap · Reading time ~8 min*

## What the problem is really asking

Delete the node that sits n places from the end (n = 1 is the last node) and return the head of what is left. n is always
valid.

The answer is the same list minus one node, so it is really a question about finding a node. To delete a node in a singly
linked list you must stand on the node **before** it and skip over it. The trouble is that "n from the end" is measured
from a place you cannot see. You only have the head, and the list does not know its own length.

```text
n = 2

 [1] -> [2] -> [3] -> [4] -> [5] -> None
                       ^
                  2nd from end (delete)
                ^
         stand here: [3].next = [3].next.next

 [1] -> [2] -> [3] -> [5] -> None
```

And there is an edge you must not forget: if n equals the length, the node to delete is the head itself, which has no
predecessor.

## Do it by hand first

With the list drawn on paper, you would count it: five nodes. Second from the end is position 5 - 2 + 1 = 4, so you stand
on position 3 and cut node 4 out.

```text
 count:  1    2    3    4    5     length = 5
 cut:              ^    x          stand on 5 - 2 = 3
```

Your hand needed one number, the length, to convert "from the end" into "from the start". Hold on to that; the turning
point is about getting the conversion without the number.

## The first honest attempt

Two passes. First walk the list to count its length L. Then walk again L - n steps from a dummy node to land on the
predecessor, and unlink. O(L) time, O(1) space.

That is already linear, so the interviewer's follow-up is "can you do it in one pass?" Look at what the first pass
produces:

```text
pass 1:  [1] [2] [3] [4] [5]      -> learn one number, L = 5
         visits all 5 nodes
pass 2:  [1] [2] [3]              -> walk L - n = 3 steps
         visits 3 of them again
```

Every node in pass 1 is visited only to increment a counter. The nodes up to the predecessor are visited twice. The
counting pass exists only to translate between "distance from the end" and "distance from the start", and that
translation is what we want to eliminate.

## The turning point

**Claim: you do not need the length, only a pointer that is a fixed number of links ahead. When the leading pointer runs
off the end, the trailing one is exactly that many links from the end.**

Think of a ruler of fixed length slid along the list. Its front and back ends move together, so the distance between them
never changes. When the front end passes the last node and reaches `None`, the back end is a known distance from `None`.

Now pick the length of the ruler. We want the back end, `slow`, to stop on the **predecessor** of the target. The target
is n links before `None` (the last node is 1 link before `None`), so the predecessor is n + 1 links before `None`. So
`fast` must lead `slow` by n + 1 links.

```text
 gap n+1 = 3 links, n = 2

 slow                fast
  v                   v
 [3] -> [4] -> [5] -> None
   1      2      3          links from slow to fast
        target
```

Where do both start? On a **dummy** node placed in front of the head. This is the fix for the edge case. If n equals the
length, the target is the head, and its predecessor is the dummy. Since `slow` starts on the dummy, it can stop there, and
the same line `slow.next = slow.next.next` deletes the head. Returning `dummy.next` then gives the new head, whatever it
is.

The algorithm:

1. `dummy -> head`; `slow = fast = dummy`.
2. Move `fast` forward n + 1 times. This opens the gap.
3. Move both forward together until `fast` is `None`.
4. `slow.next = slow.next.next`; return `dummy.next`.

Step 2 never runs off the end prematurely: the dummy plus L nodes give L + 1 links to `None`, and n + 1 <= L + 1.

## Watch it work

List `1 -> 2 -> 3 -> 4 -> 5`, n = 2. `s` is `slow`, `f` is `fast`.

```text
Frame 1: start, both on the dummy
 [D] -> [1] -> [2] -> [3] -> [4] -> [5] -> None
 s,f
```

The ruler has length 0.

```text
Frame 2: fast moved n + 1 = 3 times
 [D] -> [1] -> [2] -> [3] -> [4] -> [5] -> None
  s                   f
```

Gap opened: `fast` is 3 links ahead of `slow`. From now on the gap never changes.

```text
Frame 3: slide once
 [D] -> [1] -> [2] -> [3] -> [4] -> [5] -> None
         s                   f
```

Both moved one link. `fast` is not `None`, keep going.

```text
Frame 4: slide again
 [D] -> [1] -> [2] -> [3] -> [4] -> [5] -> None
                s                   f
```

`fast` is on the last node; still not `None`.

```text
Frame 5: slide again; fast is None, stop
 [D] -> [1] -> [2] -> [3] -> [4] -> [5] -> None
                       s                   f
```

`slow` is 3 links from `None`: it is the predecessor of node 4, the 2nd from the end.

```text
Frame 6: slow.next = slow.next.next
 [D] -> [1] -> [2] -> [3] ---------> [5] -> None
                       s      [4] (orphaned)
 return D.next = [1]
```

Node 4 is skipped. The result reads 1, 2, 3, 5.

Across frames 2 to 5 the number of links from `slow` to `fast` stayed exactly n + 1. Nothing was rewired until the last
frame, and the dummy was never moved, so `dummy.next` still pointed at the head.

## Why it is correct

Let L be the list length. Number positions with the dummy at 0 and `None` at L + 1. After the gap step, `fast` is at
position n + 1 and `slow` at 0. Each slide adds 1 to both, so `fast - slow = n + 1` at all times. The loop stops when
`fast` is at L + 1, which puts `slow` at L - n. The target, n-th from the end, is at position L - n + 1, so `slow` is
exactly its predecessor. One write skips it and leaves every other node linked in order.

When n = L, `slow` stays at position 0, the dummy, and the write removes the head; `dummy.next` returns the correct new
head, which is `None` when the list had one node.

## Cost

- Time: O(L), a single pass: `fast` walks L + 1 links in total, and `slow` follows behind.
- Space: O(1), a dummy node and two references.

Strictly, the two-pass version also visits O(L) nodes. The one-pass version wins by touching each node at most twice in
one sweep, and, more usefully, by teaching a technique that works when you cannot afford a separate counting pass, such
as on a stream.

## Variations you will meet

- **Return the k-th node from the end** without deleting it. Gap of k instead of k + 1; `slow` lands on the node itself.
- **Middle of the linked list** (LeetCode 876). Here the "ruler" is not fixed length but stretches: `fast` moves two
  links per step, so when it reaches the end `slow` is halfway. That is the find-middle primitive.
- **Rotate list by k** (LeetCode 61). Reduce k modulo the length, use the gap to find the new tail (k + 1 from the end),
  then cut and reattach the last k nodes in front.
- **Intersection of two lists.** The same "equalise the distance to the end, then walk together" idea, applied to two
  lists instead of one.

## What to carry forward

Two pointers a fixed gap apart form a ruler; when the front falls off, the back is the gap's distance from the end, and a
dummy in front lets the back stop before the head. The next problem keeps two pointers but makes them run at different
speeds, which turns the ruler into a cycle detector.
