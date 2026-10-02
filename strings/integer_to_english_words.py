"""
Integer to English Words (LeetCode 273)  — Hard
Pattern: Chunk by thousands + fixed lookup tables

Problem
-------
Convert a non-negative integer (< 2^31) to its English words.
Example: 1234567 -> "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven",
12345 -> "Twelve Thousand Three Hundred Forty Five", 0 -> "Zero".

Brute force
-----------
Spell every number from 0 to 999 up front with a triple loop over hundreds / tens / ones digits
(1000 strings), then peel the input into 3-digit chunks and look each one up in that table.
Correct, but every call builds and throws away 1000 strings to use at most four of them, and the
table-building loop still has to encode the teens/tens irregularity, so nothing is saved.
O(1000 + log10 n) time, O(1000) space per call; the wasted work is spelling 996 chunks that the
input never asks for.

From brute force to optimal
---------------------------
The redundancy is pre-spelling chunks we never read. Observation: English is already a
positional system in base 1000: a number is a sequence of 3-digit groups, each read the same way
("X Hundred Y Z") followed by a scale word (Thousand, Million, Billion). Inside a group the only
irregularity is 1..19 having their own names and 20..90 having their own tens names. So one
function chunk(n) for 0 <= n < 1000 plus two short tables covers everything; apply it on
demand to num % 1000 while dividing by 1000, and prepend the scale word. The data structure is
nothing more than three lists and a loop, O(log n) work.

Intuition
---------
Divide and conquer by place value: split on 1000, not 10. A 3-digit chunk is read as
hundreds-digit + "Hundred", then either a teen word (n < 20) or tens-word + ones-word. Zero
chunks produce nothing (and no scale word): 1000010 -> "One Million Ten", not
"One Million Zero Thousand Ten". Build low chunks first and prepend, so the loop never needs to
know how many groups there are.

Geometric view
--------------
Write the number right-aligned in columns of width 3: |  1|234|567|. Each column is a cell that
gets a label from the same stencil; the column position chooses the suffix Million / Thousand /
"" . Empty (000) cells are skipped entirely. Read the cells left to right.

Steps
-----
1. If num == 0 return "Zero".
2. chunk(n): words = []; if n >= 100 add ONES[n//100], "Hundred", n %= 100; if n >= 20 add
   TENS[n//10], n %= 10; if n add ONES[n].
3. out = []; for scale in ["", "Thousand", "Million", "Billion"]: if num % 1000 != 0,
   out = chunk(num % 1000) + [scale if scale] + out; num //= 1000.
4. Return " ".join(out).

Complexity: O(log n) time, O(1) space — at most four 3-digit chunks, constant tables.
Pitfalls: emitting "Zero" or a scale word for an empty chunk; "Forty" not "Fourty"; teens
(10..19) must be looked up as a whole, not as tens + ones; stray double spaces from joining
empty strings.
"""
from typing import List


class Solution:
    ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
            "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
            "Eighteen", "Nineteen"]
    TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    SCALES = ["", "Thousand", "Million", "Billion"]

    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        def chunk(n: int) -> List[str]:               # words for 0 <= n < 1000
            words = []
            if n >= 100:
                words += [self.ONES[n // 100], "Hundred"]
                n %= 100
            if n >= 20:
                words.append(self.TENS[n // 10])
                n %= 10
            if n:                                     # 1..19 (teens are one word)
                words.append(self.ONES[n])
            return words

        out = []
        for scale in self.SCALES:                     # peel 3 digits at a time, low to high
            if num % 1000:
                out = chunk(num % 1000) + ([scale] if scale else []) + out
            num //= 1000
        return " ".join(out)


def brute_force(num: int) -> str:
    if num == 0:
        return "Zero"
    ones, tens = Solution.ONES, Solution.TENS
    table = [""] * 1000                               # spell every chunk 0..999 up front
    for h in range(10):
        for t in range(10):
            for o in range(10):
                parts = [ones[h], "Hundred"] if h else []
                if t >= 2:
                    parts += [tens[t]] + ([ones[o]] if o else [])
                elif 10 * t + o:
                    parts.append(ones[10 * t + o])
                table[100 * h + 10 * t + o] = " ".join(parts)
    out = []
    for scale in Solution.SCALES:
        if num % 1000:
            out.insert(0, (table[num % 1000] + " " + scale).strip())
        num //= 1000
    return " ".join(out)


if __name__ == "__main__":
    s = Solution()
    assert s.numberToWords(123) == "One Hundred Twenty Three"
    assert s.numberToWords(12345) == "Twelve Thousand Three Hundred Forty Five"
    assert s.numberToWords(1234567) == ("One Million Two Hundred Thirty Four Thousand "
                                         "Five Hundred Sixty Seven")
    assert s.numberToWords(0) == "Zero"
    assert s.numberToWords(1000000) == "One Million"
    assert s.numberToWords(1000010) == "One Million Ten"
    assert s.numberToWords(2147483647) == ("Two Billion One Hundred Forty Seven Million "
                                            "Four Hundred Eighty Three Thousand Six Hundred "
                                            "Forty Seven")
    import random
    random.seed(0)
    for n in [0, 1, 10, 19, 20, 99, 100, 101, 110, 1000, 1001, 100000, 2147483647] + \
            [random.randint(0, 2 ** 31 - 1) for _ in range(300)]:
        assert s.numberToWords(n) == brute_force(n), n
    print("ok")
