# Stacks

*16 problems · Reading time ~22 min*

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

## Advanced patterns

The sections above give you a stack, the pop-while loop, and the staircase picture. That is enough for the Mediums. The
Hard problems in this chapter ask for more: each pop has to *measure* something, the input is two-dimensional or
circular, a pop has to mean "delete" rather than "resolve", or the nesting carries real state. The seven patterns below
are the ideas that close that gap. Each one is small; what makes it advanced is knowing that it exists.

### 1. One pop, two walls

**When it shows up.** The answer for each element depends on how far it reaches on *both* sides before something
smaller (or larger) stops it: the widest rectangle a bar can anchor, the number of subarrays in which an element is the
minimum, how many days a price has been the highest.

**The intuition.** Keep an increasing stack of indices. When bar `t` is popped by the newcomer `i`, two facts are known
at once. The newcomer is `t`'s nearest strictly smaller bar on the right, because it is the first one that beat `t`.
The index now directly beneath `t` on the stack is its nearest smaller-or-equal bar on the left, because when `t` was
pushed it had just cleared away every taller bar to its left, and anything between them that was pushed later has been
popped since. So the pop hands you the whole open interval `(left, i)` in which `t` is the minimum: a rectangle of
height `h[t]` and width `i - left - 1`. The same two walls let you *count*: `t` is the minimum of exactly
`(t - left) * (i - t)` subarrays (pick a start in the left gap, an end in the right gap). Summing "value times count"
over all elements is the contribution technique. With duplicates, make one side strict and the other non-strict, or two
equal minimums will both claim the same subarray.

```text
 h = [2, 1, 5, 6, 2, 3]      newcomer: i=4, height 2

 6 |          #
 5 |       #  #
 4 |       #  #
 3 |       #  #     #
 2 | #     #  #  #  #
 1 | #  #  #  #  #  #
   +------------------
     0  1  2  3  4  5
 stack before (idx): 1 2 3     heights 1 5 6

 pop 3: walls (2, 4)  width 1  area 6 * 1 = 6
 pop 2: walls (1, 4)  width 2  area 5 * 2 = 10  <- best
 h[1] = 1 < 2: stop, push 4    stack: 1 4
```

```text
 contribution view, a = [3, 1, 2, 4]
 element 1 (idx 1): left wall -1, right wall 4
   starts 0..1 -> 2 choices, ends 1..3 -> 3 choices
   1 is the minimum of 2 * 3 = 6 subarrays
 sum of all subarray minimums
   = 3*1 + 1*6 + 2*2 + 4*1 = 17
```

**Where you'll use it.** Largest Rectangle in Histogram and Maximal Rectangle compute an area at every pop; Daily
Temperatures and Next Greater Element II use only the right wall. Beyond the chapter: Sum of Subarray Minimums (LeetCode
907) is the counting version, and Online Stock Span (901) is the left wall alone.

### 2. Sentinels: a wall at the bottom, a flush at the end

**When it shows up.** A pop needs "the element under me" even when the stack is about to empty, or elements left on the
stack after the scan still need their answer computed.

**The intuition.** Special cases are where stack bugs live, and two sentinels remove almost all of them. A *bottom
wall* (index `-1`) pretends there is a position just before the array that never gets popped, so the width formula
`i - stack[-1]` or `i - left - 1` works on every pop without an `if`. In Longest Valid Parentheses the wall has a real
meaning: it is the most recent position a valid run cannot cross, and a stray `)` *replaces* it, sliding the wall right.
An *end flush* (a height-0 bar appended to the histogram, or a `+` appended to an expression) is an input that beats
everything, so the leftovers are processed by the ordinary loop instead of a second cleanup loop with its own
off-by-one errors. Ask of every stack solution: "what does the bottom look like, and what happens to whatever is left at
the end?" If either answer is a special case, a sentinel probably removes it.

```text
 s = ") ( ) ( ) )"    stack starts as [-1] (the wall)

 i  c   action              stack      best
 0  )   only wall: replace  [0]        0
 1  (   push                [0, 1]     0
 2  )   pop, 2 - 0 = 2      [0]        2
 3  (   push                [0, 3]     2
 4  )   pop, 4 - 0 = 4      [0]        4
 5  )   only wall: replace  [5]        4
        ^ the wall slid from 0 to 5; nothing
          before index 5 can join a later run
```

**Where you'll use it.** Longest Valid Parentheses (the wall), Largest Rectangle in Histogram and Maximal Rectangle (the
height-0 flush), Basic Calculator and Basic Calculator II (scanning `s + "+"` to flush the last number). Beyond the
chapter: Maximum Subarray Min-Product (LeetCode 1856) is pattern 1 plus prefix sums, and a 0 flush keeps it to one loop.

