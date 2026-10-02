# Course Schedule II

*LeetCode 210 · Medium · Pattern: Topological sort (Kahn's BFS) / cycle detection · Reading time ~7 min*

## What the problem is really asking

Same catalogue as before: courses 0..n-1, and `[a, b]` means b must come before a. This time, do not just say whether it is possible. Hand back an actual order in which to take all the courses, or an empty list if a cycle makes it impossible.

The answer is a permutation of 0..n-1 with one property: for every arrow `b -> a`, b appears to the left of a. Such a permutation is called a **topological order**. Lay the nodes on a line in that order and every arrow points right.

```text
 numCourses = 6
 prerequisites = [1,0] [2,0] [3,1] [3,2] [4,3] [5,2]

 the thing:                       stored as:
          +--> 1 --+                adj
          |        v                  0: [1, 2]
          0        3 --> 4            1: [3]
          |        ^                  2: [3, 5]
          +--> 2 --+                  3: [4]
               |                      4: []
               +--> 5                 5: []
                                    indeg = [0,1,1,2,1,1]

 one topological order, every arrow pointing right:
   0   1   2   3   5   4
```

What makes it slightly harder than the yes/no version: the answer is usually not unique (`0 2 1 3 4 5` is also fine), so you must produce one that is valid, and you must be sure you never emit a course before its prerequisites.

## Do it by hand first

Do what the student did last time, but write each course down as you take it.

```text
 free now: {0}            take 0      written: 0
 free now: {1, 2}         take 1      written: 0 1
 free now: {2}            take 2      written: 0 1 2
 free now: {3, 5}         take 3      written: 0 1 2 3
 free now: {5, 4}         take 5      written: 0 1 2 3 5
 free now: {4}            take 4      written: 0 1 2 3 5 4
```

The list you wrote is the answer. Your hand tracked the same two things as before: how many unmet prerequisites each course has, and the set of courses that are free. The only new thing is the written list itself.

## The first honest attempt

The obvious loop: repeat n times, scan every untaken course, and for each one scan all prerequisite pairs to check that every prerequisite is already taken. Take the first course that passes. If a full scan finds nothing, there is a cycle.

Each round reads all E pairs for up to V courses, and there are V rounds: O(V · (V + E)) at best with a little care, worse without.

```text
 round 1: is 0 ready? scan all 6 pairs ... yes, take 0
 round 2: is 1 ready? scan all 6 pairs ... yes, take 1
 round 3: is 2 ready? scan all 6 pairs ... yes, take 2
 round 4: is 3 ready? scan all 6 pairs ... yes ...
          ^ pairs [4,3] and [5,2] were read in every round,
            though nothing they mention changed
```

The waste: after taking one course, only the courses it unlocks can change status. Everybody else's readiness is exactly what it was, yet it is recomputed.

## The turning point

**Claim: the order in which Kahn's algorithm pops courses is a topological order, because a course is pushed only after its last prerequisite has been popped.**

Readiness is a counter, and taking a course touches only its outgoing arrows. That is the Kahn loop from Course Schedule: `indeg` counts unmet prerequisites, a queue holds courses whose count is zero, and popping a course decrements exactly the counters on its arrows. Course Schedule only counted pops. Here we append each pop to `order`.

Why that list respects every arrow `b -> a`: course a's counter starts at least 1 because of this arrow, and that particular unit is removed only when b is popped. So a cannot reach zero, cannot be pushed, and cannot be popped until after b has been popped. Since `order` is the pop sequence, b is to the left of a.

And the failure case is unchanged: if a cycle exists, its courses never reach zero, `order` comes out shorter than n, and we must return `[]`. Returning the partial list is the classic bug; a partial order is not an answer.

Which valid order you get depends on the queue's tie-breaking. A FIFO queue gives a "layer by layer" order: everything free at the start, then everything those unlocked, and so on. Swap in a min-heap and you get the lexicographically smallest topological order, at a log factor. Both are accepted, which is why tests should check validity, not equality with one fixed list.

There is also a DFS route: run DFS colouring, and append each node when it turns black (all its descendants finished). That post-order list has every course after everything it unlocks, so reversing it gives a topological order. You will see this "write down when finished, then reverse" move again in Reconstruct Itinerary at the end of this stretch.

## Watch it work

Example above. State per frame: `indeg`, the queue (front on the left), and `order`. A dash marks a popped course.

**Frame 1.** Only 0 starts at zero.

```text
 course:  0  1  2  3  4  5
 indeg:   0  1  1  2  1  1
 queue:  [0]
 order:  []
```

**Frame 2.** Pop 0; arrows to 1 and 2. Both drop to 0 and are enqueued in adjacency order.

```text
 course:  0  1  2  3  4  5
 indeg:   -  0  0  2  1  1
 queue:  [1, 2]
 order:  [0]
```

**Frame 3.** Pop 1; its arrow to 3 drops 3 from 2 to 1. Not free yet: 3 still waits on 2.

```text
 indeg:   -  -  0  1  1  1
 queue:  [2]
 order:  [0, 1]
```

**Frame 4.** Pop 2; arrows to 3 and 5. Course 3 hits 0, then 5 hits 0.

```text
 indeg:   -  -  -  0  1  0
 queue:  [3, 5]
 order:  [0, 1, 2]
```

**Frame 5.** Pop 3; arrow to 4 drops it to 0. 4 joins behind 5.

```text
 indeg:   -  -  -  -  0  0
 queue:  [5, 4]
 order:  [0, 1, 2, 3]
```

**Frame 6.** Pop 5, then pop 4; neither unlocks anything. `order` has 6 entries, so return it.

```text
 queue:  []
 order:  [0, 1, 2, 3, 5, 4]       len 6 == numCourses
```

The invariant across frames: everything in `order` has all its prerequisites earlier in `order`, and each queued course has every prerequisite already in `order`. Frame 3 is the important one: a course with two prerequisites sat at count 1 until the second one was popped.

## Why it is correct

Validity: shown above, each arrow `b -> a` keeps a's counter positive until b is popped, so b precedes a in `order`.

Completeness: if the graph is acyclic, Course Schedule's argument says the queue never runs dry while courses remain, so all n courses are appended. If it has a cycle, the cycle's courses are never popped, `len(order) < n`, and returning `[]` is right because no order exists at all.

Each course is appended at most once, because it is pushed exactly once: at the moment its counter goes from 1 to 0, which happens once.

## Cost

- Time O(V + E): one push and pop per course, one decrement per arrow.
- Space O(V + E): adjacency lists, in-degree array, queue, and the output list.
- The rescanning brute force was O(V · (V + E)).

## Variations you will meet

- **Smallest order in lexicographic terms.** Use `heapq` instead of a deque. Time becomes O(E + V log V).
- **Is the order unique?** It is unique iff the queue never holds more than one course at a time. Sequence Reconstruction (LeetCode 444) asks exactly this.
- **Minimum number of semesters.** Pop the queue a whole layer at a time and count layers (Parallel Courses, LeetCode 1136). When courses have durations, you need the longest path instead; that is Parallel Courses III, two problems ahead.
- **Constraints hidden in data.** Sometimes nobody gives you the arrows. Alien Dictionary makes you dig them out of a sorted word list first.

## What to carry forward

Kahn's pop order is a topological order because a node is released only by its last prerequisite; if the order is shorter than n, return nothing. The next problem uses the exact same sort but makes you build the graph yourself, from adjacent words in an alien dictionary.
