"""
Robot Room Cleaner (LeetCode 489)  — Hard
Pattern: Blind DFS with relative coordinates and a constant-time turn-around backtrack

Problem
-------
A robot sits in an unknown room (grid of open and blocked cells) and exposes only four calls:
move() -> bool (step forward if possible), turnLeft(), turnRight() (90 degrees in place) and
clean(). You do not know the map, your position or your heading. Clean every reachable cell.
Example: in the room below (1 = open) starting at row 1, col 3 facing up, every 1 reachable from
the start must end up cleaned:
    1 1 1 1 1 0 1 1
    1 1 1 1 1 0 1 1
    1 0 1 1 1 1 1 1
    0 0 0 1 0 0 0 0
    1 1 1 1 1 1 1 1

Brute force
-----------
Keep your own relative coordinates (start = (0,0), heading 0 = "up") and run DFS over cells with a
visited set. Without a trick for stepping back, the natural way to return to the parent cell is to
retrace: walk the recorded path from the root in reverse to get back to the start, then replay the
parent's path. Every backtrack costs O(depth) robot commands, so a corridor of N cells costs
O(N^2) moves in total (and O(N) extra memory for the path). The waste: re-walking cells that were
already cleaned purely as transport, over and over, when the parent is always exactly one step
behind the robot.

From brute force to optimal
---------------------------
The redundancy is the long transport walk on every backtrack. Observation: when DFS enters a child
cell it is facing direction d and the parent is directly behind it, so "turn around, move, turn
around" (four commands) puts the robot back on the parent cell with its original heading; the
recursion stack is the path, no retrace needed. The second ingredient is keeping the robot's
heading in sync with the recursion: try the four directions in clockwise order starting from the
current heading and turnRight() after each attempt, so after four attempts the heading is restored
and the caller can reason about where the robot points. With a visited set of relative coordinates
each cell is entered once and each edge is traversed at most twice, so the total is O(N) commands.

Intuition
---------
You cannot see the room, but you can remember where you have been relative to where you started.
Dead-reckoning (dx, dy) plus a heading index turns the blind robot into an ordinary DFS over an
implicit grid graph. The only subtle part is physically undoing a move: the robot has to walk back,
and the cheapest walk back is the four-command turn-around because the parent is behind you.

Geometric view
--------------
Picture the DFS tree drawn on the floor: each edge is a move the robot made, the stack is the
path from the start to the robot. Entering a child = one move forward; returning = spin 180,
step, spin 180. The robot "paints" the tree edge by edge, always facing the same way after a
cell's four tries as when it arrived, so headings can be tracked as (d + k) mod 4.

Steps
-----
1. Directions clockwise: 0 up (-1,0), 1 right (0,1), 2 down (1,0), 3 left (0,-1).
2. dfs(r, c, d): mark (r,c) visited, clean().
3. For k in 0..3: nd = (d + k) % 4; if the cell ahead is unvisited and move() succeeds, dfs on it
   with heading nd, then go_back() (turn twice, move, turn twice).
4. turnRight() after each k so the heading becomes (d + k + 1) % 4; after four turns it is d again.
5. Call dfs(0, 0, 0).

Complexity: O(N) robot commands and time for N reachable cells (each cell entered once, each
entry costs at most 4 turns + 1 move + 4 for returning), O(N) space for visited + recursion.
Pitfalls: forgetting the final turnRight() so headings drift; calling move() before checking
visited (the robot then has to come back); not restoring heading after go_back (the two extra
turns matter); using absolute grid coordinates - you only have relative ones.
"""
from collections import deque
from typing import List, Set, Tuple


class Solution:
    def cleanRoom(self, robot: "Robot") -> None:
        D = ((-1, 0), (0, 1), (1, 0), (0, -1))             # up, right, down, left: clockwise
        visited: Set[Tuple[int, int]] = set()

        def go_back() -> None:                             # to the parent cell, same heading
            robot.turnRight(); robot.turnRight()
            robot.move()
            robot.turnRight(); robot.turnRight()

        def dfs(r: int, c: int, d: int) -> None:          # robot at (r, c) facing D[d]
            visited.add((r, c))
            robot.clean()
            for k in range(4):
                nd = (d + k) % 4
                nr, nc = r + D[nd][0], c + D[nd][1]
                if (nr, nc) not in visited and robot.move():
                    dfs(nr, nc, nd)
                    go_back()
                robot.turnRight()                          # now facing (d + k + 1) % 4

        dfs(0, 0, 0)


def brute_force(robot: "Robot") -> None:
    # Same DFS, but backtracking retraces the whole path to the start and replays it to the parent.
    D = ((-1, 0), (0, 1), (1, 0), (0, -1))
    visited, heading = set(), [0]

    def face(d: int) -> None:
        while heading[0] != d:
            robot.turnRight(); heading[0] = (heading[0] + 1) % 4

    def walk(path: List[int], forward: bool) -> None:    # replay the path, or undo it backwards
        for d in (path if forward else reversed(path)):
            face(d if forward else (d + 2) % 4); robot.move()

    def dfs(r: int, c: int, path: List[int]) -> None:
        visited.add((r, c)); robot.clean()
        for d, (dr, dc) in enumerate(D):
            if (r + dr, c + dc) not in visited:
                face(d)
                if robot.move():
                    dfs(r + dr, c + dc, path + [d])
                    walk(path + [d], False); walk(path, True)   # O(depth) commands per backtrack

    dfs(0, 0, [])


class Robot:
    """Grid-backed mock of LeetCode's interface: 1 = open, 0 = blocked; starts facing up."""
    def __init__(self, room: List[List[int]], row: int, col: int):
        self.room, self.r, self.c, self.d = room, row, col, 0
        self.cleaned: Set[Tuple[int, int]] = set()
        self.moves = 0

    def move(self) -> bool:
        dr, dc = ((-1, 0), (0, 1), (1, 0), (0, -1))[self.d]
        nr, nc = self.r + dr, self.c + dc
        if 0 <= nr < len(self.room) and 0 <= nc < len(self.room[0]) and self.room[nr][nc] == 1:
            self.r, self.c, self.moves = nr, nc, self.moves + 1
            return True
        return False

    def turnLeft(self) -> None:
        self.d = (self.d - 1) % 4

    def turnRight(self) -> None:
        self.d = (self.d + 1) % 4

    def clean(self) -> None:
        self.cleaned.add((self.r, self.c))


def reachable(room: List[List[int]], row: int, col: int) -> Set[Tuple[int, int]]:
    seen, q = {(row, col)}, deque([(row, col)])
    while q:
        r, c = q.popleft()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < len(room) and 0 <= nc < len(room[0]) and room[nr][nc] == 1 and (nr, nc) not in seen:
                seen.add((nr, nc)); q.append((nr, nc))
    return seen


if __name__ == "__main__":
    s = Solution()
    rooms = (
        ([[1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1, 1, 1],
          [0, 0, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]], 1, 3),
        ([[1]], 0, 0),                                              # single cell
        ([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], 0, 0),                   # corridor: brute is quadratic
        ([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 0),                  # U shape
    )
    for room, r, c in rooms:
        a, b = Robot(room, r, c), Robot(room, r, c)
        s.cleanRoom(a); brute_force(b)
        want = reachable(room, r, c)
        assert a.cleaned == want and b.cleaned == want, room
        assert a.moves <= b.moves
    corridor = Robot([[1] * 10], 0, 0); s.cleanRoom(corridor)
    assert corridor.moves == 18                                     # 9 forward + 9 back = O(N)
    print("ok")
