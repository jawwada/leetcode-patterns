# Set Matrix Zeroes

*LeetCode 73 · Medium · Pattern: In-place markers (reuse first row/column as flags) · Reading time ~7 min*

## What the problem is really asking

You get an `m x n` grid. Every cell that is `0` *in the original grid* condemns its whole row and its whole column: all of them must become `0`. Do it in place, and the follow-up asks for `O(1)` extra space.

The answer is a modified grid. The difficulty is the phrase "in the original grid". The moment you write a `0` into a cell, that cell looks exactly like an original zero, and if a later step reads it, it will wrongly condemn another row and column. A chain reaction like that zeroes the entire grid.

```text
 input                 output
 1  2  3  4            0  0  3  4
 5 [0] 7  8     ->     0  0  0  0     row 1 and column 1
[0]10 11 12            0  0  0  0     row 2 and column 0
 two original zeros: (1,1) and (2,0)
```

## Do it by hand first

On paper you would first *look*, then *write*. Scan the grid, and jot down two lists in the margin: "rows with a zero: 1, 2" and "columns with a zero: 0, 1". Then go cell by cell: a cell becomes zero iff its row is on the first list or its column is on the second.

```text
           col flags:  c0  c1  c2  c3
                       Y   Y   .   .
 row flags   r0 .     1   2   3   4
             r1 Y     5   0   7   8
             r2 Y     0  10  11  12
 cell (r,c) -> 0  iff  row r flagged OR column c flagged
```

What did your hand keep track of? `m + n` yes/no marks in the margins. That is all the information the answer depends on. The seed is "two margin vectors"; the puzzle is where to put them without using extra memory.

## The first honest attempt

The most naive version copies the grid, and for every zero in the copy, writes zeros across its row and column in the original. It is `O(mn)` space for the copy and `O(mn(m+n))` time, because a row with `k` zeros is cleared `k` times.

The honest improvement is the hand solution: two sets, `zero_rows` and `zero_cols`, filled in one pass and applied in a second. That is `O(mn)` time, which is optimal, and `O(m + n)` space. It is the answer most people give first, and it is correct.

Where is the waste now? Not in time. In memory: we allocate two margin vectors while the grid already contains two strips of exactly the right lengths that we will have to overwrite anyway.

```text
 margins we allocate      strips we already own
  row flags: m slots        column 0 of the grid: m cells
  col flags: n slots        row 0 of the grid:    n cells
```

## The turning point

**Claim: the first column can hold the row flags and the first row can hold the column flags, because writing a flag there destroys nothing the final answer needs.**

Justify it carefully. Suppose cell `(r, c)` with `c >= 1` is zero. We write `0` into `matrix[r][0]` (flag "row `r` dies") and into `matrix[0][c]` (flag "column `c` dies"). Did we destroy information? `matrix[r][0]` is in row `r`, which is going to be zero in the output anyway. `matrix[0][c]` is in column `c`, also going to be zero anyway. So the flag overwrites a value whose final state is already decided. That is the key: we only ever write a `0` where the answer will be `0`.

There is one collision. Cell `(0, 0)` sits in both strips. It would have to mean both "row 0 dies" and "column 0 dies", and those are independent facts. Resolve it with one extra boolean: let `(0, 0)` mean "row 0 dies", and keep `first_col_zero` for column 0, computed *before* any flags are written (because flag writes put zeros into column 0).

```text
 storage plan
        c0     c1..c(n-1)
  r0  [row0?]  [ col flags for c1..c(n-1) ]
  r1  [ row ]
  ..  [ flags]       interior: cells with r>=1, c>=1
  rm  [r1..  ]
  + one boolean: first_col_zero
```

The second subtlety is *order of application*. The strips are both data and flags. If you zero row 0 early (because `(0,0)` says so), you wipe all the column flags before the interior has read them. So:

1. Compute `first_col_zero` from the original column 0.
2. Mark: for every cell with `c >= 1` that is zero, write the two flags.
3. Apply to the interior (`r >= 1`, `c >= 1`) using the flags.
4. Apply to row 0 using `(0, 0)`.
5. Apply to column 0 using `first_col_zero`.

Why does step 2 skip `c = 0`? A zero in column 0 is recorded by `first_col_zero`, and the cell itself already serves as its own row flag. Writing `matrix[0][0] = 0` for it would wrongly claim row 0 dies.

## Watch it work

