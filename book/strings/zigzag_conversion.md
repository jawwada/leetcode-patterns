# Zigzag Conversion

*LeetCode 6 · Medium · Pattern: Row buckets with a bouncing row pointer · Reading time ~7 min*

## What the problem is really asking

You are given a string and a number of rows. Imagine writing the string on squared paper: go straight down the first column, then climb diagonally back up to the top row, then go down again, and so on, like a saw blade. When you are done, read the paper row by row, left to right, top row first. Return that reading.

The answer is a string of the same length as the input. It is a permutation of the input characters. Nothing is computed about the characters themselves; the whole problem is about where each character lands.

```text
s = "PAYPALISHIRING", numRows = 3

 row 0:  P       A       H       N
 row 1:  A   P   L   S   I   I   G
 row 2:  Y       I       R

 read row 0, then 1, then 2:
 "PAHN" + "APLSIIG" + "YIR" = "PAHNAPLSIIGYIR"
```

What makes it feel hard is that the picture is two-dimensional, with columns that have one or several characters, and diagonals that leave holes. People spend their time computing column numbers and gap widths. The trick is to notice that half of that picture is irrelevant.

## Do it by hand first

Take a shorter input, `"PAYPALI"` with 3 rows, and actually draw it. Your pen goes down, then up, then down:

```text
 pen path:  P  A  Y  P  A  L  I
 row:       0  1  2  1  0  1  2
            down  ^bottom ^top  ^bottom

 paper:  P       A
         A   P   L
         Y       I
```

Now read it. Row 0 is `P A`. Row 1 is `A P L`. Row 2 is `Y I`. Look at how you read row 1: you did not care that `A` was in column 0, `P` in column 1, `L` in column 2. You only cared that they were all in row 1 and in what order your pen put them there. And the order your pen put them there is simply the order they appear in the input.

So what your hand actually kept track of was two things: which row the pen is on right now, and which way it is moving (down or up). That pair, a row index and a direction, is the seed of the whole solution.

## The first honest attempt

The honest first approach is to simulate the paper. Allocate a grid of `numRows` rows and `n` columns, all blank. Walk the zigzag: while going down, increase the row; at the bottom, switch to going up, and while going up, increase the column on every step as well as decreasing the row. Place each character at its `(row, col)`. At the end, scan the grid row by row and collect the non-blank cells.

It is correct, and it is `O(numRows * n)` in both time and space. The waste is visible in the drawing:

```text
 grid 3 x 14 for "PAYPALISHIRING" (. = blank cell)

 P . . . A . . . H . . . N . . . ...
 A . P . L . S . I . I . G . . . ...
 Y . . . I . . . R . . . . . . . ...
   ^   ^   ^   ^   ^   ^   ^
   diagonal columns: one char, the rest blank
```

Most cells are blank. We pay to allocate them and then pay again to scan past them, only to throw them away. With 1000 rows and a 1000-character string, that is a million cells to hold a thousand characters. The column coordinate is what creates the grid, and the column coordinate is exactly what the output never uses.

## The turning point

**Claim: the output depends only on which row each character lands in; within a row, characters appear in input order.**

Why is that true? Along the zigzag the column number never decreases: going down it stays the same, going up it increases. So if character `a` comes before character `b` in the input and both land in the same row, `a` is at a column no greater than `b`'s. Could they share a column? Only on a vertical stroke, and on a vertical stroke every row appears once, so two characters in the same row cannot share a column. Hence in each row, left-to-right order is the same as input order.

That kills the grid. Replace it with one list per row, a "bucket". Each character is appended to the bucket of the row it lands in. Appending preserves input order, which by the claim is exactly the left-to-right order on paper.

All that remains is computing the row for each character, and your hand already told you how: the row index bounces. It goes `0, 1, 2, ..., numRows-1`, then `numRows-2, ..., 1, 0`, then up again. Keep a pointer `r` and a step of `+1` or `-1`. After placing a character, if you are on the top row the step becomes `+1`; if you are on the bottom row it becomes `-1`; then move.

```text
 numRows = 4: the row pointer bounces like a ball

 r: 0 1 2 3 2 1 0 1 2 3 2 1 0 ...
    \     /\     /\     /
     \   /  \   /  \   /
      \ /    \ /    \ /
  top=0      bottom=3 reverses step
```

