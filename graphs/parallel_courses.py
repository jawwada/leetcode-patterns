"""
Parallel Courses (LeetCode 1136)  — Medium
Pattern: Topological sort by layers (Kahn's BFS, one layer per round) / cycle detection

Problem
-------
numCourses courses labelled 0..numCourses-1 and prerequisites [a, b] = "b before a" (Course
Schedule's convention). In one round you may take any number of courses whose prerequisites were
all finished in earlier rounds. Put every course in the earliest round it can go and return the
rounds, each sorted ascending, or [] if a dependency cycle makes a full schedule impossible.
LeetCode 1136 asks only for the number of rounds (or -1), with relations [prev, next] labelled
from 1; minimumSemesters adapts.
Example: numCourses=6, [[4,0],[2,1],[3,0],[3,4],[5,3],[5,2]] -> [[0,1],[2,4],[3],[5]].

Brute force
-----------
Take the definition literally: each round, rescan every unplaced course and check all of its
prerequisites against the courses placed in earlier rounds; everything that passes is the round.
A scan that finds nothing while courses remain means a cycle. Scanning in ascending order makes
each round sorted for free. There are up to V rounds (a single chain), each rereading every
course and prerequisite -> O(V*(V+E)) time, O(V + E) space. The waste: a course is rechecked in
every round although only finishing one of its own prerequisites can change its answer.

From brute force to optimal
---------------------------
Readiness is a counter: waiting[c] = prerequisites of c not yet finished, and finishing a course
changes only the counters on its own arrows. That is Kahn's loop from Course Schedule II with one
change: take the queue a whole layer at a time. Finish every course in the current round; the
courses whose counter hits zero during that sweep are the next round, and they must not join the
round they were unlocked in. Each arrow is decremented once -> O(V + E), plus sorting the rounds.

Intuition
---------
A course is released by its last prerequisite, so it lands exactly one round after the latest of
them: its round is the length of the longest prerequisite chain leading into it, which is the
earliest any legal timetable allows. A plain BFS with a visited set places a course on its first
arrival, the shortest chain, which is too early (in the example it puts 3 beside 4, which 3
needs). Sorting each round makes the output depend only on the graph, never on the order of the
pairs. If fewer than numCourses courses were placed, a cycle blocked the rest: return [].

Geometric view
--------------
Draw the DAG in columns, one per round. Every arrow points strictly rightward, and each course
sits in the column right after the rightmost tail among its incoming arrows: its column index is
the longest path into it. The sweep is a vertical line moving left to right; crossing a column
cuts that column's outgoing arrows, and every node whose last incoming arrow was just cut drops
into the next column.

Steps
-----
1. Build arrows prerequisite -> [courses] and waiting[c] = number of prerequisites of c.
2. Round 0 = every course with waiting 0.
3. Sort the round and append it; for each course in it, decrement waiting for every course it
   unlocks, collecting those that hit 0 as the next round.
4. Stop at an empty round; return the rounds if all numCourses were placed, else [].

Complexity: O(V log V + E) time, O(V + E) space — each course placed once, each arrow decremented
once, and the sorts add up to O(V log V). Recording each course's round and then dropping courses
into their rounds in ascending ID order gives sorted rounds in O(V + E) with no sort at all.
Pitfalls: placing a course on its first arrival (shortest chain) instead of after its last
prerequisite; letting a course unlocked mid-round join the current round; returning the partial
timetable on a cycle; leaving rounds unsorted; LeetCode 1136's [prev, next] pairs labelled from 1.
"""
from typing import List


class Solution:
    def scheduleRounds(self, numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
        unlocks = [[] for _ in range(numCourses)]  # prerequisite -> courses waiting on it
        waiting = [0] * numCourses                 # unfinished prerequisites per course
        for course, pre in prerequisites:
            unlocks[pre].append(course)
            waiting[course] += 1
        rounds, placed = [], 0
        current = [c for c in range(numCourses) if waiting[c] == 0]
        while current:
            current.sort()  # unlock order follows the input pairs; sorting fixes it
            rounds.append(current)
            placed += len(current)
            next_round = []
            for c in current:
                for d in unlocks[c]:
                    waiting[d] -= 1
                    if waiting[d] == 0:  # its last prerequisite just finished
                        next_round.append(d)
            current = next_round
        return rounds if placed == numCourses else []

    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        # LeetCode 1136: courses 1..n, relations [prev, next]. Flip and shift, then count rounds.
        rounds = self.scheduleRounds(n, [[nxt - 1, prev - 1] for prev, nxt in relations])
        return len(rounds) if rounds else -1


def brute_force(numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
    # Each round, rescan every unplaced course and all of its prerequisites.
    needs = [[] for _ in range(numCourses)]
    for course, pre in prerequisites:
        needs[course].append(pre)
    done, rounds = set(), []
    while len(done) < numCourses:
        ready = [c for c in range(numCourses)
                 if c not in done and all(p in done for p in needs[c])]
        if not ready:
            return []
        rounds.append(ready)
        done.update(ready)
    return rounds


if __name__ == "__main__":
    s = Solution()
    cases = (
        (6, [[4, 0], [2, 1], [3, 0], [3, 4], [5, 3], [5, 2]], [[0, 1], [2, 4], [3], [5]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], [[0], [1, 2], [3]]),
        (3, [], [[0, 1, 2]]),
        (3, [[1, 0], [2, 1], [0, 2]], []),       # cycle 0 -> 1 -> 2 -> 0
        (2, [[1, 1]], []),                       # self-loop
        (2, [[1, 0], [1, 0]], [[0], [1]]),       # duplicate pair
        (4, [[1, 0], [2, 3], [3, 2]], []),       # a cycle in one part blocks everything
        (0, [], []),
    )
    for n, pre, want in cases:
        assert s.scheduleRounds(n, pre) == want, (n, pre)
        assert brute_force(n, pre) == want, (n, pre)
        assert s.scheduleRounds(n, pre[::-1]) == want  # pair order never changes the answer
    assert s.minimumSemesters(3, [[1, 3], [2, 3]]) == 2
    assert s.minimumSemesters(3, [[1, 2], [2, 3], [3, 1]]) == -1
    print("ok")
