# Rectangle Area II
*LeetCode 850 · Hard · Pattern: Sweep line over sorted events · Reading time ~11 min*

## What the problem is really asking

You get n axis-aligned rectangles `[x1, y1, x2, y2]` (bottom-left and top-right corners). Paint them all on the plane and report the total painted area. Where rectangles overlap, the paint counts once. Coordinates go up to 10^9, so return the area modulo 10^9 + 7.

The answer is one number, the area of the union. Adding up the individual areas overcounts every overlap. Inclusion-exclusion fixes the overcount in principle, but it has 2^n terms. The real difficulty is that the union of rectangles can be a very irregular shape, and you need a way to measure it without ever describing that shape.

Running example: `[[0,0,2,2], [1,0,2,3], [1,0,3,1]]`, answer 6.

```text
 the thing (cells labelled by who covers them)

 y
 3 +---+---+---+
   |   | B |   |         A = [0,0,2,2]  area 4
 2 +---+---+---+         B = [1,0,2,3]  area 3
   | A |A B|   |         C = [1,0,3,1]  area 2
 1 +---+---+---+         sum = 9, union = 6
   | A |ABC| C |
 0 +---+---+---+
   0   1   2   3  x

 how it is stored

 rectangles = [[0,0,2,2], [1,0,2,3], [1,0,3,1]]
                x1 y1 x2 y2
```

## Do it by hand first

How would you measure that shape with a ruler? Cut it into vertical strips wherever any rectangle edge appears: at x = 0, 1, 2, 3. Inside one strip, the shape is the same at every x. The covered part of a vertical line through the strip does not change, because no rectangle starts or stops inside the strip. So each strip's area is (strip width) x (covered length of one vertical line through it).

```text
 strip [0,1): line cuts A only        covered y: [0,2] -> 2
 strip [1,2): line cuts A, B, C       covered y: [0,3] -> 3
 strip [2,3): line cuts C only        covered y: [0,1] -> 1

 y   [0,1) [1,2) [2,3)
 3  .     |#####|      .
 2  |#####|#####|      .
 1  |#####|#####|#####|
 0  +-----+-----+-----+
    0     1     2     3
     1*2  + 1*3 + 1*1 = 6
```

What did your hand keep track of? Two things. As you moved right, it kept **which rectangles the vertical line currently cuts**, the active set, which changes only at x1 (enter) and x2 (leave). For each strip it kept **the length of the union of the active y-intervals**, and measuring a union of intervals on a line is Merge Intervals, the first problem of the chapter.

## The first honest attempt

"Coordinates are huge, so I cannot paint unit squares. But I can compress. The distinct x's split the plane into columns, and the distinct y's split it into rows. Every rectangle covers a whole block of the resulting cells. Make a boolean grid, paint each rectangle's block, then sum `width x height` of the painted cells using the real coordinate differences."

```text
 xs = [0,1,2,3]  ys = [0,1,2,3]  -> 3 x 3 cells

 paint A: cells (0,0) (0,1) (1,0) (1,1)     4 writes
 paint B: cells (1,0) (1,1) (1,2)           3 writes
 paint C: cells (1,0) (2,0)                 2 writes
              ^^^^^ cell (1,0) painted three times
 painted cells: 6, each 1x1 -> area 6
```

This is correct, and with up to 2n distinct values per axis it is O(n^3) time and O(n^2) memory. Where is the repeated work? Within one column, a rectangle covers a **contiguous run** of rows. Painting that run cell by cell spends O(n) writes on what is really one interval. Then overlapping rectangles repaint the same cells again. Cell (1,0) above was written three times.

```text
 column [1,2):  rows painted by A: 0,1      (an interval)
                rows painted by B: 0,1,2    (an interval)
                rows painted by C: 0        (an interval)
 one merge of three intervals would give [0,3] directly
```

## The turning point

**Claim: area is the integral of covered length. Between consecutive x-events the covered length is constant, so area = the sum over gaps between sorted x-events of (gap width) x (union length of the active y-intervals), and each union length is one Merge Intervals pass.**

Unpack this in two layers.

