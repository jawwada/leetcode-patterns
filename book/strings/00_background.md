# Strings: Scanning, Parsing, Canonical Forms
*17 problems · Reading time ~16 min*

## Why this chapter exists

Almost every interview has a string question, and almost none of them are really about strings. They are about walking a sequence once while remembering the right small thing. The string is just the most common sequence, and it comes with three traps of its own: it is immutable, its "characters" are code points rather than bytes, and the input format is usually fussier than it looks.

The seventeen problems fall into five families:

- **Cutting and reassembling** (Implement Split, Reverse Words, Text Justification): find the boundaries between pieces, then build a new string from them without wasting copies.
- **Counting and canonical forms** (Valid Anagram, Group Shifted Strings): throw away what does not matter (order, absolute letter values) so that strings that are "the same" turn into the same key.
- **Parsing with a little state** (Compare Version Numbers, atoi, Valid Number, Integer to English Words, Zigzag): one pointer moves left to right, and its behaviour depends on a phase or a few flags.
- **Matching with a stack** (Simplify Path, Minimum Remove to Make Valid Parentheses): something later cancels the most recent unfinished thing.
- **Self-similarity** (Longest Palindromic Substring, Longest Happy Prefix, Shortest Palindrome, Palindrome Pairs, Longest Duplicate Substring): the string is compared against itself, reversed, shifted, or windowed. This is where borders, the failure function and rolling hashes come in.

## What it is

A Python `str` is an immutable array of Unicode code points. "Array" means indexing `s[i]` is O(1) and `len(s)` is stored rather than counted. "Code point" means each slot holds one abstract character such as `a`, `é` or `→`, not one byte. "Immutable" means no operation changes a string in place. Every operation that looks like an edit builds a new string.

```text
s = "héllo"

 index:    0     1     2     3     4
         +-----+-----+-----+-----+-----+
 slots:  |  h  |  é  |  l  |  l  |  o  |   one code point
         +-----+-----+-----+-----+-----+   per slot
 len(s) = 5   (stored, O(1))

 UTF-8 bytes on disk:  68 | C3 A9 | 6C | 6C | 6F   (6 bytes)
                            ^^^^^ one code point, two bytes
```

The byte picture matters only when someone asks about encodings. Inside Python, think in slots.

Immutability has one expensive consequence. Building a string by repeated `+=` can copy everything built so far on each step:

```text
out = ""; for piece in pieces: out += piece

 step 1:  [a]                      copy 1 char
 step 2:  [a b]                    copy 2 chars
 step 3:  [a b c]                  copy 3 chars
 ...
 step n:  [a b c ... n]            copy n chars
                                   total 1+2+...+n = O(n^2)

 fix:  parts = []; parts.append(piece) ...; "".join(parts)
       join measures the total once, allocates once: O(n)
```

CPython sometimes resizes in place when only one reference to the string exists. Do not rely on that. Interviewers know the trap, and it does not exist in other languages. When a problem asks you to "modify the string in place", convert to `list(s)` first. That gives you a mutable array of one-character strings, and you `"".join` it back at the end.

Nearly every problem here is solved by one of three workhorses, sometimes two at once.

**1. The counter.** A histogram of symbols, usually 26 cells for lowercase letters (`ord(c) - 97`) or a dict for anything wider. It deliberately forgets order.

```text
"banana"  ->   a  b  c ... n ... z
              [3][1][0]...[2]...[0]
```

**2. The two-pointer scan.** One index reads and another writes, or two indices walk toward each other, or two indices walk two different strings in lockstep. The state is just the positions plus maybe an accumulator.

```text
 read/write compaction       converge (reverse)     lockstep
 r ->                        L ->       <- R        i ->  (s1)
 w ->  (w <= r always)       swap s[L], s[R]        j ->  (s2)
```

**3. The stack.** You need it when a later symbol cancels or closes the most recent open thing: `..` cancels the last directory and `)` closes the last `(`.

