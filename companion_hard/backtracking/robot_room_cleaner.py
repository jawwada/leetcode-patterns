"""
Robot Room Cleaner (LeetCode 489) - Hard
Chapter: backtracking
Pattern: Blind DFS with relative coordinates and turn-around backtrack

A robot is in an unknown grid room with open and blocked cells. It only exposes move() -> bool
(step forward if possible), turnLeft(), turnRight() and clean(). You know neither the map, your
position nor your heading. Clean every cell reachable from the start.
Example: a 5x8 room, start at row 1, col 3 facing up -> all 30 open cells connected to the start
are cleaned.
"""


# --- helpers ---
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]   # up, right, down, left: clockwise order
ROOM = [[1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]]


class Robot:
    """Grid-backed stand-in for LeetCode's robot: 1 = open, 0 = blocked; starts facing up."""
    def __init__(self, room, row, col):
        self.room = room
        self.row = row
        self.col = col
        self.heading = 0                          # index into DIRECTIONS
        self.cleaned = set()
        self.moves = 0

    def move(self):
        next_row = self.row + DIRECTIONS[self.heading][0]
        next_col = self.col + DIRECTIONS[self.heading][1]
        if 0 <= next_row < len(self.room) and 0 <= next_col < len(self.room[0]):
            if self.room[next_row][next_col] == 1:
                self.row = next_row
                self.col = next_col
                self.moves += 1
                return True
        return False

    def turnLeft(self):
        self.heading = (self.heading - 1) % 4

    def turnRight(self):
        self.heading = (self.heading + 1) % 4

    def clean(self):
        self.cleaned.add((self.row, self.col))


# --- brute force ---
def brute_force(robot):
    """DFS on relative coordinates; backtrack by walking to the start and out again. O(N^2)."""
    visited = set()
    explore(robot, 0, 0, [], visited, 0)
    return sorted(robot.cleaned)                  # returned only so the demo can print it


def face(robot, heading, wanted):
    """Turn right until the robot faces `wanted`; return the new heading."""
    while heading != wanted:
        robot.turnRight()
        heading = (heading + 1) % 4
    return heading


def walk(robot, heading, path, forward):
    """Replay the recorded moves from the start, or undo them from the end back to the start."""
    if forward:
        for step in path:
            heading = face(robot, heading, step)
            robot.move()
    else:
        for step in path[::-1]:
            heading = face(robot, heading, (step + 2) % 4)   # the opposite direction
            robot.move()
    return heading


def explore(robot, row, col, path, visited, heading):
    visited.add((row, col))
    robot.clean()
    for direction in range(4):
        next_row = row + DIRECTIONS[direction][0]
        next_col = col + DIRECTIONS[direction][1]
        if (next_row, next_col) not in visited:
            heading = face(robot, heading, direction)
            if robot.move():
                heading = explore(robot, next_row, next_col, path + [direction], visited, heading)
                heading = walk(robot, heading, path + [direction], False)   # all the way back
                heading = walk(robot, heading, path, True)                  # and out to the parent
    return heading


# --- optimal ---
def robot_room_cleaner(robot):
    """DFS; return to the parent with spin, move, spin; turn right after each try. O(N) moves."""
    visited = set()
    clean_from(robot, 0, 0, 0, visited)
    return sorted(robot.cleaned)                  # returned only so the demo can print it


def go_back(robot):
    """The parent is right behind us: spin, step onto it, spin back to the old heading."""
    robot.turnRight()
    robot.turnRight()
    robot.move()
    robot.turnRight()
    robot.turnRight()


def clean_from(robot, row, col, heading, visited):
    visited.add((row, col))
    robot.clean()
    for k in range(4):
        direction = (heading + k) % 4             # the robot is facing this way right now
        next_row = row + DIRECTIONS[direction][0]
        next_col = col + DIRECTIONS[direction][1]
        if (next_row, next_col) not in visited and robot.move():
            clean_from(robot, next_row, next_col, direction, visited)
            go_back(robot)
        robot.turnRight()                         # after four turns we face `heading` again


# --- try the brute force ---
print(len(brute_force(Robot(ROOM, 1, 3))))                          # -> 30
print(brute_force(Robot([[1]], 0, 0)))                              # -> [(0, 0)]
print(brute_force(Robot([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 0)))
# -> [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
print(len(brute_force(Robot([[1] * 10], 0, 0))))                    # -> 10


# --- try the optimal ---
print(len(robot_room_cleaner(Robot(ROOM, 1, 3))))                          # -> 30
print(robot_room_cleaner(Robot([[1]], 0, 0)))                              # -> [(0, 0)]
print(robot_room_cleaner(Robot([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 0, 0)))
# -> [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
print(len(robot_room_cleaner(Robot([[1] * 10], 0, 0))))                    # -> 10
