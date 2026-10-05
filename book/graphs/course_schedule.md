# Course Schedule

*LeetCode 207 · Medium · Pattern: Topological sort (Kahn's BFS) / cycle detection · Reading time ~8 min*

## The problem

There are numCourses courses labelled 0..n-1, and prerequisites [a, b] means course b must be taken before course a.
Return true if it is possible to finish every course, i.e. the prerequisite graph has no directed cycle.

```text
Example: numCourses=2, [[1,0]] -> true; numCourses=2,
  [[1,0],[0,1]] -> false.
```

## What the problem is really asking

There are `numCourses` courses labelled 0 to n-1. A pair `[a, b]` means "you must take b before a". Can you take every course?

Draw each pair as an arrow from the prerequisite to the course it unlocks: `[a, b]` becomes `b -> a`. Now the question is about the shape of the arrows. If the arrows ever loop back on themselves, say 1 needs 3, 3 needs 2, 2 needs 1, then none of the three can ever be taken first. If there is no loop, you can always find an order. So the answer is a single boolean: does this directed graph contain a cycle?

```text
 numCourses = 5
 prerequisites = [1,0] [2,1] [3,2] [1,3] [4,0]

 the thing:                       how it is stored:

        +-----> 4                 adj (prereq -> unlocks)
        |                           0: [1, 4]
        0 ----> 1 ----> 2           1: [2]
                ^       |           2: [3]
                |       v           3: [1]
                +------ 3           4: []
                                  indeg = [0, 2, 1, 1, 1]
```

What makes it hard is that a cycle is a global property. Looking at any one arrow tells you nothing; you have to know where the arrows lead.

## Do it by hand first

Pretend you are a student with the course catalogue. You do not think about cycles at all. You ask: which courses can I take right now? Only those with no unmet prerequisites. Here that is course 0. Take it. Now cross out its arrows: course 1 loses one of its two prerequisites, course 4 loses its only one. Course 4 is now free. Take it.

```text
 taken: 0, 4
 still waiting:
   1 needs {3}       (0 is done)
   2 needs {1}
   3 needs {2}
```

Now you are stuck. Every remaining course waits on another remaining course: 1 on 3, 3 on 2, 2 on 1. That ring is the cycle, and you found it without searching for it. You simply ran out of free courses.

What did your hand track? For each course, how many of its prerequisites are still unmet: a count that only ever goes down. And a pile of courses whose count had reached zero, waiting to be taken. That count is the in-degree from the previous problem, and the pile is a queue.

## The first honest attempt

The direct way to look for a cycle: for every course s, walk the arrows from s and see whether you can come back to s.

```text
 start 0: 0 -> 1 -> 2 -> 3 -> 1 (seen) ... 4      no return
 start 1: 1 -> 2 -> 3 -> 1                        RETURN: cycle
 (with no cycle, you would walk from 2, 3, 4 as well)
```

Each walk costs O(V + E), and there are V starting points, so O(V · (V + E)). The repeated work: the walk from 0 explored 1, 2 and 3; the walk from 1 explores 1, 2 and 3 again; the walk from 2 would explore them a third time. Every walk rediscovers the same region of the graph from scratch, and nothing learned from one start ("from here you cannot loop back to 0") helps the next.

## The turning point

**Claim: a course with in-degree 0 cannot lie on any cycle, and deleting it cannot create one; so repeatedly deleting in-degree-0 nodes removes every node exactly when the graph has no cycle.**

Why the first half: a cycle is a ring of arrows, so every node on it has at least one arrow arriving (from the node before it on the ring). In-degree 0 means no arrow arrives, so the node is not on a ring.

Why deletion is safe: removing a node and its arrows only removes arrows. It can lower in-degrees, never raise them, and it cannot make a new ring.

Why getting stuck means a cycle: suppose nodes remain and every one of them has in-degree at least 1 counting only arrows from remaining nodes. Pick any remaining node and walk an incoming arrow backwards to its source, which is also remaining. Repeat. Since there are finitely many nodes, you must eventually revisit one. That revisit closes a ring.

So the algorithm is the student's procedure made precise. This is **Kahn's algorithm**:

1. Compute `indeg[c]` for every course and build `adj[pre]`, the list of courses that `pre` unlocks.
2. Put every course with `indeg == 0` in a queue.
3. Pop a course, count it as taken, and for each course it unlocks, do `indeg -= 1`; if that hits 0, enqueue it.
4. At the end, all courses were possible iff `taken == numCourses`.

The trick that kills the brute force's waste: we never recompute who is free. A course's readiness only changes when one of its prerequisites is taken, and then exactly one counter moves by exactly one. Each arrow is processed once in total.

There is a second way to see the same thing, which you will meet in many solutions: **DFS colouring**. Give every node one of three colours: white (unvisited), grey (on the current DFS path), black (fully explored, known cycle-free). A cycle exists iff the DFS ever follows an arrow into a grey node, because grey means "an ancestor of where I am now".

```text
 DFS from 0 with colours (W white, G grey, B black)

   0:G -> 1:G -> 2:G -> 3:G -> 1 is G   => back edge, cycle
```

Black nodes are never re-entered, which is precisely the "remember what you already proved" fix for the brute force. Both methods are O(V + E). Kahn's is iterative, has no recursion-depth worry, and its pop order is a valid course order for free, which the next problem asks for.

## Watch it work

Same example. State per frame: the `indeg` array, the queue, and the count taken. Removed nodes are shown in brackets.

**Frame 1.** Initial in-degrees; only course 0 is free.

```text
 course:  0  1  2  3  4
 indeg:   0  2  1  1  1
 queue:   [0]
 taken:   0
```

**Frame 2.** Pop 0. Its arrows go to 1 and 4. Course 1 drops 2 -> 1, course 4 drops 1 -> 0 and joins the queue.

```text
 course: [0] 1  2  3  4
 indeg:   -  1  1  1  0
 queue:   [4]
 taken:   1
```

**Frame 3.** Pop 4. It unlocks nothing.

```text
 course: [0] 1  2  3 [4]
 indeg:   -  1  1  1  -
 queue:   []
 taken:   2
```

**Frame 4.** The queue is empty with three courses left, each still showing in-degree 1. Each one's remaining arrow comes from another leftover:

```text
        1 ----> 2
        ^       |
        |       v
        +------ 3          indeg 1, 1, 1 forever
```

`taken = 2 != 5`, so return false.

Across frames, the invariant was: `indeg[c]` equals the number of prerequisites of c that have not yet been taken, and the queue holds exactly the untaken courses whose count is 0. Counters only fell; nothing was ever recomputed.

## Why it is correct

Two directions.

If the graph has no cycle, every non-empty set of remaining nodes contains a node with no arrow arriving from inside the set (otherwise the backward walk above would find a cycle). That node's `indeg` is 0, so it is in the queue. So the queue is never empty while nodes remain, and every node is eventually taken: `taken == n`.

If the graph has a cycle, no node on the cycle can ever be popped first, since each has an arrow from its predecessor on the cycle that is only removed when that predecessor is popped. The first cycle node to be popped would need its predecessor popped earlier, a contradiction. So at least the cycle nodes remain, `taken < n`, and we return false.

The invariant that makes the bookkeeping right: a course enters the queue exactly once, at the moment its last prerequisite is taken.

## Cost

- Time O(V + E): every course is enqueued and popped at most once; every arrow decrements one counter once.
- Space O(V + E): the adjacency lists hold E entries, plus the in-degree array and queue.
- The brute force was O(V · (V + E)) time.

## Variations you will meet

- **Course Schedule II (LeetCode 210).** Return the order itself. Record pops; nothing else changes. It is the next problem.
- **DFS colouring version.** Same complexity, recursive. Interviewers like it because the grey state is the subtle part: a plain visited set cannot tell "on my current path" (cycle) from "finished earlier from a different branch" (fine).
- **Undirected cycle detection.** Kahn's idea does not transfer, since every undirected edge counts both ways. Use union-find or a DFS that ignores the edge back to the parent; Graph Valid Tree later in the chapter does this.
- **Parallel Courses (LeetCode 1136).** Minimum number of semesters: process the queue level by level, like BFS layers, and count the levels.

## What to carry forward

A cycle is exactly "everyone left is waiting on someone else left": peel off in-degree-0 nodes with a queue, and if you peel all of them, there is no cycle. The next problem keeps the identical loop and simply writes down the pop order, which turns the yes/no answer into an actual schedule.
