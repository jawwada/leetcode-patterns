# Stacks

*16 problems · Reading time ~14 min*

## Why this chapter exists

A stack answers one question better than anything else: "what is the most recent thing that is still unfinished?" That
question hides inside a surprising number of problems. A closing bracket wants the most recent unclosed opener. An
operator in postfix wants the two most recent unused numbers. A warm day wants every earlier day that is still waiting
for something warmer, nearest first. Each time, the answer lives at the top of a pile, and once it is used it leaves.

The sixteen problems in this chapter fall into three families:

- **Matching and nesting.** Something opens, something later closes it, and closings pair with the most recent opening
  (valid parentheses, minimum add to make valid, decode string, longest valid parentheses).
- **Evaluation.** An expression is read left to right, and the stack holds the partial results that cannot be combined yet
  because their right-hand side has not arrived (reverse Polish notation, the two basic calculators, the boolean parser,
  and min stack, which keeps a running summary beside each element).
- **Monotonic stack.** Each element waits for the first later element that beats it; the waiters are kept in sorted order
  so a newcomer can settle many of them at once (asteroid collision as a warm-up, daily temperatures, next greater element
  II, car fleet, largest rectangle in histogram, maximal rectangle, create maximum number).

## What it is

A stack is a list you only touch at one end. You put things on top (push), you look at the top (peek), and you take the
top off (pop). Nothing in the middle is ever read or changed. That is the whole contract, and the restriction is the
point: because the middle is frozen, anything you computed about it stays true.

Draw it as a column, bottom at the floor, top at the ceiling. Pushing 4, then 7, then 2:

```text
  push 4        push 7        push 2        pop -> 2
                              +---+
                              | 2 | <- top
                +---+         +---+         +---+
                | 7 | <- top  | 7 |         | 7 | <- top
  +---+         +---+         +---+         +---+
  | 4 | <- top  | 4 |         | 4 |         | 4 |
  +---+         +---+         +---+         +---+
  floor         floor         floor         floor
```

Last in, first out (LIFO). The 2 arrived last and left first. The 4 arrived first and will leave last.

In memory, a Python stack is just a dynamic array lying on its side. The "top" is the last index, so push is `append` and
pop is `pop()`, both at the right end where no shifting is needed:

```text
index    0   1   2   3   4   5   6   7
       +---+---+---+---+---+---+---+---+
list   | 4 | 7 | 2 |   |   |   |   |   |   capacity 8
       +---+---+---+---+---+---+---+---+
                 ^
                 top = len - 1 = 2
       spare slots to the right make append O(1) amortised
```

**The stack as "the nearest unresolved thing".** Here is the idea that makes the whole chapter click. When you scan
input left to right, some items cannot be dealt with when you first see them. A `(` cannot be judged until its `)`
shows up. A temperature cannot be answered until a warmer one arrives. Those items are *unresolved*, and you park them.
Which parked item does the next arrival concern? Almost always the most recently parked one, because nesting and
"nearest" both point backwards to the closest unresolved item. A stack hands you exactly that one, at the top, in O(1).

```text
input:   (   [   {   }   ]   )
         |   |   |   ^ cursor: a closer
         |   |   +-- nearest unresolved -> top
         |   +------ waiting
         +---------- waiting longest -> bottom
```

**The call stack is a stack.** Every time a function calls another function, the computer pushes a frame holding the
caller's local variables and where to resume. When the callee returns, its frame is popped and the caller picks up
where it stopped. So recursion is a stack you did not have to write:

```text
decode("3[a2[c]]")             call stack (top at top)
  sees "3[" -> recurse         +----------------------+
    sees "a2[" -> recurse      | inner: build "c"     | <- top
      builds "c", returns      +----------------------+
    "a" + "c"*2 = "acc"        | mid: have "a", x2    |
  "acc"*3                      +----------------------+
                               | outer: have "", x3   |
                               +----------------------+
```

Any recursive parser can be turned into a loop with an explicit stack that holds the same frames. You do this for two
reasons: Python's recursion limit (about 1000 frames) will crash deep inputs, and an explicit stack lets you see and
store only the part of the frame you actually need. Decode string, the basic calculator and the boolean parser are all
"recursion, unrolled".

## Operations and what they cost

