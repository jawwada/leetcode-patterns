# Group Shifted Strings

*LeetCode 249 · Medium · Pattern: Canonical key hashing (shift-invariant signature) · Reading time ~7 min*

## The problem

A string is shifted by moving every letter forward by the same amount with wrap-around z -> a, so 'abc' -> 'bcd' ->
... -> 'xyz' -> 'yza'. Given lowercase strings, group all strings that belong to the same shifting sequence; groups
may be returned in any order.

```text
Example: ['abc','bcd','acef','xyz','az','ba','a','z'] ->
  [['acef'], ['a','z'], ['az','ba'], ['abc','bcd','xyz']].
```

## What the problem is really asking

"Shifting" a lowercase string means moving every letter forward by the same amount, wrapping from `z` back to `a`. Shift `"abc"` by one and you get `"bcd"`; by 23 and you get `"xyz"`; by 24 and you get `"yza"`. Given a list of strings, put together every pair of strings where one can be shifted into the other. Return the groups in any order.

The answer is a partition of the input: a list of groups, each a list of strings, with every input string in exactly one group. That tells you what kind of problem this is. "Can be shifted into" is an equivalence relation (every string is a zero-shift of itself; shifting back undoes a shift; two shifts compose into one), and the groups are its equivalence classes.

```text
 input: abc  bcd  az  ba  acef  xyz  a  z

 groups:  { abc, bcd, xyz }   staircase +1 +1
          { az, ba }          one step of 25 (= -1)
          { acef }            steps +2 +2 +1
          { a, z }            no steps at all
```

The hard part is `"az"` and `"ba"`. They look unrelated, but shifting `"az"` by one gives `"ba"`: `a` goes to `b`, and `z` wraps to `a`. Any solution must see through the wrap-around.

## Do it by hand first

Take `"abc"` and `"xyz"`. How do you, by hand, convince yourself they belong together? You probably do not try all 26 shifts. You look at the shape: each letter is one more than the previous one. Write the letters as numbers (`a=0, ..., z=25`) and plot them as heights:

```text
 height
  25 |                    z
  24 |                 y
  23 |              x
     |      ...
   2 |    c
   1 |  b
   0 |a
     +--------------------------
      "abc" = 0 1 2   "xyz" = 23 24 25
      steps:  +1 +1   steps:   +1 +1
```

Same staircase, slid up. What your eye actually compared was the list of steps between neighbours, not the letters. Now `"az"`: heights 0 then 25, a step of +25. `"ba"`: heights 1 then 0, a step of -1. On a clock with 26 positions, going forward 25 is the same as going back 1. So if you measure steps around the clock, both are 25. The thing your hand kept track of is the sequence of steps, measured mod 26.

## The first honest attempt

The direct approach: keep a list of groups. For each new string, compare it with the first string (the representative) of every existing group. Two strings belong together if they have the same length and a single shift `k` works for every position: compute `k` from the first letters, `k = (b[0] - a[0]) mod 26`, then verify every other position has the same difference. If no group matches, start a new one.

Cost: for `n` strings of length `L`, each new string may be compared with up to `n` representatives at `O(L)` each, so `O(n^2 * L)` time.

```text
 new string "xyz" arrives; groups so far:
   [abc bcd]   compare xyz vs abc: k=23, check y-b, z-c  ok
   [az ba]     (length differs, skipped)
   [acef]      (length differs, skipped)

 new string "z" arrives:
   vs abc  vs az  vs acef  vs a   <- every group touched again
```

The repeated work: each comparison re-derives the shape of the representative and the shape of the newcomer, pair by pair. The representative `"abc"` has its shape recomputed every time someone is compared with it, and the newcomer's shape is recomputed for every group. The shape is a property of a single string, but we keep computing it inside a pairwise test.

## The turning point

**Claim: two strings of the same length are shifts of each other exactly when their sequences of consecutive differences, taken mod 26, are equal.**

Justify both directions. If `b` is `a` shifted by `k`, then `b[i] = a[i] + k (mod 26)` for every `i`, so `b[i+1] - b[i] = a[i+1] - a[i] (mod 26)`: the `k` cancels. Conversely, if the difference sequences agree, set `k = b[0] - a[0] (mod 26)`; then `b[0] = a[0] + k`, and since each next letter is obtained from the previous one by the same step in both strings, `b[i] = a[i] + k` follows for every `i` by induction. Note that the difference tuple also encodes the length (a string of length `L` has `L-1` differences), so equal tuples imply equal lengths.

