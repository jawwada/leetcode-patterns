# Parallel Courses III

*LeetCode 2050 · Hard · Pattern: Topological order + longest-path relaxation (Kahn) · Reading time ~10 min*

## What the problem is really asking

Courses are labelled 1..n. A relation `[prev, next]` means prev must be finished before next can start. Course c takes `time[c-1]` months. You may run any number of courses at once, as long as each one starts only after all its prerequisites have finished. What is the fewest months needed to finish everything?

The graph is guaranteed to be a DAG, so the answer always exists. It is a single number, and here is what it really is: unlimited parallelism means no course ever waits for a free slot, only for its prerequisites. So every course starts at the instant its slowest prerequisite finishes. The answer is the finish time of the last course to finish, which is the heaviest chain of courses through the graph, the **critical path**.

```text
 n = 5, time = [1, 2, 3, 4, 5]
 relations = [1,5] [2,5] [3,5] [3,4] [4,5]

 the thing (time in parentheses):     stored (0-indexed):
                                        adj
   1(1) ---------------+                 0: [4]
                       v                 1: [4]
   2(2) ------------> 5(5)               2: [4, 3]
                       ^                 3: [4]
   3(3) ---> 4(4) -----+                 4: []
     |                 ^               indeg = [0,0,0,1,4]
     +-----------------+
```

What makes it hard is that "minimum time" sounds like a shortest-path or scheduling-optimisation problem, and it is the opposite. Nothing is being chosen. The schedule is forced: start everything as early as possible. The work is computing those forced times in the right order.

## Do it by hand first

Draw it as a Gantt chart. Courses 1, 2, 3 have no prerequisites, so they start at month 0.

```text
 month: 0  1  2  3  4  5  6  7  8  9  10 11 12
 c1     [==]  0->1
 c2     [=====]  0->2
 c3     [========]  0->3
 c4              [===========]  3->7
 c5                          [==============]  7->12
```

Course 4 needs only course 3, so it starts at 3 and ends at 3 + 4 = 7. Course 5 needs 1, 2, 3 and 4. Those finish at 1, 2, 3 and 7. The slowest is 7, so course 5 runs from 7 to 12. The answer is 12.

What did your hand compute, for each course? One number: its finish time. And it computed it as

```text
 finish(c) = time(c) + max( finish(p) for each prerequisite p )
 finish(c) = time(c)                if c has no prerequisites
```

Crucially, you filled the chart top to bottom in an order where every prerequisite's bar was already drawn when you needed it. You could not have drawn course 5 before course 4. That order is a topological order, and the number per course is the state.

## The first honest attempt

If you do not think about order, you can still use the formula: start with `finish[c] = time[c]` for everyone, then sweep over all relations repeatedly, raising `finish[next]` to `finish[prev] + time[next]` whenever that is larger. Stop when a whole sweep changes nothing. This is Bellman-Ford adapted to longest paths, which is safe here because a DAG has no cycles to inflate forever.

A longest chain can have up to n courses, and each sweep may only push correct values one link further along it, so up to n sweeps of E relations: O(V · E).

```text
 relations in input order, sweep by sweep (finish for c1..c5):

 start:   1  2  3  4  5
 sweep 1: [1,5] c5=6  [2,5] c5=7  [3,5] c5=8
          [3,4] c4=7  [4,5] c5=12
          after:  1  2  3  7  12
 sweep 2: nothing changes -> stop
```

Here the input order happened to be friendly, so two sweeps sufficed. Reverse the relations and `[4,5]` is checked while course 4 still reads 4, so sweep 1 leaves course 5 at 9; sweep 2 fixes it to 12 and sweep 3 confirms. One extra full sweep, just to carry one value one link. In a long chain listed backwards, each sweep advances the truth by one link, and every sweep rereads every relation, including ones whose source has not changed since last time. That is the waste: relaxing an edge before its source's value is final, and then relaxing it again.

## The turning point

**Claim: if courses are processed in topological order, every prerequisite's finish time is final at the moment a course is reached, so each relation needs to be relaxed exactly once.**

Justification: a course's finish time depends only on its prerequisites' finish times. In a topological order, all of them come earlier. By induction along the order, each one was already computed exactly when we reached it. So one pass suffices, and no value is ever revised after it is used.

Which structure gives a topological order on the fly? Kahn's queue from Course Schedule II. And it gives something more: the in-degree counter tells you precisely when a course's value has become final. That is the moment its last prerequisite is popped.

So we fuse the two. Instead of each course pulling from its prerequisites, each popped course pushes into the courses it unlocks:

```text
 pop cur  (finish[cur] is final now)
 for nxt in adj[cur]:
     finish[nxt] = max(finish[nxt], finish[cur] + time[nxt])
     indeg[nxt] -= 1
     if indeg[nxt] == 0: queue.append(nxt)
```

Two details that bite:

