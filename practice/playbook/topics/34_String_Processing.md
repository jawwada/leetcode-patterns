## String Processing

> A Python string is a frozen row of characters. Reading `s[i]` costs O(1), but every "change" builds a brand-new string. So string algorithms are about **reading** cleverly, with one cursor `i` that only moves right or two pointers closing in from both ends, plus a little memory of what has been seen; and about **building** the answer in a list that you `"".join` once at the end.

[Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) moved two fingers to the right and kept a summary between them. A string parser needs only one finger: a cursor that never moves back. This section is that cursor and the toolbox around it: splitting, reading numbers, keys, palindromes, runs and carries.

**Reach for it when** the input is text and you must **parse** it: split it, read a number or a version. Or **reshape** it: reverse the words, compress runs, write a zigzag. Or compare **letters**, as in shifted strings and palindromes; do **arithmetic on digits** given as text; or find a **repeat**, such as a prefix that is also a suffix or the longest repeated substring. "Longest substring such that ..." is usually a [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) instead.

### The picture

Reading: one cursor that never steps back. Here it splits a string by hand, the classic warm-up.

```text
s = "ab,,c,"   sep = ","      i = the cursor, it only moves right;  start = where the open piece began

    a b , , c ,            index 0 1 2 3 4 5, and the end is 6
   [a b]                   i=2 is ",":  emit s[0:2] = "ab"   start = 3
         []                i=3 is ",":  emit s[3:3] = ""     start = 4    two commas in a row
           [c]             i=5 is ",":  emit s[4:5] = "c"    start = 6
               []          the end:     emit s[6:6] = ""                 the last piece has no "," after it

=> ["ab", "", "c", ""]     the same as "ab,,c,".split(",")
```

Building: collect the pieces in a list and `"".join` them once. Each `out += piece` builds a new string and may copy everything built so far, O(n²) characters over n appends in the worst case. CPython sometimes grows a string in place, but that is an implementation detail, not a promise.

Why it is fast: the brute-force split calls `find`, then slices off the remainder for every piece, which copies the rest of the string each time: O(n²) characters at worst. The cursor keeps one index, `start`, instead of a copy, so each position is compared with the separator once: O(n·m) for a separator of length m, O(n) for one character.

### From idea to code

**The idea in one sentence:** *walk a cursor `i` from left to right; each character either extends the open token or ends it; when a token ends, emit it and open the next one, and emit the last one after the loop.*

The **State** is the cursor `i` plus the **open token**, kept as where it began, `start`, or as its running value, `num` and `sign`; and the output list. The **Definition**: `s[start:i]` is the token read so far, and everything before `start` has been emitted. The **Invariant**, true after every step: every separator that starts before `i` has been cut, and `i` never moves left. A **Step** looks at `s[i]` and either extends the token, `i += 1`, or ends it, emits it and opens the next one past the separator.

The **Record** happens when a token ends, **and once more after the loop**, because the last token has no separator after it; a number parser records early instead, clamping the moment it overflows. **Init** is `i = start = 0` with `parts = []`, or `num, sign = 0, 1`. The **Return** is `parts`, `sign * num` or a flag, and you say out loud what empty input gives: `[""]` for a split, 0 for a number.

The warm-up you are most likely to meet is Implement String Split: cut `"ab,,c,"` at every comma into `['ab', '', 'c', '']`, exactly as `str.split(",")` does. Its sibling is `s.split()` with no argument, where a run of spaces counts as one gap and no empty word comes back. The piece so far is `s[start:i]`, and skipping a gap is `while i < n and s[i] == " ": i += 1`. In both functions the order of two lines is a decision: close the piece with the *old* `start` (RECORD), then move `start` (STEP).

<!-- cell -->

```python
def split_on_char(s, sep):                   # the 6-line answer for a one-character sep
    parts, start = [], 0                     # STATE + INIT: s[start:i] is the open piece
    for i, ch in enumerate(s):
        if ch == sep:
            parts.append(s[start:i])         # RECORD: close the piece (it may be "")
            start = i + 1                    # STEP: the next piece opens after the separator
    parts.append(s[start:])                  # RECORD the last piece: no separator follows it
    return parts                             # RETURN


def split_words(s):                          # like s.split(): runs of spaces, no empty words
    words, i, n = [], 0, len(s)              # STATE + INIT: i = the cursor
    while i < n:
        while i < n and s[i] == " ":         # phase 1: skip the gap
            i += 1
        start = i                            # STEP: a word opens here
        while i < n and s[i] != " ":         # phase 2: read the word
            i += 1
        if start < i:                        # a trailing gap reads an empty word: drop it
            words.append(s[start:i])         # RECORD
    return words                             # RETURN


print(split_on_char("a,,b,", ","), split_on_char("", ","))   # ['a', '', 'b', ''] ['']
print(split_words("  the sky   is blue "))                   # ['the', 'sky', 'is', 'blue']
```

<!-- cell -->

