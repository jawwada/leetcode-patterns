## Math, Bits & Geometry

> An integer is a row of bits, and a row of bits is a small set: bit `v` is 1 exactly when `v` is in it. Bits answer set questions a whole word at a time; the math tools count things instead of listing them.

[Matrices](#s21) turned a grid into index arithmetic on `(r, c)`. This section does the same arithmetic inside one integer, whose bits are a row of cells you can set, flip and count, and then on the digits, primes and points behind the math questions.

**Reach for it when** the problem mentions *bits*, *XOR*, *powers of two*, *"every element appears twice except one"*, *subsets of a small set* (n ≤ 20, 26 letters, 10 digits), *parity* ("an odd number of times"), *modulo 10⁹ + 7*, *gcd, primes or digits*, *points, lines and slopes*, or when n goes up to 10⁹ so nothing can be listed one at a time.

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

A set of small integers, such as letters, digits or up to about 60 items, fits in one word, so "add", "is it in?", union, intersection, subset test and "flip the parity" are each one operation instead of a loop. The math tools win the same way, by **counting instead of listing**: the sieve crosses off multiples instead of testing every number, fast power squares instead of multiplying n times, and the Hard puzzles at the end count a whole digit column, subtree or block of permutations at a time.

### From idea to code

Two parts follow, **bits** and then **math recipes**; the Hard puzzles that reuse them wait at the end of Variations. The bits rest on one template, the one "bit array" interview questions are built on: a set of small integers stored as bits. The idea in one sentence: *to remember which small integers you have seen, keep one bit per possible value: test bit `v` to ask, set bit `v` to add.*

The **State** is one integer, `seen`, used as a set, and its **Definition** is that `(seen >> v) & 1` is 1 exactly when value `v` has appeared so far. The **Invariant** follows: after reading `nums[i]`, `seen` holds exactly the values in `nums[0..i]`. **Init** is `seen = 0`, the empty set.

A **Step** tests bit `v` and only *then* adds it, `seen |= 1 << v`: the test asks whether v appeared *before* this item, so it must run while `seen` still describes the earlier items. The **Record** happens when the test finds the bit already set, a repeat. The **Return** reads what is missing from the bits still 0 at the end, where `full & ~seen` is "everything not seen" in one step.

The template solves Set Mismatch: a list should hold 1..n once each, but one number was copied over another, so one value appears twice and one is missing; return both. `[1, 2, 2, 4]` gives `[2, 3]`. The set {1, ..., n} is `(1 << (n + 1)) - 2`, the bits 0..n minus bit 0, and `full & ~seen` keeps the single value never seen. A lone bit turns into its value with `.bit_length() - 1`.

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

How big can the set be? An int bitset costs O(largest value / 64) per operation: perfect for letters, digits and n up to about 10⁴; beyond that, or whenever you claim O(1), use a bytearray or 64-bit words. A Python int is immutable, so every `|=` builds a new one. The capstone at the end of the bit toolbox builds the 64-bit-word version.

### Watch it work

The trace runs the template on `[3, 1, 4, 1, 5, 2]` and draws the set after each value as 8 bits, value 0 on the right. The second 1 finds its bit already set, so the test fires before the add changes anything. The last two lines are the full set {1, ..., 6} and what `seen` lacks of it: one bit, the missing value 6.

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

The template used three moves on single bits. The toolbox adds the rest, each piece building on the one before: the tricks to type without thinking, XOR as parity, Python's negative numbers, a greedy that reads the lowest bits, and a bit array that scales.

`1 << i` is a lone 1 at position i: OR it in to set bit i, AND with its complement to clear it, XOR to flip it, and shift down and `& 1` to read it. On whole sets, `a | b`, `a & b` and `a & ~b` are union, intersection and difference, and a is a subset of b exactly when `(a & ~b) == 0`. `for mask in range(1 << n)` visits every subset of n items, bit i saying whether item i is in.

The lowest 1 has tricks of its own. `x & (x - 1)` deletes it, so a loop of it runs once per 1-bit, and a power of two, with exactly one 1, becomes 0; so does 0 itself, so test `x > 0` too. `x & -x` keeps only the lowest 1, which makes `(x & -x).bit_length() - 1` the smallest member, and `~x & (x + 1)` keeps the lowest *0* as a lone 1. The size of the set is `x.bit_count()`.

The cell tries each trick on 180, the set {2, 4, 5, 7}, lists the eight subsets of `"abc"`, then solves three problems. Number of 1 Bits counts the 1s of an integer, 4 for 180, with one `x &= x - 1` per 1-bit. Counting Bits asks for that count for every i from 0 to n, `[0, 1, 1, 2, 1, 2]` for n = 5, and since `i >> 1` is `i` without its last bit, each answer reuses an earlier one. Reverse Bits mirrors a 32-bit integer, so 1 becomes 2³¹ = 2147483648.

```python
def show(x, width=8):
    return format(x, f"0{width}b")             # x in binary, padded to width digits


x = 0b10110100                                 # 180, the set {2, 4, 5, 7}
print((x >> 5) & 1, (x >> 3) & 1)              # 1 0: get bit 5, get bit 3
print(show(x | (1 << 3)), show(x & ~(1 << 2)), show(x ^ (1 << 7)))   # 10111100 10110000 00110100
print(show(x & (x - 1)), show(x & -x))         # 10110000 00000100: delete / keep the lowest 1
y = 0b10110111
print(show(~y & (y + 1)))                      # 00001000: the lowest 0 of y, as a lone 1
print([[ch for i, ch in enumerate("abc") if (mask >> i) & 1] for mask in range(1 << 3)])
# [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]


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
- Change `"abc"` to `"abcd"` and `1 << 3` to `1 << 4` in the subsets line: 16 subsets, and the last 8 are the first 8 with `'d'` added.

XOR remembers, for every bit column, whether it has seen an odd or an even number of 1s. Values that come in pairs cancel, whatever their order, so what is left is the value with no partner. Single Number asks for the one value that appears once when every other value appears twice: `[4, 1, 2, 1, 2]` gives 4. Missing Number asks which value of 0..n is absent from n distinct numbers, `[3, 0, 1]` gives 2: XOR every index with every value, and each present value cancels against its equal index.

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
- Run `single_number([2, 2, 3, 2])`: 1, which is neither value. A value that appears three times no longer cancels; count each column modulo 3 instead, as Single Number II does in the next cell.
- Start `missing_number` with `acc = 0` and run `missing_number([0, 1])`: 0 instead of 2. The value n never got a partner.
- Single Number III (260) has two loners: `both = single_number([1, 2, 1, 3, 2, 5])` is `3 ^ 5 = 6`, and `low = both & -both` is 2, a bit where 3 and 5 differ. XOR-ing only the numbers that have that bit, `single_number([v for v in [1, 2, 1, 3, 2, 5] if v & low])`, gives 3, and `both ^ 3` is 5.

A Python int has no width. A negative number behaves as if its sign bit repeated forever to the left, so `-5` is `...1111 1011` with infinitely many 1s. The operators work on that infinite pattern, which is why `x & -x` is right for negatives too, but also why `bin(-5)` cannot show the bits, why `-1 >> 1` stays `-1`, and why a loop that waits for the bits to run out never ends. When a problem means 32-bit integers, mask to 32 bits, work there, and convert back at the end.

```text
   5 = ...0000 0101          no width: the sign bit repeats forever to the left
  -5 = ...1111 1011          bin(-5) hides this and prints '-0b101'
  -5 & 0xFF       = 1111 1011 = 251               keep the low 8 bits
  -5 & 0xFFFFFFFF = 4294967291                    the 32-bit pattern C and Java store
  back to signed:  u - (1 << 32) if u >> 31 else u      (bit 31 set means negative)
```

Two problems need exactly that. Single Number II (137) has every value three times except one, `[-2, -2, 1, 1, 4, 1, 4, 4, -4, -2]` gives -4: count the 1s in each of the 32 bit columns modulo 3, and the columns left over spell the loner's pattern. Sum of Two Integers (371) adds without `+`: `a ^ b` is the sum without carries, `(a & b) << 1` is the carries, and the loop repeats until no carry is left, all inside 32 bits.

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

A greedy can read the low bits too. When the moves are "halve" and "add or subtract 1", halving only drops the last bit, so the cost of reaching 1 lies in clearing 1-bits.

Integer Replacement asks for the fewest steps from n to 1, where an even n is halved and an odd n becomes n + 1 or n − 1: 7 takes 4 steps, 7 → 8 → 4 → 2 → 1. For an odd n the last two bits decide. Ending in `01`, subtract: that leaves `00` and two free halvings. Ending in `11`, add: the carry wipes out the whole run of 1s at once. The single exception is 3, where 3 → 2 → 1 beats 3 → 4 → 2 → 1.

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

The capstone keeps every operation O(1) for a big universe by cutting the bits into fixed-size words. Bit `i` lives in word `i >> 6`, which is `i // 64`, at position `i & 63`, which is `i % 64`. Set, clear and get touch one word. Counting is a popcount per word, and "the next member from `i` on" skips empty words 64 values at a time, then reads the lowest 1 with `x & -x`.

```text
          word 2                 word 1            word 0
  [ 191 ... 130 129 128 ]  [ 127 ... 65 64 ]  [ 63 ... 2 1 0 ]
            ^
            i = 130: word 130 >> 6 = 2, position 130 & 63 = 2        (bytes: byte i >> 3, bit i & 7)
```

`Bits(200)` holds a set of integers in [0, 200) in four words. After setting 3, 64, 130 and 199 it counts 4 members; `next_set(4)` skips the rest of word 0 and finds 64, `next_set(131)` finds 199, and `next_set(200)` is −1, because no member is 200 or more.

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
- Flip every bit at once, `b.words = [~w & (2**64 - 1) for w in b.words]`, and call `b.count()`: 252, not 196. The last word also flipped its 56 padding bits, the values 200..255, which are not in the universe. [Design Problems](#s24) handles "flip everything" lazily, with one flag and a maintained count.
- Time it (`import time` first): put `random.sample(range(10**6), 20_000)` through `Bits.set` and through a plain int (`seen |= 1 << v`), timing each with `time.perf_counter()`. The int is dozens of times slower, because every `|=` copies the whole number.

### Math recipes

The math recipes count instead of listing too. Four of them cover what medium interviews ask: number theory, digits and bases, random sampling and exact slopes.

Euclid's rule is that every common divisor of `a` and `b` also divides `a % b`, so `gcd(a, b) = gcd(b, a % b)`, and the pair shrinks fast; then `lcm(a, b) = a // gcd(a, b) * b`. Trial division stops at √n, because divisors come in pairs `d · (n / d)` and one of the two is at most √n. The sieve lists the primes up to n by crossing off the multiples of each prime p from `p * p` on; the smaller multiples have a smaller prime factor and are gone already.

Fast power writes the exponent in binary, `3^13 = 3^8 · 3^4 · 3^1`: square the base once per bit and multiply it in when the bit is 1. Reduce after every multiply, because `(a * b) % m == ((a % m) * (b % m)) % m`: reducing early never changes the answer and keeps every number below m², under 2⁶³ for m = 10⁹ + 7, which fixed-width languages need. Python never overflows, but `3 ** 10**6` has 477 122 digits, and multiplying giants is slow.

Python has most of this built in: `math.gcd`, `math.lcm`, `pow(b, e, m)`, `pow(x, -1, m)` for the inverse of x modulo m, `math.isqrt` and `math.comb`. Write each one once by hand so that you can explain it: gcd(252, 105) is 21, ten primes lie below 30, and 3¹³ mod 1000 is 323.

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

Digits come next. `n % 10` is the last digit and `n // 10` drops it, so digits come out lowest first, and `rev * 10 + d` pushes a digit onto the right end of `rev`. Work on `abs(x)` and put the sign back at the end. Every base works the same way with `divmod(n, b)`, and reading digits back is Horner's rule, `n = n * b + d`. Excel columns are base 26 with digits 1..26 and *no zero*, so shift each digit down by one before the divmod.

Reverse Integer asks for the digits of a 32-bit integer in reverse order, or 0 when the result leaves 32 bits: −123 gives −321, and 1534236469 gives 0. A 32-bit language cannot compute `rev * 10 + d` and look afterwards, so test *before* pushing, `rev > (LIMIT - d) // 10`. One limit, 2³¹ − 1, serves both signs: −2³¹ could only come from reversing 8463847412, which is not a 32-bit input.

Palindrome Number asks whether an integer reads the same backwards, without turning it into a string: 12321 does, 10 does not. Reverse only the lower half of the digits and compare it with the upper half. Excel Sheet Column Title turns a column number into its letters, 28 into `AB`, and `column_number` goes back, `ZY` to 701.

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

The third recipe is random sampling. Reservoir sampling picks k items uniformly from a stream too long to store: keep the first k, and after that item i, counting from 0, replaces a random member with probability k/(i+1). With k = 1 it is the random pick behind Linked List Random Node, a uniformly random node of a list of unknown length, and Random Pick Index, a random index among the copies of a target value.

Why that is uniform: item i gets in with probability k/(i+1), and each later item j removes it with probability (k/(j+1)) · (1/k) = 1/(j+1), so it survives item j with probability j/(j+1). The product k/(i+1) · (i+1)/(i+2) · ... · (n−1)/n telescopes to k/n. The cell samples 2 of `range(5)` ten thousand times, so each value should be picked about 10 000 · 2/5 = 4000 times.

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

The last recipe is geometry without floats. Max Points on a Line asks for the largest number of the given points that lie on one straight line: `[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]` gives 4. All points on one line through an anchor share a direction `(dx, dy)`. Floats cannot be trusted as keys, but the direction reduced by the gcd, with a fixed sign, is exact and hashable: `(2, 6)` and `(-1, -3)` both become `(1, 3)`, and vertical lines are `(0, 1)` with no division at all.

A copy of the anchor has no direction, since `gcd(0, 0)` is 0, but it lies on every line through the anchor, so the code counts copies separately and adds them to the best line. Each point anchors only the points after it, because a line through an earlier point was already counted from there. Two copies of `[1, 1]` and the point `[2, 2]` make one line of 3.

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

### Where it goes wrong

Most bit bugs come from Python ints having no width, and most math bugs from floats or from numbering that starts at 1.

1. **Operator precedence.** In Python `&`, `|` and `^` bind tighter than `==`, so `x & 1 == 0` works, unlike in C and Java. But `<<` and `>>` bind *looser* than `+` and `-`: `1 << k - 1` is `1 << (k - 1)`, and `x & mask + 1` is `x & (mask + 1)`. Parenthesise every bit expression.
2. **`~x` is negative in Python.** Ints have no fixed width, so `~0b1010 == -11`, not `0b0101`. For a k-bit complement use `x ^ ((1 << k) - 1)`.
3. **Negative numbers never run out of bits.** `-1 >> 1 == -1`, so `while x: x >>= 1` never ends for a negative x, and neither does the `x &= x - 1` loop. Mask first: `x & 0xFFFFFFFF` is the 32-bit pattern, and `to_signed32` turns it back.
4. **Digits of a negative number.** `divmod(-123, 10) == (-13, 7)`, so the last digit comes out as 7; and `divmod(-1, 10) == (-1, 9)`, so `while n:` never ends. Work on `abs(x)` and restore the sign; [Python Toolkit](#s02) has more on `%` and `//` with negatives.
5. **Stopping a fixed-width loop early.** Reverse Bits must run exactly 32 rounds; stopping when `x == 0` loses the leading zeros that should become trailing zeros, so `reverse_bits(1)` comes back as 1 instead of 2147483648.
6. **Zero passes the power-of-two test.** `0 & (0 - 1) == 0`, so write `x > 0 and (x & (x - 1)) == 0`.
7. **Floats for exact questions.** `math.log(243, 3) == 4.999999999999999`, and `int(math.sqrt(100000001**2 - 1))` is 100000001 while `math.isqrt` gives the true 100000000. Use integers: reduced `(dx, dy)` pairs, cross products, `math.isqrt`, repeated multiplication instead of logs.
8. **Reducing mod at the wrong moment.** Reduce after every multiply (`ans = ans * x % MOD`), but never before comparing: with `a = 10**9 + 8` and `b = 5`, `max(a % MOD, b % MOD)` picks `b`.
9. **Off by one in 1-indexed systems.** Excel columns need `n - 1` before the divmod, or `column_title(26)` gives `"BA"`; the k-th permutation needs the rank `k - 1`; and "primes less than n" is not "primes up to n".
10. **Testing after adding.** In the bit-array template, test bit v *before* you set it, or every value looks like a repeat: `[1, 2, 2, 4]` answers `[4, 3]`.
11. **Duplicate points.** `slope_key(0, 0)` divides by `gcd(0, 0) == 0`: count copies of the anchor separately.

### Edge cases to say out loud

Say these before coding, because each one lands on a guard above. 0 and 1 (no set bits, `is_prime(1)`) · negative numbers (infinite sign bits in Python) · the 32-bit limits (2³¹ − 1 and −2³¹) · the missing value is 0 or n · duplicate points and vertical lines · `mod = 1` · an empty input.

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
assert max_points([[1, 0], [1, 5], [1, -3], [2, 2]]) == 3  # a vertical line
print("edge cases pass")
```

**Try it**
- Run `all(column_number(column_title(n)) == n for n in range(1, 1000))`: True. Two inverse functions test each other.
- What should `missing_number([])` return? Write the assert before running it (0: the range 0..0 lost its only value).
- Predict `find_error_nums([1, 2, 3, 3])` before running: `[3, 4]`, where the missing value is n itself, the top bit of `full`. Build `full` as `(1 << n) - 2` instead and that bit is lost: the answer becomes `[3, -1]`.

### Variations

The bit-array template is the root of a family: change what a bit means, or how masks are compared. The table says what changes and what each problem asks; most of the code is in the bit toolbox above, and the cell after the table works out the bit-column count.

| Variation | What changes from the template | Problems |
|---|---|---|
| **Parity set** | toggle instead of set (`^=`): bit d means "d has been seen an odd number of times" | 1371 Find the Longest Substring Containing Vowels in Even Counts: the longest substring with every vowel an even number of times, in [Prefix Sums](#s04) |
| **Prefix masks + hash map** | a substring's mask is the XOR of two prefix masks; a `Counter` of masks counts the substrings | 1915 Number of Wonderful Substrings: how many substrings have at most one letter an odd number of times |
| **Letter sets** | a word becomes a 26-bit mask; two words share no letter exactly when `(a & b) == 0` | 318 Maximum Product of Word Lengths: the largest `len(a) * len(b)` over two words with no letter in common |
| **All subsets of n items** | `for mask in range(1 << n)`: bit i says whether item i is in | 78 Subsets: every subset of a list of distinct numbers |
| **Maximum XOR** | a binary trie of the numbers; from the top bit down, take the opposite bit whenever it exists | 421 Maximum XOR of Two Numbers in an Array: the largest `a ^ b` over all pairs |
| **XOR as parity** | pairs cancel: the single number, the missing number, two singles | 136 Single Number, 268 Missing Number, 260 Single Number III: the two values that appear once |
| **Count each bit column** | `% 3` per column for "three times" (137); `ones * (n - ones)` differing pairs per column (477) | 137 Single Number II; 477 Total Hamming Distance: the bit differences summed over all pairs, worked out below |
| **32-bit arithmetic** | mask with `0xFFFFFFFF`, convert back through bit 31 | 371 Sum of Two Integers, 190 Reverse Bits |
| **AND of a whole range** | the answer is the common binary prefix of the two ends: `while right > left: right &= right - 1` | 201 Bitwise AND of Numbers Range: the AND of every integer from `left` to `right` |
| **Gray code** | `i ^ (i >> 1)`: neighbours differ in exactly one bit | 89 Gray Code: all n-bit numbers in an order where neighbours differ in one bit |
| **Rolling bit code** | 2 bits per DNA letter, keep the last 20 bits with `& 0xFFFFF` | 187 Repeated DNA Sequences: every 10-letter stretch that occurs more than once |
| **Big universe** | a bytearray or 64-bit words | (no repo problem) |
| **Global flip** | a lazy flag and a maintained count, in [Design Problems](#s24) | 2166 Design Bitset: fix, unfix, flip all and count, each in O(1) |
| **Long division** | a remainder seen before starts the repeating part; handle the sign with `abs` | 166 Fraction to Recurring Decimal: a fraction as a decimal string, the repeating part in parentheses |
| **Simulate one cycle** | after one pass of the moves, bounded iff back at the origin or not facing north | 1041 Robot Bounded In Circle: does a robot that repeats its moves forever stay inside a circle |
| *Second pass:* **Letter subsets** | flip the loop: walk the puzzle's 2⁷ submasks with `sub = (sub - 1) & mask` | 1178 Number of Valid Words for Each Puzzle: for each puzzle, how many words use only its letters and include its first letter |
| *Second pass:* **One odd digit** | earliest index of each prefix mask; look up the mask and its 10 one-bit neighbours | 1542 Find Longest Awesome Substring: the longest substring that can be rearranged into a palindrome |
| *Second pass:* **Maximum XOR with a limit** | sort the queries by limit and grow the binary trie offline | 1707 Maximum XOR With an Element From Array: the best `x ^ y` with y at most a per-query limit |
| *Second pass:* **Turns and corners** | the cross product's sign; toggled corners plus an area check | 587 Erect the Fence: the trees on the convex hull; 391 Perfect Rectangle: do rectangles tile a rectangle exactly |
| *Second pass:* **Count whole blocks** | a digit column, a subtree of prefixes, a block of (n−1)! permutations | 233 Number of Digit One: the 1s written in 1..n; 440 K-th Smallest in Lexicographical Order: the k-th of 1..n in dictionary order; 60 Permutation Sequence: the k-th ordering of 1..n |
| *Second pass:* **Outcomes, not tests** | a pig has T + 1 outcomes, so p pigs tell (T + 1)^p buckets apart | 458 Poor Pigs: the fewest pigs that find the one poisoned bucket |

Total Hamming Distance (477) asks for the number of differing bits summed over all pairs: `[4, 14, 2]` gives 6. The total is a sum over bit columns, and in a column with `ones` ones and `n - ones` zeros exactly `ones * (n - ones)` pairs differ. That is 32 passes instead of n² pairs.

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
- Change `range(32)` to `range(3)`: the answer drops to 4. Bit 3 is never looked at, so its two differences, 14 against 4 and 14 against 2, are lost.

The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them until the main path is automatic.

Number of Valid Words for Each Puzzle (1178) asks, for each 7-letter puzzle, how many words are valid for it: every letter of the word is in the puzzle, and the word contains the puzzle's first letter. Words with the same letter *set* are interchangeable, so a `Counter` holds each word's mask once. Then flip the loop: a puzzle has only 2⁷ = 128 letter subsets, so look each one up instead of testing every word. The walk over the subsets of a mask is one line, `sub = (sub - 1) & mask`:

```text
  mask      1 0 1 1      the allowed positions (the puzzle's letters)
  sub       1 0 0 0
  sub - 1   0 1 1 1      the borrow: the lowest 1 becomes 0, everything below it becomes 1
  & mask    0 0 1 1      drop the forbidden positions: the next smaller subset of mask
  the walk: 1011, 1010, 1001, 1000, 0011, 0010, 0001, 0000   (counting down on mask's own bits)
```

The cell prints that walk for `0b1011`, then counts the valid words for six puzzles. For `"actresz"` four words fit: `"aaaa"`, `"asas"`, `"actt"` and `"access"`. `"gaswxyz"` gets none, because no word contains its first letter, g.

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


print([bin(s) for s in submasks(0b1011)])   # ['0b1011', '0b1010', '0b1001', '0b1000', '0b11', '0b10', '0b1', '0b0']
print(valid_word_counts(["aaaa", "asas", "able", "ability", "actt", "actor", "access"],
                        ["aboveyz", "abrodyz", "abslute", "absoryz", "actresz", "gaswxyz"]))   # [1, 1, 3, 2, 4, 0]
```

**Try it**
- Replace `(sub - 1) & mask` with `sub - 1` and comment out the puzzle line before rerunning, because a puzzle with a `z` would now count down through tens of millions of numbers. The first line shows why: all 12 numbers from 11 down to 0, including ones like `0b100` that are not subsets.
- Move the `if sub == 0: return` check above the `yield`: the empty set 0 is never produced (7 values instead of 8).
- Drop the `if s & first` filter: the last puzzle, `"gaswxyz"`, answers 2 instead of 0, because `"aaaa"` and `"asas"` fit its letters but lack its first letter `g`.

Find Longest Awesome Substring (1542) asks for the longest substring of digits that can be rearranged into a palindrome: `"3242415"` gives 5, since `"24241"` rearranges into `"24142"`. It is the parity mask of [Prefix Sums](#s04) with 10 bits, one per digit: keep the earliest index of each prefix mask, and at each end make 11 lookups, the same mask for all counts even and the 10 masks one bit away for one odd digit.

Maximum XOR With an Element From Array (1707) asks, for each query `(x, m)`, for the largest `x ^ y` over the numbers y ≤ m, or −1 if there is none: with the numbers 0..4, `(5, 6)` gives `5 ^ 2 = 7`. Bits are decided from the top, since a 1 at bit 29 outweighs all the lower bits together. So the numbers go into a binary trie, the trie of [Tries](#s12) with children 0 and 1, and a query walks down taking the child opposite to x's bit whenever it exists: 30 steps.

The limit is handled offline, which means answering the queries in an order of your choosing rather than the order given. Sort the queries by m and insert the sorted numbers while they are ≤ m, so the trie holds exactly the allowed numbers when each query is answered, and write every answer back to its query's original position. Answered in input order, a query would see the numbers above its limit that an earlier query inserted.

Erect the Fence (587) asks which trees stand on the convex hull, the tightest fence around them all, counting trees on a straight stretch: of `[[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]]` all but (2, 2) do. Walk the sorted trees left to right with the lower fence on a stack, popping the last post while the path through it turns right, then walk back for the upper fence. Pop only on `cross < 0`: popping when straight deletes the trees on a straight stretch.

```text
   cross(o, a, b) = (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

   cross(o, a, b) > 0       cross(o, a, b) < 0       cross(o, a, b) == 0
           b                  o ---- a                 o ---- a ---- b
           |                         |
     o --- a                         b
       left turn               right turn              straight
```

Perfect Rectangle (391) asks whether some axis-aligned rectangles tile one big rectangle with no gap and no overlap. They do exactly when their areas add up to the bounding box's area and toggling every tile's four corners in a set leaves only the box's four corners: every inner corner belongs to 2 or 4 tiles and switches back off. Both tests are needed: in `[[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 2, 2]]` the two copies of the small square cancel each other's corners, and only the area test sees the overlap.

```text
   X--------+-----X         A, B, C, D tile the box: every "+" is a corner of exactly 2 tiles,
   |   A    |  B  |         so toggling all corners switches every "+" back off and leaves
   +----+---+-----+         exactly the four X corners on
   |  C |    D    |
   X----+---------X
```

Number of Digit One (233) counts the 1s written in all the numbers from 1 to n: up to 13 there are 6, in 1, 10, 11 twice, 12 and 13. Count per column instead: in the column worth p the digit cycles through 0..9, holding each value for p numbers. Split n into `high`, `cur` and `low`, the digits above, at and below the column. Each of the `high` full cycles shows a 1 for p numbers, and the last cycle adds p if `cur > 1`, `low + 1` if `cur == 1`, else nothing.

```text
  n = 2315, tens column (p = 10): high = 23, cur = 1, low = 5
  0000..2299: 23 full cycles, each with ten numbers showing a 1 in the tens column -> 23 * 10 = 230
  2300..2315: we are inside the 1-run (cur = 1): 2310..2315                         -> low + 1 = 6
```

K-th Smallest in Lexicographical Order (440) asks for the k-th number of 1..n in dictionary order: for n = 13, k = 2 gives 10 and k = 6 gives 2. That order is a pre-order walk of the 10-ary tree whose node v has the children 10v..10v+9, drawn below. Standing on a node, count its subtree level by level, clipped to n. If the k-th number lies past that whole subtree, jump to the next sibling in one step; otherwise step down to the first child.

```text
  n = 13:     1          2   3   4   5   6   7   8   9         pre-order: 1, 10, 11, 12, 13, 2, ..., 9
           /  |  \  \
         10  11  12  13                                         subtree of 1 = {1} + {10..13} = 5 numbers
```

Permutation Sequence (60) asks for the k-th of the n! orderings of 1..n in lexicographic order: n = 3, k = 3 gives `"213"`. The orderings come in n blocks of (n−1)!, one per first digit, so the 0-based rank divided by (n−1)! picks the first digit from the unused ones, and the remainder is the rank inside that block; repeat with (n−2)!. That is the rank written in the factorial number system. The rank is `k - 1`: starting from k itself, `(3, 3)` gives `"231"`, the 4th ordering.

```text
  n = 4, k = 9 -> rank r = 8 = 1·3! + 1·2! + 0·1! + 0·0!
  unused [1 2 3 4] take index 1 -> 2;  [1 3 4] take index 1 -> 3;  [1 4] take index 0 -> 1;  [4] -> 4:  "2314"
```

Poor Pigs (458) asks for the fewest pigs that find the poisoned bucket when a pig dies `minutesToDie` after drinking and the test lasts `minutesToTest`: 4 buckets and one round need 2 pigs. Over T rounds a pig has T + 1 outcomes, death in one round or survival, so p pigs tell apart (T + 1)^p buckets. Label the buckets with p digits in base T + 1, and pig i drinks, in round r, every bucket whose i-th digit is r. So 1000 buckets and 4 rounds need 5 pigs: 5⁵ ≥ 1000 > 5⁴.

```text
  4 buckets, 1 round: a pig ends dead or alive, so 2 pigs tell apart 2 x 2 = 4 buckets
  bucket   label (A, B)      A drinks every bucket whose A-digit is 1: buckets 2 and 3
     0         0 0           B drinks every bucket whose B-digit is 1: buckets 1 and 3
     1         0 1
     2         1 0           A dies, B lives -> label 1 0 -> bucket 2 is the poisoned one
     3         1 1
```

### Say it in the interview

> "I need to remember which of 1..n I've seen, so I keep one bit per value. I test the bit before setting it; a bit already set means this value is the duplicate. At the end, the one bit of 1..n still 0 is the missing value. The brute force rescans for each value, O(n²). With a fixed-size bit array, a bytearray or 64-bit words, test and set touch one word, so it's O(n) time and n bits; a single Python int works too, but every `|=` copies it. If you want O(1) extra space, I'd mark value v by negating `nums[v - 1]`."

Point at the line that tests *before* it sets, and say what a bit means out loud: "bit v of `seen` means v appeared". The negation trick is in [Arrays & Hashing](#s03). For the math tools, name the constraint that rules out listing, such as n up to 10⁹, then the unit you count instead: a bit of the exponent, a digit column, a subtree, a block of (n−1)!.

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
<details><summary>Answer</summary>Python's <code>&gt;&gt;</code> keeps the sign: -8 becomes -4, -2, -1, and <code>-1 &gt;&gt; 1</code> is -1 again, so x never reaches 0. Work on the 32-bit pattern: <code>x &amp;= 0xFFFFFFFF</code> first, then the same <code>while x: x &gt;&gt;= 1</code> ends after at most 32 shifts. Looping exactly 32 times works too.</details>

4. In Maximum XOR With an Element From Array, why sort the queries by their limit?
<details><summary>Answer</summary>Each query may only use numbers ≤ its limit. In increasing limit order the allowed sets only grow, so a single trie that we keep inserting into (never deleting from) holds exactly the allowed numbers when each query is answered. The answers are written back to the queries' original positions.</details>
