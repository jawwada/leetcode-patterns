---
rank: 100
slug: url_shortener
---

Design a service that turns a long URL into a short code and back. `encode(long_url)` returns a code, `decode(short_code)` returns the original URL, or the empty string for a code never handed out, and a URL seen before gets its old code again. The design gives every new URL the next integer id and writes that id in base 62, whose digits are `0-9`, `a-z` and `A-Z`. If this server's ids start at 1,000,000, the first URL gets the code `4c92` and the next new one `4c93`, and decoding `4c93` returns the second URL.

Base 62 is positional notation with 62 digits instead of 10. `n mod 62` is the last digit, dividing by 62 drops it, and repeating until `n` reaches 0 produces the digits from right to left, so they are reversed at the end. Reading a code back runs the other way: start from 0 and, for each character, multiply by 62 and add the character's value. Every extra character multiplies the number of codes by 62, so 6 characters cover 56.8 billion ids and 7 cover 3.5 trillion. Two maps complete the design: code to URL for `decode`, and URL to code, so that a repeated URL gets its old code back instead of using up a new id.

The obvious alternative hashes the URL and keeps the first 7 characters of the hash written in base 62. The same URL then always gets the same code without a second map, but different URLs can share those 7 characters: by the birthday bound a collision becomes likely after about two million URLs, the square root of `62^7`, so every insert must look its code up and rehash on a clash. A counter cannot collide, since every id is new, and it hands out the shortest codes possible, because the ids are used in order with no gaps.

```text
to_base62(1000000): the last digit is n mod 62, then n ← floor(n / 62)
   n          n mod 62   digit   floor(n / 62)
   1000000        2        2        16129
   16129          9        9          260
   260           12        c            4
   4              4        4            0
   the digits come out as 2 9 c 4; reversed they read 4c92

from_base62("4c92"): n ← n × 62 + the value of the next digit
   0 × 62 + 4 = 4    4 × 62 + 12 = 260    260 × 62 + 9 = 16129
   16129 × 62 + 2 = 1000000

after encode(long_url), encode(other_url), encode(long_url):
   next_id   1000002              the repeat took no new id
   url_of    4c92 → https://example.com/articles/2026/how-base62-works
             4c93 → https://example.com/docs
   code_of   the same two pairs the other way round
```

```pseudo
ALPHABET ← "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

FUNCTION ToBase62(n)
    IF n = 0
        RETURN "0"
    digits ← empty list
    WHILE n > 0
        digits.append(ALPHABET[n mod 62])      // the last digit comes out first
        n ← floor(n / 62)
    digits.reverse()                           // most significant digit first
    RETURN join(digits)

FUNCTION FromBase62(code)
    n ← 0
    FOR EACH ch IN code
        n ← n * 62 + ALPHABET.index(ch)        // index = the digit's value
    RETURN n

CLASS URLShortener
    FUNCTION Init(first_id)
        self.next_id ← first_id                // start of this server's ids
        self.url_of ← empty map                // code → long url
        self.code_of ← empty map               // long url → code

    FUNCTION Encode(long_url)
        IF long_url IN self.code_of
            RETURN self.code_of[long_url]      // seen before: same code
        code ← ToBase62(self.next_id)
        self.next_id ← self.next_id + 1
        self.url_of[code] ← long_url
        self.code_of[long_url] ← code
        RETURN code

    FUNCTION Decode(short_code)
        IF short_code NOT IN self.url_of
            RETURN ""
        RETURN self.url_of[short_code]
```

Encoding costs `O(log n)` for id n, one step per character, plus the map lookups, and the maps hold every pair. At scale the single counter is a bottleneck and a single point of failure, so a coordinator, such as a database sequence or ZooKeeper, hands each server a block of ids, a million at a time, which is what `first_id` stands for; each server counts through its block alone, and a crash wastes at most the rest of one block. Snowflake ids (#145) drop the central counter altogether. Sequential codes are guessable, so links that must not be enumerable scramble the id first or use the hash with its collision check. A custom alias is a code the user picks, accepted only if the code-to-URL table lacks it; the counter must then skip any code already taken, or the id that later reaches an alias would overwrite it. Reads far outnumber writes, so hot codes live in an LRU cache (#44) in front of a store split across machines by code (#139). Excel column titles are the same conversion in base 26 with no zero digit, so each step subtracts 1 before taking the remainder. The classic mistakes are skipping the reversal, which turns 1,000,000 into `29c4`, and forgetting that 0 needs the code `0`: the loop never runs and the code comes out empty.

*Practice:* LC 535 Encode and Decode TinyURL · LC 168 Excel Sheet Column Title · LC 171 Excel Sheet Column Number
