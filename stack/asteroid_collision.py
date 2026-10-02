"""
Asteroid Collision (LeetCode 735)  — Medium
Pattern: Stack simulation

Problem
-------
Each asteroid has a size (absolute value) and direction (positive = right, negative = left),
all moving at the same speed. When two meet the smaller explodes (both if equal). Return the
asteroids left after all collisions.
Example: [5,10,-5] -> [5,10]; [8,-8] -> []; [10,2,-5] -> [10]; [-2,-1,1,2] -> [-2,-1,1,2].

Brute force
-----------
Repeatedly scan the list for an adjacent pair (positive, negative) -- the only pair that can
collide -- resolve it, and restart the scan. O(n^2) time (up to n-1 collisions, each an O(n)
scan and delete), O(n) space. The wasted work: every restart re-reads the prefix that is
already collision-free.

From brute force to optimal
---------------------------
The redundancy is rescanning a settled prefix. Observation: a right-mover can only ever be hit
by a later left-mover, and the left-mover hits the most recent surviving right-mover first --
LIFO. So keep survivors on a stack; when a left-mover arrives, let it fight the stack top
while the top is a right-mover: pop smaller tops, stop (and die) on a larger top, and both
vanish on a tie. Left-movers and right-movers never fight each other otherwise, so everything
else is simply pushed. Each asteroid is pushed and popped at most once.

Intuition
---------
Only "-> <-" pairs collide, and the newcomer heading left meets the nearest surviving
right-mover first. A stack of survivors makes "nearest" the top.

Geometric view
--------------
Asteroids enter from the right. The stack is the lane so far. A left-mover (<-) arriving
behind a run of right-movers (->) plows into them from the right end of the run, knocking
out smaller ones until it meets one at least as big or the run ends.

Steps
-----
1. stack = [].
2. For each asteroid a: alive = True. While alive and a < 0 and stack top > 0:
   if top < |a| pop and continue; if top == |a| pop and alive = False; else alive = False.
3. If alive, push a.
4. Return stack.

Complexity: O(n) time, O(n) space — each asteroid pushed once and popped at most once.
Pitfalls: Forgetting the equal-size case destroys both; letting a left-mover fight a
left-mover on the stack; pushing a dead asteroid.
"""
from typing import List


class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for a in asteroids:
            alive = True
            # only a left-mover can hit right-movers already on the stack
            while alive and a < 0 and stack and stack[-1] > 0:
                if stack[-1] < -a:
                    stack.pop()                       # top explodes, keep fighting
                elif stack[-1] == -a:
                    stack.pop()
                    alive = False                     # both explode
                else:
                    alive = False                     # a explodes
            if alive:
                stack.append(a)
        return stack


def brute_force(asteroids: List[int]) -> List[int]:
    arr = list(asteroids)
    changed = True
    while changed:                                    # restart the scan after each collision
        changed = False
        for i in range(len(arr) - 1):
            if arr[i] > 0 and arr[i + 1] < 0:
                l, r = arr[i], -arr[i + 1]
                if l == r:
                    del arr[i:i + 2]                  # both explode
                else:
                    del arr[i + 1 if l > r else i]    # smaller one explodes
                changed = True
                break
    return arr


if __name__ == "__main__":
    s = Solution()
    cases = [[5, 10, -5], [8, -8], [10, 2, -5], [-2, -1, 1, 2], [1, -1, -2, -2], [3, 5, -6, 4, -1]]
    assert s.asteroidCollision([5, 10, -5]) == [5, 10]
    assert s.asteroidCollision([8, -8]) == []
    assert s.asteroidCollision([10, 2, -5]) == [10]
    assert s.asteroidCollision([-2, -1, 1, 2]) == [-2, -1, 1, 2]
    assert s.asteroidCollision([1, -1, -2, -2]) == [-2, -2]
    for c in cases:
        assert s.asteroidCollision(c) == brute_force(c)
    print("ok")
