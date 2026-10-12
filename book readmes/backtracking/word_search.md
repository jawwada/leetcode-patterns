# Word Search
*LeetCode 79 · Medium · Pattern: Grid DFS backtracking with in-place visited marking · Reading time ~9 min*

## The problem

Given an m x n grid of letters and a word, return True if the word can be traced through horizontally or vertically
adjacent cells, using each cell at most once.

```text
Example: board=[[A,B,C,E],[S,F,C,S],[A,D,E,E]], word="ABCCED" ->
  True; word="ABCB" -> False because the B would be reused.
```

## What the problem is really asking

You get a rectangle of letters and a word. Put your finger on one cell, then slide it up, down,
left or right, one cell per letter, and never land on a cell you already used. Can your finger
spell the word? The answer is a single yes or no.

The object we are looking for is a **path**: a list of cells where each cell touches the
previous one along an edge, no cell appears twice, and the letters read off in order equal the
word.

```text
        c0  c1  c2  c3
  r0  [ A   B   C   E ]       word = "ABCE"
  r1  [ S   C   D   F ]

  one valid path:  (0,0) -> (0,1) -> (0,2) -> (0,3)
                     A        B        C        E
```

Two things make it harder than a flood fill. Paths branch: up to four moves per cell, so
the number of paths grows like 4 to the power of the word length. And the "never reuse a
cell" rule makes the legal moves depend on the **whole path so far**: a cell forbidden on
one path is fine on another. So the visited set belongs to one path and must be undone when
that path is abandoned. That is exactly what backtracking is for.

## Do it by hand first

Look for "ABCE" in the board above. Your eye first hunts for an `A`. There is one, at (0,0).
Next you glance at its neighbours for a `B`: below it is `S` (no), above is off the board,
to the right is `B` (yes). Now you need a `C` next to that `B`. There are two: one below at
(1,1) and one to the right at (0,2).

Try the one below first. You need an `E` next to (1,1): its neighbours are the used `B`,
`D`, `S`, and nothing below. Dead end. Lift your finger off (1,1), go back to the `B`, and
try the other `C`. Next to (0,2) sits an `E`. Done.

```text
  finger path, with the cells it covers shaded as #

  try 1:  [ # # C E ]     stuck on (1,1): no E next to it
          [ S # D F ]

  undo (1,1), try the other C

  try 2:  [ # # # # ]     spelled A B C E
          [ S C D F ]
```

What did your hand keep track of? Three things: **where you are**, **how many letters you
have matched so far** (call it `k`), and **which cells your finger has covered on this
attempt**. The third one is the seed of the algorithm. It grows by one cell when you advance
and shrinks by one cell when you back off. It behaves like a stack, and the recursion stack
of a depth-first search is exactly that.

## The first honest attempt

The brute force a strong candidate says out loud: from every cell, enumerate every
self-avoiding path of exactly `L = len(word)` cells, spell out its letters, and compare the
string to the word at the end.

Look at what it builds from (0,0):

```text
  every length-4 path from A(0,0), built in full,
  compared only at the end:

    A S C B      wrong at letter 2 -- built 2 more cells
    A S C D      wrong at letter 2 -- built 2 more cells
    A B C S      wrong at letter 4
    A B C D      wrong at letter 4   (C at (1,1))
    A B C D      wrong at letter 4   (C at (0,2))
    A B C E      match

  and from the 7 other start cells (S, B, C, ...):
  every path is wrong at letter 1, yet all are built
```

The cost is `O(m * n * 4^L * L)`: up to `4^L` paths per start, `L` work to spell each. The
repeated work is plain in the drawing: the path `A S ...` is already lost the moment `S` is
compared with `B`, yet it is extended twice more. Paths starting on `S`, `C`, `D`... are lost
at the very first letter and still extended `L - 1` steps. The comparison happens at the
leaf, so the whole dead subtree is paid for.

## The turning point

**Claim: if the first `k` letters of a path do not equal `word[:k]`, no extension of that
path can ever spell the word, so check each cell against `word[k]` the moment you step on
it, and turn back on a mismatch.**

Why it holds: extending a path only appends letters; a wrong prefix stays wrong forever.
This is the idea that separates backtracking from brute-force enumeration: test the
constraint **at the node**, not at the leaf. The tree is the same, but a branch stops the
moment it has a wrong letter, and on a real board that removes almost all of it.

Now the visited set. We need "cells on the current path" with cheap add, remove and lookup.
A separate `m x n` boolean matrix works. The neat trick is to use the board itself:
overwrite the cell with a sentinel such as `#` when you step on it, and write the letter
back when you step off.

