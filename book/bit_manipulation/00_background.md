# Bit Manipulation

*9 problems · Reading time ~24 min*

## The chapter

An integer is a row of 32 switches, and the and, or, xor and shift operators act on all of them at once. This chapter
teaches counting and moving bits without strings, cancellation with xor, reading low bits to make greedy decisions,
bitmasks as small sets, and a binary trie that walks a number bit by bit to maximise an xor.

Problems, in reading order:

1. [Number of 1 Bits](number_of_1_bits.md) · Easy
2. [Counting Bits](counting_bits.md) · Easy
3. [Reverse Bits](reverse_bits.md) · Easy
4. [Single Number](single_number.md) · Easy
5. [Missing Number](missing_number.md) · Easy
6. [Integer Replacement](integer_replacement.md) · Medium
7. [Number of Valid Words for Each Puzzle](number_of_valid_words_for_each_puzzle.md) · Hard
8. [Find Longest Awesome Substring](find_longest_awesome_substring.md) · Hard
9. [Maximum XOR With an Element From Array](maximum_xor_with_an_element_from_array.md) · Hard

## Why this chapter exists

Most of the time you treat an integer as a quantity: you add it, compare it, sort it. This chapter treats an integer as a row of 32 tiny switches, each one on or off, and asks questions about the switches directly. Once you can see the switches, a family of problems that look like counting or searching problems collapse into a handful of one-line operations.

The nine problems fall into five families:

- **Counting and moving bits** (Number of 1 Bits, Counting Bits, Reverse Bits): read the switches of one number, count them, or rearrange them, without ever turning the number into a string.
- **Cancellation with XOR** (Single Number, Missing Number): XOR makes equal things disappear, so "find the one without a partner" becomes "XOR everything".
- **Reading the low bits to make decisions** (Integer Replacement): the last two bits of a number tell you which move is cheaper, so a search tree collapses into a greedy walk.
- **Bitmasks as small sets** (Number of Valid Words for Each Puzzle, Find Longest Awesome Substring): a set of at most 26 letters or 10 digits fits in one integer, so set equality is `==`, subset is one AND, and "which counts are odd" is a running XOR.
- **Bits as a path in a tree** (Maximum XOR With an Element From Array): a binary trie stores numbers by their bits from the top down, and a greedy walk down it finds the partner that maximises XOR.

## What it is

An integer in memory is a fixed row of bits. Number the columns from the right, starting at 0. Column `i` is worth `2^i`. The number is the sum of the worths of the columns that hold a 1.

```text
n = 44, as a 32-bit word (one char per column)

col: 31                             5 4 3 2 1 0
     0000000000000000000000000000 1 0 1 1 0 0
                                  | | | | | |
worth:                           32 16 8 4 2 1
44 = 32 + 8 + 4         set columns = {5, 3, 2}
```

Read the bottom line again: a number IS a set of column indices. 44 is the set `{2, 3, 5}`. That double reading is the whole chapter. Sometimes we care about the value (Integer Replacement halves it), sometimes about the set (the puzzle problem asks whether one letter-set fits inside another), and often about both at once.

Two facts about the layout matter constantly:

- **Shifting is multiplying by two.** `n << 1` slides every column one place to the left, appending a 0 at column 0. That doubles the value. `n >> 1` slides right, and column 0 falls off the edge. That halves the value, rounding down.
- **Column 0 is parity.** `n & 1` is 1 exactly when `n` is odd.

```text
n      =  0 1 0 1 1 0   (22)
n << 1 =  1 0 1 1 0 0   (44)  all columns move left, 0 enters
n >> 1 =  0 0 1 0 1 1   (11)  all columns move right, col 0 lost
```

Negative numbers are stored in **two's complement**: `-n` is `~n + 1`, where `~n` flips every column. The useful consequence is that `n` and `-n` agree on the lowest set bit and on everything below it, and disagree on everything above it. We will exploit that in a moment.

## Operations and what they cost

Every operator works on all columns at once, independently, in one machine instruction. Here are the per-column truth tables:

