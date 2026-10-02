# Math and Geometry

*10 problems · Reading time ~12 min*

## Why this chapter exists

Most chapters in this book hand you a data structure and ask you to protect an invariant inside it. This chapter is different. The problems here are solved by *noticing a structure that is already in the input* — a coordinate system, a number system, a count, a geometric sign — and then reading the answer off that structure instead of simulating your way to it. The code is usually short. The thinking is not.

There are four families, and every problem belongs to one of them.

- **Matrices as coordinate systems.** Rotate Image, Spiral Matrix and Set Matrix Zeroes treat a grid not as "a list of lists" but as a set of points `(r, c)` that you move with formulas: reflections, layer walks, and flags stored in the grid's own border.
- **Counting by digit positions.** Permutation Sequence, K-th Smallest in Lexicographical Order and Number of Digit One never list the objects they count. They split the objects into blocks whose sizes are known in closed form, and jump over whole blocks at once.
- **Information counting.** Poor Pigs asks "how few experiments distinguish N possibilities?", and the answer is a product of states per experiment, written in a mixed-radix number.
- **Exact geometry.** Max Points on a Line, Perfect Rectangle and Erect the Fence are about points and shapes on an integer grid. Their common law: never let a float near the decision. Slopes become reduced integer pairs, turns become the sign of a cross product, coverage becomes integer area plus corner parity.

## What it is

Start with the grid, because three problems live on it.

A Python matrix is a list of row lists. Row `r` is one Python object; cell `(r, c)` is element `c` of that object. The picture on the whiteboard and the picture in memory look like this:

```text
 on the board (3 x 3)        in memory
                              matrix --> [ row0, row1, row2 ]
      c=0 c=1 c=2                          |     |     |
 r=0 [ 1   2   3 ]                         v     v     v
 r=1 [ 4   5   6 ]                     [1,2,3] [4,5,6] [7,8,9]
 r=2 [ 7   8   9 ]
                              matrix[1][2] -> row1, index 2 -> 6
```

The key shift is to stop thinking of cells as boxes and start thinking of them as coordinates. Every geometric move of the board is a formula on `(r, c)`:

```text
 move                    (r, c) goes to
 transpose (main diag)   (c, r)
 mirror left<->right     (r, n-1-c)
 mirror top<->bottom     (n-1-r, c)
 rotate 90 clockwise     (c, n-1-r)  = transpose, then mirror
```

A *layer* (or ring) of an `m x n` grid is the border of the sub-rectangle `top..bottom x left..right`. Peeling layers is how you walk a spiral; four integers describe the whole remaining grid.

```text
 layer 0 is the outer ring, layer 1 the next one in
   L     R
 T o o o o      o = layer 0 (top=0,bottom=2,left=0,right=3)
   o x x o      x = layer 1 (top=1,bottom=1,left=1,right=2)
 B o o o o
```

Next, the number systems. A decimal number is a *mixed-radix* number where every radix happens to be 10: the digit in position `p` has weight `10^p`. A *factorial* number system uses weights `0!, 1!, 2!, 3!, ...` and digit `i` ranges over `0..i`. That is exactly the shape of permutations: the first choice has `n` options, each option owns a block of `(n-1)!` permutations, and so on.

```text
 rank r = 8 among the 24 permutations of 1234
 weights:   3!=6     2!=2    1!=1    0!=1
 digits:     1        1       0       0      (8 = 1*6+1*2)
 meaning: "skip 1 block of 6, then 1 block of 2, then 0, 0"
```

The integers `1..n` in *string* order form a tree: node `v` has children `10v .. 10v+9`. Dictionary order is a pre-order walk of that tree.

```text
            (root)
     /  /  |  ...  \
    1   2  3  ...   9        pre-order (n=13):
  / | \                      1 10 11 12 13 2 3 4 5 6 7 8 9
 10 11 12 13 (14..19 > n)
```

Then counting outcomes. If one experiment can end in `s` distinguishable ways and you run `p` independent experiments, there are `s^p` outcome vectors. To pick one item out of `N`, you need `s^p >= N`. This is the same base-`s` digits idea from the other direction: each experiment reports one digit of the item's label.

Finally, exact geometry on integer points. Two tools do all the work:

```text
 direction from P to Q:  (dx, dy) = (Qx-Px, Qy-Py)
 canonical form: divide by g = gcd(dx, dy), then force
                 dx > 0, or dx == 0 and dy > 0
   (2,4) -> (1,2)    (-3,-6) -> (1,2)    (0,-5) -> (0,1)

 cross(O, A, B) = (A-O) x (B-O)
               = (Ax-Ox)(By-Oy) - (Ay-Oy)(Bx-Ox)
   > 0  B is LEFT of ray O->A   (counter-clockwise turn)
   = 0  O, A, B collinear
   < 0  B is RIGHT of ray O->A  (clockwise turn)
```