- `finish[nxt]` starts at `time[nxt]`, which is the right value for a course with no prerequisites and a correct lower bound for everyone else. The relaxation adds `time[nxt]`, never `time[cur]` again: `finish[cur]` already contains cur's own duration.
- While `indeg[nxt] > 0`, `finish[nxt]` is provisional: some prerequisite has not pushed yet. Reading it in that state is the bug the brute force kept committing. Kahn's order guarantees nobody reads it until it is final, because nxt is only popped after its counter hits zero.

The answer is `max(finish)`, not `finish` of the last course popped. Several courses may be sinks, and the last one popped is not necessarily the slowest.

This is the general pattern of **dynamic programming over a DAG**: topological order is the order in which subproblems become solvable, and the relaxation is the recurrence. Longest path is hard in general graphs, but on a DAG it is this one linear pass.

## Watch it work

Example above, using course labels 1..5 in the drawings. State per frame: `indeg`, `finish`, and the queue (front on the left).

**Frame 1.** Initialise `finish = time`; courses 1, 2, 3 have in-degree 0.

```text
 course:   1  2  3  4  5
 indeg:    0  0  0  1  4
 finish:   1  2  3  4  5
 queue:  [1, 2, 3]
```

**Frame 2.** Pop 1 (final at 1). Relax `1 -> 5`: max(5, 1 + 5) = 6. Course 5's counter drops to 3.

```text
 indeg:    -  0  0  1  3
 finish:   1  2  3  4  6
 queue:  [2, 3]               finish[5]=6 is provisional
```

**Frame 3.** Pop 2 (final at 2). Relax `2 -> 5`: max(6, 2 + 5) = 7. Counter 3 -> 2.

```text
 indeg:    -  -  0  1  2
 finish:   1  2  3  4  7
 queue:  [3]
```

**Frame 4.** Pop 3 (final at 3). Its list is `[5, 4]`. Relax `3 -> 5`: max(7, 3 + 5) = 8, counter 2 -> 1. Relax `3 -> 4`: max(4, 3 + 4) = 7, counter 1 -> 0, so 4 is enqueued.

```text
 indeg:    -  -  -  0  1
 finish:   1  2  3  7  8
 queue:  [4]                  finish[4]=7 is final
```

**Frame 5.** Pop 4 (final at 7). Relax `4 -> 5`: max(8, 7 + 5) = 12. Counter 1 -> 0; 5 is enqueued.

```text
 indeg:    -  -  -  -  0
 finish:   1  2  3  7  12
 queue:  [5]
```

**Frame 6.** Pop 5; it unlocks nothing. Queue empty. Answer `max(finish) = 12`.

```text
 finish:   1  2  3  7  12        answer = 12
 critical path:  3 -> 4 -> 5     3 + 4 + 5 = 12
```

Across frames, every popped course's finish time never changed again, and every unpopped course's finish time was the best value delivered by the prerequisites popped so far. Course 5's value climbed 6, 7, 8, 12 as its four prerequisites reported in; only the last report, from the slowest chain, mattered.

## Why it is correct

Invariant: when a course c is popped, `finish[c]` equals the true earliest finish time of c.

Base: a course with no prerequisites is in the initial queue with `finish = time[c]`, which is its true value since it starts at 0.

Step: a course c with prerequisites is pushed only when its counter reaches 0, which happens after every prerequisite p has been popped. By the invariant each such p had its true finish when popped, and at that moment pushed `finish[p] + time[c]` into `finish[c]` through a max. So after the last one, `finish[c] = time[c] + max over p of finish[p]`, the recurrence for the true value.

Every course is popped because the graph is a DAG (Course Schedule's argument), so every finish time is computed. The project ends when the last course ends, so the answer is the maximum. No schedule can do better, because each course on the critical path genuinely cannot start before its predecessor on that path ends.

## Cost

- Time O(V + E): each course popped once, each relation relaxed once.
- Space O(V + E): adjacency lists plus three arrays of size V.
- The sweeping version was O(V · E); a memoised DFS on the reversed graph also achieves O(V + E), pulling instead of pushing.

## Variations you will meet

- **Parallel Courses (LeetCode 1136).** All durations equal 1, so the answer is the number of BFS layers in Kahn's process. Same loop, process the queue a level at a time.
- **Parallel Courses II (LeetCode 1494).** At most k courses per semester. Parallelism is now limited, the schedule is no longer forced, and topological order is not enough: it becomes bitmask DP over sets of taken courses, a different chapter.
- **Report the critical path itself.** Store, for each course, which prerequisite produced its max, then walk back from the course with the largest finish.
- **Longest path in a DAG with edge weights.** Same relaxation with `finish[cur] + w(cur, nxt)`. Replace max with min and you get single-source shortest paths in a DAG, linear time with negative weights allowed.

## What to carry forward

On a DAG, Kahn's in-degree reaching zero means "this node's value is final", so any max/min recurrence over prerequisites can be relaxed along each edge exactly once. The next problem, Sort Items by Groups, keeps the plain Kahn sort but runs it twice, at two levels at once: once over items and once over the groups that contain them.
