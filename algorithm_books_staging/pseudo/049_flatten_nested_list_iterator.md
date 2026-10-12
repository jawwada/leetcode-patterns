---
rank: 49
slug: flatten_nested_list_iterator
---

Design an iterator over a nested list, in which every item is either an integer or another nested list: `next()` returns the next integer from left to right, and `has_next()` says whether any integer is left. Plain Python lists stand in for LeetCode's `NestedInteger`, so "the item is a list" plays the part of `not item.isInteger()`. For `[1, [4, [6]], [], 8]` the calls to `next()` return 1, 4, 6 and 8, and then `has_next()` is false.

The easy answer flattens everything up front with a recursive walk and serves the values from a list, which stores every integer and walks the whole input before the first call, even if the caller stops after one value. A lazy iterator pauses that walk between calls instead, and what a paused walk must remember is its place in every list it is inside, one position per level. Keep those places as a stack of frames `[list, index]`, the outermost list at the bottom, where `index` is the next item of that list still to visit. The stack is exactly the call stack the recursive walk would hold, made explicit so that it can stop and resume.

`has_next()` does all the work: it moves the top frame forward until the frame points at an integer. If the top frame has run off the end of its list, that list is used up, so pop it and carry on with the frame below. If it points at a sub-list, step the frame past the sub-list first and only then push a new frame for it, so that the parent resumes at the right item once the child is done. If it points at an integer, stop. Empty lists are entered and popped by the same loop, so they never surface. `next()` calls `has_next()` to settle on an integer, reads it and steps past it.

```text
A = [1, B, D, 8]   B = [4, C]   C = [6]   D = []    a frame is (list, index)
call        returns  stack, top at right   steps inside has_next
start                (A, 0)
next()      1        (A, 1)
has_next()  true     (A, 2) (B, 0)         enter B
next()      4        (A, 2) (B, 1)
next()      6        (A, 2) (B, 2) (C, 1)  enter C
next()      8        (A, 4)                pop C, pop B, enter D, pop D
has_next()  false    empty                 pop A
next() runs has_next() first, then returns the integer on top and steps on
```

```pseudo
CLASS NestedIterator
    FUNCTION Init(nested)
        self.stack ← empty stack
        self.stack.push([nested, 0])      // frame: a list and its next index

    FUNCTION HasNext()
        WHILE len(self.stack) > 0
            frame ← self.stack.top()
            items ← frame[0]
            index ← frame[1]
            IF index = len(items)
                self.stack.pop()          // this list is used up
            ELSE IF items[index] is a list
                frame[1] ← index + 1      // step past the sub-list first
                self.stack.push([items[index], 0])    // then enter it
            ELSE
                RETURN true               // the top points at an integer
        RETURN false

    FUNCTION Next()
        self.HasNext()
        frame ← self.stack.top()
        value ← frame[0][frame[1]]
        frame[1] ← frame[1] + 1
        RETURN value
```

Each list is pushed once and popped once and each integer is returned once, so draining the iterator costs `O(N + L)` for `N` integers and `L` lists, `O(1)` amortized per call unless the lists far outnumber the integers, and the stack holds one frame per level of nesting, `O(depth)` memory. It is the pause-and-resume trick of the BST iterator (#77) and the frames of Decode String (#25). Signals: "design an iterator", "lazy", "flatten", or an input too large to copy or too deep to recurse. Two cousins come up as follow-ups. Peeking Iterator (LC 284) caches one value, so that `peek()` can show the next element without consuming it, and Zigzag Iterator (LC 281) keeps a queue of iterators, takes one value from the front one and rotates it to the back until it runs dry. The classic mistake is a `has_next()` that only checks that the stack is not empty: for `[[], [[]]]` it promises an integer that does not exist. The other is pushing the child frame without first stepping the parent past it; on the example the iterator then returns 1, 4 and 6, and 6 again forever, because every time `C` is used up its parent still points at it.

*Practice:* LC 341 Flatten Nested List Iterator · LC 284 Peeking Iterator · LC 281 Zigzag Iterator · LC 173 Binary Search Tree Iterator
