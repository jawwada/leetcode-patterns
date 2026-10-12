# Parallel Courses

*LeetCode 1136 · Medium · Pattern: Topological sort by layers (Kahn's BFS) / cycle detection · Reading time ~8 min*

## The problem

Courses 0..numCourses-1 and prerequisites [a, b] meaning b before a. In one round you may take any number of courses, as long as all their prerequisites were finished in earlier rounds. Put every course in the earliest round it can go and return the rounds, each sorted ascending, or an empty list if a cycle makes a full schedule impossible. LeetCode 1136 asks only how many rounds that takes, or -1.

```text
Example: numCourses=6, [[4,0],[2,1],[3,0],[3,4],[5,3],[5,2]]
  -> [[0,1],[2,4],[3],[5]]
```

## What the problem is really asking

Course Schedule II wanted one line of courses. This problem wants a timetable: every course goes into a numbered round, and a course may sit in round r only if each of its prerequisites sits in an earlier round. Of all legal timetables we want the one in which every course goes as early as it possibly can. LeetCode's version only counts the rounds; handing back the rounds themselves is the stronger answer, since the count is just its length.

```text
 numCourses = 6
 prerequisites = [4,0] [2,1] [3,0] [3,4] [5,3] [5,2]
 an arrow p ---> c means p before c

   round 0      round 1      round 2      round 3

      0 ---------> 4 ---------> 3 ---------> 5
      |                         ^            ^
      +-------------------------+            |
                                             |
      1 ---------> 2 ------------------------+
```

Read the picture column by column. 0 and 1 need nothing, so they open round 0. 4 needs only 0 and 2 needs only 1, so both go in round 1. Course 3 is the one to stare at: its arrow from 0 is short, but its arrow from 4 leaves from round 1, so 3 cannot go before round 2. Course 5 waits for 3 and lands in round 3. A course's round is the length of the longest chain of prerequisites leading into it, not the shortest.

Two more demands hide in the statement. The answer is a nested list compared by equality, so the order inside a round must be fixed; we sort each round ascending. And a cycle anywhere means some course can never be placed, so the answer is `[]`, not the part of the timetable that happened to work out.

## Do it by hand first

Tick off what is free, take all of it at once, then look at what that freed.

```text
 round 0: free {0, 1}                 take 0 and 1
 round 1: 0 freed 4, 1 freed 2        take 2 and 4
          3 lost one prerequisite, still waits on 4
 round 2: 4 freed 3                   take 3
          5 lost one prerequisite, still waits on 3
 round 3: 3 freed 5                   take 5
```

Your hand tracked two things. For each course, how many of its prerequisites are still unfinished: the same counter as in Course Schedule. And it worked a whole round at a time: everything free at the start of a round goes together, and only after the round is finished do you look at what became free. That second habit is the only new idea in this problem.

## The first honest attempt

Take the definition literally. Each round, scan every course not yet placed and check all of its prerequisites against the set of courses placed in earlier rounds; everything that passes is the round. Scanning in ascending order even hands you sorted rounds for free. If a scan finds nothing while courses remain, they are blocked by a cycle.

It is correct, and it is slow in a specific way. A chain of V courses needs V rounds, and every round rereads every remaining course and every prerequisite: O(V · (V + E)).

```text
 round 1: is 5 ready? needs 3 and 2: no
 round 2: is 5 ready? needs 3 and 2: no
 round 3: is 5 ready? needs 3 and 2: yes
          ^ 5 was re-examined every round, though its
            answer could change only when 3 or 2 finished
```

The waste is the same waste Course Schedule II removed: finishing a course can change the status only of the courses it points to. Everyone else's answer is exactly what it was a round ago.

## The turning point

**Claim: run Kahn's loop a whole layer at a time and each layer is exactly one round, because a course is released by its last prerequisite and joins the layer right after that prerequisite's layer.**

Readiness is a counter. `waiting[c]` starts as the number of prerequisites of c, and finishing a course decrements only the counters on its own arrows. The courses that start at zero are round 0. Then repeat: take the whole current round, finish every course in it, and collect the courses whose counter hits zero during that sweep. Those form the next round. They must not join the round in which they were unlocked; that is the single difference from Course Schedule II, whose queue let the layers run together.

Why each course lands in its earliest round: its counter reaches zero during the sweep of the round that holds its latest prerequisite, so it lands exactly one round after that prerequisite. No legal timetable does better, because the course must come after every one of its prerequisites, the latest included. Unrolled, a course's round is the number of courses on the longest prerequisite chain that ends just before it.

This is where the tempting shortcut breaks. A plain BFS from the free courses with a visited set places each course the first time an arrow reaches it, which measures the shortest chain. In the example, that BFS reaches 3 straight from 0 and puts it in round 1, right beside 4, which 3 needs. The counter is what makes a course wait for its last prerequisite instead of its first.

Two finishing touches complete the algorithm. Courses unlocked during a sweep come out in arrow order (in the example, finishing 0 frees 4 before finishing 1 frees 2), so sort each round before appending it; then the answer depends only on the graph, never on how the pairs were listed. And count the placed courses: no course on a cycle ever reaches zero, so the layers stop early and the count falls short of numCourses. Return `[]` then, never the partial timetable.

## Watch it work

Example above. State per frame: `waiting` for each course (a dash marks a course already finished) and the round being formed. The arrows: 0 frees 4 and 3, 1 frees 2, 2 frees 5, 3 frees 5, 4 frees 3.

**Frame 1.** Count prerequisites. Only 0 and 1 start at zero, so round 0 is [0, 1].

```text
 course:    0  1  2  3  4  5
 waiting:   0  0  1  2  1  2
 round 0:  [0, 1]
```

**Frame 2.** Finish 0: 4 drops to 0 and 3 drops to 1. Finish 1: 2 drops to 0. The sweep unlocked [4, 2], in that order; sorted, round 1 is [2, 4].

```text
 waiting:   -  -  0  1  0  2
 unlocked: [4, 2]   sorted -> round 1: [2, 4]
```

**Frame 3.** Finish 2: 5 drops to 1. Finish 4: 3 drops to 0. Round 2 is [3]: course 3 had a prerequisite in round 0 and still waited for 4.

```text
 waiting:   -  -  -  0  -  1
 round 2:  [3]
```

**Frame 4.** Finish 3: 5 drops to 0, so round 3 is [5]. Finishing 5 frees nothing, the next round is empty, and the loop stops with all six courses placed.

```text
 waiting:   -  -  -  -  -  0
 round 3:  [5]
 placed 6 == numCourses -> [[0,1],[2,4],[3],[5]]
```

The invariant across frames: every course already placed has all its prerequisites in earlier rounds, and the round being formed holds exactly the courses whose last prerequisite finished in the previous sweep.

Now close a cycle by adding `[0, 5]`, so 0 also waits on 5. The loop `0 -> 4 -> 3 -> 5 -> 0` can never start, because each course on it waits on the one before it.

```text
 waiting:   1  0  1  2  1  2     round 0: [1]
 finish 1:  2 drops to 0         round 1: [2]
 finish 2:  5 drops to 1         next round is empty
 placed 2 < 6 -> return []
```

## Why it is correct

Every round is legal. A course enters a layer only when its counter reaches zero, which happens only after each of its prerequisites was finished in an earlier sweep, so all of its prerequisites sit in earlier rounds.

Every round is the earliest. Argue round by round. A course with no prerequisites goes in round 0, the earliest there is. For any other course, assume its prerequisites already sit in their earliest rounds, and let r be the latest of those. In any legal timetable that prerequisite sits in round r or later, so the course sits in round r + 1 or later; Kahn's loop places it in exactly r + 1, because its counter hits zero during the sweep of round r.

All or nothing. If there is no cycle, Course Schedule's argument applies: while courses remain, some remaining course has no unfinished prerequisite, so no round comes out empty too early and all numCourses courses are placed. If there is a cycle, no course on it can be the first of the cycle to reach zero, the count falls short, and `[]` is right, because no timetable exists at all.

Determinism. The set of courses in each round is fixed by the graph, since it is each course's earliest round, and each round is sorted, so any listing of the same pairs gives the same output.

## Cost

- Time O(V log V + E): arrows and counters take O(V + E) to build, each course is placed once and each arrow decremented once, and the sorts add up to O(V log V) at worst, when one round holds everything.
- Space O(V + E): arrow lists, counters, and the rounds themselves.
- The rescanning brute force was O(V · (V + E)).

## Variations you will meet

- **Only the count.** LeetCode 1136 itself: return the number of rounds, or -1 for `[]`. It labels courses 1..n and writes each relation as `[prev, next]`, the reverse of Course Schedule's `[course, pre]`, so flip and shift before reusing the loop; `minimumSemesters` in the file does exactly that.
- **Sorted rounds without sorting.** Record each course's round number during the loop, then walk course IDs 0..n-1 in ascending order and drop each one into its round's list. Every round comes out sorted, and the whole thing is O(V + E).
- **At most k courses per round.** Parallel Courses II (LeetCode 1494). The timetable is no longer forced and layering is not enough; it becomes bitmask DP over sets of taken courses.
- **Courses with names.** Swap the lists for dictionaries keyed by course and sort each round by name. The loop does not change.
- **Courses that take time.** Parallel Courses III, the next problem: the round number becomes a finish time.

## What to carry forward

Take Kahn's queue a whole layer at a time and each layer is a round: a course lands one round after its last prerequisite, so its round is its longest prerequisite chain, and a visited-set BFS, which measures the shortest, places it too early. Sort each round so the answer is fixed, and return nothing if the count falls short. The next problem, Parallel Courses III, gives every course a duration: the round number becomes a finish time, and the same counter says when that time is final.