**Try it**
- Delete the last `parts.append(s[start:])` and run `split_on_char("a,b", ",")`: `['a']`. The final piece never meets a separator, so only that line can emit it.
- Change `start = i + 1` to `start = i`: `split_on_char("a,b", ",")` gives `['a', ',b']`, because the separator leaks into the next piece.
- Swap the two lines inside the `if` (move `start` first) and run `split_on_char("a,b", ",")`: `['', 'b']`. Every closed piece is now `s[i + 1:i]`, which is empty.
- Drop the `if start < i:` test (append every time) and run `split_words("the sky  ")`: `['the', 'sky', '']`. A trailing gap reads an empty word.

<!-- cell -->

A separator of any length needs one more idea. A match can start at `i` only while `i <= len(s) - m`, it is tested with `s[i:i + m] == sep`, which is what `s.startswith(sep, i)` does, and the cursor then jumps past the *whole* match. Matches never overlap, so `"aaa"` split on `"aa"` gives `['', 'a']`, as in Python.

Reading a number adds phases, the shape of every number parser. String to Integer (8), the classic atoi, reads an integer from the front of a text: skip the spaces, take at most one sign, read the digits, and clamp to the 32-bit range, so `"   -042abc"` gives −42. A digit is `"0" <= c <= "9"`, its value is `ord(c) - ord("0")`, and it joins the number as `num = num * 10 + d`. The cell holds both parsers.

<!-- cell -->

```python
def split_by_hand(s, sep):                   # any non-empty sep: the same result as s.split(sep)
    if not sep:
        raise ValueError("empty separator")  # what Python does; ask what they want
    parts, start, i, m = [], 0, 0, len(sep)  # STATE + INIT: s[start:i] is the open piece
    while i <= len(s) - m:                   # could a separator start at i?
        if s[i:i + m] == sep:
            parts.append(s[start:i])         # RECORD: close the piece (it may be "")
            i += m                           # STEP: jump over the whole separator ...
            start = i                        # ... and open the next piece right after it
        else:
            i += 1                           # STEP: the open piece grows by one character
    parts.append(s[start:])                  # RECORD the last piece
    return parts                             # RETURN


def my_atoi(s):
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    i, n, sign, num = 0, len(s), 1, 0        # STATE + INIT: cursor, sign, magnitude so far
    while i < n and s[i] == " ":             # phase 1: leading spaces
        i += 1
    if i < n and s[i] in "+-":               # phase 2: at most one sign
        sign = -1 if s[i] == "-" else 1
        i += 1
    while i < n and "0" <= s[i] <= "9":      # phase 3: digits
        num = num * 10 + (ord(s[i]) - ord("0"))   # STEP: append the digit
        if sign * num > INT_MAX:             # RECORD early: clamp the moment it overflows
            return INT_MAX
        if sign * num < INT_MIN:
            return INT_MIN
        i += 1
    return sign * num                        # RETURN: whatever follows the digits is ignored


print(split_by_hand("a,,b,", ","), split_by_hand("aaa", "aa"))       # ['a', '', 'b', ''] ['', 'a']
print(my_atoi("   -042abc"), my_atoi("+7"), my_atoi("-91283472332"))  # -42 7 -2147483648
```

<!-- cell -->

**Try it**
- Change `<=` to `<` in `while i <= len(s) - m:` and run `split_by_hand("a,", ",")` and `split_by_hand(",", ",")`: `['a,']` and `[',']` instead of `['a', '']` and `['', '']`, because the last position is never tested. Then try `while i < len(s):`: every result is right again.
- Change `i += m` to `i += 1` and run `split_by_hand("aaa", "aa")`: `['', '', 'a']` instead of `['', 'a']`, because the two matches overlap.
- Add `print(i, s[i], num)` right after the `num = ...` line and run `my_atoi("  -042x")`: `3 0 0`, `4 4 4`, `5 2 42`. The number is built without its sign; the sign is applied at the end.

<!-- cell -->

### Watch it work

The trace runs the general split on `"ab,,c,"` and prints a line each time a piece is closed: where the cursor found a separator, which slice it emitted, and where the next piece starts. The last line is the tail, the one piece the loop itself never closes.

<!-- cell -->

```python
def trace_split(s, sep):
    parts, start, i, m = [], 0, 0, len(sep)
    print(f"s={s!r}  sep={sep!r}")
    while i <= len(s) - m:
        if s[i:i + m] == sep:
            parts.append(s[start:i])
            print(f"i={i}: separator -> emit s[{start}:{i}] = {s[start:i]!r:5} next piece starts at {i + m}")
            i += m
            start = i
        else:
            i += 1
    parts.append(s[start:])
    print(f"end: emit the last piece s[{start}:] = {s[start:]!r}")
    return parts


print(trace_split("ab,,c,", ","))   # ['ab', '', 'c', '']
```

<!-- cell -->

**Try it**
- Run `trace_split(",a,,", ",")` and predict the pieces first: `['', 'a', '', '']`. A separator at the very start closes an empty first piece.
- Run `trace_split("a--b---c", "--")`: `['a', 'b', '-c']`. After the match at index 4 the cursor jumps to 6, so the third `-` stays in the last piece, exactly as `str.split` does.
- Swap `i += m` and `start = i` (set `start` first) and run `trace_split("a,b", ",")`: `['a', ',b']`. The new piece now starts *on* the separator.
- Give `split_by_hand` a parameter `maxsplit=-1` and loop `while i <= len(s) - m and len(parts) != maxsplit:`. It now matches `s.split(sep, maxsplit)`: `split_by_hand("a,b,c", ",", 1)` is `['a', 'b,c']`, and the tail append needs no change.

