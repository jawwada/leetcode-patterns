# Palindrome Pairs

*LeetCode 336 · Hard · Pattern: Hash map of reversed words + palindrome split · Reading time ~10 min*

## The problem

Given distinct words, return all index pairs (i, j), i != j, such that words[i] + words[j] is a palindrome.

```text
Example: ["abcd","dcba","lls","s","sssll"] ->
  [[0,1],[1,0],[3,2],[2,4]] ("abcddcba", "dcbaabcd", "slls",
  "llssssll"); ["a",""] -> [[0,1],[1,0]].
```

## What the problem is really asking

You get a list of distinct words. Return every ordered pair of indices `(i, j)`, `i != j`, such that gluing `words[i]` in front of `words[j]` gives a palindrome. Order matters: `"abcd" + "dcba"` and `"dcba" + "abcd"` are both palindromes and count as two pairs.

The answer is a set of index pairs. What makes it hard is the scale: up to 5000 words of length up to 300. There are about 25 million ordered pairs, and each check costs up to 600 character comparisons. That is too slow, so you need a way to find a word's partners without trying all of them.

```text
 words: 0 abcd  1 dcba  2 lls  3 s  4 sssll

 pairs:  (0,1) abcd|dcba   = abcddcba
         (1,0) dcba|abcd   = dcbaabcd
         (3,2) s|lls       = slls
         (2,4) lls|sssll   = llssssll
```

## Do it by hand first

Take the pair `(2, 4)`: `"lls" + "sssll" = "llssssll"`. Ask where each character of the shorter word finds its mirror image. The palindrome reads the same from both ends, so the `lls` at the front must be mirrored by `sll` at the very back. That `sll` is the tail of the longer word. What is left of the longer word, `ss`, ends up in the middle with nothing to mirror against except itself, so it must be a palindrome on its own.

```text
   l l s s s s l l
   [lls][ss][sll]
    [A]  [P] [rev A]      A = "lls"   P = "ss"

   cut the longer word:  sssll = "ss" | "sll"
                                 pre    suf
   pre is a palindrome, and suf = reverse("lls")
```

So what your hand kept track of was a cut inside the longer word: one side of the cut is a palindrome sitting in the middle of the result, and the other side, reversed, must be a whole word from the list. The partner is determined by the cut. Nothing needs to be searched, only looked up.

## The first honest attempt

Try every ordered pair: build `words[i] + words[j]` and compare with its reverse.

```text
 for "lls" (i=2), test j = 0, 1, 3, 4:
   lls+abcd  l vs d  fail
   lls+dcba  l vs a  fail
   lls+s     l vs s  fail
   lls+sssll l=l l=l s=s s=s  ok
 and again for every other i: n-1 partners each
```

That is `O(n^2 * L)`: for 5000 words of length 300, billions of operations. The repeated work is visible: for a fixed `words[i]`, we test it against all `n - 1` partners, rereading `words[i]` each time, and almost all fail on the very first character. Everything that makes a partner valid is determined by `words[i]` itself, yet we discover it by trial against every other word.

## The turning point

**Claim: if `w + x` is a palindrome, then cutting the longer of the two words at the right point gives one palindromic piece and one piece whose reverse is the other word.**

Prove it for `|w| >= |x|`. The palindrome `w + x` reads the same backwards, so its last `|x|` characters, which are `x`, reversed, equal its first `|x|` characters, which are the start of `w`. So `w = reverse(x) + rest`. And the middle of the palindrome, after removing the mirrored ends `reverse(x)` and `x`, is `rest`, which must itself be a palindrome. So: `w = pre + suf` with `pre = reverse(x)` and `suf` a palindrome, and the partner `x` goes **after** `w`. The case `|w| < |x|` is the mirror: `x` is the longer one, and from `w`'s point of view, `w = pre + suf` with `pre` a palindrome and `suf = reverse(x)`, partner placed **before** `w`.

So, for each word `w`, slide a cut over every position `j = 0..len(w)`:

```text
 w = [ pre | suf ]

 rule A: pre is a palindrome and reverse(suf) is a word
         -> reverse(suf) + pre + suf     pair (that, w)
 rule B: suf is a palindrome and reverse(pre) is a word
         -> pre + suf + reverse(pre)     pair (w, that)
```

The question "is `reverse(piece)` a word, and which one?" is answered in `O(1)` by a hash map built once: `where[reverse(word)] = index`. Then `suf in where` asks whether some word equals `reverse(suf)`, because a word `v` is stored under key `reverse(v)`. Each word now costs `len(w) + 1` cuts, each with an `O(L)` palindrome test and an `O(L)` hash of the piece. Total `O(n * L^2)` instead of `O(n^2 * L)`; with `L = 300` and `n = 5000` that is a big win.

Three guards make the output exact.

1. **Not with itself.** A palindromic word `w` has `reverse(w) == w` in the map pointing to its own index. Skip when `where[...] == i`.
2. **No duplicates.** If `w` and `v` are full reverses of each other (`abcd`, `dcba`), the pair `(w, v)` is found by rule B at cut `j = len(w)` (empty `suf`, `pre = w`) from `w`'s side, and also by rule A at cut `j = 0` (empty `pre`, `suf = v`) from `v`'s side. Only one of these must count. The code disables rule B at `j = len(w)`, so the full-reverse pairs come only from rule A.
3. **The empty word.** `""` with a palindromic word `p` gives both `p + ""` and `"" + p`, and both come out naturally while processing `p`. At cut `j = 0`, `suf = p` is a palindrome and `pre = ""` is in the map, so rule B emits `(p, "")`. At cut `j = len(p)`, `pre = p` is a palindrome and `suf = ""` is in the map, so rule A emits `("", p)`. Each once.

