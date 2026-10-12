# Word Squares
*LeetCode 425 · Hard · Pattern: Prefix trie + row-by-row backtracking · Reading time ~10 min*

## The problem

Given distinct words that all have length n, return every word square: n words (reuse allowed) such that the k-th row
and the k-th column read the same word.

```text
Example: ["area","lead","wall","lady","ball"] returns
  [["ball","area","lead","lady"],
  ["wall","area","lead","lady"]].
```

## What the problem is really asking

You get a list of distinct words, all of the same length n. Build every n × n grid, one word per row, such that reading column k top to bottom gives the same word as row k. Words may be used more than once. Return all such squares.

The answer is a list of squares (lists of n words). The defining property is symmetry: the grid equals its own transpose, `square[r][c] == square[c][r]` for every r, c. What makes it hard: the number of ordered choices is W^n, and you need a way to reject bad partial squares long before they are full.

```text
 words: area, lead, wall, lady, ball

   b a l l        row 0 = col 0 = "ball"
   a r e a        row 1 = col 1 = "area"
   l e a d        row 2 = col 2 = "lead"
   l a d y        row 3 = col 3 = "lady"

 answer: [wall,area,lead,lady], [ball,area,lead,lady]
```

## Do it by hand first

Pick `ball` for row 0. Because column 0 must also read `ball`, the rows below must start with `a`, `l`, `l` in order. So row 1 must start with `a`.

```text
 after row 0         after row 1          after row 2
 b a l l             b a l l              b a l l
 a . . .             a r e a              a r e a
 l . . .             l e . .              l e a d
 l . . .             l a . .              l a d .
 row1 starts "a"     row2 starts "le"     row3 starts "lad"
```

Pick `area` for row 1 (the only word starting with `a`). Now columns 0 and 1 are fixed in their top two cells, and row 2 must start with `l` (from `ball`) then `e` (from `area`): prefix `le`. Only `lead` fits. Then row 3 must start with `l`,`a`,`d`: `lady`. Done.

Your hand kept track of one thing: **the required prefix of the next row**, which is column k of the rows already written. Then you asked "which words start with this prefix?". That question, asked over and over, is what a trie is for.

## The first honest attempt

Generate every ordered n-tuple of words (repetition allowed) and keep those whose grid is symmetric. That is O(W^n · n²).

The waste is that symmetry is checked only at the end. Most tuples are dead after row 1:

```text
 tuple (area, lead, ....)
   a r e a
   l e a d     col 0 says row 1 must start with 'r';
   ? ? ? ?     it starts with 'l' -> already dead,
   ? ? ? ?     yet W^2 completions of rows 2,3 are tried
```

A smarter brute force backtracks row by row and checks the prefix, but still filters all W words at every step with `startswith`: O(W · n) per step, re-reading the same prefixes against the same words at every node of the search.

## The turning point

**Claim: after placing rows 0..k−1, row k must begin with the string `square[0][k] + square[1][k] + ... + square[k−1][k]`, and any word with that prefix keeps the square consistent so far.**

Justify it. Symmetry says `square[k][j] == square[j][k]`. For j < k, the right-hand side is already written (row j, column k). So the first k letters of row k are forced: they are column k read down through the rows so far. The letters from position k on are unconstrained by anything placed yet. So the legal choices for row k are exactly the words with that prefix — no more, no fewer.

This turns the problem into backtracking with a strong filter: at depth k, compute the prefix, try only words with it, recurse. Any partial square with a prefix no word has dies immediately.

The remaining cost is the question "which words start with this prefix?". A plain trie answers "does any word?", but listing them requires walking the subtree. So augment the trie: **at every node, store the indices of all words that pass through it.** Then the query is a walk of length k plus reading a list.

```text
 trie with index lists (indices: 0 area,1 lead,
                        2 wall,3 lady,4 ball)
 root  $:[0,1,2,3,4]
  a    $:[0]        -> r -> e -> a
  l    $:[1,3]
    le $:[1]        -> lead
    la $:[3]        -> lad -> lady
  w    $:[2]
  b    $:[4]
```

Is storing a list at every node wasteful? Each word appears in exactly n lists (one per letter on its path), so the total payload is W · n integers — the same order as the trie itself. Compare that with what it saves: without the lists, every candidate query would walk the entire subtree below the prefix node to collect the words hanging there, and that subtree can be most of the trie when the prefix is short. Storing indices rather than strings keeps each entry one small integer and lets the search read the word back from the original list.

