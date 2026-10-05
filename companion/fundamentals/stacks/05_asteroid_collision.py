"""
Asteroid Collision (LeetCode 735) - Fundamentals
Chapter: fundamentals/stacks
Key operations: push right-movers, fight the top while top > 0 and current < 0, pop the loser

Each asteroid has a size (absolute value) and a direction (sign: positive moves right). Two
asteroids moving toward each other collide: the smaller explodes, equal sizes both explode.
Asteroids moving the same way never meet. Return the survivors in order.
Example: [5, 10, -5] -> [5, 10]; [8, -8] -> []; [10, 2, -5] -> [10]
"""


# --- algorithm ---
def asteroid_collision(asteroids):
    """Stack of survivors; a left-mover fights the right-moving tops until it dies or wins."""
    stack = []
    for size in asteroids:
        alive = True
        while alive and size < 0 and len(stack) > 0 and stack[-1] > 0:   # top right, size left
            top = stack[-1]
            if top < -size:
                stack.pop()                 # the top explodes; keep fighting the next one
            elif top == -size:
                stack.pop()
                alive = False               # both explode
            else:
                alive = False               # the current asteroid explodes, the top survives
        if alive:
            stack.append(size)
    return stack


# --- try it ---
print(asteroid_collision([5, 10, -5]))        # -> [5, 10]
print(asteroid_collision([8, -8]))            # -> []
print(asteroid_collision([10, 2, -5]))        # -> [10]
print(asteroid_collision([-2, -1, 1, 2]))     # -> [-2, -1, 1, 2]
print(asteroid_collision([1, -2, -2, -2]))    # -> [-2, -2, -2]
