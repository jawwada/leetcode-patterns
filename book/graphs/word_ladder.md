# Word Ladder
*LeetCode 127 · Hard · Pattern: BFS on implicit graph (wildcard buckets) · Reading time ~11 min*

## What the problem is really asking

You have a start word, an end word and a dictionary. A move changes exactly one letter, and
the word you land on must be in the dictionary (the start word need not be). What is the
smallest number of **words** in a chain from start to end, counting both ends? If no chain
exists, return `0`.

Strip away the words and this is a graph question. Every dictionary word is a node; two
words are joined by an edge when they differ in exactly one position. The answer is the
length of the shortest path from `beginWord` to `endWord`, counted in nodes rather than
edges. All edges cost the same, so "shortest" means BFS.

```text
  begin = hit   end = cog
  dict  = hot dot dog lot log cog

             hit
              |
             hot
            /   \
         dot --- lot
          |       |
         dog --- log
            \   /
             cog

  shortest chain: hit hot dot dog cog  -> 5 words
```

What makes it hard is that **nobody gives you the edges**. You have a bag of strings. The
graph exists only implicitly, and finding a word's neighbours naively costs a scan of the
whole dictionary. With `N` up to 5000 words, the way you discover edges decides whether the
solution runs in time.

## Do it by hand first

Start at `hit`. Which dictionary words differ by one letter? Running your eye down the list:
`hot` (i -> o). That is the whole first ring. From `hot`: `dot` and `lot` (first letter).
From `dot`: `dog`. From `lot`: `log`. From `dog` or `log`: `cog`. Five rings, counting the
start.

```text
  ring 1   hit
  ring 2   hot
  ring 3   dot  lot
  ring 4   dog  log
  ring 5   cog          <- first time we see the end
```

Two things your hand tracked. First, the **current ring**, the words found last step, since
only they can produce new words. That is the BFS queue. Second, a mental "already used"
list: from `lot` you would not go back to `hot` or count `dot` again. That is the visited set.

And a third thing, hidden: how your eye found neighbours. For `hot` you probably did not
compare it letter by letter against all six words; you thought "something-ot" and spotted
`dot` and `lot`. Hold on to that; it is the turning point.

## The first honest attempt

Run BFS from `beginWord`. To expand a word, compare it with **every** dictionary word and keep
those that differ in exactly one position.

```text
  expanding "hot" (L = 3):
    hot vs hot  0 diffs        hot vs lot  1  keep
    hot vs dot  1  keep        hot vs log  2
    hot vs dog  2              hot vs cog  2
  6 comparisons x 3 letters to find 2 neighbours

  expanding "dot": the same 6 comparisons again
  expanding "lot": the same 6 comparisons again
  ...
```

Each expansion is `O(N * L)`, and up to `N` words get expanded, so `O(N^2 * L)`. With
`N = 5000`, `L = 10`, that is 250 million character comparisons. The waste is in the drawing:
nearly every comparison fails, and the dictionary is rescanned for every word even though it
never changes. We keep rediscovering the shape of the same graph.

## The turning point

**Claim: two words are neighbours exactly when they become equal after blanking out the same
single position, so indexing the dictionary by its blanked-out forms turns "find my
neighbours" into `L` hash lookups.**

Blank position 0 of `hot` and you get `*ot`. Blank position 0 of `dot` and you get `*ot` too.
Same pattern means the words agree everywhere except that one slot, which is exactly the
one-letter-change rule. Conversely, if two words differ only in slot `i`, blanking slot `i`
makes them identical.

So build, once, a map from pattern to the words that produce it:

```text
  pattern  -> bucket              each word sits in L buckets
  *ot      -> hot dot lot          (hot is in *ot, h*t, ho*)
  h*t      -> hot
  ho*      -> hot
  d*t      -> dot
  do*      -> dot dog
  *og      -> dog log cog
  lo*      -> lot log
  ...      (l*t, l*g, d*g, c*g, co*: one word each)
```

Picture the buckets as hub nodes: each word hangs off `L` hubs, and two words are adjacent
when they share a hub. A word's neighbours are the union of its `L` buckets, minus itself.

Now BFS on this implicit graph:

- Queue entries are `(word, depth)`, starting with `(beginWord, 1)`, since depth counts words.
- On pop, if the word is `endWord`, return its depth. BFS pops in depth order, so the first
  pop of `endWord` is the shortest.
- Otherwise, for each of the `L` patterns of the word, for each word in that bucket that is
  not visited, mark it visited **and then** enqueue it with `depth + 1`.

Marking on push, not on pop, matters a lot here. Buckets are large and heavily shared: in
the example, `cog` sits in `*og` with both `dog` and `log`. If visited were checked on pop,
`cog` would be pushed once by `dog` and again by `log`; in a big dictionary a popular word
could be pushed hundreds of times. Marking on push keeps the queue at most `N` long.