```text
 a b | a&b  a|b  a^b        a | ~a
 0 0 |  0    0    0         0 |  1
 0 1 |  0    1    1         1 |  0
 1 0 |  0    1    1
 1 1 |  1    1    0
       both  any  differ
```

The tables are easy. What each one is FOR is the useful part. Think of the second operand as a **mask**, a stencil you lay over the number:

| Operation | Expression | Cost | What it is for |
|---|---|---|---|
| test bit i | `(n >> i) & 1` | O(1) | reads one column |
| set bit i | `n \| (1 << i)` | O(1) | OR with 1 forces a column on |
| clear bit i | `n & ~(1 << i)` | O(1) | AND with 0 forces a column off |
| toggle bit i | `n ^ (1 << i)` | O(1) | XOR with 1 flips a column |
| keep only a mask | `n & m` | O(1) | AND keeps columns where the mask is 1 |
| clear lowest set bit | `n & (n - 1)` | O(1) | borrow ripples to the lowest 1 |
| isolate lowest set bit | `n & -n` | O(1) | two's complement agrees only there |
| subset test | `a & ~b == 0` | O(1) | nothing of `a` lies outside `b` |
| popcount | `n.bit_count()` | O(1) | hardware counts the ones |
| shift by k | `n << k`, `n >> k` | O(1) | multiply / floor-divide by `2^k` |

The two lowest-bit tricks deserve a drawing, because Number of 1 Bits is built on the first one.

```text
clear lowest set bit: n & (n - 1)

n       = 1 0 1 1 0 0   (44)
n - 1   = 1 0 1 0 1 1   borrow: lowest 1 -> 0, zeros below -> 1
          ----------- AND
result  = 1 0 1 0 0 0   (40)   lowest 1 gone, rest untouched
```

Subtracting 1 has to borrow from somewhere. It borrows from the lowest 1, which becomes 0, and every 0 below it becomes 1. Everything above that 1 is unchanged. AND-ing the two rows keeps the unchanged top, kills the flipped 1, and kills the new 1s below it.

```text
isolate lowest set bit: n & -n

n       = ...0 1 0 1 1 0 0   (44)
~n      = ...1 0 1 0 0 1 1   every column flipped
-n=~n+1 = ...1 0 1 0 1 0 0   carry stops at the lowest 1 of n
          ---------------- AND
result  = ...0 0 0 0 1 0 0   (4)
```

XOR has two readings, and the chapter uses both.

**XOR cancels pairs.** `a ^ a = 0` and `a ^ 0 = a`, and the order you XOR things in does not matter. So if you XOR a pile of numbers in which everything appears twice except one, the pairs vanish and the loner remains.

**XOR is parity.** Look at one column of many numbers. XOR-ing them all gives 1 in that column exactly when an odd number of them had a 1 there. A running XOR is a row of 32 odd/even counters, one per column.

```text
column-wise parity of 4, 1, 2, 1, 2

        4 = 1 0 0
        1 = 0 0 1
        2 = 0 1 0
        1 = 0 0 1
        2 = 0 1 0
  ones in col: 1 2 2
  parity     : 1 0 0   = 4   the paired values cancelled
```

A **bitmask** is a set of up to 32 (in Python, any number of) small things, stored as one integer. Letter `c` becomes bit `ord(c) - 97`. Union is `|`, intersection is `&`, "add element" is `|= 1 << i`. The set of all subsets of a mask `p` can be walked without touching any non-subset, using `sub = (sub - 1) & p`:

```text
submasks of p = 1011 (bits {0,1,3}), walked downward

 sub     how we got it            set
 1011    start at p               {3,1,0}
 1010    (1011-1) & 1011          {3,1}
 1001    (1010-1) & 1011          {3,0}
 1000    (1001-1) & 1011          {3}
 0011    (0111) & 1011            {1,0}
 0010    (0010) & 1011            {1}
 0001    (0001) & 1011            {0}
 0000    (0000) & 1011            {}     stop
 8 rows = 2^3: one per subset of the 3 set bits
```

Subtracting 1 counts down in binary, and AND-ing with `p` snaps the count onto the columns that `p` owns. Think of the 3 owned columns as a tiny 3-bit counter going from 111 to 000, with the unowned columns glued at 0.

