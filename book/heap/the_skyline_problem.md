# The Skyline Problem

*LeetCode 218 · Hard · Pattern: Sweep line over events + max-heap with lazy removal · Reading time ~12 min*

## What the problem is really asking

Each building is a rectangle `[left, right, height]` standing on the ground. Look at the city from far away: you see one outline, the upper envelope of all the rectangles. Describe that outline as a list of **key points** `[x, y]`: the places where, walking left to right, the outline's height changes, and the new height there. The last key point always drops to height 0. Two consecutive key points may not share a height (no redundant points).

The answer is a list of corners. What makes it hard is overlap: a tall building can hide a short one completely, partially, or not at all, and when the tall one ends, the outline falls back to *whichever building is next tallest and still standing*, which may have started long ago.

Our example has three buildings, P, Q and R:

```text
 x       0    5    10
         |....|....|..
 P h10     #######         [2,9)
 Q h15      ####           [3,7)
 R h12        #######      [5,12)

 h
 15         +-------+
            |       |
 12         |       +---------+
            |                 |
 10       +-+                 |
          |                   |
  0 ------+                   +----
    0     2 3       7         12

 key points: [2,10] [3,15] [7,12] [12,0]
```

P is mostly hidden. It contributes the stretch from 2 to 3 and then never shows again, not even at its own right edge, x=9, because R is taller there.

## Do it by hand first

Put a ruler vertically at the left and slide it right. The outline's height at the ruler is "the tallest building the ruler currently cuts through". That height can only change where some building starts or ends, so stop the ruler only at edges: 2, 3, 5, 7, 9, 12.

- x=2: P starts. Standing: {P10}. Tallest 10. New height: corner `[2,10]`.
- x=3: Q starts. Standing: {Q15, P10}. Tallest 15: corner `[3,15]`.
- x=5: R starts. Standing: {Q15, R12, P10}. Tallest still 15: no corner.
- x=7: Q ends. Standing: {R12, P10}. Tallest 12: corner `[7,12]`.
- x=9: P ends. Standing: {R12}. Tallest still 12: no corner.
- x=12: R ends. Nothing standing. Height 0: corner `[12,0]`.

Your hand kept a **set of standing buildings** and asked one question of it at every stop: "what is the tallest?" Items get added (a building starts) and removed (a building ends), and you only ever read the maximum. That is a max-heap, with one complication we will meet in a moment: removal of an item that is not at the top.

## The first honest attempt

Collect every edge x, sort them, and at each one scan all `n` buildings for the tallest with `left <= x < right`. Emit `[x, h]` when `h` differs from the previous height. That is `2n` stops times `n` buildings: `O(n^2)`.

The repeated work is the scan. Between consecutive stops, exactly one building was added or removed, yet each stop rebuilds the whole picture:

```text
 stop   scanned          standing          changed
 x=2    P Q R            P                 +P
 x=3    P Q R            P Q               +Q
 x=5    P Q R            P Q R             +R
 x=7    P Q R            P R               -Q
 x=9    P Q R            R                 -P
 x=12   P Q R            -                 -R
        ^^^^^ full rescan every time, for a one-item change
```

## The turning point

**Claim: the outline's height at the sweep line is the maximum of the set of standing buildings, and that set changes by one building per edge, so a max-heap of standing buildings, read at its top after every edge, produces the skyline.**

The first half is the definition of the outline. The second half is the efficiency win: each edge costs one heap operation instead of a scan.

The difficulty is the "building ends" event. A heap gives you the top cheaply but cannot delete an item from the middle. When Q ends at x=7 it happens to be at the top, but when P ends at x=9 it is buried under R. Removing it would mean searching the heap.

**Lazy removal** dissolves the difficulty. Observe that we only ever *read the top*. A dead building buried in the heap is harmless: it influences nothing until it surfaces. So store each building as `(-height, right)` and, before reading the top, pop while the top's `right <= x`. A building is checked for death only when it is about to be reported as the maximum. Dead entries deeper down wait, and are thrown away when they reach the top, or never if the sweep ends first.

This makes the "building ends" event almost empty. In fact the end events are only there to make the sweep *stop* at that x, so that the lazy loop runs and the new height is read. The building to remove is identified by its stored right edge, not by the event.

Three details make the loop clean:

1. **A sentinel.** Start the heap with `(0, infinity)`: a building of height 0 that never ends. The heap is never empty, and when the last real building dies, the top is the sentinel, so the outline drops to 0 on its own.
2. **Emit only on change.** After each event, compare the top's height with the last key point's height; append `[x, top]` only if it differs. A dummy `[0, 0]` at the start of the output means "the last height" always exists; drop it at the end.
3. **Order events at the same x.** Encode a start as `(left, -height, right)` and an end as `(right, 0, 0)`. Sorting then puts starts before ends at the same x (negative before 0), and taller starts first. That prevents phantom corners: if a building ends at x where another starts, we never momentarily report a dip; if two start together, we never report the shorter first.

## Watch it work

