# Linked Lists

*12 problems · Reading time ~27 min*

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

## Advanced patterns

The three primitives above solve the Easy problems almost by themselves. The Medium and Hard problems ask for something
more: an argument for why a pointer ends up where it does, or a way to fit an extra piece of state into memory you are not
allowed to use. The six patterns below are those ideas. Each one is small once you have seen it, and none of them is
obvious the first time.

### Bounded reversal with a pre-attached tail

**When it shows up**: only part of the list is reversed (positions left..right, every block of k, pairs), and the reversed
piece has to stay connected to what comes before and after it.

**The intuition**: a whole-list reversal starts with `prev = None` because the old head becomes the new tail and must point
at `None`. In a bounded reversal the old head of the block also becomes its tail, but it must point at the first node
*after* the block. So start with `prev` set to that node. The first flip then attaches the block to its right neighbour,
and the right side never needs a separate fix. What is left is one link on the left: the node before the block still
points at the old head, which is now the block's tail. Save that old head, hook the left neighbour onto the new head, and
the old head is exactly the "node before the next block". Before you flip anything, walk k steps ahead to confirm the
block is full; if the lookahead hits `None`, you have touched nothing and the short tail stays in order for free.

```text
 k = 3, gp = node before the block

 lookahead:  gp -> 1 -> 2 -> 3 -> 4 -> 5
                             kth  nxt
 start:      prev = nxt (4), cur = 1

 after 2 flips (1.next = 4, then 2.next = 1):
             gp -> 1 -> 4 -> 5     1 born attached
             2 -> 1                cur = 3 -> 4 still
             ^ prev
 after flip 3 (3.next = 2), cur == nxt, stop:
             3 -> 2 -> 1 -> 4 -> 5    gp still -> 1
 stitch:     old gp.next = 3 ; gp = 1
        old gp -> 3 -> 2 -> 1 -> 4 -> 5
                            ^ new gp
```

**Where you'll use it**: Reverse Nodes in k-Group is this pattern in a loop. Beyond the chapter, Reverse Linked List II
(LeetCode 92) is one block of it and Swap Nodes in Pairs (LeetCode 24) is the k = 2 case.

### Floyd's two phases: the meeting point as a ruler

**When it shows up**: you must find *where* a loop begins, not just whether one exists, with O(1) memory.

**The intuition**: name the pieces. The tail before the loop has a steps, the loop has c nodes, and slow and fast meet b
steps past the entrance. When they meet, slow has walked a + b and fast has walked twice that. They stand on the same node,
so fast's extra distance, also a + b, is a whole number of laps: a + b = k * c. Rewrite it as a = (c - b) + (k - 1) * c.
From the meeting point, c - b steps bring you round to the entrance and extra whole laps keep you there. So walking a
steps from the meeting point lands on the entrance, and walking a steps from the head also lands on the entrance. You
never learn a; you just start one pointer at each place and step them together until they coincide.

```text
 the rho from earlier: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 3
 a = 2 (nodes 1, 2), c = 4 (3, 4, 5, 6)

 phase 1 (slow +1, fast +2)   phase 2 (both +1)
 tick  slow  fast             step  from head  from meet
  1     2     3                0       1          5
  2     3     5                1       2          6
  3     4     3                2       3          3  <- entry
  4     5     5  <- meet, b = 2
 check: a + b = 4 = 1 * c ; c - b = 2 = a
```

**Where you'll use it**: Linked List Cycle (phase 1 only), Linked List Cycle II (both phases), Find the Duplicate Number
(both phases on an array). Beyond the chapter, Happy Number (LeetCode 202) runs phase 1 on a sequence of digit sums.

### The array that is secretly a linked list

**When it shows up**: an array of n + 1 values, each a valid index (1..n), with "do not modify" and "O(1) extra space".
Any time `x = f(x)` is iterated over a finite set, you are walking a list whose `next` is `f`.

**The intuition**: read index i as a node and `nums[i]` as its `next` pointer. Every value is a legal index, so no arrow
falls off; a walk from index 0 can never stop, and with finitely many nodes it must eventually repeat. That forces the rho
shape. No value is 0, so nothing points into index 0, which makes index 0 a tail node and never part of the loop. The
loop's entrance has two incoming arrows, one from the tail and one from inside the loop: two different indices holding
the same value. That value is the duplicate. The problem has turned into Floyd's two phases with `node.next` replaced by
`nums[i]`.

