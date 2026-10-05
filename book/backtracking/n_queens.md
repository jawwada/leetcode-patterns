# N-Queens
*LeetCode 51 · Hard · Pattern: Row-by-row backtracking with column/diagonal sets · Reading time ~10 min*

## The problem

Place n queens on an n x n board so that no two attack each other (same row, column or diagonal) and return every
distinct board as a list of strings with Q for a queen and . for empty.

```text
Example: n=4 ->
  [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]].
  Example: n=1 -> [["Q"]].
```

## What the problem is really asking

Put `n` queens on an `n x n` chessboard so that no two attack each other. A queen attacks
along its row, its column and both diagonals, any distance. Return **every** arrangement,
each drawn as `n` strings with `Q` for a queen and `.` for an empty square.

The answer is a list of boards. For `n = 4` there are exactly two:

```text
  solution A            solution B
    c0 c1 c2 c3           c0 c1 c2 c3
  r0 .  Q  .  .         r0 .  .  Q  .
  r1 .  .  .  Q         r1 Q  .  .  .
  r2 Q  .  .  .         r2 .  .  .  Q
  r3 .  .  Q  .         r3 .  Q  .  .

  stored as columns per row:  [1,3,0,2]     [2,0,3,1]
```

What makes it hard: the constraints are global. Whether a square is safe depends on every
queen already placed, along four different kinds of line. And we need all solutions, so we
cannot stop at the first one; we have to walk the whole space of placements and keep only
the legal leaves. The challenge is to make "is this square attacked?" cheap and to discard
illegal partial boards long before they are complete.

## Do it by hand first

Take `n = 4`. There must be exactly one queen per row (two in a row would attack), so think
of it as choosing a column for row 0, then row 1, and so on.

Put the first queen at row 0, column 0. Now shade what it attacks: all of column 0, and the
diagonal running down-right through (1,1), (2,2), (3,3). In row 1, columns 0 and 1 are
shaded, so try column 2. Shade again. Row 2 is now fully shaded: column 0 by the first
queen, column 2 by the second, column 1 by the second queen's down-left diagonal, column 3
by its down-right diagonal. You erase the row-1 queen and try column 3 instead.

```text
  after (0,0) and (1,2)        * = attacked
     c0 c1 c2 c3
  r0  Q  *  *  *
  r1  *  *  Q  *
  r2  *  *  *  *      <- every square attacked: back up
  r3  *  .  *  *
```

What your hand tracked: which **columns** are taken and which **diagonals** are taken. You
shaded lines, not squares. That is the seed of the data structure: a queen "owns" one
column and two diagonals, and a square is safe exactly when none of its three lines is
owned.

## The first honest attempt

Since there is one queen per row and one per column, a placement is a permutation: row `r`
gets column `perm[r]`. Enumerate all `n!` permutations, check every pair of queens for a
shared diagonal (`|c_i - c_j| == |i - j|`), and render the ones that pass.

Cost: `O(n! * n^2)`. For `n = 8` that is 40,320 permutations times 28 pair checks. Now
look at the waste:

```text
  permutations starting with columns [0, 1, ...]

    r0  Q  .  .  .     queens (0,0) and (1,1) share a
    r1  .  Q  .  .     diagonal -- already illegal
    r2  ?  ?  ?  ?
    r3  ?  ?  ?  ?     yet all (n-2)! tails are generated:
                       [0,1,2,3] x   [0,1,3,2] x
                       each rejected at the END, separately
```

A conflict created in the first two rows is not noticed until the board is full. The
`(n - 2)!` completions of that doomed prefix are each built and checked. Using permutations
already pruned columns for free; diagonals are still checked only at the leaf.

## The turning point

**Claim: a new queen at (r, c) conflicts with earlier queens if and only if its column `c`,
its down-right diagonal `r - c`, or its down-left diagonal `r + c` is already owned; three
hash sets answer this in O(1), so a conflict is detected at the node where it is created.**

The key fact is about diagonals. Walk down-right from any square: row and column both go
up by one, so `r - c` never changes. Walk down-left: row goes up, column goes down, so
`r + c` never changes. Every diagonal is therefore labelled by a single integer.

```text
  r - c on a 4x4 board         r + c on a 4x4 board
     c0  c1  c2  c3              c0  c1  c2  c3
  r0  0  -1  -2  -3           r0  0   1   2   3
  r1  1   0  -1  -2           r1  1   2   3   4
  r2  2   1   0  -1           r2  2   3   4   5
  r3  3   2   1   0           r3  3   4   5   6

  equal numbers = same "\" line   equal numbers = same "/" line
```

So the attack state of the whole board is three sets: `cols`, `diag` (values of `r - c`)
and `anti` (values of `r + c`). Rows need no set because we place exactly one queen per row
by construction. Placing a queen adds three numbers; lifting it removes the same three.

The algorithm: `dfs(r)` tries each column `c` of row `r`. If `c`, `r - c` or `r + c` is in
its set, skip that column: the whole subtree under it is pruned without being generated.
Otherwise add to the three sets, record the column in `queens`, recurse to `dfs(r + 1)`, and
on return remove from the sets and pop. When `r == n`, every row has a safe queen, so
render the board from `queens` and record it.

