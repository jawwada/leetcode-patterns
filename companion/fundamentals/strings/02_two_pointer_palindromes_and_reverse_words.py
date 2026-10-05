"""
Two Pointer Palindromes and Reverse Words - Fundamentals
Chapter: fundamentals/strings
Key operations: lo/hi pointers skipping non-alphanumerics, compare lowercase, reverse a range

Two drills on a string with two pointers. (1) is_palindrome: ignore everything that is not a
letter or digit and compare case-insensitively. (2) reverse the order of the words in a sentence
of single-space separated words in place: reverse the whole char list, then reverse each word back.
Example: "A man, a plan, a canal: Panama" -> True; "the sky is blue" -> "blue is sky the"
"""


# --- algorithm ---
def is_palindrome(s):
    """Two pointers from both ends; skip non-alphanumerics; compare lowercase. O(n), O(1) space."""
    lo = 0
    hi = len(s) - 1
    while lo < hi:
        if not s[lo].isalnum():
            lo += 1
        elif not s[hi].isalnum():
            hi -= 1
        else:
            if s[lo].lower() != s[hi].lower():    # compare case-insensitively
                return False
            lo += 1
            hi -= 1
    return True


def reverse_range(chars, lo, hi):
    """Swap inward until the pointers cross. O(hi - lo)."""
    while lo < hi:
        chars[lo], chars[hi] = chars[hi], chars[lo]
        lo += 1
        hi -= 1


def reverse_words(s):
    """Reverse the whole list, then reverse each word back into reading order. O(n), O(1) extra."""
    chars = list(s)
    reverse_range(chars, 0, len(chars) - 1)
    start = 0
    for i in range(len(chars) + 1):               # i == len(chars) closes the last word
        if i == len(chars) or chars[i] == " ":
            reverse_range(chars, start, i - 1)    # the word ends just before the space at i
            start = i + 1
    return "".join(chars)


# --- try it ---
print(is_palindrome("A man, a plan, a canal: Panama"))   # -> True
print(is_palindrome("race a car"))                       # -> False
print(is_palindrome(" "))                                # -> True
print(reverse_words("the sky is blue"))                  # -> blue is sky the
print(reverse_words("hello"))                            # -> hello
