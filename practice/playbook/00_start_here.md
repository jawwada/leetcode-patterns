**From idea to implementation.** Most interview failures are not "I had no idea". They are "I had the idea and could not turn it into code in 25 minutes". This playbook is about that gap. Every technique is taught the same way: the picture, then the **seven decisions** that turn the idea into lines of code, then the traps, edge cases and variations, and finally a map of every problem in this repo that uses it.

The playbook is split into twelve notebooks, one per family of techniques; the full list closes this section, under *The notebooks*. This first notebook holds the method; the last one holds the interview-day checklists and the A-Z finder for every problem.

<!-- cell -->

## Start Here

### How to read a section

Every technique section has the same shape, so you always know where to look:

| Part | What it gives you |
|---|---|
| **Reach for it when** | the words in a problem statement that should make you think of this technique |
| **The picture** | what the data looks like and how the algorithm moves over it; why it beats brute force |
| **From idea to code** | the idea in one sentence, the seven decisions, an "in words → in code" table, a tagged template |
| **Try it** | after every code cell: 3–4 small experiments that break one line on purpose or feed a tricky input |
| **Watch it work** | a trace that prints the state step by step |
| **Where it goes wrong** | the implementation traps, each with a tiny failing input and its fix |
| **Edge cases** | the inputs to say out loud, as runnable asserts |
| **Variations** | what changes from the template for each family of problems |
| **Say it in the interview** | a short script: brute force → waste → optimal → complexity, plus likely follow-ups |
| **Problem map** | every repo problem that uses the technique, with its one key insight |
| **Self-check** | questions with hidden answers |

**How to study a section (60–90 minutes).** Run each cell. Do its Try-it bullets as *predict → run → explain → undo*: say what will happen before you run it. Answer each Self-check question before opening it. Then close the notebook and type the template from its seven decisions in a plain editor (no autocomplete, no running), and only then run it. The decision where you stalled is the one to reread.

Start with **[From Idea to Code](#s01)**: it is the method every other section applies.

### The interview loop (45 minutes)

```text
 1. Understand   (3-5 min)   restate; ask size, ranges, duplicates, negatives, empty input,
                             sortedness, output format (sizes are often NOT given: ask, or
                             say "I'll assume n up to about 10^5"); 2-3 tiny examples, one an edge case
 2. Match        (1-2 min)   size -> target complexity; clues -> technique
 3. Brute force  (1-2 min)   say it and its cost; point at the work it repeats
 4. Plan         (3-5 min)   the seven decisions as 4-6 comment lines + target complexity;
                             ask "Does this sound right? Shall I code it?"
 5. Implement    (10-15 min) skeleton first, then fill in; narrate as you go
 6. Test         (5 min)     you usually cannot run the code: trace a tiny input by hand
                             with a state table, then walk the edge cases
 7. Follow-up    (the rest)  aim to be here by about minute 30; most interviewers keep a
                             second part ("a stream?", "k is huge?", "it doesn't fit in memory?")
```

Two habits matter more than speed: **say the brute force before optimising** (it is a correct answer you can fall back to, and it shows you what to optimise) and **write the plan as comments before code** (you can't lose your place, and the interviewer can follow you and correct you early).

### Constraints tell you the target complexity

Python does roughly 10⁷ simple steps per second. The input size tells you which complexity will pass, and that narrows down the technique. Google problems often state no sizes at all: ask, or state your assumption out loud.

| Input size n up to | Target | Usually means |
|---|---|---|
| 10–12 | O(n!) | permutations, backtracking over orders |
| 20–25 | O(2ⁿ) | subsets, bitmasks, backtracking with pruning |
| 100–500 | O(n³) | triple loops, Floyd-Warshall |
| 1 000–5 000 | O(n²) | all pairs, simple nested loops |
| 10⁵–10⁶ | O(n log n) or O(n) | sorting, heaps, binary search, two pointers, sliding window, hashing, BFS/DFS |
| a **value** (not a length) up to 10⁹–10¹⁸ | O(log V) or O(√V) | binary search on the answer, divisor or digit math |

### Clues → technique

Skim this table now; come back to it when a problem gives you no idea.

| If the problem says or implies … | Reach for | Section |
|---|---|---|
| "have I seen it before", pairs with a target, grouping, counting | hash map / set | [Arrays & Hashing](#s03) |
| contiguous subarray with a sum or count, negatives allowed | prefix sums + hash map | [Prefix Sums](#s04) |
| sorted array, pairs or triples, "in place", from both ends | two pointers | [Two Pointers](#s05) |
| longest / shortest / count of contiguous windows whose rule only gets *more* broken as the window grows (counts, distinct letters, sums of non-negatives) | sliding window | [Sliding Window](#s06) |
| matching brackets, nested structure, undo, evaluate expressions | stack | [Stacks & Queues](#s07) |
| next greater / smaller, spans, histograms, "remove digits to make it smallest" | monotonic stack | [Monotonic Stack](#s08) |
| sorted or rotated input, "minimum possible maximum", "smallest speed / capacity that works" | binary search (on the answer) | [Binary Search](#s09) |
| linked list rewiring, middle, cycle, k-th from the end | dummy head, fast/slow pointers | [Linked Lists](#s10) |
| hierarchy, recursion on children, BST, levels | DFS (return vs record) / BFS | [Trees](#s11) |
| prefixes, autocomplete, many words against one board | trie | [Tries](#s12) |
| top k, k-th largest, merge k sorted, running median, "always the cheapest next" | heap | [Heaps](#s13) |
| overlapping ranges, meetings, rooms, coverage | sort + sweep | [Intervals & Sweep Line](#s14) |
| a choice you can argue is never worse (earliest end first, farthest reach so far); "minimum jumps" along a line | greedy | [Greedy](#s15) |
| all combinations / permutations / partitions / placements | backtracking | [Backtracking](#s16) |
| grid regions, spreading, "minimum number of steps / moves" in an unweighted world | BFS / DFS | [Graphs I: BFS & DFS](#s17) |
| fewest moves when the state is more than the position (keys held, obstacles you may still remove, a board layout) | BFS over (position, extra) states | [Graphs I: BFS & DFS](#s17) |
| prerequisites, ordering, "are these connected", merging groups | topological sort / union-find | [Graphs II: Ordering & Connectivity](#s18) |
| weighted shortest path, cheapest network, "minimise the maximum effort on a path" | Dijkstra / MST (or binary search + BFS) | [Graphs III: Weighted Paths & MST](#s19) |
| parsing, palindromes, pattern matching | string toolbox | [Strings](#s20) |
| rotate, spiral, in-place grid updates | index arithmetic | [Matrices](#s21) |
| parity, powers of two, subsets as bits, gcd, primes | bits and math | [Math, Bits & Geometry](#s22) |
| a custom order, "arrange to form the largest", k-th smallest without sorting everything | sort with `key=` / `cmp_to_key`, quickselect | [Sorting & Selection](#s23) |
| "design a class that supports …", "implement a tracker" | operations → data structures | [Design Problems](#s24) |

### When no clue fits

1. **Solve a tiny example by hand** and notice what you write down while doing it. That is your state.
2. **Write the brute force**, then ask which work it repeats; the structure that remembers that work is your optimisation.
3. **Change the representation**: sort it, take prefix sums, turn it into a graph, process it backwards, or count the complement.
4. **Fix one thing and optimise the other**: "for every right end, what is the best left?", "for every candidate answer, is it feasible?"
