"""
Simplify Path (basics: stacks)
Return the canonical form of an absolute Unix path ('.' = stay, '..' = up one level, '//' = '/').
  "/a/./b/../../c/"  ->  "/c"

Idea: a stack holds the directory names from the root down to where we are.
      A name goes one level down (push), '..' goes one level up (pop), and the
      empty names (from '//' or a trailing '/') and '.' change nothing.

Pseudocode:
  stack = []
  for part in path.split("/"):
      if part == "" or part == ".": skip
      elif part == "..": pop, but only if the stack is not empty   # never above the root
      else: push part                                              # any other name, even '...'
  return "/" + "/".join(stack)

Time O(n), space O(n).
"""


def simplify_path(path):
    stack = []                           # directory names, root side at the bottom
    for part in path.split("/"):
        if part == "" or part == ".":    # '//', trailing '/' and '.' change nothing
            continue
        if part == "..":                 # one level up ...
            if stack:                    # ... but never above the root
                stack.pop()
        else:
            stack.append(part)           # one level down
    return "/" + "/".join(stack)


if __name__ == "__main__":
    print(simplify_path("/a/./b/../../c/"))  # /c
    print(simplify_path("/home//foo/"))      # /home/foo
    print(simplify_path("/../"))             # /
    print(simplify_path("/.../a/../b"))      # /.../b
