# Valid Palindrome
*LeetCode 125 · Easy · Pattern: Converging two pointers · Reading time ~5 min*

## What the problem is really asking

You get a string full of letters, digits, spaces and punctuation. Throw away everything that is not a letter or a digit, ignore upper versus lower case, and ask: does what is left read the same forwards and backwards? The answer is a single boolean.

The interesting part is doing it without building a cleaned copy, while junk characters sit at different positions on the two sides.

```text
s = "race a car"          (_ = space, ignored)

index:  0  1  2  3  4  5  6  7  8  9
char:   r  a  c  e  _  a  _  c  a  r
pairs:  (0,9) r=r    (1,8) a=a
        (2,7) c=c    (3,5) e!=a   -> False
```

## Do it by hand first

Take `"Taco cat!"`. Put one finger on the first character and one on the last. The right finger is on `!`, which does not count, so slide it left to `t`. Compare `T` and `t`: same letter. Move both fingers one step inward and repeat. When you hit the space, you slide past it. When the fingers meet or cross, you are done.

```text
index:  0   1   2   3   4   5   6   7   8
char:   T   a   c   o   _   c   a   t   !
        L                               R
pairs checked:  (0,7) T=t  (1,6) a=a
                (2,5) c=c  (3,3) o=o   -> True
```

What did your hands keep track of? Two positions, nothing else. You never wrote the cleaned string down. That is the seed of the algorithm: two integers walking toward each other.

## The first honest attempt

The obvious solution: build `cleaned`, the lowercased alphanumerics, and return `cleaned == cleaned[::-1]`. It is O(n) time but needs two extra strings of length up to n, and it does work it does not need. For `"race a car"` the mismatch is visible at the fourth pair, yet the brute force has already copied every character twice before it compares anything.

```text
input      "race a car"            read all 10
cleaned    "raceacar"              written 8
reversed   "racaecar"              written 8
compare    r=r a=a c=c e!=a stop   only 4 needed
```

The repeated work is structural: the reversed copy is just the cleaned copy read from the other end. Reading from the other end needs an index, not a copy.

## The turning point

**Claim: a string is a palindrome exactly when every mirror pair of kept characters matches, and those pairs can be visited by two indices moving inward from the ends.**

Why it holds: `cleaned == reversed(cleaned)` says position `k` equals position `m - 1 - k` for every `k`, where `m` is the cleaned length. The pair `(k, m - 1 - k)` is the k-th kept character from the left and the k-th kept character from the right. A left index that skips junk visits the kept characters left to right; a right index that skips junk visits them right to left. Advancing both by one kept character per step pairs them up exactly as the comparison does.

The filter is applied lazily: junk is a cell you walk over. That also lets the algorithm stop at the very first mismatch.

The one subtlety is the guard: `while not s[l].isalnum(): l += 1` walks off the end of `"..."`, so every skip loop must also check `l < r`. If the guard stops a skip early, comparing a character with itself is harmless.

## Watch it work

`s = "Taco cat!"`, indices 0 to 8. `_` marks the space.

Frame 1. `R` starts on `!`, which is junk, so it slides to index 7. Compare `T` and `t`, equal after lowercasing.

```text
 0   1   2   3   4   5   6   7   8
 T   a   c   o   _   c   a   t   !
 L                           R <-R
 compare s[0]='T' s[7]='t'  -> equal
```

Frame 2. Both pointers step inward. Compare `a` and `a`.

```text
 0   1   2   3   4   5   6   7   8
 T   a   c   o   _   c   a   t   !
     L                   R
 compare s[1]='a' s[6]='a'  -> equal
```

Frame 3. Inward again. Compare `c` and `c`.

```text
 0   1   2   3   4   5   6   7   8
 T   a   c   o   _   c   a   t   !
         L           R
 compare s[2]='c' s[5]='c'  -> equal
```

Frame 4. `L = 3` is on `o`. `R = 4` is the space, so it slides left; the `l < r` guard stops it at 3. The middle character is compared with itself. Then `L = 4`, `R = 2`, the pointers have crossed, and the answer is True.

```text
 0   1   2   3   4   5   6   7   8
 T   a   c   o   _   c   a   t   !
             L  <-R
             R
 compare s[3]='o' s[3]='o'  -> equal, then L > R: True
```

Across every frame, everything left of `L` and right of `R` was junk or already matched with its mirror.

## Why it is correct

Invariant before each comparison: the kept characters strictly left of `L` and strictly right of `R` form matching mirror pairs, and there are the same number of them on each side.

Initially both regions are empty. Skipping junk does not change the kept characters in either region. If the kept characters at `L` and `R` match, moving both inward adds one matched pair. If they differ, a mirror pair of the cleaned string differs, so False is correct.

When the loop exits, `L >= R`. At most one kept character remains unpaired in the middle, and a single middle character mirrors itself. So every mirror pair has been checked and matched, and True is correct.

## Cost

- Time: O(n). Each index is passed over by exactly one pointer, once.
- Space: O(1). Two integers, no copies.

## Variations you will meet

- **Valid Palindrome II (LeetCode 680)**: you may delete at most one character. On the first mismatch, try two sub-checks: skip `L` or skip `R`, each with the same two-pointer walk on the remaining range. Still O(n), because only one branch point is allowed.
- **Palindrome Linked List (LeetCode 234)**: you cannot index from the end. Find the middle with fast/slow pointers (Geometry 3), reverse the second half, then compare with two forward pointers.
- **Longest Palindromic Substring (LeetCode 5)**: pointers start in the middle and expand outward instead of converging. Same mirror comparison, opposite direction.

## What to carry forward

Two indices walking inward can replace "compare with the reversed copy", and junk is just a cell the pointer walks over, as long as every skip loop is guarded by `l < r`. The next problem keeps two indices but sends them the same direction: one reads, one writes.
