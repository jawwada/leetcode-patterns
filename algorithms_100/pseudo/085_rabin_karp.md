---
rank: 85
slug: rabin_karp
---

Given a text and a pattern, return every index where the pattern starts in the text. In `abracadabra` the pattern `abra` starts at `0` and at `7`, so the answer is `[0, 7]`.

The brute force compares the pattern with every window of `m` characters, `O(n · m)` time in the worst case. Rabin-Karp compares numbers instead. Read a string as a number written in base 256, one digit per character, so `abra` is the four digits `97 98 114 97`; kept modulo a large prime, that number is the string's hash. Equal strings always have equal hashes, so a window whose hash differs from the pattern's is dismissed by one integer comparison. Equal hashes almost always mean equal strings, but not always, so every hash hit is confirmed by comparing the characters.

The trick that makes it fast is the roll. Sliding a window over the decimal digits of `31415926` from `31415` to `14159` means removing the leading 3, worth 30000, shifting left by multiplying by 10, and adding the 9. A window of text slides the same way in base 256: subtract the leading character times `BASE^(m - 1)`, multiply by `BASE`, add the incoming character, all modulo the prime. Each slide costs `O(1)`, however long the pattern is.

```text
"abra" = base-256 digits 97 98 114 97 → pattern_hash 633841754 (MOD 10^9 + 7)

start   window   window_hash   hash hit?   compare characters
  0      abra     633841754      yes        abra = abra ✓   match at 0
  1      brac     651663196      no
  2      raca     918985050      no
  3      acad     633902941      no
  4      cada     667327066      no
  5      adab     633968475      no
  6      dabr     684103787      no
  7      abra     633841754      yes        abra = abra ✓   match at 7

roll 0 → 1:  drop 'a': (633841754 - 97 × 16777216) mod MOD = 6451809
             add 'c':  (6451809 × 256 + 99) mod MOD = 651663196
```

```pseudo
BASE ← 256                    // one digit per character code
MOD ← 1000000007              // a large prime keeps collisions rare

FUNCTION PolyHash(s)
    value ← 0
    FOR EACH ch IN s
        value ← (value * BASE + code(ch)) mod MOD   // shift left, add a digit
    RETURN value

FUNCTION RabinKarp(text, pattern)
    n ← len(text)
    m ← len(pattern)
    IF m = 0 OR m > n
        RETURN empty list
    high ← BASE^(m - 1) mod MOD               // weight of the leading digit
    pattern_hash ← PolyHash(pattern)
    window_hash ← PolyHash(text[0..m - 1])
    matches ← empty list
    FOR start FROM 0 TO n - m
        IF window_hash = pattern_hash AND text[start..start + m - 1] = pattern
            matches.append(start)             // a hash hit, confirmed
        IF start + m < n                      // roll the window one step right
            window_hash ← (window_hash - code(text[start]) * high) mod MOD
            window_hash ← (window_hash * BASE + code(text[start + m])) mod MOD
    RETURN matches
```

Hashing the pattern and the first window costs `O(m)`, each of the `n - m` rolls costs `O(1)`, and each hash hit costs `O(m)` to verify, so the expected time is `O(n + m)` when matches are few; many true matches, or a modulus small enough to collide often, push it toward `O(n · m)`. Collisions are real: with these constants `neonatus` and `plumular` share the hash 7749640, which is why the compare stays. KMP (#64) guarantees `O(n + m)` without luck, so Rabin-Karp earns its place where hashing many substrings is the point. Repeated DNA Sequences hashes every length-10 window into a set. Longest Duplicate Substring binary searches the length (#10), since a repeat of length `L` contains a repeat of length `L - 1`, and tests each length with a set of rolling hashes. The classic mistakes are trusting a hash hit without the compare and, outside Python, letting the subtraction go negative: `%` in Java or C++ keeps the sign, so add `MOD` back before reducing.

*Practice:* LC 28 Find the Index of the First Occurrence in a String · LC 187 Repeated DNA Sequences · LC 1044 Longest Duplicate Substring · LC 1316 Distinct Echo Substrings
