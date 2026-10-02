# Flood Fill

*LeetCode 733 · Easy · Pattern: Grid flood fill (DFS/BFS) · Reading time ~5 min*

## What the problem is really asking

You get an image as a grid of colour numbers, a starting pixel `(sr, sc)` and a new colour. Do what the paint-bucket
tool in any drawing program does: recolour the start pixel and every pixel you can reach from it by stepping up, down,
left or right through pixels of the start pixel's *original* colour. Diagonals do not count.

The answer is the same grid, modified. The set of pixels that change is one **connected component** of the grid graph:
the nodes are pixels, and an edge joins two side-by-side pixels of the old colour.

```text
  image, start (1,1), color 2       result
      c0 c1 c2                      c0 c1 c2
  r0   1  1  1                  r0   2  2  2
  r1   1 [1] 0                  r1   2  2  0
  r2   1  0  1                  r2   2  0  1
                                          ^
          (2,2) is a 1 but only touches 0s: not reached
```

The difficulty is organisational: reach every connected pixel, touch no disconnected one, and never process a pixel
twice.

## Do it by hand first

With a pen you would colour the start cell, then look at its four neighbours, colour the ones that are still 1, and
remember that those new cells still need *their* neighbours checked. You keep a little to-do list of "painted but not
yet looked around":

```text
  paint (1,1)           to-do: (1,1)
  look around (1,1)     paint (0,1),(1,0)
                        to-do: (0,1),(1,0)
  look around (1,0)     paint (0,0),(2,0)
                        to-do: (0,1),(0,0),(2,0)
  ...until the to-do list is empty
```

That to-do list is the whole data structure: the frontier of the spreading paint, cells already wet whose neighbours
might not be. Taking from its end (stack, DFS) or its front (queue, BFS) does not matter here; we want *which* cells,
not distances.

## The first honest attempt

Without a to-do list, you might sweep the whole grid repeatedly: "paint any old-colour pixel that touches an
already-painted pixel", and repeat until a sweep paints nothing.

```text
  sweep 1: scan all 9 cells, paint the ones touching paint
  sweep 2: scan all 9 cells again ...
  sweep k: scan all 9 cells, nothing new -> stop

  snake-shaped region (o = old colour, # = other):
    o o o o o
    # # # # o
    o o o o o        each sweep may extend the paint by
    o # # # #        only a few cells along the snake
    o o o o o
```

Correct but slow: a snake can need O(m*n) sweeps of O(m*n) each, so O((m*n)^2). Every sweep re-examines pixels that
are already painted or never will be. Only pixels next to *freshly* painted ones can change, and the sweep does not
know which those are.

## The turning point

**Claim: only the neighbours of a pixel just painted can become painted next, so keep exactly those pixels in a
container and look nowhere else.**

A pixel joins the region because it touches a region pixel and has the old colour. So painting a pixel is the only
event that creates new candidates, and they are its four neighbours. Push each newly painted pixel onto a stack; when
you pop it, check its four neighbours.

The second half is the visited set. A pixel pushed twice could make the stack cycle between two neighbours forever.
But painting changes a pixel's colour away from `old`, and the push test is "neighbour still equals `old`". So
**painting is the visited mark**.

That needs painting to change something. If `old == color`, painted pixels still match and the loop never ends, so
return at once; the image is already correct. And paint at **push** time: painting on pop would let (0,0) be pushed by
both (1,0) and (0,1).

## Watch it work

Stack top is on the right. `*` marks painted pixels (value 2), `[ ]` marks the pixel being popped.

```text
Frame 1  start: paint (1,1), push it
      c0 c1 c2
  r0   1  1  1        stack: [(1,1)]
  r1   1  *  0
  r2   1  0  1
```

Painted at once, so nothing can push it again.

```text
Frame 2  pop (1,1); up (0,1)=1 paint+push;
         down (2,1)=0 no; left (1,0)=1 paint+push
      c0 c1 c2
  r0   1  *  1        stack: [(0,1), (1,0)]
  r1   * [*] 0
  r2   1  0  1
```

Two neighbours matched the old colour and were painted on the spot.

```text
Frame 3  pop (1,0); up (0,0) paint+push; down (2,0) paint+push
      c0 c1 c2
  r0   *  *  1        stack: [(0,1), (0,0), (2,0)]
  r1  [*] *  0
  r2   *  0  1
```

LIFO: DFS dives into (1,0) before returning to (0,1).

```text
Frame 4  pop (2,0): neighbours are painted or 0, nothing pushed
         pop (0,0): neighbours (0,1),(1,0) already painted
      c0 c1 c2
  r0  [*] *  1        stack: [(0,1)]
  r1   *  *  0
  r2  [*] 0  1
```

(0,1) was painted at push time, so (0,0) does not push it again.

```text
Frame 5  pop (0,1); right (0,2)=1 paint+push
      c0 c1 c2
  r0   * [*] *        stack: [(0,2)]
  r1   *  *  0
  r2   *  0  1
```

The last cell of the region joins.

```text
Frame 6  pop (0,2): down (1,2)=0, nothing new. stack empty
      c0 c1 c2
  r0   2  2  2        stack: []
  r1   2  2  0        (2,2) never touched: its only
  r2   2  0  1        neighbours are 0s
```

In every frame, each stacked pixel is already painted, and each painted pixel is either stacked or has had its
neighbours checked. An empty stack means no painted pixel has an unchecked neighbour.

## Why it is correct

Invariant: every pixel in the stack or already popped is painted and belongs to the region; every popped pixel has had
all four neighbours examined.

*Nothing outside the region is painted*: we only paint a pixel that has the old colour and is adjacent to a painted
region pixel, which is exactly the definition of being connected to the start.

*Everything in the region is painted*: if region pixel p stayed unpainted, some old-colour path from the start to p
has a painted pixel next to an unpainted one. The painted one was popped and its neighbours checked, so that neighbour
would have been painted. Contradiction.

*It terminates*: each pixel is pushed at most once, because pushing paints it and painted pixels fail the push test.

## Cost

- **Time O(m*n).** Each pixel is pushed and popped at most once, with four neighbour checks each.
- **Space O(m*n).** The stack can hold much of the region at once. A recursive DFS uses the same space on the call
  stack and can overflow Python's recursion limit.

## Variations you will meet

- **BFS instead of DFS.** Swap in a `deque` and `popleft`. Same pixels, same cost; the paint spreads in rings. It
  matters only once a question asks for distances.
- **8-directional connectivity.** Add the four diagonal offsets. Nothing else changes.
- **Colour only the border of the component** (LeetCode 1034). Flood to find the component, then repaint cells with a
  neighbour outside it or on the grid edge. You need a separate visited set, since you still compare against the old
  colour while deciding which cells are border cells.

## What to carry forward

A flood fill is "push the start, pop, push matching neighbours, mark on push"; when you can write into the grid, the
grid itself is the visited set. The next problem runs this flood once per unvisited land cell and counts how many floods
it had to start.
