# Encode and Decode Strings
*LeetCode 271 · Medium · Pattern: Length-prefixed serialization · Reading time ~6 min*

## What the problem is really asking

You must write two functions. `encode` squeezes a list of strings into one single string, and `decode` turns that string back into the exact same list. Exact means exact: the same number of strings, in the same order, with the same characters, and that includes empty strings and strings full of commas, `#` signs, digits, backslashes, or anything else. You may not assume any character is "safe".

The answer is a pair of inverse functions, a format. What makes it hard is that the strings can contain *anything*, so whatever you use to mark "one string ends here" could also appear inside a string. The real problem is boundaries.

```text
input:   ["ab", "", "3#x"]

encode   "2#ab" + "0#" + "3#3#x"
           |       |      |
           v       v      v
output:  "2#ab0#3#3#x"

decode   "2#ab0#3#3#x"  ->  ["ab", "", "3#x"]
```

This example is deliberately nasty. The middle string is empty, and the last string itself looks like a header (`3#`). Any scheme that survives it is a real scheme.

## Do it by hand first

Imagine reading a list of names to a friend over the phone, and the names may contain any punctuation. Saying "comma" between names fails the moment a name contains a comma. What people actually do is announce: "the next one is two letters: a, b". Then "the next one is zero letters". Then "the next one is three letters: 3, hash, x". Your friend never has to guess where a name ends; they count.

```text
you say:   "two:"   a b     "zero:"   "three:"  3 # x
friend:    count=2  a b     count=0   count=3   3 # x
           ^ remaining 2,1,0 ^ done   ^ 3,2,1,0 ^ done
```

What your friend's hand kept track of was a single counter: *how many characters remain in the current string*. When it hits zero, the string is over, no matter what the characters were. That counter is the seed of the format.

## The first honest attempt

The first idea is to join with a delimiter, say a comma, and split on it. It breaks instantly:

```text
["a,b", "c"] --join--> "a,b,c" --split--> ["a","b","c"]
                          ^ payload comma read as a boundary
```

The standard patch is escaping. Encode turns every `\` into `\\` and every `,` into `\,`. Decode walks the string one character at a time, keeping a "previous char was a backslash" flag, and only treats an *unescaped* comma as a boundary. This is correct, and it is O(total length).

But look at where the work goes. The decoder must inspect every single character of every payload just to find out where the payload stops. The payload's content is irrelevant to us, yet we read it with suspicion character by character. And the output size depends on the content: a string made of commas doubles in size.

```text
encode:  "a,b" -> "a\,b"        ",,," -> "\,\,\,"  (2x)
decode:  a  \  ,  b  ,  c
         ^  ^  ^  ^  ^  ^   every char checked against
                            the escape flag and ','
```

## The turning point

**Claim: if every string is preceded by its length, the decoder never needs to look inside a payload, so no character is ever ambiguous.**

A delimiter asks the decoder to *search* for a boundary, and search fails when the payload can contain what you are searching for. A length *tells* the decoder where the boundary is. It reads a number, then consumes exactly that many characters, whatever they are. The payload's content stops mattering.

One detail remains: the length itself is written in digits, and a payload can start with digits. If we glue the length straight onto the payload, the decoder cannot tell where the number stops:

```text
no separator:   "123abc..."
   length 1  ?  payload "2", next frame starts "3abc..."
   length 12 ?  payload "3abc...(12 chars)"
   length 123?  payload of 123 chars
   -> the digits of the length run into the payload

with '#':       "12#3abc..."   the length ends at the first '#'
```

So after the digits we write one terminator, `#`. Because digits are never `#`, the first `#` at or after the start of a frame is always the end of the length. The `#` characters *inside* payloads are never searched for, because the decoder has already jumped past them.

The format is a sequence of frames, each `[length]#[payload]`, and the decoder is a pointer that hops:

```text
frame:     | len | # |   payload (len chars)   |
pointer:     i     j   j+1 ............ j+len   next i = j+1+len
```

This is how real wire protocols work (HTTP chunked encoding, Protobuf, netstrings): content-agnostic framing by length.

## Watch it work

Decoding `s = "2#ab0#3#3#x"` (positions 0..10).

```text
Frame 1   pos: 0 1 2 3 4 5 6 7 8 9 10
          s:   2 # a b 0 # 3 # 3 # x
               ^i
          out = []
```
The pointer starts at the first frame's length digits.

```text
Frame 2   s:   2 # a b 0 # 3 # 3 # x
               i j [a b]
          len = 2, out = ["ab"], next i = 1+1+2 = 4
```
The first `#` from 0 is at 1; read 2 characters after it and jump to 4.

```text
Frame 3   s:   2 # a b 0 # 3 # 3 # x
                       i j
          len = 0, out = ["ab", ""], next i = 5+1+0 = 6
```
A zero length yields the empty string and the pointer just steps over the `#`.

```text
Frame 4   s:   2 # a b 0 # 3 # 3 # x
                           i j [3 # x]
          len = 3, out = ["ab", "", "3#x"], next i = 11
```
The payload `3#x` contains a `#`, but we never search inside it; we take 3 characters blindly.

```text
Frame 5   i = 11 = len(s)  ->  stop
          out = ["ab", "", "3#x"]
```
The pointer landed exactly on the end, so the loop ends with the original list.

At every frame the pointer sat on the first digit of a frame, never inside a payload. The only search the decoder ever does is for the `#` right after a run of digits.

## Why it is correct

The invariant: at the top of the decode loop, `i` is the start of a frame (or the end of the string). Initially `i = 0` is the start of the first frame. Inside a frame, the characters from `i` are the decimal digits of the length followed by `#`; digits contain no `#`, so `s.index("#", i)` finds exactly the terminator of this frame's length, never a `#` inside any payload (all payload characters lie after it). The next `length` characters are precisely the payload, and `j + 1 + length` is the first character of the next frame, which restores the invariant. Each iteration therefore recovers one original string, in order, and the loop ends exactly at `len(s)` after the last frame.

Encoding is injective as a result: two different lists produce two different strings, because the decoder would recover each list from its encoding.

## Cost

- **Time O(N):** where N is the total number of characters across all strings, plus O(log L) digits per string of length L. Encode writes each character once; decode copies each payload once with a slice and reads only the header digits.
- **Space O(N):** for the output (string or list). The overhead per string is its length digits plus one `#`.

The escaping version has the same big-O, but every payload character is inspected, and output size depends on content. Length-prefixing is content-independent.

## Variations you will meet

- **Fixed-width header.** Write every length as exactly 4 characters (or 4 bytes): `"0002ab0000..."`. No terminator is needed because the decoder always reads 4. This is what binary protocols do; it caps the maximum string length.
- **Serialize and Deserialize Binary Tree (297).** Same problem with structure instead of a flat list: you must encode where a subtree ends. Pre-order with null markers plays the role the length plays here.
- **Streaming decode.** If the encoded string arrives in chunks, the decoder must be able to stop mid-header or mid-payload and resume. Lengths make this easy: you know exactly how many more characters you are waiting for.
- **Unicode or bytes.** Decide whether the length counts characters or bytes; encoder and decoder must agree, or multi-byte characters will desynchronize every frame after them.

## What to carry forward

Say how long, not where it ends: a length prefix lets the reader jump, so the content can be anything. The next problem pushes "information stored in position" further: in First Missing Positive, the array's own indices become the hash table, and the place a value sits encodes whether it was seen.
