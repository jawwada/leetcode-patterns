"""
Design In-Memory File System (LeetCode 588)  — Hard
Pattern: Trie of directories (path components as edges)

Problem
-------
Implement FileSystem with: ls(path) -> sorted names directly inside the
directory, or [filename] if path is a file; mkdir(path) creating every
missing directory on the way; addContentToFile(path, content) creating
the file if needed and appending otherwise; readContentFromFile(path).
Paths are absolute, "/" is the root, components are lowercase letters.
Example: ls("/") -> []; mkdir("/a/b/c"); addContentToFile("/a/b/c/d",
"hello"); ls("/") -> ["a"]; readContentFromFile("/a/b/c/d") -> "hello".

Brute force
-----------
A flat dict full_path -> content (None for directories). mkdir inserts
every prefix path; add/read index the dict directly. ls(path) must find
the direct children: scan all P stored paths, keep those that start with
path + "/" and contain no further "/", strip the prefix and sort.
O(P * L) per ls, O(P * L) space. The wasted work is the scan: every ls
touches every path in the system, and every mkdir/add re-hashes long
path strings whose prefixes are already known to exist.

From brute force to optimal
---------------------------
A path is a sequence of components, and every component after the first
is only meaningful relative to its parent, which is exactly a trie keyed
by component instead of by character. Each node is a directory with a
dict name -> child, or a file with a content string. Walking a path costs
one dict lookup per component (O(L) total) and lands on the node that ls,
add and read need; the children of a directory node ARE its ls result,
so no scan is needed, only a sort of that one directory's names. mkdir
and addContentToFile share the same walk with setdefault, which creates
missing directories on the way. The invariant is that the trie mirrors
the directory tree one-to-one: a node is a file iff its content is not
None.

Intuition
---------
A file system is already a tree; representing it as one makes every
operation a path walk followed by O(1) work at the destination node. The
only non-constant step is sorting a directory's names for ls, which the
problem requires.

Geometric view
--------------
Draw the trie as a branching diagram rooted at "/": edges are directory
or file names, internal nodes are folders holding a dict, leaves marked
with content are files. ls on a folder reads the labels of its outgoing
edges; mkdir extends a chain of edges downward; addContentToFile walks
to a leaf and lengthens its content string.

Steps
-----
1. Node: children dict, content = None (directory) or str (file).
2. _walk(path): split on "/", skip empty parts, descend via
   setdefault(part, Node()) so missing directories are created.
3. ls: node = _walk(path); if node.content is not None return
   [last component]; else return sorted(node.children).
4. mkdir: _walk(path).
5. addContentToFile: node = _walk(path); node.content =
   (node.content or "") + content.
6. readContentFromFile: return _walk(path).content.

Complexity: O(L) per mkdir/add/read, O(L + k log k) per ls, O(total
components + content) space — each op walks one component per level; ls
additionally sorts the k names in that directory.
Pitfalls: splitting "/" into [""] and creating a node named ""; ls of a
file must return just the file name, not the full path; appending to
content must create the file when absent; returning children unsorted.
"""
from typing import Dict, List, Optional


class _Node:
    __slots__ = ("children", "content")

    def __init__(self):
        self.children: Dict[str, "_Node"] = {}
        self.content: Optional[str] = None        # None = directory, str = file


class FileSystem:
    def __init__(self):
        self.root = _Node()

    def _walk(self, path: str) -> _Node:
        node = self.root
        for part in path.split("/"):
            if part:                               # skip the empty component before the leading "/"
                node = node.children.setdefault(part, _Node())   # creates missing directories
        return node

    def ls(self, path: str) -> List[str]:
        node = self._walk(path)
        if node.content is not None:               # a file: list just its own name
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)

    def mkdir(self, path: str) -> None:
        self._walk(path)

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath)
        node.content = (node.content or "") + content

    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath).content or ""


class BruteForce:
    """Flat dict full_path -> content (None for dirs); ls scans every stored path: O(P*L)."""

    def __init__(self):
        self.entries: Dict[str, Optional[str]] = {"/": None}

    def _ensure_dirs(self, path: str) -> None:
        parts = [p for p in path.split("/") if p]
        for i in range(1, len(parts) + 1):
            self.entries.setdefault("/" + "/".join(parts[:i]), None)

    def ls(self, path: str) -> List[str]:
        if self.entries.get(path) is not None:
            return [path.rsplit("/", 1)[-1]]
        prefix = path.rstrip("/") + "/"
        names = [p[len(prefix):] for p in self.entries                 # full scan of every path
                 if p.startswith(prefix) and p != prefix and "/" not in p[len(prefix):]]
        return sorted(names)

    def mkdir(self, path: str) -> None:
        self._ensure_dirs(path)

    def addContentToFile(self, filePath: str, content: str) -> None:
        self._ensure_dirs(filePath.rsplit("/", 1)[0])
        self.entries[filePath] = (self.entries.get(filePath) or "") + content

    def readContentFromFile(self, filePath: str) -> str:
        return self.entries.get(filePath) or ""


if __name__ == "__main__":
    import random

    fs = FileSystem()
    assert fs.ls("/") == []
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    assert fs.ls("/") == ["a"]
    assert fs.readContentFromFile("/a/b/c/d") == "hello"
    fs.addContentToFile("/a/b/c/d", " world")                # append to an existing file
    assert fs.readContentFromFile("/a/b/c/d") == "hello world"
    assert fs.ls("/a/b/c/d") == ["d"]                        # ls of a file is just its name
    fs.mkdir("/a/b/a")
    assert fs.ls("/a/b") == ["a", "c"]                       # sorted names
    assert fs.ls("/a/b/c") == ["d"]

    rng = random.Random(588)
    fast, slow = FileSystem(), BruteForce()
    dirs, files = ["/"], []
    for _ in range(400):
        op = rng.random()
        parent = rng.choice(dirs)
        path = parent.rstrip("/") + "/" + rng.choice("abc")
        if op < 0.3:
            deep = path + "/" + rng.choice("xyz")
            fast.mkdir(deep)
            slow.mkdir(deep)
            dirs += [path, deep]
        elif op < 0.6:
            text = rng.choice("pq")
            fast.addContentToFile(path + ".f", text)       # files are named <letter>.f, never a dir
            slow.addContentToFile(path + ".f", text)
            files.append(path + ".f")
        elif op < 0.8 and files:
            f = rng.choice(files)                          # only existing files are read, as on LeetCode
            assert fast.readContentFromFile(f) == slow.readContentFromFile(f), f
        else:
            assert fast.ls(parent) == slow.ls(parent), parent
    print("ok")
