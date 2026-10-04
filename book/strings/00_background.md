# Strings: Scanning, Parsing, Canonical Forms
*17 problems · Reading time ~26 min*

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

## Advanced patterns

The tape-and-notebook picture carries you through every Medium in this chapter. The Hard problems ask for more: a notebook that is provably small, an output assembled by arithmetic instead of trial and error, or a notebook that records how the string relates to itself. Seven patterns cover all of them. Each one is a way of answering the question "what is the least I must remember, and how do I update it in O(1) amortised?"

### 1. Collapse the automaton into flags

**When it shows up**: a validation or parsing problem with optional parts (sign, fraction, exponent, scheme, port) where the full state diagram has more than five or six states and you would be coding a table in an interview.

**The intuition**: a state in a recogniser is just a name for "what kind of prefix have I read". Write the states down and describe each one by a few yes/no facts: have I seen a digit in the current part, have I seen a dot, have I seen an exponent. States with identical facts behave identically on every future character, so they merge. What remains is a handful of booleans plus one rule per character class saying which flags it requires, which it sets, and which it clears. The clearing is the subtle part: entering a new part of the grammar (the exponent) restarts the "digit seen" fact, because the new part needs its own digits. Acceptance at the end is a condition on the flags, not a list of accepting states.

```text
 "-1.5e+3"  flags D = digit in current part, P = dot, X = exp

 char:   -    1    .    5    e    +    3
 D:      0    1    1    1    0    0    1   e clears D
 P:      0    0    1    1    1    1    1
 X:      0    0    0    0    1    1    1
                                         end: D = 1 -> valid

 "1e":   D after 'e' = 0 at the end      -> invalid
 rules:  '.'  needs not P and not X        sets P
         'e'  needs D and not X            sets X, clears D
         sign only at start or after 'e'
```

**Where you'll use it**: Valid Number is the full version; String to Integer (atoi) is the small version, where a single phase variable is already the collapsed form. Beyond the chapter: Validate IP Address (LeetCode 468) has the same "parts with their own rules" shape.

### 2. Decompose positionally, then apply one stencil per chunk

**When it shows up**: output that spells or formats a number or a structure whose rules repeat at every scale: number names, roman numerals, grouping digits with commas, durations like "2h 5m".

**The intuition**: English names numbers in base 1000. Above the hundreds, every group of three digits is spoken the same way and then labelled with a scale word that depends only on its position. So the problem splits into two independent parts: a function that spells any number below 1000, and a loop that peels chunks off with `% 1000` and `// 1000`. All the irregularity of English (teens, "Twenty" not "Twoty") lives in two lookup tables inside the chunk function, and zero chunks simply say nothing. Once you see the repeat, the special cases stop being cases and become table entries. The only case the loop cannot produce is the number zero itself, which you handle before it starts.

```text
 1234567 -> peel low to high with divmod by 1000

      1   |   234    |   567       chunk values
  Million | Thousand |  (none)     scale = position
     |         |          |
  "One"  "Two Hundred   "Five Hundred
          Thirty Four"   Sixty Seven"

 1000010 ->   1 | 000 | 010    middle chunk is zero:
              "One Million Ten"   no "Thousand" emitted
```

**Where you'll use it**: Integer to English Words. Beyond the chapter: Integer to Roman (LeetCode 12) is the same idea with a greedy table instead of chunks.

### 3. Greedy packing, then distribute by divmod

**When it shows up**: "fit as many as possible on each line, then pad to a fixed width", or any problem where k units must be spread over g slots "as evenly as possible" with a stated tie-break.

**The intuition**: the problem has two halves that never talk to each other. Packing decides which items share a line, and it only needs a running width that counts one mandatory space before each added word. Distribution decides how the leftover columns are spread, and it does not change which words are on the line. "As even as possible" forces every gap to hold either `q` or `q + 1` spaces, because if two gaps differed by two you could move one space and be more even. Counting then gives `spaces = gaps * q + r` with `0 <= r < gaps`, which is exactly `divmod(spaces, gaps)`, and "extra to the left" says the first `r` gaps get the `+1`. One division replaces a loop that hands out spaces one at a time. The special lines (one word, last line) use a different rule and must be checked before the division, which would otherwise divide by zero.

