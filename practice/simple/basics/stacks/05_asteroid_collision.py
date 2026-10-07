"""
Asteroid Collision (basics: stacks)
Return the surviving asteroids: + flies right, - flies left; when two meet the smaller explodes.
  [10, 2, -5]  ->  [10]

Idea: only a left-mover that comes after a right-mover can crash. Keep the survivors on a stack;
      a new left-mover fights the right-moving top until it explodes or nothing is left to hit.

Pseudocode:
  stack = []
  for a in asteroids:
      alive = True
      while alive and a < 0 and stack is not empty and top > 0:   # head-on
          if top < -a: pop                       # top explodes, a flies on
          elif top == -a: pop; alive = False     # same size: both explode
          else: alive = False                    # a explodes
      if alive: push a
  return stack

Time O(n) (each asteroid is pushed and popped at most once), space O(n).
"""


def asteroid_collision(asteroids):
    stack = []                           # survivors so far, left to right
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:  # head-on collision
            top = stack[-1]
            if top < -a:                 # top is smaller: it explodes
                stack.pop()
            elif top == -a:              # same size: both explode
                stack.pop()
                alive = False
            else:                        # a is smaller: it explodes
                alive = False
        if alive:
            stack.append(a)
    return stack


if __name__ == "__main__":
    print(asteroid_collision([5, 10, -5]))     # [5, 10]
    print(asteroid_collision([8, -8]))         # []
    print(asteroid_collision([10, 2, -5]))     # [10]
    print(asteroid_collision([-2, -1, 1, 2]))  # [-2, -1, 1, 2]
