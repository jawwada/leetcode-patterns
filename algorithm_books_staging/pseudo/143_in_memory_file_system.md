---
rank: 143
slug: in_memory_file_system
---

Design a file system that lives in memory and answers four calls on absolute paths such as `/a/b/c`. `mkdir(path)` creates the directory and every missing directory above it; `add_content_to_file(path, content)` creates the file if needed and appends the content; `read_content_from_file(path)` returns what the file holds; and `ls(path)` returns the sorted names inside a directory, or a one-item list with the file's own name when the path is a file. After `mkdir("/a/b/c")` and `add_content_to_file("/a/b/c/d", "hello")`, `ls("/")` is `["a"]`, `ls("/a/b/c/d")` is `["d"]`, and reading `/a/b/c/d` gives `"hello"`.

The brute force is a flat map from full path to content. Creating and reading are single lookups, but `ls` must scan every stored path for the ones exactly one level below, `O(P · L)` for `P` paths of length `L`. A directory tree is already a trie, the trie of #43 with whole names on the edges instead of letters. Each node holds a map from child name to child node, an `is_file` flag and the file's content, and the children of a directory node are exactly its listing, so `ls` reads them off and sorts them. Every call splits the path on `/` and walks down from the root one name at a time. Splitting `/a/b/c/d` gives `['', 'a', 'b', 'c', 'd']`; the empty string before the leading slash is skipped, as is any left by a trailing or doubled slash, which makes `/` itself the empty walk that stays at the root.

One walk serves all four calls, with a single switch. `mkdir` and `add_content_to_file` walk with `create` on, so every missing name becomes a fresh node on the way down and `mkdir("/a/b/c")` builds the whole chain in one pass. `ls` and `read_content_from_file` walk with `create` off and stop at the first missing name, so asking about a path never brings it into existence. A file is a node like any other with its flag set. When `ls` lands on one, it answers with the last name of the path, because a node does not store its own name; its parent's map does.

```text
mkdir("/a/b/c"), add "hello" then " world" to /a/b/c/d,
mkdir("/a/b/apps"), add "todo" to /a/notes:

root
└── a
    ├── b
    │   ├── c
    │   │   └── d        file: "hello world"
    │   └── apps
    └── notes            file: "todo"

ls("/a/b")      [a, b]: root → a → b, a directory → sorted children
                stored in insertion order c, apps → ['apps', 'c']
ls("/a/b/c/d")  [a, b, c, d]: ends on a file → its own name ['d']
ls("/a")        ['b', 'notes']: files and directories list alike
```

```pseudo
CLASS FileNode
    FUNCTION Init()
        self.children ← empty map           // name → FileNode
        self.is_file ← false
        self.content ← ""

FUNCTION SplitPath(path)
    names ← empty list
    FOR EACH part IN path.split("/")
        IF part ≠ ""                        // '/' at the start or end leaves ''
            names.append(part)
    RETURN names

CLASS FileSystem
    FUNCTION Init()
        self.root ← new FileNode()

    FUNCTION Walk(path, create)
        node ← self.root
        FOR EACH name IN SplitPath(path)
            IF name NOT IN node.children
                IF NOT create
                    RETURN null             // the path does not exist
                node.children[name] ← new FileNode()
            node ← node.children[name]
        RETURN node

    FUNCTION Ls(path)
        node ← self.Walk(path, false)
        IF node = null
            RETURN empty list
        IF node.is_file
            names ← SplitPath(path)
            RETURN [names[-1]]              // the last name in the path
        RETURN sorted(node.children)        // the child names, in order

    FUNCTION Mkdir(path)
        self.Walk(path, true)

    FUNCTION AddContentToFile(path, content)
        node ← self.Walk(path, true)
        node.is_file ← true
        node.content ← node.content + content

    FUNCTION ReadContentFromFile(path)
        node ← self.Walk(path, false)
        IF node = null
            RETURN ""
        RETURN node.content
```

Every call visits one node per name, so it costs `O(L)` for a path of `L` names plus the characters read while splitting it; `ls` on a directory adds `O(k log k)` to sort its `k` children, and the tree holds one node per directory or file. Appending copies the old content, since Python strings are immutable, so a file grown by many small appends would keep a list of chunks and join them on read. Deleting a directory is one removal from its parent's map, which drops the whole subtree at once. Reach for a trie of tokens whenever keys are paths: file systems, URL routers, nested configuration keys. Design File System (LC 1166) is the strict cousin, where creating a path succeeds only if its parent exists and the path does not, which is the walk with `create` off for all but the last name; Simplify Path (LC 71) splits the same way and keeps the names on a stack, popping on `..` and skipping `.`. The classic mistake is treating every path in `ls` as a directory: `ls("/a/b/c/d")` must return `["d"]`, the file's own name, not the children of the file's node, which are none.

*Practice:* LC 588 Design In-Memory File System · LC 1166 Design File System · LC 71 Simplify Path
