"""
Encode and Decode Strings (LeetCode 271)  — Medium
Pattern: Length-prefixed serialization

Problem
-------
Design encode(list of strings) -> one string and decode(string) -> the original list,
so that decode(encode(strs)) == strs for ANY strings, including empty strings and
strings containing any character (commas, '#', digits, etc.).
Example: ["lint", "code", "love", "you"] -> "4#lint4#code4#love3#you" -> back to the list.

Brute force
-----------
Join with a delimiter such as ',' and split on it. That breaks as soon as a string
contains ','. The obvious fix is escaping: double every backslash and prefix every
delimiter with a backslash, then decode by scanning character by character and
tracking an "escaped" flag. Correct, O(total length) time, but every single
character has to be inspected on both encode and decode just to find the boundaries,
and the output grows unpredictably when the data is full of delimiters.

From brute force to optimal
---------------------------
The character-by-character scan exists only because the decoder does not know where
a string ends. Tell it: write each string's length before it, followed by one
terminator ('#') so the digits of the length are unambiguous. Now decoding never
looks inside a string — it reads digits up to '#', then jumps forward exactly that
many characters. No escaping, no restrictions on content, and the overhead per
string is O(log length) digits. Content-agnostic framing (like TCP or Protobuf
length prefixes) is the invariant that removes the dependence on the alphabet.

Intuition
---------
A delimiter is ambiguous because the payload might contain it. A length is never
ambiguous because the decoder is told how many characters to consume rather than
asked to search for a boundary. The '#' after the length just separates the digits
of the length from a payload that may itself start with a digit.

Geometric view
--------------
The encoded string is a sequence of frames [len]#[payload][len]#[payload]... Decoding
is a pointer that hops: read digits, land on '#', step over it, then leap exactly len
characters to the start of the next frame. The pointer never examines payload bytes.

Steps
-----
1. encode: for each string s, append f"{len(s)}#{s}".
2. decode: i = 0; while i < len(data):
3.   find j = data.index('#', i); length = int(data[i:j]).
4.   append data[j+1 : j+1+length]; set i = j + 1 + length.
5. Return the collected list.

Complexity: O(n) time, O(n) space for both directions — each character is written
and read once; the decoder's jumps skip payloads.
Pitfalls: using a delimiter alone; forgetting the '#' so "12" + "3abc" is ambiguous
with "1" + "23abc"; mishandling empty strings (encode as "0#").
"""
from typing import List


class Codec:
    def encode(self, strs: List[str]) -> str:
        return "".join(f"{len(s)}#{s}" for s in strs)

    def decode(self, s: str) -> List[str]:
        out: List[str] = []
        i = 0
        while i < len(s):
            j = s.index("#", i)          # digits of the length end here
            length = int(s[i:j])
            out.append(s[j + 1:j + 1 + length])
            i = j + 1 + length           # leap over the payload
        return out


class BruteForce:
    """Delimiter with backslash escaping: must inspect every character."""

    def encode(self, strs: List[str]) -> str:
        escaped = [s.replace("\\", "\\\\").replace(",", "\\,") for s in strs]
        return ",".join(escaped) + ("," if strs else "")

    def decode(self, s: str) -> List[str]:
        out, cur, i = [], [], 0
        while i < len(s):
            ch = s[i]
            if ch == "\\":
                cur.append(s[i + 1])
                i += 2
            elif ch == ",":
                out.append("".join(cur))
                cur = []
                i += 1
            else:
                cur.append(ch)
                i += 1
        return out


if __name__ == "__main__":
    codec = Codec()
    cases = [
        ["lint", "code", "love", "you"],
        ["", "a", ""],
        [],
        ["a#1b", "12#", "\\,,", "#"],
    ]
    assert codec.encode(["lint", "code", "love", "you"]) == "4#lint4#code4#love3#you"
    assert codec.decode(codec.encode(["", "a", ""])) == ["", "a", ""]
    assert codec.decode(codec.encode([])) == []
    assert codec.decode(codec.encode(["a#1b", "12#", "\\,,", "#"])) == ["a#1b", "12#", "\\,,", "#"]
    bf = BruteForce()
    for c in cases:
        assert codec.decode(codec.encode(c)) == c == bf.decode(bf.encode(c))
    print("ok")