**Layer 1: the x-sweep (events).** Each rectangle produces two events: `(x1, enter, y1, y2)` and `(x2, leave, y1, y2)`. Sort all 2n events by x. Walk them with a vertical line, keeping `prev_x` (where the line last stopped) and `active` (the y-intervals the line cuts). At each event at position x:

1. **First** add the slab `(x - prev_x) * covered(active)`. This slab lies to the left of x, so it belongs to the active set *before* this event changes it.
2. Then set `prev_x = x` and apply the event: add or remove `(y1, y2)` from `active`.

This is My Calendar III's sweep moved to two dimensions. Events at boundaries change the state, and the quantity being integrated is constant between them. The difference is that the state is no longer a single counter. It is a multiset of y-intervals, because we need to know how much of the line is covered, not just how many rectangles cut it.

```text
 events sorted by x:

 x=0  enter (0,2)  A
 x=1  enter (0,1)  C        same x: zero-width slab
 x=1  enter (0,3)  B        between them, harmless
 x=2  leave (0,2)  A
 x=2  leave (0,3)  B
 x=3  leave (0,1)  C
```

Multiple events at the same x are fine. The second one adds a slab of width 0.

**Layer 2: the y-measure (merge).** `covered(active)` is the total length of the union of some y-intervals. Sort them by start and sweep with a running `reach`. For each `(s, e)`, clip its start to `max(s, reach)` so already-counted length is not counted twice. If anything remains (`e > s`), add `e - s` and set `reach = e`. This is Merge Intervals, but it sums lengths instead of building the list. Endpoint convention does not matter here, because a shared point has length zero.

```text
 covered([(0,2),(0,1),(0,3)]):
 sorted:  (0,1) (0,2) (0,3)
 (0,1): s=max(0,-inf)=0  add 1  reach 1
 (0,2): s=max(0,1)=1     add 1  reach 2
 (0,3): s=max(0,2)=2     add 1  reach 3   total 3
```

Why must the slab be added **before** applying the event? Picture the line arriving at x = 2. The strip `[1, 2)` is covered by A, B and C. If you first remove A and then measure, you multiply the width of `[1,2)` by the coverage of `[2,3)`. That is the classic off-by-one-slab bug.

**What about modulo?** In Python, integers do not overflow, so take `% (10^9+7)` once at the end. In Java or C++ the per-slab product can reach 10^18, so use 64-bit and reduce as you go.

Cost of this version: 2n events, each calling `covered` on up to n intervals with a sort, gives O(n^2 log n). For n <= 200 that is tiny. The remaining slack is re-sorting the active set at every event. A segment tree over the compressed y-coordinates, storing for each node a cover count and covered length, updates in O(log n) per event and reads the root's covered length in O(1), for O(n log n) total. That is the expected follow-up, but the sweep-plus-merge is the version to build first, and it passes.

## Watch it work

Rectangles A `[0,0,2,2]`, B `[1,0,2,3]`, C `[1,0,3,1]`. State before each event: `prev_x`, `active`, covered length, and `area`. In each frame the slab is computed with the active set before the event is applied.

**Frame 1.** x = 0, enter A. Slab width 0 - 0 = 0, so add 0. Then `active = [(0,2)]`.

```text
 y
   3 |                      prev_x=0
   2 |                      active=[(0,2)]
   1 |  <- line at x=0      area=0
   0 +---+---+---+
     0   1   2   3
```

The line has only just entered A, so nothing has been swept yet.

**Frame 2.** x = 1, enter C. Slab: width 1, covered(`[(0,2)]`) = 2, so add 2 and `area = 2`. Then `active = [(0,2),(0,1)]`.

```text
 y
   3 |                      prev_x=1
   2 |####                  active=[(0,2),(0,1)]
   1 |####                  area=2
   0 +---+---+---+
     0   1   2   3          strip [0,1) x [0,2]
```

The first slab is banked: A alone, 1 wide and 2 tall.

**Frame 3.** x = 1, enter B. Slab width 0, so add 0. Then `active = [(0,2),(0,1),(0,3)]`.

```text
                            prev_x=1
 tie at x=1: width 0        active=[(0,2),(0,1),(0,3)]
 nothing added              area=2
```

Ties between events cost nothing and need no special ordering.