Both are integer formulas. Both are exact. The convex hull — the rubber band snapped around a point set — is built entirely from the cross-product sign.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| Transpose an `n x n` grid in place | O(n^2) | swap each pair above the diagonal once |
| Mirror every row | O(n^2) | `n` reversals of length `n` |
| Walk one layer of a grid | O(perimeter) | four straight runs, bounds move inward |
| Read a digit of `n` at weight `p` | O(1) | `(n // p) % 10` |
| Split `n` around weight `p` | O(1) | `high = n // (10p)`, `low = n % p` |
| Convert rank to factorial digits | O(n) divisions | one `divmod` per position |
| Size of a 10-ary subtree clipped to `n` | O(log n) | one range per level |
| Reduce a direction `(dx, dy)` | O(log C) | Euclid's gcd on coordinates up to C |
| Cross product sign | O(1) | two multiplications, one subtraction |
| Convex hull of `n` points | O(n log n) | sort, then each point pushed and popped once |

Transpose, drawn on a 3x3. Only cells above the diagonal are visited; each swap fixes two cells at once.

```text
 before       swap(0,1)    swap(0,2)    swap(1,2)
 1 2 3        1 4 3        1 4 7        1 4 7
 4 5 6   ->   2 5 6   ->   2 5 6   ->   2 5 8
 7 8 9        7 8 9        3 8 9        3 6 9
 diagonal 1,5,9 never moves
```

Splitting a number around one position, here `n = 213` at weight `p = 10`:

```text
   n = 2 | 1 | 3
       high cur low      high = 213 // 100 = 2
                         cur  = (213 // 10) % 10 = 1
                         low  = 213 % 10 = 3
```

Counting a 10-ary subtree clipped to `n = 130`, rooted at `1`:

```text
 level  range [a, b)      clipped to n+1=131   count
   0    [1, 2)            [1, 2)                 1
   1    [10, 20)          [10, 20)              10
   2    [100, 200)        [100, 131)            31
   3    [1000, ...)       a > n, stop
                                       total =  42
```

The cross product, drawn. Stand at `O`, face `A`; the sign tells you which side `B` is on.

```text
        B1 (cross > 0, left)
         \
    O ----------> A ------ B2 (cross = 0, on the line)
         /
        B3 (cross < 0, right)
```

The monotone-chain hull: sort points by `(x, y)`, sweep left to right keeping a stack, and pop the top while the last turn is clockwise.

```text
 stack [P, Q], new point R
   cross(P,Q,R) < 0 : right turn, Q is inside -> pop Q
   cross(P,Q,R) >= 0: left or straight       -> push R
```

## The invariant

The single property this chapter protects is **exactness of representation**: every intermediate quantity is an integer (or an integer pair) that names the thing it stands for *uniquely*.

- A grid move is a bijection on coordinates, so no cell is lost or duplicated.
- A rank is a unique mixed-radix numeral, so "skip `d` blocks of size `w`" lands on exactly one object.
- A direction is a unique reduced pair, so two points are collinear with an anchor iff their keys are equal.
- A turn is a sign, so "inside or on the fence" is decided by `< 0` versus `>= 0` with no tolerance.

Legal versus illegal, for slopes:

```text
 LEGAL: key = reduced (dx, dy) with sign fixed
   (0,0)->(3,1)  key (3,1)
   (0,0)->(6,2)  key (3,1)     same key, same line: exact
 ILLEGAL: key = dy / dx as a float
   1/3  = 0.3333333333333333
   (big coords) 9999/29997 may round differently from 1/3
   (0,0)->(0,5)  dy/dx -> ZeroDivisionError
```

Legal versus illegal, for in-place grid moves:

```text
 LEGAL (transpose, c > r only)   ILLEGAL (all r, c)
 swap(0,1) once                  swap(0,1) then swap(1,0)
 1 4 . / 2 5 .                   1 2 . / 4 5 .  -> unchanged!
```

## How to picture it

Carry four pictures, one per family.

- **The card.** A square matrix is a card you can flip along its diagonal or turn like a page. Rotation is two flips. A spiral is an onion of rectangular rings with four fences closing in.
- **The ruler.** A rank `r` among `N` ordered objects is a point on a ruler of length `N`. The big ticks are the first-level blocks, smaller ticks the second level. You read the digits off tick by tick and never count the space between ticks.
- **The grid of outcomes.** With `p` pigs and `s` states each, the buckets sit in a `p`-dimensional cube of side `s`. Each pig reads one coordinate.
- **The rubber band.** For geometry, everything is a turn. Walk along the boundary keeping the region on your left: a left turn is fine, a straight step is fine, a right turn means the last post was not a corner.