### 3. Stacking rows into histograms

**When it shows up.** A binary matrix and a question about the largest (or the number of) all-ones rectangles.

**The intuition.** Every rectangle has a bottom row, so fix the bottom row and ask what the rectangles resting on it look
like. Above each cell of that row stands a tower of consecutive ones, and a rectangle of height `k` over columns
`c1..c2` is all ones exactly when every tower in that range is at least `k` tall. That is a histogram, word for word. The
towers update in O(cols) per row: a `1` grows its tower by one, a `0` knocks it to the ground. Then pattern 1 solves each
row's histogram in O(cols), so the whole matrix costs O(rows * cols) instead of the O(rows^2 * cols^2) or worse of trying
every rectangle. The general lesson: when a 2-D problem has a "bottom" (or a "right edge"), sweep it and carry a 1-D
summary that an already-solved problem can consume.

```text
 matrix          towers after each row     best on that row
 1 0 1 0 0       1 0 1 0 0                 1
 1 0 1 1 1       2 0 2 1 1                 3
 1 1 1 1 1       3 1 3 2 2  <- histogram   6  (height 2,
 1 0 0 1 0       4 0 0 3 0                 4   cols 2..4)

 row 2 as bars:  3 |#     #
                 2 |#     #  #  #
                 1 |#  #  #  #  #
                   +---------------
                    0  1  2  3  4
```

**Where you'll use it.** Maximal Rectangle is exactly this, reusing Largest Rectangle in Histogram once per row. Beyond
the chapter: Count Submatrices With All Ones (LeetCode 1504) carries the same towers but counts instead of maximising.

### 4. The stack as a greedy remover with a budget

**When it shows up.** "Keep `t` of these digits (or letters) in order to make the largest/smallest result", "remove `k`
digits", "lexicographically smallest subsequence".

**The intuition.** Up to now a pop *recorded an answer* for the popped element. Here a pop *deletes* it. Lexicographic
order is decided at the first position where two candidates differ, so earlier positions matter infinitely more than
later ones. If the top of the stack is `y`, a newcomer `x > y` arrives, and you can still afford a deletion, then
dropping `y` lets `x` slide into `y`'s position, and every candidate keeping `y` there loses at that position no matter
what follows. So pop while the top is smaller and the budget lasts, then push. The budget `d = len - t` is the only new
piece of state: when it hits zero, everything else is pushed unconditionally; if it is left over at the end, the tail
of the stack is cut. When two such greedy results must be interleaved, compare whole remaining *tails*, not just the
front digits, because a tie at the front is broken by what lies behind it.

```text
 best([9, 1, 2, 5, 8, 3], t = 3)     budget d = 6 - 3 = 3

 x   pops (top < x, d > 0)   stack        d
 9   -                       9            3
 1   -                       9 1          3
 2   1                       9 2          2
 5   2                       9 5          1
 8   5                       9 8          0
 3   - (budget spent)        9 8 3        0
                             result: 983
```

**Where you'll use it.** Create Maximum Number runs this on each array, then merges with tail comparison. Beyond the
chapter: Remove K Digits (LeetCode 402) is the smallest-number mirror image, and Remove Duplicate Letters (316) adds a
"can I still get this letter later?" check before each pop.

### 5. The context stack: push only what the outer level needs to resume

**When it shows up.** Nested groups where the inside must be finished before the outside can continue: `k[...]`
repetition, parenthesised arithmetic, nested function-like syntax.

**The intuition.** A `(` is a function call and a `)` is a return. On the call, push the caller's unfinished state; on
the return, pop it and combine. The skill is choosing the *smallest* state that suffices. Decode String must push the
text built so far and the repeat count, because the inner result is glued to one and multiplied by the other. Basic
Calculator, with only `+` and `-`, can push a single number: the flat sign of the group, because subtraction
distributes over the group and every term can go straight into one running total. Less state means fewer things to
restore and fewer bugs. Ask "when this group closes, what exactly does the outer level need from me, and what does it
need back?"

```text
 "1 - ( 2 - ( 3 + 4 ) )"   signs stack, top = flat sign
                           of the innermost open group
 read       res  sign  signs
 1 -        1    -1    [1]
 (          1    -1    [1, -1]
 2 -        -1   +1    [1, -1]
 (          -1   +1    [1, -1, +1]   <- 3 and 4 are seen
 3 +        2    +1    [1, -1, +1]      through two minus
 4 ) )      2    +1    [1]              lenses: net +1
                                        (4 still pending)
 end flush  6                        1 - (2 - 7) = 6
```