**Frame 4.** x = 2, leave A. Slab: width 1, covered = 3 (the merge shown in the turning point), so add 3 and `area = 5`. Then remove `(0,2)`, leaving `active = [(0,1),(0,3)]`.

```text
 y
   3 |    ####              prev_x=2
   2 |########              active=[(0,1),(0,3)]
   1 |########              area=5
   0 +---+---+---+
     0   1   2   3          strip [1,2) x [0,3]
```

The overlap of A, B and C in this strip was counted once, because the merge clipped it.

**Frame 5.** x = 2, leave B. Slab width 0, so add 0. Then `active = [(0,1)]`.

```text
                            prev_x=2
 tie at x=2: width 0        active=[(0,1)]
 nothing added              area=5
```

Only C remains under the line.

**Frame 6.** x = 3, leave C. Slab: width 1, covered(`[(0,1)]`) = 1, so add 1 and `area = 6`. Then `active = []`.

```text
 y
   3 |    ####              prev_x=3
   2 |########              active=[]
   1 |############          area=6
   0 +---+---+---+
     0   1   2   3          strip [2,3) x [0,1]
```

The final area is 6, matching the solution. Note the sum of slabs: 2 + 3 + 1.

Invariant across frames: after processing the events at positions up to x, `area` equalled the union's area to the left of x exactly, and `active` held the y-intervals of precisely the rectangles with `x1 <= x < x2`.

## Why it is correct

Let `x_0 < x_1 < ... < x_k` be the distinct event coordinates. Inside any open strip `(x_i, x_{i+1})`, no rectangle starts or ends. So a vertical line at any x in the strip cuts the same set of rectangles, namely those with `x1 <= x_i` and `x2 >= x_{i+1}`, and therefore the same union of y-intervals with the same length `L_i`. The union restricted to that strip is a set of full-width columns, `L_i` tall in total, and its area is `(x_{i+1} - x_i) * L_i`. Strips do not overlap, and together they cover every x where anything is painted, so the union area is the sum of these slabs.

The loop computes exactly that sum. When it reaches the first event at `x_{i+1}`, `active` still reflects every event at or before `x_i` and nothing after, which is the strip's rectangle set. The slab added is `(x_{i+1} - x_i) * covered(active)`. Extra events at the same coordinate add width-zero slabs. `covered` is correct by the Merge Intervals argument. In sorted order, `reach` is the right edge of everything counted so far, and clipping each start to `reach` counts each y-point of the union exactly once.

## Cost

- **Time O(n^2 log n).** 2n events. At each one, `covered` sorts and scans up to n active intervals, and `active.remove` is O(n).
- **Space O(n).** The event list and the active list.

The compressed-grid paint is O(n^3) time and O(n^2) space. With a segment tree over compressed y's (cover count + covered length per node), it drops to O(n log n) time and O(n) space.

## Variations you will meet

- **Two rectangles only** (223, Rectangle Area): inclusion-exclusion is fine. Compute `area(A) + area(B) - area(A ∩ B)`, with the intersection's width `max(0, min(right) - max(left))`.
- **Perfect Rectangle** (391): do the rectangles tile one big rectangle exactly? Area sums plus corner-parity counting, or the same x-sweep checking that the active y-intervals never overlap and always cover the full height.
- **The Skyline Problem** (218): sweep x-events, but the state is the *max height* among active buildings, so use a heap with lazy removal instead of a merged length. Every idea from Meeting Rooms II and Minimum Interval to Include Each Query applies.
- **Union of rectangles with large n** (10^5): the segment-tree sweep is mandatory. It is the same events in x, with "cover count > 0" lengths maintained per node over compressed y's.

## What to carry forward

To measure a union in two dimensions, sweep one axis with enter and leave events, and at each stop measure the other axis with Merge Intervals. Area = sum of (width x covered length), with each slab added before the event changes the active set. This closes the chapter by stacking every earlier idea: sort and merge (Merge Intervals), +1/-1 events with constant pieces between them (Meeting Rooms II, My Calendar III), a state that only changes at boundaries (every sweep here), and coordinate compression in the brute force. Faced with a new interval problem, ask the same two questions: which axis do I sweep, and what is the smallest state that makes everything to the left of the line finished?