The root holds every index, because row 0 has the empty prefix and any word may start a square. The invariant during the search: *the first k rows and the first k columns already agree*, so nothing placed ever needs repair later, and any square reaching depth n is valid.

## Watch it work

These frames come from instrumenting the solution on the example. Candidates are tried in index order: area, lead, wall, lady, ball.

**Frame 1** — depth 0, prefix `""`: candidates are all five words. Try `area` first.

```text
 square: [area]          next prefix = col 1 of rows
 a r e a                 = "r"
 trie walk "r": no edge -> no candidates, backtrack
```

**Frame 2** — try `lead` as row 0: prefix `e`, no word starts with `e`. Dead at once. Try `wall`: prefix is `a`, candidates `[area]`.

```text
 square: [wall]
 w a l l       prefix "a" -> node a, $:[0] -> area
 a . . .
```

**Frame 3** — `[wall, area]`: prefix for row 2 = `l` (wall[2]) + `e` (area[2]) = `le`. Candidates `[lead]`.

```text
 w a l l
 a r e a       column 2 so far: l, e
 l e . .       prefix "le" -> [lead]
```

**Frame 4** — `[wall, area, lead]`: prefix = `l`+`a`+`d` = `lad`, candidates `[lady]`. Place it: depth 4 = n, record the square.

```text
 w a l l
 a r e a
 l e a d       prefix "lad" -> [lady]
 l a d y       FOUND [wall,area,lead,lady]
```

**Frame 5** — back to depth 0, try `lady`: prefix `a` -> `area`; then prefix `d`+`e` = `de`: no edge. Dead.

```text
 l a d y
 a r e a       prefix "de": trie has no "d" child
 d e . .       -> backtrack
```

**Frame 6** — try `ball`: same chain as `wall` (prefixes `a`, `le`, `lad`) and records `[ball, area, lead, lady]`.

```text
 b a l l
 a r e a
 l e a d
 l a d y       FOUND [ball,area,lead,lady]
```

Across frames, the next prefix was always read from the column, the trie returned exactly the words with that prefix, and every partial square was symmetric in its filled corner. Dead ends cost one short walk.

## Why it is correct

**Invariant at depth k:** the k rows placed satisfy `square[r][c] == square[c][r]` for all r, c < k, and for every row r < k and column c ≥ k, the letter `square[r][c]` will be matched by the first letters of row c when it is placed.

**Soundness.** Each new row k is chosen with prefix equal to column k of earlier rows, so `square[k][j] == square[j][k]` for all j < k. Combined with the invariant, the first k+1 rows are symmetric in their (k+1) × (k+1) corner, and the later columns' constraints are deferred to the rows that will satisfy them. At depth n, every pair (r, c) has been checked once, from whichever of r or c was placed later. So every recorded square is valid.

**Completeness.** Take any valid square. Its row 0 is among the root's candidates. Inductively, if its first k rows are on the current search path, its row k has the required prefix (by symmetry), so it is among the candidates the trie returns, and the search tries it. So every valid square is reached.

The trie returns exactly the words with a prefix because each insert appended the word's index to every node on its path — the payload invariant.

## Cost

- **Build:** O(W · n) time and space — each word contributes n index entries along its path.
- **Search:** O(W · n · 26^(n−1)) worst case — n−1 rows below the first, each choosing among words sharing a prefix (at most 26 branches per level of a dense trie), with an O(n) prefix walk per step. In practice pruning collapses this drastically.
- **Space:** O(W · n) for the trie plus O(n) for the current square and recursion.

Without the trie, each step filters all W words, adding a factor W per node of the search tree.

## Variations you will meet

- **Words may not be reused.** Keep a used set; skip indices already in the square. The prefix logic is unchanged.
- **Hash map of prefixes instead of a trie.** Precompute `prefix -> [words]` for every prefix of every word (O(W · n²) memory). Same O(1)-ish lookup, simpler code, more memory; a fine interview answer if you name the trade-off.
- **Non-square or non-symmetric crosswords.** Rows and columns come from different word lists; you need two tries and must check both directions at each cell, so placement goes cell by cell rather than row by row.
- **N-Queens.** Same skeleton: place row by row, let earlier rows dictate constraints on the next, prune immediately.

## What to carry forward

When backtracking needs "all words with this prefix" at every step, store the answer at each trie node, so the query is a walk plus a read. The next problem stores a payload at every node too — the best index — but first rewrites a two-sided prefix-and-suffix question into a single prefix walk.