| Operation | Time | Why |
|---|---|---|
| push | O(1) amortised | append at the end; the array occasionally doubles |
| pop | O(1) | remove the last slot, nothing shifts |
| peek (top) | O(1) | read index `len - 1` |
| is empty | O(1) | check the length |
| search for a value | O(n) | not a stack operation; if you need it, you want another structure |
| pop k items | O(k) | each pop is O(1); see the amortised argument below |

The one non-trivial operation is the **pop-while loop**, the engine of every monotonic stack. A new item arrives and
pops everything on top that it "beats", then sits down:

```text
before: stack (values)        new item 4 arrives
  +---+
  | 1 | <- top   1 < 4 pop
  +---+
  | 3 |          3 < 4 pop
  +---+
  | 5 |          5 > 4 stop
  +---+

after:
  +---+
  | 4 | <- top   (4 pushed)
  +---+
  | 5 |
  +---+
```

That single arrival did two pops. Is the scan then O(n^2)? No, and this argument is worth memorising because every
monotonic-stack problem leans on it:

**Each element is pushed exactly once and popped at most once.** So over the whole scan there are at most n pushes and
at most n pops: 2n operations, O(n) total, no matter how the pops are spread out. One arrival may pop many, but those
many were each pushed earlier and will never be popped again. Think of each element carrying one coin for its push and
one coin for its pop; the total bill cannot exceed 2n coins.

```text
a = [5, 3, 1, 4, 2, 6]        (pop anything smaller)

i  item  pops        stack after (bottom -> top)
0   5    -           5
1   3    -           5 3
2   1    -           5 3 1
3   4    1, 3        5 4
4   2    -           5 4 2
5   6    2, 4, 5     6
                     pushes 6, pops 5  -> 11 ops
```

## The invariant

Every stack algorithm protects some statement about what is on the stack. In matching problems: "the stack holds exactly
the openers that are not yet closed, in the order they were opened". In the monotonic family, the statement is about
order: "the values from bottom to top are strictly decreasing" (or increasing, depending on the problem). The pop-while
loop exists only to restore that statement before each push.

A legal state for a decreasing stack, and an illegal one:

```text
  LEGAL (decreasing up)       ILLEGAL
  +---+                       +---+
  | 2 | <- top                | 6 | <- top  6 > 4 below it
  +---+                       +---+
  | 4 |                       | 4 |   4 never learned that
  +---+                       +---+   6 was its answer
  | 5 |                       | 5 |
  +---+                       +---+
```

The illegal state means some element is sitting *under* a bigger later element without having been resolved. That is
exactly the information the algorithm promised to record, so an illegal state is always a bug: you pushed without
running the pop-while loop first.

## How to picture it

For matching problems, picture a mountain path: each opener steps up one level, each closer steps down. The stack is the
list of steps you took to reach your current height. A valid string starts and ends at sea level and never dips below it.

```text
 height after each char (stack size = altitude)

  3 |              *
  2 |     *     *     *
  1 |  *     *           *
  0 +-----------------------*-- sea level
       (  [  ]  (  {  }  )  )
```

For the monotonic family, picture a **skyline seen from the right**, a staircase. The stack holds the bars that are
still visible: each one is shorter than the one behind it, so they form steps going down toward the cursor. A tall new
bar knocks down every shorter step in front of it, and those knocked-down bars have just found their "next greater".

```text
 a = [5, 3, 1, 4, 2, 6], cursor at i=3 (value 4)

 5 |#                      5 |#
 4 |#                      4 |#        #
 3 |#  #                   3 |#  .     #
 2 |#  #                   2 |#  .     #
 1 |#  #  #                1 |#  .  .  #
   +---------                +------------
    0  1  2                   0  1  2  3
 stack: 5 3 1              stack: 5 4
 (before 4 arrives)        (3 and 1 popped: their
                            next greater is 4)
```

The staircase always descends toward the cursor. Whatever is popped is resolved forever; whatever remains is still
waiting, and the nearest waiter is the top.

## Signals in a problem statement

- Brackets, tags, "valid", "balanced", "nested", "matching" -> matching stack.
- An expression to evaluate, "without eval", postfix, operators with precedence, parentheses -> evaluation stack.
- "Next greater", "next smaller", "how many days until", "first element to the right/left that..." -> monotonic stack.
- "Largest rectangle", "span", "visible", bars or a histogram -> monotonic stack giving both boundaries.
- "Remove k digits to make the smallest/largest number", "lexicographically smallest subsequence" -> monotonic stack with
  a deletion budget.