Events, sorted: `(2,-10,9)`, `(3,-15,7)`, `(5,-12,12)`, `(7,0,0)`, `(9,0,0)`, `(12,0,0)`. The heap is shown as `height@right`, tallest first; `S` is the sentinel `0@inf`.

Frame 1: x=2, P starts. Push `10@9`.

```text
 heap  10@9  S           top 10   last 0
 out   [2,10]
```

The top changed from 0 to 10, so a corner is emitted.

Frame 2: x=3, Q starts. Push `15@7`.

```text
 heap  15@7  10@9  S     top 15   last 10
 out   [2,10] [3,15]
```

A taller building took the top.

Frame 3: x=5, R starts. Push `12@12`. Top is still 15.

```text
            15@7            array:
           /    \           [(-15,7), (-12,12),
       12@12    10@9         (-10,9), (0,inf)]
        /
       S
 out   [2,10] [3,15]        (no change, no corner)
```

R slides in under Q. The outline does not see it yet.

Frame 4: x=7, Q's end. Lazy loop: top `15@7` has right 7 <= 7, pop it. Top `12@12` is alive.

```text
 popped 15@7 (dead)
 heap  12@12  10@9  S    top 12   last 15
 out   [2,10] [3,15] [7,12]
```

The outline falls to the next tallest standing building, R, not to P.

Frame 5: x=9, P's end. Lazy loop: top `12@12` is alive (12 > 9). Nothing popped.

```text
 heap  12@12  10@9  S    top 12   last 12
               ^ dead (9 <= 9) but buried: ignored
 out   unchanged
```

P is dead but invisible. Leaving it in costs nothing.

Frame 6: x=12, R's end. Lazy loop pops `12@12` (12 <= 12), then the ghost `10@9` (9 <= 12). Top is the sentinel.

```text
 popped 12@12, then 10@9 (the ghost)
 heap  S                 top 0    last 12
 out   [2,10] [3,15] [7,12] [12,0]
```

The ghost was cleaned up the first time it reached the top. The sentinel reports ground level.

Across frames: after the lazy loop at each x, the top was always a building with `left <= x < right` and the tallest such; the output's last height always equalled the outline just left of the sweep line.

## Why it is correct

This is a sweep, not a greedy choice: the outline is fully determined, and there is nothing to exchange. The proof is an invariant.

**Invariant.** After processing the event at x (lazy loop, then push if it is a start), the heap contains every building with `left <= x < right` that has been seen, plus possibly some dead buildings (`right <= x`), plus the sentinel; and **the top is alive**.

*It holds.* Every building is pushed when the sweep reaches its left edge, and popped only when it is dead, so no live building is ever missing. The lazy loop runs until the top is alive, and the sentinel never dies, so the loop always stops with a live top. Pushing a live building cannot make the top dead.

*It implies the answer.* The top is the tallest entry in the heap and it is alive, so it is at least as tall as every live entry: it is the tallest standing building. Dead entries below it do not matter, because nothing below the top is ever read. So the top's height is exactly the outline's height just right of x. The outline changes only at edges, and we read the top after every edge, so every change is caught, and we emit only when the height differs, so no redundant point appears.

*Same-x events.* Several events can share an x, and we must not emit a height that exists only "between" two of them. Look at the first event at a given x. If it is a start, it is the tallest start at x (taller starts sort first), and its lazy loop has already removed every building with `right <= x`. If there is no start at x, the first event is an end, and its lazy loop does the same removal. Either way, after the first event the top already equals the true height at x. The remaining events at x are shorter starts (which cannot change the top) or ends whose buildings were already popped. So the first reading at x is final, and no phantom corner is emitted.

## Cost

- **Time `O(n log n)`.** Sorting `2n` events; each building is pushed once and popped at most once, `O(log n)` each.
- **Space `O(n)`.** The events and the heap, which can hold every building including ghosts.

The rescanning version is `O(n^2)` time, `O(n)` space.

## Variations you will meet

- **Eager removal with a sorted container.** Replace the heap with a balanced multiset of heights (in Python, `sortedcontainers.SortedList`); remove a height exactly at its right edge. Same complexity, no ghosts, but needs a structure beyond the standard library.
- **Divide and conquer.** Split the buildings in half, build both skylines, and merge two skylines like merging sorted lists, keeping the current height of each side and emitting the max. `O(n log n)` with no heap at all.
- **Area of the skyline / Rectangle Area II.** Instead of corners, sum `height × width` between consecutive edges. For overlapping rectangles in 2D, the sweep stays but the "structure of alive things" becomes a segment tree over y.
- **Falling Squares (LeetCode 699).** Squares stack on top of whatever is below instead of overlapping; the question is the max height after each drop. A sweep no longer applies because drops arrive in arbitrary x order; coordinate compression plus a segment tree replaces it.

## What to carry forward

Sweep the edges, keep the "alive" set in a heap, and delete lazily: a dead item only matters when it reaches the top, so check deaths only there. The next problem, Trapping Rain Water II, keeps "always look at the heap's extreme item" but turns the sweep line into a closed ring on a 2D grid that shrinks inward from the border.
