"""
Asteroid Collision (LeetCode 735) - Basics
Area: stacks
Key operations: push right-movers, fight the top while top > 0 and current < 0, pop the loser

Each asteroid has a size (absolute value) and a direction (sign: positive moves right). Two asteroids
moving toward each other collide: the smaller explodes, equal sizes both explode. Asteroids moving
the same way never meet. Return the survivors in order.
Example: [5, 10, -5] -> [5, 10]; [8, -8] -> []; [10, 2, -5] -> [10]
"""
import sys
from typing import List

VERBOSE = "--quiet" not in sys.argv


def log(*args):
    if VERBOSE:
        print(*args)


# --- brute force ---
def brute_force(asteroids: List[int]) -> List[int]:
    """Repeatedly find the leftmost adjacent pair moving toward each other and resolve it, then rescan from the start. O(n^2)."""
    a = list(asteroids)
    i = 0
    while i < len(a) - 1:
        if a[i] > 0 and a[i + 1] < 0:
            left, right = a[i], -a[i + 1]
            if left == right:
                del a[i:i + 2]
            elif left < right:
                del a[i]
            else:
                del a[i + 1]
            i = 0
        else:
            i += 1
    return a


# --- optimal ---
def solve(asteroids: List[int]) -> List[int]:
    """Stack of survivors; a left-mover fights the right-moving tops until it explodes or nothing can hit it. O(n)."""
    stack = []
    for a in asteroids:
        log(f"a={a} | stack top->bottom {stack[::-1]}")
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            top = stack[-1]
            if top < -a:
                stack.pop()
                log(f"    {a} destroys {top}; stack top->bottom {stack[::-1]}")
            elif top == -a:
                stack.pop()
                alive = False
                log(f"    {a} and {top} both explode; stack top->bottom {stack[::-1]}")
            else:
                alive = False
                log(f"    {a} explodes against {top}")
        if alive:
            stack.append(a)
            log(f"    push {a}; stack top->bottom {stack[::-1]}")
    return stack


# --- demo ---
def demo():
    return solve([5, 10, -5])


# --- tests ---
def tests():
    assert solve([5, 10, -5]) == [5, 10]
    assert solve([8, -8]) == []
    assert solve([10, 2, -5]) == [10]
    assert solve([-2, -1, 1, 2]) == [-2, -1, 1, 2]   # moving apart or same way: no collision
    assert solve([1, -2, -2, -2]) == [-2, -2, -2]
    assert solve([-5, -10]) == [-5, -10]              # two left-movers never meet
    assert solve([3, 5, -5, -4]) == [-4]              # 5 and -5 both explode; -4 then destroys 3
    assert solve([]) == []
    assert solve([7]) == [7]
    import random
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.choice([-1, 1]) * rng.randint(1, 6) for _ in range(rng.randint(0, 8))]
        assert solve(a) == brute_force(a), a


# --- bugs ---
BUGS = [
    {
        "replace": "            if top < -a:",
        "with":    "            if top <= -a:",
        "fix": "equal sizes destroy BOTH asteroids; only a strictly smaller top is destroyed alone",
        "why": "[8, -8] pops the 8 and then pushes -8, returning [-8] instead of [].",
        "decoys": [
            {"line": "        while alive and a < 0 and stack and stack[-1] > 0:", "change": "should be stack[-1] >= 0"},
            {"line": "            stack.append(a)", "change": "should append abs(a)"},
            {"line": "    return stack", "change": "should return stack[::-1]"},
        ],
    },
    {
        "replace": "        while alive and a < 0 and stack and stack[-1] > 0:",
        "with":    "        while alive and a < 0 and stack:",
        "fix": "a collision needs the top moving RIGHT (top > 0) and the current moving left; two left-movers never meet",
        "why": "[-5, -10] lets -10 'destroy' -5 because -5 < 10, returning [-10] instead of [-5, -10].",
        "decoys": [
            {"line": "            elif top == -a:", "change": "should be top == a"},
            {"line": "        alive = True", "change": "should be alive = a > 0"},
            {"line": "            top = stack[-1]", "change": "should be stack.pop()"},
        ],
    },
]

if __name__ == "__main__":
    log("--- demo ---")
    print("result:", demo())
    VERBOSE = False  # the demo above is the worked example; tests run quietly
    tests()
    print("ok")
