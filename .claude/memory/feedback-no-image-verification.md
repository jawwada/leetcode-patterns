---
name: feedback-no-image-verification
description: "Don't verify work by rendering pages/diagrams to images and viewing them; costly in tokens. Use text checks (layout stats, LaTeX logs, linters)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2a1dc6c0-b859-4815-b9c7-507d86ff5c51
  modified: 2026-10-12T09:05:03.305Z
---

Do not verify documents, PDFs or diagrams by rendering them to PNG and reading the images, and do not ask subagents to do so.

**Why:** On 2026-10-12, while building the algorithm and system design books, the user said: "do not do image based verification, that is very costly in tokens".

**How to apply:** Verify with text instead. For Graphviz, read the size and node/edge counts from `dot -Tplain`. For LaTeX/PDF, compile and grep the log for "Missing character" and "Overfull \hbox". Otherwise rely on checkers and linters. Tell workflow agents explicitly that image previews are off-limits. Related: [[algorithm-books]].
