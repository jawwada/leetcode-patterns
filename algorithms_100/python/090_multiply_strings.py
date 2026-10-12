"""
Multiply Strings - Grade-School Multiplication into a Digit Array

Multiply two non-negative integers given as decimal strings (no leading zeros)
and return the product as a string, without converting the whole inputs to
numbers: "123", "456" -> "56088".
"""


# --- algorithm ---
def multiply(num1, num2):
    """Each digit pair adds its product into slot i + j + 1 of an m + n
    digit array, carrying left. O(m * n) time, O(m + n) space."""
    if num1 == "0" or num2 == "0":
        return "0"
    m = len(num1)
    n = len(num2)
    digits = [0] * (m + n)              # the product has at most m + n digits
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            product = int(num1[i]) * int(num2[j])   # one digit times one digit
            total = digits[i + j + 1] + product
            digits[i + j + 1] = total % 10          # keep the ones digit
            digits[i + j] += total // 10            # carry one slot left
    start = 0
    if digits[0] == 0:                  # only m + n - 1 digits were needed
        start = 1
    result = []
    for k in range(start, m + n):
        result.append(str(digits[k]))
    return "".join(result)


# --- try it ---
print(multiply("123", "456"))           # -> 56088
print(multiply("2", "3"))               # -> 6
print(multiply("99", "99"))             # -> 9801
print(multiply("12345", "0"))           # -> 0
