---
name: algorithm-books
description: "algorithm_books/ (150 algorithms, pseudocode + Python PDFs) and system_design_book/ (50 designs, one PDF): ranked by importance, built with pandoc + lualatex; how to extend and rebuild"
metadata:
  node_type: memory
  type: project
  originSessionId: 2a1dc6c0-b859-4815-b9c7-507d86ff5c51
  modified: 2026-10-12T09:11:06.058Z
---

Built 2026-10-12 at the user's request. Scope grew during the session: about 100 algorithms, then 120 ("total 120"), then 150 with at least 30 designs. The user then asked for a 50-chapter system design book from a ranked outline.

**algorithm_books/**
- `manifest.json`: 150 entries with rank, tier (three tiers of 50: Must Know Cold / Should Know Well / Good to Know), topic, title, subtitle and brief. 32 of them are Design.
- `pseudo/NNN_slug.md`: flowing prose, then a ```text picture, then ```pseudo, then a closing paragraph and a *Practice:* line of LC problems.
- `python/NNN_slug.py`: simple-Python rules from SPEC.md, with a `# --- try it ---` demo whose `# -> expected` comments are checked.
- `check.py <ranks>` validates every entry.
- `build.py` writes `150_Algorithms_Pseudocode.pdf`, `150_Algorithms_Python.pdf` and `algorithms.txt` at the repo root.
- "#N" in prose links to entry N. Renumbering means remapping those references in prose and comments, never in strings or demo outputs.
- The user's fixed counts are 5 sorting, 5 DFS, 5 backtracking, 10 greedy, 10 strings, 2 shortest path, 2 MST; keep them when adding entries.

**system_design_book/**
- `manifest.json`: 50 designs with tiers of 17, 17 and 16.
- `chapters/NN_slug.md` follows the 11-part template in SPEC.md, with ```dot Graphviz bodies that use `class=client|service|edge|cache|store|queue|worker|external`.
- `diagrams.py` handles styling and layout stats; `check.py` validates chapters.
- `build.py` writes `50_System_Designs.pdf` and `system_designs.txt`. "#N" points into the 150-algorithm books and "Chapter N" links within the book.
- Graphviz was installed via brew with the user's permission.

**Why:** Google interview prep; the user wants ranked, printable books in the flowing-prose style ([[writing-style-flowing-prose]]).

**How to apply:** To add or change an entry, edit the manifest and the files per SPEC.md, run check.py, then run build.py. Verify PDFs through LaTeX logs, never by viewing images ([[feedback-no-image-verification]]).