```text
 input:  ( a ( b ) )
 stack:  [0] [0] [0,2] [0,2] [0] []      (indices of open '(')
                          ^ ')' pops 2
```

On top of these sit two ideas that turn a messy question into a clean one.

**Canonical forms.** Two strings are "equivalent" under some rule. You pick one representative per class and compare representatives instead of strings. Sorted letters are the canonical form under rearrangement. Gaps between consecutive letters are the canonical form under shifting. The reversed string is what you look up when you want to know whether something "mirrors" a word.

```text
 rule: rearrange    "eat" -> "aet"   "tea" -> "aet"   same key
 rule: shift all    "abc" -> (1,1)   "xyz" -> (1,1)   same key
 rule: mirror       want w + ? palindrome -> look up reverse(w)
```

**State machines for parsing.** A parser that reads one character at a time and keeps only a phase label is a finite automaton. Draw it before you code it. Here is the one for atoi:

```text
          ' '                 digit
         +---+               +-----+
         v   |               v     |
     +--------+  '+'/'-' +------+  |  digit   +--------+
 --> | SPACE  |--------->| SIGN |--+--------->| DIGITS |
     +--------+          +------+             +--------+
         |  digit                                 ^  |
         +----------------------------------------+  | other
                                                     v
              any other char from any state ---> [ STOP ]
```

Each arrow is labelled with the character class that takes it. Any character with no arrow ends the run. Valid Number has the same shape with three flags in place of a phase.

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| `s[i]`, `len(s)` | O(1) | array slot; length is stored |
| `s[a:b]` | O(b - a) | copies the slice into a new string |
| `s + t` | O(len s + len t) | new string, both copied |
| `"".join(parts)` | O(total) | one size pass, one allocation |
| `s == t` | O(min len) | stops at first mismatch; length checked first |
| `hash(s)` / dict lookup by `s` | O(len s) first time | hash is cached on the object afterwards |
| `s.find(t)`, `t in s` | O(n·m) worst | CPython uses a fast heuristic, not a guaranteed bound |
| `sorted(s)` | O(n log n) | general comparison sort |
| `Counter(s)` / 26-array fill | O(n) | one pass |
| `list(s)` / `s[::-1]` | O(n) | full copy |
| stack push / pop on a list | O(1) amortised | end of a dynamic array |

The slice and the `+` are the operations people undercount. A slice looks like a view and is actually a copy:

```text
 s = "abcdefgh"          t = s[2:5]
 +-+-+-+-+-+-+-+-+        +-+-+-+
 |a|b|c|d|e|f|g|h|  --->  |c|d|e|   new object, 3 chars copied
 +-+-+-+-+-+-+-+-+        +-+-+-+
      ^   ^
      2   5 (exclusive)
```

So "slice off the remainder after each match" inside a loop is quadratic. The cure is to carry an index, as in Implement Split.

Comparison `s[i:i+m] == sep` costs O(m). It builds a slice and then compares it. For one-character separators that is O(1). For long ones it is the O(n·m) of naive matching, which the hard problems replace with borders or hashes.

## The invariant

The invariant that protects every scan in this chapter:

> **Everything left of the read pointer has been fully accounted for in the state, and the state is all you need to continue.**

"Accounted for" means something different in each problem. For a split it means every finished piece is in `parts` and `start` marks the piece in progress. For a counter it means the histogram equals the counts of the prefix read so far. For a stack it means the stack holds exactly the unmatched openers of the prefix. The scan never looks back, because the state already summarises the past.

```text
 LEGAL (split "a,,b," on ",", after reading index 2)

  a , , b ,
  0 1 2 3 4
        ^ i = 3, start = 3
  parts = ["a", ""]     <- every cut left of i is in parts
                           piece in progress = s[3:3] = ""

 ILLEGAL (same position)

  parts = ["a"]          <- a cut at index 2 happened but its
  start = 2                 empty piece was never emitted;
                            the state no longer describes the
                            prefix, and the answer will be
                            missing a "" forever
```