Example: `[[1,2,3,4],[5,0,7,8],[0,10,11,12]]`. Flags live in the strips marked `*`.

Frame 1 — compute `first_col_zero`: column 0 holds `1, 5, 0`, so it is `True`.

```text
        c0   c1   c2   c3
  r0  *  1 *  2 *  3 *  4      first_col_zero = True
  r1  *  5    0    7    8
  r2  *  0   10   11   12
```

Frame 2 — mark pass. `(1,1)` is zero: write `matrix[1][0]=0` (row 1) and `matrix[0][1]=0` (col 1). Row 2 has no zero at `c>=1`; its `matrix[2][0]` is already `0` from the input.

```text
        c0   c1   c2   c3
  r0     1   [0]   3    4      col flags: c1
  r1    [0]   0    7    8      row flags: r1, r2
  r2     0   10   11   12
```

Frame 3 — interior pass. Row 1 flagged: `(1,2),(1,3)` become 0. Column 1 flagged: `(2,1)` becomes 0. Row 2 flagged: `(2,2),(2,3)` become 0.

```text
        c0   c1   c2   c3
  r0     1    0    3    4
  r1     0    0   [0]  [0]
  r2     0   [0]  [0]  [0]
```

Frame 4 — row 0: `matrix[0][0]` is `1`, so row 0 is not cleared (only the flag at `c1` is zero there, which is correct).

```text
  r0     1    0    3    4      (0,0) = 1 -> keep row 0
```

Frame 5 — column 0: `first_col_zero` is `True`, so all of column 0 becomes 0. Final grid.

```text
        c0   c1   c2   c3
  r0    [0]   0    3    4
  r1     0    0    0    0
  r2     0    0    0    0
```

Invariant across frames: after the mark pass, `matrix[r][0] == 0` iff row `r >= 1` must die, `matrix[0][c] == 0` iff column `c >= 1` must die, and `matrix[0][0] == 0` iff row 0 must die. The interior pass reads these strips but never writes them, so they stay valid until steps 4 and 5, which touch only the strips themselves. Note what the boolean saved us from: had `(0,0)` stood for column 0, frame 5's rule would also have wiped row 0's `3 4`.

## Why it is correct

Define the target: `(r, c)` is zero in the output iff some original zero shares its row or its column.

After step 1, `first_col_zero` is exactly "column 0 has an original zero". During step 2, every write is a `0` into a cell whose output is `0` (argued in the turning point). Does step 2 ever *read* a flag it wrote, mistaking it for an original zero? No. It scans row by row. Row 0 is scanned first, before any later row writes into it. While scanning row `r >= 1`, the writes go to `matrix[r][0]` (column 0, which the scan skips) and to row 0 (already scanned). So every cell step 2 reads still holds its original value, and after step 2 the strips hold exactly the flags stated in the invariant.

Step 3 sets each interior cell from two flags that step 3 itself never modifies, so each interior cell gets its correct value. Step 4 zeroes row 0 iff `(0,0)` is zero: either it was an original zero, or some cell in row 0 at `c >= 1` was. Both mean row 0 dies. Cells in row 0 that are not cleared keep either their original value or a column flag `0`, and a column flag is correct output for that cell because its column dies. Step 5 clears column 0 iff it had an original zero; cells in column 0 not cleared are either original values or row flags `0`, again correct output. Every cell ends right.

## Cost

- **Time:** `O(mn)` — one pass to mark, one pass over the interior, then one row and one column.
- **Space:** `O(1)` extra — one boolean; flags live in the grid's own first row and column.

The two-set version has the same time; the gain is only in space.

## Variations you will meet

- **"Use `O(m + n)` space" (the original constraint).** Two sets or two boolean arrays. Many interviewers accept this first and then ask for `O(1)`; say the set version, then move the sets into the strips.
- **Game of Life (LeetCode 289).** Also in place, also "the new value depends on the old neighbours". The trick there is encoding old and new state in one cell (e.g. values `2` and `3` meaning "was alive, now dead" and "was dead, now alive"). Same idea: make writes that keep the old information recoverable.
- **Only zero the row, or only the column.** Then one strip suffices and the `(0, 0)` collision disappears.

## What to carry forward

When the answer depends on only a few bits per row and column, store those bits inside the cells whose final value is already decided, and apply updates in an order that reads every flag before it is erased.

The next problem, Permutation Sequence, leaves the grid behind: instead of coordinates on a board, we use positions in a number system, where each digit picks a block of known size.
