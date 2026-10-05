# Find Longest Awesome Substring

*LeetCode 1542 · Hard · Pattern: Prefix parity mask + first-seen positions · Reading time ~10 min*

## The problem

A string of digits is awesome if some rearrangement of it is a palindrome, i.e. at most one digit occurs an odd number
of times. Given a digit string s, return the length of its longest awesome substring (a single character always
qualifies).

```text
Example: s = "3242415" returns 5 ("24241" rearranges to
  "24142"). Example: s = "12345678" returns 1.
```

## What the problem is really asking

You get a string of digits. A substring is **awesome** if its characters can be rearranged into a palindrome. Return the length of the longest awesome substring. A single character always qualifies, so the answer is at least 1.

First translate "can be rearranged into a palindrome" into something checkable. A palindrome pairs each character with its mirror, so every digit must occur an even number of times. The one exception is the middle character of an odd-length palindrome, which is unpaired. So:

**A substring is awesome exactly when at most one digit occurs an odd number of times in it.**

The answer is a length. The hardness: n is up to 10^5, there are about 5 · 10^9 substrings, and we need something close to linear.

```text
s = 3 2 4 2 4 1 5
    0 1 2 3 4 5 6   index

"24241" = s[1..5]: 2 x2, 4 x2, 1 x1
          one odd digit -> awesome, rearranges to 24142
length 5 is the best
```

## Do it by hand first

Pick a fixed start and extend to the right, keeping a tally of odd/even for each digit as you go. Ignore the actual counts and track only whether each one is odd.

```text
start at index 1 ("2..."):
  add 2 -> odd {2}          one odd   ok  len 1
  add 4 -> odd {2,4}        two odd   no
  add 2 -> odd {4}          one odd   ok  len 3
  add 4 -> odd {}           none odd  ok  len 4
  add 1 -> odd {1}          one odd   ok  len 5
  add 5 -> odd {1,5}        two odd   no
```

What your hand kept track of was a **set of digits with odd count**. Each new character toggles one digit in or out of that set. There are only 10 digits, so the set is a 10-bit mask, and "toggle digit d" is `mask ^= 1 << d`. That is the XOR-as-parity reading from Single Number, with ten columns instead of 32.

## The first honest attempt

For every start `i`, extend `j` to the right, maintaining ten counts (or one parity mask), and record `j - i + 1` whenever at most one digit is odd.

```text
start 0: 3 | 32 | 324 | 3242 | 32424 | ...
start 1:     2  | 24  | 242  | 2424  | ...
start 2:          4   | 42   | 424   | ...
            the parities of "24" and "242" are
            recomputed from scratch for each start
```

That is O(n²) substrings and O(n² · 10) work for the count version, about 10^11 at n = 10^5. Too slow.

The waste: the parity of `s[i..j]` is a fixed function of two prefix states, the one at `i` and the one at `j`. Yet we rebuild it by walking from `i` every time.

A natural second attempt is a sliding window: grow the right end, and shrink the left end while the window is not awesome. It fails because awesomeness is not monotone. In the hand trace above, "24" is not awesome but "242" and "2424" are. Adding characters can repair a bad window, so a two-pointer scheme that drops the left end as soon as the window turns bad throws away windows that would have recovered. When a property can come back after breaking, sliding windows are the wrong tool, and prefix states usually are the right one.

## The turning point

**Claim: if `M[k]` is the parity mask of the prefix `s[:k]`, then the parity mask of `s[i:j]` is `M[j] ^ M[i]`.**

That is prefix sums with XOR in place of addition. The prefix up to `j` is the prefix up to `i` followed by the substring. Each digit's parity in the long prefix is its parity in the short prefix, flipped once for each occurrence in the substring. XOR-ing out the short prefix leaves the substring's parities.

```text
prefix masks (columns d5 d4 d3 d2 d1; d0, d6-d9 stay 0)

 k   prefix     M[k]
 0   ""         0 0 0 0 0
 1   3          0 0 1 0 0
 2   32         0 0 1 1 0
 3   324        0 1 1 1 0
 4   3242       0 1 1 0 0
 5   32424      0 0 1 0 0
 6   324241     0 0 1 0 1

 s[1:6] = "24241":  M[6] ^ M[1] = 0 0 0 0 1   one bit -> ok
```

So "substring `s[i:j]` is awesome" becomes "`M[i]` and `M[j]` differ in at most one bit". For a fixed right end `j`, the compatible left masks are:

- `M[j]` itself (all even), or
- `M[j] ^ (1 << d)` for `d` in 0..9 (exactly digit `d` odd).

That is **11 target masks**. To maximise the length `j - i`, we want the **earliest** `i` whose prefix mask is one of the 11. So keep a dictionary `first[mask] = smallest index at which this prefix mask occurred`, and seed it with `first[0] = -1` for the empty prefix. In code, position `j` is the character index, so prefix `s[:j+1]` pairs with the stored index `i` to give a substring of length `j - i`.

