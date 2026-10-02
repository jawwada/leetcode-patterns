# Trapping Rain Water II

*LeetCode 407 · Hard · Pattern: Min-heap frontier expanding inward from the boundary (lowest wall first) · Reading time ~13 min*

## What the problem is really asking

You get a grid of non-negative heights, an elevation map seen from above. It rains a lot. Water flows between cells that share an edge (up, down, left, right), and it can leave the map only by flowing over the outer border. How much water stays on the map?

The answer is a volume: the sum, over every cell, of (final water surface at that cell) minus (the cell's height). So the real object is a second grid, the **water level** of each cell. Border cells have level equal to their own height, since water simply runs off them. For an interior cell, the level is decided by the *weakest escape route*: water rises until it finds the lowest way out.

That is the difficulty. In the one-dimensional version (Trapping Rain Water) a cell has exactly two escape directions, left and right, and its level is `min(tallest to the left, tallest to the right)`. In 2D, water can escape along any winding path, around corners, through a single low gap far away. The tallest wall in each of the four straight directions is not enough: a path can sneak around a tall wall.

Our example:

```text
 the board (heights)            B = border cell
        c0 c1 c2 c3 c4 c5
  r0  [  1  4  3  1  3  2 ]     B  B  B  B  B  B
  r1  [  3  2  1  3  2  4 ]     B  .  .  .  .  B
  r2  [  2  3  3  2  3  1 ]     B  B  B  B  B  B

 final water levels             water stored
  r1  [  3  3  3  3  3  4 ]     .  1  2  0  1  .
                                total = 1 + 2 + 0 + 1 = 4
```

The interior cells at `(1,1)`, `(1,2)`, `(1,4)` fill up to 3. The cell `(1,3)` is itself 3 tall and holds nothing.

## Do it by hand first

Think about the border as a **dam**. Water rises from outside. Where does it first get in? At the lowest point of the dam.

The lowest border cells have height 1: `(0,0)`, `(0,3)` and `(2,5)`. Water at level 1 pours over `(0,3)` and meets the cell behind it, `(1,3)`, which has height 3. That cell is taller than the water, so it holds nothing; instead it becomes *part of the dam*, a wall of height 3. The other two low corners have nothing unvisited behind them.

Next lowest: the 2s on the border, `(0,5)`, `(2,0)`, `(2,3)`. Behind them are border cells or `(1,3)`, already handled. Nothing new.

Next: the 3s. Water at level 3 pours over `(0,2)` into `(1,2)`, which has height 1. It fills to 3: two units. That cell is now part of the dam too, at level 3 (the water surface acts as a wall at that height). Over `(0,4)` into `(1,4)`, height 2: fills to 3, one unit. Over `(1,0)` into `(1,1)`, height 2: one unit. Total 4.

What did your hand keep? A **ring of cells that currently forms the dam**, each with the level water must reach to get over it, and it always asked: "where is the dam lowest?" A collection where you repeatedly take the minimum and add new members is a min-heap. You also kept a "done" mark on cells already absorbed into the dam: a visited grid.

## The first honest attempt

Define `level[c]` for every cell. Border: `level = height`. Interior: the water at a cell can stand no higher than its lowest neighbour's level (it would spill there), and no lower than its own floor. So `level[c] = max(height[c], min over neighbours of level[nb])`.

Start interior levels at infinity, sweep the whole grid applying the rule, and repeat until a sweep changes nothing. The answer is `sum(level - height)`.

Each sweep is `O(mn)`. How many sweeps? A drop in level can travel only one cell per sweep in the bad direction, and along a snaking corridor it may need `O(mn)` sweeps: `O((mn)^2)` total. The waste is plain:

```text
 sweep 1: every cell re-examined  . . . . . . . . . . . .
 sweep 2: every cell re-examined  . . . . . . . . . . . .
 sweep 3: every cell re-examined  . . . . . . . . . . . .
                                        ^
          only cells next to a just-lowered neighbour
          can change, yet all mn are recomputed each time
```

It recomputes cells whose levels are already final.

## The turning point

**Claim: if you always expand from the lowest cell of the current dam, every cell's level is final the moment it joins the dam, and it equals `max(level of the dam cell it came through, its own height)`.**

Picture the dam: all the cells that are already decided, drawn as a closed ring around the undecided interior. Water from inside can only escape by crossing that ring. Suppose the ring's lowest cell has level `L`. Then:

- No water inside can escape *below* `L`: every crossing point of the ring needs at least `L`.
- A neighbour `x` just behind that lowest cell *can* escape at `max(L, height[x])`: through that very cell.

So the level of `x` is exactly `max(L, height[x])`, and it is final; nothing discovered later can lower it, because later dam cells are never lower than `L` (levels only grow as the ring moves inward, since each new member's level is `max(L, own height) >= L`). If `height[x] < L`, the cell traps `L - height[x]` units of water. If `height[x] >= L`, it traps nothing and simply becomes a taller section of the dam.

This is Dijkstra's algorithm in disguise. The "distance" of a cell is its water level, and the "length" of a path is not the sum of its edges but the **highest wall along it**. You want the path to the border that minimises its highest wall (a minimax path). Dijkstra works for any path cost that never decreases as the path gets longer, and "max so far" never decreases. The border cells are all sources at once, with distance equal to their own height.

The machinery:

- a **min-heap** of `(level, r, c)` for the dam, seeded with every border cell;
- a **visited grid**, marked when a cell is *pushed*, so no cell enters the dam twice;
- pop the lowest, and for each unvisited neighbour: add `max(0, level - height)` to the answer, push `(max(level, height), r, c)`.

The second argument of that `max` is the most important line. A cell joins the dam at the *water* level when it is flooded, not at its floor height, because the water surface is what the next cell sees as a wall.

## Watch it work

Heap entries are `level@(r,c)`. The board marks cells: `#` popped (retired from the dam), `o` in the heap (the dam), `.` not yet reached.

Frame 1: Seed. All 14 border cells enter the heap.

```text
        c0 c1 c2 c3 c4 c5
  r0    o  o  o  o  o  o       heap min = 1
  r1    o  .  .  .  .  o       1@(0,0) 1@(0,3) 1@(2,5) ...
  r2    o  o  o  o  o  o       water 0
 array: [1@(0,0), 1@(0,3), 1@(2,5), 2@(2,0), 3@(0,4),
         2@(0,5), 3@(0,2), ...]
```

The dam is the whole border; its lowest points are three cells of height 1.

Frame 2: Pop the three level-1 cells. `(0,3)` admits `(1,3)`, height 3, at level `max(1,3) = 3`.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  o  o  #  o  o       (1,3): h 3 >= 1, no water
  r1    o  .  .  o  .  o       pushed 3@(1,3)
  r2    o  o  o  o  o  #       water 0
```

Water at level 1 got in at `(0,3)` and hit a taller cell, which became new dam.

Frame 3: Pop the level-2 cells `(0,5)`, `(2,0)`, `(2,3)`. All their neighbours are already visited.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  o  o  #  o  #       nothing admitted
  r1    o  .  .  o  .  o       heap min is now 3
  r2    #  o  o  #  o  #       water 0
```

The dam's lowest point has risen to 3; every remaining dam cell is at least 3.

Frame 4: Pop `3@(0,2)`. It admits `(1,2)`, height 1.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  o  #  #  o  #       (1,2): h 1 < 3
  r1    o  .  o  o  .  o       water += 3 - 1 = 2
  r2    #  o  o  #  o  #       pushed 3@(1,2)   water 2
```

The cell is flooded to 3 and joins the dam at 3, not at 1.

Frame 5: Pop `3@(0,4)`. It admits `(1,4)`, height 2.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  o  #  #  #  #       (1,4): h 2 < 3
  r1    o  .  o  o  o  o       water += 1
  r2    #  o  o  #  o  #       pushed 3@(1,4)   water 3
```

Frame 6: Pop `3@(1,0)`. It admits `(1,1)`, height 2.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  o  #  #  #  #       (1,1): h 2 < 3
  r1    #  o  o  o  o  o       water += 1
  r2    #  o  o  #  o  #       pushed 3@(1,1)   water 4
```

Every cell is now visited.

Frame 7: The remaining pops (`(1,1)`, `(1,2)`, `(1,3)`, `(1,4)`, `(2,1)`, `(2,2)`, `(2,4)`, then `4@(0,1)`, `4@(1,5)`) find no unvisited neighbours.

```text
        c0 c1 c2 c3 c4 c5
  r0    #  #  #  #  #  #
  r1    #  #  #  #  #  #       heap empty
  r2    #  #  #  #  #  #       answer 4
```

Across frames, the popped levels never decreased (1, 1, 1, 2, 2, 2, 3, ...), every unvisited cell touched only unvisited cells or dam cells, and each cell's water was added exactly once, at the moment it joined the dam.

## Why it is correct

**Invariant.** At every moment: (a) each visited cell carries its true water level; (b) every unvisited cell's neighbours are unvisited or in the heap, never retired, because retiring a cell pushes all its unvisited neighbours. So the heap is a ring that separates the unvisited region from the border.

**The greedy step, as an exchange argument.** The greedy choice is "breach the dam at its lowest cell `p`, level `L`". Suppose instead you believed some neighbour `x` of `p` deserved a level lower than `max(L, height[x])`. That would require an escape path from `x` to the border whose highest point is below `max(L, height[x])`. The path starts at `x`, so its highest point is at least `height[x]`. Look at the heap just before `p` was popped. The path starts at the unvisited cell `x`, so by (b) it must cross the ring at some heap cell `f` (possibly `p` itself) before reaching any retired cell or the border. From `f` onward, any route to the border has a highest point at least `level[f]`, by (a). And `level[f] >= L`, because `L` is the heap's minimum. So every escape path from `x` has a highest point of at least `max(L, height[x])`. The path through `p` achieves exactly that. Swapping any other escape route for the one through `p` never makes the level higher, so `max(L, height[x])` is the true level, and (a) is preserved for the new cell.

Notice where the greedy *order* matters. If you breached a higher dam cell `q` first, with level `Q > L`, a cell behind it would be assigned `max(Q, h)`, but its real escape might run through `p` at the lower level `L`. Popping the minimum is exactly what rules out a cheaper route through some other part of the ring.

When the heap empties, every cell is visited with its true level, and the sum of `level - height` over all cells is the volume.

## Cost

- **Time `O(mn log(mn))`.** Every cell is pushed and popped exactly once, and each pop inspects four neighbours.
- **Space `O(mn)`.** The visited grid, plus a heap that can hold up to `O(mn)` cells.

The relaxation version is `O((mn)^2)` time and `O(mn)` space.

## Variations you will meet

- **Trapping Rain Water (1D, LeetCode 42).** Two pointers replace the heap: the "dam" is just the two ends, and you always advance the lower end. That is this algorithm on a single row, where the ring has only two cells.
- **Swim in Rising Water (LeetCode 778).** One source, one target, and the answer is the minimax path value: the same "Dijkstra with max instead of sum", stopped when the target is popped.
- **Path With Minimum Effort (LeetCode 1631).** The edge weight is the height *difference* between neighbours, and the path cost is the largest such difference. Again Dijkstra with `max`.
- **Pacific Atlantic Water Flow (LeetCode 417).** Flood inward from each ocean's border, but only to cells at least as high. No levels to compute, so a plain BFS from the border suffices; the heap is needed only when the *order* of expansion decides the values.

## What to carry forward

When a value is set by the weakest point of a boundary, grow the boundary from its weakest point with a min-heap and every value is final the moment it is reached: Dijkstra, with "highest wall so far" in place of distance.

That closes the chapter. You started with a heap that only filtered: keep the `k` largest, and its root is the answer. You then used it to choose greedily, always the most frequent letter or the most profitable project, sometimes with a cooldown queue beside it. You merged `k` sorted sources by keeping one front item each, and balanced two heaps facing each other to expose a median. In the second half the heap became the engine of greedy proofs: procrastinate and take the largest past option when stuck, keep a plate and evict its worst item, fix the bottleneck and keep the best `k` behind it, shrink the extreme. Then it ran simulations: two heaps shuttling rooms, a heap with lazy deletion under a sweep line, and here a heap ordering a frontier across a grid. Facing a new problem, you can now ask: *which single item do I keep needing (the largest, the smallest, the earliest)?* *Does the set change by small steps?* *If I commit greedily to the root, can I swap any other choice for it without losing?* If yes, reach for a heap, and prove the greedy with a swap.