## The invariant

Every bit operation in this chapter is **column-wise**: the output in column `i` depends only on column `i` of the inputs. Only three things cross columns: shifts (which move columns), and the carry or borrow of `+` and `-`. That is why `n & (n - 1)` works (the borrow is the only cross-column effect, and it stops at the lowest 1), and why XOR parity works (no carries at all, so each column keeps its own count).

Hold that invariant whenever you reason: "what happens to column `i`?" If the answer only involves column `i`, you can reason about one column and multiply by 32.

```text
legal reasoning: XOR of 3 and 5, column by column

   3 = 0 1 1
   5 = 1 0 1
 3^5 = 1 1 0  (6)   each column decided alone

illegal reasoning: treating + like XOR

   3 = 0 1 1
   5 = 1 0 1
 3+5 = 1 0 0 0 (8)  carry crossed from col 0 to col 3;
                    "1 1 0" would be wrong
```

## How to picture it

Carry two pictures.

The first is **a row of switches**. Every number is a strip of 32 lamps. AND, OR, XOR and NOT are stencils laid over the strip; shifts slide the strip; `+1` and `-1` send a ripple from the right that stops at the first lamp it can absorb.

The second is **a binary trie**: the strip read from the top bit down as a path in a tree, left edge for 0, right edge for 1. Store several numbers and their paths share their common prefixes. This is the picture for "which stored number has the largest XOR with x?": XOR rewards a disagreement, and a disagreement in a higher column outweighs every lower column combined, so walk down from the root and at every level take the edge opposite to x's bit if it exists.

```text
trie of {0, 1, 2, 3, 4} on 3 bits     x = 5 = 101

             root
         0 /      \ 1    bit 2: x=1, want 0 -> left
          *        *
       0 / \ 1     | 0   bit 1: x=0, want 1 -> right
        *   *      *
      0/\1 0/\1    | 0   bit 0: x=1, want 0 -> left
      0  1 2  3    4
           ^ path 0,1,0 = 2;   5 ^ 2 = 7
```

Stored as arrays it is just `child[node] = [left, right]`, with 0 meaning "no child" (numbering shown breadth-first; real code numbers nodes in insertion order):

```text
node: 0      1      2      3      ...
     [1, 2] [3, 4] [5, 0] [6, 7]  ...  index of child per bit
```

## Advanced patterns

The operations above are the alphabet. What follows are the words built from them: seven moves that keep coming back in the harder problems. Each one rests on the column-wise invariant plus one extra observation. If you can say that observation out loud, you can rebuild the pattern from scratch in an interview.

### 1. Peel the lowest bit: every number points at a smaller one

**When it shows up**: you need a per-number quantity (popcount, a lowest-bit value) for one number fast, or for every number from 0 to n, and the quantity is additive over set bits.

**The intuition**: `n & (n - 1)` is not just "delete a bit". It is a pointer from `n` to a strictly smaller number that differs from `n` in exactly one column. Follow the pointer repeatedly and you reach 0 after exactly popcount(n) hops, so a loop built on it does work proportional to the answer, not to the width. Read the other way, it is a recurrence: anything additive over the set bits of `n` equals the same thing for `n & (n - 1)`, plus the contribution of the bit you removed. The shift gives a second pointer, `n >> 1`, which drops column 0 instead of the lowest 1. Both pointers land on smaller numbers, so if you fill a table from 0 upward, the entry you need has always been filled already.

```text
two ways a number points at a smaller one

 i   bits   i&(i-1)       i>>1 , i&1
 9   1001   8  (1000)     4 (100), 1
10   1010   8  (1000)     5 (101), 0
11   1011  10  (1010)     5 (101), 1
12   1100   8  (1000)     6 (110), 0

popcount(12) = popcount(8) + 1 = popcount(0) + 2 = 2
popcount(11) = popcount(5) + 1 = 3     (via the shift)
```

The isolating twin, `n & -n`, is the same idea seen from the other side: it names the lowest column as a value. A Fenwick tree is nothing more than this: index `i` is responsible for a block of length `i & -i`, and stepping `i += i & -i` or `i -= i & -i` jumps between blocks in O(log n) hops.

