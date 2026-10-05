# Add Two Numbers

*LeetCode 2 · Medium · Pattern: Dummy head + carry · Reading time ~8 min*

## The problem

Two non-empty linked lists store non-negative integers with digits in reverse order (342 is 2 -> 4 -> 3). Return their
sum as a linked list in the same format.

```text
Example: (2->4->3) + (5->6->4) = (7->0->8), since 342 + 465 =
  807.
```

## What the problem is really asking

Two non-negative integers are stored as chains of digits, ones digit first. The number 942 is stored as `2 -> 4 -> 9`.
Return their sum in the same format, as a new chain.

The answer is a list of digits, least significant first. What makes it worth a Medium is the bookkeeping: the lists can
have different lengths, a carry can ripple across several digits, and the sum can be one digit longer than either input.

```text
 942 stored as:  [2] -> [4] -> [9]
  65 stored as:  [5] -> [6]
1007 stored as:  [7] -> [0] -> [0] -> [1]

  ones  tens  hundreds  thousands
```

The reversed storage looks awkward until you notice it is a gift: the list starts at the ones digit, which is exactly
where addition starts.

## Do it by hand first

Write the numbers the way you did in school, right-aligned, and add column by column from the right.

```text
   carry:   1  1
            9  4  2
     +         6  5
     -------------
         1  0  0  7
```

Ones: 2 + 5 = 7, carry 0. Tens: 4 + 6 = 10, write 0, carry 1. Hundreds: 9 + (nothing) + 1 = 10, write 0, carry 1.
Thousands: nothing + nothing + 1 = 1, write 1.

Now flip the picture left to right so it matches the lists:

```text
 column:    ones  tens  hund  thou
 l1:         2     4     9     -
 l2:         5     6     -     -
 carry in:   0     0     1     1
 digit out:  7     0     0     1
```

Your hand tracked one column at a time and a single small number, the carry, which is always 0 or 1. That carry is the
only thing one column tells the next. The data structure is a cursor on each list plus one integer.

## The first honest attempt

Walk each list and rebuild the integer: `2 + 4*10 + 9*100 = 942`, `5 + 6*10 = 65`. Add them to get 1007. Then peel the
sum apart with `% 10` and `// 10` to build the answer chain. Every node is touched a constant number of times, so it is
O(m + n) time.

So why not stop there? Look at the round trip:

```text
 [2]->[4]->[9] --assemble--> 942 \
                                   +--> 1007
 [5]->[6]      --assemble-->  65 /       |
                                         | peel
                                         v
                          [7]->[0]->[0]->[1]
```

The lists are already the positional representation of the numbers. Assembling them into integers only to tear the sum
back into digits does two conversions that cancel out. In Python it works because integers are unbounded, but the lists
can be 100 digits long; in a language with 64-bit integers the assembled number overflows. The interviewer wants to see
that you can work in the representation you were given.

## The turning point

**Claim: digit i of the sum depends only on digit i of each input and the carry out of column i-1, so you can produce the
answer one node at a time while walking both lists forward.**

This is just the schoolbook rule, and the reversed storage lines it up with the direction a linked list can be walked.
At each step:

```text
 total = (l1 digit or 0) + (l2 digit or 0) + carry
 carry, digit = divmod(total, 10)
 append a new node holding digit
```

The total is at most 9 + 9 + 1 = 19, so the carry is never more than 1.

Three details turn this into a correct loop:

- **Uneven lengths.** When one list has ended, treat its digit as 0. Do not stop the loop; check each list separately and
  only advance the one that still has nodes.
- **The final carry.** If the last column produces a carry, there is one more digit to write. Make the loop condition
  `while l1 or l2 or carry` so that the carry alone keeps it running for one more round.
- **Building the output.** This is the splice skeleton from the previous problem: a dummy node and a `tail` pointer.
  The difference is that each appended node is new (`ListNode(digit)`), since the output digits are not input nodes.

## Watch it work

`l1 = 2 -> 4 -> 9`, `l2 = 5 -> 6`. Each frame shows one loop iteration: where the input cursors were, the arithmetic, and
the output chain with `tail` on its last node.

```text
Frame 1: start
 l1: [2] -> [4] -> [9]      carry = 0
 l2: [5] -> [6]
 out: [D]
      tail
```

Nothing written yet; `tail` sits on the dummy.

```text
Frame 2: 2 + 5 + 0 = 7  -> digit 7, carry 0
 l1: [4] -> [9]             carry = 0
 l2: [6]
 out: [D] -> [7]
             tail
```

Both cursors advanced; the ones digit is written.

```text
Frame 3: 4 + 6 + 0 = 10 -> digit 0, carry 1
 l1: [9]                    carry = 1
 l2: None
 out: [D] -> [7] -> [0]
                    tail
```

The first carry appears. `l2` has just run out.

```text
Frame 4: 9 + 0 + 1 = 10 -> digit 0, carry 1
 l1: None                   carry = 1
 l2: None
 out: [D] -> [7] -> [0] -> [0]
                           tail
```

`l2` contributed 0. Both inputs are now exhausted, but the carry is 1.

```text
Frame 5: 0 + 0 + 1 = 1  -> digit 1, carry 0
 out: [D] -> [7] -> [0] -> [0] -> [1] -> None
                                  tail
 return D.next  (reads 1007)
```

Only the carry kept the loop alive for this round. Now all three conditions are false and the loop stops.

Across the frames, the output chain always held the low digits of the sum, in order, and `carry` was exactly what those
columns pushed into the next one. The inputs were read once each and never modified.

## Why it is correct

Invariant at the top of each iteration, after k iterations: the output chain holds the k lowest digits of (A + B), and
`carry` equals the carry out of column k-1, which is the value of the low k digits of A plus those of B, divided by
10^k and rounded down.

It holds at k = 0: empty output, carry 0. One iteration computes column k exactly as schoolbook addition does, using
a missing digit as 0, which is what a number with fewer digits has in that column. So after it, the output has k+1
correct digits and the new carry is correct.

The loop stops only when both lists are exhausted and the carry is 0. At that point every column of A and B has been
used, nothing is carried into a higher column, so there are no more nonzero digits in the sum. No spurious leading
zero appears either: the loop runs past the longer input only to write a carry, which is 1.

## Cost

- Time: O(max(m, n)), one iteration per column, plus at most one extra for the final carry.
- Space: O(1) extra beyond the output list, which has max(m, n) or max(m, n) + 1 nodes.

The brute force is also linear in Python, but it allocates big integers and breaks under fixed-width arithmetic.

## Variations you will meet

- **Most significant digit first** (Add Two Numbers II, LeetCode 445). Now addition must start at the tail. Either
  reverse both lists first (the first problem in this chapter), add as here, and reverse the result; or push digits onto
  two stacks and pop them together, building the output by inserting at the front.
- **Add one to a number stored as a list** (Plus One Linked List). Single input, carry starts at 1. A trick: find the
  last non-9 digit, increment it, and zero everything after it.
- **Multiply two numbers as strings** (LeetCode 43). Same column thinking, but every pair of digits contributes to a
  position i + j, so you accumulate into an array first and carry at the end.
- **Subtract or compare.** Borrow replaces carry; you need to know which number is larger, which often means a length
  comparison first.

## What to carry forward

Walk both lists in lockstep with `while l1 or l2 or carry`, treat a missing node as 0, and splice new digits behind a
dummy. The next problem leaves the output alone and instead uses a second pointer as a ruler, to find a node by its
distance from the end in one pass.