Most bugs in string problems are this illegal state in some form: a piece forgotten at the end, a flag not reset, a stack entry left over. When you debug, stop at any index and ask whether the state describes exactly the prefix.

## How to picture it

Picture a **tape with a read head** moving right, and a **small notebook** beside it. The tape is the string. The notebook is the state: a phase name, a few flags, a 26-cell histogram, or a stack of open things. The head never moves left. If you catch yourself wanting to move it left, either the notebook is missing something or you need a second head.

```text
  tape:  | - | 0 | 4 | 1 | 2 | x | 9 |
                     ^ head
  notebook:  phase = DIGITS   sign = -1   num = 4
```

For the self-similar problems at the end, picture the **string laid against a copy of itself**. You slide the copy, or reverse it, or cut a window from it, and ask where the two agree. A **border** is a prefix that is also a suffix:

```text
  s = a b a c a b a
      [a b a]              prefix "aba"
              [a b a]      suffix "aba"     longest border = 3

  failure function (longest border of each prefix s[:i+1]):
  i:     0 1 2 3 4 5 6
  s:     a b a c a b a
  fail:  0 0 1 0 1 2 3
```

The failure function (KMP's table) computes this for every prefix in O(n). It does this by extending the previous border when the next characters match, and by falling back to "the border of the border" when they do not. Longest Happy Prefix is exactly this table. Shortest Palindrome runs it on `s + "#" + reverse(s)`.

A **rolling hash** treats a window as a number in base B. Sliding the window drops the leading digit and appends a trailing one in O(1):

```text
  s = a b c a b      digits a=0 b=1 c=2, base 26, window 2

  [a b] c a b     h = 0*26 + 1           = 1
   a [b c] a b    h = (1  - 0*26)*26 + 2 = 28
   a b [c a] b    h = (28 - 1*26)*26 + 0 = 52
   a b c [a b]    h = (52 - 2*26)*26 + 1 = 1   <- "ab" again
```

Equal windows always give equal hashes. Unequal windows may collide, so a hash hit is confirmed by comparing characters. Combined with binary search on the window length, this is Longest Duplicate Substring. These two tools are what the hard problems add on top of the scan-and-notebook picture: the notebook now remembers something about the string's relation to itself.

## Signals in a problem statement

- "anagram", "permutation of", "same letters", "rearrange" → counter, or sorted string as a key.
- "group strings that are …", "equivalent under" → canonical key in a dict.
- "parse", "valid", "convert string to …", a grammar of optional signs, dots and exponents → state machine with flags. Draw it first.
- "words separated by one or more spaces", "leading/trailing spaces" → compaction scan or split; watch the empty pieces.
- "in place", "O(1) extra space" on a string → `list(s)`, two pointers, reversal tricks.
- "cancel", "go up", "matching", "balanced", nesting → stack of indices.
- "palindrome" with "substring" → expand around centres. With "prefix" or "add characters in front" → borders on `s + # + reverse(s)`. With "pairs of words" → hash map of reversed words.
- "longest prefix which is also suffix", "repeated pattern", "period" → failure function.
- "longest repeated / duplicate substring", length up to 3·10^4 → binary search on length plus rolling hash (or a suffix array).
- "fixed width", "justify", "format into lines" → greedy packing plus careful arithmetic.
- **Counter-signals**: "subsequence" (not substring) usually means DP, not scanning. "Minimum window containing …" or "longest substring without …" is the sliding-window chapter. A dictionary of words to match against with shared prefixes points to a trie. "Edit distance" means DP.

## Python toolbox

```python
idx = ord(c) - 97  # 'a'..'z' -> 0..25; chr(97+k) back
cnt = [0] * 26     # beats Counter for a fixed alphabet
from collections import Counter, defaultdict
groups = defaultdict(list)   # groups[key].append(w)
key = tuple(cnt)   # lists unhashable; tuples are keys
```

```python
"".join(parts)     # the safe way to build big strings
chars = list(s); chars[i] = "x"; s2 = "".join(chars)
s.split()      # runs of whitespace, NO empty pieces
s.split(" ")   # every single space cuts; empty pieces kept
s.isdigit()    # True for '²' and other scripts too!
"0" <= c <= "9"    # the ASCII digit test you want
s[::-1]                      # reversed copy, O(n)
```

```python
divmod(spaces, gaps)         # even spread + remainder (justify)
s.startswith(p, i)           # compare at offset without slicing
```

Two quirks are worth memorising. `str.split()` with no argument and `str.split(" ")` have different semantics. `isdigit` is wider than ASCII.

## Mistakes people make

1. **`out += piece` in a loop.** Quadratic in other languages and risky in Python. Fix: collect in a list and `"".join` once.
2. **Forgetting the last piece after the loop.** "Emit on separator" never fires at the end of the string. Fix: always emit `s[start:]` (or flush the accumulator) after the loop.
3. **Slicing the remainder each iteration.** `s = s[k+1:]` copies the tail every time. Fix: carry a `start` index.
4. **Using `isdigit()` as an ASCII test.** It accepts superscripts and other scripts' digits. Fix: `"0" <= c <= "9"`.
5. **Comparing numeric fields as strings.** `"01" != "1"` and `"10" < "9"`. Fix: parse to int, or strip leading zeros and compare length first.
6. **Not resetting a flag when the phase changes.** In Valid Number, `e` must clear "seen digit", or `"1e"` passes. Fix: list the flags each transition sets and clears.
7. **Deleting from a string or list while iterating over its indices.** Indices shift under you. Fix: mark positions (`chars[i] = ""`) and join at the end.
8. **Treating a hash hit as equality.** Rolling hashes collide. Fix: confirm with a character comparison, or use two moduli.
9. **Off-by-one on the last window or last word.** `range(len(s) - m)` misses the final position. Fix: `while i <= len(s) - m`, and loop to `len(s)` inclusive when the end acts as a separator.
10. **Mutating a `str`.** `s[i] = "x"` raises TypeError. Fix: work on `list(s)`.

## The journey ahead

1. **Implement Split**: the baseline scan. One read index, one `start` marker, and the discipline of emitting the final piece. The string-as-tape picture starts here.
2. **Valid Anagram**: the counter. Forget order, keep counts. It is the first canonical form, a histogram.
3. **Reverse Words in a String**: two pointers on a mutable copy. It adds read/write compaction and the "reverse all, then reverse each" composition.
4. **Compare Version Numbers**: two strings scanned in lockstep, with numbers parsed in place. An exhausted pointer reads as zero.
5. **String to Integer (atoi)**: the first explicit state machine (SPACE → SIGN → DIGITS → STOP), plus overflow clamping during accumulation.
6. **Valid Number**: the state machine grows into a grammar. Three flags replace the phase, and you must know exactly which transition resets which flag.
7. **Simplify Path**: the stack arrives. `..` cancels the most recent surviving name.
8. **Minimum Remove to Make Valid Parentheses**: the stack holds indices instead of values, so unmatched characters can be marked for deletion in one pass.
9. **Zigzag Conversion**: back to scanning, with a row pointer that bounces between walls. It shows that you rarely need the 2-D picture you are given.
10. **Group Shifted Strings**: the canonical key generalised from "sorted letters" to "gaps mod 26".
11. **Integer to English Words**: parsing in reverse. Chunk by thousands, with one rule per chunk and lookup tables.
12. **Text Justification**: the hard version of cut-and-reassemble. Greedy line packing, then divmod to spread spaces.
13. **Longest Palindromic Substring**: the first self-comparison. Grow mirrors outward from 2n − 1 centres.
14. **Longest Happy Prefix**: borders and the failure function, built incrementally with fallback.
15. **Shortest Palindrome**: reuses the failure function on `s + "#" + reverse(s)` to find the longest palindromic prefix.
16. **Palindrome Pairs**: combines palindromes with canonical lookup. Store reversed words in a map and try every cut of every word.
17. **Longest Duplicate Substring**: rolling hash plus binary search on the answer length. The window is compared against every earlier window in O(1) each.
