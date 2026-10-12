# Sudoku Solver
*LeetCode 37 · Hard · Pattern: Constraint backtracking with bitmasks (most-constrained cell first) · Reading time ~11 min*

## The problem

Fill a partially filled 9x9 board (digits '1'-'9', '.' for empty) in place so that every row, every column and every
3x3 box contains each digit exactly once. The input has exactly one solution.

```text
Example: the classic board whose first row is "53..7...." is
  completed so that row becomes "534678912".
```

## What the problem is really asking

Fill the empty cells of a 9 x 9 grid with digits 1 to 9 so that every row, every column and
every 3 x 3 box contains each digit exactly once. You modify the board in place. The puzzle
is guaranteed to have exactly one solution.

The answer is the completed board. Here is the puzzle we will follow in this chapter. It has
27 givens and 54 empty cells, which is a hard puzzle by newspaper standards:

```text
       c0 c1 c2   c3 c4 c5   c6 c7 c8
  r0   .  .  9  | 7  4  8  | .  .  .
  r1   7  .  .  | .  .  .  | .  .  .
  r2   .  2  .  | 1  .  9  | .  .  .
       ---------+----------+---------
  r3   .  .  7  | .  .  .  | 2  4  .
  r4   .  6  4  | .  1  .  | 5  9  .
  r5   .  9  8  | .  .  .  | 3  .  .
       ---------+----------+---------
  r6   .  .  .  | 8  .  3  | .  2  .
  r7   .  .  .  | .  .  .  | .  .  6
  r8   .  .  .  | 2  7  5  | 9  .  .

  box index b = (r // 3) * 3 + c // 3     boxes 0..8
```

What makes it hard: each cell is a variable with nine possible values, every value choice
constrains twenty other cells (eight in its row, eight in its column, four more in its box),
and the constraints chain. With 54 empties the raw space is `9^54`. There is no formula;
backtracking is the general tool. The whole game is pruning: noticing a contradiction as
early as possible and branching where the fewest choices remain.

## Do it by hand first

A human never starts at the top-left and guesses. You scan for a cell where only one digit
fits. Look at (3,5), the centre box's right column. Row 3 already has 2, 4, 7. Column 5 has
8, 9, 3, 5. The centre box has 1. Together that rules out 1, 2, 3, 4, 5, 7, 8, 9. Only 6 is
left, so you write 6, and that new 6 makes some neighbouring cells easier.

```text
  cell (3,5): what is already used around it

  row 3    : 2 4 7
  column 5 : 3 5 8 9
  box 4    : 1
  union    : 1 2 3 4 5 7 8 9     -> only 6 fits
```

You kept, in your head, three small lists per cell: **digits used in my row, my column, my
box**. And you picked **the cell with the fewest options** first. Those two habits are the
two optimisations of this problem.

## The first honest attempt

The textbook backtracker: find the first empty cell in reading order, try digits 1 to 9,
and for each digit walk the row, column and box (27 reads) to see if it is legal. Place it,
recurse, and on failure erase and try the next digit. If no digit works, return False.

It solves our puzzle, but it makes **13,528 placements** to do so. Two separate kinds of
waste:

```text
  waste 1: rediscovering used digits
    try 1 at (0,0): read 27 cells   x
    try 2 at (0,0): read the same 27 cells again
    ... every node re-reads what never changed

  waste 2: branching in the wrong place
    first empty in reading order = (0,0): 4 candidates
    meanwhile (3,5) had exactly 1 candidate
       (0,0)
      / |  \  \        a wrong guess here is explored
     1  3   5  6       for many levels before some other
     x  x  OK  .       cell finally runs out of digits
```

The first waste is a constant factor per node. The second is exponential: a wrong guess at
a loosely constrained cell is only discovered many levels deeper, after a whole subtree has
been built on top of it.

## The turning point

There are two claims, one per waste.

**Claim 1: "is digit d used in row r?" is set membership, so keep one 9-bit mask per row,
per column and per box; a cell's legal digits are the complement of the OR of its three
masks, an O(1) computation.**

Bit `d` of `rows[r]` is 1 when digit `d` is already in row `r`; same for `cols[c]` and
`boxes[b]`. Then:

```python
used = rows[r] | cols[c] | boxes[b]
cand = ~used & 0x3FE          # bits 1..9 that are still free
place:  rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
undo:   rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
```

`0x3FE` is binary `11 1111 1110`: bits 1 through 9, leaving bit 0 unused so digit `d` maps
to bit `d`. Placing is three ORs; undoing is three XORs (the bit was 0 before, so XOR clears
exactly it). This is the N-Queens idea again, with nine "values" per line instead of one.
The invariant: the masks always equal the digits currently written on the board.

**Claim 2: always branch on the empty cell with the fewest candidates.** This is called
minimum remaining values, or "most constrained first". Two cases make it powerful:

- A cell with **0** candidates means the current partial board is already impossible. MRV
  picks it immediately (0 is the minimum), the loop over its candidates does nothing, and
  the branch dies at once instead of after more guesses elsewhere.
- A cell with **1** candidate is a forced move: the search tree has one child, no guessing.
  Filling it can create more single-candidate cells, and the chain continues.

Only when every remaining cell has two or more options does the search genuinely guess, and
then it guesses where the guess is most likely right (one of two, not one of six) and where
a wrong guess is refuted soonest.

Why must MRV still be complete? Because every empty cell must eventually get some digit.
Whichever cell we choose, trying all its candidates covers every possible solution; the
order of cells changes the shape of the tree, not the set of leaves. So we are free to pick
the cell that makes the tree narrowest.

