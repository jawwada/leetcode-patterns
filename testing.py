# ─────────────────────────────────────────────────────────────
# 1. GRAPH DFS — recursive, adjacency list + visited set
# ─────────────────────────────────────────────────────────────
x=5

# define the dfs function: current node, the graph (adjacency list), the visited set
def dfs(node, graph:dict, visited:set):
    
    # mark the current node as visited so we never process it twice
    visited.add(node)
    print(visited)

    # (optional) do the work for this node here — record it, print it, add to a result

    # loop over every neighbor of the current node in the graph
    for v in G.get(node,[]):
        
        # if this neighbor hasn't been visited yet
        if v not in visited:
            print ("recursing into",+int(v))
            # recurse into it, carrying the same graph and visited set
            dfs(v,G,visited)
    return
            
            
                    

# --- test ---
# build a small graph as a dict mapping each node to its list of neighbors
G= {1:[2,3,4], 2: [3,1],3:[1,2]}

# create an empty set to track visited nodes
visited = set()

# call dfs starting from node 0, passing the graph and the visited set
dfs(1,G,visited)
# print the visited set to confirm every reachable node was explored


# ─────────────────────────────────────────────────────────────
# 2. GRID / MATRIX DFS — recursive, 4-directional (e.g. islands)
# ─────────────────────────────────────────────────────────────

# define the dfs function: the grid, and the current row r and column c

    # base case: if (r, c) is off the grid (row/col out of bounds), return

    # base case: if this cell is water / already visited / not the target value, return

    # mark this cell as visited — flip it in place or add (r, c) to a visited set

    # recurse up    (r - 1, c)

    # recurse down  (r + 1, c)

    # recurse left  (r, c - 1)

    # recurse right (r, c + 1)

# --- test ---
# build a small 2D grid as a list of lists (e.g. 1 = land, 0 = water)

# call dfs from a known land cell, e.g. row 0, col 0

# print the grid afterwards to confirm the connected land was flipped/marked

##!


# ─────────────────────────────────────────────────────────────
# 3. BINARY TREE DFS — recursive traversal
# ─────────────────────────────────────────────────────────────

# define a Node class with a value and left/right child pointers
class TreeNode():

    # constructor: store the value, default left and right children to None
    def __init__(self,val:int):
        self.val = val
        self.left = None
        self.right = None

# define the dfs function: the current node
def dfs(node:TreeNode):
    # base case: if the node is None, return (nothing to explore)
    if node is None:
        return
    else:
        print("recursing into" + str(node.val))
    dfs(node.left)
    print("coming back from:" +str(node.val))
    dfs(node.right)

# --- test ---
# build a small tree by creating the root node and attaching children
node = TreeNode(7)
node.left = TreeNode(3)
node.right = TreeNode(5)
node.left.left=TreeNode(1)
node.left.right=TreeNode(0)
node.right.left=TreeNode(4)
node.right.right=TreeNode(2)


# call dfs on the root to traverse the whole tree
dfs(node)

# (printing happens inside dfs, so the traversal order shows up in the output)


# ─────────────────────────────────────────────────────────────
# 4. ITERATIVE DFS — explicit stack, no recursion
# ─────────────────────────────────────────────────────────────

# define the dfs function: the graph and the starting node

    # create a visited set to track nodes we've already handled

    # initialize the stack with the starting node

    # loop while the stack still has nodes to explore

        # pop a node off the top of the stack

        # if we've already visited this node, skip it and continue

        # mark the node as visited

        # (optional) do the work for this node here

        # loop over the node's neighbors

            # if a neighbor hasn't been visited, push it onto the stack

    # return the visited set once the stack is empty

# --- test ---
# reuse (or build) a small adjacency-list graph

# call dfs starting from node 0 and capture the returned visited set

# print the result to confirm every reachable node was visited
