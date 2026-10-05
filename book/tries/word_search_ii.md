# Word Search II
*LeetCode 212 · Hard · Pattern: Trie-guided grid backtracking · Reading time ~10 min*

## The problem

Given an m x n board of letters and a list of words, return every word that can be spelled by a path of horizontally
or vertically adjacent cells without reusing a cell.

```text
Example: board [[o,a,a,n],[e,t,a,e],[i,h,k,r],[i,f,l,v]], words
  [oath,pea,eat,rain] -> [eat, oath].
```

## What the problem is really asking

You have an m × n board of letters and a list of words. A word is "on the board" if you can spell it by starting on some cell and repeatedly stepping up, down, left or right, never stepping on the same cell twice within one word. Return every listed word that is on the board.

The answer is a set of words. The single-word version (Word Search I) is a backtracking DFS from every cell. What makes this version hard is that the word list can hold tens of thousands of words, and running the single-word search once per word multiplies an already exponential search by the dictionary size.

Our running example:

```text
 board            words: oat, oath, eta, the
     c0 c1 c2
 r0   o  a  t     oath: o(0,0) a(0,1) t(1,1) h(1,2)
 r1   e  t  h      (or via t(0,2): two paths, one word)
                  answer: oat, oath, eta   ("the" is not there)
```

## Do it by hand first

Try to find words by eye. You put a finger on `o` and start tracing. From `o` you can go right to `a` or down to `e`. You go to `a` because `oat` and `oath` both continue with `a`, and no word starts with `oe`. From `a` you go down to `t` — `oat` complete. From that `t` you go right to `h` — `oath` complete.

```text
  o -> a          finger path: o a t h
       |          spelled so far, after each step:
       t -> h       "o"  "oa"  "oat"*  "oath"*
```

The decisive thing your finger did was refuse to step onto `e` from `o`. You knew no word starts with `oe`. Then, on the `oat` path, you checked both `oat` and `oath` with one trace, not two. You were tracking *the letters spelled so far* and *which words still begin with them*. That is a node in a trie of the words, moving in lockstep with your finger.

## The first honest attempt

For each word, run Word Search I: try every cell as a start, DFS while the next letter matches, backtrack on dead ends.

Cost: O(W · m · n · 4 · 3^(L−1)) — W words, each starting a branching search from every cell. The repeated work is glaring once two words share a prefix:

```text
 searching "oat":   o(0,0) -> a(0,1) -> t(1,1)  found
 searching "oath":  o(0,0) -> a(0,1) -> t(1,1) -> h(1,2)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^
                    the same three steps, walked again
 searching "eta":   tries o(0,0), a(0,1), t(0,2), ...
                    as starts even though none is 'e'
```

With a thousand words starting `oa`, the board path `o → a` is rediscovered a thousand times. And every cell is tried as a start for every word, even when no word begins with that cell's letter.

## The turning point

**Claim: explore each board path once and test it against all words at the same time, by walking a trie of the words in lockstep with the path.**

Justify it: whether a board path can be extended usefully depends only on the string it spells, and "does any word start with this string?" is exactly what a trie node answers. So run one DFS per start cell, carry the current trie node along, and step onto a neighbour only if its letter is a child of the current node. The moment the trie has no edge for a neighbour, that whole direction is pruned for every word at once. Reaching a node that stores a word means that word is on the board.

```text
 two structures move together

 board path          trie pointer
  o -> a -> t        root -o-> o -a-> oa -t-> oat*
                                                |h
                                               oath*
```

Turning the claim into a fast algorithm takes three refinements, each fixing a specific waste:

1. **Store the word itself at its terminal node** (`node["$"] = word`) instead of `True`. When the DFS reaches it, you have the word without rebuilding it from the path.
2. **Pop the word when found** (`node.pop("$")`). A word can be spelled by several paths; popping guarantees it is emitted once, and later paths stop treating that node as a goal.
3. **Prune emptied trie branches.** After a node's DFS returns, if the node has no children and no word left, delete it from its parent. Later start cells will then not even try that letter. The trie *shrinks* as words are found, so the search gets cheaper as it goes.

Visited cells are marked in place: overwrite the cell with `#` on entry and restore it on exit. `#` is never a trie key, so the "is the neighbour's letter a child?" check automatically refuses visited cells — one test does both jobs.

The invariant: *the current trie node is exactly the node for the letters on the current board path.* Every step extends both by the same letter.

## Watch it work

These frames come from instrumenting the solution on the example. Neighbours are tried in the order down, up, right, left. Found order: `oat`, `oath`, `eta`.

