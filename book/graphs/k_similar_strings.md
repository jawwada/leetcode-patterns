# K-Similar Strings
*LeetCode 854 · Hard · Pattern: BFS over states with pruned branching (fix the first mismatch) · Reading time ~10 min*

## What the problem is really asking

You get two strings `s1` and `s2` that are anagrams of each other: same letters, same
counts, different order. Letters come from `a`..`f` and the length is at most 20. One move
swaps any two characters of `s1`. Return the minimum number of moves that turns `s1` into
`s2`.

The answer is a shortest-path length, but the "graph" is not drawn anywhere. A node is a
whole string (an arrangement of the letters), and an edge is one swap. So this is BFS
where every node is a state of the entire input, exactly like Sliding Puzzle, where a node
was a whole board.

```text
  s1 = a b c a b          s2 = b c a b a
  pos  0 1 2 3 4               0 1 2 3 4

  one optimal route (3 swaps):
    a b c a b
    ^       ^    swap 0,4
    b b c a a
      ^ ^        swap 1,2
    b c b a a
        ^ ^      swap 2,3
    b c a b a    = s2
```

What makes it hard: the state space is every arrangement of the letters, which for 20
letters with repeats can be in the billions, and each state has up to n(n-1)/2 = 190 swaps
leading out of it. Plain BFS is correct and hopeless. The whole problem is deciding which
edges you are allowed to ignore without losing the optimum.

## Do it by hand first

Write `s2` under `s1` and look at the columns that disagree.

```text
  pos      0  1  2  3  4
  have     a  b  c  a  b
  want     b  c  a  b  a
           x  x  x  x  x      every column is wrong
```

A person does not try random swaps. You look at position 0 and say "it needs a `b`. Where
is a `b` that is itself in the wrong place?" There are two: position 1 (has `b`, wants `c`)
and position 4 (has `b`, wants `a`). Position 4 is the better pick, because position 4
wants an `a`, and position 0 currently has an `a`. One swap fixes **two** columns:

```text
  swap 0,4:   b b c a a
  want        b c a b a
              ok x  x  x  ok
```

Now position 1 wants `c`; position 2 has `c`. Swap, and position 2 gets `b`, still wrong.
Position 2 wants `a`; position 3 has it. Swap. Done in three.

What did your hand keep track of? **The leftmost column that is still wrong**, and **the
positions holding the letter it needs**. You never touched a column that was already right,
and you never considered swapping two letters that were both irrelevant to the column you
were fixing. That habit is the pruning rule.

## The first honest attempt

BFS over strings with every swap as an edge. Start from `s1`, generate all n(n-1)/2 swaps
of the current string, enqueue the ones not seen yet, and stop when `s2` is dequeued. BFS
layers are swap counts, so the first time `s2` appears is optimal.

It is correct. On our 5-letter example it works through 28 of the 30 distinct arrangements
before it dequeues `s2`. On length 20 it explodes. The waste is visible in the root's
children alone:

```text
  root  a b c a b   has 10 swaps:

  swap 0,1 -> b a c a b    fixes col 0       useful
  swap 0,4 -> b b c a a    fixes cols 0, 4   useful
  swap 0,3 -> a b c a b    two a's: no-op    wasted
  swap 1,2 -> a c b a b    fixes col 1       col 0 still wrong
  swap 2,3 -> a b a c b    fixes col 2       ... same
  swap 1,3 -> a a c b b    fixes col 3       ... same
  ...
  every non-useful child grows its own subtree,
  and those subtrees overlap in many orders
```

Two kinds of repeated work. First, swaps that fix nothing, or that fix one column while
breaking another. Second, the same set of repairs done in different orders: fixing column
1 then column 0 and fixing column 0 then column 1 lead to the same string by different
paths, and BFS explores the neighbourhood of both orders before it notices.

## The turning point

**Claim: from any string, it is enough to branch only on swaps that put the correct letter
into the leftmost wrong position i, taking it from a position j that is itself wrong. Some
optimal answer always starts with one of those swaps.**

That kills both wastes at once. The ordering waste disappears because we always repair
left to right, so "fix 1 then 0" is never generated. The useless-swap waste disappears
because every allowed swap fixes column i and never breaks a correct column.

Why is it safe? Draw the wrong columns as arrows between letters: a wrong position p that
holds letter x and wants letter y is an arrow `x -> y`.

```text
  have  a  b  c  a  b
  want  b  c  a  b  a
  arrow a>b b>c c>a a>b b>a

  arrows split into cycles:
     cycle A : a -> b -> a           (pos 3, pos 4)
     cycle B : a -> b -> c -> a      (pos 0, 1, 2)
```

Every letter has as many arrows leaving as entering (the strings are anagrams), so the
arrows split into cycles. A cycle of length L needs exactly L - 1 swaps: each swap inside a
cycle fixes one position and shortens the cycle by one, and the last swap of a 2-cycle fixes
both its positions. Swaps cannot do better than that: a single swap changes only two
arrows, so it can at most split off one extra cycle. The minimum number of swaps is
therefore `(wrong positions) - (most cycles you can split them into)`. Here 5 - 2 = 3.

Now take the leftmost wrong position i, with arrow `x -> y`. In a best cycle split, the arrow
at i belongs to some cycle, and the next arrow on that cycle starts at letter y: it is some
wrong position j holding y. Swapping i and j puts y into i, which is fixed, and the two
arrows `x -> y` and `y -> z` become one arrow `x -> z` at j. The cycle gets one shorter, the
cycle count stays the same (or, if z == x, a 2-cycle closes and both positions are fixed),
and the formula drops by exactly one. So one of the allowed swaps is on an optimal path,
and since BFS tries every allowed j, it finds that path.

