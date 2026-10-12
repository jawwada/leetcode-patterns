# Find All People With Secret
*LeetCode 2092 · Hard · Pattern: Time-grouped union-find with reset of non-informed components · Reading time ~11 min*

## The problem

There are n people, 0..n-1. Person 0 tells a secret to firstPerson at time 0. meetings[i] = [x, y, t] means x and y
meet at time t. If either of them knows the secret then, both do, and within the same time t the secret passes
instantly along chains of meetings. Return everyone who knows the secret after all meetings.

```text
Example: n=6, meetings=[[1,2,5],[2,3,8],[1,5,10]], firstPerson=1
  -> [0,1,2,3,5].
```

## What the problem is really asking

There are `n` people, numbered `0` to `n - 1`. Person `0` knows a secret and tells it to
`firstPerson` at time 0. Then a list of meetings happens: `[x, y, t]` means `x` and `y`
meet at time `t`. If either of them knows the secret during the meeting, afterwards both
do. Meetings at the **same** time happen in an instant, so the secret can race along a
whole chain of meetings that share a timestamp. Return everyone who knows the secret at
the end.

The answer is a set of people. What makes it hard is time. Connectivity alone is not
enough, because a link that existed at time 5 is useless at time 8: two people who met
before either of them knew the secret did not exchange it, and they do not "remember" the
meeting.

The example we will trace: `n = 6`, `firstPerson = 1`.

```text
   meetings (sorted by time)        timeline
   [1, 2, 5]                        t=0   0 tells 1
   [3, 4, 5]                        t=5   1-2 meet, 3-4 meet
   [2, 3, 8]                        t=8   2-3 meet
   [4, 5, 10]                       t=10  4-5 meet

   answer: [0, 1, 2, 3]
   (4 met 3 at t=5, before 3 knew; 4 never hears it)
```

## Do it by hand first

Walk the timeline with a pen and a set of people who know.

```text
   knows = {0, 1}
   t=5   1-2: 1 knows  -> knows = {0,1,2}
         3-4: neither  -> nothing
   t=8   2-3: 2 knows  -> knows = {0,1,2,3}
   t=10  4-5: neither  -> nothing
   final {0, 1, 2, 3}
```

Your hand kept two kinds of information. One is permanent: the set of people who know.
The other is temporary: who is linked to whom **right now**, at this one timestamp. You
used the temporary links to decide who joins the permanent set, and then you threw the
links away. When you got to `t=8` you did not think "3 is linked to 4"; that link belonged
to `t=5`.

One more detail your hand handles silently: within one timestamp, order does not matter.
If at `t=5` the meetings were `[3,4]`, then `[2,3]`, then `[1,2]`, the secret would still
reach 4, because all three meetings are simultaneous.

## The first honest attempt

Sort the meetings by time and process one time group at a time. Inside a group, sweep the
meetings repeatedly: whenever exactly one side knows, mark both as knowing. Stop when a
whole sweep changes nothing.

That gets the "instant chain" right, but it is slow. A group of `g` meetings arranged as a
chain listed in the worst order spreads one hop per sweep and needs `g` sweeps, so a group
costs `O(g^2)` and the whole input `O(m^2)` in the worst case.

```text
   one group, t=7, listed in the worst order:
     [4,5] [3,4] [2,3] [1,2]      1 knows

   sweep 1: [4,5] no  [3,4] no  [2,3] no  [1,2] YES -> 2
   sweep 2: [4,5] no  [3,4] no  [2,3] YES -> 3  [1,2] ok
   sweep 3: [4,5] no  [3,4] YES -> 4  ...
   sweep 4: [4,5] YES -> 5
   sweep 5: nothing changes, stop
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   each sweep re-reads every meeting to move one hop
```

The waste: within a group the question is pure connectivity ("is this person connected,
through this group's meetings, to someone who knows?"), but the sweep answers it one hop
at a time, re-reading settled meetings every pass.

## The turning point

**Claim: within one timestamp, the people who learn the secret are exactly those connected
by that timestamp's meetings to someone who already knows; and after the timestamp, only
the links that touched the secret should survive.**

The first half says each time group is a connectivity question, and union-find answers
connectivity in near-constant time per edge, regardless of order. Union every meeting of
the group, then everyone whose root equals `find(0)` knows. The chain `[4,5] [3,4] [2,3]
[1,2]` costs four unions, not sixteen meeting reads.

The second half is the trap. Union-find only merges; it never forgets. If we simply keep
unioning across all timestamps, a link made at `t=5` between two people who did not know
leaks into the future:

```text
   WITHOUT reset
   t=5   union 1-2, union 3-4      sets: {0,1,2} {3,4}
   t=8   union 2-3                 sets: {0,1,2,3,4}
                                                   ^ wrong!
   4 joined because of the stale t=5 link 3-4.
   t=10  union 4-5                 sets: {0,..,5}  5 wrong too
```

The fix uses an asymmetry in the problem. Knowing the secret is **permanent**; not knowing
is **temporary and carries no information**. So after each time group:

- anyone in `0`'s component knows, forever. Leave their links alone. Merging them into one
  permanent blob around `0` is exactly right.
- anyone else who took part in this group is cut loose: `parent[p] = p`. Their links were
  real only at this instant and must not affect the future.

Why is it safe to reset just the **participants**, rather than rebuilding the whole forest?
Before the group, every person was either in `0`'s component or a singleton (that is what
the resets guarantee). During the group, only participants get linked. So the only
non-singleton trees outside `0`'s component consist entirely of this group's participants,
and resetting each of them dissolves those trees completely.

