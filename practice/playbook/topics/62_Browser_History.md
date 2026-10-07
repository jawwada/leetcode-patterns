## Browser History

Track the current page with an index and the valid forward range with a logical endpoint.

<!-- cell -->

Design Browser History splits the same way, with a bound in place of a deletion. `visit(url)` opens a page and clears the forward history, and `back(k)` and `forward(k)` move at most k pages and return the page they land on, each in O(1): from home, after visiting a and then b, `back(1)` is a and `forward(5)` is b.

One list holds the pages, a cursor marks the current one, and clearing the forward history only moves a logical end, `last = cur`. So `visit` overwrites the slot after the cursor, appending when the list ends there, `back(k)` is `max(0, cur - k)` and `forward(k)` is `min(last, cur + k)`: index arithmetic.

<!-- cell -->

### Runnable implementation

Adapted from [`design/design_browser_history.py`](../../design/design_browser_history.py).

<!-- cell -->

```python
import random

class BrowserHistory:
    def __init__(self, homepage: str):
        self.pages = [homepage]
        self.cur = 0        # index of the current page
        self.last = 0       # index of the newest reachable page (forward history ends here)

    def visit(self, url: str) -> None:
        self.cur += 1
        if self.cur == len(self.pages):
            self.pages.append(url)
        else:
            self.pages[self.cur] = url     # overwrite stale forward history in place
        self.last = self.cur

    def back(self, steps: int) -> str:
        self.cur = max(0, self.cur - steps)
        return self.pages[self.cur]

    def forward(self, steps: int) -> str:
        self.cur = min(self.last, self.cur + steps)
        return self.pages[self.cur]

h = BrowserHistory("home")
h.visit("a")
h.visit("b")
assert h.back(1) == "a"
h.visit("c")
assert h.forward(10) == "c"
assert h.back(10) == "home"
print(h.forward(1))  # a
```
