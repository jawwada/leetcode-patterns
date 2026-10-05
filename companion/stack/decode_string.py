"""
Decode String (LeetCode 394) - Medium
Chapter: stack
Pattern: Stack of nested contexts

Decode a string where k[encoded] means encoded repeated k times. Brackets may nest, and
digits appear only as repeat counts.
Example: "3[a]2[bc]" -> "aaabcbc"; "3[a2[c]]" -> "accaccacc".
"""


# --- brute force ---
def brute_force(s):
    """Expand the first innermost k[...] group, rebuild the string, repeat. O(n * output) time."""
    while "[" in s:                                 # one innermost group per pass
        close_at = s.index("]")                     # the first ']' closes an innermost group
        open_at = s.rindex("[", 0, close_at)        # the last '[' before it
        start = open_at
        while start > 0 and s[start - 1].isdigit():
            start -= 1                              # walk back over the digits of k
        k = int(s[start:open_at])
        inner = s[open_at + 1:close_at]
        s = s[:start] + inner * k + s[close_at + 1:]      # rebuilds the whole string
    return s


# --- optimal ---
def decode_string(s):
    """On '[' park (text so far, count); on ']' pop and repeat. O(output) time, O(depth) space."""
    stack = []                  # frames: [text before the '[', repeat count]
    current = ""
    num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)                # counts can have several digits
        elif ch == "[":
            stack.append([current, num])            # park the outer text and its count
            current = ""
            num = 0
        elif ch == "]":
            frame = stack.pop()
            current = frame[0] + current * frame[1]   # resume the outer text
        else:
            current += ch
    return current


# --- try the brute force ---
print(brute_force("3[a]2[bc]"))       # -> aaabcbc
print(brute_force("3[a2[c]]"))        # -> accaccacc
print(brute_force("2[abc]3[cd]ef"))   # -> abcabccdcdcdef
print(brute_force("2[3[a]b]"))        # -> aaabaaab


# --- try the optimal ---
print(decode_string("3[a]2[bc]"))       # -> aaabcbc
print(decode_string("3[a2[c]]"))        # -> accaccacc
print(decode_string("2[abc]3[cd]ef"))   # -> abcabccdcdcdef
print(decode_string("2[3[a]b]"))        # -> aaabaaab
