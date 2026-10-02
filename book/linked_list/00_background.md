# Linked Lists

*12 problems · Reading time ~17 min*

## Why this chapter exists

Linked list problems are rarely about storing data. They are about moving arrows without dropping anything. Every
problem in this chapter hands you a chain of nodes and asks you to rearrange it, measure it, or detect something about its
shape, usually with O(1) extra memory. The difficulty is never the idea "reverse this" or "find that"; it is doing it
when you can only see one node at a time and every write to a `next` field can sever the chain behind your back.

The twelve problems fall into a few families:

- **Rewire in place.** Turn the arrows around (reverse a list, reverse every block of k nodes).
- **Build an output chain behind a dummy.** Splice existing nodes or freshly made ones onto a tail pointer (merge two
  sorted lists, add two numbers).
- **Measure with two runners.** A fixed gap between two pointers turns "n-th from the end" into a single pass (remove the
  n-th node from the end, intersection of two lists).
- **Detect shape with two speeds.** A fast and a slow runner discover whether the chain loops, and a little arithmetic
  finds where the loop starts (cycle, cycle II, and the duplicate number hidden in an array).
- **Combine the primitives.** Find the middle, reverse half, then compare or interleave (palindrome list, reorder list).
- **Copy a tangled structure.** Clone a list whose nodes point at arbitrary other nodes (copy list with random pointer).

## What it is

A singly linked list is a set of separate objects scattered around memory. Each object (a node) holds a value and one
reference, `next`, to another node or to `None`. The only thing you are given is a reference to the first node, `head`.

```text
the picture you draw:

 head
  |
  v
 +---+---+    +---+---+    +---+---+
 | 1 | o-+--> | 2 | o-+--> | 3 | / |
 +---+---+    +---+---+    +---+---+
  val next     val next     val next (None)

what memory actually looks like:

 address  0x40        0x98        0x1c
         +---+----+  +---+----+  +---+----+
         | 1 |0x1c|  | 3 |None|  | 2 |0x98|
         +---+----+  +---+----+  +---+----+
          ^ head
 1 says "next is at 0x1c", 2 says "next is at 0x98";
 the order in memory is arbitrary
```

The nodes are not next to each other. The address in `next` is the only thing that says which node comes second. That
is why there is no index: an array can compute "element 5 lives at base + 5 * size", but a list has no base and no fixed
size per step. To reach the fifth node you must follow four arrows, one at a time. Position in a linked list is not a
number you can jump to; it is a walk you have to take.

A Python variable like `cur` or `prev` is not a node. It is a name tag tied to a node. Moving `cur = cur.next` slides the
tag along; it changes nothing in the list. Writing `cur.next = something` is different: it changes the arrow stored inside
the node, and that change is permanent and visible to everyone who reaches that node.

```text
cur = cur.next   (move a tag, list unchanged)

 before:   [1] -> [2] -> [3]        after:  [1] -> [2] -> [3]
            ^                                       ^
           cur                                     cur

cur.next = None  (edit an arrow, list changed)

 before:   [1] -> [2] -> [3]        after:  [1]    [2] -> [3]
            ^                                ^      (unreachable
           cur                              cur      from head)
```

Keep those two kinds of statement apart in your head and half of this chapter's bugs disappear.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Read head | O(1) | you hold a reference to it |
| Reach the k-th node | O(k) | must follow k arrows; no index arithmetic |
| Find length | O(n) | walk to `None` and count |
| Insert after a known node | O(1) | two arrow writes |
| Delete the node after a known node | O(1) | one arrow write |
| Delete a node given only itself | O(1) trick or O(n) | you need its predecessor's arrow |
| Reverse the whole list | O(n) | one arrow flip per node |
| Find the middle | O(n) | fast runner reaches the end in n/2 steps |

Insert `X` after node `A`. The order of the two writes matters: hook `X` onto `A`'s successor first, then hook `A` onto
`X`. Do it the other way round and `A.next` already points at `X`, so you have lost the address of `B`.

```text
insert X after A:

 start:     A -> B -> C          X -> None
 step 1:    X.next = A.next      X -> B   (A still -> B)
 step 2:    A.next = X           A -> X -> B -> C
```

Delete the node after `A`. One write skips over it; the skipped node still exists in memory (it may even still point at
`C`) but nothing reachable from `head` leads to it, so it is gone from the list.

```text
delete after A:

 start:     A -> B -> C
 A.next = A.next.next
 result:    A ------> C          B -> C  (orphaned)
```

Reverse in place. Three tags walk the list: `prev` (head of the part already reversed), `cur` (the node being flipped),
`nxt` (the rest, saved before the flip).

