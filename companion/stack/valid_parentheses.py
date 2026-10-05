"""
Valid Parentheses (LeetCode 20) - Easy
Chapter: stack
Pattern: Stack matching

Given a string made of the characters ()[]{}, decide whether it is valid: every opener is
closed by the same type of bracket, and brackets close in nested order.
Example: "()[]{}" -> True; "([)]" -> False; "{[]}" -> True.
"""


# --- brute force ---
def brute_force(s):
    """Delete an adjacent matched pair and start over until stuck. O(n^2) time, O(n) space."""
    changed = True
    while changed:                                  # rescan from the start after each deletion
        changed = False
        for pair in ["()", "[]", "{}"]:
            if pair in s:
                s = s.replace(pair, "", 1)
                changed = True
    return s == ""                                  # valid iff everything cancelled out


# --- optimal ---
def is_valid(s):
    """Push openers; each closer must match the most recent opener. O(n) time, O(n) space."""
    pairs = {")": "(", "]": "[", "}": "{"}         # closer -> the opener it needs
    stack = []
    for ch in s:
        if ch in pairs:
            if len(stack) == 0:
                return False
            top = stack.pop()
            if top != pairs[ch]:                    # the closer must match the innermost opener
                return False
        else:
            stack.append(ch)
    return len(stack) == 0                          # leftover openers mean invalid


# --- try the brute force ---
print(brute_force("()[]{}"))   # -> True
print(brute_force("([)]"))     # -> False
print(brute_force("{[]}"))     # -> True
print(brute_force("(("))       # -> False


# --- try the optimal ---
print(is_valid("()[]{}"))   # -> True
print(is_valid("([)]"))     # -> False
print(is_valid("{[]}"))     # -> True
print(is_valid("(("))       # -> False
