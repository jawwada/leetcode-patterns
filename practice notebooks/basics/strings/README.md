# Strings

A Python string is an immutable sequence of characters. Every operation that "changes" a string builds a new one, so the cost of an algorithm on strings is governed by how many characters it copies and how many times it rescans. The fundamentals here are the four habits that keep that cost linear: count characters instead of sorting them, walk with two pointers instead of slicing, remember what already matched instead of restarting, and collect pieces in a list instead of concatenating.

## Core operations and cost

| Operation | Cost | Note |
|---|---|---|
| `s[i]`, `len(s)`, `ord`/`chr` | O(1) | characters are small integers in disguise |
| `s[a:b]` | O(b - a) | copies; a slice inside a loop multiplies the work |
| `s + t`, `s += t` | O(len(s) + len(t)) | in a loop this is O(n^2) characters copied |
| `"".join(parts)` | O(total length) | one allocation, each character copied once |
| `sorted(s)` | O(n log n) | fine for a key, wasteful when a count array works |
| 26-slot count array | O(n) build, O(26) compare | the key for anagram questions |
| two pointers `lo`, `hi` | O(n) | each pointer moves at most n times |
| naive `find` | O(n * m) | restarts the pattern after every mismatch |
| KMP / Rabin-Karp | O(n + m) | never moves the text index backwards |

## Drawn example: KMP failure table of `aabaaab`

`fail[i]` is the length of the longest proper prefix of `pattern[:i + 1]` that is also its suffix.

```
i      0   1   2   3   4   5   6
char   a   a   b   a   a   a   b
fail   0   1   0   1   2   2   3

i=1  'a' == pattern[0]               k=1        fail[1]=1   border "a"
i=2  'b' != pattern[1]  k=fail[0]=0  'b' != 'a' fail[2]=0
i=3  'a' == pattern[0]               k=1        fail[3]=1   border "a"
i=4  'a' == pattern[1]               k=2        fail[4]=2   border "aa"
i=5  'a' != pattern[2]  k=fail[1]=1  'a' == pattern[1] k=2  fail[5]=2   border "aa"
i=6  'b' == pattern[2]               k=3        fail[6]=3   border "aab"
```

Searching `aabaaabaab` for `aab`: after the hit at 0 the matched length falls to `fail[2] = 0`; at index 5 the third `a` mismatches `b`, the matched length falls to `fail[1] = 1` and the text index never goes back.

## The invariant to say out loud

"The text pointer only moves forward; what I already matched is remembered by a number, not by rescanning."

For counting: "two strings are anagrams exactly when their 26 counts are equal." For building: "append to a list, join once at the end."

## Exercises

| File | Drills |
|---|---|
| `01_character_counting_and_anagrams.py` | 26-slot counts instead of sorting; the count tuple as a dict key for grouping |
| `02_two_pointer_palindromes_and_reverse_words.py` | lo/hi pointers that skip and compare; reverse all then reverse each word, in place |
| `03_kmp_prefix_function.py` | build the failure table, fall back with `fail[j - 1]`, find all (overlapping) hits |
| `04_rabin_karp_rolling_hash.py` | polynomial hash, O(1) roll with `BASE^(m-1)`, verify on every hash hit |
| `05_encode_decode_strings_and_join.py` | length-prefix framing that survives any character; list + join versus `+=` cost |