<!-- cell -->

### Where it goes wrong

1. **Forgetting the last piece.** Emitting only when a separator is seen drops the tail: `"a,b"` gives `["a"]`. Fix: `parts.append(s[start:])` after the loop; it also makes `""` give `[""]` and `"a,"` give `["a", ""]`, like Python.
2. **`+=` in a loop.** Each `+=` builds a new string and may copy everything so far: O(n²) characters over n appends. Fix: append pieces to a list, `"".join` once.
3. **Reading `s[i]` before checking `i < n`.** `"-"` or `"   "` makes a parser read past the end (`IndexError`). Fix: every `while` starts with `i < n and ...`.
4. **A branch that never moves the cursor.** Every path through the body of `while i < n` must advance `i` or leave the loop; a branch that forgets spins forever on the first character that reaches it. Replace the `i += 1` of phase 2 in `split_words` with `pass`, and `split_words("a")` never returns. Fix: before running, point at the `i += ...` in each branch.
5. **`isdigit()` as the digit test.** `"²".isdigit()` is True, yet `int("²")` raises `ValueError`. Fix: `"0" <= c <= "9"`.
6. **Clamping too late, or not at all.** Python ints never overflow, so the bug hides: `"-91283472332"` must give `-2147483648`. Fix: check after every digit; in Java or C++, check *before* multiplying, with `num > (INT_MAX - d) / 10`.
7. **Moving by 1 after a separator match.** Matches must not overlap: `"aaa"` split on `"aa"` is `["", "a"]`. Fix: `i += len(sep)`.
8. **Comparing numbers as strings.** `"1.01" != "1.001"` as strings, yet they are the same version, and `"10" < "9"` is True. Fix: parse each field into an int (`x = x * 10 + d`).
9. **A 26-slot count on text that isn't lowercase.** `ord(ch) - ord("a")` sends `"Z"` into the `'t'` slot and `"A"` out of range ([Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets), trap 3). Ask the alphabet; otherwise key on `"".join(sorted(w))` or a `Counter`.
10. **Deleting while scanning.** Removing characters from the list you are indexing shifts every later index: `del chars[i]` in Minimum Remove turns `"a)b)c"` into `'ab)'`. Fix: mark (`chars[i] = ""`) during the scan and join once at the end.
11. **The palindrome expansion overshoots.** The `while` stops one step past the palindrome on both sides, `lo = -1` and `hi = 3` on `"aba"`, so the palindrome is `s[lo + 1:hi]`, of length `hi - lo - 1`.

### Edge cases to say out loud

Empty string · only separators, only spaces · a separator at the start, at the end, twice in a row · a separator that overlaps itself (`"aaa"` on `"aa"`) · one character · a sign with no digits (`"+"`) · overflow both ways · leading zeros · uppercase, digits or spaces where the code assumes lowercase letters (ask the alphabet) · non-ASCII text (Python indexes code points; one visible character can be several of them). The asserts below check the splitters against Python's own `split` and walk `my_atoi` through the number cases.

<!-- cell -->

```python
for text in ["", ",", ",a,", "abc", "a,,b,"]:
    assert split_on_char(text, ",") == split_by_hand(text, ",") == text.split(",")
for text in ["", "   ", " a  b ", "x"]:
    assert split_words(text) == text.split()
assert split_by_hand("aaa", "aa") == ["", "a"] and split_by_hand("a--b----c", "--") == ["a", "b", "", "c"]
assert my_atoi("") == 0 and my_atoi("   ") == 0      # nothing to read
assert my_atoi("+") == 0 and my_atoi("-") == 0       # a sign with no digits
assert my_atoi("+-12") == 0                          # only one sign is allowed
assert my_atoi("  + 4") == 0                         # no space between sign and digits
assert my_atoi("2147483647") == 2**31 - 1            # exactly INT_MAX is fine
assert my_atoi("2147483648") == 2**31 - 1            # one more: clamp
assert my_atoi("-2147483648") == -2**31              # INT_MIN itself is reachable
assert my_atoi("0000123") == 123                     # leading zeros
assert my_atoi("²") == 0                             # not an ASCII digit
print("edge cases pass")
```

<!-- cell -->

**Try it**
- Compare `" a  b ".split(" ")` with `" a  b ".split()`: `['', 'a', '', 'b', '']` versus `['a', 'b']`. The first is `split_on_char`, the second is `split_words`; ask which one the problem means.
- Predict, then check: `my_atoi("-0012a42")` is -12 and `my_atoi("3.14")` is 3; the scan stops at the first non-digit.
- Add `assert split_on_char("a", "a") == ["", ""]` and predict whether it passes before running it (it does: one separator, two empty pieces).

<!-- cell -->

### Variations