Two details are load-bearing:

1. **Never overwrite** `first[mask]`. A later index can only give shorter substrings.
2. **Seed `first[0] = -1`.** Without it, a whole prefix like "32424" can never be measured, because its left partner is the empty prefix.

There are only 2^10 = 1024 possible masks, so the dictionary stays tiny no matter how long the string is.

## Watch it work

`s = "3242415"`. Masks are shown as columns d5 d4 d3 d2 d1. `first` maps each mask to its earliest index.

```text
Frame 1   seed
  mask = 00000   first = {00000:-1}   best = 0
```
The empty prefix sits at index -1 so whole prefixes can be measured.

```text
Frame 2   j=0..2  read 3, 2, 4
  j=0 mask 00100: flip d3 -> 00000 @-1  len 1
  j=1 mask 00110: flip d2 -> 00100 @0   len 1
  j=2 mask 01110: flip d4 -> 00110 @1   len 1
  first += {00100:0, 00110:1, 01110:2}  best = 1
```
Each new mask is unseen, and only one-character substrings qualify so far.

```text
Frame 3   j=3  read 2   mask 01100
  flip d2 -> 01110 @2   len 1
  flip d4 -> 00100 @0   len 3  ("242")
  first += {01100:3}                     best = 3
```
The partner at index 0 differs only in d4: "242" has 2 twice and 4 once, so 4 is the one odd digit.

```text
Frame 4   j=4  read 4   mask 00100
  same    -> 00100 @0   len 4  ("2424")
  flip d3 -> 00000 @-1  len 5  ("32424")
  flip d2 -> 00110 @1   len 3
  flip d4 -> 01100 @3   len 1
  00100 already in first: keep @0       best = 5
```
The seeded empty prefix pays off: the whole prefix "32424" has only 3 odd.

```text
Frame 5   j=5  read 1   mask 00101
  flip d1 -> 00100 @0   len 5  ("24241")
  first += {00101:5}                     best = 5
```
A second length-5 window appears; it ties, so `best` stays 5.

```text
Frame 6   j=6  read 5   mask 10101
  flip d5 -> 00101 @5   len 1
  first += {10101:6}                     best = 5
```
No partner is old enough to beat 5, so the answer is 5.

Throughout, `first` held the earliest index of every prefix mask seen so far and was never overwritten (see Frame 4). At each `j`, the 11 lookups covered every left end that could make an awesome substring ending at `j`.

## Why it is correct

**Reduction.** A substring `s[i:j]` is awesome iff `M[i] ^ M[j]` has at most one set bit. Prefix parities compose by XOR, and a palindrome rearrangement exists iff at most one digit count is odd.

**Exhaustiveness at each right end.** Fix the right end. A left prefix index `i` works iff `M[i]` is one of the 11 masks `M[j]`, `M[j] ^ (1 << d)`. For each of those masks, the best `i` is the smallest one at which that mask appeared, which is exactly what `first` stores. We consult all 11, so the best awesome substring ending at `j` is found.

**Invariant on `first`.** Before processing position `j`, `first` contains every prefix mask of `s[:k]` for `k ≤ j`, each mapped to its smallest such index (with -1 for the empty prefix). It is seeded correctly, and after the lookups we insert the current mask only if it is absent, which preserves "smallest". The lookups happen before the insert, but that loses nothing: pairing `j` with itself would mean an empty substring.

Taking the maximum over all right ends gives the global answer.

## Cost

- Time: O(11 · n) = O(n). Eleven dictionary lookups per character.
- Space: O(2^10) = O(1024). At most 1024 distinct masks are ever stored.

You can replace the dict with a list of 1024 entries initialised to "unseen". That is faster in practice, with the same complexity.

The brute force is O(n² · 10). The win comes entirely from replacing "walk from each start" with "look up the earliest matching prefix state".

## Variations you will meet

- **Find the Longest Substring Containing Vowels in Even Counts** (LeetCode 1371): a 5-bit mask of vowel parities, and the target is only `mask` itself (all even). One lookup per position, with the same `first` dictionary.
- **Number of Wonderful Substrings** (LeetCode 1915): count the substrings with at most one odd letter instead of finding the longest. Store how many times each mask has appeared (not the first index) and add up the counts of the 11 partners.
- **Contiguous Array** (LeetCode 525) and **Subarray Sum Equals K**: the same "prefix state + earliest/count map" skeleton with sums instead of XOR. If you know one, you know the other.
- **Larger alphabets** (26 letters): the mask grows to 26 bits and the partners to 27. It is still linear, and a dictionary is now required, since 2^26 slots is too many for a list.

## What to carry forward

A palindrome rearrangement is a statement about parity. Parity of a substring is XOR of two prefix masks, so store the first index of each mask and query the 11 partners. The next problem keeps XOR but asks for its **maximum** over pairs, which needs a binary trie and a greedy walk from the top bit.
