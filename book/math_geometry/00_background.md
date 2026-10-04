# Math and Geometry

*10 problems · Reading time ~22 min*

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
   94911150/94911151 == 94911151/94911152 -> True,
   yet the cross-multiplied difference is -1: different
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

## Advanced patterns

The basics above give you the tools: coordinate formulas, mixed-radix digits, outcome counts, gcd keys and the cross product. The chapter's seven Hard problems need more than the tools. Each one leans on a *way of using* a tool that is easy to miss the first time. These are the seven ideas worth carrying out of the chapter.

### Count, then descend (unranking)

**When it shows up**: "return the k-th object" in some order, where the objects are far too many to list (`n!` permutations, `10^9` numbers, `C(m+n, n)` paths), but you can *count* how many objects start with any given prefix.

**The intuition**: An ordered family of objects built one choice at a time is a tree, and the order is a left-to-right walk of that tree. You do not need to walk it. At each choice point, look at the options in order and ask how many complete objects hang under each one. If `k` is larger than that count, the target is not under this option: subtract the count and move to the next option. Otherwise the target is inside: commit to the option and repeat one level down with what remains of `k`. The factorial number system is this idea in the special case where every option owns the same count, `(m-1)!`, so the "subtract until it fits" loop collapses into one `divmod`. The reverse direction, *ranking*, is the same walk read backwards: for each chosen item, add (number of smaller unused options) times (block size).

```text
 unrank k=9 (r=8) among permutations of 1234
 level  options : block size          r   decision
   1    1:6  2:6  3:6  4:6            8   skip 1, take 2, r=2
   2    1:2  3:2  4:2                 2   skip 1, take 3, r=0
   3    1:1  4:1                      0   take 1
   4    4:1                           0   take 4   -> 2314
 rank 2314 back:  2 -> 1 smaller unused * 3! = 6
                  3 -> 1 smaller unused * 2! = 2
                  1 -> 0,  4 -> 0           rank = 8
```

**Where you'll use it**: Permutation Sequence (equal blocks, one division per level) and K-th Smallest in Lexicographical Order (unequal blocks, so the loop really does subtract). Beyond the chapter, Kth Smallest Instructions (LeetCode 1643) uses the same walk with binomial coefficients as the block sizes.

### Sizing a clipped implicit subtree

**When it shows up**: the tree from the previous pattern is not stored anywhere, its shape follows a rule (node `v` has children `10v..10v+9`), and an upper limit `n` cuts off part of it, so block sizes differ from option to option.

**The intuition**: You cannot count a subtree by visiting it; it may hold hundreds of millions of nodes. But in the denary tree, the descendants of prefix `v` at depth `d` are exactly the integers in one contiguous range, `[v * 10^d, (v+1) * 10^d)`. A contiguous range intersected with `1..n` is still a contiguous range, so each level's count is one subtraction, and there are at most ten levels. The whole subtree is a stack of intervals, each clipped at `n + 1`. The clipping is what makes the blocks uneven, and it is also why a closed-form like `(m-1)!` does not exist here: the last level of each subtree can be full, partial or empty depending on where `n` falls.

```text
 subtree of prefix 1, n = 1234: one interval per level
 level 0  [1, 2)                              ->   1
 level 1  [10, 20)                            ->  10
 level 2  [100, 200)                          -> 100
 level 3  [1000, 2000) clipped [1000, 1235)   -> 235
 level 4  [10000, ..)  starts past n          -> stop
                                       size   =  346
 check: prefixes 2..9 have 1 + 10 + 100 = 111 each,
        346 + 8 * 111 = 1234 = n   (every number counted)
```

**Where you'll use it**: K-th Smallest in Lexicographical Order, where this count feeds the skip-or-descend decision. Lexicographical Numbers (LeetCode 386) walks the same tree without the counting.

### Swap the order of summation (count columns, not rows)

**When it shows up**: "count the total number of X across all numbers from 1 to n" (or across all pairs), where `n` is up to `10^9` and looping over the numbers is out.

**The intuition**: Picture the numbers as rows of a table and the digit positions as columns. The answer is the number of marked cells. Counting row by row means visiting `n` rows. Counting column by column means visiting about ten columns, and a single column is not random: the digit at weight `p` cycles `0, 1, ..., 9`, each value held for `p` consecutive numbers. That rhythm gives each column's count as a formula in `high`, `cur` and `low`. Nothing about the answer changed; you only regrouped the same sum. The move generalises to any per-position or per-bit total: decide what one column contributes, in closed form, and add the columns.

```text
 count the digit 1 in 1..13
 number  tens units      column by column
    1     0    1         units: 1, 11           -> 2
    2     0    2                (high=1, cur=3: 1*1 + 1)
   ..    ..   ..         tens : 10, 11, 12, 13  -> 4
   10     1    0                (high=0, cur=1: low+1=4)
   11     1    1
   12     1    2         total = 2 + 4 = 6
   13     1    3         13 rows scanned vs 2 formulas
```

