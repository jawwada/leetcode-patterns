## Strings

> A Python string is a frozen row of characters. Reading `s[i]` costs O(1), but every "change" builds a brand-new string. So string algorithms are about **reading** cleverly (one cursor `i` that only moves right, or two pointers closing in from both ends, plus a little memory of what has been seen) and **building** the answer in a list that you `"".join` once at the end.

**Reach for it when** the input is text and you must **parse** it (split, a number, a version), **reshape** it (reverse the words, compress runs, zigzag), compare **letters** (shifted strings, palindromes), do **arithmetic on digits** given as text, or find a **repeat** (a prefix that is also a suffix, the longest repeated substring). "Longest substring such that ..." is usually a [Sliding Window](#s06) instead.

**In this repo:** `strings/` (17 problems) · bank: `practice/simple/50_longest_palindromic_substring.py` · basics: `practice/simple/basics/strings/01_character_counting_and_anagrams.py`, `practice/simple/basics/strings/02_two_pointer_palindromes_and_reverse_words.py`, `practice/simple/basics/strings/03_kmp_prefix_function.py`, `practice/simple/basics/strings/04_rabin_karp_rolling_hash.py`, `practice/simple/basics/strings/05_encode_decode_strings_and_join.py`

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

Building: collect the pieces in a list and `"".join` them once. Each `out += piece` builds a new string and may copy everything built so far, O(n²) characters over n appends in the worst case (CPython sometimes grows a string in place, but that is an implementation detail, not a promise).

Why it is fast: the brute-force split calls `find`, then slices off the remainder for every piece, which copies the rest of the string each time: O(n²) characters at worst. The cursor keeps one index, `start`, instead of a copy, so each position is compared with the separator once: O(n·m) for a separator of length m, O(n) for one character.

### From idea to code

**The idea in one sentence:** *walk a cursor `i` from left to right; each character either extends the open token or ends it; when a token ends, emit it and open the next one, and emit the last one after the loop.*

| Decision | Cursor-scan answer |
|---|---|
| **State**: what must I remember? | the cursor `i`, plus the **open token**: where it began (`start`) or its running value (`num`, `sign`, a few flags); and the output list |
| **Definition**: what exactly does each variable mean? | `s[start:i]` = the token read so far; everything before `start` has been emitted |
| **Invariant**: what is true at the end of every step? | every separator that starts before `i` has been cut, `s[start:i]` is the open piece, and `i` never moves left |
| **Step**: how does one character change the state? | look at `s[i]` (or `s[i:i + m]`): it extends the token (`i += 1`) or ends it (emit, jump past the separator, `start = i`) |
| **Record**: when is the answer updated? | when a token ends, **and once more after the loop**: the last token has no separator after it (atoi: clamp the moment it overflows) |
| **Init**: starting values | `i = start = 0`, `parts = []` (or `num, sign = 0, 1`) |
| **Return**: what comes back, and for "not found"? | `parts`, `sign * num` or a flag; say out loud what empty input gives (`[""]` for split, `0` for atoi) |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "while there is still input" | `while i < n:` (check it before every `s[i]`) |
| "could a separator start at i?" | `while i <= len(s) - m:` (`while i < len(s)` also works in Python: a slice running off the end is shorter than `sep`, never equal to it) |
| "skip the spaces" | `while i < n and s[i] == " ": i += 1` |
| "is it a digit?" | `"0" <= s[i] <= "9"` (not `s[i].isdigit()`, which also says yes to `"²"`) |
| "its value" | `ord(s[i]) - ord("0")` |
| "append the digit to the number" | `num = num * 10 + digit` |
| "a separator starts here" | `s[i:i + m] == sep` (or `s.startswith(sep, i)`) |
| "the piece so far" | `s[start:i]` |
| "emit it, open the next piece" | `parts.append(s[start:i])`, then `i += m` and `start = i` |
| "build the output" | `parts.append(piece)` ... then `"".join(parts)` once |

The warm-up you are most likely to meet is a split on one character. Its sibling is `s.split()` with no argument, where a run of spaces counts as one gap and no empty words come back. In both, the order of the two middle lines is a decision: close the piece with the *old* `start` (RECORD), then move `start` (STEP).

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

**Try it**
- Delete the last `parts.append(s[start:])` and run `split_on_char("a,b", ",")`: `['a']`. The final piece never meets a separator, so only that line can emit it.
- Change `start = i + 1` to `start = i`: `split_on_char("a,b", ",")` gives `['a', ',b']`, because the separator leaks into the next piece.
- Swap the two lines inside the `if` (move `start` first) and run `split_on_char("a,b", ",")`: `['', 'b']`. Every closed piece is now `s[i + 1:i]`, which is empty.
- Drop the `if start < i:` test (append every time) and run `split_words("the sky  ")`: `['the', 'sky', '']`. A trailing gap reads an empty word.

A separator of any length needs one more idea: test for a match at each position and jump past the *whole* match. Reading a number adds phases, the shape of every number parser.

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

**Try it**
- Change `<=` to `<` in `while i <= len(s) - m:` and run `split_by_hand("a,", ",")` and `split_by_hand(",", ",")`: `['a,']` and `[',']` instead of `['a', '']` and `['', '']`, because the last position is never tested. Then try `while i < len(s):`: every result is right again.
- Change `i += m` to `i += 1` and run `split_by_hand("aaa", "aa")`: `['', '', 'a']` instead of `['', 'a']`, because the two matches overlap.
- Add `print(i, s[i], num)` right after the `num = ...` line and run `my_atoi("  -042x")`: `3 0 0`, `4 4 4`, `5 2 42`. The number is built without its sign; the sign is applied at the end.

### Watch it work

The general split, printing each time a piece is closed: where the cursor found a separator and which slice it emitted.

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

**Try it**
- Run `trace_split(",a,,", ",")` and predict the pieces first: `['', 'a', '', '']`. A separator at the very start closes an empty first piece.
- Run `trace_split("a--b---c", "--")`: `['a', 'b', '-c']`. After the match at index 4 the cursor jumps to 6, so the third `-` stays in the last piece, exactly as `str.split` does.
- Swap `i += m` and `start = i` (set `start` first) and run `trace_split("a,b", ",")`: `['a', ',b']`. The new piece now starts *on* the separator.
- Give `split_by_hand` a parameter `maxsplit=-1` and loop `while i <= len(s) - m and len(parts) != maxsplit:`. It now matches `s.split(sep, maxsplit)`: `split_by_hand("a,b,c", ",", 1)` is `['a', 'b,c']`, and the tail append needs no change.

### Where it goes wrong

1. **Forgetting the last piece.** Emitting only when a separator is seen drops the tail: `"a,b"` gives `["a"]`. Fix: `parts.append(s[start:])` after the loop; it also makes `""` give `[""]` and `"a,"` give `["a", ""]`, like Python.
2. **`+=` in a loop.** Each `+=` builds a new string and may copy everything so far: O(n²) characters over n appends. Fix: append pieces to a list, `"".join` once.
3. **Reading `s[i]` before checking `i < n`.** `"-"` or `"   "` makes a parser read past the end (`IndexError`). Fix: every `while` starts with `i < n and ...`.
4. **A branch that never moves the cursor.** Every path through the body of `while i < n` must advance `i` or leave the loop; a branch that forgets spins forever on the first character that reaches it. Fix: before running, point at the `i += ...` in each branch.
5. **`isdigit()` as the digit test.** `"²".isdigit()` is True, yet `int("²")` raises `ValueError`. Fix: `"0" <= c <= "9"`.
6. **Clamping too late, or not at all.** Python ints never overflow, so the bug hides: `"-91283472332"` must give `-2147483648`. Fix: check after every digit (in Java or C++, check *before* multiplying: `num > (INT_MAX - d) / 10`).
7. **Moving by 1 after a separator match.** Matches must not overlap: `"aaa"` split on `"aa"` is `["", "a"]`. Fix: `i += len(sep)`.
8. **Comparing numbers as strings.** `"1.01" != "1.001"` as strings, yet they are the same version, and `"10" < "9"` is True. Fix: parse each field into an int (`x = x * 10 + d`).
9. **A 26-slot count on text that isn't lowercase.** `counts[ord(ch) - ord("a")]` for `"Z"` is index -7, which Python quietly maps to the `'t'` slot, so `"Z"` and `"t"` look like anagrams; `"A"` (index -32) raises `IndexError`. Fix: ask the alphabet; otherwise key on `"".join(sorted(w))` or a `Counter`.
10. **Deleting while scanning.** Removing characters from the list you are indexing shifts every later index. Fix: mark (`chars[i] = ""`) during the scan and join once at the end.
11. **The palindrome expansion overshoots.** The `while` stops one step past the palindrome on both sides, so the palindrome is `s[lo + 1:hi]`, of length `hi - lo - 1`.

### Edge cases to say out loud

Empty string · only separators, only spaces · a separator at the start, at the end, twice in a row · a separator that overlaps itself (`"aaa"` on `"aa"`) · one character · a sign with no digits (`"+"`) · overflow both ways · leading zeros · uppercase, digits or spaces where the code assumes lowercase letters (ask the alphabet) · non-ASCII text (Python indexes code points; one visible character can be several of them).

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

**Try it**
- Compare `" a  b ".split(" ")` with `" a  b ".split()`: `['', 'a', '', 'b', '']` versus `['a', 'b']`. The first is `split_on_char`, the second is `split_words`; ask which one the problem means.
- Predict, then check: `my_atoi("-0012a42")` is -12 and `my_atoi("3.14")` is 3; the scan stops at the first non-digit.
- Add `assert split_on_char("a", "a") == ["", ""]` and predict whether it passes before running it (it does: one separator, two empty pieces).

### Variations

| Variation | What changes from the template | Problems |
|---|---|---|
| **Split on one character** | emit at each separator, and once more at the end | warm-up |
| **Split on runs of spaces** | phases: skip the gap, read a word; drop the empty word a trailing gap reads | 151, 58 |
| **Read a number** | phases spaces → sign → digits; `num = num * 10 + d`; clamp | 8 |
| **Two cursors in lockstep** | read one field from each string, compare, step over the dots | 165 |
| **Quoted fields** | a flag flips at each `"`; a separator cuts only outside quotes | split follow-up |
| **Difference key** | the tuple of `(s[i+1] - s[i]) % 26` forgets the shift | 249 |
| **Expand around center** | 2n − 1 centers; grow while both ends match | 5, 647 |
| **One deletion allowed** | two pointers; at the first mismatch, try skipping either side | 680 |
| **Runs** | `j` walks to the end of the run; the next run starts at `j` | 443, 809, 38 |
| **Digits with a carry** | walk both strings from the right; `divmod(d, 10)`; build backwards | 415, 67, 43 |
| **Mark, then join** | stack of open-bracket indices; blank what can't be matched | 1249 |
| **Reverse twice** | reverse the whole list, then reverse each word back | 151, 186 |
| **Row buckets** | a row index bouncing between 0 and numRows − 1; one list per row | 6 |
| Hard ones (at the end) | grammar flags; chunks of three; cut + hash map; KMP borders; rolling hash + binary search; greedy packing + divmod | 65, 273, 336, 1392, 214, 28, 1044, 68 |

Many string problems are taught where their technique lives:

| Problems | Technique | Section |
|---|---|---|
| longest without repeats, minimum window, permutation in string, all anagrams (3, 76, 567, 438) | a window with letter counts | [Sliding Window](#s06) |
| valid palindrome with punctuation (125) | two pointers that skip non-letters | [Two Pointers](#s05) |
| brackets, decode string, calculators, simplify path (20, 394, 224, 227, 71) | a stack | [Stacks & Queues](#s07) |
| anagram counts, group anagrams, encode/decode strings (242, 49, 271) | a fingerprint key; length-prefix framing | [Arrays & Hashing](#s03) |
| word search II, word squares (212, 425) | a trie walked along the board | [Tries](#s12) |
| phone letters, IP addresses, palindrome partitioning (17, 93, 131) | backtracking over cuts | [Backtracking](#s16) |

**More parsing: two cursors, a quote flag.** Compare Version Numbers runs two cursors in lockstep, one field at a time; a string that has run out simply reads as 0, which is exactly the rule "missing revisions count as 0". Quoted fields are the classic follow-up to the split warm-up: one flag remembers whether we are inside quotes, and a separator only cuts outside them.

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


def split_quoted(line, sep=","):             # a sep inside "..." does not cut
    fields, piece, in_quotes = [], [], False # STATE: piece = the characters of the open field
    for ch in line:
        if ch == '"':
            in_quotes = not in_quotes        # a quote flips the mode; it is not kept
        elif ch == sep and not in_quotes:
            fields.append("".join(piece))    # RECORD: the field is closed
            piece = []
        else:
            piece.append(ch)                 # STEP: the field grows
    fields.append("".join(piece))            # RECORD the last field
    return fields


print(compare_version("1.01", "1.001"), compare_version("1.0", "1.0.1"), compare_version("1.10", "1.9"))   # 0 -1 1
print(split_quoted('1,"Smith, John",42'))   # ['1', 'Smith, John', '42']
```

**Try it**
- Change `or` to `and` in `while i < len(v1) or j < len(v2)` and run `compare_version("1.0.1", "1")`: 0 instead of 1. The loop stopped when the shorter string ran out.
- Why is `compare_version("1.10", "1.9")` 1? Compare `"10" < "9"` (True: strings compare character by character) with `10 < 9`.
- Drop `and not in_quotes` and run `split_quoted('1,"Smith, John",42')`: `['1', 'Smith', ' John', '42']`.

**Keys: group by "the same up to ...".** To group words that are equal up to some change, compute a key that forgets exactly that change and let a dict do the grouping. Shifted strings forget the starting letter: the gaps between neighbours, taken mod 26 so that `z → a` is a gap of 1. Anagrams forget the order: the letter counts or the sorted letters, built in [Arrays & Hashing](#s03).

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
print(group_by_key(["eat", "tea", "tan", "ate"], lambda w: "".join(sorted(w))))   # [['eat', 'tea', 'ate'], ['tan']]
```

**Try it**
- Drop the `% 26` from `shift_key` and rerun: `'az'` and `'ba'` land in different groups, because their gaps are now 25 and -1.
- Print `shift_key("a")` and `shift_key("z")`: both `()`, so all one-letter words form one group. That is right: any letter shifts into any other.
- See why a 26-slot count needs lowercase: `counts = [0] * 26; counts[ord("Z") - ord("a")] += 1; print(counts.index(1))` prints 19, the slot of `'t'`. Ask the alphabet first; otherwise key on the sorted letters, as the second print does.

**Palindromes: from the middle, and from the ends.** A palindrome is decided by its center, and growing it one step on each side costs one comparison: try all 2n − 1 centers (each letter for odd lengths, each gap for even lengths) and stop at the first mismatch, since no wider palindrome can share that center. Valid Palindrome II (680) walks two pointers inward instead; at the first mismatch one of the two letters must go, so check both leftovers. (With punctuation to skip, see [Two Pointers](#s05).)

```python
def longest_palindrome(s):                   # O(n²) time, O(1) extra space
    best_lo, best_len = 0, 0
    for center in range(len(s)):
        for lo, hi in ((center, center), (center, center + 1)):   # odd and even centers
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo -= 1                      # grow while both ends match
                hi += 1
            if hi - lo - 1 > best_len:       # the loop overshot by one on each side
                best_lo, best_len = lo + 1, hi - lo - 1
    return s[best_lo:best_lo + best_len]


def valid_palindrome_ii(s):                  # a palindrome after deleting at most one letter? O(n)
    def is_pal(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo, hi = lo + 1, hi - 1
        return True
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:                   # the first mismatch: one of these two must go
            return is_pal(lo + 1, hi) or is_pal(lo, hi - 1)
        lo, hi = lo + 1, hi - 1
    return True


print(longest_palindrome("babad"), longest_palindrome("cbbd"))   # bab bb
print(valid_palindrome_ii("abca"), valid_palindrome_ii("abc"))   # True False
```

**Try it**
- Delete the even center `(center, center + 1)` and run `longest_palindrome("cbbd")`: `'c'`. The palindrome `"bb"` has no middle letter, so only a gap can be its center.
- Add `print(center, lo, hi)` after the `while` loop and run `longest_palindrome("aba")`: the line `1 -1 3` shows the loop stopping one step outside `s[0:3]` on both sides.
- Keep only the left skip (`return is_pal(lo + 1, hi)`) and run `valid_palindrome_ii("cbbcc")`: False instead of True. Deleting the `c` at index 3 works; deleting the `b` at index 1 does not.

**Runs and carries.** A *run* is a block of equal letters: a second cursor `j` walks to its end, and the next run starts at `j`. Expressive Words (809) compares the runs of two strings; String Compression (443) and Count and Say (38) write them out. Adding numbers given as strings walks both from the right with a carry, like on paper, and builds the answer backwards. All of them are O(n).

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

**Try it**
- Change `i = j` to `i = j + 1` and run `runs("aaabcc")`: `[('a', 3), ('c', 2)]`. The `b` run vanishes, because the next run already starts at `j`.
- Predict `expressive("zzzzzyyyyy", "zzyy")` and `expressive("aaa", "aaaa")`: True (both runs can grow to 5) and False (a run can't shrink).
- Drop `or carry` from the loop and run `add_strings("999", "1")`: `'000'`. The last carry needs one more turn of the loop.

**Mark, then join; reverse twice; row buckets.** Minimum Remove matches brackets with a stack of the indices of `(` still open; a `)` with nothing to close, or a `(` still open at the end, is exactly what must go, so blank them during the scan and join once. Reverse Words in place: reversing the whole character list puts the words in the right order but spells each one backwards, and a second pass reverses each word back (in Python, say `" ".join(reversed(s.split()))` first; the two reversals are the follow-up for mutable strings). Zigzag: only the *row* of each character matters, and the row bounces 0, 1, ..., numRows − 1, ..., 1, 0.

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

**Try it**
- Print `open_idx` after the loop for `"(a(b(c)d)"`: `[0]`. Only the first `(` never found a partner, so the answer is `'a(b(c)d)'`.
- Replace `chars[i] = ""` in the `)` branch with `del chars[i]` and rerun the cell: `IndexError` on `"))(("`, because the saved indices of the `(` now point past the end of the shorter list. On `"a)b)c"` it fails quietly instead, returning `'ab)'`.
- Remove the second loop (the per-word flips) and run `reverse_words("the sky is blue")`: `'eulb si yks eht'`, halfway there.
- Remove the early `return s` (the first `if` in `zigzag`) and run `zigzag("AB", 1)`: `IndexError`. With one row the step never flips, so `r` walks off to row 1.

**Optional: the Hard ones.** Each is the same cursor with heavier bookkeeping. Read them once the mediums above feel easy.

Valid Number (65) keeps three flags instead of a value: each character is legal or not depending only on what has been seen. Integer to English Words (273) works in base 1000: every 3-digit chunk is spelled the same way, followed by its scale word.

```python
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


print([is_number(t) for t in ["2", "-.9", "4.", "3e+7", "e3", "99e2.5", ".", "1e"]])
# [True, True, True, True, False, False, False, False]
print(number_to_words(12345), "|", number_to_words(1000010))   # Twelve Thousand Three Hundred Forty Five | One Million Ten
```

**Try it**
- Change `seen_exp, seen_digit = True, False` to `seen_exp = True` and run `is_number("1e")`: True. The exponent now borrows the mantissa's digits.
- Predict `[is_number(t) for t in ["+.8", "-e5", "1e5.", " 1"]]` before running: `[True, False, False, False]`.
- Remove the `if num % 1000:` guard and run `number_to_words(1000000)`: `'Billion One Million Thousand'`. Empty chunks must stay silent, scale word included.

Palindrome Pairs (336) cuts each word in two: if one half is a palindrome, the other half's reverse must be a whole word, and a dict of reversed words finds it with one lookup, O(n·L²) for n words of length L. The **KMP prefix function** asks, at every position, how much of the start of the string reappears just before it. `fail[i]` is the length of the longest *border* of `s[:i + 1]`, a prefix that is also a suffix and is *proper* (shorter than the whole string). When the next letter does not extend the current border, fall back to the border of the border, `fail[k - 1]`, instead of starting over:

```text
s = a a b a a a b        fail so far = [0, 1, 0, 1, 2]
i=5 ('a'): extend the border "aa"? its next letter s[2] = 'b' != 'a'
           fall back to the border of "aa", which is "a": s[1] = 'a' == 'a'  ->  "aa", fail[5] = 2
i=6 ('b'): extend "aa": s[2] = 'b' == 'b'  ->  "aab", fail[6] = 3
```

Each fall-back pays for an earlier step forward, so the table costs O(n) and a search O(n + m). Longest Happy Prefix is `fail[-1]`. Shortest Palindrome needs the longest palindromic *prefix*, which is the border of `s + "#" + reverse(s)`. `kmp_find` glues pattern and text with `"\0"`, a character in neither string, so no border can cross it.

```python
def palindrome_pairs(words):                 # O(n·L²): n words, L + 1 cuts, O(L) per test
    index = {w[::-1]: i for i, w in enumerate(words)}   # reversed word -> its index
    pairs = []
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):        # w = pre + suf
            pre, suf = w[:cut], w[cut:]
            if pre == pre[::-1] and suf in index and index[suf] != i:
                pairs.append([index[suf], i])    # reverse(suf) + pre + suf
            if cut < len(w) and suf == suf[::-1] and pre in index and index[pre] != i:
                pairs.append([i, index[pre]])    # pre + suf + reverse(pre); cut < len(w) avoids doubles
    return pairs


def prefix_function(s):
    fail = [0] * len(s)                      # fail[i] = longest proper border of s[:i + 1]
    for i in range(1, len(s)):
        k = fail[i - 1]                      # the border we hope to extend by s[i]
        while k and s[i] != s[k]:
            k = fail[k - 1]                  # fall back to the next shorter border
        if s[i] == s[k]:
            k += 1
        fail[i] = k
    return fail


def longest_happy_prefix(s):                 # the longest proper prefix that is also a suffix
    return s[:prefix_function(s)[-1]] if s else ""


def shortest_palindrome(s):                  # letters may only be added in front
    keep = prefix_function(s + "#" + s[::-1])[-1]   # the longest palindromic prefix of s
    return s[keep:][::-1] + s


def kmp_find(text, pattern):                 # every start of pattern in text, overlaps too
    m, fail = len(pattern), prefix_function(pattern + "\0" + text)
    return [i - 2 * m for i, k in enumerate(fail) if k == m]


print(palindrome_pairs(["abcd", "dcba", "lls", "s", "sssll"]))         # [[1, 0], [0, 1], [3, 2], [2, 4]]
print(prefix_function("aabaaab"))                                      # [0, 1, 0, 1, 2, 2, 3]
print(longest_happy_prefix("ababab"), longest_happy_prefix("level"))   # abab l
print(shortest_palindrome("aacecaaa"), shortest_palindrome("abcd"))    # aaacecaaa dcbabcd
print(kmp_find("aabaaabaab", "aab"))                                   # [0, 4, 7]
```

**Try it**
- Remove `cut < len(w) and` and run `palindrome_pairs(["abcd", "dcba"])`: `[[1, 0], [0, 1], [0, 1], [1, 0]]`, each pair found twice, once from each word.
- Replace `k = fail[k - 1]` with `k = 0` (start over on a mismatch) and rerun: `prefix_function("aabaaab")` is `[0, 1, 0, 1, 2, 1, 0]`. The borders `"aa"` and `"aab"` at the end are missed.
- Remove the `"#"` in `shortest_palindrome` and run it on `"aaba"`: `'aaba'`, which is not a palindrome. The border of `"aabaabaa"` is 5, longer than `s`; the separator caps it at `len(s)`. The right answer is `'abaaba'`.
- Run `kmp_find("aaaa", "aa")`: `[0, 1, 2]`. Overlapping matches are found because a full match keeps its border.

Longest Duplicate Substring (1044) stacks two ideas. If some substring of length L occurs twice, so does its prefix of length L − 1, so "a repeat of length L exists" is true up to the answer and false after it: binary search the length. To test one length in O(n), read each window as a number in base B (mod a big prime) and *roll* it one step in O(1); in base 10 the window `"123"` becomes `"234"` as 123 · 10 − 1 · 1000 + 4 = 234. Equal strings have equal hashes, and equal hashes are confirmed by comparing letters: O(n log n) expected. (In Java or C++, add `MOD` after the subtraction; Python's `%` never returns a negative number here.)

```python
def longest_dup_substring(s):
    n, MOD, BASE = len(s), (1 << 61) - 1, 131
    codes = [ord(c) for c in s]

    def repeat_of_length(L):                 # start of a length-L substring seen earlier, or -1
        h = 0
        for c in codes[:L]:
            h = (h * BASE + c) % MOD         # hash of the first window
        top = pow(BASE, L, MOD)              # weight of the leaving char after the shift
        seen = {h: [0]}
        for i in range(1, n - L + 1):
            h = (h * BASE - codes[i - 1] * top + codes[i + L - 1]) % MOD   # roll one step right
            for j in seen.get(h, []):
                if s[j:j + L] == s[i:i + L]: # verify: different strings can share a hash
                    return i
            seen.setdefault(h, []).append(i)
        return -1

    lo, hi, best = 1, n - 1, ""              # a length-n substring can't occur twice
    while lo <= hi:
        mid = (lo + hi) // 2
        i = repeat_of_length(mid)
        if i >= 0:
            best, lo = s[i:i + mid], mid + 1 # works: try longer
        else:
            hi = mid - 1                     # fails, and so does every longer length
    return best


print(longest_dup_substring("banana"), repr(longest_dup_substring("abcd")))   # ana ''
```

**Try it**
- Add `print(mid, i)` right after `i = repeat_of_length(mid)` and run `longest_dup_substring("banana")`: `3 3` (the second `"ana"` starts at 3), then `4 -1`. Two probes settle the answer.
- Set `MOD = 5`, so hashes collide all the time, and rerun: still `ana ''`, because every hash hit is checked letter by letter. Collisions cost time, never correctness.
- Keep `MOD = 5` and change `if s[j:j + L] == s[i:i + L]:` to `if True:` (trust the hash): `longest_dup_substring("aba")` returns `'ba'`, which occurs once. Since `131 % 5 == 1`, this hash is just the letter sum mod 5, so `"ab"` and `"ba"` collide.

Text Justification (68) has no trick, just two jobs done cleanly in O(total characters): which words fit on this line (greedy), and how to spread the spare spaces, which is one `divmod`: every gap gets the quotient and the leftmost `remainder` gaps get one more.

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

**Try it**
- Work out the second line by hand: `"example"`, `"of"`, `"text"` hold 13 letters, so 3 spaces go into 2 gaps: `divmod(3, 2)` is `(1, 1)`, and the left gap gets the extra one.
- Change `<=` to `<` in the packing loop and run `full_justify(["ab", "cd"], 5)`: `['ab   ', 'cd   ']` instead of `['ab cd']`. A line that fits exactly is legal.
- Remove `j == len(words) or` and run `full_justify(["What", "must", "be", "acknowledgment", "shall", "be"], 16)`: the last line becomes `'shall         be'` (nine spaces in one gap) instead of `'shall be        '`.

### Say it in the interview

> "Two questions first: if two separators are adjacent, do you want an empty string between them, like `split(",")`, or should a run count as one, like `split()`? And can the separator be longer than one character? I'll walk the string once with an index and remember where the current piece started. When the separator starts at `i` I emit `s[start:i]`, which may be empty, jump past the whole separator, and start the next piece there. After the loop I emit the tail; that line makes `"a,"` give `["a", ""]` and `""` give `[""]`. Each position compares up to m characters, so O(n·m), which is O(n) for one character, plus O(n) for the output. Using `find` and slicing off the remainder copies the rest of the string per piece, which is O(n²) at worst."

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
| Simplify Path | `strings/simplify_path.py` | split on "/"; a stack of names: push a name, pop on "..", skip "" and "." ([Stacks & Queues](#s07)) |
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
