"""
Decode String - One Stack Frame per Bracket

Decode a string in which k[text] means text repeated k times; groups may nest,
k is a positive integer that may have several digits, and digits appear only
as repeat counts: "3[a2[c]]" -> "accaccacc".
"""


# --- algorithm ---
def decode_string(s):
    """On '[' park (text before it, count); on ']' pop and repeat the group.
    One scan; each ']' builds a string no longer than the output."""
    stack = []                  # frames: (text before the '[', its count)
    current = ""                # decoded text of the innermost open level
    count = 0                   # the repeat count being read
    for ch in s:
        if ch.isdigit():
            count = count * 10 + int(ch)        # counts can have several digits
        elif ch == "[":
            stack.append((current, count))      # park the outer level
            current = ""                        # the inner level starts empty
            count = 0
        elif ch == "]":
            before, repeat = stack.pop()
            current = before + current * repeat     # resume the outer level
        else:
            current += ch
    return current


# --- try it ---
print(decode_string("3[a2[c]]"))           # -> accaccacc
print(decode_string("3[a]2[bc]"))          # -> aaabcbc
print(decode_string("2[abc]3[cd]ef"))      # -> abcabccdcdcdef
print(decode_string("12[x]"))              # -> xxxxxxxxxxxx
print(decode_string("leet"))               # -> leet