```text
 index:  0   1   2   3   4
 nums:  [1,  3,  4,  2,  2]

 0 -> 1 -> 3 -> 2 -> 4
                ^    |
                +----+       entrance = 2 (arrows from 3 and 4)

 phase 1 (slow, fast): (1,3) (3,4) (2,4) (4,4) meet at 4
 phase 2 (head, meet): (0,4) (1,2) (3,4) (2,2) -> answer 2
```

**Where you'll use it**: Find the Duplicate Number. The same reading powers First Missing Positive and "cyclic sort"
problems in the arrays chapter, where you follow `i -> nums[i]` to place values.

### Equalise the remaining distance, then walk in lockstep

**When it shows up**: two lists that may share a tail, or any time two pointers must arrive somewhere "at the same moment"
but start at different distances from it.

**The intuition**: once two lists merge, they share every node to the end, so the merge node is the same distance from the
end in both. If two pointers start equally far from the end and step together, they stay equally far from the end, so
they reach the merge node on the same step and cannot be equal earlier. Counting both lengths and advancing the longer
list by the difference sets that up. A slicker version needs no counting: each pointer walks its own list and then
switches to the head of the other. Pointer A travels (A's private part) + (shared) + (B's private part); pointer B travels
the same three pieces in a different order. The totals are equal, so after both have switched, they are the same
distance from the merge node. If the lists never merge, both reach `None` together and `None is None` ends the loop.

```text
 A: a1 a2 \                 private A = 2
           c1 c2 c3         shared    = 3
 B: b1 b2 b3 /              private B = 3

 step:   0  1  2  3  4  5  6  7  8
 pA:    a1 a2 c1 c2 c3 b1 b2 b3 c1  <- same node
 pB:    b1 b2 b3 c1 c2 c3 a1 a2 c1     at step 8
         2 + 3 + 3  ==  3 + 3 + 2
```

**Where you'll use it**: Intersection of Two Linked Lists. Remove Nth Node From End is the one-list cousin: there you
create the distance on purpose (a fixed gap) instead of cancelling it.

### Fold the list: split, reverse the back, weave

**When it shows up**: the answer pairs the i-th node from the front with the i-th node from the back (palindrome checks,
"L0, Ln, L1, Ln-1, ..." orderings, twin sums).

**The intuition**: a singly linked list cannot walk backwards, but after you reverse the back half it does not need to.
"The i-th from the back" becomes "the i-th of the reversed half", an ordinary forward walk, so two forward pointers can
move in lockstep. Three choices decide whether it works. Which middle: with `while fast and fast.next`, slow stops on the
middle (odd length) or the right-middle (even); with `while fast.next and fast.next.next`, slow stops on the last node of
the front half, which is the node you need if you plan to cut. Cut: set the front half's last `next` to `None`, or the
weave will create a cycle. Weave: save both nexts before writing either link.

```text
 reorder 1 -> 2 -> 3 -> 4 -> 5

 middle (fast.next and fast.next.next): slow on 3
 cut:      1 -> 2 -> 3 -> None     4 -> 5 -> None
 reverse:  1 -> 2 -> 3             5 -> 4
           ^ first                 ^ second
 weave:    1 -> 5 -> 2 -> 4 -> 3 -> None

 slow stops on   n = 4   n = 5   n = 6
 fast&&fast.next   3       3       4
 f.next&&f.n.next  2       3       3
```

**Where you'll use it**: Palindrome Linked List (compare instead of weave), Reorder List (weave). Beyond the chapter,
Maximum Twin Sum of a Linked List (LeetCode 2130) is the same fold with a sum.

### Weave the clones into the original instead of using a hash map

**When it shows up**: you must deep-copy a list whose nodes carry an extra pointer (`random`, `child`) to arbitrary other
nodes, and you want O(1) extra space beyond the copy.

**The intuition**: setting a copy's `random` needs one question answered in O(1): "given original X, where is X's copy?"
A dictionary answers it. So does position: insert each copy directly after its original, and "the copy of X" is just
`X.next`. Then a copy's random is one hop: `X.next.random = X.random.next`. The order of the three passes is the whole
trick. Every copy must exist before any random is set, because the hop needs the target's copy to be there. Every random
must be set before you unweave, because once unwoven, `X.next` no longer means "my copy". Unweaving restores the original
list exactly.

