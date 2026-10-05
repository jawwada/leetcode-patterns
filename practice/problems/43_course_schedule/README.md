# Course Schedule (LeetCode 207)

**Area:** graphs · **Difficulty:** Medium · **Key operations:** adjacency prereq -> course plus indegrees, queue the indegree-0 courses, pop and release dependents, cycle iff taken < n

## Problem

There are `n` courses `0..n-1` and a list of prerequisites `[a, b]` meaning `b` must be taken before `a`. Return `True` iff every course can be taken, i.e. the prerequisite graph has no directed cycle.

## Example

```
n = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]

    0 -> 1 -> 3
    0 -> 2 -> 3          -> True   (take 0, then 1 and 2, then 3)

n = 2, prerequisites = [[1, 0], [0, 1]]      0 <-> 1   -> False
```

## Brute force

Depth-first search with three colours: white = not visited, gray = on the current recursion path, black = finished. From every white node run the DFS; an edge that leads into a gray node closes a cycle. This is also O(V + E), so here it is less a slow method than a *different* one, used as an independent check: it is recursive (deep chains hit Python's recursion limit), path based, and it produces no order in which to take the courses. Kahn's algorithm below needs no recursion and reads a valid order straight off the queue.

## From brute force to optimal

A course with indegree 0 has no outstanding prerequisites, so it can be taken now, and taking it cannot create a cycle, only lower other indegrees. Repeatedly peel off indegree-0 courses: keep them in a queue, pop one, decrement each dependent's indegree, enqueue any that hit 0. Each edge is decremented exactly once, so the whole thing is O(V + E). If every course gets taken, the graph is acyclic. If some are left, each of them still has indegree ≥ 1, which means each is waiting on another leftover: that is only possible inside a cycle.

## Intuition

Write each course's indegree next to it: the number of prerequisites it is still waiting for. The queue holds the courses labelled 0, the ones you could register for today. Taking a course deletes it and its outgoing arrows, so every course it pointed to loses one from its label; a label that drops to 0 joins the queue. If you can keep doing this until nothing is left, the schedule works. A cycle is a ring of courses whose labels never reach 0 because each is held up by the one before it in the ring; the loop stops with them still on the board, and `taken < n` reports it.

## Walkthrough

`n = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]`. `adj` maps a prerequisite to the courses it unlocks.

```
build     adj {0: [1, 2], 1: [3], 2: [3], 3: []}
          indegree {0: 0, 1: 1, 2: 1, 3: 2}
          queue [0]                                   (the only course with indegree 0)

take 0    taken 1    queue []
  release 0 -> 1     indegree {0: 0, 1: 0, 2: 1, 3: 2}   1 hits 0 -> enqueue   queue [1]
  release 0 -> 2     indegree {0: 0, 1: 0, 2: 0, 3: 2}   2 hits 0 -> enqueue   queue [1, 2]
take 1    taken 2    queue [2]
  release 1 -> 3     indegree {0: 0, 1: 0, 2: 0, 3: 1}   still waiting on 2
take 2    taken 3    queue []
  release 2 -> 3     indegree {0: 0, 1: 0, 2: 0, 3: 0}   3 hits 0 -> enqueue   queue [3]
take 3    taken 4    queue []
          nothing to release

taken 4 == n -> True.     Order read off the queue: 0, 1, 2, 3.
```

For `n = 2, [[1, 0], [0, 1]]`: indegree `{0: 1, 1: 1}`, the queue starts empty, `taken` stays 0, `0 < 2` → `False`. Both courses are stuck with indegree 1, each waiting for the other.

## Steps

1. Build `adj[pre] -> [course, ...]` and `indeg[course] += 1` for every pair `[course, pre]`.
2. Enqueue every course with indegree 0.
3. Pop a course, `taken += 1`; for each dependent, decrement its indegree and enqueue it when it reaches 0.
4. Return `taken == n`.

## Complexity

O(V + E) time: each course is enqueued and popped once, each edge decremented once. O(V + E) space for the adjacency list, indegrees and queue.

## Pitfalls

- **Reversing the adjacency.** `[a, b]` means `b -> a`: `adj[pre].append(course)`. Reversing it while the indegrees stay as they are releases the wrong side; `n = 2, [[1, 0]]` returns `False`.
- **Decrementing the popped course.** `indeg[cur] -= 1` instead of `indeg[nxt] -= 1` means nothing new ever reaches 0 and every graph with an edge looks cyclic.
- **Counting the indegree on the prerequisite.** `indeg[pre] += 1` counts outgoing edges; courses with prerequisites then start free and real prerequisites never do.
- **Forgetting isolated courses.** They start at indegree 0, go straight into the queue and must be counted in `taken`.
- **Duplicate edges and self loops.** Kahn handles both: a duplicate adds 2 to the indegree and is decremented twice; a self loop `[0, 0]` gives course 0 an indegree it can never shed, so the answer is `False`.
