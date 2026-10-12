"""
In-Memory File System - A Trie of Path Components

Support ls(path), mkdir(path), add_content_to_file(path, content) and
read_content_from_file(path) on absolute paths like "/a/b/c". After
mkdir("/a/b/c") and add_content_to_file("/a/b/c/d", "hello"):
ls("/") -> ["a"], ls("/a/b/c/d") -> ["d"], read "/a/b/c/d" -> "hello".
"""


# --- helpers ---
class FileNode:
    def __init__(self):
        self.children = {}          # name -> FileNode
        self.is_file = False
        self.content = ""


def split_path(path):
    """'/a/b/c' -> ['a', 'b', 'c']: split on '/', skip empty parts. O(len)."""
    names = []
    for part in path.split("/"):
        if part != "":              # '/' at the start or end leaves ''
            names.append(part)
    return names


# --- algorithm ---
class FileSystem:
    """One node per directory or file; children are keyed by name.
    O(path length) per call, plus sorting the names for ls."""

    def __init__(self):
        self.root = FileNode()

    def walk(self, path, create):
        """Follow the names from the root; make missing nodes if create,
        else return None. O(path length)."""
        node = self.root
        for name in split_path(path):
            if name not in node.children:
                if not create:
                    return None         # the path does not exist
                node.children[name] = FileNode()
            node = node.children[name]
        return node

    def ls(self, path):
        """A file lists its own name, a directory its sorted children.
        O(path length + k log k) for k children."""
        node = self.walk(path, False)
        if node is None:
            return []
        if node.is_file:
            names = split_path(path)
            return [names[-1]]          # the last name in the path
        return sorted(node.children)    # the child names, in order

    def mkdir(self, path):
        """Create every missing directory on the path. O(path length)."""
        self.walk(path, True)

    def add_content_to_file(self, path, content):
        """Create the file (and its directories) if needed, then append.
        O(path length + file length): the string is copied."""
        node = self.walk(path, True)
        node.is_file = True
        node.content = node.content + content

    def read_content_from_file(self, path):
        """The file's content, or "" if there is no such file.
        O(path length)."""
        node = self.walk(path, False)
        if node is None:
            return ""
        return node.content


# --- try it ---
fs = FileSystem()
print(fs.ls("/"))                                   # -> []
fs.mkdir("/a/b/c")
fs.add_content_to_file("/a/b/c/d", "hello")
print(fs.ls("/"), fs.ls("/a/b/c"), fs.ls("/a/b/c/d"))   # -> ['a'] ['d'] ['d']
fs.add_content_to_file("/a/b/c/d", " world")        # appends
print(fs.read_content_from_file("/a/b/c/d"))        # -> hello world
fs.mkdir("/a/b/apps")
fs.add_content_to_file("/a/notes", "todo")
print(fs.ls("/a/b"), fs.ls("/a"))       # -> ['apps', 'c'] ['b', 'notes']
