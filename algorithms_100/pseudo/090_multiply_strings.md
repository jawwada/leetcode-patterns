---
rank: 90
slug: multiply_strings
---

Multiply two non-negative integers given as decimal strings with no leading zeros and return the product as a string, without converting the inputs to numbers; they can be far longer than any machine integer. `"123"` times `"456"` is `"56088"`.

The method is the one from school, minus the partial rows written out on paper. Index both strings from the left. Digit `i` of `num1` is worth `10^(m-1-i)` and digit `j` of `num2` is worth `10^(n-1-j)`, so their product is worth `10^(m+n-2-i-j)`. A product of an `m`-digit and an `n`-digit number has at most `m + n` digits, so it fits in an array `digits` of `m + n` slots, where slot `p` is worth `10^(m+n-1-p)`; matching the two powers lands the product of digits `i` and `j` in slot `i + j + 1`. Walk both strings from the right, add each digit product into its slot, keep the ones digit there and push the tens into slot `i + j`, one to the left. The textbook alternative builds one shifted partial product per digit of `num2` and adds them up with the Add Strings loop; it makes the same digit multiplications but also allocates `n` intermediate strings and adds them one by one.

Picture the `m × n` grid of digit pairs. Every cell on one anti-diagonal, where `i + j` is constant, has the same place value, so the whole anti-diagonal pours into the same slot, and carries ripple right to left like the column sums on paper. No final carry pass is needed: every slot except the leftmost is last touched by its own `mod 10`, and the leftmost cannot overflow because the product fits in `m + n` digits.

```text
 i  j   num1[i] * num2[j]   slot i+j+1   total   digits after the step
 2  2     3 * 6 = 18            5          18     [0, 0, 0, 0, 1, 8]
 2  1     3 * 5 = 15            4          16     [0, 0, 0, 1, 6, 8]
 2  0     3 * 4 = 12            3          13     [0, 0, 1, 3, 6, 8]
 1  2     2 * 6 = 12            4          18     [0, 0, 1, 4, 8, 8]
 1  1     2 * 5 = 10            3          14     [0, 0, 2, 4, 8, 8]
 1  0     2 * 4 =  8            2          10     [0, 1, 0, 4, 8, 8]
 0  2     1 * 6 =  6            3          10     [0, 1, 1, 0, 8, 8]
 0  1     1 * 5 =  5            2           6     [0, 1, 6, 0, 8, 8]
 0  0     1 * 4 =  4            1           5     [0, 5, 6, 0, 8, 8]
digits[0] is 0 (the product needs only 5 digits), so the answer is "56088"
```

```pseudo
FUNCTION Multiply(num1, num2)
    IF num1 = "0" OR num2 = "0"
        RETURN "0"
    m ← len(num1)
    n ← len(num2)
    digits ← array of m + n zeros          // the product has at most m + n
    FOR i FROM m - 1 DOWNTO 0
        FOR j FROM n - 1 DOWNTO 0
            product ← ToInt(num1[i]) * ToInt(num2[j])
            total ← digits[i + j + 1] + product
            digits[i + j + 1] ← total mod 10                    // ones digit
            digits[i + j] ← digits[i + j] + floor(total / 10)   // carry left
    start ← 0
    IF digits[0] = 0                       // only m + n - 1 digits needed
        start ← 1
    result ← empty list
    FOR k FROM start TO m + n - 1
        result.append(ToString(digits[k]))
    RETURN join(result, "")
```

The double loop does `m × n` digit multiplications, so the time is `O(m × n)` and the space is the `O(m + n)` digit array. The signals are numbers given as strings or digit arrays, "without converting to integers", or values too big for 64 bits. The same right-to-left carry loop with `total = a + b + carry` is all of Add Strings (LC 415), and Add Binary (LC 67) is that loop in base `2`; Karatsuba multiplies faster, in `O(n^1.585)`, but no interview expects it. The classic mistakes are forgetting the `"0"` case, which otherwise returns a string of zeros or nothing at all, adding the carry into slot `i + j + 1` instead of `i + j`, and keeping the leading zero when the product needs only `m + n - 1` digits.

*Practice:* LC 43 Multiply Strings · LC 415 Add Strings · LC 67 Add Binary