The full loop: keep a list of empty cells. In `dfs()`, if the list is empty the board is
solved. Otherwise scan it for the cell with the fewest candidate bits, remove it, and for
each candidate bit place it (board and three masks), recurse, and return True on success;
otherwise undo the masks and try the next bit. If none works, write `.` back, put the cell
back in the list, and return False.

## Watch it work

The puzzle above. Depth means the number of placements on the current path.

```text
Frame 1   scan once: build 27 masks, list 54 empties
  candidate counts over the 54 empty cells:
    1 cand: 3   2: 10   3: 14   4: 15
    5 cand: 9   6:  1   7:  2
```
Three cells are already forced; nothing requires a guess yet.

```text
Frame 2   MRV picks (3,5); masks as bits, digits 9..1
             9 8 7 6 5 4 3 2 1
  rows[3]    0 0 1 0 0 1 0 1 0     {2,4,7}
  cols[5]    1 1 0 0 1 0 1 0 0     {3,5,8,9}
  boxes[4]   0 0 0 0 0 0 0 0 1     {1}
  OR         1 1 1 0 1 1 1 1 1
  candidates 0 0 0 1 0 0 0 0 0     -> place 6 (depth 1)
```
The legality test that cost 27 reads is now three ORs and a NOT.

```text
Frame 3   depths 1..20: every MRV pick has 1 candidate
  (3,5)=6  (1,5)=2  (4,3)=3  (4,0)=2  (4,5)=7
  (4,8)=8  (3,8)=1  (5,5)=4  (5,3)=5  (1,3)=6 ...
  20 forced placements, zero branching
```
Each forced digit lowers its neighbours' counts until no single-candidate cell remains.

```text
Frame 4   depth 20: minimum count is 2 -> first guess
  (0,6) candidates {1,6}: try 1
     then depth 21: (0,1) candidates {3,5}: try 3
         (0,6)
         /   \
        1     6
       / \
      3   5
```
The search guesses only where two options remain, and only after exhausting forced moves.

```text
Frame 5   (0,6)=1, (0,1)=3: forced chain to depth 27
  MRV finds (1,2) with 0 candidates   x
  undo to (0,1), try 5: forced chain to depth 37
  MRV finds (2,4) with 0 candidates   x
  (0,1) exhausted -> undo to (0,6)
```
Both children of the guess `1` die on a zero-candidate cell; MRV spots each contradiction at
the first level where it exists.

```text
Frame 6   (0,6)=6; depth 21 picks (0,0) with {3,5}
  try 3: forced chain, (7,7) has 0 candidates  x
  try 5: forced chain to depth 54, empties = [] OK
         (0,6)
         /   \
        1x    6
             / \
            3x  5  -> solved
```
The surviving branch fills every cell; `dfs` returns True all the way up and the board is
left filled.

```text
Frame 7   totals for this puzzle
               placements   2-way nodes   dead ends
  MRV+masks         88            3            3
  first-empty   13,528
```
88 placements, of which 82 were forced; the brute force made 153 times as many.

Across all frames the masks matched the board exactly, because every place was a triple OR
and every undo the matching triple XOR. The search only branched three times; everything
else was a chain of forced moves.

## Why it is correct

**Invariant.** At every call of `dfs()`, the masks are exactly the digits on the board, the
empty list is exactly the `.` cells, and the board breaks no rule.

**Preservation.** A digit is placed only if its bit is in `cand`, i.e. not in the row,
column or box masks, so no rule is broken; the three ORs keep the masks exact. On failure
the three XORs remove exactly that bit, the cell is reset to `.`, and it is reinserted at
the same list position, so the caller sees the state it left.

**Soundness.** `dfs()` returns True only when no empty cells remain, and by the invariant
the full board breaks no rule, so it is a valid solution.

**Completeness.** Any solution assigns some digit to the chosen cell; that digit is legal
with respect to the current board, so it is among the candidates and gets tried. Choosing
the cell by MRV only reorders the levels, so the solution's branch is always reachable. A
cell with zero candidates correctly rejects the current branch: no digit can go there.

## Cost

- **Time `O(9^E)` worst case** for `E` empty cells, but MRV makes most levels single-child;
  this puzzle took 88 placements. Each node also pays `O(E)` to scan for the MRV cell.
- **Space `O(E)`**: 27 integers of masks, the empty list, and recursion depth `E`.
- The brute force has the same exponential bound with `O(27)` per legality test and a far
  bushier tree (13,528 placements here).

## Variations you will meet

- **Valid Sudoku (LeetCode 36).** No search: one pass, three arrays of sets (or masks), report
  a duplicate. It is exactly the "build the masks" step.
- **Constraint propagation.** Before guessing, repeatedly fill every single-candidate cell
  and also every digit that has only one possible cell in a unit ("hidden single"). Many
  puzzles then need no backtracking at all; the remaining search is tiny.
- **Exact cover / Dancing Links.** Sudoku is an exact cover problem: 324 constraints, each
  satisfied exactly once. Knuth's Algorithm X with MRV on constraints is the same idea at
  full generality.
- **Generic CSPs (graph colouring, scheduling).** Same three ingredients: incremental
  constraint state, most-constrained variable first, undo on failure.

## What to carry forward

Keep constraint state incrementally (OR to place, XOR to undo) and branch on the most
constrained variable, so contradictions surface at the first level where they exist. Next,
Remove Invalid Parentheses moves from boards back to strings, and adds a different kind of
pruning: computing, before any search, exactly how much you are allowed to change.