**Where you'll use it.** Decode String (text and count), Basic Calculator (one sign per group), and Basic Calculator II
as the one-level case where the stack holds signed terms. Beyond the chapter: Basic Calculator III (LeetCode 772)
combines precedence and parentheses by pushing the whole term stack as the context.

### 6. Collapse on close: a finished group becomes one token

**When it shows up.** Nested expressions whose operators take a variable number of operands, or any grammar where you
would rather not write a recursive parser.

**The intuition.** Push every meaningful token, including the `(` as a marker. On `)`, pop until the marker: the popped
items are exactly the operands of the group that just closed, because anything pushed after that `(` belongs to it and
every inner group has already been squashed to a single token by its own `)`. Pop the marker and the operator under it,
compute, and push the single result back. From then on the stack looks as if the whole group had been a literal value
all along, so the enclosing group needs no special handling. Each character is pushed once and popped at most once, so
the pass is O(n). Evaluate Reverse Polish Notation is the same move without markers: an operator collapses the top two
values into one.

```text
 "&(|(f,t),!(f))"      commas skipped, top at right

 after "&(|(f,t"     & ( | ( f t
 read ')'            pop t f, pop (, pop |  -> |{f,t} = t
 now                 & ( t
 after "!(f"         & ( t ! ( f
 read ')'            pop f, pop (, pop !    -> !f = t
 now                 & ( t t
 read ')'            pop t t, pop (, pop &  -> &{t} = t
 now                 t                         answer: true
```

**Where you'll use it.** Parsing a Boolean Expression, Evaluate Reverse Polish Notation (collapse two into one), and
Decode String if you push characters and collapse on `]`. Beyond the chapter: Number of Atoms (LeetCode 726) collapses
a group into counts and multiplies them by the number after `)`.

### 7. Circular arrays: walk twice, push once

**When it shows up.** "The array is circular", "the next element after the last is the first", and a next-greater or
next-smaller question.

**The intuition.** After one ordinary pass, the stack holds exactly the indices that found nothing bigger to their
right. Their only remaining hope is the wrap-around, the prefix of the array. So walk the indices a second time
(`i % n`) and run the same pop loop, but push nothing: every index has already had its turn to wait. One extra lap is
enough because the second lap offers every waiting index all the positions before it, which together with the first lap
covers the whole circle. The cost stays O(n): each index is still pushed once and popped at most once. Whatever is left
after both laps is the global maximum (and its equals), which truly has no answer.

```text
 a = [5, 4, 3, 6, 1]

 lap 1  idx: 0 1 2 3 4          lap 2 (pop only)
             5 4 3 6 1          idx: 0 ...
 6 pops 3, 4, 5                 5 > 1: pop idx 4, ans 5
 stack after lap 1:             6 > 5? no: stop
   idx 3 4  (values 6 1)        stack: idx 3 (value 6)

 answers: [6, 6, 6, -1, 5]      6 is the max: stays -1
```

**Where you'll use it.** Next Greater Element II. Beyond the chapter: the same "double the array, act only on the first
copy" view handles Maximum Sum Circular Subarray (LeetCode 918) with a monotonic deque.

## Signals in a problem statement

- Brackets, tags, "valid", "balanced", "nested", "matching" -> matching stack.
- An expression to evaluate, "without eval", postfix, operators with precedence, parentheses -> evaluation stack.
- "Next greater", "next smaller", "how many days until", "first element to the right/left that..." -> monotonic stack.
- "Largest rectangle", "span", "visible", bars or a histogram -> monotonic stack giving both boundaries.
- A binary matrix and "largest rectangle of 1s" -> stack the rows into histograms.
- "Circular array", "wraps around" with a next-greater question -> walk the indices twice, push on the first lap.
- "Sum over all subarrays of the minimum/maximum" -> both walls per element, then count contributions.
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

The order follows one thread: what does the stack hold, and what does a pop mean? First it holds brackets and a pop
means "matched". Then it holds values and a pop means "consumed by an operator". Then it holds waiters and a pop means
"answered". At the Hard end, a pop measures a width, or deletes a digit.

### Warm-up: brackets and summaries

**Valid Parentheses.** Three bracket types, and the only question is whether every closer finds the right partner. The
naive idea, counting each type, fails on `"([)]"`: the counts balance but the nesting crosses. That failure is the lesson:
a closer must match the *most recent* unclosed opener, and "most recent unfinished" is what a stack is for.

**Minimum Add to Make Parentheses Valid.** Now the string may be broken and you count the repairs. With one bracket type,
every entry on the stack is an identical `(`, so the stack carries no information except its height, and it collapses
to a counter. The new idea is that unmatched items are not errors to reject but the answer itself: stray `)`s seen when
the counter is zero, plus whatever `(`s are left at the end.

