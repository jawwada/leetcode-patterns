# Design Browser History

*LeetCode 1472 · Medium · Pattern: Array with current pointer and logical end · Reading time ~7 min*

## The problem

Implement BrowserHistory(homepage): visit(url) opens url and clears all forward history; back(steps) moves back at
most steps pages and returns the current url; forward(steps) moves forward at most steps pages, never past the newest
page, and returns the current url.

```text
Example: home leetcode; visit google, facebook, youtube; back(1)
  -> facebook; back(1) -> google; forward(1) -> facebook; visit
  linkedin; forward(2) -> linkedin; back(2) -> google; back(7)
  -> leetcode.
```

## What the problem is really asking

Model one browser tab. It starts on a homepage. `visit(url)` opens a new page *and throws away all forward history*. `back(steps)` moves back up to `steps` pages (stopping at the homepage) and returns the current URL. `forward(steps)` moves forward up to `steps` pages (stopping at the newest page still reachable) and returns the current URL.

The answer to each call is a URL; the state is the history line and where you stand on it. The tricky rule is the one about visits: after you go back and then visit something new, the pages you had gone back over are gone for good, even though you visited them.

```text
 history:  lc -> g -> f -> y        you are at y
 back(2):  lc -> g -> f -> y        you are at g
                ^
 visit(x): lc -> g -> x             f and y are erased
                     ^
```

## Do it by hand first

On paper, write the pages in a row and put your finger under the current one. `back(2)` moves the finger two cells left. `forward(1)` moves it one cell right. Neither changes the row.

`visit(x)` from g: write x in the cell right after your finger. What about the old cells after it? You could erase them — or you could draw a vertical bar after x meaning "the row ends here", and simply never let your finger move past the bar. The leftover ink beyond the bar is invisible to every future operation.

```text
 cells:  lc | g | x | y         y is leftover ink
              finger -^  |
                      end bar
```

Your hand tracked three things: the row of pages, the finger position, and where the bar is. That is an array, a current index `cur` and a logical end `last`.

## The first honest attempt

Two stacks, the way many people first think of back/forward: `back_stack` holds the pages behind you, `forward_stack` the pages ahead, and `current` the page you are on.

- `back(steps)`: repeat up to `steps` times: push `current` onto forward, pop back into `current`.
- `forward(steps)`: the mirror image.
- `visit(url)`: push `current` onto back, set `current = url`, and clear the forward stack.

It is correct. `back` and `forward` cost O(steps); clearing the forward stack element by element costs O(size of forward history).

```text
 back(3): pages move one at a time between stacks
  back: [lc, g, f]  cur: y   fwd: []
  back: [lc, g]     cur: f   fwd: [y]
  back: [lc]        cur: g   fwd: [y, f]
  back: []          cur: lc  fwd: [y, f, g]
 3 pops + 3 pushes to answer "where is 3 to the left?"
```

The waste: shuffling pages one by one to reach a destination that is a single subtraction away, and physically deleting forward pages that only need to become unreachable.

## The turning point

**Claim: history is a single line, so every navigation is arithmetic on an index, and "clear the forward history" is just moving the end of the line.**

Justification: at any moment the reachable pages form a contiguous sequence from the homepage to the newest visit, and the current page is one position in it. `back(steps)` lands on position `max(0, cur - steps)` — clamp because you cannot go before the homepage. `forward(steps)` lands on `min(last, cur + steps)` — clamp because you cannot go past the newest reachable page. Neither needs to touch any page except the destination.

For `visit`, the new page goes right after the current one, at `cur + 1`. Everything after that position becomes unreachable. Instead of deleting it, set `last = cur + 1`. If `cur + 1` is past the physical end of the array, append; otherwise overwrite the stale slot that is there. Any stale slots beyond `last` are never read, because `forward` clamps to `last`, not to the array's length.

This is a pattern you will see again: **turn a deletion into a bound**. Data you would have to remove one by one is instead declared dead by moving a single index, and is overwritten later when that space is reused. The tracker remembers the page array plus two integers; it forgets nothing eagerly, and pays for that with a few stale strings in memory.

```text
 back:    cur = max(0, cur - steps)
 forward: cur = min(last, cur + steps)
 visit:   cur += 1; write pages[cur]; last = cur
```

## Watch it work

Homepage `lc`; then visit g, f, y; back(2); forward(1); visit li; back(2); visit x; forward(5); back(7).

```text
Frame 1  visit g, f, y
 idx:    0    1   2   3
 pages: [lc] [g] [f] [y]
                      ^cur=3   last=3
```
Each visit appended because cur + 1 equalled the array length.

```text
Frame 2  back(2) -> g ; forward(1) -> f
 pages: [lc] [g] [f] [y]
          back: cur = max(0, 3-2) = 1  (g)
          fwd:  cur = min(3, 1+1) = 2  (f)
                  ^cur=2   last=3
```
Two jumps, each one line of arithmetic; the array is untouched.

```text
Frame 3  visit(li)
 pages: [lc] [g] [f] [li]
                      ^cur=3   last=3
```
cur + 1 = 3 already exists, so y is overwritten by li, and last = 3.

```text
Frame 4  back(2) -> g
 pages: [lc] [g] [f] [li]
              ^cur=1          last=3
```
f and li are still reachable going forward, since last = 3.

```text
Frame 5  visit(x)
 pages: [lc] [g] [x] [li]
                  ^cur=2  last=2
                       |li| is now stale
```
x overwrites slot 2 and last drops to 2; li remains in memory but beyond the bar.

```text
Frame 6  forward(5) -> x ; back(7) -> lc
 fwd:  cur = min(2, 2+5) = 2   (x, not li)
 back: cur = max(0, 2-7) = 0   (lc)
 pages: [lc] [g] [x] [li]
         ^cur=0       last=2
```
Forward clamps at last, so the stale li is never returned.

Across frames, `0 <= cur <= last < len(pages)` always holds, and `pages[0..last]` is exactly the reachable history.

## Why it is correct

Invariant: `pages[0..last]` is the current reachable history in order, and `cur` indexes the current page within it. Initially both are 0 with only the homepage. `back` and `forward` move `cur` within `[0, last]`, which is exactly the "at most steps, never beyond the ends" rule. `visit` writes the new page at `cur + 1` and sets `last` to that index, so the reachable history becomes the old prefix up to the current page followed by the new page — precisely the browser rule that forward history is discarded. Slots beyond `last` may hold stale strings, but no operation reads past `last`, so they never influence an answer.

## Cost

- **Time:** O(1) per operation — a clamp and an index, or one write.
- **Space:** O(number of pages visited) at worst; stale slots are reused by later visits.

The two-stack version is O(steps) per navigation and O(forward history) per visit, because it moves and deletes pages one at a time.

## Variations you will meet

- **Doubly linked list version.** Each page is a node; back/forward walk pointers (O(steps)); visit cuts the `next` link (O(1)). Natural if the interviewer says "steps is always 1".
- **Memory-bounded history (keep only the last N pages).** Use a ring buffer of N slots: indices modulo N, with a separate count of how far back is valid. The "end as a bound" idea carries over unchanged.
- **Undo/redo in an editor.** Same structure: undo is back(1), redo is forward(1), and a new edit truncates the redo history — moving `last`.
- **History across tabs, or "go to the most visited page".** Now you need per-page counters in a hash map, and maybe a heap; the array alone stops being enough.

## What to carry forward

A linear history is an array plus a cursor; jumps are clamped arithmetic, and clearing a suffix is moving a logical end instead of deleting. The next problem keeps two pieces of state with very different lifetimes — open journeys and lifelong route statistics — in two hash maps.
