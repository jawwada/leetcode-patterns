"""
Encode and Decode Strings - Fundamentals
Chapter: fundamentals/strings
Key operations: length-prefix each string, collect parts in a list, join once, read length, slice

Encode a list of strings into one string and decode it back (LeetCode 271); the strings may contain
any character, including the delimiter. Each part is written as "<length>#<string>", so the decoder
reads a number, skips the '#', and slices exactly that many characters. Building the output with
a list and one join copies every character once; += in a loop recopies the accumulator each step.
Example: ["lint", "code", "love", "you"] -> "4#lint4#code4#love3#you" -> back to the four strings
"""


# --- algorithm ---
def encode(strs):
    """Length-prefix each string, collect the parts in a list, join once. O(total length)."""
    parts = []
    for s in strs:
        parts.append(str(len(s)) + "#" + s)
    return "".join(parts)             # one join copies each char once; += in a loop is quadratic


def decode(s):
    """Read the length up to '#', slice exactly that many characters, jump past them. O(n)."""
    out = []
    i = 0
    while i < len(s):
        j = s.index("#", i)           # the first '#' after i ends the length field
        length = int(s[i:j])
        start = j + 1
        out.append(s[start:start + length])
        i = start + length            # the next part begins right after the payload
    return out


# --- try it ---
print(encode(["lint", "code", "love", "you"]))     # -> 4#lint4#code4#love3#you
print(decode("4#lint4#code4#love3#you"))           # -> ['lint', 'code', 'love', 'you']
print(encode(["a#b", "", "c"]))                    # -> 3#a#b0#1#c
print(decode("3#a#b0#1#c"))                        # -> ['a#b', '', 'c']
