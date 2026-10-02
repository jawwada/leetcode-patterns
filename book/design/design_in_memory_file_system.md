# Design In-Memory File System

*LeetCode 588 · Hard · Pattern: Trie of directories (path components as edges) · Reading time ~10 min*

## What the problem is really asking

Build a toy file system that lives in memory. Paths look like `/a/b/c`. Four operations:

- `mkdir(path)`: create the directory, and every missing directory along the way (like `mkdir -p`).
- `addContentToFile(path, content)`: create the file if needed, then append content to it.
- `readContentFromFile(path)`: return the file's full content.
- `ls(path)`: if path is a directory, return the sorted names directly inside it; if it is a file, return a list
  holding just the file's name.

The answer objects are strings and sorted name lists. The data you maintain is a hierarchy. The difficulty is not any
clever algorithm; it is choosing a representation in which every operation is a direct walk instead of a search, and
getting the edge cases right (the root `/`, `ls` on a file, appending to a file that does not exist yet).

```text
mkdir("/a/b/c"); addContentToFile("/a/b/c/d", "hello")

the thing                 ls("/")          -> ["a"]
  /                       ls("/a/b/c")     -> ["d"]
  `-- a/                  ls("/a/b/c/d")   -> ["d"]
      `-- b/              read("/a/b/c/d") -> "hello"
          `-- c/
              `-- d  "hello"
```

## Do it by hand first

You have used a file system for years, so think about how you find `/a/b/c/d` in a file browser. You open the root,
click `a`, click `b`, click `c`, and there is `d`. At no point do you look at every file on the disk. At each level you
only choose among the children of the folder you are in.

```text
path "/a/b/c/d".split("/") = ["", "a", "b", "c", "d"]
                              ^ skip: empty before leading /

root --a--> [a] --b--> [b] --c--> [c] --d--> (file d)
 1 step     2 steps    3 steps    4 steps
```

Your hand kept a tree whose edges are labelled with names. Each folder knew its own children by name. That is a trie,
keyed by path component rather than by character.

## The first honest attempt

Store a flat dict from full path string to content: `"/a/b/c/d" -> "hello"`, and directories as keys with no content.
Read and append are a single dict lookup, which is good. `mkdir` must insert every prefix `"/a"`, `"/a/b"`, `"/a/b/c"`
separately. And `ls("/a")` has to scan every key in the dict, keep those that start with `"/a/"` and have no further
slash, and sort them.

```text
flat dict keys:
  /a  /a/b  /a/b/c  /a/b/c/d  /a/x  /a/m  /z  /z/q ...
ls("/a"): test every key
  /a      no (itself)
  /a/b    yes -> b
  /a/b/c  no (deeper)
  /a/b/c/d no (deeper)
  /a/x    yes -> x
  /a/m    yes -> m
  /z ...  no            <- scanned anyway
```

`ls` is O(total paths) per call, and every call rescans entries that have nothing to do with the directory asked
about. Also, prefix handling ("is `/ab` inside `/a`?") is a string-matching trap.

## The turning point

**Claim: a path's meaning is "this name, inside that parent", so the natural index is a tree where each node maps child
names to child nodes; then every operation is a walk of one dictionary lookup per component, and a directory's
`ls` answer is literally its key set.**

Build it with one node type:

- `children`: a dict from name to node.
- `content`: `None` for a directory, a string for a file.

```text
node layout (memory)

root: children {"a": A}         content None
A:    children {"b": B}         content None
B:    children {"c": C}         content None
C:    children {"d": D}         content None
D:    children {}               content "hello"
```

One helper does all the work: walk the path from the root, and for each non-empty component step into
`children[part]`, creating an empty node if it is missing. Python's `dict.setdefault(part, Node())` does "look up, or
insert and return" in one call.

Every operation is now a walk plus O(1) work at the destination:

- `mkdir(path)`: walk. The walk itself creates the missing directories.
- `addContentToFile(path, s)`: walk (creating the file node if new), then `content = (content or "") + s`.
- `readContentFromFile(path)`: walk, return `content`.
- `ls(path)`: walk. If the node is a file, return `[last component of path]`. Otherwise return
  `sorted(children)`. Only that one directory's names are sorted.

```text
ls("/a") after a few more operations:

A.children = {"b": B, "x": X, "m": M}
             sorted -> ["b", "m", "x"]
nothing outside A is looked at
```

Two details to say aloud in an interview. First, splitting `"/"` gives `["", ""]` and splitting `"/a/b"` gives
`["", "a", "b"]`, so skip empty components or you will create a child named `""`. Second, files and directories share
one node type; `content is None` is the test that distinguishes them. The problem guarantees operations are valid (no
reading a missing file, no `mkdir` on top of a file), so the walk can safely create as it goes.

