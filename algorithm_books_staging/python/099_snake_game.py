"""
Design Snake Game - A Deque for the Body, a Set for Collisions

A snake starts at cell (0, 0) of a width x height grid and food appears at the
given (row, col) cells one piece at a time; move(direction) returns the score,
or -1 once the head leaves the grid or hits the body. Grid 3 wide, 2 high,
food (1, 2) then (0, 1): moves R, D, R, U, L, U -> 0, 0, 1, 1, 2, -1.
"""
from collections import deque      # appendleft and pop are O(1)


# --- helpers ---
def play(game, moves):
    """Make each move in turn; return the list of results."""
    results = []
    for direction in moves:
        results.append(game.move(direction))
    return results


# --- algorithm ---
MOVES = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class SnakeGame:
    """The body as a deque of cells, head first, plus a set of the same cells
    for O(1) collision tests. O(1) per move."""

    def __init__(self, width, height, food):
        self.width = width
        self.height = height
        self.food = food                # (row, col) cells, eaten in this order
        self.score = 0                  # pieces eaten = index of the next one
        self.body = deque()             # head at the front, tail at the back
        self.body.append((0, 0))
        self.occupied = set()           # the same cells, for O(1) lookups
        self.occupied.add((0, 0))
        self.over = False

    def move(self, direction):
        """New head; eat or let the tail go; then test the body. O(1)."""
        if self.over:
            return -1
        row, col = self.body[0]
        step_row, step_col = MOVES[direction]
        row = row + step_row
        col = col + step_col
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            self.over = True            # hit a wall
            return -1
        head = (row, col)
        if self.score < len(self.food) and head == self.food[self.score]:
            self.score += 1             # eat: the tail stays, the snake grows
        else:
            tail = self.body.pop()      # the tail leaves first, so the head
            self.occupied.remove(tail)  # may enter the cell it just left
        if head in self.occupied:
            self.over = True            # ran into its own body
            return -1
        self.body.appendleft(head)
        self.occupied.add(head)
        return self.score


# --- try it ---
game = SnakeGame(3, 2, [(1, 2), (0, 1)])
print(play(game, "RDRUL"))              # -> [0, 0, 1, 1, 2]
print(list(game.body))                  # -> [(0, 1), (0, 2), (1, 2)]
print(game.move("U"), game.move("D"))   # -> -1 -1
board = SnakeGame(2, 2, [(0, 1), (1, 1), (1, 0)])
print(play(board, "RDLU"))              # -> [1, 2, 3, 3]
print(list(board.body))                 # -> [(0, 0), (1, 0), (1, 1), (0, 1)]
print(board.move("D"))                  # -> -1
