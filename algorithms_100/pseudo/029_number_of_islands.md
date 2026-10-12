---
rank: 29
slug: number_of_islands
---

Given a grid of `"1"` for land and `"0"` for water, count the islands: groups of land cells joined up, down, left or right, never diagonally. The grid with rows `11000`, `11000`, `00100` and `00011` has `3` islands, a two-by-two block at the top left, a single cell in the middle and a pair at the bottom right.

Read the grid as a graph whose nodes are land cells and whose edges join horizontal and vertical neighbors. An island is a connected component, so counting islands is counting components. A scan walks every cell in reading order; whenever it meets a `"1"`, that cell belongs to an island nobody has counted yet, so the count goes up by one. Then a flood fill sinks the whole island, turning every land cell reachable from that start into `"0"`. Sinking is the visited mark, written straight into the grid: when the scan later reaches another cell of the same island it finds water and moves on, so each island is counted exactly once, at its first cell in reading order.

The flood fill is the depth-first search of #28 on a graph that is never built. The four neighbors of `(row, col)` are one step down, up, right and left, computed on the fly. This version pushes all four without looking and lets the pop decide: a position off the map, on water or on land already sunk is thrown away, and a land cell is sunk and pushes its own four neighbors. Only the set of cells reached matters here, not their order, so this simplest form is enough.

```text
the grid      sink order     the scan
1 1 0 0 0     1 2 . . .      (0, 0) is land: count 1, sink 4 cells in 17 pops
1 1 0 0 0     4 3 . . .
0 0 1 0 0     . . 1 . .      (2, 2) is land: count 2, sink 1 cell in 5 pops
0 0 0 1 1     . . . 1 2      (3, 3) is land: count 3, sink 2 cells in 9 pops
every other cell is water by the time the scan reaches it → 3 islands
```

```pseudo
FUNCTION NumIslands(grid)
    count ← 0
    FOR row FROM 0 TO len(grid) - 1
        FOR col FROM 0 TO len(grid[0]) - 1
            IF grid[row][col] = "1"
                count ← count + 1          // a new island starts here
                Sink(grid, row, col)       // so it is never counted again
    RETURN count

FUNCTION Sink(grid, start_row, start_col)
    stack ← empty stack
    stack.push((start_row, start_col))
    WHILE stack is not empty
        (row, col) ← stack.pop()
        IF row < 0 OR row ≥ len(grid) OR col < 0 OR col ≥ len(grid[0])
            CONTINUE                       // stepped off the map
        IF grid[row][col] ≠ "1"
            CONTINUE                       // water, or land already sunk
        grid[row][col] ← "0"               // sinking is the visited mark
        stack.push((row + 1, col))         // down, up, right, left
        stack.push((row - 1, col))
        stack.push((row, col + 1))
        stack.push((row, col - 1))
```

Every cell is scanned once and sunk at most once, and each sinking pushes four positions, so the count costs `O(R × C)` time for `R` rows and `C` columns, and the stack can reach `O(R × C)` on solid land. The recursive form reads the same, with `Sink` calling itself on the four neighbors instead of pushing them, but on a 300 by 300 grid of land it snakes through every cell and goes 90,000 calls deep, far past Python's recursion limit; the explicit stack has no such ceiling. When the caller's grid must survive, keep a visited set of positions instead of sinking. Signals are a grid and "how many groups"; the same fill measures the largest island by counting cells as it sinks them, recolors a region in flood fill, and solves surrounded regions by first marking everything connected to the border. The classic mistake in Python is dropping the `row < 0` or `col < 0` test: `grid[-1]` silently reads the last row, so an island on the top edge leaks into one on the bottom edge.

*Practice:* LC 200 Number of Islands · LC 695 Max Area of Island · LC 733 Flood Fill · LC 130 Surrounded Regions
