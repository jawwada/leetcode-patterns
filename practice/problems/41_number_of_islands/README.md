# Number of Islands (LeetCode 200)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** scan for unvisited land, flood fill with a stack, mark visited on push, count the floods

## Problem

Given an m × n grid of `'1'` (land) and `'0'` (water), count the islands: maximal groups of `'1'`s connected up, down, left or right (not diagonally). The grid must not be modified.

## Example

```
1 1 0 0 0
1 1 0 0 0        -> 3
0 0 1 0 0
0 0 0 1 1
```

The 2 × 2 block, the lone cell at (2,2), and the pair on the bottom row.

## Brute force

Treat the land cells as nodes of a graph and use union-find: give every land cell its own parent, union each land cell with its right and down land neighbours, then count the distinct roots.

O(mn · α(mn)) time and O(mn) space for the parent table, so asymptotically fine, but it builds and walks a parent structure (two `find` calls per edge, path lengths that grow without compression) when all the question needs is "how many times does a scan have to start a new region". The flood fill below touches each cell exactly once with a plain stack and no parent table.

## From brute force to optimal

Once any search from a cell of an island finishes, every cell of that island has been seen, so no other cell of it should ever start a new search. Scan the grid row by row; each time you meet land that is not yet visited, that is a brand-new island: count it, then flood the whole island so none of its other cells triggers another count. Marking a cell visited *when it is pushed* (not when it is popped) guarantees each cell enters the stack at most once, so the whole pass is O(mn).

## Intuition

Pour paint onto the grid. The scan pointer walks cell by cell; whenever it lands on dry land it pours, and the paint spreads to every 4-connected land cell. The number of pours is the number of islands. The stack is the wet front of the paint expanding outward from the pour point; the `seen` matrix is the paint itself. Painted land is never poured on again, which is where the linear time comes from.

## Walkthrough

Neighbours are tried in the order down, up, right, left. The visited grid is drawn after each island with `#` for visited land, `1` for land not yet reached, `0` for water.

```
scan (0,0): land, unvisited -> island #1, mark (0,0), stack [(0,0)]
  pop (0,0)   down (1,0) land -> mark, push      right (0,1) land -> mark, push    stack [(1,0),(0,1)]
  pop (0,1)   down (1,1) land -> mark, push      left (0,0) already seen          stack [(1,0),(1,1)]
  pop (1,1)   all neighbours water or seen                                        stack [(1,0)]
  pop (1,0)   all neighbours water or seen                                        stack []
  island #1 done     ##000 / ##000 / 00100 / 00011

scan (0,1) (1,0) (1,1): land but visited -> skip        scan the 0s -> skip
scan (2,2): land, unvisited -> island #2, mark, stack [(2,2)]
  pop (2,2)   all four neighbours water                                           stack []
  island #2 done     ##000 / ##000 / 00#00 / 00011

scan (3,3): land, unvisited -> island #3, mark, stack [(3,3)]
  pop (3,3)   right (3,4) land -> mark, push                                      stack [(3,4)]
  pop (3,4)   left (3,3) already seen                                             stack []
  island #3 done     ##000 / ##000 / 00#00 / 000##

scan (3,4): visited -> skip.  End of grid: 3 islands.
```

Every land cell was pushed exactly once; the three pours are the answer.

## Steps

1. `seen` = all `False`, `count = 0`.
2. For every cell `(r, c)`: if it is `'1'` and not seen, `count += 1`, mark it seen, push it.
3. While the stack is non-empty: pop `(x, y)`; for each of the four neighbours that is in bounds, is `'1'` and not seen, mark it seen and push it.
4. Return `count`.

## Complexity

O(mn) time: every cell is examined by the scan once and pushed at most once. O(mn) space for `seen` and, in the worst case (one giant island), the stack.

## Pitfalls

- **Starting a flood from already-visited land.** Dropping `and not seen[r][c]` makes every land cell its own island: the example returns 7.
- **Swapping the bounds.** `nx` is a row index and is bounded by `rows`; `ny` by `cols`. Swapped bounds crash with `IndexError` or miss rows on non-square grids.
- **Only looking down and right.** An island can bend back up or left of the scan; a U shape like `111 / 001 / 111` is then counted twice. Check all four directions.
- **Marking on pop instead of on push.** Still gives the right count, but a cell can sit in the stack several times and the stack can grow past mn; marking on push keeps the invariant "each cell pushed once".
- **Mutating the input.** Sinking `'1'`s to `'0'` is a valid trick but destroys the caller's grid; a separate `seen` matrix avoids that.
- **Recursion depth.** A recursive DFS on a 300 × 300 all-land grid blows the Python stack; use an explicit stack.
