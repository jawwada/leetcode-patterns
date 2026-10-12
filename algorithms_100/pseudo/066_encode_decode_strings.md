---
rank: 66
slug: encode_decode_strings
---

Design `encode`, which packs a list of strings into a single string, and `decode`, which recovers exactly the same list. The strings may contain any character, `#` and digits included. `["ab#", "12", ""]` encodes to `3#ab#2#120#` and decodes back to the same three strings.

The obvious scheme puts a delimiter between the strings and splits on it, and it breaks the moment a string contains the delimiter: joining with `#` turns `["ab#", "12", ""]` into `ab##12#`, which splits back into four strings. It cannot even tell `[]` from `[""]`, since both join to the empty string. Escaping can patch it, at the price of inspecting and rewriting every character on both sides. Framing sidesteps the question. Write each string's length in front of it, then a `#` that ends the length field, then the string itself. The decoder reads digits up to the first `#`, which is unambiguous because a length is made only of digits, and then takes exactly that many characters without looking at them.

Picture the encoded string as a train of boxes, each with a label on its front that says how long the box is. The decoder reads a label, steps over the whole box, and lands on the next label. A `#` or a digit inside a payload is never read as structure, because the decoder jumps over payloads instead of scanning them.

```text
encode   "ab#" → 3#ab#      "12" → 2#12      "" → 0#

data     3 # a b # 2 # 1 2 0 #
index    0 1 2 3 4 5 6 7 8 9 10

i = 0    digits "3", '#' at j = 1    take data[2..4] = "ab#"   next i = 5
i = 5    digits "2", '#' at j = 6    take data[7..8] = "12"    next i = 9
i = 9    digits "0", '#' at j = 10   take nothing      = ""    next i = 11
i = 11 = len(data): stop             → ["ab#", "12", ""]

the '#' at index 4 sits inside a payload: the decoder steps over it unread
```

```pseudo
FUNCTION Encode(strs)
    parts ← empty list
    FOR EACH s IN strs
        parts.append(str(len(s)) + "#" + s)   // length, '#', then s itself
    RETURN join(parts)                        // concatenate once at the end

FUNCTION Decode(data)
    strs ← empty list
    i ← 0
    WHILE i < len(data)
        j ← i
        WHILE data[j] ≠ "#"                   // the length ends at a '#'
            j ← j + 1
        length ← int(data[i..j - 1])
        strs.append(data[j + 1..j + length])  // exactly length characters
        i ← j + 1 + length                    // jump over the payload unread
    RETURN strs
```

Both directions touch every character a constant number of times, so encoding and decoding take `O(total length)` time and space; collect the pieces in a list and join once, because `+=` in a loop can recopy the growing string every time. Reach for length-prefix framing whenever several values must travel through one string or one stream and come back intact: serializing a list or a record, or messages on a network socket. Serializing a binary tree (#55) is the same contract with the shape recorded by null markers, and the TinyURL design meets it with a counter and a map. The classic mistake is a pure delimiter, which passes the examples until a string contains it; the subtler one is reading a single digit as the length, which breaks on the first string of ten or more characters.

*Practice:* LC 271 Encode and Decode Strings · LC 535 Encode and Decode TinyURL · LC 297 Serialize and Deserialize Binary Tree
