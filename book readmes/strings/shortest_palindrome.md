# Shortest Palindrome

*LeetCode 214 · Hard · Pattern: KMP failure function (longest border) · Reading time ~10 min*

## The problem

You may add characters only in front of s; return the shortest palindrome you can form.

```text
Example: "aacecaaa" -> "aaacecaaa" (prepend "a"); "abcd" ->
  "dcbabcd" (prepend "dcb"). Equivalently: find the longest
  palindromic prefix p of s and return reverse(s[len(p):]) + s.
```

## What the problem is really asking

You may add characters only to the front of `s`. Return the shortest palindrome you can make that way. `"abcd"` becomes `"dcbabcd"`. `"aacecaaa"` becomes `"aaacecaaa"`: one `a` in front is enough.

Think about what survives. Whatever you prepend, the original `s` sits at the end of the result. The result is a palindrome, so its first `n` characters, read backwards, equal `s`. The cheapest plan keeps the longest piece at the start of `s` that is already a palindrome, call it `p`, and mirrors everything after it into the front. So the problem reduces to: **find the longest palindromic prefix of `s`**. The answer is `reverse(s[len(p):]) + s`.

```text
 s = a b a b         longest palindromic prefix: "aba"
     [a b a] b
            \_ leftover "b", mirror it in front

 answer = "b" + "abab" = "babab"
           ^ reverse of leftover
```

The answer is a string, but it is fully determined by one number: the length of that prefix. The hard part is `n` up to `5 * 10^4`, with a naive test that is quadratic.

## Do it by hand first

For `s = "abab"`, test prefixes from longest to shortest by checking whether each reads the same backwards.

```text
 "abab"  reversed "baba"   no
 "aba"   reversed "aba"    yes -> keep 3
 leftover "b" -> prepend "b" -> "babab"
```

Now look at what the check `prefix == reverse(prefix)` really compares. The reverse of a prefix of `s` is a suffix of `reverse(s)`. For `"aba"`: the last three characters of `reverse(s) = "baba"` are `"aba"`. So the hand test is: "is this prefix of `s` equal to the same-length suffix of `reverse(s)`?"

```text
 s       = a b a b
 rev(s)  = b a b a
           [a b a]  prefix of s, length 3
             [a b a] suffix of rev(s), length 3   equal
```

What your hand kept track of was an overlap between the beginning of one string and the end of another. That is a border question, and the previous problem built a machine for exactly that.

## The first honest attempt

For `L = n` down to `1`, test whether `s[:L]` is a palindrome by comparing it to its reverse. The first `L` that passes is kept.

```text
 s = a a a a b a a a        (n = 8)
 L=8 aaaabaaa: a=a a=a a=a a/b  fail (4 compares)
 L=7 aaaabaa:  a=a a=a a/b      fail (3 compares)
 L=6 aaaaba:   a=a a/b          fail (2 compares)
 L=5 aaaab:    a/b              fail (1 compare)
 L=4 aaaa:     a=a a=a          pass -> keep 4
     ^ the same leading a's re-read for every L
```

Each test is `O(L)`, so the total is `O(n^2)` in the worst case. The repeated work: the test for `L` and the test for `L - 1` compare almost the same characters, and when a test fails deep inside, nothing about where it failed is carried over to the next `L`. This is the same waste as in the brute force for the longest border: testing every candidate length independently.

## The turning point

**Claim: the longest palindromic prefix of `s` has length equal to the longest border of `t = s + "#" + reverse(s)`, where `#` is a character not in `s`.**

From the hand work, a palindromic prefix of length `L` is a prefix of `s` that equals a suffix of `reverse(s)` of the same length. In `t`, a prefix of `s` is a prefix of `t`, and a suffix of `reverse(s)` is a suffix of `t`. So a palindromic prefix of length `L` gives a border of `t` of length `L`. Conversely, a border of `t` can never contain the `#`: the `#` appears once, at position `n`, so a prefix of `t` that contained it would need a matching `#` at the same offset in the suffix, which does not exist unless the border were the whole string. So every border of `t` has length at most `n`, sits inside `s` on the left and inside `reverse(s)` on the right, and is therefore a palindromic prefix of `s`. The longest border of `t` is the answer's length.

Why the separator? Without it, `s = "aaaa"` gives `t = "aaaaaaaa"` whose longest border is 7, longer than `s` itself, meaningless as a prefix length. With `#`, `t = "aaaa#aaaa"` has longest border 4.

Now the tool. The previous problem built it; here it is again from zero, because everything below depends on it.

**The failure function.** For a string `t`, let `fail[i]` be the length of the longest proper border (a prefix that is also a suffix, not the whole thing) of `t[0..i]`. Computing it for every `i` in `O(n)` rests on two facts.

Fact 1, growth by one. A border of `t[0..i]` of length `b`, with its last character removed, is a border of `t[0..i-1]` of length `b - 1`. So the longest border at `i` is some border of the previous prefix, extended by one character. With `k` the length of a border of `t[0..i-1]`, it extends exactly when `t[i] == t[k]` (the character just after the prefix copy equals the new character after the suffix copy).

Fact 2, nested borders. If the longest border `k` of `t[0..i-1]` cannot be extended, the next shorter border of `t[0..i-1]` is the longest border of `t[0..k-1]`, which is `fail[k-1]`. Any shorter border lies inside both copies of the length-`k` border, so it is a border of that border.

