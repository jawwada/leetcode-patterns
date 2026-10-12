"""
Valid Parentheses - The Matching Stack

Given a string of the brackets ()[]{}, decide whether every opener is closed
by a bracket of the same kind, innermost first:
"([]{})" -> True, "([)]" -> False.
"""


# --- algorithm ---
def is_valid(s):
    """Push openers; every closer must match the top. O(n) time and space."""
    partner = {")": "(", "]": "[", "}": "{"}     # closer -> its opener
    stack = []                                   # openers still waiting
    for ch in s:
        if ch in partner:
            if len(stack) == 0 or stack[-1] != partner[ch]:
                return False                     # nothing open, or wrong kind
            stack.pop()                          # the innermost opener closes
        else:
            stack.append(ch)
    return len(stack) == 0                       # leftovers never closed


# --- try it ---
print(is_valid("([]{})"))       # -> True
print(is_valid("([)]"))         # -> False
print(is_valid("(("))           # -> False
print(is_valid(")("))           # -> False
print(is_valid(""))             # -> True
