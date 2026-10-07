## Peeking Iterator

Preserve one prefetched value and a separate exhaustion flag. A real item may be None or zero, so its value must not determine whether iteration has ended.

<!-- cell -->

An iterator with lookahead closes the main path, because it is a design in miniature. Peeking Iterator (284) wraps an ordinary iterator and adds `peek()`, which shows the next item without consuming it, next to `next()` and `hasNext()`, all O(1): over `[1, 2, 3]`, `next()` is 1, `peek()` is 2, and the following `next()` is that same 2.

Keep the next item in a buffer, refilled by `next(self.it)` inside `try / except StopIteration`, plus a separate `done` flag. `hasNext()` returns `not self.done`: a test like `self.buffered is not None` fails when `None` is a real item, and `if self.buffered` fails on 0.

Flatten Nested List Iterator (341) runs `next()` and `hasNext()` over lists nested inside lists, `[[1, 1], 2, [1, 1]]` giving 1, 1, 2, 1, 1, and Zigzag Iterator (281) reads two lists alternately, `[1, 2]` and `[3, 4, 5, 6]` giving 1, 3, 2, 4, 5, 6. Both use the same buffer, and there `hasNext` does the work of finding the next real item.
