# Perfect Rectangle

*LeetCode 391 · Hard · Pattern: Corner parity + area invariant · Reading time ~9 min*

## What the problem is really asking

You get `n` axis-aligned rectangles, each as `[x1, y1, x2, y2]` (bottom-left and top-right corners), with `n` up to `2 * 10^4`. Return `True` iff together they tile one big rectangle *exactly*: no gaps, no overlaps.

The answer is a yes/no certificate. What makes it hard is that "no overlap" sounds like a pairwise question — does tile `i` intersect tile `j`? — and pairwise is `O(n^2)`, `4 * 10^8` checks. The puzzle is to certify a global property (exact cover) with local, countable facts, in one pass.

```text
 five tiles that form the 3x3 square [1,1,4,4]: True
 y
 4 +---+---+---+
   | R4| R5|   |
 3 +---+---+ R3|
   |       |   |
 2 |  R1   +---+
   |       | R2|
 1 +-------+---+
   1   2   3   4  x
 R1=[1,1,3,3] R2=[3,1,4,2] R3=[3,2,4,4]
 R4=[1,3,2,4] R5=[2,3,3,4]
```

## Do it by hand first

On graph paper, two things convince you that a tiling is perfect. First, the pieces' areas add up to the area of the outline: `4 + 1 + 2 + 1 + 1 = 9 = 3 * 3`. Second, nothing is doubled, which you check by eye.

Can the eye's check be turned into counting? Look at the *corners* of the tiles. Put a dot at every tile corner, and write next to it how many tiles have a *corner* there. Careful: `(2, 3)` is a corner of `R4` and `R5`, but it lies in the middle of `R1`'s top edge, so it counts 2, not 3. Likewise `(3, 3)` is a corner of `R1` and `R5`, and mid-edge for `R3`.

```text
 how many tiles have a CORNER at each point
 4 1---2---2---1
 3 2---2---2   .
 2 .       2---2
 1 1-------2---1
   1   2   3   4
 every point is 2 except the four outline corners: 1
```

Your hand noticed: inside a perfect tiling, corners come in pairs (or fours); only the outline's four corners are lonely. That is the seed.

## The first honest attempt

Check every pair of rectangles for a positive-area overlap (`ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2`), then check that the total area equals the bounding box area. No overlaps plus equal area means every point of the box is covered exactly once.

Cost: `O(n^2)` time, `O(1)` space. At `n = 2 * 10^4` that is `2 * 10^8` overlap tests, too slow.

Where is the waste? The pairwise loop exists only to rule out overlaps, and almost all pairs are nowhere near each other. The area check is already `O(n)`, but it cannot alone rule out an overlap that is compensated by an equal-sized gap.

```text
 box [0,0,3,1]; tiles A=[0,0,1,1] twice, C=[2,0,3,1]
   0   1   2   3
   +---+---+---+
   |A,A|   | C |    covered twice | empty | once
   +---+---+---+
 area 1 + 1 + 1 = 3 = box area, yet not a tiling
```

## The turning point

**Claim: in a perfect tiling, every point that is a corner of some tile is a corner of an even number of tiles, except the four corners of the bounding box, which are corners of exactly one tile each.**

Justify it with angles. Stand at a point `p` and look at the 360 degrees around it. Every tile that has `p` as a corner fills a 90-degree wedge. Every tile that has `p` in the middle of an edge fills 180 degrees. A tile with `p` in its interior fills all 360. In a perfect tiling, the wedges around `p` fill the space covered by the big rectangle *exactly once*.

```text
 around a point p:  covered angle = 90 * corners
                                  + 180 * edge-midpoints
 p strictly inside the box: 360 -> corners = 0, 2 or 4
 p on a side of the box:    180 -> corners = 0 or 2
 p a corner of the box:      90 -> corners = 1

   cross (4 corners)   T-junction (2)    outline corner (1)
        |                   |                 |
     A  |  B             A  |                 |  A
   -----p-----         -----p   C           --p----
     C  |  D             B  |
```

So every corner count is even except at the four outline corners. Now the algorithm writes itself: keep a set, and for each tile *toggle* its four corners (add if absent, remove if present). A point survives iff it was toggled an odd number of times. In a perfect tiling, exactly the four outline corners survive.

The corner test alone has a loophole: duplicates cancel. Two copies of `[0,0,1,1]` toggle the same four points twice and vanish, so `[[0,0,1,1],[0,0,1,1],[0,0,2,2]]` leaves exactly the outline `(0,0),(0,2),(2,0),(2,2)` — but its area is `1 + 1 + 4 = 6`, not `4`. The area test alone has the loophole drawn above. **Together** they are exact: corners equal the outline *and* area equals the box. Each closes the other's loophole.

Both tests are `O(1)` per rectangle: four set toggles, one area addition, four min/max updates for the bounding box. All integers, so no tolerance anywhere.

## Watch it work

Example: `R1..R5` from the first drawing, in input order. State: the toggled corner set and the running area.

Frame 1 — `R1 = [1,1,3,3]`: add its four corners. Area `4`.

```text
 4 .   .   .   .
 3 *   .   *   .     set: (1,1) (1,3) (3,1) (3,3)
 2 .   .   .   .     area = 4
 1 *   .   *   .
   1   2   3   4
```

