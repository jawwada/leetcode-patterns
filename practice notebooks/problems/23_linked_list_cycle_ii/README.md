# Linked List Cycle II (LeetCode 142)

**Area:** linked list · **Difficulty:** Medium · **Key operations:** slow/fast race, meeting check by identity, reset one pointer to head, same-speed walk to the entry

## Problem

Given the head of a linked list, return the node where a cycle begins, or nothing if there is no cycle. Do not modify the list and use O(1) extra space. In this script `solve(values, pos)` builds the list itself (the tail links back to index `pos`, `-1` for no cycle) and returns the **index** of the entry node, or `-1`, so the answer is easy to test.

## Example

```
values [3, 2, 0, -4], pos 1

3 -> 2 -> 0 -> -4
     ^          |
     +----------+          answer: index 1 (the node holding 2)
```

## Brute force

Walk from the head and put every node you pass into a set (by identity, not by value). The first node that is already in the set is the entry; reaching `None` means no cycle.

O(n) time, O(n) space. The wasted work is the memory: the set remembers every node only to answer "have I been here before?", and the shape of the structure (a straight tail flowing into a loop, a rho) lets two pointers answer that with arithmetic instead.

## From brute force to optimal

Two pointers, slow moving 1 step and fast moving 2, must meet inside the loop if there is one: once both are in the loop fast gains one step per move on a finite circle, so the gap shrinks to zero. If fast runs into `None` there is no loop. That replaces the set with two pointers.

The second observation turns the meeting point into a ruler. Call the tail length `a`, the loop length `c`, and say they meet `b` steps past the entry. Slow walked `a + b`, fast walked `2(a + b)`, so the difference `a + b` is a whole number of loops: `a + b = k·c`, hence `a = k·c - b`. Walking `a` more steps from the meeting point lands exactly on the entry. So reset one pointer to the head and advance both one step at a time: the head walker needs `a` steps to reach the entry, and so does the walker starting at the meeting point. They collide there.

## Intuition

Picture a running track with a straight approach road. A slow runner and a fast runner start together on the road; the fast one laps the slow one somewhere on the track. Now a new walker starts from the beginning of the road while the slow runner keeps walking from the lap point, both at the same pace. The lap point was chosen by the race so that the distance from it to the track entrance (going around) equals the length of the road, so both walkers step onto the entrance at the same moment. Phase 1 proves there is a loop; phase 2 uses the race result as a measuring stick.

## Walkthrough

`[slow]`, `[fast]`, `[ptr]` mark where each pointer stands; the tail links back to the node holding 2.

```
start   3[slow+fast] -> 2 -> 0 -> -4 -> back to 2
race    3 -> 2[slow] -> 0[fast] -> -4 -> back to 2       slow +1, fast +2
race    3 -> 2[fast] -> 0[slow] -> -4 -> back to 2       fast wrapped: -4 -> 2
race    3 -> 2 -> 0 -> -4[slow+fast] -> back to 2        slow is fast: met at index 3

reset   ptr = head, slow stays at the meeting point
walk    3[ptr] -> 2 -> 0 -> -4[slow] -> back to 2
walk    3 -> 2[ptr+slow] -> 0 -> -4 -> back to 2         ptr +1 (to 2), slow +1 (-4 -> 2)
ptr is slow at index 1: the cycle entry -> return 1
```

Check the arithmetic: tail `a = 1`, loop `c = 3`, meeting point `b = 2` steps past the entry. `a + b = 3 = 1·c`, and `a = c - b = 1`: one step from the meeting point lands on the entry.

## Steps

1. `slow = fast = head`.
2. While `fast` and `fast.next`: move `slow` one step and `fast` two; if `slow is fast`, break.
3. If the loop ended because `fast` ran off the end, there is no cycle: return `-1`.
4. `ptr = head`. While `ptr is not slow`: move both one step.
5. `ptr` (equal to `slow`) is the entry; return its index.

## Complexity

O(n) time: the race takes at most `a + c` moves and the second walk exactly `a` moves. O(1) extra space, three pointers.

## Pitfalls

- **Comparing by value.** `slow.val == fast.val` "meets" as soon as two different nodes share a value: `[1, 1, 1, 1]` with no cycle declares a meeting, and phase 2 then walks off the end and crashes. Compare nodes with `is`.
- **Forgetting `fast.next`.** `while fast:` lets `fast.next.next` read the `next` of `None` when `fast` sits on the last node; `[1]` with no cycle crashes. Fast moves two steps, so both `fast` and `fast.next` must exist.
- **Walking toward the frozen pointer.** In phase 2 `slow` keeps moving; `fast` stays parked at the meeting point. `while ptr is not fast` stops at the meeting point and reports index 3 instead of 1 in the example.
- **Checking the meeting before the first move.** `slow` and `fast` start on the same node, so a check placed before the move declares a cycle on every list. Move first, then compare.
- **Returning the meeting point as the entry.** The race proves the loop exists; the meeting point is generally not the entry (here it is index 3, the entry is index 1). The second walk is what finds it.
