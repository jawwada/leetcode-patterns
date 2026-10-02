# Max Points on a Line

*LeetCode 149 · Hard · Pattern: Anchor point + slope as a reduced fraction · Reading time ~8 min*

## What the problem is really asking

You get up to 300 distinct points with integer coordinates (absolute value up to `10^4`). Find the largest number of them that sit on one straight line.

The answer is a count. A line is determined by any two of its points, so the question is really "which pair of points defines the line that the most other points also lie on?" What makes it hard is not speed — `n` is small — but *exactness*. Deciding whether three points are collinear by comparing floating-point slopes invites rounding errors and division by zero, and a correct-looking solution fails on a hidden test with large coordinates or a vertical line.

```text
 points A(1,1) B(3,2) C(5,3) D(4,1) E(2,3) F(1,4)
 y
 4  F  .  .  .  .
 3  .  E  .  .  C
 2  .  .  B  .  .
 1  A  .  .  D  .
    1  2  3  4  5  x
 best line: F E B D (slope -1), 4 points
```

## Do it by hand first

With a ruler you would pick a point and swing the ruler around it, noting which other points line up. Put the pivot on `B(3,2)`:

```text
 from B, the "arrows" to every other point
   to C(5,3): (+2,+1)
   to D(4,1): (+1,-1)
   to E(2,3): (-1,+1)   same line as (+1,-1), other side
   to F(1,4): (-2,+2)   same direction as (-1,+1), longer
   to A(1,1): (-2,-1)   same line as (+2,+1)
```

`D`, `E` and `F` all lie along the direction "one right, one down" from `B` — some ahead of it, some behind. With `B` itself that is 4 points. Your hand grouped arrows by *direction*, ignoring length and ignoring which way along the line they point. That grouping is the seed: a hash map from direction to count, from one pivot.

## The first honest attempt

A line is fixed by two points. For every pair `(i, j)`, scan all points `k` and count those collinear with `i` and `j`. Collinearity is tested exactly with the cross product: `(xj-xi)(yk-yi) - (yj-yi)(xk-xi) == 0`. Keep the maximum.

That is `O(n^3)`: about `2.7 * 10^7` cross products for `n = 300`, borderline but exact.

Where is the repeated work? A line holding `c` points is rediscovered once for *every pair* on it, `c(c-1)/2` times, and each rediscovery rescans all `n` points.

```text
 line F-E-B-D found by every pair on it
   (F,E) (F,B) (F,D) (E,B) (E,D) (B,D)   6 times
   each time: scan all 6 points again
```

## The turning point

**Claim: fix an anchor point `P`; two other points `Q` and `R` lie on one line through `P` if and only if their direction vectors from `P`, reduced by their gcd and normalised in sign, are equal.**

Justify it. `Q` and `R` are collinear with `P` iff the vectors `Q - P = (dx1, dy1)` and `R - P = (dx2, dy2)` are parallel, i.e. one is a nonzero rational multiple of the other. Dividing each vector by the gcd of its components gives the unique *primitive* vector in that direction: `(4, 2) -> (2, 1)`, `(-6, -3) -> (-2, -1)`. Two vectors are parallel iff their primitive forms are equal *or opposite*. Flipping sign so that `dx > 0`, or `dx == 0 and dy > 0`, picks one of the two opposite forms canonically. So the canonical pair is a perfect hash key for "line through `P`".

```text
 canonical direction keys
   raw (dx,dy)   gcd   reduced    sign fix   key
   (+2,+1)        1    (2,1)      keep       (2,1)
   (-2,-1)        1    (-2,-1)    flip       (2,1)
   (-2,+2)        2    (-1,1)     flip       (1,-1)
   (+1,-1)        1    (1,-1)     keep       (1,-1)
   (0,-5)         5    (0,-1)     flip       (0,1)   vertical
   (+3,0)         3    (1,0)      keep       (1,0)   horizontal
```

Why not use `dy / dx` as a float? Two reasons. Vertical lines divide by zero. And floats can't represent most fractions exactly, so two mathematically equal slopes computed from different points (`1/3` versus `3333/9999`) are not guaranteed to produce the same bits. The reduced integer pair is exact and has no special cases: vertical lines become `(0, 1)`, horizontal lines `(1, 0)`.

Turning the claim into an algorithm: for each anchor `i`, build a `Counter` of keys over the other points; the best line through `i` has `max(counter) + 1` points (the `+1` is the anchor). Take the maximum over anchors.

A Python detail makes the normalisation painless. `math.gcd` always returns a non-negative number, even for negative arguments, and since the points are distinct it is strictly positive. So `dx // g` and `dy // g` are exact divisions that keep the original signs, and the sign fix afterwards is a single comparison. In Java or C++ you would write your own gcd and take its absolute value before dividing, or the signs can come out inconsistent.