Two small edge cases fall out of the bounce. If `numRows == 1`, the top row is also the bottom row and the step would flip on every character without ever moving, so return the string unchanged. If `numRows >= n`, the pen never reaches the bottom; each character is alone in its row and the output is the input. The solution handles both with one guard.

The order of operations matters: append first, then decide the step, then move. If you flip before appending, every character lands one row off.

## Watch it work

`s = "PAYPALISHIRING"`, `numRows = 3`. State: the three buckets, the row pointer `r`, the step.

Frame 1. The first three characters go straight down.

```text
 read: P A Y          r after: 1   step: -1
 rows[0]: P
 rows[1]: A
 rows[2]: Y      <- r hit 2 (bottom), step flips to -1
```

`Y` landed on the bottom row, so the step turned negative and `r` moved back to 1.

Frame 2. The pen climbs: `P` to row 1, `A` to row 0.

```text
 read: P A            r after: 1   step: +1
 rows[0]: P A    <- r hit 0 (top), step flips to +1
 rows[1]: A P
 rows[2]: Y
```

At the top the step flips again; the next character will go to row 1.

Frame 3. Down again: `L` to row 1, `I` to row 2; then up: `S` to row 1, `H` to row 0.

```text
 read: L I S H        r after: 1   step: +1
 rows[0]: P A H
 rows[1]: A P L S
 rows[2]: Y I
```

Each bucket only grew at its right end; nothing was ever inserted in the middle.

Frame 4. The rest: `I`->1, `R`->2, `I`->1, `N`->0, `G`->1.

```text
 rows[0]: P A H N
 rows[1]: A P L S I I G
 rows[2]: Y I R
 r sequence overall: 0 1 2 1 0 1 2 1 0 1 2 1 0 1
```

Frame 5. Concatenate the buckets top to bottom.

```text
 "PAHN" + "APLSIIG" + "YIR" -> "PAHNAPLSIIGYIR"
```

Across all frames, two things held: `r` always stayed in `[0, numRows-1]` because the step reversed exactly at the two walls, and every bucket held its row's characters in input order. The column never appeared anywhere.

## Why it is correct

Two facts, one per half of the algorithm.

First, the bounce produces the right row for every character. The zigzag on paper is defined as down to the bottom, diagonally up to the top, repeat. The row sequence of that path is precisely `0..numRows-1..0..` repeating, and the pointer reproduces it: it moves by one each step and reverses only at row 0 and row `numRows-1`. By induction on the character index, character `k` gets the same row the paper drawing gives it.

Second, the order inside each row is right. That is the claim from the turning point: columns are non-decreasing along the path and no two characters of one row share a column, so left-to-right order on paper equals input order, which is append order.

Reading the paper row by row is then exactly concatenating the buckets in row order.

## Cost

- Time `O(n)`: each character is appended once, and the final join touches each character once.
- Space `O(n)`: the buckets together hold exactly `n` characters (plus the output string).

There is also a pure index-arithmetic version: the pattern repeats every `cycle = 2 * numRows - 2` characters, and row `r` takes indices `k*cycle + r` and, for middle rows, `k*cycle + cycle - r`. Same time, only the output buffer, but easier to get wrong.

## Variations you will meet

- **Decode the zigzag.** Given the row-by-row string and `numRows`, recover the original. Run the same bounce on a dummy string to count how many characters each row receives, slice the encoded string into rows of those sizes, then replay the bounce taking the next character from each row's slice.
- **Write the zigzag by cycle formula.** Some interviewers ask for O(1) extra space. Use the cycle length above and emit row by row directly, being careful that the top and bottom rows take one character per cycle and middle rows take two.
- **Spiral or diagonal traversal of a matrix.** Same move: do not build the picture; find the rule that says where the next element goes and keep only the state that rule needs (here a row and a direction; in a spiral, four boundaries).

## What to carry forward

When a problem draws a picture, ask which coordinate the answer actually reads; often one coordinate vanishes and the grid collapses into buckets keyed by the other. The next problem also buckets strings, but the bucket key is no longer a row number handed to us; we have to invent a key that two "equivalent" strings share.
