---
rank: 31
slug: kahn_topological_sort
---

There are `n` courses numbered `0` to `n - 1`, and a prerequisite pair `[a, b]` means course `b` must be taken before course `a`. Return an order that takes every course, or an empty list if no order exists. With six courses and the pairs `[3, 0]`, `[3, 1]`, `[4, 3]`, `[2, 3]`, `[5, 4]`, `[5, 2]`, one valid order is `[0, 1, 3, 4, 2, 5]`.

Read each pair as an arrow `b → a`. An order is valid when every arrow points forward, which makes it a topological order of the graph. The brute force tries all `n!` orders and checks each one. Kahn's insight is that a graph without a cycle always has a free course, one with no arrow coming in. Take a free course, erase its outgoing arrows, and what remains is a smaller copy of the same problem. An indegree array makes the erasing cheap: `indegree[c]` counts the prerequisites of `c` not yet taken, taking a course subtracts one from each course it unlocks, and a course whose count reaches zero joins the queue of free courses. The queue holds exactly the courses that are free and not yet taken.

Picture the drawing eaten from the left. The courses with nothing pointing at them form its left edge; taking one erases its arrows, and any course that loses its last incoming arrow joins the new left edge. Course `3` sits behind two arrows, so it surfaces only after both `0` and `1` are taken, and `5` only after `4` and `2`. If the queue runs dry with courses left over, each of them still has an arrow coming in from another leftover course, and walking those arrows backward must eventually revisit a course. So a cycle exists, and `len(order) < num_courses` is the entire cycle test.

```text
    0 ──┐            ┌──→ 4 ──┐
        ├──→ 3 ──────┤        ├──→ 5
    1 ──┘            └──→ 2 ──┘

take   indegree of 0..5     queue     order
 -     [0, 0, 1, 2, 1, 2]   [0, 1]    []
 0     [0, 0, 1, 1, 1, 2]   [1]       [0]
 1     [0, 0, 1, 0, 1, 2]   [3]       [0, 1]
 3     [0, 0, 0, 0, 0, 2]   [4, 2]    [0, 1, 3]
 4     [0, 0, 0, 0, 0, 1]   [2]       [0, 1, 3, 4]
 2     [0, 0, 0, 0, 0, 0]   [5]       [0, 1, 3, 4, 2]
 5     [0, 0, 0, 0, 0, 0]   []        [0, 1, 3, 4, 2, 5]
```

```pseudo
FUNCTION FindOrder(num_courses, prerequisites)
    graph ← array of num_courses empty lists
    indegree ← array of num_courses zeros  // prerequisites not yet taken
    FOR EACH (course, before) IN prerequisites
        graph[before].append(course)       // [a, b] is the edge b → a
        indegree[course] ← indegree[course] + 1
    queue ← empty queue
    FOR course FROM 0 TO num_courses - 1
        IF indegree[course] = 0            // free to take right away
            queue.enqueue(course)
    order ← empty list
    WHILE queue is not empty
        course ← queue.dequeue()
        order.append(course)
        FOR EACH next_course IN graph[course]
            indegree[next_course] ← indegree[next_course] - 1    // one done
            IF indegree[next_course] = 0
                queue.enqueue(next_course)
    IF len(order) < num_courses            // the rest wait on each other
        RETURN empty list
    RETURN order
```

Each course enters the queue at most once and each arrow is erased at most once, so Kahn's algorithm runs in `O(V + E)` time and `O(V + E)` space for the graph. Reach for it whenever a problem speaks of prerequisites, dependencies, build steps or "must come before", or only asks whether an order exists at all, as Course Schedule (LC 207) does. It bends easily: processing the queue one level at a time counts the semesters in Parallel Courses (LC 1136), and in Alien Dictionary each arrow comes from the first differing letter of two adjacent words. Topological Sort with DFS (#61) builds an order from the other end. The classic mistake is reversing the pair: `[a, b]` is the arrow `b → a`, and building `a → b` instead returns an order that breaks every prerequisite.

*Practice:* LC 207 Course Schedule · LC 210 Course Schedule II · LC 269 Alien Dictionary · LC 1136 Parallel Courses