## Watch it work

`words = ["abcd","dcba","lls","s","sssll"]`. The map stores each word reversed:

```text
 where = { dcba:0, abcd:1, sll:2, s:3, llsss:4 }
```

Frame 1. `w = "abcd"` (i=0). Cut `j = 0`.

```text
 pre="" | suf="abcd"
 A: pre "" palindrome, "abcd" in where -> 1  => (1,0)
 B: suf "abcd" not palindrome
 result: [(1,0)]          "dcba"+"abcd"
```

Cuts 1..3 find nothing. At `j = 4`, `pre = "abcd"` is in the map, but rule B is disabled at the last cut, which is the duplicate guard.

Frame 2. `w = "dcba"` (i=1). Cut `j = 0`.

```text
 pre="" | suf="dcba"
 A: "dcba" in where -> 0                    => (0,1)
 result: [(1,0),(0,1)]    "abcd"+"dcba"
```

The pair `(0, 1)` is found here, once, by rule A; the symmetric rule-B hit at `w = "abcd"`, `j = 4` was suppressed.

Frame 3. `w = "lls"` (i=2). Cuts 0 to 3.

```text
 j=0  "" | lls   A: lls not in map   B: lls not pal
 j=1  l  | ls    A: ls not in map    B: ls not pal
 j=2  ll | s     A: ll pal, s in map -> 3  => (3,2)
                 B: s pal, ll not in map
 j=3  lls| ""    A: lls not pal  (B disabled)
 result: [(1,0),(0,1),(3,2)]   "s"+"lls" = slls
```

The palindrome `ll` sits in the middle; `s` mirrors `s`.

Frame 4. `w = "s"` (i=3).

```text
 j=0  "" | s   A: "s" in map -> 3, but 3 == i: skip
 j=1  s  | ""  A: "" not in map  (B disabled)
 nothing added
```

The self-pairing guard fired: `"s" + "s"` would need two copies of the same word.

Frame 5. `w = "sssll"` (i=4).

```text
 j=0  ""   | sssll  A: not in map
 j=1  s    | ssll   A: ssll not in map; B: ssll not pal
 j=2  ss   | sll    A: ss pal, sll in map -> 2 => (2,4)
 j=3  sss  | ll     A: ll not in map; B: sss not in map
 j=4  sssl | l      B: l pal, sssl not in map
 j=5  sssll| ""     A: sssll not pal (B disabled)
 result: [(1,0),(0,1),(3,2),(2,4)]
```

This is the hand-worked cut from earlier: `lls` in front, `ss` in the middle.

Across the frames, each word only ever looked at its own cuts and asked the map; no word was compared with another word character by character.

## Why it is correct

Completeness: take any valid pair `(a, b)`, `a != b`, with `words[a] + words[b]` a palindrome. If `|words[a]| >= |words[b]|`, the claim says `words[a] = reverse(words[b]) + P` with `P` a palindrome; processing `w = words[a]` at cut `j = |words[b]|` triggers rule B, unless `j = len(w)`, which means `P` is empty and the words are full reverses; in that case processing `words[b]` at `j = 0` triggers rule A for the same pair. If `|words[a]| < |words[b]|`, the claim says `words[b] = P + reverse(words[a])`; processing `w = words[b]` at cut `j = |P|` triggers rule A, and since `|P| < len(w)`, nothing is disabled. So every valid pair is emitted.

Soundness: each emitted pair has the shape `reverse(suf) + pre + suf` with `pre` a palindrome, or `pre + suf + reverse(pre)` with `suf` a palindrome, both palindromes by construction, and the index guard excludes `i == j`.

No duplicates: for a given pair, the only cut that produces it from the longer word is unique (its length fixes `j`), and for equal lengths the disabled cut leaves exactly one route.

## Cost

- Time `O(n * L^2)`: `n` words, `L + 1` cuts each, each cut does an `O(L)` slice, reverse check, and hash lookup.
- Space `O(n * L)`: the map of reversed words, plus the output.

A trie of reversed words removes the slicing and hashing of each piece, and precomputing which prefixes and suffixes of every word are palindromes removes the repeated palindrome tests; the constants shrink a lot, though the simple worst-case bound is still quoted as `O(n * L^2)`.

## Variations you will meet

- **Count pairs instead of listing them.** Same scan; increment a counter. Duplicate handling still matters.
- **Words not distinct.** The map needs a list of indices per key, and the self-pair guard becomes "different index", not "different key".
- **Trie of reversed words.** Walk `w` down the trie; at each node, if the rest of `w` is a palindrome and a word ends here, that is rule B; at the end of `w`, any word below the node whose remaining part is a palindrome gives rule A. Precompute "palindromic remainder" lists per node.
- **Two-word anagram or concatenation queries.** "Does `w + x` equal a target?" uses the same cut-and-look-up pattern without the palindrome test.

## What to carry forward

When pairs are too many to test, let one element of the pair determine what the other must look like, then look it up in a hash map; here a cut plus a palindrome test pins down the partner exactly. The final problem pushes hashing further: instead of hashing whole words, it hashes every sliding window of a string in `O(1)` each and combines that with binary search on the length.
