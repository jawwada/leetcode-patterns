"""
Valid Palindrome (LeetCode 125) - Easy
Chapter: two_pointers
Pattern: Converging two pointers

A phrase is a palindrome if, after lowercasing and removing every non-alphanumeric
character, it reads the same forwards and backwards. Return True if s is a palindrome.
Example: "A man, a plan, a canal: Panama" -> True ("amanaplanacanalpanama");
         "race a car" -> False.
"""


# --- brute force ---
def brute_force(s):
    """Build the cleaned string and compare it with its reverse. O(n) time, O(n) space."""
    cleaned = ""
    for ch in s:
        if ch.isalnum():  # keep only letters and digits
            cleaned += ch.lower()
    return cleaned == cleaned[::-1]


# --- optimal ---
def is_palindrome(s):
    """Two pointers walk inward, skipping junk as they go. O(n) time, O(1) space."""
    left = 0
    right = len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1  # filter lazily: step over punctuation and spaces on the fly
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# --- try the brute force ---
print(brute_force("A man, a plan, a canal: Panama"))   # -> True
print(brute_force("race a car"))                       # -> False
print(brute_force(".,"))                               # -> True
print(brute_force("0P"))                               # -> False


# --- try the optimal ---
print(is_palindrome("A man, a plan, a canal: Panama"))   # -> True
print(is_palindrome("race a car"))                       # -> False
print(is_palindrome(".,"))                               # -> True
print(is_palindrome("0P"))                               # -> False
