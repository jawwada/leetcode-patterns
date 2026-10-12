# Implement String Split
*Custom warm-up (no LeetCode number) · Easy · Pattern: Linear scan with state · Reading time ~6 min*

## The problem

Implement split(s, sep) with the exact semantics of Python's str.split(sep) for a non-empty separator, without
str.split or re: empty pieces between adjacent separators and at the ends are kept, and matches are non-overlapping
left to right.

```text
Example: split("a,,b,", ",") -> ["a", "", "b", ""]; split("aaa",
  "aa") -> ["", "a"]; split("", ",") -> [""].
```

## What the problem is really asking

Write `split(s, sep)` that behaves exactly like Python's `s.split(sep)` for a non-empty separator, without calling `split` or `re`. The answer is a list of strings. Adjacent separators produce an empty piece between them. A separator at either end produces an empty piece at that end. An empty input produces `[""]`, not `[]`. A multi-character separator matches left to right without overlapping, so `"aaa"` split on `"aa"` is `["", "a"]`.

```text
 s   =  a  ,  ,  b  ,          sep = ","
        0  1  2  3  4
 cuts:     |  |     |
 pieces: "a" "" "b" ""         four pieces from three cuts
```

The number of pieces is always one more than the number of cuts. Hold on to that rule.

## Do it by hand first

Take `"a,,b,"` and a pencil. Put your finger at the start and slide right. You remember one thing: where the current piece began. When your finger lands on a comma, you write down everything from "where it began" up to the finger, then move the "began" mark to just after the comma.

```text
 a , , b ,
 ^             piece starts at 0
   ^           comma at 1 -> write "a",  piece now starts at 2
     ^         comma at 2 -> write "",   piece now starts at 3
         ^     comma at 4 -> write "b",  piece now starts at 5
           ^   end of string -> write s[5:] = ""
```

Your hand kept track of two positions: the **scan finger** and the **start of the current piece**. That pair is the whole data structure.

## The first honest attempt

The version most people say out loud uses `find`. Find the first separator, emit what is before it, chop the string to what is after it, and repeat until `find` returns −1.

```text
 remainder            find   emit   new remainder (copied!)
 "a,,b,"              1      "a"    ",b,"
 ",b,"                0      ""     "b,"
 "b,"                 1      "b"    ""
 ""                   -1     ""     (stop)
```

It is correct but wasteful. Every `s = s[k+1:]` copies the entire tail. If there are p pieces in a string of length n, the copies add up to roughly n + (n − 1) + … ≈ O(n·p), which is O(n²) when pieces are short. The drawing shows the same tail characters copied again and again.

```text
 copy 1:   , , b ,   <- most of the string
 copy 2:     b ,     <- same characters again
 copy 3:             (and again for longer inputs)
```

## The turning point

**The remainder is just a suffix, and a suffix is fully described by one integer.**

"Everything from index 2 onward" carries the same information as the copy `",b,"`. So keep `start` (where the current piece began) and `i` (the scan head) as integers on the original string. At each `i`, ask whether `sep` starts here.

- **Match:** emit `s[start:i]`. This may be the empty string, and that is correct. Then jump `i` forward by `len(sep)`, not by 1. Jumping the whole separator is what makes matches non-overlapping. Set `start = i`.
- **No match:** `i += 1`.

When the loop ends, emit `s[start:]` unconditionally. This one line produces the trailing `""` for `"a,"` and the `[""]` for an empty input. It is the line people forget.

The loop condition is `i <= len(s) - len(sep)`, the last position where the separator still fits. With a one-character separator every position gets a check.

## Watch it work

`s = "a,,b,"`, `sep = ","`.

**Frame 1.** Scan starts. Index 0 holds `a`, not a separator, so `i` moves on.
```text
 a , , b ,
 ^ start=0, i=0 -> no match, i=1
 parts = []
```

**Frame 2.** A comma at `i = 1`. Emit `s[0:1] = "a"`, jump to 2, and set start = 2.
```text
 a , , b ,
     ^ start=2, i=2
 parts = ["a"]
```

**Frame 3.** Another comma at `i = 2`. Emit `s[2:2] = ""`, the empty piece between adjacent separators.
```text
 a , , b ,
       ^ start=3, i=3
 parts = ["a", ""]
```

**Frame 4.** `b` at 3 is not a match. The comma at 4 emits `s[3:4] = "b"`.
```text
 a , , b ,
           ^ start=5, i=5 (loop ends: 5 > 5-1)
 parts = ["a", "", "b"]
```

**Frame 5.** After the loop, emit the tail `s[5:] = ""`.
```text
 parts = ["a", "", "b", ""]      matches str.split(",")
```

In every frame, `parts` held exactly the pieces whose right cut was already seen, and `s[start:i]` was the piece in progress.

## Why it is correct

Invariant: before each loop test, `parts` equals the list of pieces cut off by every separator match that begins at an index below `i`, and `start` is the index just after the most recent match (0 if none). It holds trivially at the start. On a match at `i`, the new piece is exactly `s[start:i]`, the text between the previous cut and this one, so appending it and moving `start` past the separator keeps the invariant. On a non-match, nothing is cut, and `i += 1` keeps it. When `i` passes `len(s) - len(sep)`, no further match can fit, so the only piece left is `s[start:]`. Jumping by `len(sep)` after a match means no position inside a matched separator is ever tested again, which is Python's leftmost, non-overlapping rule.

## Cost

- **Time O(n·m)**, where m = `len(sep)`: each position is compared against `sep` at most once, at O(m) per comparison. It is O(n) for a single-character separator.
- **Space O(n)** for the output. Every input character lands in at most one piece. Extra working space is O(1) apart from the m-character comparison slice. Use `s.startswith(sep, i)` to avoid even that.

## Variations you will meet

- **`str.split()` with no argument.** Splits on runs of whitespace and never emits empty pieces. Skip runs, and emit only when the piece is non-empty. Reverse Words uses exactly this.
- **`maxsplit`.** Count the matches and stop matching after k. The final `s[start:]` swallows the rest.
- **Long separators with a worst-case guarantee.** Naive comparison is O(n·m). KMP (Longest Happy Prefix later in the chapter) brings it to O(n + m).
- **Empty separator.** Python raises `ValueError`; other languages split into characters. Ask.

## What to carry forward

Two integers, `start` and `i`, replace every substring you might have copied. Always flush the last piece after the loop. The next problem keeps the single left-to-right pass but stops caring where things are, only how many of each there are.
