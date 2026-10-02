# Asteroid Collision

*LeetCode 735 · Medium · Pattern: Stack simulation · Reading time ~6 min*

## What the problem is really asking

Asteroids sit in a row. Each number's absolute value is its size and its sign is its direction: positive moves right,
negative moves left, all at the same speed. When two meet, the smaller one explodes; if they are the same size, both do.
Return the asteroids still alive after every collision has happened, in their original order.

The answer is a list of survivors. What makes it tricky is chain reactions: one big left-mover can plough through a whole
line of smaller right-movers, and whether it survives depends on asteroids it meets several steps later.

```text
[3, 5, -6, 4, -1]

 3->  5->  <-6   4->  <-1
       \____/          \___/  only "-> <-" pairs ever meet
 -6 destroys 5, then 3;  4 destroys -1
 survivors: [-6, 4]
```

## Do it by hand first

Which pairs can collide at all? Two asteroids moving the same way never meet. A left-mover to the left of a right-mover
moves away from it. Only a right-mover with a left-mover somewhere to its right (`-> <-`) can collide.

So read left to right and keep a row of survivors. Right-movers just join the row: nothing seen so far can hit them from
the left. When a left-mover arrives, it heads toward the row, and the first asteroid it reaches is the *last* one in the
row. If that one is a smaller right-mover, it explodes, and the left-mover keeps going to the next one.

```text
row so far: 3 5           new: -6
            3 5 <- -6     5 < 6: 5 explodes
            3 <- -6       3 < 6: 3 explodes
            -6            nothing left to hit: -6 survives
```

Your hand only ever touched the right end of the row, and it removed from there repeatedly. The row of survivors is a
stack.

## The first honest attempt

Simulate literally: scan for the first adjacent pair (positive, negative), resolve that one collision, and restart the
scan from the beginning. Stop when a full scan finds nothing.

```text
pass 1: 3 5 -6 4 -1   scan... 5,-6 collide -> 3 -6 4 -1
pass 2: 3 -6 4 -1     scan from 0 AGAIN: 3,-6 -> -6 4 -1
pass 3: -6 4 -1       scan from 0 AGAIN: 4,-1 -> -6 4
pass 4: -6 4          scan, nothing -> done
        ^^
        settled prefix re-read on every pass
```

Up to n-1 collisions, each followed by an O(n) rescan and an O(n) deletion: O(n^2). The waste is the prefix that is
already collision-free. A collision only changes what touches the spot where it happened.

## The turning point

**Claim: an arriving left-mover always hits the most recent surviving asteroid first, and only right-movers on top can
fight it.**

Why "most recent surviving"? All survivors so far lie to the left of the newcomer, and the newcomer moves left, so it
meets them from right to left, nearest first. The nearest survivor is the one added last. That is the stack top.

Why does it stop at the first non-right-mover? If the top is a left-mover, both are moving left at the same speed and
never meet; everything further down is shielded behind that left-mover. So the fight is a loop against the top:

- top is a right-mover smaller than the newcomer: pop it, keep fighting;
- top is a right-mover of equal size: pop it, and the newcomer dies too;
- top is a right-mover that is bigger: the newcomer dies, the stack is unchanged;
- stack empty or top is a left-mover: the newcomer survives and is pushed.

A right-mover never fights on arrival. It is simply pushed; any collision it is part of will be initiated later by a
left-mover arriving behind it.

This is the first **pop-while loop** in the chapter: one arrival may pop many elements. The background's amortised
argument applies directly. Each asteroid is pushed at most once and popped at most once, so the total number of loop
iterations over the whole run is at most 2n, even though a single step can do many pops.

The stack has a recognisable shape at all times: some left-movers at the bottom (they escaped everything to their left)
followed by right-movers on top (still waiting for a left-mover to come).

```text
stack shape (bottom -> top):   <- <- <-  -> -> ->
                               escaped    waiting
a new "<-" only ever fights the "->" block, from its top
```

## Watch it work

Input `[3, 5, -6, 4, -1]`. The cursor marks the asteroid being processed; the stack of survivors is drawn as a column,
top at the top.

```text
Frame 1:  [ 3  5  -6  4  -1 ]     stack
               ^                  |  5 | <- top
          3, 5 move right: push   |  3 |
```

Right-movers cannot be hit by anything to their left, so both are pushed without a fight.

```text
Frame 2:  [ 3  5  -6  4  -1 ]     stack
                  ^               |  3 | <- top
          -6 meets top 5: 5 < 6, pop 5
```

The left-mover reaches the nearest survivor, 5, which is smaller and explodes. -6 is still alive and keeps fighting.

```text
Frame 3:  [ 3  5  -6  4  -1 ]     stack
                  ^               | -6 | <- top
          -6 meets top 3: pop 3; stack empty,
          -6 survives: push
```

A second pop from the same arrival. With nothing left to hit, -6 joins the stack at the bottom of the escaped block.

```text
Frame 4:  [ 3  5  -6  4  -1 ]     stack
                      ^           |  4 | <- top
          4 moves right: push     | -6 |
```

4 moves away from -6, so no fight. It sits on top, waiting.

```text
Frame 5:  [ 3  5  -6  4  -1 ]     stack
                         ^        |  4 | <- top
          -1 meets top 4: 4 > 1,  | -6 |
          -1 explodes, no push
          end: answer [-6, 4]
```

-1 loses to the bigger right-mover and is never pushed. The scan ends; the stack, read bottom to top, is the answer
`[-6, 4]`. Throughout, the stack was always "escaped left-movers, then waiting right-movers", and no two asteroids on it
were on a collision course. (For a tie, try `[4, -4, 2]`: -4 pops 4 and dies too, leaving `[2]`.)

## Why it is correct

Invariant: after processing the first i asteroids, the stack holds exactly the asteroids among them that survive when
only those i asteroids exist, in order, and no adjacent pair on the stack is `-> <-`. It holds trivially for i = 0.

When asteroid i+1 is a right-mover, it cannot collide with anything to its left, and anything to its left that was
stable stays stable, so pushing it preserves the invariant. When it is a left-mover, it meets the survivors from the
nearest outward, and each meeting is resolved by size, exactly as the loop does. Collisions among the earlier survivors
cannot happen (the invariant says no `-> <-` pair exists among them), so the newcomer's fights are the only new events.
The loop stops precisely when the newcomer dies or when nothing it could meet remains. After the scan, the stack is the
survivor set of the whole row.

## Cost

Time O(n): each asteroid is pushed at most once and popped at most once, so the while loop runs at most 2n times in total.
Space O(n): in the worst case (everything moves right) every asteroid stays on the stack.

## Variations you will meet

- **Different speeds.** Who meets whom now depends on time, not just position. Car Fleet II (LeetCode 1776) still uses
  a stack of the cars ahead, but pops a car when it would vanish into its own fleet before you could catch it.
- **Remove adjacent duplicates (LeetCode 1047, 1209).** A newcomer cancels the top when they match; for groups of k,
  store `(char, count)` on the stack.
- **Robot collisions (LeetCode 2751).** Same stack, but the winner loses health instead of keeping its size, and you
  must report survivors in original index order, so push indices.
- **Make the string great (LeetCode 1544).** A letter and its opposite case annihilate when adjacent: the same "fight the
  top" rule with a different test.

## What to carry forward

When a newcomer interacts with its nearest survivors one at a time, let it fight the stack top in a loop; each element is
pushed and popped at most once, so the loop is O(n) overall. The next problem goes back to expressions, where `*` and `/`
reach back to fight the top term while `+` and `-` simply push.
