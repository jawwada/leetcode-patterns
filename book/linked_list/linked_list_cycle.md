# Linked List Cycle

*LeetCode 141 · Easy · Pattern: Floyd's tortoise and hare (fast/slow pointers) · Reading time ~6 min*

## What the problem is really asking

Follow `next` from the head. Either you eventually reach `None`, or you never do because some node's arrow points back to
a node you already passed. Return whether the second case happens.

The answer is yes or no. The difficulty: walking alone cannot tell a loop from a very long list, and the follow-up asks
for O(1) memory, so you may not write down where you have been.

```text
 [3] -> [2] -> [0] -> [-4]
         ^              |
         +--------------+        -4.next = node 2: True

 [1] -> [2] -> [3] -> None       reaches the end: False
```

## Do it by hand first

On paper you follow the arrows with a finger, ticking every node you touch. The moment your finger lands on
a node that already has a tick, there is a loop. If your finger falls off the end, there is none.

```text
 visit:  3   2   0  -4   2
 ticks:  v   v   v   v   v <- already ticked: cycle
```

Your hand kept a record of every node visited: a set.

## The first honest attempt

Walk the list, adding each node to a hash set. If the current node is already in the set, return True; if you reach
`None`, return False. O(n) time and O(n) space.

It is a fine first answer. The waste is in what it stores:

```text
 set after 5 steps: {3, 2, 0, -4}   (every node on the path)
 question asked:    "did we ever come back?"  (one bit)
```

To answer one bit we store the whole path, paying memory to detect a repetition that the structure reveals by itself if
we look at it differently.

## The turning point

**Claim: if two pointers walk the list, one moving one node per tick and the other two, then the fast one reaches `None`
if there is no cycle, and lands on the same node as the slow one if there is.**

No cycle: fast simply runs off the end. Cycle: draw the list as the Greek letter rho, a straight tail leading into a loop of length c. The fast pointer enters the
loop first and goes round and round. Eventually slow enters too. From that moment both are on the circle, and we can
measure the gap as "how many steps fast must take forward to reach slow". Each tick slow moves one step away from fast,
and fast moves two steps closer. Net effect: the gap shrinks by exactly 1 per tick.

```text
 gap 3 -> 2 -> 1 -> 0
```

A gap that starts below c and shrinks by exactly 1 per tick must hit 0 within c ticks, and it cannot jump past 0, because
it moves one unit at a time. Gap 0 means they are on the same node. So a meeting is guaranteed.

Two references replace the set. `while fast and fast.next` guards the double step, and `slow is fast` compares identity,
after moving, since both start on the head.

## Watch it work

List `1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7`, with 7 pointing back to 3. Tail of 2 nodes, loop of c = 5 nodes. `s` is slow,
`f` is fast; gap is the forward distance from fast to slow on the loop.

```text
Frame 1: tick 0, both on the head
 [1] -> [2] -> [3] -> [4] -> [5]
 s,f            ^             |
                |             v
               [7] <-------- [6]
```

Both start together; we do not compare yet.

```text
Frame 2: tick 1   s = 2, f = 3
 [1] -> [2] -> [3] -> [4] -> [5]
         s      f             |
                ^             v
               [7] <-------- [6]
```

Fast has already reached the loop entrance; slow is still on the tail.

```text
Frame 3: tick 2   s = 3, f = 5   gap 3 (5->6->7->3)
 [1] -> [2] -> [3] -> [4] -> [5]
                s             f
                ^             |
               [7] <-------- [6]
```

Slow enters the loop. Now both are on the circle and the chase begins.

```text
Frame 4: tick 3   s = 4, f = 7   gap 2 (7->3->4)
 [1] -> [2] -> [3] -> [4] -> [5]
                ^      s      |
                |             v
               [7] <-------- [6]
                f
```

Fast came round the back of the loop; the gap shrank by one.

```text
Frame 5: tick 4   s = 5, f = 4   gap 1 (4->5)
 [1] -> [2] -> [3] -> [4] -> [5]
                ^      f      s
                |             |
               [7] <-------- [6]
```

Fast is right behind slow.

```text
Frame 6: tick 5   s = 6, f = 6   gap 0
 [1] -> [2] -> [3] -> [4] -> [5]
                ^             |
                |             v
               [7] <-------- [6]
                             s,f
```

`slow is fast`: return True. On a straight `1 -> 2 -> 3`, fast reaches 3 after one tick, `fast.next` is `None`, and
the loop exits with False.

Once both were in the loop, the gap fell by one per tick: 3, 2, 1, 0.

## Why it is correct

No cycle: fast is strictly ahead of slow after the first move, so it cannot meet slow, and it reaches the end, so the
loop ends with False.

If there is a cycle, fast enters it within the first a ticks (a is the tail length) and never leaves. Slow enters after
exactly a ticks. At that moment the forward gap from fast to slow is some g with 0 <= g < c. Every tick reduces it by 1
modulo c, so after g more ticks it is 0 and the pointers coincide. The loop returns True. Total ticks: a + g < a + c <= n.

## Cost

- Time: O(n). Slow takes at most a + c ticks, about n, and each tick is constant work.
- Space: O(1), two references.

## Variations you will meet

- **Where does the cycle start?** The next problem: the meeting point locates the entrance with a second walk.
- **Happy Number** (LeetCode 202). There is no list, only a function "next number = sum of squares of digits". Iterating
  any function on a finite set is a linked list in disguise, so the same race detects whether you reach 1 or loop.
- **Other speeds.** Speeds 1 and 3 can circle forever: the gap shrinks by 2, so on an even loop with an odd gap it never
  hits 0. Speeds 1 and 2 always meet.

## What to carry forward

On a loop, a runner twice as fast closes the gap by one per tick and must land on the slow runner; on a line it falls off
the end. The next problem asks not whether there is a loop but where it begins, and the meeting point turns out to be a
ruler that measures exactly that.
