"""
Two Pointer Palindromes and Reverse Words (basics: strings)
Test a palindrome over letters and digits (any case), and reverse a sentence's words in place.
  "A man, a plan, a canal: Panama"  ->  True;    "the sky is blue"  ->  "blue is sky the"

Idea: two pointers start at both ends and step inward. Palindrome: skip anything that is not a
      letter or digit and compare in lowercase. Sentence: reverse the whole char list (the word
      order flips, but each word reads backwards), then reverse every word back.

Pseudocode:
  reverse_range(chars, lo, hi): while lo < hi: swap chars[lo], chars[hi]; lo += 1; hi -= 1

  is_palindrome(s):
      lo, hi = 0, len(s) - 1
      while lo < hi:
          if s[lo] is not a letter or digit: lo += 1
          elif s[hi] is not a letter or digit: hi -= 1
          elif s[lo].lower() != s[hi].lower(): return False
          else: lo += 1; hi -= 1
      return True

  reverse_words(s):
      reverse_range over the whole list         # "eulb si yks eht"
      reverse_range over each word              # "blue is sky the"

Time O(n) each, extra space O(1) (reverse_words swaps inside its own char list).
"""


def reverse_range(chars, lo, hi):
    while lo < hi:                       # swap inward until the pointers meet
        chars[lo], chars[hi] = chars[hi], chars[lo]
        lo += 1
        hi -= 1


def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if not s[lo].isalnum():          # skip junk on the left
            lo += 1
        elif not s[hi].isalnum():        # skip junk on the right
            hi -= 1
        elif s[lo].lower() != s[hi].lower():
            return False
        else:                            # this pair matches: step both inward
            lo += 1
            hi -= 1
    return True


def reverse_words(s):
    chars = list(s)                      # a list can change in place, a str can't
    reverse_range(chars, 0, len(chars) - 1)  # whole sentence: "eulb si yks eht"
    start = 0
    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":  # a word ends at i - 1
            reverse_range(chars, start, i - 1)  # flip that word back
            start = i + 1
    return "".join(chars)


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))  # True
    print(is_palindrome("race a car"))                      # False
    print(reverse_words("the sky is blue"))                 # blue is sky the