```text
 ruler for 4! = 24 permutations of 1234, rank 8 marked
 |--- 1... ---|--- 2... ---|--- 3... ---|--- 4... ---|
 0            6            12           18           24
              |-21-|-23-|-24-|
              6    8   10   12
                   ^ rank 8 lands in "23.." -> 2314
```

## Signals in a problem statement

- "in place", "O(1) extra space" on a matrix: express the move as reflections, or store flags in the matrix itself.
- "spiral", "clockwise", "layer", "ring": four bounds.
- "the k-th permutation", "the k-th in lexicographical order", `k` up to `10^9`: blocks of known size; skip, do not enumerate.
- "count the digit d in all numbers up to n", `n` up to `10^9`: per-position counting with `high / cur / low`.
- "minimum number of tests / pigs / weighings / queries": count outcomes per test, raise to the power.
- "points", "collinear", "same line": anchor plus reduced direction.
- "fence", "enclose", "perimeter of the smallest", "convex": hull by cross product.
- "rectangles exactly cover", "no overlap and no gap": area plus corner parity.
- Small `n` (`n <= 9`) with factorials in sight: factorial number system.

Counter-signals:

- "shortest path" on a grid: that is BFS, not a coordinate trick.
- "count numbers with property P up to n" where P depends on several digits at once (no two adjacent equal, digit sum = s): that is digit DP, a heavier tool than this chapter's per-position formula.
- Real-valued coordinates with tolerances in the statement: floats may be intended; integer exactness only works because LeetCode gives integer inputs.

## Python toolbox

```python
m[r][c], m[c][r] = m[c][r], m[r][c]   # tuple swap, no temp
for row in m: row.reverse()           # in-place mirror
list(zip(*m))                         # transpose COPY (tuples)
```

```python
from math import gcd, factorial
gcd(-4, 6)           # 2 (always >= 0); gcd(0, 5) == 5
q, r = divmod(8, 6)  # (1, 2): block index, offset in block
pool.pop(idx)        # remove the idx-th unused item, O(len)
```

```python
from collections import Counter
cnt = Counter(); cnt[(1, 2)] += 1     # tuples are hashable keys
s = set(); s ^= {(3, 1)}              # toggle membership
pts = sorted(map(tuple, pts))         # sort by x, then y
```

Python integers never overflow, so `states ** pigs` and `high * p` are safe here; in Java or C++ the same lines need `long`.

## Mistakes people make

1. Transposing with `for c in range(n)` instead of `range(r + 1, n)`: every pair is swapped twice and nothing moves. Start the inner loop above the diagonal.
2. Reversing columns instead of rows after a transpose: you get the counter-clockwise rotation. Clockwise is transpose then mirror rows.
3. Forgetting to re-check `top <= bottom` and `left <= right` mid-layer in a spiral: a single leftover row is emitted twice. Re-check before the return trip.
4. Clearing the flag row or flag column before the interior has been processed: the flags are gone. Clear them last.
5. Using 1-indexed `k` directly as a rank: off by one block. Convert to `r = k - 1` first.
6. Clipping a subtree range with `min(n, b)` instead of `min(n + 1, b)`: drops `n` itself. Ranges are half-open.
7. Counting a pig as a yes/no bit when there are several rounds: a pig has `T + 1` states. Use `minutesToTest // minutesToDie + 1`.
8. Using `math.log` and `ceil` to find the smallest exponent: float error at exact powers. Multiply in a loop.
9. Float slopes (`dy / dx`): precision loss and division by zero on vertical lines. Use gcd-reduced pairs with a fixed sign.
10. Popping collinear points (`cross <= 0`) when the problem wants every tree on the fence: use `cross < 0`.

## The journey ahead

1. **Rotate Image** — a geometric move is a formula on coordinates, and a rotation is two in-place reflections.
2. **Spiral Matrix** — the same board, walked layer by layer; four bounds replace a visited grid.
3. **Set Matrix Zeroes** — the board's own border becomes storage; order of updates matters when you write into your input.
4. **Permutation Sequence** — leave the board for number systems: blocks of `(n-1)!`, the factorial number system.
5. **K-th Smallest in Lexicographical Order** — the same block skipping, but block sizes must be computed on a ragged 10-ary tree.
6. **Number of Digit One** — count across positions instead of across numbers: the `high / cur / low` split.
7. **Poor Pigs** — counting turned into a lower bound, and a base-`s` labelling that meets it.
8. **Max Points on a Line** — exact geometry begins: a slope as a canonical integer pair, grouped in a hash map.
9. **Perfect Rectangle** — integer invariants (area and corner parity) that certify a whole tiling in one pass.
10. **Erect the Fence** — the cross-product sign drives a stack sweep that builds the convex hull; the chapter's capstone.