```python
saved, board[r][c] = board[r][c], "#"    # step on
found = any(dfs(nr, nc, k + 1) for nr, nc in neighbours)
board[r][c] = saved                      # step off
```

The beauty is that `#` never equals a letter of the word, so the very same test that prunes
a wrong letter, `board[r][c] != word[k]`, also prunes a reused cell. One comparison does two
jobs. Off-board positions are the only other reason to stop, and they are checked first so
we never index outside the grid (Python's negative indices would silently wrap around).

So `dfs(r, c, k)` asks: "can `word[k:]` be spelled from (r, c), given the marked cells?"
True when `k == len(word)`, False on off-board or mismatch, otherwise mark, try the four
neighbours with `k + 1`, unmark, report. The outer loop calls it from every cell. The `or`
chain stops at the first success, and the unmark line still runs after it.

## Watch it work

Board and word as above. The solution tries neighbours in the order down, up, right, left.
`#` marks cells on the current path; `x` marks a pruned branch.

```text
Frame 1   dfs(0,0,k=0): A == word[0], mark it
  [ # B C E ]      tried:  down (1,0) S != B   x
  [ S C D F ]              up   off board      x
  path: A                  next: right (0,1)
```
The first cell matches, so it is marked; two of its four branches die on the first check.

```text
Frame 2   dfs(0,1,k=1): B == word[1], mark it
  [ # # C E ]      tree:   A
  [ S C D F ]             / \
  path: A B              S x  B   <- here
```
The second letter matches; the path is now two cells long and the next letter needed is `C`.

```text
Frame 3   dfs(1,1,k=2): C == word[2], mark it; need E
  [ # # C E ]      tried from (1,1):
  [ S # D F ]        down  off board   x
  path: A B C        up    (0,1) is #  x   <- reuse blocked
                     right D != E      x
                     left  S != E      x
```
Every neighbour fails, so `dfs(1,1,2)` restores the `C` at (1,1) and returns False.

```text
Frame 4   back at B: up is off board x; try right
  [ # # # E ]      tree:       A
  [ S C D F ]                 / \
  path: A B C                x   B
                                / \
                        C(1,1) x   C(0,2)  <- here
```
The dead `C` has been un-marked; the second `C` matches and is marked in its place.

```text
Frame 5   dfs(0,2,k=2) needs E: down D x, up off x,
          right (0,3) == E -> dfs(0,3,k=3) marks it,
          its first child is called with k = 4 = len
  [ # # # # ]      k == len(word)  -> True
  [ S C D F ]      unwinding restores A B C E
```
The True travels back up the `or` chains; each frame restores its letter on the way out, so
the caller gets the board back untouched.

Across all frames the `#` cells were exactly the current path, `k` equalled their count,
and every call restored what it marked before returning.

## Why it is correct

The invariant: when `dfs(r, c, k)` is called, the marked cells are exactly a valid path that
spells `word[:k]` and ends next to (r, c). Marking (r, c) after a successful letter check
extends that path by one valid cell, so the invariant holds for the children with `k + 1`.
Unmarking on return restores the parent's view, so sibling branches see the right set.

Soundness: True is returned only when `k == len(word)`, which by the invariant means the
marked cells spell the whole word along a valid path.

Completeness: take any valid path. Starting from its first cell the outer loop calls `dfs`.
At each step the next cell of that path is in bounds, has the right letter, and is not on
the current path (paths do not repeat cells), so it passes every check and is tried.
Pruning only removes branches that fail a necessary condition, so the valid path is never
cut, and the search finds it (or another one first).

## Cost

- **Time `O(m * n * 3^L)`.** Up to `m * n` starts; the first step has 4 directions and every
  later step at most 3, since the cell you came from is marked.
- **Space `O(L)`.** Recursion depth is at most `L`; the board doubles as the visited set.
- The brute force was `O(m * n * 4^L * L)`.

## Variations you will meet

- **Word Search II (LeetCode 212): many words at once.** Running this per word is too slow.
  Put all words in a trie and walk the trie in lockstep with the grid; the pruning test
  becomes "is the current path a prefix of any word", and you remove trie leaves once found.
- **Count occurrences instead of yes/no.** Drop the short-circuit and add up the results of
  the four children; the marking discipline stays the same.
- **You may not mutate the input.** Keep a `visited` set or a bitmask of cells; add before
  recursing, remove after. The invariant is unchanged; only the storage moves.
- **Cheap pre-checks.** If the board lacks enough copies of some letter, answer False at
  once; if the last letter is rarer than the first, search for the reversed word.

## What to carry forward

Mark on the way in, unmark on the way out, and test the constraint at the node rather than at
the leaf. The next problem, Unique Paths III, keeps this exact grid snake but must cover
every empty cell, so instead of a word to match it carries a count of cells still owed.
