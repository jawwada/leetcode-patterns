# Simplify Path
*LeetCode 71 · Medium · Pattern: Stack simulation · Reading time ~7 min*

## The problem

Convert an absolute Unix path to canonical form: a single leading '/', no trailing '/', no '.' components, '..'
resolved to the parent (a no-op at root) and consecutive slashes collapsed.

```text
Example: "/home//foo/" -> "/home/foo"; "/a/./b/../../c/" ->
  "/c"; "/../" -> "/".
```

## What the problem is really asking

You are given an absolute Unix path and must return its canonical form: one leading `/`, components separated by single slashes, no trailing slash, no `.` components, and every `..` resolved by removing the directory before it. A `..` at the root does nothing. Runs of slashes collapse. The answer is a string, the shortest path that names the same directory.

The tricky part is that `..` acts on the *result so far*, not on the raw text before it. In `/a/b/../../c` the second `..` cancels `a`, which is four characters back in the input, because `b` has already been cancelled.

```text
 input:   / a / . / b / . . / . . / c / / d /
 parts:     a   .   b   ..    ..    c  ""  d  ""
 effect:   in  -   in   up    up   in   -  in  -
 answer:  /c/d
```

## Do it by hand first

Treat the path as directions for walking a directory tree, starting at the root. Keep a finger on "where am I". `a`: go into a. `.`: stay. `b`: go into b. `..`: climb back to a. `..`: climb back to root. `c`: into c. Empty (from `//`): stay. `d`: into d.

```text
        /                 location after each step
        |                 a       -> /a
        a     c           .       -> /a
        |     |           b       -> /a/b
        b     d  <- end   ..      -> /a
                          ..      -> /
                          c       -> /c
                          d       -> /c/d
```

What your hand kept track of is the **chain of directories from the root to where you stand**. Going in appends to the end of that chain, and going up removes from the end. A list where you only touch the end is a stack.

## The first honest attempt

Split on `/`, throw away empty strings and `.`. Then, repeatedly: find the first `..`, delete it together with the component just before it (or only the `..` if it is first), and start scanning again from the beginning. Stop when no `..` remains.

```text
 pass 1:  [a, b, .., .., c, d]   .. at 2: delete b, ..
 pass 2:  [a, .., c, d]          rescan; .. at 1: delete a, ..
 pass 3:  [c, d]                 rescan from 0; none -> done
```

It is correct, but each deletion is O(k) list surgery plus a rescan from index 0. With many `..` that is O(k²) in the number of components. The repeated work is the prefix before the first `..`, which has already been checked and contains no `..`, yet it is rescanned on every pass.

```text
 pass 1:  a b [..] .. c d
 pass 2:  a [..] c d          <- 'a' rescanned
 pass 3:  c d                 <- (longer inputs: same prefix
                                  rescanned k times)
```

## The turning point

**A `..` always cancels the most recent component that is still alive. That is last-in-first-out, so a stack resolves every `..` in O(1) the moment it is read.**

Justification: when you reach a `..`, everything before it has already been resolved into a canonical chain with no `.` and no `..` in it. "Go up one level" from that chain means removing its last element. No other element can be affected, and nothing later can bring the removed one back. So one left-to-right pass suffices:

- part is `""` (from `//` or the leading or trailing slash) or `.`: skip it
- part is `..`: pop if the stack is non-empty, otherwise do nothing (you are at the root)
- anything else: push it. This includes `...`, `.hidden` and `..a`, which are ordinary names.

At the end, the stack *is* the path: `"/" + "/".join(stack)`. An empty stack gives `"/"`, which is exactly right.

Splitting on `/` is fine here because every component is consumed anyway, and Python's `split` keeps the empty pieces, which we simply skip. A scan with a `start` index, as in Implement Split, works just as well and avoids the list.

## Watch it work

`path = "/a/./b/../../c//d/"`. `split("/")` gives `["", "a", ".", "b", "..", "..", "c", "", "d", ""]`.

**Frame 1.** `""` is skipped. `a` is pushed. `.` is skipped.
```text
 parts: "" a . b .. .. c "" d ""
             ^
 stack: [a]
```

**Frame 2.** `b` is pushed.
```text
 parts: "" a . b .. .. c "" d ""
               ^
 stack: [a, b]
```

**Frame 3.** The first `..` pops `b`. The second `..` pops `a`.
```text
 parts: "" a . b .. .. c "" d ""
                    ^^ ^^
 stack: []                 back at the root
```

**Frame 4.** `c` is pushed, `""` is skipped, and `d` is pushed.
```text
 parts: "" a . b .. .. c "" d ""
                       ^    ^
 stack: [c, d]
```

**Frame 5.** The trailing `""` is skipped. Join the stack.
```text
 stack: [c, d]   ->   "/" + "c/d"   =   "/c/d"
```

In every frame the stack was the canonical path of the prefix read so far: no `.`, no `..`, no empties. Each component was pushed at most once and popped at most once.

## Why it is correct

Invariant: after processing parts `p[0..k]`, the stack, read bottom to top, is the canonical directory chain that the prefix path `p[0..k]` resolves to. It holds initially (empty stack is the root). Skipping `""` and `.` keeps it, because those do not move you. Pushing a name keeps it, because entering a child appends that child to the chain. For `..`, the parent of the current directory is the chain minus its last element. At the root the parent is the root itself, so a no-op pop is right. After the last part, the stack is the canonical chain of the whole path, and joining it with `/` behind a leading `/` is the canonical string by definition.

## Cost

- **Time O(n)**: `split` is one pass over n characters, and each component is pushed and popped at most once. The final join is O(n).
- **Space O(n)**: the parts list and the stack can each hold O(n) characters.
- The rescan approach is O(k²) in the number of components.

## Variations you will meet

- **Relative paths.** A leading `..` cannot be cancelled. Instead of dropping it at the bottom of the stack, push it, and only pop when the top is a real name. `a/../../b` becomes `../b`.
- **Change directory (`cd`) from a current working directory.** Seed the stack with the cwd's components and process the argument. If the argument starts with `/`, clear the stack first.
- **Symbolic links.** The stack model breaks: `..` after a symlink goes to the *target's* parent. Mention it as a real-world caveat. `os.path.normpath` is purely textual, while `realpath` resolves links.
- **Backspace String Compare (LeetCode 844).** `#` is a `..` that deletes one character. It is the same stack, or a right-to-left scan with a skip counter for O(1) space.

## What to carry forward

When a later token undoes "the most recent surviving thing", keep the survivors on a stack, and the stack at the end is the answer. The next problem uses the same stack, but stores **indices** of open parentheses instead of values, so that the unmatched characters can be found and cut out of the original string.