Every variation is the same cursor with one more piece of memory: a second cursor, a flag, a key, a center, a carry. The table is the overview; its first three rows are the templates above, and the rest follow the order of the cells below.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Split on one character** | emit at each separator, and once more at the end | Implement String Split, the warm-up |
| **Split on runs of spaces** | phases: skip the gap, read a word; drop the empty word a trailing gap reads | Reverse Words in a String (151): the words in reverse order; Length of Last Word (58) |
| **Read a number** | phases spaces → sign → digits; `num = num * 10 + d`; clamp | String to Integer (8) |
| **Two cursors in lockstep** | read one field from each string, compare, step over the dots | Compare Version Numbers (165): which of two versions is larger |
| **Quoted fields** | a flag flips at each `"`; a separator cuts only outside quotes | the split follow-up |
| **Difference key** | the tuple of `(s[i+1] - s[i]) % 26` forgets the shift | Group Shifted Strings (249): group the words that shift into each other |
| **Expand around center** | 2n − 1 centers; grow while both ends match | Longest Palindromic Substring (5); Palindromic Substrings (647): count them all |
| **One deletion allowed** | two pointers; at the first mismatch, try skipping either side | Valid Palindrome II (680): a palindrome after deleting at most one letter |
| **Runs** | `j` walks to the end of the run; the next run starts at `j` | Expressive Words (809): can a word stretch into `s`; String Compression (443): `aaabb` → `a3b2` in place; Count and Say (38): read the previous term's runs aloud |
| **Digits with a carry** | walk both strings from the right; `divmod(d, 10)`; build backwards | Add Strings (415): add two numbers given as text; Add Binary (67); Multiply Strings (43) |
| **Mark, then join** | stack of open-bracket indices; blank what can't be matched | Minimum Remove to Make Valid Parentheses (1249) |
| **Reverse twice** | reverse the whole list, then reverse each word back | Reverse Words in a String (151); Reverse Words in a String II (186): the same, in place |
| **Row buckets** | a row index bouncing between 0 and numRows − 1; one list per row | Zigzag Conversion (6): write the string in a zigzag, read it row by row |
| *Second pass:* **grammar flags** | three flags instead of a value; the `e` resets "digit seen" | Valid Number (65): is the text a decimal or scientific number |
| *Second pass:* **chunks of three** | base 1000: each chunk is spelled alike, then its scale word | Integer to English Words (273): spell a number in English words |
| *Second pass:* **cut + hash map** | cut each word in two; one half a palindrome, the other half's reverse a whole word | Palindrome Pairs (336): the pairs of words that join into a palindrome |
| *Second pass:* **KMP borders** | `fail[i]` = the longest proper border of `s[:i + 1]`; on a mismatch, fall back | Longest Happy Prefix (1392): the longest prefix that is also a suffix; Shortest Palindrome (214): the fewest letters added in front; Find the Index of the First Occurrence in a String (28) |
| *Second pass:* **rolling hash + binary search** | binary search the length; a rolling hash tests one length in O(n) | Longest Duplicate Substring (1044): the longest substring that occurs twice |
| *Second pass:* **greedy packing + divmod** | pack words greedily; `divmod(spaces, gaps)` puts the extras on the left | Text Justification (68): lines of exactly `width` characters |

Many string problems are taught where their technique lives:

