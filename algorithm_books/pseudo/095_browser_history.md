---
rank: 95
slug: browser_history
---

Design the history of one browser tab. It starts on a homepage; `visit(url)` opens a new page and erases every page that `forward` could still have reached, and `back(steps)` and `forward(steps)` move up to `steps` pages through the history, stopping at either end, and return the page they land on. Starting at `home` and visiting `news`, `mail` and `maps`, `back(2)` lands on `news`; visiting `docs` from there erases `mail` and `maps`, so `forward(1)` stays on `docs`.

The natural model is two stacks, the pages behind the current one and the pages ahead of it. It works, but `back(steps)` carries pages from one stack to the other one at a time, `O(steps)`, and `forward` does the same in reverse. The history is a straight line, though, and a position on a line is just an index. Keep every page in one array with a cursor `current` on the page on screen, and `back` and `forward` become arithmetic: subtract or add `steps`, clamp to the ends, and read one slot, `O(1)` however far the jump. The only delicate call is `visit`, which must cut off the forward history. Truncating the array works, but a single visit can then pay for thousands of dropped pages, so a second index, `last`, marks where the live history ends instead. `visit` moves the cursor one slot forward, writes the new page there, overwriting a dead page or appending when the array has no slot left, and sets `last` to that slot. The slots past `last` still hold old pages, but no call can reach them, because `forward` clamps at `last`.

Picture the array as a ruler, with the cursor sliding along it and a fence at `last`. `back` and `forward` slide the cursor between slot 0 and the fence; `visit` steps the cursor one slot right, writes there and moves the fence right behind it, leaving everything beyond the fence dead.

```text
slot                 0     1     2     3
after visit(docs)    home  news  docs  (maps)     maps lies past last: dead
                                 ▲
                         current = last = 2

operation            pages                    current   last
start                home                     0         0
visit(news)          home news                1         1
visit(mail)          home news mail           2         2
visit(maps)          home news mail maps      3         3
back(2) → news       home news mail maps      1         3
visit(docs)          home news docs (maps)    2         2     overwrite slot 2
forward(1) → docs    home news docs (maps)    2         2     clamped at last
back(5) → home       home news docs (maps)    0         2     clamped at 0
forward(9) → docs    home news docs (maps)    2         2     clamped at last
```

```pseudo
CLASS BrowserHistory
    FUNCTION Init(homepage)
        self.pages ← [homepage]             // pages[0..last] is live history
        self.current ← 0                    // index of the page on screen
        self.last ← 0                       // the newest page forward can reach

    FUNCTION Visit(url)
        self.current ← self.current + 1
        IF self.current = len(self.pages)
            self.pages.append(url)          // the array grows by one
        ELSE
            self.pages[self.current] ← url  // overwrite a dead slot
        self.last ← self.current            // forward history ends here

    FUNCTION Back(steps)
        self.current ← max(0, self.current - steps)
        RETURN self.pages[self.current]

    FUNCTION Forward(steps)
        self.current ← min(self.last, self.current + steps)
        RETURN self.pages[self.current]
```

`back` and `forward` cost `O(1)`, `visit` costs amortized `O(1)` because the array sometimes grows, and the memory is one slot per page of the longest history so far. The signals are back and forward, undo and redo, and any cursor on a sequence where a new action throws away the redo side. The two-stack version is this array cut in two at the cursor; it fits when every move is a single step, as in undo and redo, and Design a Text Editor (#144) uses it to hold the text on either side of the cursor. A doubly linked list of pages is the third common answer, again with `O(steps)` moves. The classic mistake is clamping `forward` at `len(pages) - 1` instead of at `last`: after `visit(docs)` in the trace, `forward(9)` would bring back the dead `maps`. Updating `last` only when the array grows does the same damage.

*Practice:* LC 1472 Design Browser History · LC 2296 Design a Text Editor · LC 1381 Design a Stack With Increment Operation
