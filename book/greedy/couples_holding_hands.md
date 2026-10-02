# Couples Holding Hands

*LeetCode 765 · Hard · Pattern: Union-Find (disjoint set union) · Reading time ~9 min*

## What the problem is really asking

There are `2n` seats in a row, grouped into `n` couches: seats 0 and 1, seats 2 and 3, and so on. Person `2k` and person `2k + 1` are a couple. A swap exchanges any two people anywhere in the row. Find the fewest swaps after which every couple shares a couch.

The answer is a count. What makes it hard is that swaps can be between any two seats, so the space of plans is huge, and a single swap can sometimes fix two couches at once and sometimes only one. You need a way to see how many swaps the mess "really" contains without simulating plans.

First, a lookup trick that the whole problem rests on: person `p`'s partner is `p ^ 1` (flip the last bit), and person `p` belongs to couple number `p // 2`.

```text
row = [5, 4, 2, 6, 3, 1, 0, 7]

seat:   0 1 | 2 3 | 4 5 | 6 7
person: 5 4 | 2 6 | 3 1 | 0 7
couple: 2 2 | 1 3 | 1 0 | 0 3
couch:   A     B     C     D
A is happy (couple 2). B, C, D are mixed.
answer 2
```

## Do it by hand first

Walk the couches left to right. At each couch, keep the person on the left seat and bring their partner into the right seat with one swap, if the partner is not already there.

```text
start:  [5 4 | 2 6 | 3 1 | 0 7]
couch A: 5 & 4 partners           ok
couch B: 2 wants 3, 3 is at seat 4
  swap seats 3,4 -> [5 4 | 2 3 | 6 1 | 0 7]
couch C: 6 wants 7, 7 is at seat 7
  swap seats 5,7 -> [5 4 | 2 3 | 6 7 | 0 1]
couch D: 0 & 1 partners           ok
swaps: 2
```

Your hand needed to know where each person sits, a position table, and it got 2. But was 2 the best? Something more interesting was going on: couches B, C and D were tangled together, and A was not involved at all. The thing to keep track of is which couples are tangled with which. That is the seed of a union-find.

## The first honest attempt

Breadth-first search over seatings: from each row, try all `C(2n, 2)` swaps, stop at the first row where every couple is together.

```text
[5,4,2,6,3,1,0,7]
  -> 28 possible swaps
       many move 5 or 4, already happy
       many swap two strangers, fixing nothing
  -> 28 x 28 rows at depth 2 ...
  state space: (2n)! seatings
```

Exponential. The repeated work is that BFS explores swaps that obviously do not help, and it re-learns the tangle structure along every path.

The tempting shortcut instead is to count unhappy couches and assume each swap fixes two, giving `unhappy / 2` rounded up. It is wrong as soon as a tangle has more than two couches:

```text
row = [0,2 | 3,4 | 5,6 | 7,1]
couples:  0,1 | 1,2 | 2,3 | 3,0
4 unhappy couches -> shortcut says 2
truth (BFS):         3
```

In a ring of four tangled couches, the last swap fixes two couches, but every earlier swap fixes only one. The answer depends on how couches are tangled, not just how many are unhappy.

## The turning point

**Claim: build a graph whose nodes are couples and whose edges are couches (each couch joins the couples of its two occupants); the answer is `n` minus the number of connected components.**

Each couple has exactly two members, sitting on one or two couches, so every node has degree exactly 2 (a couple sharing a couch gives a self-loop, which counts as 2). A graph where every node has degree 2 is a disjoint union of cycles. So the seating decomposes into independent loops.

```text
couples as nodes, couches as edges:

  couch A: (2,2)       couch B: (1,3)
  couch C: (1,0)       couch D: (0,3)

     (2)--loop         1 ---B--- 3
      \__/A             \       /
                         C     D
                          \   /
                            0
  components: {2}, {0,1,3}   -> 2
  answer = 4 - 2 = 2
```

A cycle through `k` couples spans exactly `k` couches. Fixing it takes `k - 1` swaps: each greedy "bring the partner over" swap seats one couple correctly and leaves the rest as a cycle one shorter, and when two couples remain on two couches, one swap fixes both. Summing `k - 1` over all cycles gives `n - (number of cycles)`.

Go back to the ring that broke the shortcut, `[0,2 | 3,4 | 5,6 | 7,1]`. Its graph is one cycle through all four couples: 0-1-2-3-0. The first greedy swap fetches 1 next to 0 and leaves a three-couple cycle; the second leaves a two-couple cycle; the third swap fixes the final two couples at once. That is `4 - 1 = 3`, matching the BFS. The shortcut assumed every swap is a "last swap"; only one swap per cycle gets that discount.