Why is this the right shape rather than just a convenient one? Every operation in the problem is phrased relative to
a path, and a path is a chain of parent-child steps. A representation that stores those steps directly makes the
operations' cost depend only on the depth of the path and the size of the one directory involved, never on the size of
the whole file system. The flat dict made `ls` pay for every file anywhere; the tree makes it pay only for the siblings
it must return. That is the general lesson of hierarchical keys: store the hierarchy, and queries scoped to a subtree
touch only that subtree.

A last design choice worth naming: some solutions use two node classes, or store files in a separate dict on each
directory (`dirs` and `files`). That works and makes "is this a file?" a membership test, but it doubles the places a
name can live and invites bugs where a name is checked in one dict and created in the other. One node type with a
nullable content field keeps the walk uniform.

## Watch it work

Operations: `mkdir("/a/b/c")`, `addContentToFile("/a/b/c/d","hello")`, `ls("/")`, `ls("/a/b/c/d")`,
`addContentToFile("/a/b/c/d"," world")`, `addContentToFile("/a/x","hi")`, `mkdir("/a/m")`, `ls("/a")`,
`readContentFromFile("/a/b/c/d")`.

Frame 1: `mkdir("/a/b/c")`.

```text
parts: a, b, c        (empty first part skipped)
root {}       -> create a
A    {}       -> create b
B    {}       -> create c

/ --a--> A --b--> B --c--> C
```

Three lookups miss, so three directory nodes are created by the walk itself.

Frame 2: `addContentToFile("/a/b/c/d", "hello")`.

```text
walk a, b, c: all found
walk d: missing -> create D
D.content: None -> "" + "hello" = "hello"

/ - A - B - C - D("hello")
```

The same walk creates the file node; the append starts from the empty string.

Frame 3: `ls("/")` and `ls("/a/b/c/d")`.

```text
ls("/"):         walk nothing, node = root (dir)
                 sorted(root.children) = ["a"]
ls("/a/b/c/d"):  node = D, content not None (file)
                 return ["d"]  (last component)
```

The root is reached by a walk of zero steps; a file answers with its own name.

Frame 4: two appends and a mkdir.

```text
add "/a/b/c/d" " world": D.content = "hello world"
add "/a/x" "hi":         A gains X("hi")
mkdir "/a/m":            A gains M (dir)

/ - A -+- B - C - D("hello world")
       +- X("hi")
       +- M
```

Appends extend existing content; new names hang off the node where the walk ended.

Frame 5: `ls("/a")` and the final read.

```text
ls("/a"):  A is a dir, children {b, x, m}
           sorted -> ["b", "m", "x"]
read("/a/b/c/d"): walk 4 steps -> "hello world"
```

`ls` sorts three names, not the whole system; read is four dictionary lookups.

Across every frame, the tree mirrored the path structure exactly: each node's `children` held exactly the names
created inside it, and files were the nodes with non-`None` content.

## Why it is correct

Invariant: for every path p that has been created, walking p's components from the root reaches a unique node, and
that node's `children` keys are exactly the names created directly inside p; its `content` is `None` if p is a
directory and the concatenation of all appended strings if p is a file.

The walk with `setdefault` preserves this: a component that exists is followed; one that does not is created as an
empty directory, which is what `mkdir -p` semantics demand for intermediate components. `addContentToFile` then turns
the final node into a file by setting its content, and appending is string concatenation onto the existing content.
`ls` on a directory returns its children's names, sorted, which by the invariant is exactly the listing; on a file it
returns the last path component, which is the file's name. `read` returns the stored concatenation.

## Cost

Let L be the number of components in the path and k the number of entries in the listed directory.

- `mkdir`, `addContentToFile`, `readContentFromFile`: O(L) dictionary steps (plus the length of the content appended
  or returned).
- `ls`: O(L + k log k), the walk plus sorting one directory.
- Space: O(total number of nodes + total content length).

If `ls` is called very often on large directories, keep each directory's names in a sorted container so `ls` is
O(L + k) to read out.

## Variations you will meet

- **Implement Trie (Prefix Tree).** The same structure keyed by characters instead of path components; `startsWith` is
  a walk with no creation.
- **Simplify Path.** Treat `..` and `.` while walking: a stack of components, pop on `..`, ignore `.`. In a file system
  with parent pointers, `..` is just "go to parent".
- **Delete, move, size.** `rm` deletes `children[name]` from the parent node, which removes a whole subtree in O(1).
  Directory size is a post-order sum of content lengths, or a cached total updated along the path on every append.
- **Design Search Autocomplete System.** A trie where each node also stores the top-ranked completions below it;
  queries walk the typed prefix and read the answer at the destination.

## What to carry forward

If keys are paths, store them as a tree of dictionaries: every operation becomes a walk of one lookup per component,
and a directory's listing is just its children. The next and final problem, Design Skiplist, also builds a linked
structure of nodes by hand, but this time the job is ordering, and the trick is giving a sorted linked list express
lanes so a walk can skip ahead.
