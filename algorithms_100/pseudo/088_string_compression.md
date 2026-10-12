---
rank: 88
slug: string_compression
---

Compress an array of characters in place with run-length encoding: every maximal run of one repeated character becomes the character, followed by the length of the run when that length is more than `1`, written one digit per cell. Return the new length; whatever lies beyond it does not matter. `["a", "a", "b", "b", "c", "c", "c"]` becomes `["a", "2", "b", "2", "c", "3"]` with length `6`, and a run of twelve `b`s becomes `"b", "1", "2"`.

Building the answer in a second list is easy and costs `O(n)` extra space; the in-place version runs two pointers left to right over the same array. The read pointer finds runs: from `read` it walks forward while the character repeats, so the run is `chars[start..read - 1]` and its length is `read - start`. The write pointer lays down the encoding of each finished run, the character and then the digits of the count. Writing over the input is safe because the encoding of a run is never longer than the run itself: one cell for a single character, and `1 + d` cells for a run of length `k ≥ 2` whose count has `d` digits, where `1 + d ≤ k`. So `write` never passes `read`, and every cell it overwrites has already been read.

Picture the read pointer as a scout running ahead to the end of each run and the write pointer as a scribe following behind, compacting the ground the scout has covered. The gap between them grows only when a run of three or more shrinks into fewer cells, and the scribe never steps onto a cell the scout has not yet passed.

```text
slot             0   1   2   3   4   5   6
start            a   a   b   b   c   c   c
run a × 2        a   2   b   b   c   c   c      write → 2, read → 2
run b × 2        a   2   b   2   c   c   c      write → 4, read → 4
run c × 3        a   2   b   2   c   3   c      write → 6, read → 7
                                         ↑ past the new length: ignored
return 6: the compressed text is chars[0..5] = a 2 b 2 c 3
```

```pseudo
FUNCTION Compress(chars)
    write ← 0
    read ← 0
    WHILE read < len(chars)
        ch ← chars[read]
        start ← read
        WHILE read < len(chars) AND chars[read] = ch
            read ← read + 1                   // walk to the end of the run
        chars[write] ← ch
        write ← write + 1
        count ← read - start
        IF count > 1
            FOR EACH digit IN ToString(count)     // 12 is written as "1", "2"
                chars[write] ← digit
                write ← write + 1
    RETURN write
```

Each cell is passed once by the scout and written at most once by the scribe, so the time is `O(n)`, and the only extra memory is the handful of digits of the current count. The signals are runs of equal neighbors, "in place" paired with "return the new length", and any pair of encode and decode formats. Decoding is the mirror image: read a character, read digits while they are digits to rebuild the count (no digits means `1`), and emit the character that many times. That works only when the characters themselves are never digits; text that may contain digits needs an unambiguous frame such as the length prefix of #66. Count and Say (LC 38) applies run-length encoding, with the count first and `1`s written out, to its own output again and again. The classic mistakes are writing the count into one cell (`"12"` instead of `"1"`, `"2"`), writing a `"1"` after single characters, and, in the version that flushes a run only when the character changes, forgetting to flush the final run.

*Practice:* LC 443 String Compression · LC 38 Count and Say · LC 271 Encode and Decode Strings
