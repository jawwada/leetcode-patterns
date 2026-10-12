"""
URL Shortener - Base62-Encode an Increasing ID

encode(long_url) gives each new URL the next integer id and returns that id
in base 62 (digits 0-9, a-z, A-Z) as its short code; a repeated URL keeps its
code, and decode(code) returns the URL, or "" for an unknown code.
Ids starting at 1000000: encode(first url) -> 4c92, decode("4c92") -> the url.
"""


# --- algorithm ---
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base62(n):
    """Take the last digit with n % 62, drop it with n // 62, repeat; the
    digits come out backwards. O(log n)."""
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(ALPHABET[n % 62])     # the last digit comes out first
        n = n // 62
    digits.reverse()                        # most significant digit first
    return "".join(digits)


def from_base62(code):
    """Shift left one digit (times 62) and add the next one. O(len(code))."""
    n = 0
    for ch in code:
        n = n * 62 + ALPHABET.index(ch)     # index = the digit's value
    return n


class URLShortener:
    """A counter hands out ids and base 62 writes each id as a short code;
    two maps remember the pairs both ways."""

    def __init__(self, first_id):
        self.next_id = first_id         # the start of this server's id range
        self.url_of = {}                # code -> long url
        self.code_of = {}               # long url -> code

    def encode(self, long_url):
        """A known url keeps its code; else base 62 of the next id. O(log n)."""
        if long_url in self.code_of:
            return self.code_of[long_url]   # seen before: same code
        code = to_base62(self.next_id)
        self.next_id += 1
        self.url_of[code] = long_url
        self.code_of[long_url] = code
        return code

    def decode(self, short_code):
        """Look the code up; "" if it was never handed out. O(1)."""
        if short_code not in self.url_of:
            return ""
        return self.url_of[short_code]


# --- try it ---
long_url = "https://example.com/articles/2026/how-base62-works"
other_url = "https://example.com/docs"
shortener = URLShortener(1000000)       # this server's ids start here
print(shortener.encode(long_url), shortener.encode(other_url))  # -> 4c92 4c93
print(shortener.encode(long_url), shortener.next_id)    # -> 4c92 1000002
print(shortener.decode("4c93"))         # -> https://example.com/docs
print(repr(shortener.decode("4c94")))   # -> ''
print(to_base62(0), to_base62(61), to_base62(62))       # -> 0 Z 10
print(from_base62("4c92"), from_base62("10"))           # -> 1000000 62