One more saving: only look at `j > i`. Why is that enough? Take the best line and let `i` be the smallest index among its points. When `i` is the anchor, every other point on that line has a larger index, so all of them are counted. Lines whose smallest-index point is earlier were already counted with that earlier anchor.

```text
 y
 4  F                 F, E, D share key (1,-1) from B
 3     E        C     C shares key (2,1) with A
 2        B
 1  A        D
    1  2  3  4  5   x
 counted from B (j > i only): (1,-1): D,E,F   (2,1): C
```

## Watch it work

Example: the six points `A(1,1) B(3,2) C(5,3) D(4,1) E(2,3) F(1,4)` in that index order. Each frame is one anchor, looking only at later points.

Frame 1 — anchor `A(1,1)`, later points `B C D E F`.

```text
 B:(2,1)  C:(4,2)->(2,1)  D:(3,0)->(1,0)
 E:(1,2)  F:(0,3)->(0,1)
 counter {(2,1):2, (1,0):1, (1,2):1, (0,1):1}
 best through A = 2 + 1 = 3 (A,B,C)      best = 3
```

Frame 2 — anchor `B(3,2)`, later points `C D E F`. Three of them share key `(1,-1)`.

```text
 C:(2,1)  D:(1,-1)  E:(-1,1)->(1,-1)
 F:(-2,2) /2 -> (-1,1) -> (1,-1)
 counter {(2,1):1, (1,-1):3}
 best through B = 3 + 1 = 4 (B,D,E,F)    best = 4
```

Frame 3 — anchor `C(5,3)`, later points `D E F`. All different.

```text
 D:(-1,-2)->(1,2)  E:(-3,0)->(1,0)  F:(-4,1)->(4,-1)
 counter {(1,2):1, (1,0):1, (4,-1):1}
 best through C = 2                      best = 4
```

Frame 4 — anchor `D(4,1)`, later points `E F`.

```text
 E:(-2,2)->(1,-1)  F:(-3,3)->(1,-1)
 counter {(1,-1):2}
 best through D = 3 (same line, seen from D) best = 4
```

Frame 5 — anchors `E` (one later point, key `(1,-1)`, gives 2) and `F` (no later points). Final answer `4`.

```text
 E: F:(-1,1)->(1,-1)   counter {(1,-1):1} -> 2
 F: no later points    counter {}
 answer = 4
```

What stayed invariant: within one anchor's counter, each key corresponds to exactly one line through the anchor, and its count is the number of later points on that line. Across anchors, `best` is the largest line found among anchors processed so far, and the line `F-E-B-D` was found complete at its earliest-indexed member `B`.

## Why it is correct

*Keys are faithful.* For a fixed anchor `P`, the map `Q -> canonical(Q - P)` sends `Q` and `R` to the same key iff `P, Q, R` are collinear (shown in the turning point). Points are distinct, so `Q - P != (0, 0)` and the gcd is positive. Hence, for each key, its count is exactly the number of points (among those examined) on that line through `P`, and `count + 1` is the number of points on that line including `P`.

*Every line is counted in full somewhere.* Let `L` be a line with the maximum number of points, and let `P` be its point with the smallest index. When `P` is the anchor, all other points of `L` have larger indices, so they are all examined, and they all share one key. Thus `best >= |L|`.

*Nothing is overcounted.* Every value `count + 1` that updates `best` is the size of an actual set of collinear points, so `best <= |L|`.

With one point the loop sees no pairs and `best` stays `1`.

## Cost

- **Time:** `O(n^2 log C)` — `n(n-1)/2` pairs, each with a gcd on coordinates up to `C = 2 * 10^4`.
- **Space:** `O(n)` — one counter, reset per anchor.

The brute force was `O(n^3)`; the hash map removes the inner rescan by grouping each anchor's lines in one pass.

## Variations you will meet

- **Duplicate points allowed** (the original version of this problem). Count duplicates of the anchor separately and add them to every line through it: `best = max(best, max(counter) + dup + 1)`. Duplicates have `(0, 0)` direction, which must not go into the counter.
- **Lines that need not pass through two given points, e.g. "minimum lines to cover all points" (LeetCode 2152).** With `n <= 10`, enumerate lines from pairs and do bitmask DP over covered points. The collinearity test is still the integer cross product.
- **Count collinear triples, or "is there any line with `>= k` points?"** Same anchor-plus-counter; sum `C(count, 2)` per key for triples.
- **Using a string or a float with rounding as the key.** Common in discussions and fragile. If a language lacks tuple keys, encode the reduced pair as `dx * BIG + dy` with `BIG` larger than any `dy` range, never as a float slope.

## What to carry forward

To group geometric objects by an exact property, find a canonical integer form (gcd-reduce, fix the sign) and hash it; never let a float decide equality.

The next problem, Perfect Rectangle, stays with exact integer geometry, but instead of grouping points by slope it certifies a whole tiling using two invariants: total area and how often each corner appears.
