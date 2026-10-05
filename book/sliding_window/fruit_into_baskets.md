# Fruit Into Baskets
*LeetCode 904 · Medium · Pattern: Variable-size sliding window · Reading time ~7 min*

## The problem

fruits[i] is the type of the tree at position i. You have two baskets, each holding a single type in unlimited
quantity. Starting anywhere and moving right, pick one fruit per tree until a tree's type fits neither basket. Return
the maximum fruits picked, i.e. the longest subarray with at most 2 distinct values.

```text
Example: fruits = [1,2,3,2,2] -> 4 ([2,3,2,2]).
```

## What the problem is really asking

A row of trees, each bearing one type of fruit, given as `fruits[i]`. You have two baskets; each basket holds any amount of a *single* type. You pick a starting tree and walk right, taking one fruit from every tree, and you must stop as soon as a tree's type fits neither basket. How many fruits can you collect at most?

Strip the story: you collect a contiguous stretch of trees, and the stretch may contain at most two distinct types. The answer is the **length of the longest subarray with at most 2 distinct values**. Nothing about which two types; the stretch decides that for you.

```text
index:   0  1  2  3  4  5  6
fruits:  1  2  1  3  3  2  3
        [1  2  1]                types {1,2}  length 3
                  [3  3  2  3]   types {2,3}  length 4 <- answer
            [2  1  3]            types {1,2,3}: illegal
```

## Do it by hand first

Walk the row keeping the current stretch, and tally how many of each type it holds.

```text
read 1   stretch 1           tally {1:1}            len 1
read 2   stretch 1 2         tally {1:1, 2:1}       len 2
read 1   stretch 1 2 1       tally {1:2, 2:1}       len 3
read 3   third type! drop from the left until one
         of the old types is completely gone:
         drop 1 -> {1:1, 2:1, 3:1} still three
         drop 2 -> {1:1, 3:1}  type 2 gone
         stretch 1 3                                len 2
read 3   stretch 1 3 3       tally {1:1, 3:2}       len 3
read 2   third type: drop 1 -> {3:2, 2:1}
         stretch 3 3 2                              len 3
read 3   stretch 3 3 2 3     tally {3:3, 2:1}       len 4
```

The thing your hand tracked was a tally per type. Why not just a set of types? Because when you drop a 1 from the left you need to know whether *another* 1 is still inside. Only a count tells you that.

## The first honest attempt

For every start `i`, walk right adding types to a set, stop when the set would hold three, record the length. O(n^2) time, O(1) space (the set never exceeds three).

```text
start 0:  1 2 1 | 3              stop at index 3
start 1:    2 1 | 3              stop at index 3 again
start 2:      1 3 3 | 2          stop at index 5
                ^^^
   start 1 re-walks "2 1" that start 0 already proved has
   only two types, and was doomed to stop at 3 anyway
```

As in the last two problems, each new start re-validates a stretch that the previous start already validated.

## The turning point

**Claim: "at most two distinct values" survives shrinking, so when a third type arrives we only need to advance the left edge until one type's count reaches zero, never restart.**

Justification: removing elements cannot increase the number of distinct values, so every sub-window of a legal window is legal. And if `[L, R]` is the longest legal window ending at `R`, then `[L-1, R]` has three types, so `[L-1, R+1]` does too; the best start for `R+1` is at least `L`. The left edge moves forward only.

The summary has to answer "how many distinct types are inside?" in O(1), and has to update in O(1) when one fruit enters or leaves. A count map does both:

- Entering: `count[f] += 1`.
- Leaving: `count[f] -= 1`, and if it reaches 0, delete the key.
- Distinct types inside = `len(count)`.

Deleting zero keys is not tidiness; it is what makes `len(count)` mean "distinct types in the window". Forget it and the map keeps a ghost entry with count 0, `len(count)` stays at 3, and the shrink loop eats the entire window.

```text
without delete:  {1:0, 2:1, 3:1}  len 3  -> keeps shrinking
with delete:     {2:1, 3:1}       len 2  -> legal, stop
```

Look at how the summary has evolved across the chapter. Problem 3 needed "is this character already inside?" so it used last positions. Problem 4 needed "how many bad items?" so it used one integer. This problem needs "how many distinct values?" so it uses a map from value to count. The loop around it is unchanged. When you meet a new window problem, the question to ask is: what is the smallest summary that answers the legality test in O(1) and updates in O(1)?

## Watch it work

`fruits = [1, 2, 1, 3, 3, 2, 3]`.

Frame 1

```text
 i:   0  1  2  3  4  5  6
     [1  2  1] 3  3  2  3
      L     R              count={1:2, 2:1}  best=3
```

`R` walks 0 to 2; two types, so `L` stays at 0.

Frame 2

```text
 i:   0  1  2  3  4  5  6
      1  2 [1  3] 3  2  3
            L  R           count={1:1, 3:1}  best=3
```

`R = 3` brings type 3. `L` drops a 1 (count 1, key stays) then the 2 (count 0, key deleted), landing at 2.

Frame 3

```text
 i:   0  1  2  3  4  5  6
      1  2 [1  3  3] 2  3
            L     R        count={1:1, 3:2}  best=3
```

`R = 4` adds another 3; still two keys. Length 3 ties the best.

Frame 4

```text
 i:   0  1  2  3  4  5  6
      1  2  1 [3  3  2] 3
               L     R     count={3:2, 2:1}  best=3
```

`R = 5` brings back type 2, a third key. Dropping the single 1 deletes its key at once, so `L` moves one step.

Frame 5

```text
 i:   0  1  2  3  4  5  6
      1  2  1 [3  3  2  3]
               L        R  count={3:3, 2:1}  best=4
```

`R = 6` adds a 3; the window `[3,3,2,3]` has length 4, the answer.

Across the frames the map never held more than two keys after the shrink loop, its counts always summed to the window length, and `L` only moved right.

## Why it is correct

Invariant after processing `R`: `count` holds exactly the types in `fruits[L..R]` with their multiplicities (no zero entries), `len(count) <= 2`, and `L` is the smallest start for which that holds.

The map part is maintained because every entry and exit is applied, and zero entries are deleted. For the minimality of `L`: by the claim, the best start for `R` is at least the old `L`, so beginning the scan there loses nothing; the `while` loop advances `L` only while there are three types, and stops at the first legal start. Every valid collection is some window ending at some `R`, and its length is at most the best legal length for that `R`, which we recorded.

## Cost

- Time O(n): each index enters the window once and leaves at most once; map operations are O(1).
- Space O(1): the map holds at most three keys at any instant. For general "at most k distinct" it is O(k).

## Variations you will meet

- **At most k distinct (LeetCode 340).** Change the test to `len(count) > k`. Nothing else moves.
- **Exactly k distinct, count the subarrays (LeetCode 992).** The longest-window trick does not count anything, and "exactly" is not monotone under shrinking. Use `atMost(k) - atMost(k-1)`, where each `atMost` adds `R - L + 1` per step. That is problem 10 in this chapter.
- **Return the fruits, not the count.** Track the `L` and `R` where `best` was set.
- **Tracking last positions instead of counts.** With k = 2 you can store, per type, its last index in the window; when a third type arrives, drop the type with the smaller last index and set `L` to that index plus one. It jumps like problem 3, at the cost of a scan over k keys.

## What to carry forward

Memory hook: when the rule is about distinct values, the summary is a count map, and `len(map)` is only truthful if zero counts are deleted.

The next problem, Longest Repeating Character Replacement, keeps the count map but makes legality depend on the *most frequent* letter in the window, and reveals that the window need never shrink at all.
