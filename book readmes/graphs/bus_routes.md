# Bus Routes
*LeetCode 815 · Hard · Pattern: BFS on implicit graph (stop -> routes index) · Reading time ~11 min*

## The problem

routes[i] lists the stops bus i cycles through. Starting at stop source (not on a bus), return the minimum number of
buses needed to reach stop target, or -1.

```text
Example: routes = [[1,2,7],[3,6,7]], source = 1, target = 6 -> 2
  (bus 0 to stop 7, then bus 1). If source == target the answer
  is 0.
```

## What the problem is really asking

You are given a list of bus routes. `routes[i]` is the list of stops bus `i` loops through
forever, so once you are on bus `i` you can get off at any stop on its list. You start
standing at stop `source`, not on any bus. Return the fewest buses you must board to reach
stop `target`, or -1 if it cannot be done. If you are already at the target, the answer is 0.

The answer is a count of **boardings**. It is not a count of stops passed or distance
travelled. A bus that visits 10,000 stops costs exactly as much as a bus that visits two.
That one sentence is what makes the problem awkward: the natural graph (stops connected
to stops) measures the wrong thing, and the graph that measures the right thing (buses
connected to buses) is not given to you.

Here is the example we will follow all chapter:

```text
  routes = [[1,2,3], [3,4,5], [5,6], [2,8], [8,6]]
  source = 1, target = 6

  bus 0 :  1 --- 2 --- 3
  bus 1 :              3 --- 4 --- 5
  bus 2 :                          5 --- 6
  bus 3 :        2 --- 8
  bus 4 :              8 --- 6

  one answer:  bus 0 (1 -> 3), bus 1 (3 -> 5), bus 2 (5 -> 6)
  another   :  bus 0 (1 -> 2), bus 3 (2 -> 8), bus 4 (8 -> 6)
  both use 3 buses -> answer 3
```

Constraints that matter: up to 500 routes, but up to 100,000 stops in total across all
routes, and stop labels can be as large as 10^6. So individual routes can be enormous and
the stop labels are not small dense indices.

## Do it by hand first

Put your finger on stop 1. Which buses can you get on? Only bus 0. Ride it in your head:
you can now step off at 1, 2 or 3. That is everything reachable with **one** bus.

Now, from each of those stops, which buses can you board that you have not boarded yet?
Stop 2 offers bus 3. Stop 3 offers bus 1. So with **two** buses you can reach every stop on
bus 3 and bus 1: stops 8, 4, 5. Still no 6.

From 8 you can board bus 4; from 5 you can board bus 2. Both of those reach 6. So **three**
buses.

```text
  buses used  boarded so far     stops lit so far
  ----------  -----------------  -----------------------
      1       {0}                {1, 2, 3}
      2       {0, 1, 3}          {1, 2, 3, 4, 5, 8}
      3       {0, 1, 2, 3, 4}    {..., 6}   <- target lit
```

What did your hand keep track of? Two things. First, **which buses you have already
boarded**: you never consider getting on bus 0 again, because anywhere bus 0 takes you,
you already reached with one bus. Second, **for each stop, which buses pass through it**:
standing at stop 2, you had to look up "who stops here?". You did that lookup by scanning
the picture with your eyes. A program needs that lookup ready-made: a map from stop to the
list of routes through it. That map is the seed of the solution.

You also expanded the search in rounds: everything with one bus, then everything with two.
That is breadth-first search, and the rounds are BFS layers.

## The first honest attempt

A strong candidate says: "The nodes should be buses, since buses are what I am counting.
Two buses are connected if they share a stop, because you can transfer there. Build that
graph, then BFS from every bus that serves `source` until I reach a bus that serves
`target`."

That is correct. Building the graph is the problem. The obvious way is to turn each route
into a set and, for every pair of routes `(i, j)`, test whether the sets intersect.

```text
  all-pairs intersection test, R routes

            b0   b1   b2   b3   b4
      b0     -    Y    .    Y    .     each cell = one set
      b1          -    Y    .    .     intersection, cost up to
      b2               -    .    Y     the size of the smaller
      b3                    -    Y     route
      b4                         -

  R = 500  -> ~125,000 pair tests, almost all of them "no"
```

There are R(R-1)/2 pairs, and each test costs time proportional to the route sizes. With
500 routes and 100,000 total stops that is on the order of R x S, around 5 x 10^7 set
probes, and O(R^2) memory for the adjacency. Where is the waste? Most pairs of routes share
nothing, yet every pair is tested. And a busy stop shared by 100 routes causes the same
fact ("these routes meet at this stop") to be rediscovered in 100 x 99 / 2 separate pair
tests.

