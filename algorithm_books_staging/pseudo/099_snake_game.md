---
rank: 99
slug: snake_game
---

Design the game Snake on a grid `width` cells wide and `height` cells high. The snake starts as one cell in the top-left corner, `(0, 0)`, and food appears at the given cells one piece at a time, each only after the previous one is eaten. `move(direction)`, with direction `U`, `D`, `L` or `R`, moves the head one cell and returns the score, the number of pieces eaten; eating makes the snake one cell longer. Once the head leaves the grid or runs into the body the game is over, and every move returns `-1`. On a grid 3 wide and 2 high with food at `(1, 2)` and then `(0, 1)`, the moves `R D R U L U` return `0 0 1 1 2 -1`.

A plain list of cells costs `O(length)` per move, both to shift the body and to test whether the head hits it. Yet a move changes only the ends: a new cell appears at the head and, unless the snake eats, the cell at the tail disappears; everything in between stays put. So the body is a deque of cells with the head at the front, and a move is one push at the front and at most one pop at the back, both `O(1)`. For the collision test a set holds the same cells, which turns "is this cell part of the body?" into one lookup instead of a scan; every cell that enters or leaves the deque enters or leaves the set in the same step.

The order of the steps is the whole difficulty. Compute the new head and test the walls first. Then settle the tail: if the head lands on the next piece of food, the score rises and the tail stays, which is exactly how the snake grows; otherwise the tail leaves both the deque and the set. Only then test the head against the set. Letting the tail go before the test is what allows the head to enter the cell the tail is just leaving, as when a snake that fills a 2 × 2 board chases its own tail around it.

```text
3 wide, 2 high; H head, o body, * the food on the board, one piece at a time
start     R → 0     D → 0     R → 1     U → 1     L → 2     U → -1
H . .     . H .     . . .     . * .     . * H     . H o     the head
. . *     . . *     . H *     . o H     . . o     . . o     leaves the grid
                              eats:     the tail  eats:
                              the tail  leaves    the tail
                              stays     (1, 1)    stays
body after L, head first: [(0, 1), (0, 2), (1, 2)]; occupied holds the same

2 × 2, food (0, 1), (1, 1), (1, 0); t marks the tail
R D L → 1 2 3   U → 3                       D → -1
t o             H t                         the head goes to (1, 0), the
H o             o o                         neck, which stays: it bites
board full      the tail left (0, 0) first, itself
                so the head may move in
```

```pseudo
MOVES ← map with U → (-1, 0), D → (1, 0), L → (0, -1), R → (0, 1)

CLASS SnakeGame
    FUNCTION Init(width, height, food)
        self.width ← width
        self.height ← height
        self.food ← food                       // (row, col) cells, in order
        self.score ← 0                         // pieces eaten = next food index
        self.body ← empty deque                // head at the front
        self.body.push_back((0, 0))
        self.occupied ← empty set              // the same cells as body
        self.occupied.add((0, 0))
        self.over ← false

    FUNCTION Move(direction)
        IF self.over
            RETURN -1
        (row, col) ← self.body.front()
        (step_row, step_col) ← MOVES[direction]
        row ← row + step_row
        col ← col + step_col
        IF row < 0 OR row ≥ self.height OR col < 0 OR col ≥ self.width
            self.over ← true                   // hit a wall
            RETURN -1
        head ← (row, col)
        IF self.score < len(self.food) AND head = self.food[self.score]
            self.score ← self.score + 1        // eat: the tail stays
        ELSE
            tail ← self.body.pop_back()        // the tail leaves first, so
            self.occupied.remove(tail)         // the head may enter its cell
        IF head IN self.occupied
            self.over ← true                   // ran into its own body
            RETURN -1
        self.body.push_front(head)
        self.occupied.add(head)
        RETURN self.score
```

Each move is a constant number of deque and set operations, so `move` runs in `O(1)` time, and the two containers hold `O(length)` cells, at most `width × height`. The food needs no search either: pieces appear in order, so an index into the list, which is also the score, names the only piece on the board. Pairing an ordered container with a set of its members works wherever a sequence must also answer "is x in it?" at once, just as the LRU cache (#44) pairs its list with a map. The signals are a grid simulation with a body that grows at one end and shrinks at the other, plus fast membership tests. The classic mistake is testing the collision before letting the tail go, which kills a snake that follows its own tail; the opposite mistake, dropping the tail even when the snake eats, keeps it from ever growing.

*Practice:* LC 353 Design Snake Game · LC 348 Design Tic-Tac-Toe · LC 641 Design Circular Deque
