# Word Search (LeetCode 79)

**Area:** backtracking · **Difficulty:** Medium · **Key operations:** DFS from every cell, match word[k] at depth k, mark the cell '#' while on the path, restore on return

## Problem

Given an m × n board of letters and a word, return `True` if the word can be traced through horizontally or vertically adjacent cells, using each cell at most once.

## Example

```
A B C E
S F C S          word = "ABCCED" -> True
A D E E          word = "ABCB"   -> False (the B would have to be reused)
```

`ABCCED` runs right along the top row, down the C column, then left along the bottom.

## Brute force

From every cell, enumerate every self-avoiding path of exactly `len(word)` cells (keep the visited cells in a set that is copied at each step), spell the letters along the path, and compare the whole string to the word at the leaf.

O(m · n · 4^L · L) time, O(L) space per path. The waste: a path whose first letter is already wrong is still extended for L - 1 more steps and its string is still built. Almost all of the 4^L paths are dead after one or two letters, but the comparison happens only at the end.

## From brute force to optimal

The path spells the word prefix by prefix, so compare the current cell against `word[k]` at step `k` and cut the branch the moment it mismatches. Nothing else changes: same DFS, same "each cell once" rule, but the live tree now contains only paths that match a prefix of the word, which on real boards is tiny.

The "each cell once" bookkeeping is also cheaper: instead of copying a visited set, overwrite the cell with a sentinel `'#'` before recursing and put the letter back after. The `'#'` never equals a letter of the word, so the mismatch check doubles as the visited check.

## Intuition

Walk the grid letter by letter, matching the word as you go. Each cell you stand on gets covered with a coin (`'#'`) so you cannot step on it again; when you turn back, you pick the coin up. The moment a neighbouring cell does not show the next letter you need, you do not go there. The coins on the board at any moment are exactly the path you are currently trying, drawn as a snake that extends on the way down and retracts on the way up.

## Walkthrough

`word = "ABCCED"`. Directions are tried in the order down, up, right, left. The board is drawn after each mark or restore; `#` is a cell on the current path.

```
start (0,0) 'A' = word[0]   mark      #BCE / SFCS / ADEE          path A
  down  (1,0) 'S' != 'B'               cut
  up    (-1,0) off grid                cut
  right (0,1) 'B' = word[1]   mark     ##CE / SFCS / ADEE          path AB
    down  (1,1) 'F' != 'C'             cut
    up    off grid                     cut
    right (0,2) 'C' = word[2] mark     ###E / SFCS / ADEE          path ABC
      down (1,2) 'C' = word[3] mark    ###E / SF#S / ADEE          path ABCC
        down (2,2) 'E' = word[4] mark  ###E / SF#S / AD#E          path ABCCE
          down  (3,2) off grid         cut
          up    (1,2) is '#'           cut   (visited, cannot reuse)
          right (2,3) 'E' != 'D'       cut
          left  (2,1) 'D' = word[5] mark  ###E / SF#S / A##E       path ABCCED
            k = 6 = len(word) -> True
          restore (2,1) 'D'            ###E / SF#S / AD#E
        restore (2,2) 'E'              ###E / SF#S / ADEE
      restore (1,2) 'C'                ###E / SFCS / ADEE
    restore (0,2) 'C'                  ##CE / SFCS / ADEE
  restore (0,1) 'B'                    #BCE / SFCS / ADEE
restore (0,0) 'A'                      ABCE / SFCS / ADEE          board intact, answer True
```

For `"ABCB"` the same walk reaches `ABC` at (0,2); its neighbours are (1,2) `C`, (0,3) `E` and (0,1) `#`, none a `B`, so the branch dies and every other start fails too.

## Steps

1. For each cell `(r, c)`, call `dfs(r, c, 0)`; return `True` as soon as one succeeds.
2. `dfs(r, c, k)`: if `k == len(word)`, return `True`.
3. If `(r, c)` is off the grid or `board[r][c] != word[k]`, return `False` (a `'#'` never matches, so visited cells are rejected here).
4. Save the letter, write `'#'`, try the four neighbours with `k + 1`.
5. Restore the letter; return whether any neighbour succeeded.

## Complexity

O(m · n · 3^L) time: 4 choices for the first step, at most 3 after that since you never step back onto the cell you came from. O(L) space for the recursion stack; no visited matrix.

## Pitfalls

- **Not marking the cell.** Without the `'#'` a cell can be reused, so `"ABCB"` is found by stepping back onto the B already in the path.
- **`>` instead of `>=` in the bounds check.** `r == rows` passes and `board[rows]` raises `IndexError`; `r == -1` would silently wrap to the last row. The last valid index is `rows - 1`.
- **Checking `k == len(word) - 1`.** The last letter is never compared, so any in-bounds neighbour completes the word.
- **Forgetting to restore.** Leaves `'#'` in the board and corrupts every later start; restore unconditionally, whether the branch succeeded or not.
- **Indexing before the bounds check.** `board[r][c] != word[k]` must come after the `r, c` range checks in the same `or` chain.
