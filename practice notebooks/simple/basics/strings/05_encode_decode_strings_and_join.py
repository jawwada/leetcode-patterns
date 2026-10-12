"""
Encode and Decode Strings (basics: strings)
Pack a list of strings into one string and unpack it again; the strings may contain any character.
  ["lint", "code", "love", "you"]  ->  "4#lint4#code4#love3#you"  ->  the same list

Idea: write each string as "<length>#<string>". The decoder reads the digits up to the next '#',
      then slices exactly that many chars, so a '#' inside a string can't fool it. Collect the
      parts in a list and join once: += in a loop recopies the whole result every time (O(n^2)).

Pseudocode:
  encode(strs): return "".join(f"{len(s)}#{s}" for s in strs)
  decode(data):
      i = 0
      while i < len(data):
          j = index of the next '#' at or after i
          length = int(data[i:j])
          keep data[j + 1 : j + 1 + length]
          i = j + 1 + length                      # start of the next part

Time O(total length), space O(total length).
"""


def encode(strs):
    parts = []
    for s in strs:
        parts.append(f"{len(s)}#{s}")    # length first, then the raw string
    return "".join(parts)                # one join: each char is copied once


def decode(data):
    out, i = [], 0
    while i < len(data):
        j = data.index("#", i)           # the length ends at this '#'
        length = int(data[i:j])
        out.append(data[j + 1:j + 1 + length])  # exactly length chars
        i = j + 1 + length               # jump to the next part
    return out


if __name__ == "__main__":
    encoded = encode(["lint", "code", "love", "you"])
    print(encoded)                       # 4#lint4#code4#love3#you
    print(decode(encoded))               # ['lint', 'code', 'love', 'you']
    print(decode(encode(["a#b", "", "3#"])))  # ['a#b', '', '3#']