**Min Stack.** A stack that must also report its minimum in O(1). The puzzle is that popping the current minimum seems
to require a search for the next one. It does not, because a stack only changes at its top: store beside each entry the
minimum of everything at or below it, and that summary stays true until the entry itself leaves. This is the "frozen
middle" property of the chapter's opening, turned into a design trick.

### Values on the stack: evaluating expressions

**Evaluate Reverse Polish Notation.** The stack switches from holding brackets to holding numbers. Postfix has no
parentheses and no precedence, which looks like it should be hard to read, yet it is the easiest form to evaluate: each
operator takes the two most recent unconsumed values and pushes one result. The trap is operand order (`a - b` pops `b`
first) and Python's flooring division.

**Decode String.** `3[a2[c]]` nests, and the inner group must be finished before the outer one can be repeated. Here the
stack first holds real *context*: at `[` you save the text built so far and the repeat count, at `]` you restore them and
glue the inner result on. It is the recursion of a parser made visible, and the first use of the context stack
(advanced pattern 5).

**Asteroid Collision.** A row of asteroids moving left and right; collisions destroy the smaller one. The question a
curious person asks is how one left-mover can destroy several right-movers in a row without the scan going quadratic.
The answer is the chapter's first pop-while loop and its amortised argument: every asteroid is pushed once and destroyed
at most once.

**Basic Calculator II.** Infix with `+ - * /` and no parentheses. The tension is precedence: in `2 + 3 * 4` you cannot
add the 3 until you know whether a `*` follows. The fix is to act one step late: `+` and `-` push signed terms, while `*`
and `/` reach back and rewrite the top term. The answer is the sum of the stack, and the trailing number needs a flush.

**Basic Calculator.** Parentheses come back, but only `+` and `-` remain. One might expect to push whole partial
results per group; the observation is that a minus in front of a group simply flips the sign of everything inside. So
the stack shrinks to one sign per open group, and every number goes straight into one running total. It teaches you to
ask what is the *least* context that must be saved.

**Parsing a Boolean Expression.** Operators `&`, `|`, `!` with any number of operands, nested arbitrarily. Instead of
saving context and resuming, push every token and, on `)`, collapse back to the matching `(` into a single `t` or `f`
that sits where the group was. This is collapse on close (advanced pattern 6), the most general evaluator in the
chapter.

### Waiters on the stack: the monotonic stack

**Daily Temperatures.** For each day, how long until a warmer one? Brute force looks ahead from every day, O(n^2) on a
cooling stretch. Turn it around: a day waits on the stack until a warmer day arrives and resolves it. The waiters always
form a decreasing staircase, and store indices, not temperatures, because the answer is a distance.

**Next Greater Element II.** The same question on a circle. Concatenating the array to itself works but pushes
every index twice; the cleaner idea is to walk the indices twice and push only on the first lap, so the second lap is
pure resolution (advanced pattern 7). It teaches that the monotonic stack's leftovers are information, not garbage.

**Car Fleet.** Cars on a one-lane road cannot pass, so a fast car catches a slow one and they merge. Simulating time is
the trap. Sort by position, compute each car's solo arrival time, and sweep from the car nearest the target: a car that
would arrive no later than the fleet ahead is absorbed. The stack of fleet times is monotone, and the new idea is that
sorting by one key can create the order a monotonic stack needs.

### The Hard end: pops that measure, rows that stack, pops that delete

**Longest Valid Parentheses.** Back to brackets, but now you need the length of the longest valid run, and valid runs
can sit side by side (`()()`) or nest (`(())`). Pushing brackets is not enough; push *indices*, with a `-1` wall at the
bottom, and every pop turns into a length: `i - stack[-1]`. A stray `)` becomes the new wall. This is the sentinel
pattern (advanced pattern 2), and the bridge from matching to measuring.

**Largest Rectangle in Histogram.** Every bar wants to know how far it can stretch left and right at its own height.
Two scans for previous and next smaller would work; the deeper idea is that one increasing stack gives *both* walls in a
single pop (advanced pattern 1), with a height-0 flush at the end. This is the chapter's centrepiece.

**Maximal Rectangle.** The largest all-ones rectangle in a binary matrix sounds like a new, two-dimensional problem. It
is not: fix the bottom row, read the column towers as a histogram, and run the previous problem once per row (advanced
pattern 3). The lesson is reduction: recognise a solved problem inside a harder one.

**Create Maximum Number.** Pick `k` digits from two arrays, keeping each array's order, to form the largest number. It
splits into three greedy pieces: try every split of `k`, take the best subsequence from each array with a monotonic
stack that pops to *delete* within a budget (advanced pattern 4), then merge by comparing whole tails. It is the last
problem because it asks you to see the familiar staircase used for a completely different purpose.
