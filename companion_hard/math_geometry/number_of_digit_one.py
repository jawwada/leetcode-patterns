"""
Number of Digit One (LeetCode 233) - Hard
Chapter: math_geometry
Pattern: Digit counting by position

Count how many times the digit 1 appears in all integers from 0 to n (n up to 2 * 10^9).
Example: n = 13 -> 6, because 1, 10, 11, 12, 13 contain 1 + 1 + 2 + 1 + 1 ones; n = 0 -> 0.
"""


# --- brute force ---
def brute_force(n):
    """Spell out every number 0..n and count its '1' characters. O(n log n) time, O(1) space."""
    total = 0
    for i in range(n + 1):
        for ch in str(i):
            if ch == "1":
                total += 1
    return total


# --- optimal ---
def number_of_digit_one(n):
    """Count the 1s shown by each digit place, place by place. O(log n) time, O(1) space."""
    total = 0
    place = 1                                      # 1, 10, 100, ...
    while place <= n:
        high = n // (place * 10)                   # the digits above this place
        cur = (n // place) % 10                    # the digit at this place
        low = n % place                            # the digits below this place
        total += high * place                      # each full cycle above: a 1 for `place` numbers
        if cur > 1:
            total += place                         # the partial cycle passed its whole run of 1s
        elif cur == 1:
            total += low + 1                       # inside the run of 1s: ...1000 up to n
        place = place * 10
    return total


# --- try the brute force ---
print(brute_force(13))                             # -> 6
print(brute_force(0))                              # -> 0
print(brute_force(100))                            # -> 21
print(brute_force(1000))                           # -> 301


# --- try the optimal ---
print(number_of_digit_one(13))                     # -> 6
print(number_of_digit_one(0))                      # -> 0
print(number_of_digit_one(100))                    # -> 21
print(number_of_digit_one(1000))                   # -> 301
