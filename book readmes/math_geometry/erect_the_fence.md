# Erect the Fence

*LeetCode 587 · Hard · Pattern: Convex hull (monotone chain) · Reading time ~10 min*

## The problem

Given the coordinates of trees in a garden, fence the whole garden with the minimum length of rope and return every
tree that lies on the fence, i.e. on the convex hull boundary including trees on an edge between two corners, in any
order.

```text
Example: [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]] returns
  [[1,1],[2,0],[4,2],[3,3],[2,4]] since (2,2) is strictly
  inside. Example: [[1,2],[2,2],[4,2]] returns all three.
```

## What the problem is really asking

Trees stand at integer points in a garden (up to 3000 of them). Wrap the whole garden with the shortest possible rope. Return every tree that the rope touches — including trees that sit on a straight stretch of rope between two corners.

The answer is a set of points: the *convex hull* boundary, collinear points included. What makes it hard is twofold. First, "shortest rope" has to be turned into something you can test point by point. Second, the collinear requirement breaks the textbook hull algorithm, which deliberately drops points on edges; you need to understand the algorithm well enough to know which single comparison to change.

```text
 trees A(1,1) B(2,0) C(2,2) D(2,4) E(3,3) F(4,2)
 y
 4        D             fence: A -> B -> F -> E -> D -> A
 3           E          C is strictly inside
 2        C     F       answer {A, B, F, E, D}
 1  A
 0        B
    1  2  3  4  x
```

## Do it by hand first

Imagine a rubber band stretched wide and released around nails at the tree positions. It snaps onto the outermost nails. Now walk around the band counter-clockwise, keeping the garden on your *left*. At every nail the band touches, you either turn left or go straight. You never turn right: a right turn would mean the band bends *inward*, and a stretched band cannot do that.

```text
 walking the fence counter-clockwise, garden on the left
   A -> B      heading down-right
   at B        turn LEFT toward F
   at F        turn LEFT toward E
   at E        straight on toward D (F, E, D on x+y=6)
   at D        turn LEFT toward A
   at A        turn LEFT toward B, loop closed
 C: from B going to C then E would be a RIGHT turn at C
```

So the hand's test is "which way do I turn at this post?" That is a local, three-point question, and it is exactly what the cross product answers: `cross(P, Q, R) > 0` is a left turn at `Q` when walking `P -> Q -> R`, `< 0` a right turn, `0` straight. The seed is "fence posts are where you can walk without turning right".

## The first honest attempt

A segment between trees `i` and `j` is part of the fence iff every other tree lies on the same side of its line (or on it). For every pair, compute the cross-product sign of every third tree. If no two signs disagree, the line supports the whole set, and every tree with cross `0` on it is a fence tree.

That is `O(n^3)`: for `n = 3000`, about `2.7 * 10^10` operations. Hopeless.

Where is the waste? `n^2` candidate lines are each tested against all `n` points, but a hull has only `O(n)` edges. Most of the work verifies lines that cut straight through the garden.

```text
 brute force tests every pair, e.g. line A-F:
   D, E above it, B below it -> mixed signs -> not an edge
 that took a full scan; repeat for all 15 pairs of 6 trees,
 and for ~4.5 million pairs of 3000 trees
```

## The turning point

**Claim: if the trees are sorted by `(x, y)`, the lower half of the fence is the sequence you get by sweeping left to right with a stack and popping the top while the last three points make a right (clockwise) turn; the upper half is the same sweep right to left.**

Why does sorting help? The leftmost tree (smallest `x`, then smallest `y`) and the rightmost tree are certainly on the fence. Between them, the fence splits into a *lower chain* (walking left to right along the bottom) and an *upper chain* (walking right to left along the top). Along each chain, `x` never decreases in the walking direction, so visiting points in sorted order visits each chain's points in fence order.

```text
 the two chains, both walked with the garden on the left
   lower chain (left -> right):  A -> B -> F
   upper chain (right -> left):  F -> E -> D -> A
   A and F (the extreme trees) belong to both
```

Now the stack. Process points in sorted order. The stack holds the lower chain *of the points seen so far*. When a new point `p` arrives, look at the top two stack entries `s[-2], s[-1]`. If `s[-2] -> s[-1] -> p` turns right (`cross < 0`), then `s[-1]` lies strictly above the segment `s[-2] -> p`, so it is not on the lower chain of the points seen so far: pop it. Repeat until the turn is left or straight, then push `p`.

```text
 one pop decision: stack [.., P, Q], new point R
              Q                         Q is above P->R:
            /   \                       cross(P,Q,R) < 0
          P       R    -> pop Q         right turn at Q

          P       R                     Q is below P->R:
            \   /      -> keep Q        cross(P,Q,R) > 0
              Q                         left turn at Q
```

This is the same skyline-style monotonic stack you saw with histograms and temperatures, with "is it taller?" replaced by "does it turn right?". Every point is pushed once and popped at most once per chain.

Now the one-character decision that this problem is about. The classic hull pops on `cross <= 0`, removing points on straight stretches, because a hull is usually wanted as a list of *corners*. Here we want every tree the rope *touches*, so a straight step must be kept: pop only on `cross < 0`.

```text
 collinear case: P --- Q --- R on one line, cross = 0
   pop on cross <= 0 : Q removed  (corners only)
   pop on cross <  0 : Q kept     (all rope-touching trees)
```

Finally, the upper chain is built by the same loop over the reversed order. The leftmost and rightmost points end up in both chains, and on a fully collinear input every point appears in both, so return the *set union* of the two chains.