```text
 maxWidth = 16

 pack:  This(4) is(2) an(2) | example ...   4+1+2+1+2 = 10
        adding example: 10 + 1 + 7 = 18 > 16 -> close line

 line 1: letters = 8, spaces = 16 - 8 = 8, gaps = 2
         divmod(8, 2)  = (4, 0) -> "This    is    an"
 line 2: example of text, letters = 13, spaces = 3, gaps = 2
         divmod(3, 2)  = (1, 1) -> gaps 2, 1
                                 "example  of text"
```

**Where you'll use it**: Text Justification. The divmod half reappears in any "split n items into k nearly equal groups" question, such as Split Linked List in Parts (LeetCode 725).

### 4. The border chain and its amortised fallback

**When it shows up**: questions about prefixes that are also suffixes, periods ("is s a repetition of some block?"), or matching a pattern without re-reading text, all with n up to 10^5 so O(n^2) comparison is out.

**The intuition**: the borders of a string are nested. Any border shorter than the longest one is a border of that longest border, so the full list of borders is a chain: `fail[n-1]`, then `fail[fail[n-1] - 1]`, and so on down to zero. When the next character fails to extend the current border, you do not restart; you step down the chain to the next shorter candidate and try again, because nothing between two links can be a border. The cost looks quadratic because of the inner loop, but follow `k`, the current border length, as one running quantity. It rises by at most one per character and falls by at least one per fallback, and it never goes below zero, so the total number of falls is bounded by the total number of rises: O(n) overall. That potential argument is worth memorising on its own; it is the same reason a monotonic stack is linear.

```text
 s = a a b a a a b        computing fail[5] (s[5] = 'a')

 i:    0 1 2 3 4 5 6
 s:    a a b a a a b
 fail: 0 1 0 1 2 ? .

 k = fail[4] = 2   compare s[5]='a' with s[2]='b'  no
 k = fail[1] = 1   compare s[5]='a' with s[1]='a'  yes
 fail[5] = k + 1 = 2

 falls: i=2 (1 -> 0), i=5 (2 -> 1)    2 falls
 rises: i=1, 3, 4, 5, 6                5 rises
 falls can never outnumber rises -> O(n) total
```

**Where you'll use it**: Longest Happy Prefix is this table and nothing else; Shortest Palindrome builds it on a constructed string. Beyond the chapter: Repeated Substring Pattern (LeetCode 459) asks whether `n - fail[n-1]` divides `n`, and Find the Index of the First Occurrence in a String (LeetCode 28) is plain KMP.

### 5. Glue two strings with a sentinel, then ask one question

**When it shows up**: a question relating two strings (does `p` occur in `t`; how much of `s` is a palindrome from the left; which prefix of `a` is a suffix of `b`) that becomes a question about a single string once they are placed side by side.

**The intuition**: the failure function only talks about one string, its prefixes and its suffixes. If you write `x + "#" + y`, then prefixes of the combined string are prefixes of `x`, and suffixes ending inside `y` are suffixes of a prefix of `y`. A border of a prefix of the glued string is therefore "a prefix of `x` that equals something ending at this point of `y`". The separator `#`, a character in neither string, guarantees that no border can straddle the junction, so no border is longer than `x`. Choose `x` and `y` to make that border mean what you need: `p + "#" + t` gives `fail == len(p)` exactly at match ends; `s + "#" + reverse(s)` gives the longest prefix of `s` that equals a suffix of its reverse, which is the longest palindromic prefix.

```text
 pattern search: p = "aba", t = "abababa"

 g    = a b a # a b a b a b a
 i    = 0 1 2 3 4 5 6 7 8 9 10
 fail = 0 0 1 0 1 2 3 2 3 2 3
                    ^   ^    ^  fail == 3 = len(p)
 match starts in t = i - 2*len(p) = 0, 2, 4

 palindromic prefix: s = "abab"
 g = a b a b # b a b a   fail[-1] = 3 -> "aba"
     [a b a]     [a b a]   keep 3, prepend reverse("b")
```

Without the separator, `s = "aaaa"` glued to its reverse gives `"aaaaaaaa"`, whose longest border is 7, longer than `s` and meaningless.

**Where you'll use it**: Shortest Palindrome. Beyond the chapter: the same gluing with the Z-function instead of the failure function solves pattern counting, and LeetCode 28 can be done this way in one table.

### 6. Split every word at every cut, look up the mirror

**When it shows up**: pairs of items from a list whose combination must satisfy a symmetric property (palindrome, sums to a target, complements), where n^2 pairs are too many but each item is short.