**Where you'll use it**: Number of 1 Bits (the hop loop), Counting Bits (the table filled from the shift pointer, or equally from the `i & (i - 1)` pointer). Beyond the chapter: Range Sum Query - Mutable (LeetCode 307) with a Fenwick tree.

### 2. Manufacture the pairs, then let XOR cancel them

**When it shows up**: "every value appears twice except", or "one value from a known range is missing", with a demand for O(1) extra space.

**The intuition**: XOR is a set-symmetric-difference machine. Anything that enters an even number of times vanishes, anything that enters an odd number of times survives, and order does not matter. So the craft is not the XOR itself; it is arranging for everything you do not want to appear exactly twice. In Missing Number the input has no pairs, so you create them: XOR in every index 0..n as well, and each present value meets its own index while the missing one meets nobody. When the range is fixed, the XOR of 0..n has a closed form that repeats every four numbers, so you do not even need the loop over indices. And if two loners survive (Single Number III), their XOR is nonzero, so it has a lowest set bit; that bit is a column where the two loners disagree, and splitting the input by that column puts one loner in each half, where the single-loner trick applies again.

```text
XOR of 0..n repeats with period 4

 n   bits   0^1^..^n   rule (n % 4)
 0   0000      0       0 -> n
 1   0001      1       1 -> 1
 2   0010      3       2 -> n+1
 3   0011      0       3 -> 0
 4   0100      4       0 -> n
 5   0101      1       1 -> 1
 6   0110      7       2 -> n+1
 7   0111      0       3 -> 0

Missing Number, nums = [3, 0, 1], n = 3
 indices  0 1 2 3   values  3 0 1
 0^1^2^3 ^ 3^0^1 = 2   every present value met its twin
```

**Where you'll use it**: Single Number (pairs are given), Missing Number (pairs are manufactured from indices). Beyond the chapter: Single Number III (LeetCode 260) for the split-by-a-differing-bit step.

### 3. Carries are a tool: a run of 1s costs one +1

**When it shows up**: you choose between +1 and -1 (or add/subtract a power of two) and want the fewest moves to reach a target, usually 0 or 1.

**The intuition**: the cost of reaching 1 by halving is roughly "how many 1s you must get rid of, plus how many columns tall the number is". Subtracting 1 at an odd number deletes exactly one 1. Adding 1 sends a carry left through the whole trailing run of 1s and replaces the run with a single 1 one column higher. So a run of length two or more is cheaper to wipe with one carry than to chip at one bit at a time. The decision is local: the low two bits already tell you whether you are sitting at the bottom of a run (`11`) or on an isolated 1 (`01`). The one exception is 3, where the carry creates a new top column and there is nothing left above to pay for it.

```text
n = 15 = 1111, two ways down

 -1 first: 1111 -> 1110 -> 111 -> 1000 -> 100 -> 10 -> 1
           15      14      7      8      4     2     1
           6 moves (the run was chipped, then carried anyway)

 +1 first: 1111 -> 10000 -> 1000 -> 100 -> 10 -> 1
           15      16       8      4     2     1
           5 moves (one carry erased all four 1s)
```

**Where you'll use it**: Integer Replacement. Beyond the chapter: Minimum Operations to Reduce an Integer to 0 (LeetCode 2571), where each run of 1s costs two moves and a lone 1 costs one.

### 4. Tally the masks, then enumerate submasks from the small side

**When it shows up**: many items, each reducible to a set over a small alphabet, and queries of the form "how many items are subsets of this set" (or supersets), with one side of the relation much smaller than the other.