The rule in words, which is all the code does:

```text
  i = first index with cur[i] != s2[i]
  for j > i:
      if cur[j] == s2[i]      # j holds what i needs
      and cur[j] != s2[j]:    # and j is wrong too
          swap(i, j) -> child
```

Branching drops from n(n-1)/2 to "how many wrong positions hold letter s2[i]", which is at
most the count of one letter. The depth is at most n - 1. The search is still a plain BFS
with a `seen` set of strings; the state graph is just drawn with far fewer edges.

Notice the reframe again: **the graph is not the string, it is the state.** Each state
carries an invisible marker, "everything left of i is final", and that marker only moves
right.

## Watch it work

`s2 = bcaba`. The `|` marks the end of the correct prefix (the leftmost wrong position i is
just after it).

```text
Frame 1  layer 0 (swaps = 0)
  queue : [ |abcab ]                seen : 1 string
  i = 0 wants 'b'
  candidates j: 1 (b, wants c)  4 (b, wants a)
```

The root has only two legal children instead of ten swaps.

```text
Frame 2  expand root
  j=1 :  b|acab     fixes col 0
  j=4 :  b|bcaa     fixes cols 0 and 4
  queue : [ b|acab, b|bcaa ]        seen : 3 strings
```

Both children have a correct prefix of length 1; they are layer 1.

```text
Frame 3  layer 1 (swaps = 1)
  b|acab : i=1 wants 'c'; j=2 -> bca|ab
  b|bcaa : i=1 wants 'c'; j=2 -> bc|baa
  queue : [ bca|ab, bc|baa ]        seen : 5 strings
```

Each parent had exactly one legal child; the first one got column 2 right for free.

```text
Frame 4  layer 2 (swaps = 2)
  bca|ab -> i=3 wants 'b'
            j=4 (b, wants a) -> bcaba   new
  bc|baa -> i=2 wants 'a'
            j=3 (a, wants b) -> bcaba   already seen
            j=4 has 'a' but is correct -> not allowed
  queue : [ bcaba ]                  seen : 6 strings
```

Two different repair orders meet in the same string; `seen` keeps one copy. Position 4 is
skipped because taking its `a` would break it.

```text
Frame 5  layer 3 (swaps = 3)
  pop bcaba == s2  -> return 3
```

Six strings were ever created, against the 28 that the all-swaps BFS dequeued.

Invariant across the frames: every string in layer d has a correct prefix at least d long,
every string in the queue is reachable with exactly its layer's number of swaps, and no
string appears twice.

## Why it is correct

Two things: BFS layers equal swap counts, and the pruning keeps at least one optimal path.

The BFS part is standard. Each edge is one swap, the queue is processed layer by layer, and
a string is marked seen when it is pushed. So the layer in which a string first appears is
the fewest pruned-graph swaps that reach it. When `s2` is dequeued at layer d, no shorter
route exists in the pruned graph.

The pruning part is the cycle argument from the turning point. Let `need(cur)` be the
number of wrong positions minus the largest number of cycles their arrows can be split
into. Every swap lowers `need` by at most one, so `need(s1)` is a lower bound. And from any
state with `need > 0` there is an allowed swap (fix the leftmost wrong i from the next
arrow of its cycle) that lowers `need` by exactly one. Following such swaps reaches `s2` in
exactly `need(s1)` moves, all inside the pruned graph. So the pruned BFS answer equals the
lower bound, which is the true minimum.

The `-1` return is unreachable: anagrams can always be matched.

## Cost

- **Time:** O(n x b^d) in the worst case, where b is the pruned branching factor (at most the
  count of one letter), d <= n - 1 is the answer, and each state costs O(n) to build and
  hash. Still exponential, but the restriction to the alphabet `a`..`f` and the forced
  left-to-right order keep the reachable tree small; the 20-letter test in the solution
  file finishes instantly.
- **Space:** the same order, for `seen` and the queue.
- **Brute force:** up to n!/(repeat factorials) states, each with O(n^2) edges.

## Variations you will meet

- **Prefer the double fix.** If some allowed j also has `cur[i] == s2[j]`, that swap closes
  a 2-cycle and is always optimal, so you can take only that child. This prune often turns
  the search almost linear.
- **DFS with a bound or memoisation.** The same branching rule works depth-first with
  `best` as an upper bound (branch and bound), or with memoisation on the suffix string.
  Without a bound, plain DFS finds *a* solution, not the minimum.
- **Minimum swaps to sort a permutation (all letters distinct).** Every cycle is forced,
  there is no choice in splitting, and the answer is simply n minus the number of
  cycles. No search needed. Couples Holding Hands is the same cycle counting on pairs.
- **Sliding Puzzle and Open the Lock.** Same "a node is a whole configuration" BFS, but
  their branching is already small, so no pruning is needed.

## What to carry forward

When BFS states are whole configurations, shrink the branching by always repairing the
leftmost broken position; the cycle argument shows this keeps an optimal answer. The next
problem, Shortest Path in a Grid with Obstacles Elimination, goes the other way: it makes
the state *bigger*, attaching a remaining-budget counter to each cell so a plain grid BFS
can account for a limited resource.