**The intuition**: instead of testing pairs, ask what the partner of a word must look like. If `w + x` is a palindrome and `w` is the longer word, then `w` starts with `reverse(x)` and what remains of `w` is itself a palindrome. So cut `w` at every position into `pre | suf`: if one side is a palindrome, the other side's reverse is the only possible partner, and a hash map from `reverse(word)` to index answers "does it exist" in O(1). The search space moves from pairs of words (n^2) to cuts of one word (n times L). It is the same move as Two Sum: fix one element, compute the one complement that would work, look it up. The guards are about the boundaries: no word pairs with itself, and the empty cut must be allowed on only one side so a full-reverse pair is counted once.

```text
 words: 0 abcd  1 dcba  2 lls  3 s  4 sssll
 map: reverse(word) -> index   {dcba:0, abcd:1, sll:2,
                                s:3, llsss:4}

 w = "lls", cut j = 2:   pre = "ll" | suf = "s"
     pre is a palindrome; is reverse(suf) = "s" a word? yes, 3
     -> "s" + "lls" = "slls"          pair (3, 2)

 w = "sssll", cut j = 2: pre = "ss" | suf = "sll"
     pre palindrome; reverse("sll") = "lls" is word 2
     -> "lls" + "sssll" = "llssssll"  pair (2, 4)
```

The full answer for this list is `(0,1) (1,0) (2,4) (3,2)`.

**Where you'll use it**: Palindrome Pairs, which also reuses the palindrome checks from Longest Palindromic Substring and the canonical-key lookup from Group Shifted Strings. Beyond the chapter: Two Sum (LeetCode 1) is the numeric ancestor.

### 7. Binary search the length, roll a hash across windows

**When it shows up**: "longest substring that appears twice / in both strings / k times", with n around 10^4 to 10^5, where checking a single fixed length is easy but trying all lengths is too slow.

**The intuition**: two facts, one for each loop you want to remove. First, the predicate "some substring of length L repeats" is monotone: chop the last character off both copies of a repeated string of length L and you have a repeated string of length L - 1. So the lengths look like T T T F F, and binary search finds the last T with O(log n) checks. Second, one check is a sliding window of fixed width, and a polynomial hash of the window can be updated in O(1) when it slides: multiply by the base, subtract the character that fell out times `B^L`, add the new one. A dictionary from hash to start positions finds a repeat in one pass. Equal windows always hash equal; a hash hit is only a candidate, so you confirm it with a direct comparison (or carry two independent hashes). Together: O(n log n) expected, where checking every pair of windows of every length would be cubic.

```text
 s = "banana", answer length L* = 3

 lengths:  1  2  3  4  5          binary search
 repeat?:  T  T  T  F  F          lo=1 hi=5 mid=3 T
                    ^ L*          lo=4 hi=5 mid=4 F
                                  hi=3 -> L* = 3

 check(3), a=1..z=26, base 27:
   [ban]ana   h = 1499    seen {1499: [0]}
   b[ana]na   h = 1108    seen {.., 1108: [1]}
   ba[nan]a   h = 10247
   ban[ana]   h = 1108    hit! s[1:4] == s[3:6] = "ana"
```

**Where you'll use it**: Longest Duplicate Substring. Beyond the chapter: Maximum Length of Repeated Subarray (LeetCode 718) has the same shape across two arrays, and Repeated DNA Sequences (LeetCode 187) is a single fixed-length check.

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

The order follows the notebook. It starts with an index and a marker, then a histogram, then phases and flags, then a stack. After that the output has to be built to a specification, and in the last stage the notebook records how the string relates to itself. Each problem reuses the previous one's state and adds one thing.

### Warm-up: one tape, one small notebook

**Implement Split.** Cutting a string at a separator sounds like a one-liner until you ask what `"a,,b,"` should give and notice that the last piece never meets a separator. The problem teaches the baseline scan: a read index, a `start` marker, emit on every cut, and always emit once more after the loop. Every later scan in the chapter is this one with a richer notebook.

**Valid Anagram.** Sorting both strings works, but it does more than the question asks: it puts the letters in order when you only need to know how many of each there are. The 26-cell counter forgets order on purpose, and that is the chapter's first canonical form: two strings are equivalent exactly when their histograms match.

**Reverse Words in a String.** Splitting and joining is easy. Doing it in place on a character array, with runs of spaces to squeeze out, is the real puzzle. It adds a second pointer that writes behind the reader (compaction) and a composition trick: reverse the whole array, then reverse each word back, and the word order has flipped while each word reads correctly.

