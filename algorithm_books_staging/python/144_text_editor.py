"""
Design a Text Editor - Two Stacks Around the Cursor

Edit text at a cursor: add_text(text) types there, delete_text(k) backspaces
up to k characters and returns how many went, cursor_left(k) / cursor_right(k)
move it and return the last min(10, len) characters to its left. Add
"leetcode", delete_text(4) -> 4, add "practice", cursor_left(8) -> "leet".
"""


# --- algorithm ---
class TextEditor:
    """Characters left of the cursor on one stack, characters right of it on
    another, nearest on top of both. O(k) per call."""

    def __init__(self):
        self.left = []              # text before the cursor, top = nearest
        self.right = []             # text after the cursor, reversed

    def add_text(self, text):
        """Type at the cursor: push every character onto left. O(len(text))."""
        for ch in text:
            self.left.append(ch)

    def delete_text(self, k):
        """Backspace up to k times; return how many were deleted. O(k)."""
        deleted = 0
        while deleted < k and len(self.left) > 0:
            self.left.pop()
            deleted += 1
        return deleted

    def cursor_left(self, k):
        """Move up to k characters from left to right. O(k)."""
        while k > 0 and len(self.left) > 0:
            ch = self.left.pop()
            self.right.append(ch)       # it is now just after the cursor
            k -= 1
        return self.last_ten()

    def cursor_right(self, k):
        """Move up to k characters from right back to left. O(k)."""
        while k > 0 and len(self.right) > 0:
            ch = self.right.pop()
            self.left.append(ch)        # it is now just before the cursor
            k -= 1
        return self.last_ten()

    def last_ten(self):
        """The last min(10, len(left)) characters before the cursor. O(1)."""
        start = max(0, len(self.left) - 10)
        return "".join(self.left[start:])


# --- try it ---
editor = TextEditor()
editor.add_text("leetcode")
print(editor.delete_text(4))                # -> 4
editor.add_text("practice")
print(editor.cursor_right(3))               # -> etpractice
print(editor.cursor_left(8))                # -> leet
print(editor.delete_text(10))               # -> 4
print(repr(editor.cursor_left(2)))          # -> ''
print(editor.cursor_right(6), editor.right)  # -> practi ['e', 'c']