One cheap guard first: if `endWord` is not in the dictionary, return `0` immediately.

There is a second way to generate neighbours, used in the next problem: for each position,
try all 26 letters and check the candidate against a set of dictionary words. That costs
`26 * L` candidate strings per word instead of `L` bucket lookups, but needs no
preprocessing. Both remove the `N`-sized scan; buckets win when the alphabet is large.

## Watch it work

The example. `q` is the queue of `(word, depth)`; `vis` is the visited set. The layer number
is the depth.

```text
Frame 1   setup, layer 1
  q   = [ (hit,1) ]
  vis = { hit }
  buckets built (12 patterns, table above)
```
`hit` is not in the dictionary, so it is in no bucket; it is only the start.

```text
Frame 2   pop (hit,1)
  *it -> (empty)
  h*t -> hot          new: push
  hi* -> (empty)
  q   = [ (hot,2) ]           <- layer 2
  vis = { hit hot }
```
Only one pattern of `hit` matches anything; layer 2 is the single word `hot`.

```text
Frame 3   pop (hot,2)
  *ot -> hot dot lot   dot, lot new
  h*t -> hot           ho* -> hot
  q   = [ (dot,3) (lot,3) ]   <- layer 3
  vis = { hit hot dot lot }
```
One bucket hands us both layer-3 words at once; no scan of the dictionary happened.

```text
Frame 4   pop (dot,3)
  *ot -> all visited
  d*t -> dot           do* -> dot dog
  q   = [ (lot,3) (dog,4) ]
  vis = { ... dog }
```
`dog` is pushed with depth 4, behind the remaining layer-3 word `lot`.

```text
Frame 5   pop (lot,3)
  *ot -> all visited   l*t -> lot
  lo* -> lot log       log new
  q   = [ (dog,4) (log,4) ]   <- layer 4
  vis = { ... log }
```
Layer 3 is done; the queue now holds exactly layer 4.

```text
Frame 6   pop (dog,4)
  *og -> dog log cog   cog new (log seen)
  d*g -> dog           do* -> dot dog
  q   = [ (log,4) (cog,5) ]
  vis = { ... cog }
```
`cog` is marked the moment `dog` pushes it.

```text
Frame 7   pop (log,4), then pop (cog,5)
  log: *og -> cog already visited, skip
  q   = [ (cog,5) ]
  pop (cog,5): cog == endWord -> return 5
```
Because `cog` was marked on push, `log` does not push it a second time; the next pop returns 5.

Invariant across frames: the queue held words of at most two consecutive depths, in
non-decreasing order, and each word appeared in the queue at most once.

## Why it is correct

The graph is unweighted, so BFS's **layer property** applies: a word is first pushed with
depth `d` exactly when its shortest chain from `beginWord` has `d` words. Seeded with depth
1, each push sets `depth + 1` from a word of depth `d`, and words are popped in
non-decreasing depth, so the first time a word is reached is along a shortest chain; the
visited set stops any later, longer arrival from overwriting it.

The bucket index finds exactly the true neighbours: same pattern if and only if the words
differ in at most that one slot, and the word itself is skipped because it is already
visited. So the BFS walks the true graph, and the first pop of `endWord` carries the
shortest chain length. If the queue runs out, `endWord` is not connected to `beginWord`,
and `0` is correct.

## Cost

- **Brute force**: `O(N^2 * L)` time, `O(N)` space.
- **Buckets**: building takes `O(N * L^2)` (each of `N` words makes `L` patterns of length
  `L`); BFS does the same pattern-building per popped word, so `O(N * L^2)` overall plus the
  bucket scanning. Space `O(N * L^2)` characters for the pattern keys, `O(N * L)` bucket
  entries.

Bucket scanning can be heavy when a pattern like `*at` holds hundreds of words; a common speedup
is to clear a bucket after its first use, since every word in it has been pushed by then.

## Variations you will meet

- **Bidirectional BFS.** Grow one frontier from `beginWord` and one from `endWord`, always
  expanding the smaller, and stop when they meet. The search radius halves on each side,
  which in a branching graph shrinks the work dramatically.
- **Return all shortest chains (Word Ladder II).** You can no longer stop at the first pop,
  and one parent per word is not enough. That is the next problem.
- **Minimum Genetic Mutation (LeetCode 433).** The same problem with an alphabet of four
  letters and length 8; the 26-letter (here 4-letter) substitution approach is natural.
- **Weighted letter changes.** If changing some letters costs more, BFS layers stop meaning
  cost; run Dijkstra on the same implicit graph.

## What to carry forward

When the graph is a rule rather than a list, ask "how do I list a node's neighbours cheaply?",
and a hash of a cleverly blurred key (here, a blanked letter) is often the answer. The next
problem, Word Ladder II, keeps this BFS but must remember every way each word was reached so
it can return all the shortest chains.