```text
middle of a reversal:

 None <- [1] <- [2]    [3] -> [4] -> None
                 ^      ^      ^
                prev   cur    nxt  (saved first)

 cur.next = prev ; prev = cur ; cur = nxt

 None <- [1] <- [2] <- [3]    [4] -> None
                        ^      ^
                       prev   cur
```

Find the middle. A slow tag moves one arrow per tick, a fast tag moves two. When fast cannot move any more, slow has
covered half the distance.

```text
 [1] -> [2] -> [3] -> [4] -> [5] -> None
 s,f                                    tick 0
         s      f                       tick 1
                s             f         tick 2: f.next is None
                ^ middle
```

## The invariant

The one property every linked list algorithm protects:

**Every node you still need must be reachable from some reference you are holding.**

A node is reachable if you can get to it from `head`, from `dummy`, or from one of your tags (`prev`, `cur`, `nxt`,
`slow`, `tail`...) by following arrows. The moment the last arrow into a part of the list is overwritten and no tag sits
on it, that part is lost for good. Python will garbage-collect it; you cannot get it back.

This gives the working rule: **save `next` before you rewire.** Before any statement of the form `x.next = ...`, ask:
"is `x.next` the only way I know to reach the rest?" If yes, put a tag on it first.

```text
legal state (mid-reversal, rest saved):

 None <- [1] <- [2]   [3] -> [4] -> None
                 ^     ^      ^
                prev  cur    nxt
 every node reachable from prev or nxt

illegal state (flipped cur.next before saving it):

 None <- [1] <- [2] <- [3]    [4] -> None
                        ^      ^
                    prev,cur   ??? no tag here
 [4] is unreachable: the tail of the list is lost
```

The dummy head is the other half of this invariant. Many algorithms might delete or replace the first node, which would
force a special case ("if we are at the head, update `head` instead of `prev.next`"). A dummy node placed in front of the
real head removes the special case: every real node, including the first, now has a predecessor, and `dummy.next` is
always the current head no matter what happened to the original first node.

```text
without dummy: deleting [1] means "head = head.next" (special)

with dummy:
 [D] -> [1] -> [2] -> [3]       prev = D
 prev.next = prev.next.next     same code as any other delete
 [D] ---------> [2] -> [3]      answer is D.next
```

## How to picture it

Picture **boxes on a table joined by strings**, and you are only allowed to hold a few strings in your hands at once. You
cannot see the whole table. You can only feel along a string from a box you are holding to the next box. Every algorithm
in this chapter is a choreography of a few hands:

- **Reversal**: two chains meeting at a seam. Left of the seam everything points left; right of it everything points
  right. Each step moves one box across the seam.
- **Splicing**: a tail hand that always holds the last box of the output chain, picking up boxes from other chains and
  tying them on.
- **Two runners with a gap**: a ruler of fixed length sliding along the chain. When the front end falls off, the back end
  marks "k from the end".
- **Two runners with different speeds**: a track. On a straight track the fast runner finishes; on a looped track (the
  shape of the Greek letter rho, a tail leading into a circle) the fast runner must lap the slow one.

```text
the rho shape of a list with a cycle:

 [1] -> [2] -> [3] -> [4]
                ^      |
                |      v
               [6] <- [5]

 tail = 1, 2      loop entrance = 3      loop length = 4
```

Why must the fast runner catch the slow one? Once both are inside a loop of length c, measure the gap as "how many steps
fast is behind slow, going forward". Each tick slow adds one step and fast adds two, so the gap shrinks by exactly one.
A gap that starts somewhere in 0..c-1 and shrinks by one per tick hits 0 in fewer than c ticks. It cannot skip over 0,
because it moves by one. That is the whole proof, and it reappears in three problems.

Three primitives carry most of the chapter. Learn them until you can write them without thinking:

1. **Reverse** (prev, cur, nxt): flips a chain in one pass.
2. **Find middle** (slow, fast): splits a chain in half in one pass.
3. **Splice** (dummy, tail): builds an output chain by attaching nodes to `tail.next` and advancing `tail`.

The palindrome, reorder, and k-group problems are these three stitched together.

## Signals in a problem statement

- "Given the head of a linked list" plus "in place" or "O(1) extra memory": you must rewire arrows, not copy to an array.
- "Reverse", "rotate", "swap pairs", "k at a time": the prev/cur/nxt reversal, possibly bounded to a block.
- "Merge", "sorted lists", "combine", "digits stored in reverse order": dummy head and a tail pointer.
- "n-th from the end", "middle", "last k": two runners, either with a fixed gap or with speeds 1 and 2.
- "Cycle", "loop", "does it ever repeat", "where does it start": Floyd's fast and slow pointers.
- An array of n+1 values each in [1, n], with "no modification" and "O(1) space": treat `i -> nums[i]` as a linked list
  and look for a cycle.
