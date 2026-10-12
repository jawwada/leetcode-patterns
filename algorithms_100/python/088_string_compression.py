"""
String Compression - Run-Length Encoding with Read and Write Pointers

Compress a list of characters in place: each run of one repeated character
becomes the character, then the run length if it is more than 1, one digit
per cell; return the new length:
["a", "a", "b", "b", "c", "c", "c"] -> 6, with ["a", "2", "b", "2", "c", "3"].
"""


# --- algorithm ---
def compress(chars):
    """Read walks over each run, write lays down char + count digits.
    O(n) time, O(1) extra space."""
    write = 0
    read = 0
    while read < len(chars):
        ch = chars[read]
        start = read
        while read < len(chars) and chars[read] == ch:
            read += 1                   # walk to the end of the run
        chars[write] = ch
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):    # 12 is written as "1", "2"
                chars[write] = digit
                write += 1
    return write


# --- try it ---
chars = ["a", "a", "b", "b", "c", "c", "c"]
length = compress(chars)
print(length, chars[0:length])          # -> 6 ['a', '2', 'b', '2', 'c', '3']
chars = list("abbbbbbbbbbbb")
length = compress(chars)
print(length, chars[0:length])          # -> 4 ['a', 'b', '1', '2']
print(compress(["a"]), compress(list("abc")))   # -> 1 3
