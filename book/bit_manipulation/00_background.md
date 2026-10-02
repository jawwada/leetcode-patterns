# Bit Manipulation

*9 problems · Reading time ~16 min*

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

1. **Number of 1 Bits**: the clear-lowest-bit trick, so the loop runs once per 1 instead of once per column.
2. **Counting Bits**: a number is its half plus one appended bit, so the counts of 0..n build on each other like a DP.
3. **Reverse Bits**: moving bits between columns with shifts, and why a fixed width forces exactly 32 steps.
4. **Single Number**: XOR as pair cancellation; the first time we exploit "equal things vanish".
5. **Missing Number**: manufacture the missing pairs yourself (indices against values) so Single Number's trick applies.
6. **Integer Replacement**: the low two bits decide a greedy move; carries are now an ally, not a hazard.
7. **Number of Valid Words for Each Puzzle**: a word becomes a 26-bit set, and submask enumeration flips the loop to the small side.
8. **Find Longest Awesome Substring**: XOR as parity of ten counters, combined with prefix states and first-seen positions.
9. **Maximum XOR With an Element From Array**: the binary trie and the top-down greedy, plus offline sorting of queries so the trie only grows.