- Collisions or cancellations between neighbours ("adjacent equal letters vanish") -> simulation stack.
- "Undo", "back", "most recent" -> plain stack.
- A recursive grammar where recursion depth could reach 10^4 or more -> explicit stack instead of recursion.

Counter-signals:

- "Oldest first", "first come first served", level-by-level -> queue or deque, not a stack.
- "Maximum of every window of size k" -> monotonic *deque*, because elements also expire from the old end.
- "k-th largest", repeated "smallest so far" with arbitrary deletions -> heap.
- Next greater in a *sorted* structure with updates -> balanced tree or binary search, not a scan.

## Python toolbox

A list is the stack. Never use `insert(0, x)` or `pop(0)`; those shift everything.

```python
stack = []
stack.append(x)          # push
top = stack[-1]          # peek (IndexError if empty)
x = stack.pop()          # pop
if stack: ...            # non-empty test
```

The pop-while loop, with indices (store indices, not values, whenever you need distances or widths):

```python
ans = [-1] * n
st = []                          # indices, values decreasing
for i, x in enumerate(a):
    while st and a[st[-1]] < x:
        ans[st.pop()] = x        # x resolves the waiter
    st.append(i)
```

Small things that bite:

```python
int(-7 / 2)    # -3  truncate toward zero (what C/Java do)
-7 // 2        # -4  Python floors: wrong for these problems
"-3".isdigit() # False: negative tokens need care
sys.setrecursionlimit(10**6)  # if you insist on recursion
```

`collections.deque` also works as a stack (`append`/`pop`) and is the tool when you need both ends.

## Mistakes people make

1. Popping from an empty stack on a stray closer like `"]"`. Fix: check `if not stack` before every pop.
2. Returning True as soon as the scan ends, with openers left over (`"(("`). Fix: the answer is `not stack`.
3. Storing values when you later need positions or widths. Fix: push indices and look values up.
4. Pushing before running the pop-while loop, breaking the monotone order. Fix: pop first, then push, always.
5. Using `<` where duplicates need `<=` (or the reverse), so equal elements resolve each other wrongly. Fix: decide on
   paper what an equal value should do and write the comparison to match.
6. Operand order in evaluation: for `a - b` the first pop is `b`. Fix: `b = pop(); a = pop()`.
7. Python's `//` floors negatives. Fix: `int(a / b)` for truncation toward zero.
8. Forgetting to flush the last pending number at the end of a string expression. Fix: append a sentinel operator or
   handle `i == len(s) - 1`.
9. Leaving elements on a monotonic stack after the scan and forgetting they need a default answer (or a final sweep).
   Fix: initialise answers to the default, or push a sentinel that pops everything.
10. Multi-digit numbers read one digit at a time. Fix: `num = num * 10 + d` and only act when the number ends.

## The journey ahead

1. **Valid parentheses** - the purest stack: openers wait, a closer must match the top.
2. **Minimum add to make parentheses valid** - with one bracket type the stack collapses to a counter, and unmatched
   items become the answer.
3. **Min stack** - a stack only changes at the top, so a summary stored beside each element stays valid forever.
4. **Evaluate reverse Polish notation** - the stack holds values instead of brackets; an operator consumes the top two.
5. **Decode string** - nesting with real context to save: each `[` pushes a frame, each `]` resumes the outer one; this
   is recursion made explicit.
6. **Asteroid collision** - a newcomer fights the top repeatedly; the first pop-while loop of the chapter.
7. **Basic calculator II** - infix with precedence: `*` and `/` reach back one term, `+` and `-` are deferred on the stack.
8. **Basic calculator** - parentheses with only `+` and `-`: the stack holds the sign each group inherits.
9. **Parsing a boolean expression** - a general nested evaluator: push everything, collapse back to `(` on each `)`.
10. **Daily temperatures** - the monotonic stack in its plainest form: waiters resolved by a warmer day.
11. **Next greater element II** - the same stack on a circular array, solved by walking it twice.
12. **Car fleet** - sort first, then a monotone stack of arrival times where a slower car ahead absorbs faster ones.
13. **Longest valid parentheses** - matching meets measuring: a stack of indices with a barrier gives run lengths.
14. **Largest rectangle in histogram** - each pop reveals both walls of a rectangle: the staircase used to its fullest.
15. **Maximal rectangle** - turn each matrix row into a histogram and reuse problem 14.
16. **Create maximum number** - a monotonic stack with a deletion budget picks the best subsequence, then a greedy merge.
