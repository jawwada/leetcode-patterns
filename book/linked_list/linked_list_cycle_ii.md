# Linked List Cycle II

*LeetCode 142 · Medium · Pattern: Floyd's tortoise and hare (fast/slow pointers) · Reading time ~9 min*

## What the problem is really asking

If following `next` from the head eventually loops, return the node where the loop begins: the first node you visit
twice. If there is no loop, return `None`. You may not modify the list, and the follow-up asks for O(1) memory.

The answer is a node reference, not a value and not an index. The previous problem told us **whether** there is a loop.
This one asks **where** it is entered, which is harder because the race in the previous problem ends at some arbitrary
node inside the loop, not at the entrance.

```text
 [1] -> [2] -> [3] -> [4]
                ^      |
                |      v
               [6] <- [5]

 tail:     1, 2           (a = 2 nodes before the loop)
 entrance: 3              <- the answer
 loop:     3, 4, 5, 6     (c = 4 nodes)
```

## Do it by hand first

By hand you would do what you did last time: follow the arrows with a finger, tick each node, and stop at the first node
that already has a tick. That node is the entrance, because (when there is a tail) the entrance is the only node with two arrows coming into it
(one from the tail, one from the end of the loop), so it is the first one you can reach a second time.

```text
 visit:  1  2  3  4  5  6  3
 ticks:  v  v  v  v  v  v  v  <- first repeat = entrance
```

Your hand tracked the set of visited nodes again. This time the set does give the answer directly, which is why the
brute force is natural. The challenge is to get the same node with two references instead of a set.

## The first honest attempt

Walk the list, storing each node in a hash set; return the first node already in the set, or `None` at the end. O(n)
time, O(n) space.

The waste is the same as before: we store every node on the path to discover one fact about the shape. The shape is
fully described by two numbers, the tail length a and the loop length c, and the entrance is simply "the node a steps
from the head".

```text
 set stores: {1, 2, 3, 4, 5, 6}     6 references
 shape:      a = 2, c = 4           2 numbers
 answer:     walk a = 2 steps from head
```

If we could measure a without storing the path, one walk of a steps from the head would land on the entrance. We do not
know a. But the race from the previous problem leaves behind a clue.

## The turning point

**Claim: after the fast and slow pointers meet, the distance from the head to the entrance equals the distance from the
meeting point forward to the entrance, up to whole laps of the loop. So two pointers, one from the head and one from the
meeting point, moving one step at a time, meet exactly at the entrance.**

Here is the arithmetic. Let the race run t ticks until the meeting. Slow has taken t steps, fast 2t steps. Name the
pieces:

```text
 head --- a steps ---> E (entrance) --- b steps ---> M (meet)
                       |<------- loop of c nodes ------->|

 slow walked:  t  = a + b                 (+ any laps)
 fast walked:  2t = a + b + (some laps)
```

Both pointers stand on the same node M, so the extra distance fast covered, 2t - t = t, must be a whole number of laps:
t = k * c for some k >= 1. Slow's distance is t = a + b (slow is caught before it finishes its first lap, a fact from the
gap argument in the previous problem). So:

```text
 a + b = k * c
     a = k * c - b
       = (c - b) + (k - 1) * c
```

Read the last line as a walk. Start at M, which is b steps past E. Walking c - b steps brings you around to E. Walking
(k - 1) more full laps keeps you at E. So **walking a steps from M lands on E**. Walking a steps from the head also lands
on E, by the definition of a.

We still do not know a, but we do not need to. Put one pointer at the head and leave the other at M. Advance both one
step at a time. After exactly a steps both are on E, and they cannot meet earlier, because before that the head pointer
is still on the tail, where no node is in the loop. So the first node where they coincide is the entrance.

The algorithm is two phases, two references, no set:

1. Race slow (1 step) and fast (2 steps) from the head. If fast falls off, return `None`. Stop when `slow is fast`.
2. Reset one pointer to the head. Move both one step at a time until they are the same node. Return it.

## Watch it work

