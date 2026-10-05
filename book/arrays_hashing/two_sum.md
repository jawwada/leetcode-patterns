# Two Sum

*LeetCode 1 · Easy · Pattern: Hash map complement lookup · Reading time ~5 min*

## The problem

Given an integer array nums and an integer target, return the indices of the two numbers that add up to target.
Exactly one answer exists and you may not use the same element twice.

```text
Example: nums = [2, 7, 11, 15], target = 9 returns [0, 1]
  because 2 + 7 = 9.
```

## What the problem is really asking

You get an unsorted list of integers and a target. Exactly two of the numbers add up to the target; return their
positions. You may not use one element twice, and there is exactly one answer.

The answer is a pair of indices, not values, so sorting is out: it scrambles the positions you must report. The
difficulty is purely speed: checking pairs is obvious, and there are a lot of pairs.

```text
target = 10
index:   0   1   2   3
nums:  [ 3,  8,  5,  2 ]
             ^       ^
             8   +   2  = 10   -> answer [1, 3]
```

## Do it by hand first

Read the numbers aloud with target 10. "3: I would need a 7. Haven't seen one. 8: I'd need a 2. No. 5: I'd
need another 5. Only this one, and I can't reuse it. 2: I'd need an 8. Yes, I saw an 8 back at position 1."

Notice what your head did. For each number it turned the question "which pair works?" into a single, specific wish: "I
need exactly `10 - v`". Then it searched its memory of what had gone by. The thing you kept track of was a little list of
"numbers I've seen, and where". That list is the seed of the data structure.

```text
reading   wish (10 - v)   memory before reading
  3           7           {}
  8           2           {3}
  5           5           {3, 8}
  2           8           {3, 8, 5}   <- 8 is there
```

## The first honest attempt

Try every pair: for each `i`, look at every `j > i` and test `nums[i] + nums[j] == target`. Return the first hit.

This is O(n^2) time and O(1) space: about fifty million pair checks at `n = 10^4`.

Where is the waste? Fix `i`. You already know the one value that could pair with `nums[i]`: it is `target - nums[i]`. Yet
the inner loop reads the entire suffix to find it, comparing against values that cannot possibly be the answer.

```text
i=0 wants 7:   [3] 8  5  2     scan 8, 5, 2
i=1 wants 2:    3 [8] 5  2     scan 5, 2
i=2 wants 5:    3  8 [5] 2     scan 2
                      ^^^^ the same tail, read again and
                           again, each time for ONE known value
```

## The turning point

Claim: the inner loop is not a search over pairs; it is a membership question, "is the value `target - v` present, and at
which index?"

That is the value-to-position lookup that arrays are bad at and hash maps are good at. Keep a dict `seen` from value to index. Then the inner loop collapses to a single O(1)
check: `target - v in seen`.

Do we need a separate pass to build the dict first? No. Consider any valid pair `(i, j)` with `i < j`. When
the loop reaches `j`, element `i` has already gone by. If we have been inserting everything we pass, `nums[i]` is in the
dict, and the check at `j` finds it. So every pair is discovered by its second member, and one pass suffices.

The order of the two actions at each step matters. Check first, then insert. If you insert `v` before checking, then when
`v` is exactly half the target (here `5`, target `10`), the check finds `v` itself and you would return `[2, 2]`. Checking
first means the dict only ever contains elements strictly to the left, so self-pairing is impossible.

## Watch it work

`nums = [3, 8, 5, 2]`, `target = 10`.

Frame 1

```text
index:   0   1   2   3
nums:  [ 3,  8,  5,  2 ]
         ^ i         need = 10 - 3 = 7
seen = {}            7 not in seen -> insert 3:0
```

The dict is empty, so nothing can match. 3 goes in.

Frame 2

```text
index:   0   1   2   3
nums:  [ 3,  8,  5,  2 ]
             ^ i     need = 10 - 8 = 2
seen = {3:0}         2 not in seen -> insert 8:1
```

8 needs a 2, which has not appeared yet. 8 goes in.

Frame 3

```text
index:   0   1   2   3
nums:  [ 3,  8,  5,  2 ]
                 ^ i need = 10 - 5 = 5
seen = {3:0, 8:1}    5 not in seen -> insert 5:2
```

The tricky case: 5 needs a 5. Because we check before inserting, the dict does not yet hold this 5, so no self-pair.

Frame 4

```text
index:   0   1   2   3
nums:  [ 3,  8,  5,  2 ]
                     ^ i   need = 10 - 2 = 8
seen = {3:0, 8:1, 5:2}     8 in seen at index 1
return [seen[8], 3] = [1, 3]
```

The second member of the pair finds the first.

In every frame, `seen` held exactly the elements to the left of `i`, keyed by value. Each step did one lookup and at most
one insert.

## Why it is correct

The invariant: at the moment we examine index `i`, `seen` maps every value in `nums[0..i-1]` to some index where it
occurs. (If a value repeats, the later index overwrites the earlier one; either index is a valid partner, so that is
fine.)

Given that, at index `i` the check `target - nums[i] in seen` is true exactly when some earlier index `j < i` satisfies
`nums[j] + nums[i] == target`. So we never return a wrong pair (the partner is real and is a different, earlier index),
and we never miss the right pair: when the loop reaches the later index of the answer, the earlier one is in `seen`, and
the check fires.

## Cost

- Time: O(n). One pass; each step is an average O(1) dict lookup and insert.
- Space: O(n). In the worst case the answer is the last two elements, and `seen` holds nearly everything first.

## Variations you will meet

- **Two Sum II, input sorted.** Now order is free information. Put `L` at the start and `R` at the end; if the sum is too
  small move `L` right, too large move `R` left. O(1) space, no dict. Sorting does not lose indices because the input
  is already sorted.
- **Count all pairs, or return all pairs of values.** The dict becomes value to count; at each step add `count[target - v]`
  to the answer before incrementing `count[v]`. Same check-then-insert discipline.
- **Three sum.** Fix one element and run two sum on the rest, with two pointers on a sorted copy. O(n^2).

## What to carry forward

Turn "find a pair" into "find one specific value", then ask a dict about the past, checking before inserting. The next
problem keeps the same one-pass dict but changes what we store: not just that a value appeared, but where it appeared
most recently.
