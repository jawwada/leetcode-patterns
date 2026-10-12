---
rank: 36
slug: serialize_binary_tree
---

Turn a binary tree into a string, and turn that string back into the very same tree. For `[1, 2, 3, null, null, 4, 5]`, a root `1` with children `2` and `3` where `3` has children `4` and `5`, writing the values in preorder with `#` for every missing child gives `"1,2,#,#,3,4,#,#,5,#,#"`, and reading that string rebuilds the tree.

A bare preorder listing is ambiguous: `1, 2` could be a root with a left child `2` or a root with a right child `2`, and nothing in the list tells them apart. What is lost is where each subtree ends, and the null marker puts it back. With a `#` for every empty child, a value token is always followed by exactly two complete subtrees and a `#` is a complete subtree on its own, so the two trees above become the different strings `1,2,#,#,#` and `1,#,2,#,#`. A tree with `n` nodes has `n + 1` empty children, so the string holds `2n + 1` tokens.

Decoding replays the encoding. A shared index moves left to right through the tokens; each call reads one token, returns null for `#`, and otherwise builds the node and calls itself twice, first for the left subtree, then for the right. The left call eats exactly the tokens of the left subtree and stops, leaving the index on the first token of the right subtree, and that is the whole trick: in preorder every subtree is one unbroken block of tokens, its value first, then its left block, then its right block.

```text
      1     tokens  1  2  #  #  3  4  #  #  5  #  #
     / \    index   0  1  2  3  4  5  6  7  8  9 10
    2   3                          └──4──┘  └──5──┘
       / \             └──2──┘  └────────3────────┘
      4   5         └──────────────1──────────────┘
the read for 3 starts at index 4 because the read for 2 stopped after index 3
```

```pseudo
FUNCTION Serialize(root)
    tokens ← empty list
    Write(root, tokens)
    RETURN join(tokens, ",")

FUNCTION Write(node, tokens)
    IF node = null
        tokens.append("#")                 // the marker closes a branch
        RETURN
    tokens.append(str(node.val))
    Write(node.left, tokens)
    Write(node.right, tokens)

FUNCTION Deserialize(data)
    tokens ← split(data, ",")
    index ← [0]                            // one box all the calls share
    RETURN Read(tokens, index)

FUNCTION Read(tokens, index)
    token ← tokens[index[0]]
    index[0] ← index[0] + 1
    IF token = "#"
        RETURN null
    node ← new TreeNode(int(token))
    node.left ← Read(tokens, index)        // the left subtree eats its tokens
    node.right ← Read(tokens, index)       // the right one starts after them
    RETURN node
```

Both directions handle each node and each marker once, so they run in `O(n)` time, with an `O(n)` string and `O(h)` recursion depth. The commas matter: they keep `12` apart from `1` and `2` and let negative values parse with no extra rule. Reach for this whenever a tree must leave memory, to a file, across a network, or into a hash map that spots duplicate subtrees. A binary search tree needs no markers, because its values already say where the left subtree ends, at the first value larger than the root. Without markers a general tree needs a second traversal, which is how it is rebuilt from its preorder and inorder sequences together. The classic mistake is passing the index as a plain integer: each call advances its own copy, the caller never learns how many tokens its left subtree consumed, and the right subtree reads them all over again.

*Practice:* LC 297 Serialize and Deserialize Binary Tree · LC 449 Serialize and Deserialize BST · LC 105 Construct Binary Tree from Preorder and Inorder Traversal