Union-find counts the cycles without ever tracing them: start with `n` singleton components, union the two couples on each couch, and count how many unions actually merge two different components.

## Watch it work

Example: `row = [5, 4, 2, 6, 3, 1, 0, 7]`, `n = 4` couples. The solution returns 2.

Frame 1. Initialise: every couple is its own component.

```text
couple:   0  1  2  3
parent:  [0, 1, 2, 3]       components 4
```

Frame 2. Couch A, seats 0-1: persons 5, 4, couples 2, 2.

```text
seat:  [5 4] 2 6 3 1 0 7
couples 2 and 2: same root -> no merge
parent:  [0, 1, 2, 3]       components 4
```

A happy couch is a self-loop: a cycle of length 1, costing nothing.

Frame 3. Couch B, seats 2-3: persons 2, 6, couples 1, 3.

```text
seat:   5 4 [2 6] 3 1 0 7
find(1)=1, find(3)=3, differ -> parent[1]=3
parent:  [0, 3, 2, 3]       components 3
```

Frame 4. Couch C, seats 4-5: persons 3, 1, couples 1, 0.

```text
seat:   5 4 2 6 [3 1] 0 7
find(1): 1 -> 3, root 3      find(0) = 0
differ -> parent[3] = 0
parent:  [0, 3, 2, 0]       components 2
```

Couples 0, 1 and 3 are now one tangle rooted at 0.

Frame 5. Couch D, seats 6-7: persons 0, 7, couples 0, 3.

```text
seat:   5 4 2 6 3 1 [0 7]
find(0) = 0, find(3): 3 -> 0, root 0
same root -> no merge (this edge closes the cycle)
parent:  [0, 3, 2, 0]       components 2
```

Frame 6. Answer.

```text
components: {2} (size 1), {0,1,3} (size 3)
swaps = (1-1) + (3-1) = 2 = 4 - 2
```

Across the frames, the number of merges so far equalled the number of swaps that the processed couches will need, because each merge adds one couple to a growing tangle. The edge that closes a cycle (Frame 5) never merges, which is exactly why a cycle of `k` couples costs `k - 1` and not `k`.

## Why it is correct

Two halves: `n - c` swaps suffice, and fewer cannot work, where `c` is the number of cycles.

Upper bound, by the greedy. In a cycle of `k >= 2` couples, take any unhappy couch with persons `x` and `y`. Swap `y` with `x`'s partner. Now `x`'s couple sits together, forming its own cycle of length 1, and the other `k - 1` couples still form one cycle (the swap just rerouted one edge). Each swap reduces `n - c` by exactly 1, and when every couple is happy, `c = n` and `n - c = 0`. So `n - c` swaps are enough.

Lower bound, by an invariant. Any swap exchanges two people. If both are on couches of the same cycle, the swap can split that cycle into at most two pieces. If they are on different cycles, the swap merges them into one. Either way, the number of cycles grows by at most 1 per swap. The goal state has `n` cycles (all self-loops), we start with `c`, so at least `n - c` swaps are needed.

Since both bounds meet, `n - c` is exact, and the greedy "fix each couch by fetching the partner" is optimal no matter which unhappy couch you start with. That is the exchange-style insight: any optimal plan can be reordered into greedy swaps, because all that matters is that each swap increases the cycle count by one, and the greedy swap always does.

The union-find counts `c` because in a degree-2 graph, connected components and cycles are the same thing.

## Cost

Time O(n alpha(n)): one `find` pair and at most one link per couch, with path halving keeping trees shallow. Effectively linear.

Space O(n) for the parent array over couples.

The position-table greedy from "Do it by hand" is also O(n) time and O(n) space and returns the same count; the union-find version is the one that explains why the count is minimal.

## Variations you will meet

- **Minimum swaps to sort a permutation.** Same cycle lemma: the answer is `n - (number of cycles of the permutation)`, because a swap changes the cycle count by exactly one.
- **Groups of three (or `k`) must sit together.** Degree is no longer 2, so components are not cycles, and the clean `n - c` formula disappears; this becomes a much harder matching or search problem.
- **Only adjacent swaps allowed.** The cost becomes a distance, not a cycle count; think inversions and bubble-sort reasoning instead of union-find.
- **Number of Provinces / Redundant Connection.** The same union-find machinery used purely for component counting or for detecting the edge that closes a cycle (here, Frame 5's couch).

## What to carry forward

When a greedy step's quality is hard to judge locally, find a global quantity (here, the number of cycles) that every move changes by at most one, and show the greedy move always changes it by exactly one. The final problem of the chapter also needs a change of viewpoint to make greedy safe: instead of building the target forwards, it peels the last stamp off first.
