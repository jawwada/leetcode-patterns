# LeetCode Playbook (sources)

The notebooks in `practice/LeetCode_Playbook/` are organized as **one topic per notebook**.
Start with [the topic index](../LeetCode_Playbook/00_Topic_Index.ipynb). There are separate
lessons for BFS, DFS, topological sort, union-find, Dijkstra, Prim, Kruskal, KMP/LPS,
and each tracker API, as well as the other playbook topics.

The editable sources are in `topics/`; `topics/manifest.json` sets their order, titles,
filenames, and topic anchors. The active notebook folder contains the topic lessons
and navigation notebooks.

```bash
uv run python practice/playbook/build.py          # build + run every code cell + embed outputs
uv run jupyter lab practice/LeetCode_Playbook/    # open them
python3 practice/playbook/build_html.py           # the one-page reading copy (artifact.html, not committed)
```

For durable lesson edits, edit `topics/*.md`; rebuilding replaces notebook files, including
notebook-only edits. Each notebook gets its own setup and executes in a fresh Python namespace.
The build fails on a code error or a broken internal notebook link. The index includes
links to the original section groups and to the archived notebooks.

To build into another directory without replacing your notebooks:

```bash
python3 practice/playbook/build_topics.py --out-dir /tmp/playbook
```

The old `NN_slug.md` files in this folder remain as reference sources for the combined
chapters. `build.py --only 06,07 --out /tmp/x.ipynb --folders stack,queues` still supports
checking those original sections in isolation. Default builds use `topics/`.

## File format

- One file per topic in `topics/`, `NN_slug.md`, normally starting with `## Title`.
- A ` ```python ` fence becomes a runnable code cell. Cells run top to bottom in one namespace, and the setup
  cell has already imported: `Counter, defaultdict, deque, OrderedDict, cmp_to_key, lru_cache, accumulate,
  combinations, permutations, product, bisect, heapq, math, random, string`. Define every other helper
  (`ListNode`, `TreeNode`, ...) inside your own section; never rely on another section's names.
- Other fences (` ```text `) are shown but not run: use them for ASCII pictures and pseudocode.
- A line `<!-- cell -->` splits a long markdown stretch into two cells.
- Seed randomness (`random.seed(0)`), keep every cell fast (< 1 s) and its output short (< ~25 lines).
- Print results explicitly, with the expected value in a trailing comment: `print(f(x))   # 7`.

## Section recipe (the model is `06_sliding_window.md`)

The playbook's purpose is **turning an idea into an implementation**. Every technique section follows this
order, and the "From idea to code" part is the heart of it.

1. `## Title`, a one-line mental model in a blockquote, **Reach for it when** (clues in the problem
   statement).
2. `### The picture`: an ASCII drawing of the data and the motion of the algorithm, then why it is fast
   (what work the brute force repeats and how the technique avoids it).
3. `### From idea to code`: the idea in one sentence; then the seven decisions (**State, Definition,
   Invariant, Step, Record, Init, Return**) written as one or two short, definitive paragraphs, each decision
   a sentence that flows into the next; then a short paragraph that states the problem the template solves
   (a tiny example), the idea, and leads into the code; then the template code cell(s), tagged so each
   decision points at its line: `# STATE`/`# INIT` on the
   structures (with their definition), `# STEP` on the line that folds the new item into the state (not on
   the loop header), `# FIX` on the loop that restores the invariant, `# RECORD` where the answer is updated,
   `# RETURN` on the return. The order of STEP, FIX and RECORD is itself a decision; say why.
4. `### Watch it work`: a small trace that prints the state per step (encouraged, keep it short).
5. `### Where it goes wrong`: numbered implementation traps, each with the fix and a tiny failing input.
6. `### Edge cases to say out loud`: one line of cases, then a code cell of asserts ending with
   `print("edge cases pass")`.
7. `### Variations`: a table (Variation | What changes from the template | Problems), then code cells for
   the most important variations, each introduced by one or two sentences of intuition.
8. `### Say it in the interview`: a short quoted script (brute force, its waste, the optimal idea,
   complexity), plus what to point at while coding.
9. `### Problem map`: `| Problem | Where | Key insight |`, one row per problem. It is a lookup index, which is
   why it is a table. **Where** holds backticked repo paths, e.g. `` `sliding_window/fruit_into_baskets.py` ·
   `practice/simple/09_x.py` ``. **Key insight** is the single idea that cracks the problem, in under ~20
   words. What a problem asks is never a column: it is said in the prose, right before the code that solves
   it. These rows feed the A-Z problem finder.
10. `### Self-check`: 2-4 questions with the answer in `<details><summary>Answer</summary>...</details>`.

**After every code cell** add a markdown block whose first line is `**Try it**`, then 3-4 bullets of
hands-on experiments that teach the main flow and the tricky points: break one line on purpose
(`if` vs `while`, `<` vs `<=`, swap two lines, record in the wrong place) and predict the failure, feed
an edge input, print the state at a chosen point, change a parameter and predict before running.
Any outcome you state must be true. `build.py` lists code cells that lack it.

## Voice

Gentle and learning-oriented: explain *why* before *how*, short paragraphs, concrete tiny examples, pictures
over prose. Write for someone who knows Python but freezes between "I know the idea" and "I know what to
type". Every claim in a code comment or table must be true; every code cell must run.

Flowing, like an essay, and definitive:
- Prose carries the argument; a table is only for lookups (the Problem map, the Variations overview, a
  complexity or index-map reference). Where a table would make an argument, write the paragraph instead.
- Every code cell is preceded by a short paragraph, two to five sentences, that states the problem in plain
  words with a tiny example, gives the idea, and leads into the code. No label and no heading above it.
- A problem is never only a name: on its first mention, half a sentence says what it asks.
- Short paragraphs, one idea each, linked so they flow; declarative sentences; no hedging, no stacked
  parentheses, no run of rhetorical questions; define a term where it lands (amortised, monotone, invariant).
- Headings only for the recipe's parts, never `####` sub-headings; a variation begins with a sentence that
  says why it comes next. Hard or rare material comes last in Variations, introduced by the same sentence
  everywhere: "The rest of this section is a second pass: Hard problems that reuse the same moves. Skip them
  until the main path is automatic."
- Link directly to the topic notebook and its explicit anchor; filenames and anchors are in
  `topics/manifest.json`. The topic index retains the original `sNN` family anchors for
  references that span more than one newly separated topic.
The notebook speaks in one voice: never mention reviewers, agents, drafts or revision history, and never
attribute an idea to anyone; fold every improvement into the text as if it had always been there.