**Compare Version Numbers.** Two tapes are read at once, and the fields are numbers, so `"1.01"` equals `"1.001"`, and `"1.0"` equals `"1"`. The new idea is lockstep scanning with integers parsed in place, plus the convention that an exhausted string keeps reading zeros. That convention removes the length special cases.

### Parsers: phases, then flags

**String to Integer (atoi).** The input is messy (spaces, a sign, digits, then garbage) and the output must be clamped to 32 bits. This is the first time the notebook holds a phase, so the scan is an explicit state machine, and overflow is caught during accumulation, before the number grows too large to clamp, rather than after.

**Valid Number.** A dozen tricky inputs (`"4."`, `".5"`, `"1e"`, `"+.e1"`) make it feel like a pile of special cases. Drawing the automaton shows nine states, and describing each state by three facts collapses them into three flags. The skill being trained is knowing exactly which transition sets or clears which flag, which is advanced pattern 1.

### Stacks: later cancels earlier

**Simplify Path.** `..` undoes the most recent directory that survived, and `.` and empty segments do nothing. That "undo the latest" rule means the notebook is now a stack. The problem also reuses Implement Split, because you first cut the path on `/`, and its empty pieces are exactly the doubled slashes you have to ignore.

**Minimum Remove to Make Valid Parentheses.** The stack now holds positions, not characters, so an unmatched `(` that is still on the stack at the end can be found and deleted. The puzzle is that a `)` can be judged immediately while a `(` can only be judged at the end. Marking positions and joining once avoids the shifting-index bug of deleting while you scan.

### Reshaping and keys

**Zigzag Conversion.** The problem invites you to build a 2-D grid and read it row by row. The point is that you never need it: a row pointer that bounces between the top and bottom walls, appending each character to its row's list, produces the same output in one pass with no empty cells.

**Group Shifted Strings.** Grouping by sorted letters (the anagram key) fails here, because shifting changes every letter. What survives a shift is the sequence of gaps between consecutive letters, taken mod 26 so that `"az"` and `"ba"` agree. This generalises canonical forms: choose the key by asking what the equivalence rule cannot change.

### Building output to a specification

**Integer to English Words.** This one runs the other way: instead of reading structure out of a string, you write structure into one. It looks like a page of special cases (teens, tens, zeros in the middle) until you see that English repeats itself every three digits, which turns it into a chunk loop plus one stencil (advanced pattern 2).

**Text Justification.** The first true Hard of the cut-and-reassemble family, and the place where off-by-one errors pile up. Greedy packing with a running width (counting the mandatory space) decides the lines, and `divmod` spreads the padding with extras on the left (advanced pattern 3). The real lesson is to keep the two halves separate and handle the one-word line and the last line before any division.

### The string against itself

**Longest Palindromic Substring.** A palindrome is a string equal to its own mirror, so this is the first problem where you compare a string with itself. The brute force checks every substring. The better idea is to grow mirrors outward from each of the 2n - 1 centres (letters and gaps), so each extension is one comparison and stops at the first mismatch.

**Longest Happy Prefix.** Comparing every prefix with the matching suffix is quadratic. The failure function fills in every prefix's longest border in linear time by extending the previous border or falling back along the border chain. Here you meet KMP from zero, along with the amortised argument that makes the inner loop cheap (advanced pattern 4).

**Shortest Palindrome.** Adding the fewest characters in front means finding the longest palindromic prefix, and checking each prefix from scratch is quadratic. The trick is to glue `s`, a separator and `reverse(s)` together so that the answer becomes one border length (advanced pattern 5). The failure function from the previous problem then does all the work.

**Palindrome Pairs.** Testing all n^2 pairs of words is too slow when words are short and the list is long. Cutting each word at every position, checking which side is a palindrome, and looking up the reverse of the other side in a hash map replaces the pair search with a per-word search (advanced pattern 6). It combines the chapter's two threads: palindrome checks and canonical-key lookup.

**Longest Duplicate Substring.** Every pair of substrings is too many, and even one length takes O(n^2) if you compare windows character by character. Monotonicity in the length allows a binary search, and a rolling hash compares each window in O(1) (advanced pattern 7). The notebook now holds a fingerprint of every window seen so far, which is as far as the scan-and-notebook idea goes in this chapter.