There is a second honest attempt that fails differently: BFS over **stops**, where a
stop's neighbours are all stops on all buses through it, and depth counts buses. The
trouble is that every stop on a long route rescans that whole route when it is expanded.
A route of length L gets scanned L times, so one 10^5 stop route costs 10^10 work.

```text
  stop-graph BFS on one long route  r = [s1 s2 s3 ... sL]

  expand s1: scan s1 s2 s3 ... sL
  expand s2: scan s1 s2 s3 ... sL    <- same route again
  expand s3: scan s1 s2 s3 ... sL    <- and again
     ...  L times  -> L^2 work for one bus
```

Both attempts waste effort on the same thing: rediscovering the relationship between a
route and its stops, over and over.

## The turning point

**Claim: the graph is bipartite (routes on one side, stops on the other), so index it from
the stop side once, and then let BFS touch every route and every stop at most once.**

Look at the input differently. It already is a graph, just a two-coloured one. Each route
is a node, each stop is a node, and there is an edge between route `i` and stop `s` exactly
when `s` is in `routes[i]`. The input lists edges from the route side. One pass builds the
same edges from the stop side:

```text
  the thing (bipartite graph)        how it is stored

   routes      stops                 routes (given):
    b0 ------- 1                      b0: [1, 2, 3]
    b0 ----+-- 2 --+---- b3           b1: [3, 4, 5]
    b0 --+ |       |                  b2: [5, 6]
         +-3 --- b1                   b3: [2, 8]
    b1 ----4                          b4: [8, 6]
    b1 ----5 ---- b2
    b2 ----6 ---- b4                 stop_to_routes (built):
    b3 ----8 ---- b4                  1:[0] 2:[0,3] 3:[0,1]
                                      4:[1] 5:[1,2] 6:[2,4]
                                      8:[3,4]
```

Now a BFS step alternates sides. From a route you walk to its stops; from a stop you walk
to its routes. Riding a bus is route -> stop; transferring is stop -> route. Only the
stop -> route step costs a bus. Two routes are "adjacent" exactly when there is a path
route -> stop -> route, and that path is enumerated directly from the index with no failed
tests.

The repeated work is killed by **two** visited sets, one per side of the graph:

- `seen_routes`: a bus is boarded at most once. Once it is in the queue at depth d, any later
  way of reaching it has depth at least d, so it can never improve anything.
- `seen_stops`: a stop's route list is scanned at most once. When you reach stop 3 a second
  time (from bus 1, after already reaching it from bus 0), every route through stop 3 was
  already enqueued the first time. Rescanning that list would find nothing new.

With both sets in place, each (route, stop) membership pair, which is each edge of the
bipartite graph, is looked at a constant number of times. The total work is bounded by the
size of the input.

Where do the depths come from? The start is not one node but a set: every route through
`source` is at depth 1, because boarding any of them costs one bus. This is a multi-source
BFS, the same move as seeding every rotten orange at time zero. Each time we go
stop -> route for a route not yet seen, depth increases by one. The answer is the depth of
the first route that is found to contain `target`.

So the reframe is the chapter's refrain: **the graph is not the stops, it is the state of
the traveller, and the state that matters is "which bus am I on".** The stops are just the
doors between those states.

## Watch it work

The queue holds `(route, buses used to be on it)`. Routes are written `b0`..`b4`.

```text
Frame 1  seed: every route through source=1
  stop_to_routes[1] = [0]
  queue       : (b0,1)
  seen_routes : {0}
  seen_stops  : {1}
```

Only bus 0 serves stop 1, so the queue starts with one route at depth 1.

```text
Frame 2  pop (b0,1); walk its stops 1, 2, 3
  stop 1 : already seen, skip
  stop 2 : new -> routes [0,3] -> push (b3,2)
  stop 3 : new -> routes [0,1] -> push (b1,2)
  queue       : (b3,2) (b1,2)
  seen_routes : {0,1,3}
  seen_stops  : {1,2,3}
```

Riding bus 0 lights stops 2 and 3; each lit stop hands over its unseen routes at depth 2.

```text
Frame 3  pop (b3,2); walk its stops 2, 8
  stop 2 : already seen, skip    <- no rescan of [0,3]
  stop 8 : new -> routes [3,4] -> push (b4,3)
  queue       : (b1,2) (b4,3)
  seen_routes : {0,1,3,4}
  seen_stops  : {1,2,3,8}
```

