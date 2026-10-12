# Palindrome Linked List
*LeetCode 234 · Easy · Pattern: Find middle + reverse second half + interleave · Reading time ~6 min*

## The problem

Return True if a singly linked list reads the same forwards and backwards.

```text
Example: 1->2->2->1 returns True; 1->2 returns False.
```

## What the problem is really asking

Does the list read the same forwards and backwards? The answer is a single boolean. The follow-up asks for O(n) time and O(1) extra space, and that is what makes it interesting: a palindrome check compares the first element with the last, the second with the second-to-last, and so on, but a singly linked list can only be walked forward.

```text
  1 -> 2 -> 3 -> 2 -> 1 -> None
  |    |    |    |    |
  +----|----|----|----+   1 == 1
       +----|----+        2 == 2
            3             middle, no partner
  -> True
```

## Do it by hand first

On paper, you would fold the list in half like a strip of paper and check that the two layers match. Folding puts position 0 on top of position n-1, position 1 on top of n-2.

```text
  strip:     1  2  3  2  1
  fold at 3: 1  2  3
             1  2  <- back half, now read right-to-left
```

What your hand kept track of was *the middle* (where to fold) and *the back half in reverse order*. Those are the two subroutines: find the middle, reverse a list.

## The first honest attempt

Copy the values into an array and compare it to its reverse, or walk two indices inward. O(n) time, O(n) space.

```text
  list:  1 -> 2 -> 3 -> 2 -> 1
  array: [1, 2, 3, 2, 1]   <- every value copied
          i           j
```

The repeated work is not time here, it is memory: the array is a full second copy of the data, built only so we can index from the back. But we only ever need *the second half* backwards, and the first problem in this chapter taught us how to make a list go backwards without any copy.

## The turning point

**Claim: reversing the second half in place turns "walk the back half backwards" into an ordinary forward walk, so the palindrome test becomes a lockstep comparison of two lists.**

Two subroutines from earlier problems do it.

*Find the middle with slow and fast pointers.* Slow moves one step, fast moves two. When fast runs out, slow has covered half the distance. With the loop `while fast and fast.next`, slow stops on the exact middle for odd lengths and on the right-middle for even lengths.

*Reverse from slow onwards.* The standard three-pointer reversal. Its result `prev` is the old last node, which is the head of the back half read backwards.

Then compare: one pointer from the original head, one from `prev`, advancing together while the second pointer is not None. The second half is never longer than the first, so bounding the loop by it is safe. For odd lengths the middle node ends up at the end of both halves (the first half still links into it), so it is compared with itself, which is harmless.

## Watch it work

List `1 -> 2 -> 3 -> 2 -> 1`. Label nodes by position n0..n4 so we can track identity.

Frame 1 — find the middle, start.

```text
  n0   n1   n2   n3   n4
  1 -> 2 -> 3 -> 2 -> 1 -> None
  S
  F
```

Both pointers start at the head.

Frame 2 — find the middle, done.

```text
  round 1: S = n1, F = n2
  round 2: S = n2, F = n4    (F.next is None: stop)

  1 -> 2 -> 3 -> 2 -> 1 -> None
            S         F
```

Slow stops on the middle node n2, holding 3.

Frame 3 — reverse from slow.

```text
  first half:   1 -> 2 --+
                n0   n1  |
                         v
                         3 -> None      (n2)
                         ^
  back half:    1 -> 2 --+
                n4   n3
  first = n0   second = prev = n4
```

The links n2 -> n3 -> n4 became n4 -> n3 -> n2 -> None; n1 still points at n2, so both halves end at the middle.

Frame 4 — compare.

```text
  step  first  second  values
   1     n0     n4      1 == 1
   2     n1     n3      2 == 2
   3     n2     n2      3 == 3
   4     -      None    loop ends -> True
```

Every pair matched, and the loop stopped when the reversed half ran out.

Throughout, slow and fast together kept "slow is halfway to fast", and after the reversal both halves were plain forward lists, so a palindrome became "two lists with equal values position by position". With `1 -> 2 -> 3 -> 3 -> 1` the same steps would compare 1 == 1, then 2 against 3, and return False.

## Why it is correct

After the middle-finding loop, slow is at index floor(n/2). Reversing from there yields the back half in reverse: the k-th node visited by `second` is the node at index n-1-k. The first pointer visits index k at step k. The comparison runs for ceil(n/2) steps, covering every pair (k, n-1-k) with k < n/2, plus, for odd n, the middle compared with itself. A list is a palindrome exactly when all those pairs match, so returning False at the first mismatch and True otherwise is right.

## Cost

- **Time: O(n).** Half a pass to find the middle, half a pass to reverse, half a pass to compare.
- **Space: O(1).** A handful of pointers; the list itself is rewired.
- The array version is O(n) time and O(n) space.

## Variations you will meet

- **"Do not leave the input modified."** Reverse the back half again after comparing to restore the list. Same cost.
- **Recursive solution.** Recurse to the end and compare on the way back with a front pointer; elegant, but O(n) stack space.
- **Valid Palindrome (strings, LeetCode 125).** With random access, two pointers from both ends need no reversal; the reversal exists only because lists lack backward access.

## What to carry forward

No backward pointer? Find the middle, reverse the back half, and the back is now a front. The next problem, Reorder List, uses the very same two steps but, instead of comparing the halves, weaves them together.