**Frame 1** — the trie, words stored at terminal nodes.

```text
 root
  o - a - t[oat] - h[oath]
  e - t - a[eta]
  t - h - e[the]
```

**Frame 2** — start (0,0) `o`. Down is `e`: not a child of node `o` (only `a`), skipped. Right is `a`: step. Then from (0,1) down to (1,1) `t`: node `oat` holds a word — pop it.

```text
  #  #  t      path: (0,0)->(0,1)->(1,1)
  e  #  h      trie at:  o>a>t   pop "oat"
               found: [oat]
```

**Frame 3** — from (1,1): down is off the board, up is `#`, right is (1,2) `h`, a child: step and pop `oath` (left, `e`, is not a child either). Node `oath` is now empty: delete it from its parent.

```text
  #  #  t      path: ...->(1,1)->(1,2)
  e  #  #      pop "oath"; h-node {} -> prune
               trie: o-a-t (t now empty)
               found: [oat, oath]
```

**Frame 4** — unwinding: `t` is empty, pruned; then `a`, then `o`. When the DFS of (0,1) later looks right at (0,2) `t`, the edge `t` under `a` is already gone, so the second path for `oath`, through (0,2), is never walked. The whole `o` branch disappears.

```text
 trie after unwinding the (0,0) start:
 root
  e - t - a[eta]
  t - h - e[the]
```

**Frame 5** — start (0,1) `a`: not a root child, skipped. Start (0,2) `t`: step to (1,2) `h` (node `th`), whose only child is `e`; no neighbour is `e`. Dead end; `th` is not empty, so nothing is pruned.

```text
  o  a  #      path: (0,2)->(1,2)
  e  t  #      node t>h, needs 'e': none
```

**Frame 6** — start (1,0) `e`: right to (1,1) `t`, up to (0,1) `a`: pop `eta`, then prune `a`, `t`, `e` on the way back.

```text
  o  #  t      path: (1,0)->(1,1)->(0,1)
  #  #  h      pop "eta"
               trie: root - t - h - e[the]
               found: [oat, oath, eta]
```

**Frame 7** — start (1,1) `t`: `h` at (1,2), still no `e` neighbour. Start (1,2) `h`: not a root child. Done.

Across every frame, the trie node equalled the path's spelling, visited cells held `#` and so could never match a trie key, and the trie only ever lost branches that could produce no further words.

## Why it is correct

**Soundness.** A word is emitted only when the DFS reaches its terminal node, and by the invariant that node's prefix equals the letters on the current path. The path is made of adjacent cells (we only step to neighbours) and never repeats a cell (visited cells hold `#`, which matches no trie edge). So every emitted word is truly on the board. Popping ensures no duplicates.

**Completeness.** Take any word w on the board via some path P. The DFS from P's first cell considers stepping along P: each next letter is a trie child as long as w's node has not been pruned, and pruning only removes nodes with no words left beneath them. If w's node was pruned, w was already emitted. Otherwise the DFS follows P to w's node and emits it. (If w was emitted earlier through another path, popping just means it is not emitted twice.)

Restoring the cell after the recursion is what makes the search a correct backtracking: each path explores with exactly its own cells marked.

## Cost

- **Time:** O(m · n · 4 · 3^(L−1)) worst case — each cell starts a DFS of depth at most L (the longest word), with 4 choices at the first step and at most 3 afterwards (you cannot step back onto the previous cell). This no longer has a factor W: all words share each walk. Pruning makes the practical cost far lower.
- **Space:** O(total word characters) for the trie, plus O(L) recursion depth.

Against the brute force, the trie removes the factor W and replaces "try each word from each cell" with "try each path once".

## Variations you will meet

- **Word Search I (one word).** No trie needed; the path just compares against one string. Understanding this one first is what makes the pruning above feel natural.
- **Return counts or paths, not words.** Store a counter or append the path at the terminal node instead of popping; you lose the "pop to stop" optimisation if you need all paths.
- **Diagonal moves or reuse allowed.** Change the neighbour list (8 directions) or drop the `#` marker; with reuse, add memoisation since paths are no longer simple.
- **Boggle scoring.** Same algorithm; payload at the terminal node becomes a score.

## What to carry forward

When many words are searched in the same space, build a trie and let it steer one shared search: each step must have a trie edge, and found words are removed so the trie shrinks. The next problem uses a trie inside a backtracking search too, but the search builds a square of words, and each trie node carries the list of words passing through it.