Stop 2's route list is not rescanned; stop 8 is new and contributes bus 4 at depth 3.

```text
Frame 4  pop (b1,2); walk its stops 3, 4, 5
  stop 3 : already seen, skip
  stop 4 : new -> routes [1]   -> nothing new
  stop 5 : new -> routes [1,2] -> push (b2,3)
  queue       : (b4,3) (b2,3)
  seen_routes : {0,1,2,3,4}
  seen_stops  : {1,2,3,4,5,8}
```

The depth-2 layer is finished; the queue now holds exactly the depth-3 layer.

```text
Frame 5  pop (b4,3); walk its stops 8, 6
  stop 8 : already seen, skip
  stop 6 : == target  -> return 3
```

Bus 4 serves the target, so three buses suffice, and BFS order says no route at depth 2
served it.

Across every frame the queue held routes in non-decreasing depth, with at most two
distinct depths present. Every route entered `seen_routes` exactly when it was pushed, and
every stop's route list was read at most once. Bus 2 also reaches 6 at depth 3, but we never
needed to look: the first route at the frontier that touches the target ends the search.

## Why it is correct

Think of the bipartite graph with a weight of 1 on every stop -> route edge (boarding) and 0
on every route -> stop edge (riding). The number of buses on a journey is the sum of those
weights. Our BFS works on the route nodes only, where every route -> route hop (through a
shared stop) costs exactly one boarding, so plain unit-weight BFS applies.

The layer property: when a route is pushed with depth d, d is the fewest buses needed to
be on that route. Proof by layers. Depth 1 routes are exactly those serving `source`; you
cannot be on any bus with fewer than one boarding. Suppose the property holds for every
route pushed at depth d. A route first discovered while expanding a depth-d route is
reachable with d + 1 buses. It cannot be reachable with fewer, because then it would share
a stop with some route at depth d - 1 or less, and it would already have been pushed while
that earlier layer was expanded.

The `seen_stops` shortcut does not lose anything. If stop s is skipped while expanding a
route at depth d, s was already lit by a route at depth d' <= d, and at that time every
route through s was pushed at depth d' + 1 <= d + 1 (or was already seen at an even smaller
depth). Nothing the skipped scan could have pushed would get a better depth.

Finally, the first route found containing `target` has the minimum depth among all such
routes, because routes are dequeued in non-decreasing depth. Being on a bus that stops at
`target` means you can get off there, so that depth is the answer. If the queue empties,
no bus that you can ever board serves `target`, and the answer is -1. The `source ==
target` check comes first, because otherwise we would report 1 for a trip that needs no bus.

## Cost

- **Time O(S)**, where S is the total number of stops summed over all routes. Building
  `stop_to_routes` touches each (route, stop) pair once. During BFS each route is popped
  once and walks its own stop list once; each stop's route list is scanned at most once
  thanks to `seen_stops`. Both scans together are bounded by the number of bipartite edges,
  which is S.
- **Space O(S)** for the index, plus O(R) for `seen_routes` and the queue, plus O(S) for
  `seen_stops`.

The explicit route graph costs O(R x S) time and O(R^2) space by comparison.

## Variations you will meet

- **Minimum number of stops instead of buses.** Now each ride between consecutive stops
  costs 1, so BFS runs on stops. Charge for transfers as well and you have two edge
  weights, which leads to Dijkstra or 0-1 BFS (see the box-pushing problem).
- **Transfers cost money, rides are free (or the reverse).** Same bipartite graph, weights
  on the edges. A cost of 1 on transfers and 0 on rides is exactly this problem; mixing
  costs means Dijkstra over (stop, current bus) states.
- **Word Ladder through wildcard patterns.** In Word Ladder you can bucket words by
  patterns like `h*t`. The pattern is the "stop" and the words are the "routes": two words
  are adjacent if they share a pattern. Same bipartite trick, same two visited sets, same
  reason it beats the all-pairs comparison.
- **Accounts Merge.** Emails play the role of stops, accounts play the role of routes, and
  the question is connectivity instead of distance. You can solve it with the same
  bipartite BFS or with union-find, which you will meet later in the chapter.

## What to carry forward

When the cost is per *group* (a bus, a teleporter, a shared pattern), make the group the
node, index members to groups once, and mark both the group and the member visited so each
membership edge is touched once. The next problem, Jump Game IV, has the same hidden
cliques (all indices with equal value) and shows what goes wrong if you forget to retire a
group after its first use.