List `1 -> 2 -> 3 -> 4 -> 5 -> 6`, with 6 pointing back to 3. So a = 2, c = 4, entrance E = node 3. `s` is slow,
`f` is fast, `p` is the phase 2 pointer from the head.

```text
Frame 1: phase 1, tick 1   s = 2, f = 3
 [1] -> [2] -> [3] -> [4]
         s      f      |
                ^      v
               [6] <- [5]
```

Both started on node 1. Fast is already at the entrance; slow is still on the tail.

```text
Frame 2: phase 1, tick 2   s = 3, f = 5
 [1] -> [2] -> [3] -> [4]
                s      |
                ^      v
               [6] <- [5]
                       f
```

Slow enters the loop after a = 2 ticks. Fast is 2 steps behind it (5 -> 6 -> 3).

```text
Frame 3: phase 1, tick 3   s = 4, f = 3
 [1] -> [2] -> [3] -> [4]
                f      s
                ^      |
               [6] <- [5]
```

Fast went 5 -> 6 -> 3. The gap shrank to 1.

```text
Frame 4: phase 1, tick 4   s = 5, f = 5   MEET
 [1] -> [2] -> [3] -> [4]
                ^      |
                |      v
               [6] <- [5]
                      s,f
```

They meet at M = node 5 after t = 4 ticks. M is b = 2 steps past E, and t = a + b = 4 = 1 * c, so k = 1 and
c - b = 2 = a.

```text
Frame 5: phase 2, step 1   p: 1 -> 2,  s: 5 -> 6
 [1] -> [2] -> [3] -> [4]
         p             |
                ^      v
               [6] <- [5]
                s
```

`p` started on the head, `s` stayed at the meeting point; both moved one step. Different nodes, continue.

```text
Frame 6: phase 2, step 2   p: 2 -> 3,  s: 6 -> 3
 [1] -> [2] -> [3] -> [4]
               p,s     |
                ^      v
               [6] <- [5]
 return node 3
```

After a = 2 steps both pointers sit on node 3, the entrance.

In phase 1 the gap between fast and slow, once both were in the loop, fell by one each tick (2, 1, 0). In phase 2 the two
pointers were always the same number of steps from E (2, 1, 0), one along the tail and one around the loop.

## Why it is correct

No cycle: fast reaches `None` and the first phase returns `None`, exactly as in the previous problem.

Cycle: phase 1 ends with both pointers on some node M. Slow entered the loop after a ticks and was caught within fewer
than c further ticks, so slow's total distance is t = a + b with 0 <= b < c, where b is M's offset from E. Fast's
distance is 2t, and since both stand on M inside the loop, 2t - t = t is a multiple of c. Hence a = k*c - b for some
k >= 1, which says that a steps forward from M is E.

Phase 2 invariant: after i steps, `p` is i steps from the head and the other pointer is i steps past M. For i < a, `p` is
on the tail, and no tail node is in the loop, so they differ. At i = a both are on E. The loop therefore stops exactly
at the entrance.

The edge case a = 0 (the head is in the loop): phase 2 starts with `p` on the head and the other pointer on M, and
a = 0 means M is k laps from E, so M is E and they are already equal; the loop body never runs.

## Cost

- Time: O(n). Phase 1 takes a + b < a + c <= n ticks. Phase 2 takes a <= n steps.
- Space: O(1), three references, no set.

The whole gain over the set is memory, which is what the follow-up asks for.

## Variations you will meet

- **Find the Duplicate Number** (LeetCode 287), the next problem. An array with values in [1, n] defines arrows
  `i -> nums[i]`. The duplicate value has two arrows coming into it, which makes it the entrance of a cycle. The same two
  phases find it in O(1) space without modifying the array.
- **Length of the loop.** After the meeting, hold one pointer still and walk the other until it returns; the step count
  is c.
- **Remove the cycle.** Find the entrance, then walk the loop until the node whose `next` is the entrance, and set that
  `next` to `None`.

## What to carry forward

The meeting point is as far from the entrance (mod the loop length) as the head is, so restart one runner at the head
and walk both one step at a time. The next problem has no linked list at all, only an array, and the trick is seeing that
its values are arrows whose cycle entrance is the answer.
