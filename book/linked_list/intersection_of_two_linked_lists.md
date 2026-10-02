# Intersection of Two Linked Lists
*LeetCode 160 · Easy · Pattern: Length alignment, then lockstep walk · Reading time ~6 min*

## What the problem is really asking

Two singly linked lists may, at some node, start sharing the rest of their nodes. Return the first shared node, or None if they never meet. "Shared" means the *same node object*, not an equal value. You may not change the lists, and they have no cycles.

The answer is a node reference. What makes it hard: each list only knows how to walk forward, the private parts before the merge have different lengths, and equal values are a trap.

```text
  A:  a1(4) -> a2(1) --+
                       v
                       c1(8) -> c2(4) -> c3(5) -> None
                       ^
  B:  b1(5) -> b2(6) -> b3(1)
                      answer: c1 (the node holding 8)
```

Note that a2 and b3 both hold the value 1 but are different nodes. The merge is at c1.

## Do it by hand first

Look at the drawing: the two lists form a Y. You would not compare every node of A against every node of B. You would notice that the bottom of the Y is common, so both lists *end* together. Line them up by their ends:

```text
  A:        4  1  8  4  5
  B:     5  6  1  8  4  5
                  ^ same column, same node
```

Once right-aligned, you just read down the columns from the left until both rows point at the same node. What your hand kept track of was *how far each node is from the end*. Two nodes can only be the same node if they are the same distance from the end.

## The first honest attempt

For each node of A, walk all of B and check whether that exact node appears. O(m * n) time, O(1) space.

```text
  a1: scan b1 b2 b3 c1 c2 c3   no
  a2: scan b1 b2 b3 c1 c2 c3   no
  c1: scan b1 b2 b3 c1         yes
       ^^^^^^^^ B's prefix re-walked every time
```

The waste is that B is re-scanned from its head for every node of A, although after the merge the two lists move in perfect step.

## The turning point

**Claim: if both pointers start the same number of nodes away from the end, walking them one step at a time makes them arrive at the merge node at the same moment.**

Why: the tails after the merge are literally the same nodes, so the distance from the merge node to the end is the same for both lists. If both pointers start equally far from the end, after the same number of steps they are again equally far from the end. Two nodes on the shared tail at the same distance from the end are the same node. And while either pointer is still in its private prefix, the other is also in its prefix (equal distances), so they cannot be equal by accident.

How do we make the distances equal? Count the lengths m and n. The longer list has |m - n| extra nodes in front; advance its pointer that many steps. Now both are equally far from the end. If there is no intersection, the two pointers simply reach None on the same step, and `a is b` is true for None too, so the same loop returns None.

## Watch it work

A has length m = 5, B has length n = 6.

Frame 1 — lengths counted.

```text
  A:        4  1  8  4  5        m = 5
            a
  B:     5  6  1  8  4  5        n = 6
         b
```

We know B is one node longer, so b must skip one node.

Frame 2 — align.

```text
  A:        4  1  8  4  5
            a
  B:     5  6  1  8  4  5
            b
```

b advanced n - m = 1 step; both pointers are now 5 nodes from the end.

Frame 3 — lockstep step 1.

```text
  A:        4  1  8  4  5
               a
  B:     5  6  1  8  4  5
               b
  a.val == b.val == 1, but a is not b
```

Same value, different node objects, so the loop continues; this is why we compare identity.

Frame 4 — lockstep step 2.

```text
  A:        4  1  8  4  5
                  a
  B:     5  6  1  8  4  5
                  b
  a is b  -> return the node holding 8
```

Both pointers land on the shared node c1 at the same moment.

In every frame both pointers were equally far from the end, so their first coincidence is the first shared node.

## Why it is correct

Let d(x) be the number of nodes from x to the end. After alignment, d(a) = d(b), and each lockstep move lowers both by one, so equality of distances holds at every step. If the lists merge at c, then while d > d(c) both pointers are in private prefixes (different nodes), and at d = d(c) both are at c. If there is no merge, a and b are never the same node until both become None after d steps, and the loop returns None.

## Cost

- **Time: O(m + n).** One pass to count each list, then at most max(m, n) lockstep steps.
- **Space: O(1).** Two pointers and two counters.
- The hash-set version is O(m + n) time and O(m) space.

## Variations you will meet

- **The "switch heads" trick.** Walk a over A then B, and b over B then A. Both travel m + n steps total, so they align automatically without counting.
- **Lists that may contain cycles.** First detect cycles with Floyd. If one list has a cycle and the other does not, they cannot intersect; if both do, check whether their cycles share a node.
- **Lowest Common Ancestor with parent pointers (LeetCode 1650).** Two nodes walking up toward the root form exactly this Y shape; align depths, then climb in lockstep.

## What to carry forward

Shared tails line up from the right; equalise the distance to the end and walk in lockstep. The next problem, Palindrome Linked List, also needs the two ends of a list to line up, but within one list, and it gets there by reversing half of it.