Frame 2 — `R2 = [3,1,4,2]`: corners `(3,1)` toggles off (now shared), `(3,2) (4,1) (4,2)` toggle on. Area `5`.

```text
 4 .   .   .   .
 3 *   .   *   .     set: (1,1) (1,3) (3,2) (3,3)
 2 .   .   *   *          (4,1) (4,2)
 1 *   .   .   *     area = 5
   1   2   3   4
```

Frame 3 — `R3 = [3,2,4,4]`: `(3,2)` and `(4,2)` toggle off; `(3,4) (4,4)` toggle on. Area `7`.

```text
 4 .   .   *   *
 3 *   .   *   .     set: (1,1) (1,3) (3,3) (3,4)
 2 .   .   .   .          (4,1) (4,4)
 1 *   .   .   *     area = 7
   1   2   3   4
```

Frame 4 — `R4 = [1,3,2,4]`: `(1,3)` toggles off; `(1,4) (2,3) (2,4)` on. Area `8`.

```text
 4 *   *   *   *
 3 .   *   *   .     set: (1,1) (1,4) (2,3) (2,4)
 2 .   .   .   .          (3,3) (3,4) (4,1) (4,4)
 1 *   .   .   *     area = 8
   1   2   3   4
```

Frame 5 — `R5 = [2,3,3,4]`: all four of its corners `(2,3) (2,4) (3,3) (3,4)` toggle off. Area `9`.

```text
 4 *   .   .   *
 3 .   .   .   .     set: (1,1) (1,4) (4,1) (4,4)
 2 .   .   .   .     area = 9
 1 *   .   .   *
   1   2   3   4
```

Frame 6 — check. Bounding box `[1,1,4,4]`: its corners equal the set, and its area `3 * 3 = 9` equals the sum. Return `True`.

```text
 outline corners {(1,1),(1,4),(4,1),(4,4)} == set   yes
 box area 9 == sum of areas 9                       yes
 -> True
```

For contrast, the gap example `[[1,1,2,3],[1,3,2,4],[3,1,4,2],[3,2,4,4]]` ends with eight surviving corners, including `(2,1)` and `(3,4)`, and area `6` against a box of `9`: `False` on both counts.

What stayed invariant: after each rectangle, the set holds exactly the points that are corners of an odd number of tiles seen so far, and `area` is the sum of their areas. Neither depends on the order of the tiles, which is why any input order works.

## Why it is correct

*If the tiling is perfect, both tests pass.* The area of disjoint pieces that cover the box sums to the box's area. The angle argument shows every corner count is even except the four outline corners, which have count 1; so the toggle set is exactly the outline.

*If both tests pass, the tiling is perfect.* Let `f(q)` be how many tiles cover a point `q`. Look at any point `p` and the four small quadrants around it (NE, NW, SW, SE). A tile with a corner at `p` covers one quadrant; a tile with `p` mid-edge covers two; a tile with `p` inside covers four; others none. So the *parity* of "tiles with a corner at `p`" equals the parity of the sum of `f` over the four quadrants. The corner test says that sum is odd only at the four outline corners.

Now compare `f mod 2` with the box's indicator (1 inside, 0 outside). The box's indicator has exactly the same "odd only at the four corners" property. Their difference (XOR) therefore has even quadrant sums *everywhere*. Coordinates are integers, so these functions are constant on unit cells, and any nonzero pattern of unit cells has a lowest, then leftmost, cell, and at that cell's bottom-left corner the quadrant sum is 1, odd. So the XOR is zero: `f` is odd inside the box and even outside it. Odd means `f >= 1` everywhere in the box. Since the tiles' total area equals the box's area, there is no room for `f >= 2` anywhere. So `f = 1` on the box: an exact cover.

## Cost

- **Time:** `O(n)` — four hash-set toggles and constant arithmetic per rectangle.
- **Space:** `O(n)` — the corner set holds at most `4n` points.

The pairwise brute force is `O(n^2)` time, `O(1)` space; the set trades memory for a factor of `n`.

## Variations you will meet

- **Rectangle Area II (LeetCode 850).** Union area of overlapping rectangles. Overlaps are now allowed and must be measured, so you need a sweep line over x with coordinate compression of y (or a segment tree). Parity tricks no longer apply.
- **Rectangle Overlap (LeetCode 836) / Rectangle Area (LeetCode 223).** Two rectangles only: overlap iff the x-intervals and y-intervals both overlap strictly; intersection area is `max(0, min right - max left) * max(0, min top - max bottom)`.
- **Return the overlapping pair, not just "no".** Corner parity cannot name the culprits. Use a sweep line with an interval tree, `O(n log n)`.
- **Exact cover by unit squares on a grid with duplicates allowed?** If every tile is a unit square, a hash set of cells (insert, fail on duplicate) plus a count check suffices; the corner trick is the generalisation to arbitrary sizes.

## What to carry forward

To certify a global "exactly once" property in one pass, find integer quantities that cancel in pairs in the good case (corner parity) and pair them with a conservation law (area) that closes the remaining loophole.

The next problem, Erect the Fence, closes the chapter: the cross product you used for collinearity becomes a turn detector, and a stack sweep uses it to wrap a rope around a set of points.
