---
rank: 144
slug: text_editor
---

Design a text editor with a cursor. `add_text(text)` types the text at the cursor, which ends up just after it; `delete_text(k)` backspaces up to `k` characters and returns how many it actually deleted; `cursor_left(k)` and `cursor_right(k)` move the cursor up to `k` places, stopping at either end of the text, and return the last `min(10, len)` characters to the left of the cursor, where `len` is how many there are. Typing `leetcode`, deleting 4 and typing `practice` leaves `leetpractice|`, with `|` marking the cursor; then `cursor_left(8)` gives `leet|practice` and returns `"leet"`.

The brute force keeps one string and a cursor index, and every insertion or deletion in the middle rebuilds the string, `O(n)` per call even when `k` is tiny. Yet every operation happens at the cursor, and the cursor splits the text into two halves that change only at their facing ends. A stack changes only at its top. So keep the text before the cursor on one stack, `left`, with the character just before the cursor on top, and the text after the cursor on a second stack, `right`, stored reversed so that its top is the character just after the cursor. Typing pushes onto `left` and backspace pops from it; the text far from the cursor is never touched.

Moving the cursor pours characters from one stack onto the other. One step left pops the top of `left`, the character just before the cursor, and pushes it onto `right`, where it becomes the character just after the cursor; one step right is the mirror image. Both loops stop early when the stack they pop from runs empty, which is exactly the cursor reaching an end of the text, and `delete_text` counts its pops so that it can report a short delete. The answer string is always the top ten of `left`, read in text order from the bottom up.

```text
call                       before the cursor │ after the cursor  returns
add_text("leetcode")         l e e t c o d e │
delete_text(4)                       l e e t │                   4
add_text("practice") l e e t p r a c t i c e │
cursor_right(3)      l e e t p r a c t i c e │                   "etpractice"
cursor_left(8)                       l e e t │ p r a c t i c e   "leet"
delete_text(10)                              │ p r a c t i c e   4
cursor_left(2)                               │ p r a c t i c e   ""
cursor_right(6)                  p r a c t i │ c e               "practi"
both stacks keep their top at the cursor │; right is stored reversed,
so at the end it holds ['e', 'c'] with 'c' on top
```

```pseudo
CLASS TextEditor
    FUNCTION Init()
        self.left ← empty stack         // text before the cursor, top = nearest
        self.right ← empty stack        // text after the cursor, reversed

    FUNCTION AddText(text)
        FOR EACH ch IN text
            self.left.push(ch)

    FUNCTION DeleteText(k)
        deleted ← 0
        WHILE deleted < k AND len(self.left) > 0
            self.left.pop()
            deleted ← deleted + 1
        RETURN deleted

    FUNCTION CursorLeft(k)
        WHILE k > 0 AND len(self.left) > 0
            ch ← self.left.pop()
            self.right.push(ch)         // it is now just after the cursor
            k ← k - 1
        RETURN self.LastTen()

    FUNCTION CursorRight(k)
        WHILE k > 0 AND len(self.right) > 0
            ch ← self.right.pop()
            self.left.push(ch)          // it is now just before the cursor
            k ← k - 1
        RETURN self.LastTen()

    FUNCTION LastTen()
        start ← max(0, len(self.left) - 10)
        RETURN join(self.left[start..len(self.left) - 1])
```

Every call does at most one pop and one push per character it types, deletes or moves past, plus at most ten steps to build the returned string, so a request for `k` characters costs `O(k)` however long the document is, and the two stacks hold the text once, `O(n)` space. This is the gap buffer that editors such as Emacs use: one array holding the text before the cursor at its front, the text after it at its back, and free space in between, with the two stacks as the two sides of the gap. A doubly linked list of characters with a cursor node supports the same calls in `O(k)` but pays a node per character, and a rope, a balanced tree of string chunks, takes over when documents are huge and edits jump around. Reach for two facing stacks whenever a position moves back and forth through a sequence and edits happen only where it stands; Browser History (#95) has the same shape, with back pages on one side of the cursor and forward pages on the other, but there a visit erases the forward pages, so one array and a cursor can jump any distance in `O(1)`. The classic mistake is joining all of `left` and then keeping its last ten characters, which costs `O(n)` on every cursor move and turns the design back into the brute force; slice the last ten first, as `LastTen` does.

*Practice:* LC 2296 Design a Text Editor · LC 1472 Design Browser History · LC 844 Backspace String Compare
