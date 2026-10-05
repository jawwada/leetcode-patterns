"""
Design In-Memory File System (LeetCode 588) - Hard
Chapter: design
Pattern: Trie of directories (path components as edges)

Implement FileSystem with: ls(path), which returns the sorted names inside a directory, or
[filename] if path is a file; mkdir(path), which creates every missing directory;
addContentToFile(path, content), which creates the file or appends to it; and
readContentFromFile(path).
Example: mkdir("/a/b/c"); addContentToFile("/a/b/c/d","hello"); ls("/") returns ["a"] and
readContentFromFile("/a/b/c/d") returns "hello".
"""


# --- helpers ---
def components(path):
    """'/a/b/c' -> ['a', 'b', 'c'] (the split leaves an empty string before the leading '/')."""
    parts = []
    for part in path.split("/"):
        if part != "":
            parts.append(part)
    return parts


def last_name(path):
    """'/a/b/c' -> 'c'."""
    parts = components(path)
    return parts[-1]


# --- brute force ---
class BruteForce:
    """Flat dict full path -> content (None for a directory); ls scans every path. O(P*L) ls."""

    def __init__(self):
        self.entries = {"/": None}

    def ensure_dirs(self, path):
        parts = components(path)
        for i in range(1, len(parts) + 1):    # every prefix of the path is a directory
            prefix = "/" + "/".join(parts[:i])
            if prefix not in self.entries:
                self.entries[prefix] = None

    def ls(self, path):
        if self.entries.get(path) is not None:
            return [last_name(path)]          # a file: just its own name
        prefix = path.rstrip("/") + "/"
        names = []
        for stored in self.entries:           # every stored path, every ls
            if stored.startswith(prefix) and stored != prefix:
                rest = stored[len(prefix):]
                if "/" not in rest:           # a direct child, not a grandchild
                    names.append(rest)
        return sorted(names)

    def mkdir(self, path):
        self.ensure_dirs(path)

    def addContentToFile(self, filePath, content):
        parts = components(filePath)
        self.ensure_dirs("/" + "/".join(parts[:-1]))
        if self.entries.get(filePath) is None:
            self.entries[filePath] = ""
        self.entries[filePath] += content

    def readContentFromFile(self, filePath):
        return self.entries[filePath]


# --- optimal ---
class Node:
    def __init__(self):
        self.children = {}                    # name -> Node
        self.content = None                   # None = directory, a string = file


class FileSystem:
    """Trie keyed by path component; walking a path is one dict lookup per level. O(L) per op."""

    def __init__(self):
        self.root = Node()

    def walk(self, path):
        node = self.root
        for part in components(path):
            if part not in node.children:
                node.children[part] = Node()  # creates the missing directories on the way
            node = node.children[part]
        return node

    def ls(self, path):
        node = self.walk(path)
        if node.content is not None:
            return [last_name(path)]          # a file: list just its own name
        return sorted(node.children)          # the children ARE the listing

    def mkdir(self, path):
        self.walk(path)

    def addContentToFile(self, filePath, content):
        node = self.walk(filePath)
        if node.content is None:
            node.content = ""                 # a fresh file
        node.content += content

    def readContentFromFile(self, filePath):
        return self.walk(filePath).content


# --- try the brute force ---
fs = BruteForce()
print(fs.ls("/"))                            # -> []
fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
print(fs.ls("/"))                            # -> ['a']
print(fs.readContentFromFile("/a/b/c/d"))    # -> hello
fs.addContentToFile("/a/b/c/d", " world")    # appends to the existing file
print(fs.readContentFromFile("/a/b/c/d"))    # -> hello world
print(fs.ls("/a/b/c/d"))                     # -> ['d']
fs.mkdir("/a/b/a")
print(fs.ls("/a/b"))                         # -> ['a', 'c']
print(fs.ls("/a/b/c"))                       # -> ['d']


# --- try the optimal ---
fs = FileSystem()
print(fs.ls("/"))                            # -> []
fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
print(fs.ls("/"))                            # -> ['a']
print(fs.readContentFromFile("/a/b/c/d"))    # -> hello
fs.addContentToFile("/a/b/c/d", " world")    # appends to the existing file
print(fs.readContentFromFile("/a/b/c/d"))    # -> hello world
print(fs.ls("/a/b/c/d"))                     # -> ['d']
fs.mkdir("/a/b/a")
print(fs.ls("/a/b"))                         # -> ['a', 'c']
print(fs.ls("/a/b/c"))                       # -> ['d']
