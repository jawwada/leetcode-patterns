"""
Encode and Decode Strings - Length-Prefix Framing

Pack a list of strings into one string and unpack it back to the same list;
the strings may contain any character, '#' and digits included:
["ab#", "12", ""] -> "3#ab#2#120#" -> ["ab#", "12", ""].
"""


# --- algorithm ---
def encode(strs):
    """Prefix each string with its length and a '#'. O(total length)."""
    parts = []
    for s in strs:
        parts.append(str(len(s)) + "#" + s)
    return "".join(parts)               # join once; += in a loop may recopy


def decode(data):
    """Read digits up to '#', then take exactly that many characters.
    O(total length)."""
    strs = []
    i = 0
    while i < len(data):
        j = i
        while data[j] != "#":           # the length ends at the first '#'
            j += 1
        length = int(data[i:j])
        strs.append(data[j + 1:j + 1 + length])
        i = j + 1 + length              # jump over the payload unread
    return strs


# --- try it ---
print(encode(["ab#", "12", ""]))                  # -> 3#ab#2#120#
print(decode("3#ab#2#120#"))                      # -> ['ab#', '12', '']
print(decode(encode(["hello world", "#4#"])))     # -> ['hello world', '#4#']
print(decode(encode([])), decode(encode([""])))   # -> [] ['']
