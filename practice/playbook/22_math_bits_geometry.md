## Math, Bits & Geometry

> An integer is a row of bits, and a row of bits is a small set: bit `v` is 1 exactly when `v` is in it. Bits answer set questions a whole word at a time; the math tools count things instead of listing them.

**Reach for it when** the problem mentions *bits*, *XOR*, *powers of two*, *"every element appears twice except one"*, *subsets of a small set* (n ≤ 20, 26 letters, 10 digits), *parity* ("an odd number of times"), *modulo 10⁹ + 7*, *gcd, primes or digits*, *points, lines and slopes*, or when n goes up to 10⁹ so nothing can be listed one at a time.

**In this repo:** `bit_manipulation/` (9 problems) · `math_geometry/` (7 here; Rotate Image, Spiral Matrix and Set Matrix Zeroes are in [Matrices](#s21)) · basics: `practice/simple/basics/bits/01_get_set_clear_toggle_bits.py`, `02_count_bits_and_lowest_set_bit.py`, `03_xor_tricks_single_number_missing_number.py`, `04_bitmask_subset_enumeration.py`, `05_reverse_bits_and_shifts.py` and `practice/simple/basics/math/01_gcd_lcm_euclid.py`, `02_primes_sieve_and_primality.py`, `03_fast_power_and_modular_arithmetic.py`, `04_digits_reverse_integer_and_palindrome_number.py`, `05_base_conversion_and_excel_columns.py`, `06_random_pick_and_reservoir_sampling.py` · a bitset with a lazy global flip: `design/design_bitset.py` (in [Design](#s24))

### The picture

```text
   x = 180 =   1 0 1 1 0 1 0 0          bit i is worth 2^i; bit 0 is on the right
       bit:    7 6 5 4 3 2 1 0
   as a set:   {2, 4, 5, 7}             bit v is 1  <=>  v is in the set

          x  =  1 0 1 1 0 1 0 0
      x - 1  =  1 0 1 1 0 0 1 1         the borrow turns the lowest 1 into 0 and the 0s below it into 1s
  x & (x-1)  =  1 0 1 1 0 0 0 0         -> the lowest 1 is deleted    (repeat until 0 to count the 1s)
         -x  =  0 1 0 0 1 1 0 0         -x = ~x + 1 (8 bits shown): every bit above the lowest 1 flips
     x & -x  =  0 0 0 0 0 1 0 0         -> only the lowest 1 is kept  (= 4)

  XOR adds each column and keeps only "odd or even":  a ^ a = 0,  a ^ 0 = a,  in any order
       4 = 1 0 0
       1 = 0 0 1          4 ^ 1 ^ 2 ^ 1 ^ 2: in every column the pairs cancel,
       2 = 0 1 0          and the parity row that is left, 1 0 0, is the loner 4
       1 = 0 0 1
       2 = 0 1 0
     xor = 1 0 0
```

**Why it is fast:** a set of small integers (letters, digits, up to ~60 items) fits in one word, so "add", "is it in?", union, intersection, subset test and "flip the parity" are each one operation instead of a loop. The math tools win the same way, by **counting instead of listing**: the sieve crosses off multiples instead of testing every number; fast power squares instead of multiplying n times; digit problems work per column instead of per number; the k-th permutation and the k-th lexicographic number skip whole blocks whose size they can compute.

### From idea to code

This section is a toolbox in three parts: **bits** (the main template, then its family), **math recipes**, and **hard puzzles** you can leave for a second pass. The main template is the one "bit array" interview questions are built on: a set of small integers stored as bits.

**The idea in one sentence:** *to remember which small integers you have seen, keep one bit per possible value: test bit `v` to ask, set bit `v` to add.*

| Decision | Bit-array answer |
|---|---|
| **State**: what must I remember? | one integer `seen`, used as a set of small integers |
| **Definition**: what exactly does each variable mean? | `(seen >> v) & 1` is 1 exactly when value `v` has appeared so far |
| **Invariant**: what is true at the end of every step? | after reading `nums[i]`, `seen` holds exactly the values in `nums[0..i]` |
| **Step**: how does one item change the state? | test bit `v`, *then* add it: `seen \|= 1 << v` |
| **Record**: when is the answer updated? | when the test finds the bit already set (a repeat); missing values are read from the bits still 0 at the end |
| **Init**: starting values | `seen = 0`, the empty set |
| **Return**: what comes back? | the repeat and/or the missing values; `full & ~seen` is "everything not seen" in one step |

The same idea, sentence by sentence:

| In words | In code |
|---|---|
| "is v in the set?" (get bit v) | `(seen >> v) & 1` |
| "add v" (set bit v) | `seen \|= 1 << v` |
| "remove v" (clear bit v) | `seen &= ~(1 << v)` |
| "flip v" (toggle bit v) | `seen ^= 1 << v` |
| "the set {0, 1, ..., n-1}" | `(1 << n) - 1` |
| "the set {1, ..., n}" | `(1 << (n + 1)) - 2`: bits 0..n, minus bit 0 |
| "how many are in it" | `seen.bit_count()` (Python 3.10+) or `bin(seen).count("1")` |
| "its smallest member" | `(seen & -seen).bit_length() - 1` |
| "drop its smallest member" | `seen &= seen - 1` |
| "a is a subset of b" | `(a & ~b) == 0`: nothing of a lies outside b |
| "union, intersection, difference" | `a \| b`, `a & b`, `a & ~b` |

Inside the loop the order is the decision that matters: test (and RECORD) first, then the STEP that adds v. The test asks "had v appeared *before* this item?", so it must run while `seen` still describes the earlier items only.

```python
def find_error_nums(nums):                     # Set Mismatch: 1..n, one value twice, one missing
    n, seen, dup = len(nums), 0, -1            # STATE: bit v of seen = "v has appeared"; INIT: empty
    for v in nums:
        if (seen >> v) & 1:                    # test FIRST: is v already in the set?
            dup = v                            # RECORD: this is the second copy
        seen |= 1 << v                         # STEP: add v, after the test
    full = (1 << (n + 1)) - 2                  # the set {1, ..., n}
    missing = (full & ~seen).bit_length() - 1  # RECORD: the one bit of full that is still 0
    return [dup, missing]                      # RETURN


print(find_error_nums([1, 2, 2, 4]))           # [2, 3]
print(find_error_nums([3, 1, 3]))              # [3, 2]
```

**Try it**
- Print `bin(full)`, `bin(seen)` and `bin(full & ~seen)` for `[1, 2, 2, 4]`: `0b11110`, `0b10110`, `0b1000`. A set difference is one `&`.
- Swap the test and the add (add first): every value now looks like a repeat, and `[1, 2, 2, 4]` answers `[4, 3]`.
- Run `find_error_nums([2, 2])`: `[2, 1]`. The hole can be the smallest value too.

**How big can the set be?** An int bitset costs O(largest value / 64) per operation: perfect for letters, digits and n up to about 10⁴; beyond that, or whenever you claim O(1), use a bytearray or 64-bit words. (A Python int is immutable, so every `|=` builds a new one.) The capstone at the end of the bit toolbox builds the 64-bit-word version.

### Watch it work

Each line adds one value; the set is drawn as 8 bits, value 0 on the right.

```python
def trace_seen(nums):
    seen = 0
    for v in nums:
        note = "   <- bit already set: repeat" if (seen >> v) & 1 else ""
        seen |= 1 << v
        print(f"add {v}:   {seen:08b}{note}")
    full = (1 << (len(nums) + 1)) - 2
    print(f"full:    {full:08b}")
    print(f"missing: {full & ~seen:08b}")


trace_seen([3, 1, 4, 1, 5, 2])
```

**Try it**
- Run `trace_seen([2, 2, 1])` and read the missing value off the last line: bit 3, so 3.
- Add `seen.bit_count()` to the printed line: it grows by one per new value and stands still on the repeat.
- Change `- 2` to `- 1` in `full`: the missing line becomes `01000001`. Bit 0 joins the real hole, because the values start at 1 and bit 0 is never set.

### The bit toolbox

#### Bit tricks to type without thinking

**Idea:** `1 << i` is a lone 1 at position i: OR it in to set, AND with its complement to clear, XOR to flip, shift down and `& 1` to read. `x & (x - 1)` deletes the lowest 1, so a loop of it runs once per 1-bit, and a power of two (exactly one 1) becomes 0. So does 0 itself, so test `x > 0` too. `~x & (x + 1)` keeps the lowest *0* as a lone 1. And `i >> 1` is `i` without its last bit, which lets you count the bits of every number from the answers you already have.

```python
def show(x, width=8):
    return format(x, f"0{width}b")             # x in binary, padded to width digits


x = 0b10110100                                 # 180, the set {2, 4, 5, 7}
print((x >> 5) & 1, (x >> 3) & 1)              # 1 0: get bit 5, get bit 3
print(show(x | (1 << 3)), show(x & ~(1 << 2)), show(x ^ (1 << 7)))   # 10111100 10110000 00110100
print(show(x & (x - 1)), show(x & -x))         # 10110000 00000100: delete / keep the lowest 1
y = 0b10110111
print(show(~y & (y + 1)))                      # 00001000: the lowest 0 of y, as a lone 1


def popcount(x):                               # Number of 1 Bits: one round per 1-bit
    count = 0
    while x:
        x &= x - 1                             # delete the lowest 1
        count += 1
    return count


def count_bits_upto(n):                        # Counting Bits: popcount of every i in 0..n
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)         # i is its half (i >> 1) with one bit appended
    return ans


def reverse_bits(x):                           # Reverse Bits: exactly 32 rounds
    out = 0
    for _ in range(32):
        out = (out << 1) | (x & 1)             # push x's lowest bit onto the right of out
        x >>= 1
    return out


print(popcount(180), (180).bit_count())                        # 4 4
print([v for v in range(20) if v > 0 and (v & (v - 1)) == 0])  # [1, 2, 4, 8, 16]: exactly one 1-bit
print(count_bits_upto(5))                                      # [0, 1, 1, 2, 1, 2]
print(reverse_bits(1), reverse_bits(43261596))                 # 2147483648 964176192
```

**Try it**
- Drop the `v > 0 and` from the power-of-two test: 0 joins the list, because `0 & (0 - 1)` is `0 & -1`, which is 0.
- Replace `for _ in range(32):` with `while x:` in `reverse_bits`: `reverse_bits(1)` returns 1 instead of 2147483648. The 31 leading zeros of the input never became trailing zeros of the output.
- Print `count_bits_upto(15)`: the second half (8..15) is the first half (0..7) plus one, because those numbers are the first half with bit 3 added.

#### XOR as parity

**Idea:** XOR remembers, for every bit column, whether it has seen an odd or an even number of 1s. Values that come in pairs cancel, whatever their order, so what is left is the value with no partner.

```python
def single_number(nums):                       # every value twice except one
    acc = 0
    for x in nums:
        acc ^= x                               # pairs cancel: a ^ a = 0
    return acc


def missing_number(nums):                      # 0..n with exactly one value missing
    acc = len(nums)                            # n has no index of its own: start with it
    for i, x in enumerate(nums):
        acc ^= i ^ x                           # a present value cancels against its equal index
    return acc


print(single_number([4, 1, 2, 1, 2]), missing_number([3, 0, 1]))   # 4 2
```

**Try it**
- Run `single_number([2, 2, 3, 2])`: 1, which is neither value. A value that appears three times no longer cancels; count each column modulo 3 instead (Single Number II, in the next block).
- Start `missing_number` with `acc = 0` and run `missing_number([0, 1])`: 0 instead of 2. The value n never got a partner.
- Two loners (260): `both = single_number([1, 2, 1, 3, 2, 5])` is `3 ^ 5 = 6`, and `low = both & -both` is 2, a bit where 3 and 5 differ. XOR-ing only the numbers that have that bit, `single_number([v for v in [1, 2, 1, 3, 2, 5] if v & low])`, gives 3, and `both ^ 3` is 5.

#### Negative numbers: Python's infinite sign bits

**Idea:** a Python int has no width. A negative number behaves as if its sign bit repeated forever to the left, so `-5` is `...1111 1011` with infinitely many 1s. The operators work on that infinite pattern, which is why `x & -x` is right for negatives too, but also why `bin(-5)` cannot show the bits, why `-1 >> 1` stays `-1`, and why a loop that waits for the bits to run out never ends. When a problem means 32-bit integers, mask to 32 bits, work there, and convert back at the end.

```text
   5 = ...0000 0101          no width: the sign bit repeats forever to the left
  -5 = ...1111 1011          bin(-5) hides this and prints '-0b101'
  -5 & 0xFF       = 1111 1011 = 251               keep the low 8 bits
  -5 & 0xFFFFFFFF = 4294967291                    the 32-bit pattern C and Java store
  back to signed:  u - (1 << 32) if u >> 31 else u      (bit 31 set means negative)
```

```python
def to_signed32(u):                            # a 32-bit pattern back to a Python int
    return u - (1 << 32) if u >> 31 else u     # bit 31 set: the pattern is negative


def single_number_ii(nums):                    # Single Number II (137): all values 3 times but one
    out = 0
    for b in range(32):
        if sum((x >> b) & 1 for x in nums) % 3:   # this column's count is not a multiple of 3
            out |= 1 << b                      # so the loner has a 1 here
    return to_signed32(out)


def get_sum(a, b):                             # Sum of Two Integers (371): add without +
    MASK = 0xFFFFFFFF
    a, b = a & MASK, b & MASK                  # work on the 32-bit patterns
    while b:
        a, b = a ^ b, ((a & b) << 1) & MASK    # the sum without carries, then the carries
    return to_signed32(a)


print(bin(-5), -5 & 0xFF, -5 & 0xFFFFFFFF)                    # -0b101 251 4294967291
print(single_number_ii([-2, -2, 1, 1, 4, 1, 4, 4, -4, -2]))  # -4
print(get_sum(2, 3), get_sum(-1, 1), get_sum(-2, -3))        # 5 0 -5
```

**Try it**
- Return `out` instead of `to_signed32(out)` in `single_number_ii`: the example prints 4294967292, the 32-bit pattern of -4.
- Remove every `& MASK` from `get_sum` and add a counter that breaks the loop after 100 rounds: `get_sum(-1, 1)` is still running when it stops, because the carry walks left through the infinitely many 1s of -1.
- Print `bin(-1)`, `show(-x)` and `show(-x & 0xFF)`: `'-0b1'`, `'-10110100'`, `'01001100'`. Python shows a minus sign until you mask. It is also why `popcount(-1)` would never finish: -1 has infinitely many 1s to delete.

#### Letter sets and their subsets (1178)

**Idea:** a word is valid for a puzzle when the word's letter *set* is a subset of the puzzle's and contains the puzzle's first letter. Words with the same letter set are interchangeable, so count each mask once. Then flip the loop: a 7-letter puzzle has only 2⁷ = 128 letter subsets, so enumerate those and look each one up, instead of testing every word. The walk over the subsets of a mask is one line, `sub = (sub - 1) & mask`:

```text
  mask      1 0 1 1      the allowed positions (the puzzle's letters)
  sub       1 0 0 0
  sub - 1   0 1 1 1      the borrow: the lowest 1 becomes 0, everything below it becomes 1
  & mask    0 0 1 1      drop the forbidden positions: the next smaller subset of mask
  the walk: 1011, 1010, 1001, 1000, 0011, 0010, 0001, 0000   (counting down on mask's own bits)
```

```python
def letter_mask(word):
    m = 0
    for ch in word:
        m |= 1 << (ord(ch) - ord("a"))         # bit 0 = 'a', ..., bit 25 = 'z'
    return m


def submasks(mask):                            # every subset of mask, largest first, 0 last
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask                 # the next smaller subset


def valid_word_counts(words, puzzles):
    count = Counter(letter_mask(w) for w in words)
    out = []
    for p in puzzles:
        first = 1 << (ord(p[0]) - ord("a"))
        out.append(sum(count[s] for s in submasks(letter_mask(p)) if s & first))
    return out


print([[x for i, x in enumerate("abc") if (mask >> i) & 1] for mask in range(1 << 3)])
# [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
print([bin(s) for s in submasks(0b1011)])   # ['0b1011', '0b1010', '0b1001', '0b1000', '0b11', '0b10', '0b1', '0b0']
print(valid_word_counts(["aaaa", "asas", "able", "ability", "actt", "actor", "access"],
                        ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]))   # [1, 1, 3, 2, 4, 0]
```

**Try it**
- Replace `(sub - 1) & mask` with `sub - 1`: `submasks(0b1011)` now yields all 12 numbers from 11 down to 0, including ones like `0b100` that are not subsets.
- Move the `if sub == 0: return` check above the `yield`: the empty set 0 is never produced (7 values instead of 8).
- Drop the `if s & first` filter: the last puzzle, `"gaswxyz"`, answers 2 instead of 0, because `"aaaa"` and `"asas"` fit its letters but lack its first letter `g`.

#### Parity masks over prefixes (1542)

**Idea:** a digit string can be rearranged into a palindrome when at most one digit appears an odd number of times. Keep a 10-bit mask of the parities of the prefix read so far: XOR is addition where 1 + 1 = 0. The parities of a substring are the XOR of two prefix masks, so for each end `j` you want the *earliest* earlier prefix whose mask equals this one (all counts even) or differs in exactly one bit (one odd digit): 11 dictionary lookups. It is the "first index of each total" trick of [Prefix Sums](#s04), with masks as the totals.

```python
def longest_awesome(s):
    first = {0: -1}                            # mask -> earliest prefix end with it (-1: empty prefix)
    mask = best = 0
    for j, ch in enumerate(s):
        mask ^= 1 << int(ch)                   # flip the parity of this digit
        for target in [mask] + [mask ^ (1 << d) for d in range(10)]:   # all even, or one odd
            if target in first:
                best = max(best, j - first[target])
        first.setdefault(mask, j)              # keep only the EARLIEST index
    return best


print(longest_awesome("3242415"), longest_awesome("213123"), longest_awesome("12345678"))   # 5 6 1
```

**Try it**
- Print `format(mask, "04b")` after each digit of `"213123"`: `0100 0110 1110 1100 1000 0000`. Every digit appears twice, so the full string's mask is 0 and it matches the seed `-1`: length 6.
- Replace `first.setdefault(mask, j)` with `first[mask] = j` (keep the latest index): `longest_awesome("1111")` drops from 4 to 2. Each repeat of a mask drags its partner index to the right, and later substrings get measured from there.
- Start with `first = {}` instead of `{0: -1}`: `longest_awesome("213123")` drops from 6 to 5, because the whole string needs the empty prefix as its partner.

#### Maximum XOR with a limit (1707)

**Idea:** to maximise `x ^ y`, decide bits from the top: a 1 at bit 29 is worth more than all lower bits together, so at each level go to the child holding the *opposite* of x's bit when it exists. A binary trie of the numbers answers that in 30 steps. The limit `y <= m` is handled offline: sort the queries by m and insert numbers in increasing order, so the trie always holds exactly the allowed numbers.

```python
def max_xor_with_limit(nums, queries, bits=30):
    root = {}                                  # binary trie: each node is {bit: child node}

    def insert(v):
        node = root
        for b in range(bits - 1, -1, -1):      # from the top bit down
            node = node.setdefault((v >> b) & 1, {})

    def best_xor(x):
        node, out = root, 0
        for b in range(bits - 1, -1, -1):
            want = 1 - ((x >> b) & 1)          # the opposite bit makes bit b of x ^ y a 1
            if want in node:
                out |= 1 << b
                node = node[want]
            else:
                node = node[1 - want]          # forced: only one branch exists
        return out

    nums, ans, i = sorted(nums), [-1] * len(queries), 0
    for qi in sorted(range(len(queries)), key=lambda q: queries[q][1]):   # smallest limit first
        x, limit = queries[qi]
        while i < len(nums) and nums[i] <= limit:   # now the trie holds exactly nums <= limit
            insert(nums[i])
            i += 1
        if i:
            ans[qi] = best_xor(x)              # answer in the ORIGINAL query position
    return ans


print(max_xor_with_limit([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]]))   # [3, 3, 7]
```

**Try it**
- Answer `[5, 6]` by hand first: the trie holds 0..4, `5 = 101`, and the best partner is `2 = 010`, so `5 ^ 2 = 111 = 7`.
- Answer the queries in input order instead of sorted (`for qi in range(len(queries)):`) and run `max_xor_with_limit([0, 1, 2, 3, 4], [[5, 6], [3, 1]])`: `[7, 7]` instead of `[7, 3]`. The second query sees numbers above its limit that the first query inserted.
- Set `bits=2` and rerun the main example: `[3, 3, 3]`. The top bit of 4 and 5 is never looked at, so `5 ^ 2 = 7` is out of reach.

#### Greedy on the low bits (397)

**Idea** (even → halve; odd → add or subtract 1; reach 1 in the fewest steps): halving just drops the last bit, so the cost is in clearing 1-bits. For odd n, look at the last two bits: `...01` → subtract (it leaves `...00`, two free halvings), `...11` → add (the carry wipes out the whole run of 1s at once). The single exception is n = 3, where 3 → 2 → 1 beats 3 → 4 → 2 → 1.

```python
def integer_replacement(n):
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n //= 2                            # even: halving is the only move
        elif n == 3 or (n & 3) == 1:           # ends in 01 (or is 3): subtract
            n -= 1
        else:                                  # ends in 11: add; the carry clears the run of 1s
            n += 1
        steps += 1
    return steps


print(integer_replacement(8), integer_replacement(7), integer_replacement(2**31 - 1))   # 3 4 32
```

**Try it**
- Print `bin(n)` at every step for 15: `0b1111 → 0b10000 → 0b1000 → 0b100 → 0b10 → 0b1`, 5 steps. One `+ 1` turned four 1s into a single 1.
- Remove `n == 3 or`: `integer_replacement(3)` becomes 3 instead of 2 (3 → 4 → 2 → 1).
- Compare with a brute force that tries both moves at every odd number, `f(n) = 1 + min(f(n + 1), f(n - 1))`, for n in 1..200: always equal.

#### Capstone: a bit array that scales

**Idea:** to keep every operation O(1) for a big universe, cut the bits into fixed-size words: bit `i` lives in word `i >> 6` (that is `i // 64`), at position `i & 63` (`i % 64`). Set, clear and get touch one word. Counting is a popcount per word, and "the next member from `i` on" skips empty words 64 values at a time, then reads the lowest 1 with `x & -x`.

```text
          word 2                 word 1            word 0
  [ 191 ... 130 129 128 ]  [ 127 ... 65 64 ]  [ 63 ... 2 1 0 ]
            ^
            i = 130: word 130 >> 6 = 2, position 130 & 63 = 2        (bytes: byte i >> 3, bit i & 7)
```

```python
class Bits:                                    # a set of integers in [0, n), stored as 64-bit words
    def __init__(self, n):
        self.words = [0] * ((n + 63) // 64)    # STATE: bit i lives in word i >> 6, position i & 63

    def set(self, i):   self.words[i >> 6] |= 1 << (i & 63)
    def clear(self, i): self.words[i >> 6] &= ~(1 << (i & 63))
    def get(self, i):   return (self.words[i >> 6] >> (i & 63)) & 1
    def count(self):    return sum(w.bit_count() for w in self.words)

    def next_set(self, i):                     # smallest member >= i, or -1
        w = i >> 6
        if w >= len(self.words):
            return -1
        word = self.words[w] & ~((1 << (i & 63)) - 1)   # forget the bits below i
        while not word:                        # skip empty words, 64 values at a time
            w += 1
            if w == len(self.words):
                return -1
            word = self.words[w]
        return (w << 6) + (word & -word).bit_length() - 1   # the lowest 1 left in that word


b = Bits(200)
for i in (3, 64, 130, 199):
    b.set(i)
print(b.count(), b.get(64), b.get(65))                                   # 4 1 0
print(b.next_set(0), b.next_set(4), b.next_set(131), b.next_set(200))    # 3 64 199 -1
```

**Try it**
- Drop the mask in `next_set` (use `word = self.words[w]`): `b.next_set(4)` returns 3, an index below 4.
- Flip every bit at once, `b.words = [~w & (2**64 - 1) for w in b.words]`, and call `b.count()`: 252, not 196. The last word also flipped its 56 padding bits (values 200..255), which are not in the universe. [Design](#s24) handles "flip everything" lazily, with one flag and a maintained count.
- Time it (`import time` first): put `random.sample(range(10**6), 20_000)` through `Bits.set` and through a plain int (`seen |= 1 << v`), timing each with `time.perf_counter()`. The int is dozens of times slower, because every `|=` copies the whole number.

### Math recipes

#### Number theory: gcd, primes, fast power

- **Euclid:** every common divisor of `a` and `b` also divides `a % b`, so `gcd(a, b) = gcd(b, a % b)`, and the pair shrinks fast. Then `lcm(a, b) = a // gcd(a, b) * b`.
- **Trial division:** divisors come in pairs `d · (n / d)`, and one of the two is at most √n, so stop when `d * d > n`.
- **Sieve:** to list every prime up to n, cross off the multiples of each prime p starting at `p * p`; the smaller multiples have a smaller prime factor and are crossed off already.
- **Fast power:** write the exponent in binary, `3^13 = 3^8 · 3^4 · 3^1`: square the base once per bit, and multiply it in when the bit is 1.
- **Mod after every multiply:** `(a * b) % m == ((a % m) * (b % m)) % m`, so reducing early never changes the answer, and it keeps every number below m² (under 2⁶³ for m = 10⁹ + 7, which fixed-width languages need). Python never overflows, but `3 ** 10**6` has 477 122 digits, and multiplying giants is slow.
- **Built in:** `math.gcd`, `math.lcm`, `pow(b, e, m)`, `pow(x, -1, m)` (the inverse of x modulo m), `math.isqrt`, `math.comb`.

```python
def gcd(a, b):
    while b:
        a, b = b, a % b                        # (252, 105) -> (105, 42) -> (42, 21) -> (21, 0)
    return abs(a)


def lcm(a, b):
    return abs(a) // gcd(a, b) * abs(b) if a and b else 0     # divide first: smaller numbers


def is_prime(n):                               # trial division up to sqrt(n): a pair has one side there
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def primes_upto(n):                            # sieve of Eratosthenes
    alive = [False, False] + [True] * (n - 1)  # alive[i]: is i still possibly prime?
    for p in range(2, math.isqrt(n) + 1):
        if alive[p]:
            for multiple in range(p * p, n + 1, p):   # smaller multiples are crossed off already
                alive[multiple] = False
    return [i for i in range(n + 1) if alive[i]]


def power_mod(base, exp, mod):
    result, base = 1 % mod, base % mod
    while exp:
        if exp & 1:                            # this bit of exp is 1: multiply its power in
            result = result * base % mod       # reduce after EVERY multiply
        base = base * base % mod               # base, base^2, base^4, base^8, ...
        exp >>= 1
    return result


print(gcd(252, 105), lcm(4, 6), is_prime(91), primes_upto(30))   # 21 12 False [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(power_mod(3, 13, 1000), pow(3, 13, 1000))                  # 323 323
```

**Try it**
- Print `(a, b)` at the top of the `gcd` loop for `gcd(55, 34)`: 8 rounds. Neighbouring Fibonacci numbers are the slowest case for Euclid, and even they finish in O(log) steps.
- Remove the `1 % mod` (start with `result = 1`) and run `power_mod(5, 0, 1)`: 1 instead of 0. Everything is 0 modulo 1, even an empty product.
- Compare `power_mod(3, 10**6, 10**9 + 7)` with `3 ** 10**6 % (10**9 + 7)`: the same answer, but the second first builds a 1.6-million-bit number. The built-in `pow(3, 10**6, 10**9 + 7)` does the fast version for you.

#### Digits and bases

**Idea:** `n % 10` is the last digit and `n // 10` drops it, so digits come out lowest first, and `rev * 10 + d` pushes a digit onto the right end of `rev`. Work on `abs(x)` and put the sign back at the end. Every base works the same way with `divmod(n, b)`, and reading digits back is Horner's rule, `n = n * b + d` (as in `column_number`). Excel columns are base 26 with digits 1..26 and *no zero*, so shift each digit down by one before the divmod. For overflow, a 32-bit language cannot compute `rev * 10 + d` and look afterwards: test *before* pushing, `rev > (LIMIT - d) // 10`. One limit, 2³¹ − 1, serves both signs: −2³¹ could only come from reversing 8463847412, which is not a 32-bit input.

```python
def reverse_int(x):                            # Reverse Integer: 0 if the result leaves 32 bits
    LIMIT = 2**31 - 1
    n, rev = abs(x), 0
    while n:
        n, d = divmod(n, 10)                   # peel off the last digit
        if rev > (LIMIT - d) // 10:            # rev * 10 + d would pass the limit: stop BEFORE
            return 0
        rev = rev * 10 + d                     # push d onto the right of rev
    return rev if x >= 0 else -rev


def is_palindrome_number(x):                   # Palindrome Number, without strings
    if x < 0 or (x % 10 == 0 and x != 0):      # a minus sign, or a trailing 0 that cannot lead
        return False
    rev = 0
    while x > rev:                             # move digits until rev holds the lower half
        x, d = divmod(x, 10)
        rev = rev * 10 + d
    return x == rev or x == rev // 10          # even length, or odd (the middle digit is in rev)


def column_title(n):                           # 1 -> A, 26 -> Z, 27 -> AA
    out = []
    while n:
        n, r = divmod(n - 1, 26)               # shift 1..26 down to 0..25 first
        out.append(chr(ord("A") + r))
    return "".join(reversed(out))


def column_number(title):
    n = 0
    for ch in title:
        n = n * 26 + (ord(ch) - ord("A") + 1)  # Horner: shift one digit left, add this one
    return n


print(reverse_int(-123), reverse_int(1534236469), reverse_int(120))     # -321 0 21
print(is_palindrome_number(12321), is_palindrome_number(1221), is_palindrome_number(10))   # True True False
print(column_title(28), column_title(701), column_number("ZY"))         # AB ZY 701
```

**Try it**
- Remove the `- 1` in `column_title` and run `column_title(26)`: `"BA"` instead of `"Z"`. Plain base 26 writes 26 as "10"; Excel has no zero digit, so 26 is the single digit Z.
- `reverse_int(1463847412)` is 2147483641, which fits; `reverse_int(1563847412)` would be 2147483651, which does not, so it returns 0.
- Drop the `x % 10 == 0 and x != 0` test and run `is_palindrome_number(10)`: `True`. Its trailing 0 becomes the leading digit of `rev`, and the comparison cannot see it.

#### Random sampling

**Idea (reservoir sampling):** to pick k items uniformly from a stream you can't store, keep the first k; after that, item i (0-based) replaces a random member with probability k/(i+1). Why that is uniform: item i gets in with probability k/(i+1); each later item j removes it with probability (k/(j+1)) · (1/k) = 1/(j+1), so it survives with probability j/(j+1); the product k/(i+1) · (i+1)/(i+2) · ... · (n−1)/n telescopes to k/n. With k = 1 this is "random pick" from a stream (Linked List Random Node, Random Pick Index).

```python
def reservoir_sample(stream, k):
    sample = []
    for i, x in enumerate(stream):
        if i < k:
            sample.append(x)                   # the first k fill the reservoir
        else:
            j = random.randrange(i + 1)        # a uniform slot in 0..i
            if j < k:                          # happens with probability k / (i + 1)
                sample[j] = x                  # replace a uniformly chosen member
    return sample


random.seed(0)
hits = Counter()
for _ in range(10_000):
    hits.update(reservoir_sample(range(5), 2))
print(sorted(hits.items()))   # [(0, 3990), (1, 3927), (2, 4004), (3, 4035), (4, 4044)]: all near 4000
```

**Try it**
- Change `random.randrange(i + 1)` to `random.randrange(i)` and rerun the cell: values 2, 3 and 4 now show up about 5000 times and 0 and 1 about 2500. Item 2 always gets in, since `j` can only be 0 or 1.
- Use `k = 1` on `range(3)` for 9000 runs: each value about 3000 times. That is random pick.
- `reservoir_sample(range(3), 5)`: `[0, 1, 2]`. With fewer items than k, you simply get them all.

#### Exact slopes (Max Points on a Line)

**Idea:** all points on one line through an anchor share a direction `(dx, dy)`. Floats can't be trusted as keys, but the direction reduced by the gcd, with a fixed sign, is exact and hashable: `(2, 6)` and `(-1, -3)` both become `(1, 3)`, and vertical lines are `(0, 1)` with no division at all. A copy of the anchor has no direction (`gcd(0, 0)` is 0), but it lies on every line through the anchor, so count copies separately and add them to the best line.

```python
def slope_key(dx, dy):                         # one exact key per line direction
    g = math.gcd(dx, dy)                       # > 0 for two distinct points
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):         # (1, 2) and (-1, -2) are the same line
        dx, dy = -dx, -dy
    return dx, dy


def max_points(points):
    best = 0
    for i, (x1, y1) in enumerate(points):      # anchor every line at its first point
        same, dirs = 1, Counter()              # the anchor and its copies; directions to the rest
        for x2, y2 in points[i + 1:]:
            if (x1, y1) == (x2, y2):
                same += 1                      # a copy lies on every line through the anchor
            else:
                dirs[slope_key(x2 - x1, y2 - y1)] += 1
        best = max(best, same + max(dirs.values(), default=0))
    return best


print(slope_key(2, 6), slope_key(-1, -3), slope_key(0, -5))           # (1, 3) (1, 3) (0, 1)
print(max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))     # 4
print(max_points([[1, 1], [1, 1], [2, 2]]))                             # 3
```

**Try it**
- Use a float key instead, `(y2 - y1) / (x2 - x1) if x2 != x1 else math.inf`, and run `max_points([[0, 0], [94911151, 94911150], [94911152, 94911151]])`: 3. The answer is 2: the two slopes differ, but they round to the same float.
- Delete the sign rule and run `max_points([[0, 0], [1, 1], [-1, -1]])`: 2 instead of 3, because `(1, 1)` and `(-1, -1)` became different keys.
- Call `slope_key(0, 0)`: `ZeroDivisionError`. That is why copies of the anchor never reach it.

### Hard puzzles (optional)

These Hard problems each turn on one idea you would not invent under pressure. Learn the idea and the picture; the code follows from them.

#### Turns and corners: Erect the Fence, Perfect Rectangle

**Turns** (Erect the Fence). The cross product `cross(o, a, b)` is positive when the path o → a → b turns left, negative when it turns right, 0 when it goes straight. Sort the trees; walk left to right building the lower fence on a stack, and pop the last post while the new tree makes a right turn (that post sits above the lower fence; if it is on the fence at all, the upper walk will collect it). Walk back right to left for the upper fence. Popping only on `< 0` keeps trees that stand exactly on a straight stretch of fence.

**Corners** (Perfect Rectangle). Small rectangles tile a big one exactly when (1) their areas add up to the bounding box and (2) toggling every rectangle's four corners in a set leaves exactly the four outer corners: every inner corner is shared by 2 or 4 tiles, so it switches back off.

```text
   cross(o, a, b) > 0       cross(o, a, b) < 0       cross(o, a, b) == 0
           b                  o ---- a                 o ---- a ---- b
           |                         |
     o --- a                         b
       left turn               right turn              straight

   X--------+-----X         A, B, C, D tile the box: every "+" is a corner of exactly 2 tiles,
   |   A    |  B  |         so toggling all corners switches every "+" back off and leaves
   +----+---+-----+         exactly the four X corners on
   |  C |    D    |
   X----+---------X
```

```python
def cross(o, a, b):                            # > 0 left turn, < 0 right turn, 0 straight
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def fence(trees):                              # Erect the Fence: the hull, keeping trees ON edges
    pts = sorted(map(tuple, trees))
    lower, upper = [], []
    for p in pts:                              # left to right along the bottom
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
            lower.pop()                        # right turn: the middle tree is not on the lower fence
        lower.append(p)
    for p in reversed(pts):                    # right to left along the top
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:
            upper.pop()
        upper.append(p)
    return sorted(set(lower + upper))          # the two end trees are in both chains


def is_perfect_cover(rects):                   # Perfect Rectangle
    corners, area = set(), 0
    for x1, y1, x2, y2 in rects:
        area += (x2 - x1) * (y2 - y1)
        corners ^= {(x1, y1), (x1, y2), (x2, y1), (x2, y2)}   # toggle: shared corners cancel
    x1, y1 = min(r[0] for r in rects), min(r[1] for r in rects)
    x2, y2 = max(r[2] for r in rects), max(r[3] for r in rects)
    return corners == {(x1, y1), (x1, y2), (x2, y1), (x2, y2)} and area == (x2 - x1) * (y2 - y1)


print(fence([[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]))   # [(1, 1), (2, 0), (2, 4), (3, 3), (4, 2)]
print(is_perfect_cover([[1, 1, 3, 3], [3, 1, 4, 2], [3, 2, 4, 4], [1, 3, 2, 4], [2, 3, 3, 4]]))   # True
```

**Try it**
- Change `< 0` to `<= 0` in both loops and run `fence([[1, 2], [2, 2], [4, 2]])`: the middle tree (2, 2) disappears. Popping on "straight" removes trees that stand on the fence.
- `is_perfect_cover([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2]])` is `False`. Delete the area test and it says `True`: the two copies of the small square cancel each other's corners.

#### Counting instead of listing: Number of Digit One, K-th Lexicographic Number

When n goes up to 10⁹, find a unit whose size you can compute and count whole units.

**Number of Digit One:** count column by column. In the column worth p, the digit cycles 0..9, each value held for p numbers. Split n into `high` (digits above the column), `cur` (the column's digit) and `low` (digits below): `high` full cycles each show a 1 for p numbers, and the last, partial cycle adds p (`cur > 1`), `low + 1` (`cur == 1`) or nothing (`cur == 0`).

```text
  n = 2315, tens column (p = 10): high = 23, cur = 1, low = 5
  0000..2299: 23 full cycles, each with ten numbers showing a 1 in the tens column -> 23 * 10 = 230
  2300..2315: we are inside the 1-run (cur = 1): 2310..2315                         -> low + 1 = 6
```

**K-th Smallest in Lexicographical Order:** lexicographic order is a pre-order walk of the 10-ary tree whose node v has children 10v..10v+9. Standing on a node, count its subtree (level by level, clipped to n). If the k-th number lies past that whole subtree, skip it in one jump to the next sibling; otherwise step down to the first child.

```text
  n = 13:     1          2   3   4   5   6   7   8   9         pre-order: 1, 10, 11, 12, 13, 2, ..., 9
           /  |  \  \
         10  11  12  13                                         subtree of 1 = {1} + {10..13} = 5 numbers
```

```python
def count_digit_one(n):                        # Number of Digit One
    total, p = 0, 1                            # p = the column's place value: 1, 10, 100, ...
    while p <= n:
        high, cur, low = n // (p * 10), n // p % 10, n % p
        total += high * p                      # every full cycle shows a 1 for p numbers
        if cur > 1:
            total += p                         # the last cycle already passed its whole 1-run
        elif cur == 1:
            total += low + 1                   # inside the 1-run, which has lasted low + 1 numbers
        p *= 10
    return total


def kth_lexicographic(n, k):                   # K-th Smallest in Lexicographical Order
    def subtree_size(prefix):                  # how many numbers in 1..n start with prefix
        size, lo, hi = 0, prefix, prefix + 1
        while lo <= n:
            size += min(n + 1, hi) - lo        # this level is [lo, hi), clipped to n
            lo, hi = lo * 10, hi * 10
        return size

    cur, k = 1, k - 1                          # stand on 1; k = steps still to take
    while k:
        size = subtree_size(cur)
        if size <= k:                          # the answer is past this whole subtree
            k -= size
            cur += 1                           # jump to the next sibling
        else:                                  # the answer is inside: step down
            k -= 1
            cur *= 10
    return cur


print(count_digit_one(13), count_digit_one(2315))           # 6 1768
print(kth_lexicographic(13, 2), kth_lexicographic(13, 6))   # 10 2
```

**Try it**
- Change `low + 1` to `low` and run `count_digit_one(10)`: 1 instead of 2. The number 10 itself is lost.
- Print `cur, k` at the top of each loop for `kth_lexicographic(100, 10)`: it steps down once (1 → 10), skips the subtree {10, 100} in one jump, then hops 11, 12, ... and stops at 17.

#### Blocks and states: Permutation Sequence, Poor Pigs

**Permutation Sequence:** in lexicographic order the n! permutations come in n blocks of (n−1)!, one block per first digit. So the 0-based rank divided by (n−1)! picks the first digit from the unused ones, the remainder is the rank inside that block, and you repeat with (n−2)!: that is writing the rank in the factorial number system.

```text
  n = 4, k = 9 -> rank r = 8 = 1·3! + 1·2! + 0·1! + 0·0!
  unused [1 2 3 4] take index 1 -> 2;  [1 3 4] take index 1 -> 3;  [1 4] take index 0 -> 1;  [4] -> 4:  "2314"
```

**Poor Pigs:** with T = minutesToTest // minutesToDie rounds, a pig ends in one of T + 1 states (dies in round 1, 2, ..., T, or survives), so p pigs can tell apart (T + 1)^p buckets. Give each bucket a p-digit base-(T+1) label and let pig i drink, in round r, every bucket whose i-th digit is r.

```python
def kth_permutation(n, k):                     # Permutation Sequence
    pool, out, r = list(range(1, n + 1)), [], k - 1    # r = 0-based rank
    for i in range(n - 1, -1, -1):
        idx, r = divmod(r, math.factorial(i))  # each choice of the next digit owns i! orders
        out.append(str(pool.pop(idx)))
    return "".join(out)


def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    states = minutes_to_test // minutes_to_die + 1     # dies in round 1..T, or survives
    pigs = 0
    while states ** pigs < buckets:            # p pigs tell apart states ** p buckets
        pigs += 1
    return pigs


print(kth_permutation(3, 3), kth_permutation(4, 9))    # 213 2314
print(poor_pigs(4, 15, 15), poor_pigs(1000, 15, 60))   # 2 5
```

**Try it**
- Forget the `- 1` (`r = k`): `kth_permutation(3, 3)` returns `"231"`, the 4th permutation, and `kth_permutation(3, 6)` crashes with `IndexError`.
- `poor_pigs(125, 1, 4)` is 3 (5³ = 125 exactly) and `poor_pigs(126, 1, 4)` is 4. Counting only "dead or alive" (2 states) would need 7 pigs for 125 buckets.

### Where it goes wrong

1. **Operator precedence.** In Python `&`, `|` and `^` bind tighter than `==`, so `x & 1 == 0` works (unlike C and Java). But `<<` and `>>` bind *looser* than `+` and `-`: `1 << k - 1` is `1 << (k - 1)`, and `x & mask + 1` is `x & (mask + 1)`. Parenthesise every bit expression.
2. **`~x` is negative in Python.** Ints have no fixed width, so `~0b1010 == -11`, not `0b0101`. For a k-bit complement use `x ^ ((1 << k) - 1)`.
3. **Negative numbers never run out of bits.** `-1 >> 1 == -1`, so `while x: x >>= 1` never ends for a negative x, and neither does the `x &= x - 1` loop. Mask first: `x & 0xFFFFFFFF` is the 32-bit pattern, and `to_signed32` turns it back.
4. **Digits of a negative number.** `divmod(-123, 10) == (-13, 7)`, so the last digit comes out as 7; and `divmod(-1, 10) == (-1, 9)`, so `while n:` never ends. Work on `abs(x)` and restore the sign (more on `%` and `//` with negatives in the [Python Toolkit](#s02)).
5. **Stopping a fixed-width loop early.** Reverse Bits must run exactly 32 rounds; stopping when `x == 0` loses the leading zeros that should become trailing zeros.
6. **A huge int as a bitset.** An int bitset costs O(largest value / 64) per operation: perfect for letters, digits and n up to about 10⁴; beyond that, or whenever you claim O(1), use a bytearray or 64-bit words.
7. **Zero passes the power-of-two test.** `0 & (0 - 1) == 0`, so write `x > 0 and (x & (x - 1)) == 0`.
8. **Floats for exact questions.** `math.log(243, 3) == 4.999999999999999`, and `int(math.sqrt(100000001**2 - 1))` is 100000001 while `math.isqrt` gives the true 100000000. Use integers: reduced `(dx, dy)` pairs, cross products, `math.isqrt`, repeated multiplication instead of logs.
9. **Reducing mod at the wrong moment.** Reduce after every multiply (`ans = ans * x % MOD`), but never before comparing: with `a = 10**9 + 8` and `b = 5`, `max(a % MOD, b % MOD)` picks `b`.
10. **Off by one in 1-indexed systems.** Excel columns (`n - 1` before the divmod), the k-th permutation (`k - 1`), and "primes less than n" versus "up to n".
11. **Testing after adding.** In the bit-array template, test bit v *before* you set it, or every value looks like a repeat.
12. **Duplicate points.** `slope_key(0, 0)` divides by `gcd(0, 0) == 0`: count copies of the anchor separately.

### Edge cases to say out loud

0 and 1 (no set bits, one bucket, `is_prime(1)`) · negative numbers (infinite sign bits in Python) · the 32-bit limits (2³¹ − 1 and −2³¹) · the missing value is 0 or n · duplicate points and vertical lines · `mod = 1` · k = 1 and k = the last rank.

```python
assert find_error_nums([2, 2]) == [2, 1] and find_error_nums([1, 1]) == [1, 2]
assert popcount(0) == 0 and popcount(2**32 - 1) == 32
assert reverse_bits(0) == 0 and reverse_bits(2**32 - 1) == 2**32 - 1
assert single_number([-3, 7, -3]) == 7                      # negatives cancel too
assert missing_number([0]) == 1 and missing_number([1]) == 0
assert single_number_ii([-1, -1, -1, 7]) == 7 and get_sum(0, 0) == 0
assert Bits(1).count() == 0 and Bits(1).next_set(0) == -1
assert gcd(0, 5) == 5 and lcm(0, 5) == 0 and gcd(-12, 18) == 6
assert not is_prime(1) and is_prime(2) and primes_upto(1) == []
assert power_mod(5, 0, 1) == 0 and power_mod(-2, 3, 5) == 2  # with a positive modulus, % lands in [0, mod)
assert reverse_int(-2**31) == 0 and reverse_int(0) == 0 and reverse_int(120) == 21
assert is_palindrome_number(0) and not is_palindrome_number(-121)
assert column_title(1) == "A" and column_title(52) == "AZ" and column_number("AAA") == 703
assert max_points([]) == 0 and max_points([[0, 0]]) == 1 and max_points([[0, 0], [0, 0]]) == 2
assert fence([[0, 0]]) == [(0, 0)]
assert count_digit_one(0) == 0 and kth_lexicographic(1, 1) == 1
assert kth_permutation(1, 1) == "1" and kth_permutation(9, math.factorial(9)) == "987654321"
assert poor_pigs(1, 1, 1) == 0
print("edge cases pass")
```

**Try it**
- Digits of a negative number: `divmod(-123, 10)` is `(-13, 7)`, so the last digit comes out as 7, not 3; and `divmod(-1, 10)` is `(-1, 9)`, so a `while n:` digit loop on a negative number never ends. That is why `reverse_int` works on `abs(x)` and puts the sign back at the end.
- What should `missing_number([])` return? Write the assert before running it (0: the range 0..0 lost its only value).
- Add `assert count_digit_one(1000) == 301`: the leading 1 of 1000 counts once, the 300 others come from the three lower columns.

### Variations

The bit-array template is the root of a family: change what a bit means, or how masks are compared. The code for most of these is in the bit toolbox above.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Parity set** | toggle instead of set (`^=`): bit d means "d has been seen an odd number of times" | 1542, 1371 |
| **Prefix masks + hash map** | a substring's mask is the XOR of two prefix masks: the earliest index of each mask for the longest (1542), a `Counter` of masks for how many substrings (1915) | 1542, 1915 |
| **Letter sets** | a word becomes a 26-bit mask: subset test `(w & ~p) == 0` (1178), disjoint test `(a & b) == 0` (318) | 1178, 318 |
| **All subsets of n items** | `for mask in range(1 << n)`: bit i says whether item i is in | 78 |
| **Maximum XOR** | a binary trie of the numbers; greedily take the opposite bit from the top | 421, 1707 |
| **XOR as parity** | pairs cancel: the single number, the missing number, two singles | 136, 268, 260 |
| **Count each bit column** | `% 3` per column for "three times" (137); `ones * (n - ones)` differing pairs per column (477) | 137, 477 |
| **32-bit arithmetic** | mask with `0xFFFFFFFF`, convert back through bit 31 | 371, 190 |
| **AND of a whole range** | the answer is the common binary prefix of the two ends: `while right > left: right &= right - 1` | 201 |
| **Gray code** | `i ^ (i >> 1)`: neighbours differ in exactly one bit | 89 |
| **Rolling bit code** | 2 bits per DNA letter, keep the last 20 bits with `& 0xFFFFF` | 187 |
| **Big universe** | a bytearray or 64-bit words | (no repo problem) |
| **Global flip** | a lazy flag and a maintained count (see [Design](#s24)) | 2166 |
| **Long division** | a remainder seen before starts the repeating part; handle the sign with `abs` | 166 |
| **Simulate one cycle** | after one pass of the moves, bounded iff back at the origin or not facing north | 1041 |

**Count each bit column** (477). The total Hamming distance over all pairs is a sum over bit columns: in a column with `ones` ones and `n - ones` zeros, exactly `ones * (n - ones)` pairs differ. That is 32 passes instead of n² pairs.

```python
def total_hamming_distance(nums):              # Total Hamming Distance (477)
    n, total = len(nums), 0
    for b in range(32):                        # one bit column at a time
        ones = sum((x >> b) & 1 for x in nums)
        total += ones * (n - ones)             # each (1, 0) pair differs in this column
    return total


print(total_hamming_distance([4, 14, 2]))      # 6
```

**Try it**
- Check it against all pairs: `sum(bin(a ^ b).count("1") for a, b in combinations([4, 14, 2], 2))` is also 6.
- Print `ones` for every column of `[4, 14, 2]`: bits 1, 2 and 3 have 2, 2 and 1 ones, so the total is 2·1 + 2·1 + 1·2 = 6.
- Change `range(32)` to `range(3)`: the answer drops to 4. Bit 3 is never looked at, so its two differences (14 against 4, and 14 against 2) are lost.

### Say it in the interview

> "I need to remember which of 1..n I've seen, so I keep one bit per value. I test the bit before setting it; a bit already set means this value is the duplicate. At the end, the one bit of 1..n still 0 is the missing value. The brute force rescans for each value, O(n²). With a fixed-size bit array (a bytearray or 64-bit words) test and set touch one word, so it's O(n) time and n bits. A single Python int also works, but every `|=` copies it, which is fine for a few thousand values and quadratic beyond. If you want O(1) extra space, I'd mark value v by negating `nums[v - 1]`."

Point at the line that tests *before* it sets, and say what a bit means out loud ("bit v of `seen` means v appeared"). The negation trick is in [Arrays & Hashing](#s03). For the math tools, name the constraint that rules out listing (n up to 10⁹), then the unit you count instead: a digit column, a subtree, a block of (n−1)!.

### Problem map

| Problem | Where | Key insight |
|---|---|---|
| Counting Bits | `bit_manipulation/counting_bits.py` | `ans[i] = ans[i >> 1] + (i & 1)`: i is its half with one bit appended |
| Erect the Fence | `math_geometry/erect_the_fence.py` | sort, build lower and upper chains on a stack; pop only on a right turn (cross < 0) so edge trees stay |
| Excel Sheet Column Title | `practice/simple/basics/math/05_base_conversion_and_excel_columns.py` | base 26 with digits 1..26 and no zero: `divmod(n - 1, 26)` |
| Find Longest Awesome Substring | `bit_manipulation/find_longest_awesome_substring.py` | 10-bit prefix parity mask; earliest index of the same mask or of a mask one bit away |
| Integer Replacement | `bit_manipulation/integer_replacement.py` | odd n: subtract on ...01 (and for 3), add on ...11 so the carry clears the run of 1s |
| K-th Smallest in Lexicographical Order | `math_geometry/kth_smallest_in_lexicographical_order.py` | pre-order of the 10-ary tree; skip a prefix's whole subtree if k is past it, else step down |
| Max Points on a Line | `math_geometry/max_points_on_a_line.py` | per anchor, count gcd-reduced (dx, dy) with a fixed sign; copies of the anchor join every line |
| Maximum XOR With an Element From Array | `bit_manipulation/maximum_xor_with_an_element_from_array.py` | sort queries by limit, insert nums up to it into a binary trie, take the opposite bit greedily |
| Missing Number | `bit_manipulation/missing_number.py` | XOR all indices 0..n with all values: present values cancel, the missing one stays |
| Number of 1 Bits | `bit_manipulation/number_of_1_bits.py` | `n &= n - 1` deletes the lowest 1; count the deletions |
| Number of Digit One | `math_geometry/number_of_digit_one.py` | per column p: `high * p` full cycles, plus p, `low + 1` or 0 depending on the column's digit |
| Number of Valid Words for Each Puzzle | `bit_manipulation/number_of_valid_words_for_each_puzzle.py` | Counter of word letter-masks; sum over the puzzle's 128 submasks that contain its first letter |
| Palindrome Number | `practice/simple/basics/math/04_digits_reverse_integer_and_palindrome_number.py` | reverse only the lower half of the digits and compare it with the upper half |
| Perfect Rectangle | `math_geometry/perfect_rectangle.py` | areas add up to the bounding box, and toggling all corners leaves exactly its 4 corners |
| Permutation Sequence | `math_geometry/permutation_sequence.py` | factorial number system: divmod the 0-based rank by (n−1)!, (n−2)!, ... and pop from the unused digits |
| Poor Pigs | `math_geometry/poor_pigs.py` | a pig has T + 1 outcomes; the answer is the smallest p with (T + 1)^p ≥ buckets |
| Random Pick Index | `practice/simple/basics/math/06_random_pick_and_reservoir_sampling.py` | reservoir of size 1 over the matches: keep the i-th match with probability 1/i |
| Reverse Bits | `bit_manipulation/reverse_bits.py` | peel x's lowest bit onto the right of the output exactly 32 times; leading zeros matter |
| Reverse Integer | `practice/simple/basics/math/04_digits_reverse_integer_and_palindrome_number.py` | peel the digits of `abs(x)` with divmod; check `rev > (LIMIT - d) // 10` before pushing a digit |
| Single Number | `bit_manipulation/single_number.py` | XOR everything: pairs cancel, the loner stays |
| Single Number III | `practice/simple/basics/bits/03_xor_tricks_single_number_missing_number.py` | XOR of all is a ^ b; its lowest set bit splits the numbers into two Single Number problems |

### Self-check

1. Why must the bit-array template test bit v *before* it sets it?
<details><summary>Answer</summary>Setting first makes the test always see a 1, so every value would look like a repeat. The test answers "had v appeared <em>before</em> this item?", so it has to run while the set still describes the earlier items only.</details>

2. `x & (x - 1)` and `x & -x`: which one deletes the lowest 1-bit and which one keeps only it?
<details><summary>Answer</summary><code>x - 1</code> flips the lowest 1 and every 0 below it, so <code>x &amp; (x - 1)</code> deletes exactly that 1. <code>-x</code> is <code>~x + 1</code>: it flips every bit <em>above</em> the lowest 1 and keeps the lowest 1 itself, so <code>x &amp; -x</code> keeps only that bit.</details>

3. Why does `while x: x >>= 1` hang for `x = -8`, and what are the two lines that fix it?
<details><summary>Answer</summary>Python's <code>&gt;&gt;</code> keeps the sign: -8 becomes -4, -2, -1, and <code>-1 &gt;&gt; 1</code> is -1 again, so x never reaches 0. Work on the 32-bit pattern: <code>x &amp;= 0xFFFFFFFF</code> first, then the same <code>while x: x &gt;&gt;= 1</code> ends after at most 32 shifts. (Or loop exactly 32 times.)</details>

4. In Maximum XOR With an Element From Array, why sort the queries by their limit?
<details><summary>Answer</summary>Each query may only use numbers ≤ its limit. In increasing limit order the allowed sets only grow, so a single trie that we keep inserting into (never deleting from) holds exactly the allowed numbers when each query is answered. The answers are written back to the queries' original positions.</details>