| Problems | Technique | Section |
|---|---|---|
| longest without repeats, minimum window, permutation in string, all anagrams (3, 76, 567, 438) | a window with letter counts | [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) |
| valid palindrome with punctuation (125) | two pointers that skip non-letters | [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers) |
| brackets, decode string, calculators, simplify path (20, 394, 224, 227, 71) | a stack | [Stacks & Queues](00_Topic_Index.ipynb#s07) |
| anagram counts, group anagrams, encode/decode strings (242, 49, 271) | a fingerprint key; length-prefix framing | [Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets) |
| word search II, word squares (212, 425) | a trie walked along the board | [Tries](14_Tries.ipynb#topic-tries) |
| phone letters, IP addresses, palindrome partitioning (17, 93, 131) | backtracking over cuts | [Backtracking](19_Backtracking.ipynb#topic-backtracking) |

**Two cursors and a quote flag.** The first variations stay with parsing. Compare Version Numbers compares two versions field by field as integers and returns −1, 0 or 1: `"1.01"` equals `"1.001"`, and `"1.0"` is smaller than `"1.0.1"`. Run two cursors in lockstep, read one field from each string as a number, and let the first different field decide. A string that has run out simply reads as 0, which is exactly the rule that missing revisions count as 0.

<!-- cell -->

```python
def compare_version(v1, v2):                 # O(n + m) time, O(1) extra space
    i = j = 0
    while i < len(v1) or j < len(v2):        # until BOTH strings are used up
        x = 0
        while i < len(v1) and v1[i] != ".":  # read one field; a used-up string gives 0
            x = x * 10 + int(v1[i])
            i += 1
        y = 0
        while j < len(v2) and v2[j] != ".":
            y = y * 10 + int(v2[j])
            j += 1
        if x != y:
            return -1 if x < y else 1        # the first different field decides
        i += 1                               # step over the dots
        j += 1
    return 0


print(compare_version("1.01", "1.001"), compare_version("1.0", "1.0.1"), compare_version("1.10", "1.9"))   # 0 -1 1
```

<!-- cell -->

**Try it**
- Change `or` to `and` in `while i < len(v1) or j < len(v2)` and run `compare_version("1.0.1", "1")`: 0 instead of 1. The loop stopped when the shorter string ran out.
- Run `"10" < "9"` and `10 < 9`: `True` and `False`. Strings compare character by character, which is why each field is parsed into an int before `compare_version("1.10", "1.9")` can return 1.
- Run `compare_version("1", "1.0.0.0")`: 0. The used-up string keeps reading 0 while the other one still has fields.

<!-- cell -->

Quoted fields are the classic follow-up to the split warm-up: `'1,"Smith, John",42'` must give `['1', 'Smith, John', '42']`. One flag remembers whether the cursor is inside quotes. A quote flips the flag and is not kept, a separator closes the field only while the flag is off, and every other character joins the open field. The last field is emitted after the loop, exactly as in the warm-up.

**Keys: group by "the same up to ...".** Group Shifted Strings groups the words that turn into each other when every letter moves the same number of steps along the alphabet: `"abc"`, `"bcd"` and `"xyz"` form one group, `"az"` and `"ba"` another. Compute a key that forgets exactly that change, and a dict does the grouping. A shift forgets the starting letter but keeps the gaps between neighbours, taken mod 26 so that `z → a` is a gap of 1. Anagrams forget the order instead; their key is built in [Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets).

<!-- cell -->

```python
def group_by_key(words, key):
    groups = defaultdict(list)               # key -> the words that share it
    for w in words:
        groups[key(w)].append(w)
    return list(groups.values())


def shift_key(w):                            # the gaps between neighbours, mod 26
    return tuple((ord(b) - ord(a)) % 26 for a, b in zip(w, w[1:]))


print(group_by_key(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"], shift_key))
# [['abc', 'bcd', 'xyz'], ['acef'], ['az', 'ba'], ['a', 'z']]
```

<!-- cell -->

**Try it**
- Drop the `% 26` from `shift_key` and rerun: `'az'` and `'ba'` land in different groups, because their gaps are now 25 and -1.
- Print `shift_key("a")` and `shift_key("z")`: both `()`, so all one-letter words form one group. That is right: any letter shifts into any other.
- Predict which group `"cb"` joins before adding it: `shift_key("cb")` is `(25,)`, the same as `"az"` and `"ba"`, so all three shift into each other.

<!-- cell -->

**Runs and carries.** A *run* is a block of equal letters: a second cursor `j` walks to its end, and the next run starts at `j`. Expressive Words asks whether a word can be stretched into `s` by growing some of its runs to length 3 or more: `"hello"` stretches into `"heeellooo"`, and `"helo"` does not. Compare the runs of the two strings pair by pair; String Compression and Count and Say write the runs out instead.

Add Strings adds two non-negative numbers given as text: `"999"` plus `"1"` is `"1000"`. Walk both strings from the right with a carry, as on paper, and build the answer backwards; a string that has run out adds nothing, and a last carry needs a turn of its own. All of these are O(n).

<!-- cell -->

```python
def runs(s):                                 # "aaabcc" -> [('a', 3), ('b', 1), ('c', 2)]
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:   # j walks to the end of this run
            j += 1
        out.append((s[i], j - i))            # RECORD the run
        i = j                                # STEP: the next run starts where this one ended
    return out


def expressive(s, word):                     # can word be stretched into s? (809)
    a, b = runs(s), runs(word)
    return len(a) == len(b) and all(c1 == c2 and (k1 == k2 or (k1 >= 3 and k1 > k2))
                                    for (c1, k1), (c2, k2) in zip(a, b))


def add_strings(a, b):                       # 415: digit by digit from the right
    i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:         # any digit or carry left
        d = carry
        if i >= 0:
            d += ord(a[i]) - ord("0")
            i -= 1
        if j >= 0:
            d += ord(b[j]) - ord("0")
            j -= 1
        carry, digit = divmod(d, 10)
        out.append(str(digit))
    return "".join(reversed(out))            # built backwards: reverse once


print(runs("aaabcc"), expressive("heeellooo", "hello"), expressive("heeellooo", "helo"))
# [('a', 3), ('b', 1), ('c', 2)] True False
print(add_strings("999", "1"), add_strings("11", "123"))   # 1000 134
```

<!-- cell -->

**Try it**
- Change `i = j` to `i = j + 1` and run `runs("aaabcc")`: `[('a', 3), ('c', 2)]`. The `b` run vanishes, because the next run already starts at `j`.
- Predict `expressive("zzzzzyyyyy", "zzyy")` and `expressive("aaa", "aaaa")`: True (both runs can grow to 5) and False (a run can't shrink).
- Drop `or carry` from the loop and run `add_strings("999", "1")`: `'000'`. The last carry needs one more turn of the loop.

<!-- cell -->

**Mark, then join; reverse twice; row buckets.** The last three reshape a string in one pass each. Minimum Remove to Make Valid Parentheses deletes the fewest brackets so that the rest is balanced: `"lee(t(c)o)de)"` loses its last `)`. A stack of the indices of `(` still open finds exactly what must go: a `)` with nothing to close, and every `(` still open at the end. Blank them during the scan, and join once.

Reverse Words in a String puts the words in reverse order with single spaces: `"  the sky   is blue "` becomes `"blue is sky the"`. In Python, say `" ".join(reversed(s.split()))` first; reversing twice is the follow-up for a mutable list of characters. Reversing the whole list puts the words in the right order but spells each one backwards, and a second sweep reverses each word back.

Zigzag Conversion writes the string down and up across `num_rows` rows and reads it row by row: `"PAYPALISHIRING"` on 3 rows reads `"PAHNAPLSIIGYIR"`. Only the *row* of each character matters, and the row bounces 0, 1, ..., num_rows − 1, ..., 1, 0, so keep one list per row and a step of +1 or −1.

<!-- cell -->

```python
def min_remove_to_make_valid(s):
    chars, open_idx = list(s), []            # open_idx = indices of "(" still waiting for a partner
    for i, ch in enumerate(s):
        if ch == "(":
            open_idx.append(i)
        elif ch == ")":
            if open_idx:
                open_idx.pop()               # matched with the most recent "("
            else:
                chars[i] = ""                # nothing to close: mark it, delete later
    for i in open_idx:
        chars[i] = ""                        # never closed
    return "".join(chars)                    # every deletion happens here, at once


def reverse_words(s):
    chars = list(" ".join(s.split()))        # one space between words (a write pointer does this in place)
    def flip(lo, hi):
        while lo < hi:
            chars[lo], chars[hi] = chars[hi], chars[lo]
            lo, hi = lo + 1, hi - 1
    flip(0, len(chars) - 1)                  # "the sky" -> "yks eht": right order, backwards words
    start = 0
    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":
            flip(start, i - 1)               # spell this word forwards again
            start = i + 1
    return "".join(chars)


def zigzag(s, num_rows):
    if num_rows == 1 or num_rows >= len(s):
        return s
    rows, r, step = [[] for _ in range(num_rows)], 0, 1
    for ch in s:
        rows[r].append(ch)
        if r == 0:
            step = 1                         # bounce off the top row
        elif r == num_rows - 1:
            step = -1                        # bounce off the bottom row
        r += step
    return "".join("".join(row) for row in rows)


print(min_remove_to_make_valid("lee(t(c)o)de)"), repr(min_remove_to_make_valid("))((")))   # lee(t(c)o)de ''
print(reverse_words("  the sky   is blue "), zigzag("PAYPALISHIRING", 3))                   # blue is sky the PAHNAPLSIIGYIR
```

<!-- cell -->

**Try it**
- Print `open_idx` after the loop for `"(a(b(c)d)"`: `[0]`. Only the first `(` never found a partner, so the answer is `'a(b(c)d)'`.
- Replace `chars[i] = ""` in the `)` branch with `del chars[i]` and rerun the cell: `IndexError` on `"))(("`, because the saved indices of the `(` now point past the end of the shorter list. On `"a)b)c"` it fails quietly instead, returning `'ab)'`.
- Remove the second loop (the per-word flips) and run `reverse_words("the sky is blue")`: `'eulb si yks eht'`, halfway there.
- Remove the early `return s` (the first `if` in `zigzag`) and run `zigzag("AB", 1)`: `IndexError`. With one row the step never flips, so `r` walks off to row 1.

<!-- cell -->

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Valid Number asks whether a text is a number in decimal or scientific notation: `"2"`, `"-.9"`, `"4."` and `"3e+7"` are, while `"e3"`, `"99e2.5"`, `"."` and `"1e"` are not. It keeps three flags instead of a value, because each character is legal or not depending only on what has been seen. A sign stands only at the start or right after the `e`; there is one dot, never inside the exponent; and one `e`, with digits before it. The exponent needs digits of its own, so the `e` resets "digit seen".

<details><summary>Valid Number in code</summary>

```py
def is_number(s):
    seen_digit = seen_dot = seen_exp = False # the whole memory of this state machine
    for i, c in enumerate(s):
        if "0" <= c <= "9":
            seen_digit = True
        elif c in "+-":
            if i > 0 and s[i - 1] not in "eE":   # a sign only at the start or right after e
                return False
        elif c == ".":
            if seen_dot or seen_exp:         # one dot, and never inside the exponent
                return False
            seen_dot = True
        elif c in "eE":
            if seen_exp or not seen_digit:   # one e, with digits before it
                return False
            seen_exp, seen_digit = True, False   # the exponent needs digits of its own
        else:
            return False                     # a space, a letter, anything else
    return seen_digit

# [is_number(t) for t in ["2", "-.9", "4.", "3e+7", "e3", "99e2.5", ".", "1e"]]
#  -> [True, True, True, True, False, False, False, False]
# without the reset of seen_digit at the e, "1e" would pass
```

</details>

Integer to English Words spells a number in English: 12345 is `"Twelve Thousand Three Hundred Forty Five"`. Work in base 1000, because every 3-digit chunk is spelled the same way and then followed by its scale word, Thousand, Million or Billion. Read the chunks lowest first and put each new one in front of the words so far. An all-zero chunk adds nothing, not even its scale word.

<!-- cell -->

```python
ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven",
        "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

def number_to_words(num):
    if num == 0:
        return "Zero"
    def chunk(n):                            # the words for 1 <= n <= 999
        words = []
        if n >= 100:
            words += [ONES[n // 100], "Hundred"]
            n %= 100
        if n >= 20:
            words.append(TENS[n // 10])
            n %= 10
        if n:
            words.append(ONES[n])            # 1..19 each have their own word
        return words
    out = []
    for scale in ["", "Thousand", "Million", "Billion"]:   # three digits at a time, lowest first
        if num % 1000:                       # an all-zero chunk adds nothing, not even its scale
            out = chunk(num % 1000) + ([scale] if scale else []) + out
        num //= 1000
    return " ".join(out)


print(number_to_words(12345), "|", number_to_words(1000010))   # Twelve Thousand Three Hundred Forty Five | One Million Ten
```

<!-- cell -->

**Try it**
- Remove the `if num % 1000:` guard and run `number_to_words(1000000)`: `'Billion One Million Thousand'`. Empty chunks must stay silent, scale word included.
- Change `if n >= 20:` to `if n > 20:` and run `number_to_words(20)`: `IndexError`. Twenty now falls through to `ONES[20]`, and `ONES` stops at Nineteen.
- Append each chunk instead, `out = out + chunk(num % 1000) + ...`, and run `number_to_words(12345)`: `'Three Hundred Forty Five Twelve Thousand'`. The chunks arrive lowest first, so each new one belongs in front.

<!-- cell -->

Longest Duplicate Substring asks for the longest substring that occurs at least twice, overlaps allowed: `"banana"` gives `"ana"`. It stacks two ideas. If a substring of length L occurs twice, so does its prefix of length L − 1, so "a repeat of length L exists" is true up to the answer and false after it: binary search the length, as in [Binary Search](11_Binary_Search.ipynb#topic-binary-search).

To test one length in O(n), read each window as a number in base B, modulo a big prime, and *roll* it one step in O(1): in base 10 the window `"123"` becomes `"234"` as 123 · 10 − 1 · 1000 + 4 = 234. Equal strings have equal hashes, and an equal hash is confirmed by comparing letters, because different strings can share one: collisions cost time, never correctness. The whole search is O(n log n) expected.

In Java or C++, add the modulus back after the subtraction; Python's `%` never returns a negative number. The rolling hash itself is coded in `practice/simple/basics/strings/04_rabin_karp_rolling_hash.py`, with a tiny modulus that makes the collisions visible.

Text Justification lays words out in lines of exactly `width` characters with straight edges: at width 16, `["This", "is", "an", "example", "of", "text", "justification."]` becomes three lines, the first `'This    is    an'`. There is no trick, just two jobs done cleanly in O(total characters). Pack as many words as fit on the line, greedily, and spread the spare spaces with one `divmod`: every gap gets the quotient, and the leftmost `remainder` gaps get one more. The last line, and a line with one word, are left-justified.

<!-- cell -->

```python
def full_justify(words, width):
    lines, i = [], 0
    while i < len(words):
        j, used = i + 1, len(words[i])       # the line is words[i:j]; used = its letters + 1 space per gap
        while j < len(words) and used + 1 + len(words[j]) <= width:
            used += 1 + len(words[j])
            j += 1
        line, gaps = words[i:j], j - i - 1
        if j == len(words) or gaps == 0:     # last line or a single word: left-justify
            text = " ".join(line)
            lines.append(text + " " * (width - len(text)))
        else:
            q, r = divmod(width - sum(map(len, line)), gaps)
            pieces = []
            for k in range(gaps):            # gap k gets q spaces, plus one if k < r
                pieces.append(line[k] + " " * (q + (1 if k < r else 0)))
            lines.append("".join(pieces) + line[-1])
        i = j
    return lines


print(full_justify(["This", "is", "an", "example", "of", "text", "justification."], 16))
# ['This    is    an', 'example  of text', 'justification.  ']
```

<!-- cell -->

**Try it**
- Work out the second line by hand: `"example"`, `"of"`, `"text"` hold 13 letters, so 3 spaces go into 2 gaps: `divmod(3, 2)` is `(1, 1)`, and the left gap gets the extra one.
- Change `<=` to `<` in the packing loop and run `full_justify(["ab", "cd"], 5)`: `['ab   ', 'cd   ']` instead of `['ab cd']`. A line that fits exactly is legal.
- Remove `j == len(words) or` and run `full_justify(["What", "must", "be", "acknowledgment", "shall", "be"], 16)`: the last line becomes `'shall         be'` (nine spaces in one gap) instead of `'shall be        '`.

<!-- cell -->

### Say it in the interview

> "Two questions first: if two separators are adjacent, do you want an empty string between them, like `split(",")`, or should a run count as one, like `split()`? And can the separator be longer than one character? I'll walk the string once with an index and remember where the current piece started."

> "When the separator starts at `i` I emit `s[start:i]`, which may be empty, jump past the whole separator, and start the next piece there. After the loop I emit the tail; that line makes `"a,"` give `["a", ""]` and `""` give `[""]`. Each position compares up to m characters, so O(n·m), which is O(n) for one character, plus O(n) for the output. Using `find` and slicing off the remainder copies the rest of the string per piece, which is O(n²) at worst."

For any string problem, ask: which alphabet, case-sensitive or not, can it be empty? Then say the edge cases *before* coding (empty string, separator at both ends, two in a row) and point at the final `append` after the loop: it is the line most people forget. For a parser, name the phases out loud ("spaces, then one sign, then digits") and write one `while` per phase.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Compare Version Numbers | `strings/compare_version_numbers.py` | two cursors parse one field each as an int; a used-up string reads as 0 |
| Group Shifted Strings | `strings/group_shifted_strings.py` | key = gaps between neighbours mod 26; a shift doesn't change the gaps |
| Implement String Split (warm-up) | `strings/implement_split.py` | cursor + piece start; emit at each separator, jump past it, emit the tail after the loop |
| Integer to English Words | `strings/integer_to_english_words.py` | chunks of three digits from the right, each spelled alike plus Thousand/Million/Billion; skip zero chunks |
| Longest Duplicate Substring | `strings/longest_duplicate_substring.py` | binary search the length (repeats are monotone); a rolling hash tests one length in O(n) |
| Longest Happy Prefix | `strings/longest_happy_prefix.py` | KMP prefix function; the answer is `s[:fail[-1]]` |
| Longest Palindromic Substring | `strings/longest_palindromic_substring.py` · `practice/simple/50_longest_palindromic_substring.py` | expand around all 2n − 1 centers; the palindrome is `s[lo + 1:hi]` when the loop stops |
| Minimum Remove to Make Valid Parentheses | `strings/minimum_remove_to_make_valid_parentheses.py` | stack of open indices; blank unmatched `)` at once and leftover `(` at the end; join once |
| Palindrome Pairs | `strings/palindrome_pairs.py` | cut each word: one half a palindrome, the other half's reverse found in a dict of reversed words |
| Reverse Words in a String | `strings/reverse_words_in_a_string.py` | squeeze the spaces, reverse the whole list, then reverse each word back |
| Shortest Palindrome | `strings/shortest_palindrome.py` | longest palindromic prefix = border of `s + "#" + reverse(s)`; prepend the rest reversed |
| Simplify Path | `strings/simplify_path.py` | split on "/"; a stack of names: push a name, pop on "..", skip "" and "." ([Stacks & Queues](00_Topic_Index.ipynb#s07)) |
| String to Integer (atoi) | `strings/string_to_integer_atoi.py` | phases spaces → sign → digits; `num = num * 10 + d`; clamp the moment it overflows |
| Text Justification | `strings/text_justification.py` | greedy packing; `divmod(spaces, gaps)` with extras on the left; last line left-justified |
| Valid Anagram | `strings/valid_anagram.py` | one 26-count array: +1 for s, −1 for t; anagrams iff all counts are 0 (lowercase only: ask) |
| Valid Number | `strings/valid_number.py` | three flags (digit, dot, exponent); a sign only at the start or after e; e resets "digit seen" |
| Zigzag Conversion | `strings/zigzag_conversion.py` | only the row matters: a row index bouncing between the edges, one list per row |

### Self-check

1. Why does `split_on_char` append once more after the loop, and what does that give for `""` and for `"a,"`?
<details><summary>Answer</summary>The last piece has no separator after it, so nothing inside the loop ever closes it. For <code>""</code> it emits the empty piece: <code>[""]</code>. For <code>"a,"</code> it emits the empty tail: <code>["a", ""]</code>. Both match Python's <code>str.split</code>.</details>

2. `" a  b ".split(" ")` or `" a  b ".split()`: which one did the interviewer mean, and how would each change your code?
<details><summary>Answer</summary><code>split(" ")</code> keeps an empty piece between adjacent spaces and at both ends: <code>['', 'a', '', 'b', '']</code>; that is <code>split_on_char</code>. <code>split()</code> treats a run of spaces as one gap and returns no empty words: <code>['a', 'b']</code>; that is <code>split_words</code>, with a phase that skips the gap and a check that drops the empty word a trailing gap reads.</details>

3. The KMP table has a `while` inside a `for`. Why is building it still O(n)?
<details><summary>Answer</summary><code>k</code> grows by at most 1 per character, so it grows at most n times in total, and every turn of the <code>while</code> makes it smaller. It cannot shrink more often than it grew, so all the <code>while</code> turns together cost at most n.</details>

4. In Longest Duplicate Substring, why may you binary search on the length, and why compare letters after a hash hit?
<details><summary>Answer</summary>If a substring of length L occurs twice, its first L − 1 letters also occur twice, so feasibility is true up to the answer and false after it: monotone, so binary search works. Two different strings can have the same hash (a collision), so a hash hit is only a candidate until the letters agree.</details>
