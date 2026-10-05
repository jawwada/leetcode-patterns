"""
Integer to English Words (LeetCode 273) - Hard
Chapter: strings
Pattern: Chunk by thousands + lookup tables

Convert a non-negative integer below 2^31 to English words.
Example: 12345 -> "Twelve Thousand Three Hundred Forty Five"; 1000010 -> "One Million Ten";
0 -> "Zero".
"""


# --- helpers ---
ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
        "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion"]


# --- brute force ---
def spell_all_chunks():
    """Spell every number 0..999 up front: a table of 1000 strings."""
    table = [""] * 1000
    for h in range(10):
        for t in range(10):
            for o in range(10):
                parts = []
                if h > 0:
                    parts.append(ONES[h])
                    parts.append("Hundred")
                if t >= 2:
                    parts.append(TENS[t])
                    if o > 0:
                        parts.append(ONES[o])
                elif 10 * t + o > 0:
                    parts.append(ONES[10 * t + o])     # 1..19 are single words
                table[100 * h + 10 * t + o] = " ".join(parts)
    return table


def brute_force(num):
    """Build the whole 0..999 table, then look up each 3-digit group. 1000 strings per call."""
    if num == 0:
        return "Zero"
    table = spell_all_chunks()
    out = []
    for scale in SCALES:                           # lowest group first, so insert at the front
        group = num % 1000
        if group != 0:
            text = table[group]
            if scale != "":
                text = text + " " + scale
            out.insert(0, text)
        num = num // 1000
    return " ".join(out)


# --- optimal ---
def chunk(n):
    """Words for 0 <= n < 1000 with the stencil: hundreds, then tens, then ones."""
    words = []
    if n >= 100:
        words.append(ONES[n // 100])
        words.append("Hundred")
        n = n % 100
    if n >= 20:
        words.append(TENS[n // 10])
        n = n % 10
    if n > 0:
        words.append(ONES[n])                      # 1..19 are single words
    return words


def integer_to_english_words(num):
    """Peel 3 digits at a time; spell the group and add its scale word. O(log num) time."""
    if num == 0:
        return "Zero"
    out = []
    for scale in SCALES:                           # lowest group first
        group = num % 1000
        if group != 0:
            words = chunk(group)
            if scale != "":
                words.append(scale)
            out = words + out                      # a higher group goes in front of the lower ones
        num = num // 1000
    return " ".join(out)


# --- try the brute force ---
print(brute_force(123))                            # -> One Hundred Twenty Three
print(brute_force(12345))                          # -> Twelve Thousand Three Hundred Forty Five
print(brute_force(1000010))                        # -> One Million Ten
print(brute_force(0))                              # -> Zero


# --- try the optimal ---
print(integer_to_english_words(123))               # -> One Hundred Twenty Three
print(integer_to_english_words(12345))             # -> Twelve Thousand Three Hundred Forty Five
print(integer_to_english_words(1000010))           # -> One Million Ten
print(integer_to_english_words(0))                 # -> Zero
