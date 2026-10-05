# Word Ladder II
*LeetCode 126 · Hard · Pattern: Layered BFS + parents DAG, then backtrack paths · Reading time ~12 min*

## The problem

Given beginWord, endWord and a wordList, each transformation changes one letter and must land on a word in the list.
Return all shortest transformation sequences from beginWord to endWord (each including both ends), or [] if none
exists.

```text
Example: "hit" -> "cog" with
  ["hot","dot","dog","lot","log","cog"] gives
  [["hit","hot","dot","dog","cog"],
  ["hit","hot","lot","log","cog"]].
```

## What the problem is really asking

Same game as Word Ladder: change one letter at a time, every intermediate word must be in the
dictionary. But now you must return **every** shortest chain from `beginWord` to `endWord`,
each written out as a list of words. If there is none, return `[]`.

The answer is a set of paths, and that changes everything. Word Ladder needed one number per
word (its depth). Here a word can sit on many shortest chains, reached from several words in
the layer above, and we must keep all of those ways without keeping any longer chain.

We will use a dictionary chosen to show that, with every one-letter link drawn:

```text
  begin = red    end = tax
  dict  = ted tex red tax tad den rex pee

           red
          /   \
       ted     rex          den, pee: no links
       | \     /            to anything useful
       |  \   /
      tad  tex
         \  /
          tax

  answers (3 chains of 4 words):
    red ted tad tax
    red ted tex tax
    red rex tex tax
```

`tex` is reachable from two different words in the layer above (`ted` and `rex`), and `tax`
from two (`tad` and `tex`). Those merge points are where the difficulty lives: count them
wrong and you lose chains.

## Do it by hand first

Write the words in rows by distance from `red`, like a family tree upside down, and draw an
arrow from each word to every word in the **next** row it links to.

```text
  row 0   red
          |  \
  row 1   ted  rex
          | \    |
  row 2   tad tex <-+     tex has TWO arrows in
          |   |             (from ted and from rex)
  row 3   tax <-+         tax has two arrows in
```

To list the chains, start at `tax` and walk the arrows **backwards**, branching wherever a word
has more than one arrow coming in: `tax <- tad <- ted <- red`, `tax <- tex <- ted <- red`,
`tax <- tex <- rex <- red`.

What did your hand keep? For each word, **the set of words in the row above that point to it**.
Not one parent: all of them, but only from the row directly above. That map, word to parents,
is the seed of the algorithm. Arrows inside one row (none here) or upward are never drawn,
because they never lie on a shortest chain.

## The first honest attempt

DFS from `beginWord` through every simple path (no repeated word), finding neighbours by
comparing against the whole dictionary. Each time you reach `endWord`, compare the path length
with the best so far: shorter replaces the list, equal appends.

```text
  DFS tree from red (each line is one call):
  red
    ted
      tex
        tax  <- length 4, keep
        rex  (dead end: red, tex on path)
      tad
        tax  <- length 4, keep
    rex
      tex
        ted
          tad
            tax  <- length 6, thrown away
        tax  <- length 4, keep
```

In a dictionary this small the waste is mild, but look at its shape. `tex` is explored twice,
once under `ted` and once under `rex`, and each time its whole subtree is walked again. The path
`red rex tex ted tad tax` is built in full before being discarded for length. In a real
dictionary with thousands of words the number of simple paths explodes factorially: the worst
case is around `O(N!)`.

## The turning point

**Claim: every shortest chain moves from layer `k - 1` to layer `k` at each step, so all of them
are the root-to-`endWord` paths of the layered DAG built by BFS, where each word records every
parent from the previous layer.**

Justify it in two parts.

**Only downward-by-one edges matter.** Let `layer(w)` be the BFS distance of `w` from
`beginWord`. A shortest chain to `endWord` that passes through `w` reaches `w` after exactly
`layer(w)` steps; if it took longer to get there, cut in a shorter prefix and you would have a
shorter chain overall. So every step of a shortest chain goes from layer `k - 1` to layer `k`.
Edges inside a layer, or back up, never appear.

**Keep every such edge.** Conversely, any route that steps down one layer at a time from
`beginWord` to `endWord` has exactly `layer(endWord)` steps, so it is shortest. So the set of
shortest chains is exactly the set of downward routes in the DAG of layer `k - 1 -> k` edges.

That gives a two-phase algorithm:

1. **BFS, a layer at a time**, building `parents[w] = { words in the previous layer that link
   to w }`. Stop after the layer that contains `endWord`; deeper layers cannot be on a shortest
   chain.
2. **Backtrack** from `endWord` following `parents`, branching on every parent, until you reach
   `beginWord`; reverse each path. This touches nothing that is not part of an answer.

The subtle part is **when to remove words from the dictionary**. In Word Ladder we marked a word
visited the moment it was first pushed. Do that here and you lose parents. When `rex` is
expanded first, it finds `tex` and would delete it; then `ted`, in the **same** layer, could no
longer see `tex`, and the chain `red ted tex tax` is gone.

```text
  eager delete (wrong)          layer-at-a-time (right)
  expand rex: tex found,        expand rex: nxt[tex]={rex}
    delete tex now              expand ted: nxt[tex]+={ted}
  expand ted: tex missing!                  nxt[tad] ={ted}
    parents[tex] = {rex}        then delete tex, tad together
  -> 2 chains, one lost         -> 3 chains
```

