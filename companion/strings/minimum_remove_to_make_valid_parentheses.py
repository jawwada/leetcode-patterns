"""
Minimum Remove to Make Valid Parentheses (LeetCode 1249) - Medium
Chapter: strings
Pattern: Stack matching

Given a string of lowercase letters and parentheses, remove the minimum number of parentheses
so the result is valid, and return any such result.
Example: "lee(t(c)o)de)" -> "lee(t(c)o)de"; "a)b(c)d" -> "ab(c)d"; "))((" -> "".
"""


# --- brute force ---
def drop_unmatched(s, opener, closer):
    """Delete the first closer that has no opener before it, rescan from the start, repeat."""
    changed = True
    while changed:
        changed = False
        depth = 0
        for i in range(len(s)):
            if s[i] == opener:
                depth += 1
            elif s[i] == closer:
                depth -= 1
            if depth < 0:                 # this closer has no partner: delete it and restart
                s = s[:i] + s[i + 1:]
                changed = True
                break
    return s


def brute_force(s):
    """Remove unmatched ')' left to right, then unmatched '(' right to left. O(n^2), O(n) space."""
    s = drop_unmatched(s, "(", ")")
    reversed_s = s[::-1]                  # read backwards, ')' opens and '(' closes
    reversed_s = drop_unmatched(reversed_s, ")", "(")
    return reversed_s[::-1]


# --- optimal ---
def min_remove_to_make_valid(s):
    """Stack of open '(' indices; unmatched ')' and never-closed '(' are blanked. O(n), O(n)."""
    chars = list(s)
    stack = []                            # indices of '(' not yet closed
    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        elif s[i] == ")":
            if len(stack) > 0:
                stack.pop()               # pair it with the most recent open '('
            else:
                chars[i] = ""             # unmatched ')': delete
    for i in stack:
        chars[i] = ""                     # '(' never closed: delete
    return "".join(chars)


# --- try the brute force ---
print(brute_force("lee(t(c)o)de)"))                # -> lee(t(c)o)de
print(brute_force("a)b(c)d"))                      # -> ab(c)d
print(brute_force("))(("))                         # -> (empty line)
print(brute_force("(a(b(c)d)"))                    # -> a(b(c)d)


# --- try the optimal ---
print(min_remove_to_make_valid("lee(t(c)o)de)"))   # -> lee(t(c)o)de
print(min_remove_to_make_valid("a)b(c)d"))         # -> ab(c)d
print(min_remove_to_make_valid("))(("))            # -> (empty line)
print(min_remove_to_make_valid("(a(b(c)d)"))       # -> a(b(c)d)
