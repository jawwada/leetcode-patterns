# N-Queens (LeetCode 51)

**Area:** backtracking · **Difficulty:** Medium-Hard · **Key operations:** one queen per row, attacked = column / diagonal r - c / anti-diagonal r + c sets, add / recurse / remove

## Problem

Place n queens on an n × n board so that no two share a row, column or diagonal. Return every distinct board as a list of strings (`'Q'` queen, `'.'` empty), sorted.

## Example

```
n = 4 ->  . . Q .      . Q . .
          Q . . .      . . . Q
          . . . Q      Q . . .
          . Q . .      . . Q .

[["..Q.", "Q...", "...Q", ".Q.."], [".Q..", "...Q", "Q...", "..Q."]]
```

`n = 1` gives `[["Q"]]`; `n = 2` and `n = 3` have no solution.

## Brute force

One queen per row is forced, and one per column too, so every candidate board is a permutation of the columns `0..n-1`. Try all n! permutations and keep those where no pair of queens shares a diagonal: `abs(col[i] - col[j]) != j - i` for every pair.

O(n! · n²) time, O(n) space beyond the output. The waste: a permutation whose first two queens already attack each other diagonally is still completed in every possible way and each completion is checked pairwise. All (n - 2)! completions of a doomed prefix are generated and all rejected.

## From brute force to optimal

Detect the conflict the moment it is created instead of at the leaf. Placing queens row by row, a new queen at `(r, c)` attacks an earlier one iff they share column `c`, the `\` diagonal (constant `r - c`) or the `/` anti-diagonal (constant `r + c`). Three hash sets answer that in O(1), so a row only tries the columns not under attack and a conflicting prefix is never extended. The surviving leaves at depth n are exactly the solutions. Permutations already pruned the columns; the sets add the diagonals and move the check from the leaf up to the node.

## Intuition

Fill the board one row at a time. Each placed queen shades its column and its two diagonals on all the rows below; the candidate squares of the next row are the unshaded ones. When a row has no unshaded square, the branch is dead: lift the last queen (un-shade her lines) and try her next column. The three sets are just a compact way to store the shading: a square `(r, c)` is shaded iff `c`, `r - c` or `r + c` is in its set. Every queen you place adds one key to each set, every queen you lift removes the same three keys.

## Walkthrough

`n = 4`. Indentation is the row being filled. After each placement the three sets are shown; each "attacked" square names the set that rejected it (`col` = same column, `diag` = same `r - c`, `anti` = same `r + c`).

```
row 0: place (0,0)                  cols {0}      diag {0}        anti {0}       Q...
  row 1: col 0 col, col 1 diag (1-1 = 0), col 2 free
         place (1,2)                cols {0,2}    diag {0,-1}     anti {0,3}     Q... / ..Q.
    row 2: col 0 col, col 1 anti (2+1 = 3), col 2 col, col 3 diag (2-3 = -1)  -> dead
         lift (1,2); col 3 free
         place (1,3)                cols {0,3}    diag {0,-2}     anti {0,4}     Q... / ...Q
    row 2: col 0 col, col 1 free
           place (2,1)              cols {0,1,3}  diag {0,-2,1}   anti {0,4,3}   Q... / ...Q / .Q..
      row 3: col 0 col, col 1 col, col 2 diag (3-2 = 1), col 3 col             -> dead
           lift (2,1); col 2 anti (2+2 = 4), col 3 col                          -> dead
         lift (1,3)
  lift (0,0)
row 0: place (0,1)                  cols {1}      diag {-1}       anti {1}       .Q..
  row 1: col 0 anti (1+0 = 1), col 1 col, col 2 diag (1-2 = -1), col 3 free
         place (1,3)                cols {1,3}    diag {-1,-2}    anti {1,4}     .Q.. / ...Q
    row 2: col 0 free
           place (2,0)              cols {0,1,3}  diag {-1,-2,2}  anti {1,4,2}   .Q.. / ...Q / Q...
      row 3: col 0 col, col 1 col, col 2 free
             place (3,2)            all 4 rows placed -> SOLUTION   .Q.. / ...Q / Q... / ..Q.
             lift (3,2); col 3 col
           lift (2,0); col 1 col, col 2 anti (2+2 = 4), col 3 col               -> dead
         lift (1,3)
  lift (0,1)
row 0: place (0,2) ... the mirror image of column 1 -> SOLUTION   ..Q. / Q... / ...Q / .Q..
row 0: place (0,3) ... the mirror image of column 0 -> no solution
result sorted: [[..Q., Q..., ...Q, .Q..], [.Q.., ...Q, Q..., ..Q.]]
```

Lifting a queen removes exactly the three keys she added, so after each `lift` the sets are back to what they were before the `place`.

## Steps

1. `cols`, `diag` (keys `r - c`), `anti` (keys `r + c`) = empty sets; `queens = []` (column chosen per row).
2. `dfs(r)`: if `r == n`, render the board from `queens` and record it.
3. For `c` in `range(n)`: skip if `c in cols or r - c in diag or r + c in anti`.
4. Add the three keys, append `c`, call `dfs(r + 1)`, pop `c`, remove the three keys.
5. Call `dfs(0)`; return `sorted(result)`.

## Complexity

O(n!) nodes in the worst case (an upper bound on the surviving tree; the real count is far smaller), with O(1) work per node thanks to the sets. O(n) extra space for the sets, the queens list and the recursion, beyond the output.

## Pitfalls

- **Using `r + c` for both diagonals.** The `\` diagonal is constant `r - c`, the `/` one is constant `r + c`. With the same key for both, `\` attacks go unnoticed and invalid boards are returned.
- **Not removing from all three sets on backtrack.** A lifted queen that keeps guarding one of her lines prunes later branches wrongly; `n = 4` loses solutions.
- **Recording at `r == n - 1`.** Boards with `n - 1` queens get recorded; the base case is `r == n`.
- **Rendering rows and columns swapped.** `queens[r]` is the column of the queen in row `r`; the board row `r` is `'.' * c + 'Q' + '.' * (n - c - 1)`.
- **Sorted order.** `'.'` sorts before `'Q'`, so for `n = 4` the board starting `..Q.` comes before the one starting `.Q..`.