So the solution gathers the whole next layer into `nxt` (a map from new word to its parent
set), and only after every word of the current layer has been expanded does it remove all of
`nxt`'s keys from the dictionary at once. Words removed earlier than that belong to strictly
shallower layers, so dropping them is safe: no edge to them can be on a shortest chain.

Neighbours are generated the 26-letter way: for each position and each letter, build the
candidate and test it against the remaining dictionary set.

## Watch it work

The red-to-tax example. `layer` is the current frontier (the BFS queue, held as a set because
the whole layer is processed together), `words` is what remains of the dictionary.

```text
Frame 1   setup, layer 0
  layer = { red }
  words = { ted tex tax tad den rex pee }
  parents = { }
```
`red` is discarded from `words` up front so nothing can step back to it.

```text
Frame 2   expand layer 0 -> layer 1
  red: r->t gives ted, d->x gives rex
  nxt   = { ted:{red}, rex:{red} }
  words -= {ted rex}
  layer = { ted rex }
```
Both layer-1 words get `red` as their only parent.

```text
Frame 3   expand layer 1 -> layer 2   (the key frame)
  rex: r->t gives tex     nxt[tex] = {rex}
  ted: d->x gives tex     nxt[tex] = {rex ted}
       e->a gives tad     nxt[tad] = {ted}
  only now: words -= {tex tad}
  layer = { tex tad }    words = { tax den pee }
```
Because `tex` stayed in `words` until the layer finished, both `rex` and `ted` registered as
its parents.

```text
Frame 4   expand layer 2 -> layer 3, stop
  tex: e->a gives tax     nxt[tax] = {tex}
  tad: d->x gives tax     nxt[tax] = {tex tad}
  words -= {tax}          found = True
  parents = { ted:{red} rex:{red} tex:{rex ted}
              tad:{ted} tax:{tex tad} }
```
`tax` appears in layer 3, so the BFS stops; `den` and `pee` were never touched.

```text
Frame 5   backtrack from tax, branch 1
  tax -> tad -> ted -> red          (reached begin)
  path built backwards: [tax tad ted red]
  record reversed:      [red ted tad tax]
```
`tad` has a single parent, so this branch yields one chain.

```text
Frame 6   backtrack, branch 2 (via tex)
  tax -> tex -> rex -> red   => [red rex tex tax]
             \-> ted -> red   => [red ted tex tax]

  DAG used:     red
               /   \
             ted   rex
             | \   /
            tad tex
              \ /
              tax
```
`tex` has two parents, so the walk forks there and yields two more chains: three in total.

Invariant across the BFS frames: every word in `parents` had all its parents in the layer just
above, and no word was removed from `words` while the layer that could still discover it was
being expanded.

## Why it is correct

**The BFS builds exactly the shortest-path DAG.** By induction on layers: `layer` always holds
exactly the words at distance `k`, and `words` holds exactly the words at distance greater than
`k` (plus unreachable ones). Expanding every word of layer `k` against `words` therefore finds
every edge from distance `k` to distance `k + 1`, and nothing else: words at distance `k` or
less are gone from `words`. Recording each such edge in `nxt[nb]` gives every distance-`k + 1`
word its full parent set. Removing the whole of `nxt` afterwards restores the invariant for
`k + 1`.

**Backtracking lists exactly the shortest chains.** Each step from a word to one of its parents
goes up one layer, so every path from `endWord` reaches `beginWord` in exactly `layer(endWord)`
steps, a shortest chain. Every shortest chain consists of downward-by-one edges (the turning
point), all of which are recorded, so backtracking, which tries every parent, finds every one.
Distinct parent choices give distinct chains, so there are no duplicates.

If the BFS runs out of layers without seeing `endWord`, no chain exists and `[]` is returned.

## Cost

- **BFS**: each word is expanded at most once, generating `26 * L` candidates of length `L`:
  `O(N * 26 * L^2)` time.
- **Backtracking**: `O(P * D)` for `P` chains of `D` words each. The output itself can be
  exponential in size, and no algorithm can avoid writing it.
- **Space**: `O(N * L)` for the dictionary set and the layers, plus one parent entry per DAG
  edge.
- **Brute force**: exponential in `N`.

A practical refinement: store backtracking paths in one shared list (append, recurse, pop)
instead of `path + [p]` copies, and run the BFS bidirectionally when the dictionary is large.

## Variations you will meet

- **Count the shortest chains instead of listing them.** Replace parent sets by counts:
  `ways[nb] += ways[w]` along each downward edge. No backtracking, polynomial time even when
  the number of chains is exponential.
- **All shortest paths in any unweighted graph.** The same layered BFS plus parents; this
  appears in "shortest path count" questions and in Brandes' betweenness algorithm.
- **Weighted version.** Dijkstra with a parent set: add `u` to `parents[v]` when
  `dist[u] + w == dist[v]`, and reset the set when a strictly better distance is found.
- **Return any one shortest chain.** One parent per word suffices; that is Word Ladder with a
  back-pointer.

## What to carry forward

To return all shortest paths, BFS one whole layer at a time, record every parent from the layer
above, and only then retire the layer; then walk the parents backwards. The next problem,
Sliding Puzzle, goes back to one shortest distance, but the nodes become entire board
configurations that you must encode as strings.