**The intuition**: two compressions stack. First, items that have the same set are interchangeable, so replace 10^5 words by a counter keyed by mask; duplicates and letter order disappear. Second, a subset relation can be checked from either side, and the cost of each side is 2^(bits on that side). A 7-letter puzzle has 128 submasks; a word with 20 distinct letters has a million. So you always enumerate from the side with fewer set bits and look each candidate up in the counter. A forced element (the puzzle's first letter) is handled by removing it from the mask, enumerating the rest, and OR-ing it back in, which halves the work and drops an `if`. If every mask in a k-bit universe walks all of its submasks, the total is 3^k pairs, because each column independently is "outside", "in the mask only", or "in both".

```text
puzzle p = {a, c, e} -> 10101, forced letter F = a -> 00001

walk submasks of p ^ F = 10100, OR F back in:

 sub     sub | F    letters    cnt lookup
 10100   10101      {e,c,a}    cnt[10101]
 10000   10001      {e,a}      cnt[10001]
 00100   00101      {c,a}      cnt[00101]
 00000   00001      {a}        cnt[00001]
 4 = 2^2 lookups instead of 2^3 with a test
```

**Where you'll use it**: Number of Valid Words for Each Puzzle. Beyond the chapter: Maximum Product of Word Lengths (LeetCode 318) for the word-to-mask step; sum-over-subsets DP when every mask needs an answer.

### 5. Prefix parity masks with first-seen positions

**When it shows up**: "longest (or count of) substrings where each symbol appears an even number of times", "can be rearranged into a palindrome", with a small alphabet.

**The intuition**: this is prefix sums with XOR as the addition. Keep a running mask `M` whose bit `d` says whether symbol `d` has appeared an odd number of times so far. The parities of a substring `s[i:j]` are `M[j] ^ M[i]`, because the shared prefix cancels column by column. A condition on the substring's parities therefore becomes a condition on a pair of prefix masks. "All even" means the two masks are equal; "at most one odd" means they are equal or differ in one bit, which gives `1 + alphabet` partner masks per position. To get the longest substring, store for each mask the earliest index where it appeared, seed the empty prefix at index -1, and never overwrite. To count substrings instead, store how many times each mask appeared.

```text
s = "3242415", columns d5..d0 shown (d6..d9 stay 0)

 j  char  M after j   first-seen gets
 -   -    000000      M=000000 at -1  (seed)
 0   3    001000      001000 at 0
 1   2    001100      001100 at 1
 2   4    011100      011100 at 2
 3   2    011000      011000 at 3
 4   4    001000      already seen at 0: keep 0

at j = 4, try the 11 partners of M = 001000:
 M itself      001000  first 0   length 4  "2424"
 flip d3       000000  first -1  length 5  "32424"  best
 flip d2       001100  first 1   length 3  "424"
 flip d4       011000  first 3   length 1  "4"
 other 7 flips never seen
```

**Where you'll use it**: Find Longest Awesome Substring. Beyond the chapter: Find the Longest Substring Containing Vowels in Even Counts (LeetCode 1371), Number of Wonderful Substrings (LeetCode 1915).

### 6. Decide the answer one bit at a time, from the top

**When it shows up**: "maximum XOR", "maximum AND", or any objective that is a number you build from bits, over pairs or subsets.

**The intuition**: bit `b` is worth `2^b`, and all lower bits together are worth at most `2^b - 1`. So when maximising, the answer's top bit is decided first and is never revisited: any candidate with a 1 there beats every candidate with a 0, whatever happens below. That turns the search into 30 yes/no questions, each asked with the higher bits already locked in. A binary trie answers the question "can I disagree with x here, given the path so far?" by checking whether the opposite child exists. Without a trie, a hash set of prefixes does the same: to test whether the answer can start with the bit pattern `cand`, check whether some pair of prefixes XORs to `cand`, using `a ^ b = cand` exactly when `a ^ cand = b`.

```text
max XOR of a pair in [3, 10, 5, 25, 2, 8], bits 4..0

 bit  prefixes (top bits)    try ans  pair exists?  ans
  4   {0, 1}                 1        yes           1
  3   {0, 1, 11}             11       yes           11
  2   {0, 1, 10, 110}        111      yes           111
  1   {1,10,100,101,1100}    1111     no            1110
  0   {all 6 numbers}        11101    no            11100
 answer 11100 = 28 = 5 ^ 25
```

**Where you'll use it**: Maximum XOR With an Element From Array (trie walk). Beyond the chapter: Maximum XOR of Two Numbers in an Array (LeetCode 421), where the prefix-set version above is a common alternative.

### 7. Sort the queries offline so the structure only grows

**When it shows up**: each query restricts the allowed items by a threshold ("elements not exceeding m", "edges with weight below limit"), and the structure you need (trie, union-find) is easy to grow but hard to shrink or filter.

**The intuition**: you are told all the queries up front, so you may answer them in any order and write each answer back to its original index. Sort the queries by threshold and the items by value. Then the allowed set for each query is a prefix of the sorted items, and that prefix only lengthens from one query to the next. One pointer walks the items; before each query it inserts everything up to the threshold. Each item is inserted once, so the whole sweep costs one sort plus one insertion per item, and each query sees a structure that contains exactly its allowed items and nothing else.

```text
nums sorted:  0  1  2  3  4      queries (x, m) sorted by m

 query m=1   [0  1] 2  3  4      ptr -> 2   trie = {0,1}
 query m=3   [0  1  2  3] 4      ptr -> 4   trie = {0..3}
 query m=6   [0  1  2  3  4]     ptr -> 5   trie = {0..4}
 ptr only moves right; answers written to original slots
```

**Where you'll use it**: Maximum XOR With an Element From Array (the threshold sweep). Beyond the chapter: Checking Existence of Edge Length Limited Paths (LeetCode 1697), the same sweep with union-find.

## Signals in a problem statement

- "without extra space", "in O(1) memory", "every element appears twice except" -> XOR cancellation.
- "number of 1 bits", "Hamming", "binary representation", "32-bit unsigned" -> direct column work.
- "power of two", "divide by 2", "halve" -> look at the low bits; shift instead of divide.
- A small alphabet (26 letters, 10 digits) and a question about which symbols are present, or which counts are odd -> bitmask of the alphabet.
- "rearranged into a palindrome", "each vowel an even number of times" -> parity mask with prefix XOR.
- n <= 20 or a set of at most 7 to 20 items -> enumerate all 2^n masks or all submasks.
- "maximum XOR", "XOR of a pair" -> binary trie, greedy from the top bit.
- Counter-signals: if counts matter beyond odd/even (a value appears three times, "at least k"), XOR alone fails and you need per-column counting mod k or a hash map. If the alphabet is huge (arbitrary integers as set elements), a mask will not fit and a real set is right.

## Python toolbox

Python integers are unbounded. There is no overflow, `1 << 100` is fine, and a negative number behaves as if it had infinitely many leading 1s. That means `~5 == -6`, and `bin(-5)` prints `'-0b101'` rather than 32 bits. When a problem says "32-bit", you must impose the width yourself, either by masking or by looping exactly 32 times:

```python
M = 0xFFFFFFFF
x = (~5) & M            # 4294967290, the 32-bit view
bin(44)                 # '0b101100'
format(44, '032b')      # zero-padded 32-char string
(44).bit_count()        # 3  (3.10+); older: bin(44).count('1')
(44).bit_length()       # 6: index of top set bit + 1
44 & -44                # 4: lowest set bit
```

Masks of letters, and walking submasks:

```python
m = 0
for c in "able":
    m |= 1 << (ord(c) - 97)       # set of letters
sub = p
while True:
    use(sub)
    if sub == 0: break
    sub = (sub - 1) & p           # next smaller submask
```

`functools.reduce(operator.xor, nums, 0)` XORs a whole list in one line.

## Mistakes people make

1. **Looping `while n:` when a fixed width matters.** Reverse Bits must run 32 times even after `n` hits 0, or the leading zeros are lost. Fix: `for _ in range(32)`.
2. **Forgetting operator precedence.** `n & 1 == 0` parses as `n & (1 == 0)`. Fix: write `(n & 1) == 0`.
3. **Using `/` to halve.** `n / 2` gives a float in Python. Fix: `n >> 1` or `n // 2`.
4. **Confusing `n & (n - 1)` with `n & -n`.** The first deletes the lowest 1, the second keeps only it. Fix: draw the borrow once and remember which is which.
5. **Expecting a 32-bit answer from `~x`.** Python gives a negative number. Fix: `~x & 0xFFFFFFFF`.
6. **Using XOR when items appear three times.** Three copies leave one copy's bits behind. Fix: count each column mod 3.
7. **Enumerating submasks of the wrong side.** A word mask can have 26 bits (67 million submasks); a 7-letter puzzle has 128. Fix: always enumerate from the small set.
8. **Off-by-one in the submask loop.** `while sub:` skips the empty set. Fix: process, then break on 0, then step.
9. **Overwriting "first seen" with a later index.** Longest-span problems need the earliest position. Fix: only insert when the key is absent.
10. **Building the trie with too few bits.** Values below 10^9 need 30 levels. Fix: derive the width from the constraint, not from the sample.

## The journey ahead

The nine problems climb from "look at the columns of one number" to "build a data structure out of columns". Each one leaves you holding a tool that a later one picks up.

### Warm-up: reading and moving the columns

**Number of 1 Bits.** The obvious answer checks all 32 columns, and it is fine. The interesting question is whether you can skip the zeros: a number with three 1s should cost three steps, not thirty-two. `n & (n - 1)` deletes exactly one 1 per step, and this is where you first draw the borrow and see it stop at the lowest 1.

**Counting Bits.** Now you need the popcount of every number from 0 to n, and running the previous loop n times feels wasteful because the answers clearly overlap. The question is which smaller number already knows most of the answer. `i >> 1` is `i` with its last column dropped, so its count is already in the table; add `i & 1` and you are done. It is the first time a bit operation acts as a pointer to a smaller subproblem.

**Reverse Bits.** Moving columns is harder than reading them: bit 0 has to travel to bit 31. You peel bits off the bottom of `n` and push them onto the bottom of the result, which reverses their order the way unloading one stack into another does. The trap is Python itself: there is no fixed width, so stopping when `n` reaches 0 silently drops leading zeros. You learn to impose 32 columns by hand.

### XOR: making equal things vanish

**Single Number.** Every value appears twice except one, and you may use no extra memory, so a hash set of seen values is off the table. The puzzle is how to "remember" pairs without storing them. XOR answers it: pairs cancel column by column, regardless of order, and the loner is what is left. This is the chapter's first use of XOR as parity.

**Missing Number.** It looks like Single Number's opposite: nothing repeats, one thing is missing. The new idea is that you can create the pairs yourself, by XOR-ing the indices 0..n alongside the values, so each present value meets its twin and the missing one does not. The sum formula works too; XOR is the version that cannot overflow in a fixed-width language.

### Carries as an ally

**Integer Replacement.** Halve when even, add or subtract 1 when odd, and minimise the moves. It looks like a search problem, and BFS is a correct but slow first attempt. The turning point is reading the low two bits: a number ending in `11` sits at the bottom of a run of 1s that one carry can erase, while one ending in `01` wants the 1 removed directly. After four problems spent avoiding carries, here a carry does the useful work, and 3 is the single exception you have to justify.

### The Hard end: masks, prefixes and tries

**Number of Valid Words for Each Puzzle.** 10^5 words against 10^4 puzzles makes 10^9 pairs, so checking each pair is hopeless. The questions to ask: which details of a word actually matter (only its set of letters), and from which side should the subset test be run? Words collapse into a counter of 26-bit masks, and each puzzle walks its 64 submasks that contain the first letter. This is where a number stops being a value and becomes a set, and where `sub = (sub - 1) & p` earns its keep.

**Find Longest Awesome Substring.** "Can be rearranged into a palindrome" sounds like a question about arrangements, but it is really about parity: at most one digit may appear an odd number of times. That parity fits in a 10-bit mask, and XOR makes prefix masks behave like prefix sums. The new move combines Single Number's parity reading with a dictionary of first-seen positions, and asks 11 partner questions per character instead of one.

**Maximum XOR With an Element From Array.** Two difficulties stacked. Maximising XOR against arbitrary stored numbers needs a binary trie and a greedy walk from the top bit, because one high bit beats all lower bits together. And each query only allows numbers up to a bound `m`, which the trie cannot filter cheaply. Sorting queries by `m` offline means the trie only ever grows. Every earlier idea shows up here: columns, XOR as disagreement, bits as a path, and a decision made one column at a time.