Compare with the brute force: the tree has the same shape (n levels, up to n children each),
but the safety test moved from the leaf to the node. In practice most children are cut the
moment they appear, and the leaves that survive are exactly the solutions. Nothing is ever
checked twice; nothing illegal is ever extended.

A common slip is to use `r + c` for both diagonals. The two families need different keys,
which is why there are two sets. Another is forgetting to remove from the sets on the way
back: the next sibling then sees phantom attacks and solutions silently disappear.

## Watch it work

`n = 4`. Each frame shows the board (`Q` placed, `*` attacked, `.` free) and the three
sets. Columns are tried left to right; `x` marks a pruned branch.

```text
Frame 1   row 0: place at c0
  r0  Q  *  *  *     cols = {0}
  r1  *  *  .  .     diag = {0}      (r-c)
  r2  *  .  *  .     anti = {0}      (r+c)
  r3  *  .  .  *
```
One queen owns column 0, the main diagonal and the single corner anti-diagonal.

```text
Frame 2   row 1: c0 x (col), c1 x (diag 0), place c2
  r0  Q  .  .  .     cols = {0,2}
  r1  .  .  Q  .     diag = {0,-1}
  r2  x  x  x  x     anti = {0,3}
  row 2: c0 col, c1 anti 3, c2 col, c3 diag -1
```
Row 2 has no free square, so `dfs(2)` loops through four skips and returns with nothing.

```text
Frame 3   undo (1,2); row 1 place c3; row 2 place c1
  r0  Q  .  .  .     cols = {0,3,1}
  r1  .  .  .  Q     diag = {0,-2,1}
  r2  .  Q  .  .     anti = {0,4,3}
  r3  x  x  x  x     c0 col, c1 col, c2 diag 1, c3 col
```
Deeper this time, but row 3 is fully attacked. Row 2's other columns (c2 diag 0, c3 col)
are also pruned, so row 1 is exhausted.

```text
Frame 4   undo back to row 0; place c1
  r0  .  Q  .  .     row 1: c0 x anti 1
  r1  .  .  .  Q            c1 x col
  r2  Q  .  .  .            c2 x diag -1
  r3  .  .  Q  .            c3 placed
                     row 2: c0 placed; row 3: c2 placed
```
Every row finds a safe square: `queens = [1,3,0,2]`, the first solution is recorded.

```text
Frame 5   unwind; row 0 c2 gives [2,0,3,1]
  tree (row 0 choices):
     c0 -> c2 x , c3 -> c1 x        0 solutions
     c1 -> c3 -> c0 -> c2  OK       [1,3,0,2]
     c2 -> c0 -> c3 -> c1  OK       [2,0,3,1]
     c3 -> (mirror of c0)           0 solutions
```
The search finishes with two boards; every dead branch was cut at the row where it died.

Across the frames, the three sets always held exactly the lines owned by the queens
currently on the board, and `queens` had one entry per filled row. Every branch that was
cut had a conflict at its own node, never later.

## Why it is correct

**Invariant.** When `dfs(r)` is called, rows `0..r-1` each hold one queen, no two of them
attack each other, and `cols`, `diag`, `anti` contain exactly the column, `r - c` and
`r + c` values of those queens.

**Preservation.** A column passes the test only if its column and both diagonal labels are
unowned, which, by the label argument above, means the new queen attacks no earlier queen.
Adding its three labels keeps the sets exact for the child. Removing them on return
restores the caller's sets exactly (each label was owned by this queen alone, since it was
absent before).

**Soundness.** At `r == n` the invariant says all `n` queens are pairwise safe, so every
recorded board is legal.

**Completeness.** Any legal board has one queen per row, and its queen in row `r` is safe
with respect to rows above, so at each level the DFS tries that column and does not prune
it. Each legal board is reached by exactly one root-to-leaf path, so it is recorded once.

## Cost

- **Time `O(n!)`.** Row `r` has at most `n - r` free columns, so the surviving tree is
  bounded by `n!` nodes; the diagonal sets cut it far below that (for `n = 8`, 2,056
  placements against 40,320 permutations). Rendering adds `O(n^2)` per solution.
- **Space `O(n)`** for the three sets, `queens`, and recursion depth, beyond the output.
- The brute force is `O(n! * n^2)`.

## Variations you will meet

- **N-Queens II (LeetCode 52): count only.** Same search, increment a counter at the leaf;
  no rendering.
- **Bitmask version.** Store `cols`, `diag`, `anti` as integers shifted per row; the free
  squares of a row are `~(cols | diag | anti) & full`, and you pop the lowest bit each
  time. This is the fastest known simple solver and is the same trick Sudoku uses next.
- **Return one solution fast.** Stop at the first leaf, or use the known constructive
  pattern for `n >= 4`; interviewers mostly want to see the pruning, though.
- **Other pieces (rooks, kings, knights).** Change which lines a piece owns. Rooks own only
  rows and columns (answer `n!`); kings and knights own neighbourhoods, so a set of
  attacked squares replaces the line labels.

## What to carry forward

Give every constraint line a numeric label (`c`, `r - c`, `r + c`) and keep a set of owned
labels, so safety is O(1) and conflicts die at the node that creates them. Sudoku Solver,
next, has the same shape with nine digits instead of one queen, and adds a new question:
which empty cell should you fill first?