Everything is integer arithmetic: two products and a subtraction per turn test, no angles, no slopes, no `atan2`. That exactness is why `cross == 0` is a trustworthy test for "on the rope".

## Watch it work

Example: the six trees. Sorted by `(x, y)`: `A(1,1) B(2,0) C(2,2) D(2,4) E(3,3) F(4,2)`. Frames 1 to 5 build the lower chain, 6 and 7 the upper.

Frame 1 — push `A`, then `B` (fewer than two points: no test).

```text
 lower stack: [A, B]
   A(1,1) -> B(2,0)
```

Frame 2 — `C(2,2)`: `cross(A, B, C) = 2 > 0`, a left turn. Push. Then `D(2,4)`: `cross(B, C, D) = 0`, straight up the line `x = 2`. Keep (we pop only on `< 0`). Push.

```text
 lower stack: [A, B, C, D]
   B -> C -> D all on x = 2 (cross 0, kept for now)
```

Frame 3 — `E(3,3)`: `cross(C, D, E) = -2`, right turn: pop `D`. `cross(B, C, E) = -2`, right turn: pop `C`. `cross(A, B, E) = 4`, left: push `E`.

```text
 pops: D (cross -2), C (cross -2)
 lower stack: [A, B, E]
   C and D were above the segment B -> E
```

Frame 4 — `F(4,2)`: `cross(B, E, F) = -4`, right turn: pop `E`. `cross(A, B, F) = 4`: push `F`. Lower chain done.

```text
 pop: E (cross -4)
 lower chain: [A, B, F]
```

Frame 5 — upper sweep, reversed order `F E D C B A`. Push `F`, `E`. `D`: `cross(F, E, D) = 0` (line `x + y = 6`), keep, push. `C`: `cross(E, D, C) = 2`, push. `B`: `cross(D, C, B) = 0`, push.

```text
 upper stack: [F, E, D, C, B]
   F -> E -> D straight (kept: E is a rope tree)
   D -> C -> B straight down x = 2 (kept for now)
```

Frame 6 — `A(1,1)`: `cross(C, B, A) = -2`: pop `B`. `cross(D, C, A) = -2`: pop `C`. `cross(E, D, A) = 4`: push `A`.

```text
 pops: B (cross -2), C (cross -2)
 upper chain: [F, E, D, A]
```

Frame 7 — union of the chains: `{A, B, F} | {F, E, D, A}`. `C` is in neither.

```text
 fence = {A, B, F, E, D}     (C(2,2) is inside)
 matches the expected answer
```

What stayed invariant: after each push, every consecutive triple in the stack makes a left turn or goes straight, so the stack is a convex chain of the points processed so far. Collinear points were kept tentatively (`C`, `D` in frame 2) and removed only when a later point proved them to be inside (frame 3).

## Why it is correct

*Invariant for the lower sweep:* after processing the first `t` sorted points, the stack is exactly the lower chain of those `t` points, including points lying on its straight stretches.

When point `p` arrives, it is the rightmost so far (ties broken by `y`), so it is on the lower chain of the first `t + 1` points. A stack point `q` remains on the new lower chain iff it is not strictly above the segment from its predecessor to `p`, which is precisely `cross(prev, q, p) >= 0`. Popping while `cross < 0` removes exactly the points that `p` has made interior; once the top turn is non-negative, every deeper triple already satisfied the condition (they are unchanged), so nothing below needs re-examination. Pushing `p` restores the invariant.

The upper sweep is the mirror argument. The fence is the union of the lower and upper chains, because every boundary tree lies on one of the two, the extreme trees lie on both, and no strictly interior tree survives either sweep (each strictly interior point is strictly above some lower-chain segment and strictly below some upper-chain segment).

## Cost

- **Time:** `O(n log n)` — sorting dominates; each sweep is `O(n)` because each point is pushed once and popped at most once.
- **Space:** `O(n)` — the sorted copy and the two stacks.

The brute force was `O(n^3)`. Gift wrapping (Jarvis march) is `O(nh)` for `h` hull points, good when the hull is tiny but `O(n^2)` in the worst case.

## Variations you will meet

- **Classic hull, corners only.** Pop on `cross <= 0`. Then you can concatenate `lower[:-1] + upper[:-1]` to get each corner exactly once, in counter-clockwise order, without a set.
- **Rope length / hull perimeter / hull area.** Build the corners-only hull, then sum edge lengths (floats are fine at the very end, after all decisions), or use the shoelace formula `sum(x_i * y_{i+1} - x_{i+1} * y_i) / 2` for area, which stays integer until the halving.
- **Is a polygon convex? (LeetCode 469).** Walk the vertices and check that all nonzero cross products of consecutive edge triples share a sign. Same turn test, no sorting.
- **Graham scan.** Sort by angle around the lowest point instead of by `x`, then one stack sweep. Same pop rule, but angle sorting needs a cross-product comparator and careful handling of collinear points at the end of the sweep; monotone chain avoids that by sorting on plain coordinates.

## What to carry forward

A convex boundary is "never turn right": sort, sweep with a stack, pop while the integer cross product says clockwise, and choose `< 0` versus `<= 0` according to whether points on edges count.

This closes the chapter. Looking back, every problem replaced simulation with an exact structure — a coordinate formula, a block size, a digit, an outcome count, a reduced slope, a parity, a turn sign — and the habit to keep is asking, before writing a loop, which exact quantity already contains the answer.