Two ordering details matter. First, all unions of a group happen **before** any reset,
because the chain inside a group may pass through a person whose meeting appears later in
the list. Second, the check is `find(p) != find(0)`, comparing roots, since the root of
`0`'s component can change as unions happen (here it drifts from `0` to `2` to `3`).

Seeding is one union: `union(firstPerson, 0)` before any meetings.

## Watch it work

The solution's union sets `parent[root_a] = root_b`. Arrays are indexed by person.

```text
Frame 1   seed: union(1, 0)
   person  0  1  2  3  4  5
   parent  0  0  2  3  4  5      root(0) = 0
```
Person 1 hangs under 0; the knowing set is `{0, 1}`.

```text
Frame 2   t=5 unions: union(1,2) then union(3,4)
   person  0  1  2  3  4  5
   parent  2  0  2  4  4  5      root(0) = 2
   trees:  1 -> 0 -> 2      3 -> 4
```
Root of 1 is 0, so `parent[0] = 2`; separately 3 joins 4.

```text
Frame 3   t=5 reset of participants not under root(0)=2
   1: root 2  keep      2: root 2  keep
   3: root 4  reset     4: root 4  reset
   person  0  1  2  3  4  5
   parent  2  2  2  3  4  5
```
The 3-4 link is forgotten; path halving also lifted 1 to point at 2.

```text
Frame 4   t=8 union(2,3), then check
   person  0  1  2  3  4  5
   parent  3  2  3  3  4  5      root(0) = 3
   2: root 3 keep      3: root 3 keep
```
3 joins the knowing blob. Because of Frame 3, 4 does not come along.

```text
Frame 5   t=10 union(4,5), then check
   after union:  parent[4] = 5
   4: root 5 != 3  reset      5: root 5 != 3  reset
   person  0  1  2  3  4  5
   parent  3  2  3  3  4  5
```
Neither 4 nor 5 knew, so their link is erased immediately.

```text
Frame 6   collect p with find(p) == find(0) = 3
   0->3  1->2->3  2->3  3      yes
   4  5                         no
   answer: [0, 1, 2, 3]
```
Exactly the hand result.

Invariant across frames: between groups, the forest is "one blob containing everyone who
knows, plus singletons". Inside a group it may temporarily hold other trees, and the reset
removes them before the next timestamp begins.

## Why it is correct

Claim, checked after each time group: a person is in `0`'s component if and only if they
know the secret after that time, and every other person is a singleton.

Before any meeting it holds: `{0, firstPerson}` know and form one tree; everyone else is a
singleton.

Suppose it holds before group `t`. The group's unions produce components that are the
union of the old blob and the group's meeting graph. A person ends up in `0`'s component
exactly when the group's meetings connect them, possibly through several hops, to someone
in the old blob, that is, to someone who already knew. Because same-time meetings are
instant, that is exactly the rule for learning the secret at `t`. Every participant outside
`0`'s component did not learn it and is reset to a singleton; non-participants were
untouched and already satisfied the claim. So the claim holds after group `t`.

After the last group, the people in `0`'s component are exactly those who know.

## Cost

- **Time `O(m log m + (n + m) * alpha(n))`**: sorting the meetings dominates; each meeting
  then costs one union and two root checks, and the final scan is `n` finds.
- **Space `O(n + m)`**: the parent array, plus the sorted copy of the meetings.
- **The brute force** is `O(m^2)` in the worst case because of one-hop-per-sweep spreading.

## Variations you will meet

- **BFS per time group instead of union-find.** Build a small adjacency list from the
  group's meetings, start a BFS from the group's participants who already know, and mark
  everyone reached. Same complexity, no reset needed, since the adjacency list is thrown
  away after each group.
- **Dijkstra on "earliest time you can learn it".** Treat a meeting at `t` as usable only
  if you knew by time `t`; process people in order of the time they learned. This is the
  same shape as the shortest-path problems later in the chapter.
- **Secrets that expire, or need two informed partners.** Knowing stops being monotone,
  and the "keep the blob forever" step breaks. You fall back to per-group BFS with explicit
  state.
- **Number of Islands II, revisited.** Online union-find again, but there nothing is ever
  undone. This problem is the first where union-find must *forget*, and the trick is that
  only uninformed pieces ever need forgetting.

## What to carry forward

When links are valid only at one moment, group events by time, union inside the group,
then reset everything that did not reach the permanent blob. The next problem also sorts
by a parameter, but the union-find never needs to forget: as an edge-weight threshold
rises, components only ever merge.
