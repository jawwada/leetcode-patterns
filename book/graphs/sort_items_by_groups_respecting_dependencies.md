# Sort Items by Groups Respecting Dependencies

*LeetCode 1203 · Hard · Pattern: Topological sort (Kahn's BFS) / cycle detection · Reading time ~11 min*

## What the problem is really asking

There are n items. Item i belongs to group `group[i]`, one of m groups, or to no group if `group[i] == -1`. `beforeItems[i]` lists the items that must appear before item i. Produce one ordering of all n items such that

1. every "u before v" constraint holds, and
2. the items of each group sit next to each other, as one contiguous block.

Return any such ordering, or `[]` if none exists.

```text
 n = 8, m = 2
 item:        0   1   2   3   4   5   6   7
 group:      -1  -1   1   0   0   1   0  -1
 beforeItems: []  [6] [5] [6] [3,6] [] [] []

 one valid answer: 6 3 4 | 5 2 | 0 | 7 | 1
                   grp 0  grp 1
```

Without rule 2 this is Course Schedule II: items are courses, `u in beforeItems[v]` is the arrow `u -> v`. Rule 2 is what makes it hard. A plain topological order of the items will happily interleave groups, and you cannot simply "pull a group together" afterwards without possibly breaking an arrow. The answer is a permutation of items; the difficulty is that it must be ordered correctly at two scales simultaneously.

## Do it by hand first

Draw items as beads and groups as boxes. Items with no group get no box yet.

```text
     box g0              box g1        loose items
 +----------------+   +---------+
 | 6 --> 3 --> 4  |   | 5 --> 2 |     0    1    7
 | |  (also 6->4) |   +---------+          ^
 +-|--------------+                        |
   +---------------------------------------+
        6 -> 1 leaves the g0 box
```

Look at the arrows. Some stay inside a box: 6 -> 3, 3 -> 4, 6 -> 4 inside g0, and 5 -> 2 inside g1. One crosses boxes: 6 -> 1, from g0 to the loose item 1.

A human solves this at two zoom levels. Zoomed out: each box is one big block, and the crossing arrow 6 -> 1 says the block containing 6 must come before the block containing 1. Since g0 is contiguous, all of g0 comes before 1, not just item 6. Zoomed in: inside g0, put 6, then 3, then 4. Inside g1, put 5, then 2.

```text
 zoomed out: [g0] [g1] [0] [7] [1]    (g0 before [1])
 zoomed in:  g0 = 6 3 4      g1 = 5 2
 laid out:   6 3 4  5 2  0  7  1
```

What did your hand keep track of? Two orderings: one over blocks, one over items within each block. And to treat a loose item like a block, your hand quietly gave it a box of its own. That is the seed: two graphs, two topological sorts, and every ungrouped item promoted to a singleton group.

## The first honest attempt

The honest brute force tries every permutation of the n items and checks both rules: each `u before v` pair, and for each group, that its items occupy a contiguous run of positions. Return the first that passes.

There are n! permutations, each checked in O(n + E), so O(n! · (n + E)). For n = 8 that is 40,320 permutations; for the real limit of 3 · 10^4 items it is hopeless.

```text
 permutations sharing the prefix  1 ...
   1 0 2 3 4 5 6 7     fails: 6 must precede 1
   1 0 2 3 4 5 7 6     fails: 6 must precede 1
   1 0 2 3 4 6 5 7     fails: 6 must precede 1
   ... all 7! = 5040 of them fail for the SAME reason
```

The waste is enormous and visible: a violation decided by the first position is re-discovered in every one of the thousands of permutations that share it. A smarter backtracking search prunes those, but it is still searching, when the constraints actually dictate a valid answer greedily.

## The turning point

**Claim: an ordering satisfies both rules iff it is a topological order of the groups, with each group's items laid out in an order consistent with a topological order of the items; so two Kahn passes, one over items and one over groups, solve it.**

Build it in three moves.

**Move 1: make every item belong to a group.** For each item with `group[i] == -1`, assign a fresh id `m, m+1, ...`. A singleton group is trivially contiguous, so this changes nothing about the problem, but now every item has a block. Skipping this and leaving all -1 items in one pretend group is the classic bug: it forces all the loose items to be adjacent, which the problem never asked for.

**Move 2: build two graphs from the same constraints.** For every `u in beforeItems[v]`:

- add the item arrow `u -> v`;
- if `group[u] != group[v]`, also add the group arrow `group[u] -> group[v]`.

Why the group arrow is forced: v's whole block must be contiguous, and so must u's. If u is before v and they are in different blocks, then u's block cannot start after v's block or interleave with it, so u's block lies entirely before v's block. Never add a group arrow when the two items share a group, because `g -> g` is a self-loop, which Kahn reads as a cycle.

```text
 item graph (8 nodes)             group graph (5 nodes)
   6 -> 1, 6 -> 3, 6 -> 4           g0 -> g3   (from 6 -> 1)
   3 -> 4, 5 -> 2
 item indeg  0 1 1 1 2 0 0 0       group indeg  0 0 0 1 0
```

**Move 3: sort both, then nest.** Topologically sort items and groups with Kahn. If either sort comes up short, there is a cycle and the answer is `[]`. Otherwise, walk the item order once and drop each item into its group's bucket; buckets inherit the item order. Then concatenate buckets in group order.

Why the nesting is correct is the whole insight. Take any constraint `u -> v`:

- **Same group:** u and v land in the same bucket. The bucket preserves the item order, in which u precedes v. Good.
- **Different groups:** the group arrow `group[u] -> group[v]` puts u's bucket wholly before v's bucket. Good.

Contiguity holds by construction, since each bucket is output as one run. Notice what is subtle here: the item order alone interleaves groups, and the group order alone says nothing about items inside a group. Neither sort suffices; the concatenation uses the item sort only for its within-group restriction and the group sort only for its between-group order.

And notice the two ways to fail. The item graph can have a cycle (6 -> 3 -> 4 -> 6, all inside g0). Or the item graph can be fine while the group graph has a cycle: items `0 -> 1 -> 2` with 0 and 2 in g0 and 1 alone. Item 1 must sit between two members of g0, which would split the block. The group graph sees `g0 -> g1 -> g0` and catches it. That second kind of failure is invisible to an item-only sort.

## Watch it work

Example from the top. The solution's `topo` helper uses a growing list as its queue: it appends newly freed nodes to `order` and keeps iterating over it.

**Frame 1.** Promote the three ungrouped items to fresh groups 2, 3, 4.

```text
 item:   0   1   2   3   4   5   6   7
 group: -1  -1   1   0   0   1   0  -1
          |   |                       |
          v   v                       v
 group:  g2  g3  g1  g0  g0  g1  g0  g4      m = 5
```

**Frame 2.** Build both graphs and their in-degrees. Only `6 -> 1` crosses groups (g0 to g3).

```text
 item adj: 3:[4]  5:[2]  6:[1,3,4]
 item indeg:   0 1 1 1 2 0 0 0   (items 0..7)
 group adj: g0:[g3]
 group indeg:  0 0 0 1 0         (g0..g4)
```

**Frame 3.** Item Kahn. Start with the zero in-degree items, then process 0 (no arrows) and 5 (frees 2).

```text
 order:  [0, 5, 6, 7 | 2]
          done ^       ^ appended when 5 was processed
 item indeg:   0 1 0 1 2 0 0 0
```

**Frame 4.** Process 6: item 1 drops to 0 and is appended; 3 drops to 0 and is appended; 4 drops 2 -> 1.

```text
 order:  [0, 5, 6, 7, 2, 1, 3]
 item indeg:   0 0 0 0 1 0 0 0
                       ^ item 4 still waits on 3
```

**Frame 5.** Processing 7, 2, 1 frees nothing; processing 3 drops 4 to 0. All 8 items are emitted.

```text
 item order: [0, 5, 6, 7, 2, 1, 3, 4]      8 == n, no cycle
```

**Frame 6.** Group Kahn. Start: g0, g1, g2, g4. Processing g0 frees g3.

```text
 group indeg: 0 0 0 0 0
 group order: [g0, g1, g2, g4, g3]          5 == m, no cycle
```

**Frame 7.** Bucket the item order by group, keeping item order inside each bucket.

```text
 walk 0 5 6 7 2 1 3 4:
   g0: [6, 3, 4]   g1: [5, 2]   g2: [0]   g3: [1]   g4: [7]
```

**Frame 8.** Concatenate buckets in group order g0, g1, g2, g4, g3.

```text
  6 3 4 | 5 2 | 0 | 7 | 1
   g0     g1   g2  g4  g3
 6->3 ok  6->4 ok  3->4 ok  5->2 ok  6->1 ok (g0 before g3)
```

The answer `[6, 3, 4, 5, 2, 0, 7, 1]` is what the solution returns. It differs from the sample answer in the problem, which is fine; any valid order is accepted. Across frames, the item sort and the group sort never talked to each other. The only thing joining them was the bucket step, and every constraint was guaranteed by exactly one of the two sorts.

## Why it is correct

If the function returns an ordering, it is valid: every item appears once (each item is in exactly one bucket), each group is contiguous (each bucket is emitted as one run), and every constraint `u -> v` is respected by the within-bucket or between-bucket argument above.

If the function returns `[]`, no valid ordering exists. An item cycle means no ordering satisfies even the plain constraints. A group cycle `g_1 -> g_2 -> ... -> g_1` means each group must lie wholly before the next one, as argued when building the group arrows, which is impossible around a ring.

If a valid ordering exists, both graphs are acyclic. The items in that ordering form a topological order of the item graph, and reading off the blocks in that ordering gives a topological order of the group graph. So both Kahn passes complete, and the function returns an answer rather than `[]`.

## Cost

- Time O(n + m + E): each Kahn pass is linear in its nodes and arrows; there is at most one group arrow per item arrow; bucketing is O(n). Here m counts groups after promoting the ungrouped items, so it is at most the original m plus n.
- Space O(n + m + E): two adjacency structures, two in-degree arrays, and the buckets.
- The permutation search was O(n! · (n + E)).

## Variations you will meet

- **Duplicate group arrows.** Two cross-group item arrows between the same pair of groups add the same group arrow twice. That is safe here because the adjacency is a list: in-degree is incremented twice and decremented twice. It is unsafe if you deduplicate one side and not the other, the exact bug from Alien Dictionary.
- **Nested hierarchies.** Teams inside departments inside divisions: the same trick recurses. Sort at each level and nest the buckets.
- **Contiguity without dependencies between groups.** If no constraint crosses groups, the group graph has no arrows and any group order works; the problem collapses to an independent topological sort inside each group.
- **Use a min-heap** if a specific (smallest) answer is required; both sorts take a log factor.

## What to carry forward

When an ordering must be correct at two scales, build a graph at each scale, sort each one, and nest the fine order inside the coarse order; every constraint is then guarded by exactly one of the sorts. The next problem, Reconstruct Itinerary, leaves topological sorting behind: instead of ordering nodes so arrows point forward, it must walk every arrow exactly once, and it does so by writing nodes down when they are finished, the post-order trick hinted at in Course Schedule II.