**Where you'll use it**: Number of Digit One. Total Hamming Distance (LeetCode 477) is the same regrouping on bits: per bit, the contribution is (count of ones) times (count of zeros).

### Information counting: a lower bound plus a construction that meets it

**When it shows up**: "the minimum number of tests, pigs, weighings or queries to identify one item out of N", where the clever strategy seems hard to search for directly.

**The intuition**: Do not search strategies. Count what any strategy could possibly observe. If one test ends in `s` distinguishable ways and you run `p` tests, there are at most `s^p` different observations. If `N > s^p`, two items must produce the same observation (pigeonhole), so no strategy, however adaptive, can separate them. That gives a lower bound with zero cleverness. The second half is to *meet* the bound: label each item with a distinct outcome vector (its base-`s` digits) and design the tests so that the test result spells out the label. When the construction achieves `s^p >= N`, the bound is tight and the answer is just the smallest such `p`. The pitfall is counting `s` wrongly; in Poor Pigs, *when* a pig dies is information, so `s = T + 1`, not `2`.

```text
 T = 2 rounds: a pig ends as died-r1 / died-r2 / lived
 2 pigs -> 3 x 3 = 9 possible observations
                 pig 1:  r1    r2    lived
   pig 0 r1             [  ]  [  ]  [  ]
   pig 0 r2             [  ]  [  ]  [  ]
   pig 0 lived          [  ]  [  ]  [  ]
 10 buckets into 9 cells: two buckets share a cell,
 so no scheme with 2 pigs can work; 3 pigs give 27
```

**Where you'll use it**: Poor Pigs. The same argument is behind the `log2(n!)` lower bound for comparison sorting and behind why binary search is optimal for comparison-based lookup.

### Canonical exact keys for geometric relations

**When it shows up**: grouping or comparing geometric things (lines, directions, slopes, ratios) computed from integer coordinates, especially with a hash map.

**The intuition**: A hash map groups by *equality of bits*, so the key must be a representation in which equal things are byte-for-byte equal and different things never are. A float ratio fails both ways: vertical lines have no value, and two different large ratios can round to the same double. The fix is to keep the relation in integers and pick one canonical representative per equivalence class: divide by the gcd to get the primitive vector, then fix the sign by a rule. When you only need to compare two ratios rather than hash them, skip the gcd and cross-multiply: `a/b == c/d` iff `a*d == b*c`, exactly. Both moves keep every decision in integer arithmetic.

```text
 A=(0,0)  B=(94911151,94911150)  C=(94911152,94911151)
 float slopes: 94911150/94911151 == 94911151/94911152
               -> True   (wrong: they are different)
 cross-multiply: 94911150*94911152 - 94911151*94911151
               = -1      (not 0: not collinear, exact)
 gcd keys: (94911151,94911150) vs (94911152,94911151)
           already primitive, different -> different lines
```

**Where you'll use it**: Max Points on a Line, with an anchor plus a `Counter` of gcd keys. Minimum Lines to Represent a Line Chart (LeetCode 2280) is famous for failing float solutions; cross-multiplication fixes it.

### Local parity certifies a global shape

**When it shows up**: "do these pieces form exactly X" (a perfect tiling, a closed loop, a valid cover), where checking the whole shape directly would mean drawing it cell by cell.

**The intuition**: Find quantities that are cheap to accumulate piece by piece and that a correct answer pins down. Area is additive: a perfect tiling's areas sum to the box's area. Corner multiplicity is local: around any interior point the tiles' angles must sum to 360 degrees, which forces an even number of tile corners there, while each outline corner sees exactly one. Each test alone has a loophole, because each one only sees part of the picture: identical tiles cancel in the corner parity, and a gap can be paid for by an overlap of equal area. Together they leave no room. Toggling a set (add if absent, remove if present) computes parity for free, and nothing depends on the order the pieces arrive.

```text
 area fooled, corners not:
 y=2  +-----+. . . .     A = [0,0,2,1]  area 2
      |  C  :  gap  :    B = [1,0,2,1]  area 1 (overlaps A)
 y=1  +-----+-------+    C = [0,1,1,2]  area 1
      |  A  |  A+B  |    sum 4 == box [0,0,2,2] area 4
 y=0  +-----+-------+
     x=0   x=1     x=2
 odd corners left: (0,0) (1,0) (0,2) (1,2)
 box corners:      (0,0) (2,0) (0,2) (2,2)   -> not perfect
```

**Where you'll use it**: Perfect Rectangle. The habit of "find an invariant that a correct configuration must satisfy, then show it is also sufficient" shows up again in greedy proofs and in parity arguments for grid puzzles.

### Orientation as the only primitive; sort, then a turn-checking stack

**When it shows up**: anything about the boundary of a point set: enclosing fences, convexity checks, "is this polygon convex", "are all these points on one line".

