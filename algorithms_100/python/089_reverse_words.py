"""
Reverse Words in a String - Reverse All, Then Reverse Each Word

Reverse the order of the words in a string. Words are separated by one or more
spaces; the result uses single spaces and has none at either end:
"  the sky   is blue " -> "blue is sky the".
"""


# --- algorithm ---
def reverse_words(s):
    """Squeeze the spaces, reverse the whole array, then reverse each word.
    O(n) time; O(1) extra space on a mutable character array."""
    chars = list(s)                     # Python strings are immutable
    length = squeeze_spaces(chars)      # the words fill chars[0..length-1]
    reverse(chars, 0, length - 1)       # order flipped, letters backwards
    start = 0
    for i in range(length + 1):
        if i == length or chars[i] == " ":  # a word ends just before i
            reverse(chars, start, i - 1)    # spell it forwards again
            start = i + 1
    return "".join(chars[0:length])


def squeeze_spaces(chars):
    """Copy the words to the front, one space between them. O(n)."""
    write = 0
    for read in range(len(chars)):
        if chars[read] != " ":
            chars[write] = chars[read]
            write += 1
        elif write > 0 and chars[write - 1] != " ":
            chars[write] = " "          # keep one space after a word
            write += 1
    if write > 0 and chars[write - 1] == " ":
        write -= 1                      # drop the trailing space
    return write


def reverse(chars, i, j):
    """Reverse chars[i..j] in place, swapping the ends inward. O(j - i)."""
    while i < j:
        chars[i], chars[j] = chars[j], chars[i]
        i += 1
        j -= 1


# --- try it ---
print(reverse_words("  the sky   is blue "))   # -> blue is sky the
print(reverse_words("a good   example"))       # -> example good a
print(reverse_words("hello"))                  # -> hello
print(repr(reverse_words("    ")))             # -> ''
