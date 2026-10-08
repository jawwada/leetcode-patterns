**From idea to implementation.** Most interview failures are not "I had no idea". They are "I had the idea and could not turn it into code in 25 minutes". This playbook is about that gap.

Every technique is taught the same way: the picture, then the **seven decisions** that turn the idea into lines of code, then the traps, the edge cases and the variations, and finally a map of every problem in this repo that uses it.

The playbook has one notebook per topic. Use the [topic index](00_Topic_Index.ipynb#notebooks) to choose a lesson. [From Idea to Code](02_Idea_to_Code.ipynb) and [Python Toolkit](03_Python_Toolkit.ipynb) are separate notebooks, as are each graph technique and tracker API. [Interview Checklists](67_Interview_Checklists.ipynb) and the [A–Z finder](68_Problem_Finder.ipynb#finder) are reference notebooks.

<!-- cell -->

## Start Here

### How to read a section

Every technique section has the same shape, so you always know where to look. It opens with **Reach for it when**, the words in a problem statement that should make you think of this technique. **The picture** then draws the data and the motion of the algorithm over it, and says why it beats brute force.

**From idea to code** is the heart of the section: the idea in one sentence, the seven decisions answered for this technique, and a template whose lines are tagged with the decision they come from. After every code cell, **Try it** gives three or four small experiments that break one line on purpose or feed a tricky input.

The second half of a section makes the code hold. **Watch it work** prints the state step by step. **Where it goes wrong** lists the implementation traps, each with a tiny failing input and its fix, and **Edge cases** are the inputs to say out loud, as runnable asserts. **Variations** say what changes from the template for each family of problems, and they end with a second pass: Hard problems that reuse the same moves.

**Say it in the interview** is a short script: brute force, its waste, the optimal idea, the complexity, and the likely follow-ups. The **Problem map** lists every repo problem that uses the technique, with its one key insight. Sorting & Selection has no topic folder, so its problems are mapped under their home sections. **Self-check** closes with questions whose answers stay hidden until you click.

A section takes 60 to 90 minutes to study properly, and those minutes are for the main path; the second pass waits until the main path is automatic. Run each cell. Do its Try-it bullets as *predict → run → explain → undo*: say what will happen before you run it. Answer each Self-check question before opening it.

Then close the notebook and type the template from its seven decisions in a plain editor, with no autocomplete and no running, and only then run it. The decision where you stalled is the one to reread.

Start with **[From Idea to Code](02_Idea_to_Code.ipynb#topic-idea-to-code)**: it is the method every other section applies.

### The interview loop (45 minutes)

The method only pays off inside the 45 minutes you get, so here is how they are usually spent. The seven decisions are step 4.

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

Two habits matter more than speed. **Say the brute force before optimising**: it is a correct answer you can fall back to, and it shows you what to optimise. **Write the plan as comments before code**: you cannot lose your place, and the interviewer can follow you and correct you early.

### Constraints tell you the target complexity

Step 2 of the loop starts with the input size, because the size decides which complexity will pass, and that narrows down the technique. Python does roughly 10⁷ simple steps per second. For n = 10⁵, an O(n²) solution is 10¹⁰ steps, about a quarter of an hour; an O(n log n) solution is under 2 million steps, a fraction of a second. Google problems often state no sizes at all: ask, or state your assumption out loud.

| Input size n up to | Target | Usually means |
|---|---|---|
| 10–12 | O(n!) | permutations, backtracking over orders |
| 20–25 | O(2ⁿ) | subsets, bitmasks, backtracking with pruning |
| 100–500 | O(n³) | triple loops, Floyd-Warshall (all-pairs shortest paths) |
| 1 000–5 000 | O(n²) | all pairs, simple nested loops |
| 10⁵–10⁶ | O(n log n) or O(n) | sorting, heaps, binary search, two pointers, sliding window, hashing, BFS/DFS |
| a **value** (not a length) up to 10⁹–10¹⁸ | O(log V) or O(√V) | binary search on the answer, divisor or digit math |

### Clues → technique

The second half of Match is the wording: the words of a statement point at a technique. Skim this table now, and come back to it whenever a problem gives you no idea.

| If the problem says or implies … | Reach for | Section |
|---|---|---|
| "have I seen it before", pairs with a target, grouping, counting | hash map / set | [Arrays & Hashing](04_Hash_Maps_and_Sets.ipynb#topic-hash-maps-and-sets) |
| contiguous subarray with a sum or count, negatives allowed | prefix sums + hash map | [Prefix Sums](05_Prefix_Sums.ipynb#topic-prefix-sums) |
| sorted array, pairs or triples, "in place", from both ends | two pointers | [Two Pointers](06_Two_Pointers.ipynb#topic-two-pointers) |
| longest / shortest / count of contiguous windows whose rule only gets *more* broken as the window grows (counts, distinct letters, sums of non-negatives) | sliding window | [Sliding Window](07_Sliding_Window.ipynb#topic-sliding-window) |
| matching brackets, nested structure, undo, evaluate expressions | stack | [Stacks & Queues](00_Topic_Index.ipynb#s07) |
| next greater / smaller, spans, histograms, "remove digits to make it smallest" | monotonic stack | [Monotonic Stack](10_Monotonic_Stack.ipynb#topic-monotonic-stack) |
| sorted or rotated input, "minimum possible maximum", "smallest speed / capacity that works" | binary search (on the answer) | [Binary Search](11_Binary_Search.ipynb#topic-binary-search) |
| linked list rewiring, middle, cycle, k-th from the end | dummy head, fast/slow pointers | [Linked Lists](12_Linked_Lists.ipynb#topic-linked-lists) |
| hierarchy, recursion on children, BST, levels | DFS (return vs record) / BFS | [Trees](13_Trees.ipynb#topic-trees) |
| prefixes, autocomplete, many words against one board | trie | [Tries](14_Tries.ipynb#topic-tries) |
| top k, k-th largest, merge k sorted, running median, "always the cheapest next" | heap | [Heaps](16_Heaps.ipynb#topic-heaps) |
| overlapping ranges, meetings, rooms, coverage | sort + sweep | [Intervals & Sweep Line](17_Intervals_and_Sweep_Line.ipynb#topic-intervals-and-sweep-line) |
| a choice you can argue is never worse (earliest end first, farthest reach so far); "minimum jumps" along a line | greedy | [Greedy](18_Greedy.ipynb#topic-greedy) |
| all combinations / permutations / partitions / placements | backtracking | [Backtracking](19_Backtracking.ipynb#topic-backtracking) |
| grid regions, spreading, "minimum number of steps / moves" in an unweighted world | BFS / DFS | [Graphs I](00_Topic_Index.ipynb#s17) |
| fewest moves when the state is more than the position (keys held, obstacles you may still remove, a board layout) | BFS over (position, extra) states | [Graphs I](00_Topic_Index.ipynb#s17) |
| prerequisites, ordering, "are these connected", merging groups | topological sort / union-find | [Graphs II](00_Topic_Index.ipynb#s18) |
| weighted shortest path, cheapest network, "minimise the maximum effort on a path" | Dijkstra / MST (or binary search + BFS) | [Graphs III](00_Topic_Index.ipynb#s19) |
| parsing, palindromes, pattern matching | string toolbox | [Strings](00_Topic_Index.ipynb#s20) |
| rotate, spiral, in-place grid updates | index arithmetic | [Matrices](37_Matrices.ipynb#topic-matrices) |
| parity, powers of two, subsets as bits, gcd, primes, digits and bases, slopes, a random pick from a stream | bits and math | [Math, Bits & Geometry](00_Topic_Index.ipynb#s22) |
| a custom order, "arrange to form the largest", k-th smallest without sorting everything | sort with `key=` / `cmp_to_key`, quickselect | [Sorting & Selection](00_Topic_Index.ipynb#s23) |
| "design a class that supports …", "implement a tracker" | operations → data structures | [Design Problems](00_Topic_Index.ipynb#s24) |
| "in how many ways", "the best total", where the same sub-question keeps coming back (stairs, robbers, coins, two strings) | dynamic programming, outside this interview: recognise it and say so | [Dynamic Programming](20_Dynamic_Programming.ipynb#topic-dynamic-programming) |

### When no clue fits

Solve a tiny example by hand and notice what you write down while doing it: that is your state. Then write the brute force and ask which work it repeats; the structure that remembers that work is your optimisation.

If neither moves you, change the representation: sort it, take prefix sums, turn it into a graph, process it backwards, or count the complement. Or fix one thing and optimise the other: "for every right end, what is the best left?", "for every candidate answer, is it feasible?"