```text
 original:  A -> B -> C       random: A->C  B->A  C->None

 pass 1 weave:   A -> A' -> B -> B' -> C -> C' -> None
 pass 2 random:  A'.random = A.random.next = C.next = C'
                 B'.random = B.random.next = A.next = A'
 pass 3 unweave: A -> B -> C          A' -> B' -> C'
```

**Where you'll use it**: Copy List with Random Pointer. The idea of storing a map in the structure itself (in spare
pointers, signs, or positions) returns in Flatten a Multilevel Doubly Linked List (LeetCode 430) and in the arrays chapter.

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

The order is built so that each problem needs exactly one idea you have not used yet, and the last one needs all the
bookkeeping habits at once.

### Warm-up: two primitives

**Reverse Linked List.** The puzzle is that the result is obvious and the code is not: the moment you point a node
backwards, you lose the road forwards. The fix is the prev/cur/nxt walk and the rule that `nxt` is saved before any
arrow is written. Everything later in the chapter assumes you can write this loop half asleep.

**Merge Two Sorted Lists.** Now you build a list instead of flipping one. The naive version special-cases "which node is
the new head?"; the dummy node makes that question disappear, and a tail pointer that only ever moves forward splices
existing nodes in without creating any. This is the second primitive.

**Add Two Numbers.** Same dummy and tail, but the output nodes are new, the two inputs can have different lengths, and a
carry rides along. The interesting question is when to stop: not when both lists end, but when both lists end *and* the
carry is zero, which a single loop condition captures.

### Two runners

**Remove Nth Node From End.** Counting the length and walking again is two passes; can you do it in one? Two runners with a
fixed gap measure "distance from the end" without knowing the length. The off-by-one (stop on the node *before* the
target) and the dummy (so the head itself can be removed) are where the care goes.

**Linked List Cycle.** A set of visited nodes works, but the problem asks for O(1) memory. Running at different speeds
replaces the set: on a loop the gap closes by one per tick, so the fast runner cannot jump over the slow one. This is the
first problem where the answer is a proof, not a rewiring.

**Linked List Cycle II.** Knowing a loop exists is not knowing where it starts, and the meeting point looks arbitrary. A
few lines of arithmetic show it is not: it sits exactly as far from the entrance as the head does, up to whole laps. The
new idea is turning a meeting point into a ruler.

**Find the Duplicate Number.** There is no list here at all, only an array you may not modify. Reading `i -> nums[i]` as
an arrow turns it into a linked list with a loop whose entrance is the duplicate. The new idea is recognising the list
hidden in another structure; the code is the previous problem's.

**Intersection of Two Linked Lists.** Two lists with private prefixes of different lengths share a tail. Comparing values
is the trap, and a set of nodes is the easy way out. The new idea is cancelling a distance instead of creating one: line
the pointers up so they are equally far from the end, then walk together.

### Combining primitives

**Palindrome Linked List.** You need the back of the list in reverse order, and a singly linked list will not walk
backwards. Copying values to an array is O(n) space; the O(1) answer combines two primitives: find the middle, reverse the
back half, compare forwards. The new skill is choosing the right middle for the job.

**Reorder List.** The same fold, but instead of comparing you weave the halves together, so every pointer write now
matters. It adds the cut (forget it and you build a cycle) and the zip with two saved nexts. All three primitives appear in
one function.

### The far end

**Copy List with Random Pointer.** Cloning `next` is easy; cloning `random` is hard because its target's copy may not exist
yet. The hash-map solution is fine; the deeper idea is that the map can live in the list itself, with each clone woven
right after its original. Order of the three passes is everything.

**Reverse Nodes in k-Group.** The only Hard, and it contains no new primitive: it is the first problem's reversal, bounded
to k nodes, repeated. What makes it hard is the glue: look ahead before flipping, start `prev` at the right neighbour so
each block is born attached, and stitch the left side with one saved pointer. If the earlier problems have made "save
before you overwrite" automatic, this one is a careful page of bookkeeping rather than a wall.