**The intuition**: Every geometric decision in a hull reduces to one question about three points: left turn, right turn or straight, answered by the sign of an integer cross product. Sorting by `(x, y)` turns the 2-D problem into two 1-D sweeps, because each half of the boundary is monotone in `x`. Along a sweep, the stack is always a chain that only turns left; a new point that makes the top turn right proves the top is inside, so it is popped and never seen again. Each point is pushed once and popped at most once per chain, which is why the sweep is linear after the sort. The remaining subtlety is the straight case: `cross == 0` points lie on the boundary, and whether you keep them is a policy choice, not a geometric fact. Keeping them means the same point can land in both chains, so merge with a set rather than by slicing off endpoints.

```text
 all trees collinear: (0,0) (1,1) (2,2) (3,3)
 every triple has cross = 0, nothing is popped (pop on < 0)
 lower chain: (0,0) (1,1) (2,2) (3,3)
 upper chain: (3,3) (2,2) (1,1) (0,0)
 lower[:-1] + upper[:-1] -> (1,1), (2,2) listed twice
 set(lower) | set(upper)  -> 4 trees, each once
```

**Where you'll use it**: Erect the Fence. Check If It Is a Straight Line (LeetCode 1232) is the single-sign version: every cross product must be zero.

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

The ten problems climb from a board you can see, to numbers you cannot list, to shapes you must not approximate. Each one keeps something from the problem before it and changes one thing.

### Stage 1: the board as a coordinate system

**Rotate Image.** Rotating a square in place looks like it needs a second matrix, because writing a cell destroys a value you still need. The puzzle dissolves once a rotation is a formula, `(r, c) -> (c, n-1-r)`, and you notice it factors into two reflections, each of which is a set of independent swaps. The new idea is that grid moves are algebra on coordinates, not cell shuffling.

**Spiral Matrix.** The board stays, but the question changes from moving cells to visiting them in a strange order. The naive approach keeps a visited grid and turns on collisions; the better one sees that the unvisited part is always a rectangle, described by four integers that close in after each straight run. The new idea is that a layer is a rectangle's border, and its bounds replace memory. The trap to watch is a single leftover row or column visited twice.

**Set Matrix Zeroes.** Now you must write into the board while still reading it, and the follow-up forbids extra memory. The question is where the "this row has a zero" flags can live; the answer is the board's own first row and column, plus one extra bit for the cell they share. The new idea, building on the previous two, is that the order of updates matters when the input is also your scratch space: process the interior first, the flags last.

### Stage 2: numbers as addresses

**Permutation Sequence.** Listing `n!` permutations to find the k-th one is honest and hopeless. The question a curious person asks is "how many permutations start with 1?", and the answer, `(n-1)!` for every leading digit, turns the search into division. The new idea is the factorial number system: a rank is a mixed-radix numeral whose digits are indices into the shrinking pool of unused digits.

**K-th Smallest in Lexicographical Order.** The same "skip whole blocks" walk, but the blocks now have different sizes, because `n` cuts the denary tree off unevenly. What makes it interesting is that you need the size of a subtree that you cannot afford to visit. The new idea is counting a clipped implicit subtree level by level, each level one contiguous range, and choosing between skipping a sibling and stepping down.

**Number of Digit One.** Here there is no k-th object to find, only a total to count, and the obvious loop over `1..n` fails at `n = 10^9`. The twist is to stop counting numbers and start counting digit positions, where the digit at weight `p` cycles with period `10p`. The new idea is swapping the order of summation, with the `high / cur / low` split giving one column's count in `O(1)`, and the `cur == 1` case needing the partial run `low + 1`.

### Stage 3: what an experiment can tell you

**Poor Pigs.** It reads like a puzzle about clever pig schedules, and searching for schedules goes nowhere. The question to ask instead is how many different things you could possibly observe at the end, which caps what any schedule can achieve. The new idea is an information-theoretic lower bound, `(T+1)^p >= buckets`, met exactly by labelling buckets in base `T + 1`, so the digits from Stage 2 reappear as the experiment's design.

### Stage 4: exact geometry

**Max Points on a Line.** The brute force over all lines is fine in principle; what breaks naive solutions is representing a slope. Floats divide by zero on vertical lines and can merge different slopes. The new idea is a canonical integer key, the gcd-reduced direction with a fixed sign, counted from each anchor point, so that "same line" becomes "same dictionary key".

**Perfect Rectangle.** Checking a tiling cell by cell is too slow, and checking only area is fooled by a gap that an overlap pays for. The puzzle is to find something cheap that a perfect tiling must satisfy and an imperfect one cannot fake. The new idea is a pair of integer invariants, total area and odd-count corners via set toggles, each closing the other's loophole, continuing the "keep everything exact" habit from the previous problem.

**Erect the Fence.** The capstone combines exact integer tests with a stack sweep. The trees are sorted, then two passes keep a chain that never turns right, using the cross-product sign from the basics and the monotonic-stack habit from earlier chapters. The new idea is the collinear policy: pop only on a strict right turn so every tree on the rope stays, and merge the two chains with a set because straight stretches can appear in both.
