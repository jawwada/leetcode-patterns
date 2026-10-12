"""
Design Browser History - One Array and a Cursor

Start on a homepage; visit(url) opens a page and clears the forward history,
and back(steps) and forward(steps) move at most steps pages and return the page
shown: home, visit news, mail, maps, back(2), visit docs, forward(1) -> docs.
"""


# --- algorithm ---
class BrowserHistory:
    """The pages in one array, a cursor and the last reachable index.
    back and forward O(1), visit amortized O(1)."""

    def __init__(self, homepage):
        self.pages = [homepage]     # pages[0..last] is live history
        self.current = 0            # index of the page on screen
        self.last = 0               # the newest page forward can reach

    def visit(self, url):
        """Write url after the cursor; drop the pages ahead. Amortized O(1)."""
        self.current += 1
        if self.current == len(self.pages):
            self.pages.append(url)              # the array grows by one
        else:
            self.pages[self.current] = url      # overwrite a dead slot
        self.last = self.current                # forward history ends here

    def back(self, steps):
        """Move back at most steps pages, never before index 0. O(1)."""
        self.current = max(0, self.current - steps)
        return self.pages[self.current]

    def forward(self, steps):
        """Move forward at most steps pages, never past last. O(1)."""
        self.current = min(self.last, self.current + steps)
        return self.pages[self.current]


# --- try it ---
history = BrowserHistory("home")
history.visit("news")
history.visit("mail")
history.visit("maps")
print(history.back(2))              # -> news
history.visit("docs")               # mail and maps are no longer reachable
print(history.forward(1))           # -> docs
print(history.pages, history.last)  # -> ['home', 'news', 'docs', 'maps'] 2
print(history.back(5), history.forward(9))  # -> home docs
