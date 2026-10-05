# Reconstruct Itinerary

*LeetCode 332 · Hard · Pattern: Eulerian path (Hierholzer's DFS) · Reading time ~10 min*

## The problem

Given tickets [from, to] that all belong to one traveller starting at "JFK", reconstruct the itinerary that uses every
ticket exactly once; if several exist, return the lexicographically smallest when read as one string. A valid
itinerary is guaranteed.

```text
Example:
  [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]] ->
  ["JFK","MUC","LHR","SFO","SJC"].
```

## What the problem is really asking

You find a pile of used plane tickets, each `[from, to]`, all belonging to one traveller who started at `"JFK"`. Rebuild the trip: a sequence of airports that uses every ticket exactly once. Several trips may fit; return the one that is smallest when the airport names are compared in order (lexicographically). At least one valid trip is guaranteed.

Airports are nodes, tickets are directed edges, and the same ticket may appear twice (two edges). The answer is a walk that uses every edge exactly once. That has a name: an **Eulerian path**. Notice the shift from the last four problems. There, we ordered *nodes* so that every arrow points forward, and visiting a node once was the point. Here nodes may be visited many times; it is the *edges* that must each be used once.

```text
 tickets = [JFK,KUL] [JFK,NRT] [NRT,JFK]

 the thing:                       stored (sorted DESCENDING,
                                  so pop() gives the smallest):
       +-------> KUL
       |                            JFK: [NRT, KUL]
      JFK <-----------+             NRT: [JFK]
       |              |             KUL: []
       +-------> NRT -+

 answer: JFK -> NRT -> JFK -> KUL
```

What makes it hard: the lexicographic rule tempts you to always take the smallest destination, and that greedy choice can strand you. From JFK the smallest destination is KUL, but KUL has no outgoing tickets; fly there first and the NRT round trip is never used.

## Do it by hand first

Try the greedy walk with a pencil and cross off tickets as you use them.

```text
 at JFK, smallest unused: KUL   -> fly   used: JFK-KUL
 at KUL, no tickets left        -> STUCK
 unused: JFK-NRT, NRT-JFK
```

Stuck, with two tickets left. A human now does something clever without naming it. "KUL is a dead end, so KUL must be where the trip *ends*. I just got there too early. The leftover tickets form a loop out of JFK, NRT and back to JFK. Splice that loop in before going to KUL."

```text
 greedy walk:        JFK ----------------------> KUL
 detour found:       JFK -> NRT -> JFK
 spliced:            JFK -> NRT -> JFK --------> KUL
```

What did your hand track? The tickets still unused from each airport, and a growing *end* of the trip: the dead end was fixed first, at the back, and everything else was inserted in front of it. That is the seed: when you are stuck, you have found the end of the current stretch, so write it down at the back.

## The first honest attempt

Backtracking. From the current airport, try unused tickets in lexicographic order of destination. Recurse. If the recursion comes back having used fewer than all tickets, undo the last ticket and try the next destination. The first complete trip found is the lexicographically smallest, because choices were tried smallest first.

```text
 path [JFK]          try KUL
 path [JFK,KUL]      no tickets, 1 of 3 used    -> undo
 path [JFK]          try NRT
 path [JFK,NRT]      try JFK
 path [JFK,NRT,JFK]  try KUL
 path [JFK,NRT,JFK,KUL]  3 of 3 used            -> done
```

On this tiny input the waste is one bad branch. In general it is exponential: the search can commit to an early small destination, walk deep into the graph, discover that some ticket became unreachable, and unwind a long suffix only to rebuild most of it after a different choice. The repeated work is exactly that suffix: big chunks of the walk built, torn down and rebuilt in nearly the same shape.

## The turning point

**Claim: in a graph with an Eulerian path, if you walk greedily deleting each edge as you use it, the first airport where you get stuck is the end of the whole trip; and recursively, each airport is final at the moment all its outgoing tickets are used.**

Why the stuck airport is the end. Think about degrees, as in Find the Town Judge. On an Eulerian path every middle visit to an airport uses one ticket in and one ticket out. So for every airport except the start and the end, tickets in equal tickets out. The start has one more out than in; the end has one more in than out (or start equals end with all balanced, if the trip is a loop). Now, when the greedy walk arrives at an airport X that is not the end, it has used one more ticket into X than out of X, and X has at least as many outgoing tickets as incoming in total. So there is always an unused ticket leaving X. The walk can only get stuck at the trip's end.

What about the leftover tickets? They form loops hanging off airports already on the walk, like the JFK-NRT-JFK loop. Each loop must be spliced in at the airport where it starts.

**Hierholzer's algorithm** does both jobs with one recursive function:

```text
 dfs(a):
     while a has unused tickets:
         dfs(smallest unused destination from a)
     route.append(a)          # a is finished
 answer = reversed(route)
```

The key is the position of `route.append`: after the loop, not before. An airport is written down only when it has no tickets left, which means everything that comes after it in the trip has already been written. So `route` is the trip built from the back, and reversing it gives the trip. When the recursion returns from a dead end to an airport that still has tickets, the loop simply continues, which is how the leftover loops get explored and spliced in exactly at the right place: before the part already written.

Why the greedy "smallest first" choice still gives the lexicographically smallest trip: at each airport, the smallest destination is tried first. Either it leads to a loop that comes back here, in which case it belongs as early as possible and ends up as early as possible; or it is the dead-end branch, which post-order pushes to the back where it must be anyway. No search, no undo.

The storage detail: keep each airport's destinations sorted in *descending* order and `pop()` from the end, which is O(1) and gives the smallest. Sorting ascending and popping from the front is O(k) per pop on a Python list.

## Watch it work

Example `[JFK,KUL] [JFK,NRT] [NRT,JFK]`. State: the remaining ticket lists, the recursion stack (deepest on the right), and `route`.

**Frame 1.** Enter `dfs(JFK)`. It has tickets; pop the smallest, KUL.

```text
 JFK: [NRT]     NRT: [JFK]     KUL: []
 stack: JFK -> KUL
 route: []
```

**Frame 2.** `dfs(KUL)`: no tickets. KUL is finished: append it.

```text
 JFK: [NRT]     NRT: [JFK]     KUL: []
 stack: JFK
 route: [KUL]        <- the end of the trip, fixed first
```

**Frame 3.** Back in `dfs(JFK)`; the while-loop continues because JFK still has NRT. Pop it and go.

```text
 JFK: []        NRT: [JFK]     KUL: []
 stack: JFK -> NRT
 route: [KUL]
```

**Frame 4.** `dfs(NRT)` pops JFK and recurses. This is the second visit to JFK.

```text
 JFK: []        NRT: []        KUL: []
 stack: JFK -> NRT -> JFK
 route: [KUL]
```

**Frame 5.** Inner `dfs(JFK)` has no tickets: append JFK. Return to NRT, which has none either: append NRT.

```text
 stack: JFK
 route: [KUL, JFK, NRT]
```

**Frame 6.** Outer `dfs(JFK)` has no tickets left: append JFK. Reverse.

```text
 route:     [KUL, JFK, NRT, JFK]
 reversed:  [JFK, NRT, JFK, KUL]      3 tickets, 4 stops
```

Across frames, the invariant was: `route` reversed is always a valid *suffix* of the final trip, and every airport on the stack still has its later part of the trip unwritten. The dead end KUL, visited first, was correctly placed last, without any undo.

## Why it is correct

Every ticket is used exactly once: each one is popped from its list once and that pop leads to exactly one `dfs` call. Every airport visit appears in `route` once, when its call returns, so `route` has E + 1 entries.

Consecutive entries form real tickets. When `dfs(b)` is called from `dfs(a)` by ticket `a -> b`, the last thing appended before `a` itself is appended is something finished inside that subtree, and by induction the subtree's appended sequence, reversed, is a walk starting at b. Placing a in front makes a walk starting at a via the ticket a -> b. Loops explored later from a are prepended in front of earlier ones in the reversed order, which is exactly splicing a closed loop in at a.

Lexicographic minimality comes from trying destinations smallest first: the only time a smaller destination ends up later in the trip is when it was a dead-end branch, which no valid trip can visit before using the other tickets out of the current airport.

## Cost

- Time O(E log E): sorting the tickets dominates; afterwards every ticket is popped once and each `dfs` call does O(1) work apart from its loop.
- Space O(E): the adjacency lists, the route, and the recursion stack, which can be E deep on a long chain. For very large inputs, convert to an explicit stack: push the smallest destination while the top has tickets, otherwise pop the top into `route`.
- The backtracking brute force is exponential in the worst case.

## Variations you will meet

- **Valid Arrangement of Pairs (LeetCode 2097).** Same Hierholzer, but no fixed start and no lexicographic rule. Pick the start with the degree test: the node with out-degree minus in-degree equal to 1, or any node if all are balanced. This is the town judge's degree counting reused.
- **Cracking the Safe (LeetCode 753).** Build a de Bruijn sequence: nodes are (k-1)-digit strings, edges append a digit, and an Eulerian circuit covers every k-digit password once.
- **Does an Eulerian path exist?** For directed graphs: at most one node with out - in = 1, at most one with in - out = 1, all others balanced, and all edges reachable from the start. Undirected: zero or two nodes of odd degree.
- **Pre-order instead of post-order.** Appending on the way in produces `JFK KUL NRT JFK` here, which is wrong. The post-order position is the whole algorithm.

## What to carry forward

To use every edge once, walk greedily and write each node down when it runs out of edges; the list read backwards is the path, and dead ends land at the end on their own. This closes the directed-graph stretch. The next problem, Number of Connected Components, drops edge direction entirely and introduces union-find, a structure that answers "are these two nodes already connected?" as edges arrive one by one.