This turns a pairwise relation into a per-string label. That is the general move for grouping by an equivalence relation: find a canonical form that every member of a class shares and no outsider has, then hash on it. A dictionary from canonical key to list of strings does the grouping in one pass, with no pairwise comparisons at all.

```text
 key(s) = tuple( (s[i+1] - s[i]) mod 26 for each i )

 "abc"  -> (1, 1)          "az" -> (25,)
 "bcd"  -> (1, 1)          "ba" -> (-1 mod 26) = (25,)
 "xyz"  -> (1, 1)          "a"  -> ()
 "acef" -> (2, 2, 1)       "z"  -> ()
```

The mod 26 is not a detail; it is the wrap-around. Without it, `"az"` gets key `(25,)` and `"ba"` gets `(-1,)`, and they split. In Python `%` already returns a value in `0..25` for a negative left operand, which is exactly what we want. Single-letter strings all get the empty tuple, and that is correct: any one letter can be shifted into any other.

An alternative canonical form, equally valid: shift every string so it starts with `a` (subtract `s[0]` from every letter mod 26) and use the resulting string as the key. Both delete the absolute offset and keep only the shape.

## Watch it work

Input `["abc","bcd","az","ba","acef","xyz","a","z"]`. State: the dictionary `groups`, key to list.

Frame 1. `"abc"` and `"bcd"` both produce `(1, 1)`.

```text
 abc: b-a=1 c-b=1 -> (1,1)
 bcd: c-b=1 d-c=1 -> (1,1)
 groups: (1,1) -> [abc, bcd]
```

The second string found the first one's bucket by hashing, not by comparison.

Frame 2. `"az"` gives 25; `"ba"` gives -1, which mod 26 is 25.

```text
 az: z-a = 25          -> (25,)
 ba: a-b = -1 -> 25    -> (25,)
 groups: (1,1)  -> [abc, bcd]
         (25,)  -> [az, ba]
```

The wrap-around pair lands in one bucket because of the mod.

Frame 3. `"acef"` opens a new bucket; `"xyz"` joins the staircase.

```text
 acef: 2, 2, 1          -> (2,2,1)
 xyz:  1, 1             -> (1,1)
 groups: (1,1)   -> [abc, bcd, xyz]
         (25,)   -> [az, ba]
         (2,2,1) -> [acef]
```

Frame 4. `"a"` and `"z"` have no neighbours, so both keys are empty.

```text
 groups: (1,1)   -> [abc, bcd, xyz]
         (25,)   -> [az, ba]
         (2,2,1) -> [acef]
         ()      -> [a, z]
 return list(groups.values())
```

Throughout, each bucket held exactly the strings seen so far that share one shape, and every string was touched once to build its key and once to insert it.

## Why it is correct

The invariant after processing the first `t` strings: for every key, the bucket contains exactly those of the first `t` strings whose difference tuple equals that key. Appending the next string to the bucket of its own key preserves this. At the end, by the claim, "same key" is the same as "shifts of each other", so the buckets are exactly the equivalence classes. Nothing is ever compared across buckets, and nothing needs to be, because strings with different keys provably cannot be shifts of one another.

## Cost

- Time `O(n * L)`: building a key reads each character once, and hashing a tuple of length `L-1` is `O(L)`.
- Space `O(n * L)`: one key per distinct shape plus the stored strings.

The brute force was `O(n^2 * L)`; the factor of `n` disappeared because the relation was replaced by a function of one string.

## Variations you will meet

- **Group Anagrams (LeetCode 49).** Same skeleton, different canonical form: sorted letters, or a 26-count tuple. Anagram equivalence ignores order, shift equivalence ignores offset; pick the form that deletes exactly what the relation ignores.
- **Isomorphic strings / word pattern.** `"egg"` and `"add"` share the pattern "first new letter, second new letter, repeat second". Canonical form: replace each letter with the index of its first occurrence, `(0,1,1)`.
- **Caesar-cipher detection with a fixed key.** If the question asks whether `b` is `a` shifted by a given `k`, skip the key and check directly; the canonical form pays off only when you must group many strings.
- **Different alphabets.** Replace 26 with the alphabet size; the argument is unchanged because it only uses arithmetic mod the size.

## What to carry forward

To group by "same up to X", compute a key that erases X and hash on it; the hard step is proving that equal keys mean equivalent strings. The next problem also chops input into fixed-shape pieces and handles each piece with a lookup table, but the pieces are digits of a number and the table spells them in English.
