"""
Valid Number (LeetCode 65) - Hard
Chapter: strings
Pattern: Single-pass state machine with flags

Return True if the string is a valid number: an optional sign, then an integer or a decimal
("3.", ".5", "3.14"), optionally followed by 'e' or 'E', an optional sign and an integer.
No spaces, no inf or nan.
Example: "2e10", "-.9" and "4." are valid; "e3", "99e2.5" and "." are not.
"""


# --- brute force ---
def digits_only(text):
    """True when text is non-empty and every character is a digit."""
    if text == "":
        return False
    for ch in text:
        if ch < "0" or ch > "9":
            return False
    return True


def drop_sign(text):
    """Remove one leading '+' or '-' if there is one."""
    if text[:1] == "+" or text[:1] == "-":
        return text[1:]
    return text


def is_integer(text):
    """Optional sign, then digits."""
    return digits_only(drop_sign(text))


def is_decimal(text):
    """Optional sign, then digits with at most one dot and at least one digit somewhere."""
    text = drop_sign(text)
    if "." not in text:
        return digits_only(text)
    before, after = text.split(".", 1)             # re-scans both halves with digits_only
    if before != "" and not digits_only(before):
        return False
    if after != "" and not digits_only(after):
        return False
    return before + after != ""                    # "." alone has no digit


def brute_force(s):
    """Split at 'e', then at '.', and test each slice with its own helper. 3-4 passes over s."""
    for k in range(len(s)):
        if s[k] == "e" or s[k] == "E":
            return is_decimal(s[:k]) and is_integer(s[k + 1:])
    return is_decimal(s)


# --- optimal ---
def valid_number(s):
    """One pass with three flags: seen a digit, a dot, an exponent. O(n) time, O(1) space."""
    seen_digit = False
    seen_dot = False
    seen_exp = False
    for i in range(len(s)):
        ch = s[i]
        if "0" <= ch <= "9":
            seen_digit = True
        elif ch == "+" or ch == "-":
            if i > 0 and s[i - 1] != "e" and s[i - 1] != "E":
                return False                       # a sign only at the start or right after e
        elif ch == ".":
            if seen_dot or seen_exp:
                return False                       # one dot, and never inside the exponent
            seen_dot = True
        elif ch == "e" or ch == "E":
            if seen_exp or not seen_digit:
                return False                       # one e, and it needs a mantissa before it
            seen_exp = True
            seen_digit = False                     # the exponent needs its own digits
        else:
            return False
    return seen_digit


# --- try the brute force ---
print(brute_force("2e10"))                         # -> True
print(brute_force("-.9"))                          # -> True
print(brute_force("e3"))                           # -> False
print(brute_force("99e2.5"))                       # -> False


# --- try the optimal ---
print(valid_number("2e10"))                        # -> True
print(valid_number("-.9"))                         # -> True
print(valid_number("e3"))                          # -> False
print(valid_number("99e2.5"))                      # -> False