```text
 extend or fall back:

 t[0..i-1]: [ border k ] ...... [ border k ] t[i]
            [b2]                       [b2]
   try: t[i] == t[k]?   yes -> fail[i] = k+1
                        no  -> k = fail[k-1] (= b2), retry
                        k=0 and no match -> fail[i] = 0
```

The loop body: `k = fail[i-1]`; while `k > 0` and `t[i] != t[k]`, set `k = fail[k-1]`; if `t[i] == t[k]`, `k += 1`; store `fail[i] = k`. The inner loop looks quadratic but is not: `k` rises by at most 1 per character and falls by at least 1 per inner iteration, never below 0, so total falls are at most total rises, at most `|t|`.

Here is the full table for our example, which is the border table you will see built frame by frame below:

```text
 t    = a b a b # b a b a
 i    = 0 1 2 3 4 5 6 7 8
 fail = 0 0 1 2 0 0 1 2 3
                        ^ fail[8] = 3: border "aba"
 [a b a] b # b [a b a]
```

So `keep = fail[-1] = 3`, the leftover is `s[3:] = "b"`, and the answer is `"b" + "abab"`.

## Watch it work

`s = "abab"`, `t = "abab#baba"`. State: `i`, the `k` chain, the table.

Frame 1. Inside `s`: `i = 1..3`.

```text
 i=1: k=0, b vs t[0]=a no      -> 0
 i=2: k=0, a vs t[0]=a yes     -> 1
 i=3: k=1, b vs t[1]=b yes     -> 2
 fail = 0 0 1 2 . . . . .
```

This part is the border table of `s` alone; `"abab"` has border `"ab"`.

Frame 2. The separator, `i = 4`.

```text
 i=4: k=2, # vs t[2]=a no; k=fail[1]=0
      # vs t[0]=a no             -> 0
 fail = 0 0 1 2 0 . . . .
```

The `#` wipes out every border; from here on any border must restart from `t[0]`.

Frame 3. `i = 5`, the first character of `reverse(s)`.

```text
 i=5: k=0, b vs t[0]=a no      -> 0
 fail = 0 0 1 2 0 0 . . .
 t    = a b a b # b
```

Frame 4. `i = 6, 7`: matching starts and grows.

```text
 i=6: k=0, a vs t[0]=a yes     -> 1
 i=7: k=1, b vs t[1]=b yes     -> 2
 fail = 0 0 1 2 0 0 1 2 .
 suffix "ab" of t matches prefix "ab"
```

Frame 5. `i = 8`, the last character.

```text
 i=8: k=2, a vs t[2]=a yes     -> 3
 fail = 0 0 1 2 0 0 1 2 3
 keep = 3: s[:3] = "aba" is a palindrome
```

Frame 6. Build the answer.

```text
 leftover = s[3:] = "b"
 answer   = reverse("b") + "abab" = "babab"
```

The invariant across frames: every filled `fail[i]` was the true longest border of `t[0..i]`, and no border ever crossed the `#`. For `"aacecaaa"` the same run ends with `fail[-1] = 7`, keeps `"aacecaa"`, and prepends `"a"`.

## Why it is correct

Two parts. First, the reduction: by the claim, the longest border of `t` equals the longest palindromic prefix of `s`; the separator bounds borders by `n` so every border corresponds to a real prefix of `s`. Second, the failure function computes the longest border of `t` correctly, by induction on `i`: the candidates for `fail[i]` are border lengths of `t[0..i-1]` plus one, those border lengths are exactly the chain `fail[i-1], fail[fail[i-1]-1], ..., 0`, and the loop tries them longest first.

Finally, optimality. Suppose `x + s` is a palindrome with `|x| = m < n`. Its last `m` characters are the end of `s`, so `x` must be their reverse; strip those matching ends off both sides and what remains in the middle is `s[:n-m]`, which must therefore be a palindrome. So `n - m` is at most the longest palindromic prefix length, i.e. `m >= n - keep`, and our answer prepends exactly `n - keep` characters.

## Cost

- Time `O(n)`: one failure-function pass over `t` of length `2n + 1`, amortised linear.
- Space `O(n)`: `t` and its table.

The brute force was `O(n^2)`.

## Variations you will meet

- **Append to the end instead.** Find the longest palindromic suffix: run the same trick on `t = reverse(s) + "#" + s`.
- **Rolling hash version.** Scan `s` keeping a forward hash and a backward hash of `s[0..i]`; when they agree, `s[0..i]` is a palindrome candidate. Linear expected time, but collisions need care.
- **Minimum insertions anywhere (LeetCode 1312).** Inserting anywhere is a different problem: `n` minus the longest palindromic subsequence, solved by interval DP.
- **KMP on a glued string, in general.** "Prefix of A equals suffix of B" is always the longest border of `A + sep + B`; the same trick finds the longest overlap when merging two strings.

## What to carry forward

To ask "which prefix of `s` is a palindrome", glue `s`, a separator, and `reverse(s)`, and read the longest border off the failure function. The next problem also matches a word against reversed words, but now across a whole dictionary, so a hash map of reversed words replaces the failure function.
