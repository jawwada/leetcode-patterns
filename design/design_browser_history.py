"""
Design Browser History (LeetCode 1472)  — Medium
Pattern: Array with current pointer and logical end

Problem
-------
Implement BrowserHistory(homepage): visit(url) opens url and clears all forward history;
back(steps) moves back at most steps pages and returns the current url; forward(steps) moves
forward at most steps pages (never past the newest page) and returns the current url.
Example: home "leetcode.com"; visit google, facebook, youtube; back(1)->facebook; back(1)->google;
forward(1)->facebook; visit linkedin; forward(2)->linkedin; back(2)->google; back(7)->leetcode.

Brute force
-----------
Two stacks: back_stack holds pages behind the current one, forward_stack holds pages ahead.
back(steps) pops the back stack one page at a time (pushing onto forward), forward(steps) does
the reverse, and visit empties the forward stack element by element. O(steps) per back/forward
and O(forward history) per visit. The wasted work is moving pages one at a time when the
destination index is a simple subtraction, and physically deleting forward pages when they
could just be ignored.

From brute force to optimal
---------------------------
History is linear, so model it as an array with an integer cursor: back(steps) is
cur = max(0, cur - steps), forward is cur = min(end, cur + steps), both O(1). Clearing forward
history is also O(1) if we don't delete anything: keep a logical end index `last`; visit writes
at cur + 1 (overwriting a stale slot or appending) and sets last = cur. Slots beyond last are
garbage and unreachable because forward clamps to last. The tracker remembers the page array,
cur and last; it forgets nothing eagerly, trading a few stale strings for O(1) everything.

Intuition
---------
A browser tab's history is a single line of pages; where you are is an index on that line.
Jumping several steps is arithmetic on the index, not a walk. "Clearing forward history"
means "the line now ends here", which is a bound, not a deletion.

Geometric view
--------------
pages: [ leetcode, google, facebook, youtube ]   cur=3 last=3
back(2):                 cur=1 ------------------^-> ^           returns google
visit(linkedin): write at index 2, last=2
pages: [ leetcode, google, linkedin, youtube ]   cur=2 last=2   (youtube is unreachable)
forward(5): min(last, 7) = 2 -> stays on linkedin.

Steps
-----
1. pages = [homepage]; cur = 0; last = 0.
2. visit: cur += 1; if cur == len(pages) append else overwrite pages[cur]; last = cur.
3. back: cur = max(0, cur - steps); return pages[cur].
4. forward: cur = min(last, cur + steps); return pages[cur].

Complexity: O(1) time per operation, O(pages visited) space — index arithmetic only.
Pitfalls: forward clamping to len(pages) instead of last (resurrects cleared pages); forgetting
          to update last on visit; back below 0.
"""
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


class BruteForce:
    """Two stacks; every step is one pop/push and visit discards forward pages one by one."""

    def __init__(self, homepage: str):
        self.back_stack = []
        self.forward_stack = []
        self.current = homepage

    def visit(self, url: str) -> None:
        self.back_stack.append(self.current)
        self.current = url
        while self.forward_stack:            # O(forward history)
            self.forward_stack.pop()

    def back(self, steps: int) -> str:
        while steps and self.back_stack:     # O(steps)
            self.forward_stack.append(self.current)
            self.current = self.back_stack.pop()
            steps -= 1
        return self.current

    def forward(self, steps: int) -> str:
        while steps and self.forward_stack:
            self.back_stack.append(self.current)
            self.current = self.forward_stack.pop()
            steps -= 1
        return self.current


if __name__ == "__main__":
    b = BrowserHistory("leetcode.com")
    b.visit("google.com")
    b.visit("facebook.com")
    b.visit("youtube.com")
    assert b.back(1) == "facebook.com"
    assert b.back(1) == "google.com"
    assert b.forward(1) == "facebook.com"
    b.visit("linkedin.com")
    assert b.forward(2) == "linkedin.com"
    assert b.back(2) == "google.com"
    assert b.back(7) == "leetcode.com"

    e = BrowserHistory("home")               # edge: forward with no forward history, back on homepage
    assert e.forward(3) == "home" and e.back(3) == "home"

    random.seed(8)
    fast, slow = BrowserHistory("h"), BruteForce("h")
    for i in range(2000):
        r = random.random()
        if r < 0.4:
            fast.visit(f"p{i}")
            slow.visit(f"p{i}")
        elif r < 0.7:
            k = random.randint(1, 5)
            assert fast.back(k) == slow.back(k)
        else:
            k = random.randint(1, 5)
            assert fast.forward(k) == slow.forward(k)
    print("ok")