- "Two lists that merge", "intersection node": equalise the remaining lengths, then walk in lockstep.
- "Deep copy" with extra pointers (`random`, `child`): you need an old-to-new mapping, stored in a dict or woven into the
  list itself.

Counter-signals:

- Random access by position ("the element at index i") repeatedly: convert to an array, or use a different structure.
- "Sort a linked list" with no space limit: copying values to a list and sorting is acceptable; merge sort on the list is
  the in-place answer, and that belongs with divide and conquer.
- "LRU cache", "O(1) get and put": a doubly linked list plus a hash map is a design problem, covered in the design chapter.
- k sorted lists rather than two: you still splice, but the "which head is smallest" question needs a heap.

## Python toolbox

Python has no built-in singly linked list type; LeetCode gives you a class like this one.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next
```

Two helpers make testing painless: build from a Python list, and read back into one.

```python
def build(vals):
    dummy = tail = ListNode()
    for v in vals:
        tail.next = tail = ListNode(v)   # careful: see below
    return dummy.next
```

That chained assignment works because Python assigns targets left to right: `tail.next` first (old tail), then `tail`.
Tuple assignment follows the same rule and is where many reversals break:

```python
# right side evaluated first, then targets left to right
cur.next, prev, cur = prev, cur, cur.next  # correct
prev, cur, cur.next = cur, cur.next, prev  # WRONG: sets .next
                                           # on the NEW cur
```

Other things worth knowing:

- Compare nodes with `is`, not `==`. Two different nodes can hold the same value; cycle and intersection questions are
  about identity.
- `collections.deque` is a doubly linked list of blocks, useful when you need O(1) at both ends, but it is not something
  you can rewire node by node.
- Recursive list algorithms use one stack frame per node. Python's default recursion limit is about 1000, so a recursive
  reversal of a 5000-node list crashes. Prefer the loop.
- `id(node)` or the node itself can go in a `set` or `dict` as a key; nodes hash by identity by default.

## Mistakes people make

1. **Overwriting `cur.next` before saving it.** Fix: `nxt = cur.next` is always the first line of the loop body.
2. **Special-casing the head and getting it wrong.** Fix: put a dummy node in front and return `dummy.next`.
3. **Returning the old `head` after a reversal.** Fix: the old head is now the tail; return `prev`.
4. **Dereferencing `None`.** `fast.next.next` crashes when `fast.next` is `None`. Fix: loop on `while fast and fast.next`.
5. **Forgetting the leftover tail when merging.** Fix: after the loop, `tail.next = l1 or l2`.
6. **Checking `slow is fast` before the first move.** They start on the same node. Fix: move first, then compare.
7. **Comparing values instead of nodes.** Fix: use `is`; equal values do not mean the same node.
8. **Off-by-one in the gap.** To stop on the node before the target, the gap must be n+1 links, not n. Fix: draw it with
   n = 1 and check.
9. **Leaving a stray arrow that creates a cycle.** After splitting or reordering, the new last node may still point into
   the other half. Fix: explicitly set the new tail's `next` to `None`.
10. **Tuple assignment in the wrong order.** Fix: write the save, flip, advance as three separate lines until it is
    second nature.

## The journey ahead

1. **Reverse Linked List** adds the prev/cur/nxt reversal and the "save next first" rule.
2. **Merge Two Sorted Lists** adds the dummy head and the tail pointer that splices existing nodes.
3. **Add Two Numbers** keeps the dummy and tail but creates new nodes and threads a carry through the walk.
4. **Remove Nth Node From End** adds two runners with a fixed gap, and uses the dummy so the head can be deleted.
5. **Linked List Cycle** adds two runners with different speeds and the "gap shrinks by one" argument.
6. **Linked List Cycle II** turns the meeting point into a ruler: tail length equals meeting-to-entrance distance.
7. **Find the Duplicate Number** shows that an array of pointers is a linked list, so the same two phases find the repeat.
8. **Intersection of Two Linked Lists** uses lockstep walking after equalising lengths, the gap idea in reverse.
9. **Palindrome Linked List** is the first combination: find the middle, reverse the second half, compare.
10. **Reorder List** reuses all three primitives: middle, reverse, then splice the halves alternately.
11. **Copy List with Random Pointer** adds the old-to-new mapping, then removes the map by weaving clones into the list.
12. **Reverse Nodes in k-Group** bounds the reversal to blocks and reconnects each block, the hardest bookkeeping of all.
